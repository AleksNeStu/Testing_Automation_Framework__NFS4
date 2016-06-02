#!/usr/bin/python
# -*- coding: utf-8 -*-
r"""The test data generator for testing NFSv4 and ACLs (run via call parameters)

Opportunities:
--gu - Get list of users created for testing
--gg - Get list of groups created for testing
--gf - Get list of files created for testing
-u - Generate u users for testing
-g - Generate g groups for testing
-f - Generate f files for testing in -d dir
-p - Path to test dir or file for set ACEs
-m - Max count of ACEs for dir or file according of type of fs
-d - Path to export dir for creating -f files
-c - The number of loops in the test

LOCAL: python ./generator_p.py -g 60 --gg -u 76
REMOTE: cat ./generator_p.py | /usr/bin/rsh rhel python - -g 60 --gg -u 76

@Developed by AleksNeStu

"""

import random  						#Random variable generators
import commands	 					#Execute shell commands via os.popen() and return status, output
import re		 					#Support for regular expressions (RE)
from compiler.syntax import check
from optparse import OptionParser	#Parser for command line options
from time import strftime
import time
import os

class full_generator(object):


#Generate range for groups (group names, gid (7000 + g range) according input data "g - number of groups"
#GID - values between 0 and 999 are typically reserved for system accounts
	def create_groups_n(self, g):
		for i in range(1,g+1):
			gname = "nfs_group" + str(i)
			gid = str(7000 + i)
			self.create_groups(gname, gid)

#Generate groups according the data from "create_groups_n" [consistently in range]
#groupadd -f -g 7000(range) nfs_group(range)
# -f - force	-g GID
	def create_groups(self, gname, gid):
		cmd = commands.getoutput("/usr/sbin/groupadd -f -g " + gid + " " + gname)
		print "    Group: " + gname + " / GID: " + gid + " / has been created"
		if cmd != "":
			print "    Group: " + gname + " / GID: " + gid + " / with errors"
			print cmd

#Generate range for users (user names, uid (7000 + g range) according input data "u - number of users"
#UID - values between 0 and 999 are typically reserved for system accounts
	def create_users_n(self, u):
		# while len(self.groups_list) != options.g: # in order to tun "python generator_p.py -g ** --gg -u **"
		# 	print "wait"
		# else:
			for i in range(1,u+1):
				uname = "nfs_user" + str(i)
				uid = str(7000 + i)
				self.create_users(uname, uid)

#Generate users according the data from "create_users_n" [random group select]
#useradd -f -g 7000(range) nfs_group(range)
#UID The numerical value of the user's ID.
#useradd -g "random_from_exist" -m uname -u uid -p nfs
#-g - the group name for a new user's initial group
#-m - create the user's home directory and new user name
#-u - UID
#-p - the encrypted password
 	def create_users(self, uname, uid):
		rgname = self.groups_list[random.randint(0, len(self.groups_list) - 1)][0]  #random select from  the previous created groups
		cmd = commands.getoutput("/usr/sbin/useradd " + "-g " + rgname + " -p nfs" + " -m " + uname + " -u " + uid)
		print "    User: " + uname + " / UID: " + uid + " / GID: " + rgname + " / has been created"
		if cmd != "":
			print "    User: " + uname + " / UID: " + uid + " / GID: " + rgname + " / with errors"
			print cmd

#Generate file set ("nb" of files) in directory /test_path
	def create_files(self, test_path, nb):
		for i in range(1,nb+1):
			fname = "nfs_file" + str(i)
			cmd = commands.getoutput("touch " + test_path + "/" + fname)
			self.files_list.append(fname)
			print "    File: " + test_path + "/" + fname + " / has been created"
			if cmd != "":
				print "    File: " + test_path + "/" + fname + " / with errors"
				print cmd

# Generate "nb" files in directory "/test_path" with different and random access rights (chmod)
	def create_files_random_chmod(self, test_path, nb):
		commands.getoutput("touch " + test_path + "/nfs_file_444; chmod -f u=r,g=r,o=r " + test_path + "/nfs_file_444") #static file with perm 444
		self.files_list_r.append("nfs_file_444")
		commands.getoutput("touch " + test_path + "/nfs_file_666; chmod -f u=rw,g=rw,o=rw " + test_path + "/nfs_file_666") #static file with perm 666
		self.files_list_r.append("nfs_file_666")
		for i in range(1, nb + 1):
			fname = "nfs_file" + str(i)
			file = test_path + "/" + fname  # the full path to the file
			rwx1 = self.random_rwx()    #get random rights rw, rwx, x, ...
			rwx2 = self.random_rwx()
			rwx3 = self.random_rwx()
# u - user, g - group, o - others / r - read, w - write, x - execute
			cmds = commands.getoutput("touch "+file+"; chmod -f u="+rwx1+",g="+rwx2+",o="+rwx3+" "+file)
			self.files_list_r.append(fname)
			print "    File: " + file + " / has been created with permissions: u="+rwx1+",g="+rwx2+",o="+rwx3
			if cmds != "":
				print "    File: " + file + " / with errors"
				print cmds

# Generate "nb" directories in "/test_path" with different and random access rights (chmod)
	def create_dirs_random_chmod(self, test_path, nb):
		commands.getoutput("mkdir -p " + test_path + "/nfs_dir_444; chmod -R -f u=r,g=r,o=r " + test_path + "/nfs_dir_444") #static dir with perm 444
		self.files_list_r.append("nfs_dir_444")
		commands.getoutput("mkdir -p " + test_path + "/nfs_dir_666; chmod -R -f u=rw,g=rw,o=rw " + test_path + "/nfs_dir_666") #static dir with perm 666
		self.files_list_r.append("nfs_dir_666")
		for i in range(1, nb + 1):
			dname = "nfs_dir" + str(i)
			dir = test_path + "/" + dname  # the full path to the dir
			rwx1 = self.random_rwx()    #get random rights rw, rwx, x, ...
			rwx2 = self.random_rwx()
			rwx3 = self.random_rwx()
# u - user, g - group, o - others / r - read, w - write, x - execute
			cmds = commands.getoutput("mkdir -p "+dir+"; chmod -R -f u="+rwx1+",g="+rwx2+",o="+rwx3+" "+dir)
			self.dirs_list_r.append(dname)
			print "    Directory: " + dir + " / has been created with permissions: u="+rwx1+",g="+rwx2+",o="+rwx3
			if cmds != "":
				print "    Directory: " + dir + " / with errors"
				print cmds

#Get list of groups created for testing
# List of groups
	groups_list = []  # empty list of groups for start
	def get_groups(self):
		fin = open("/etc/group", "r")
		strs = fin.readlines()
		for str in strs:
			splitedline = str.split(":")
			gname = splitedline[0]
			gid = splitedline[2]
			name_true = re.match("nfs_group", gname)
			if name_true != None:
				self.groups_list.append([gname, gid])
		fin.close()

#Get list of users created for testing
#Get the list of all users from file /etc/passwd
# List of users
	users_list = []  # empty list of users for start
	def get_users(self):
		f = open("/etc/passwd", "r")
		strs = f.readlines()
		for str in strs:
			splitedline = str.split(":")
			uname = splitedline[0]
			gid = splitedline[3]
			name_true = re.match("nfs_user", uname)			#nfs_userxxx - created by generator
			if name_true != None:
				self.users_list.append(uname)
		f.close()

#Get list of files created for testing
# List of files
	files_list = []  # empty list of files for start
	def get_files(self, test_path):
		cmd = commands.getoutput("ls " + test_path)
		splitedline = cmd.split("\n")
		for i in range(len(splitedline) - 1):
			name_true = re.match("nfs_file", splitedline[i])
			if name_true != None:
				self.files_list.append(splitedline[i])

# Get list of files with random chmod
	files_list_r = []  # empty list of files for random chmod
	def get_files_random_chmod(self, test_path):
		cmd = commands.getoutput("ls " + test_path)
		splitedline = cmd.split("\n")
		for i in range(len(splitedline) - 1):
			name_true = re.match("nfs_file", splitedline[i])
			if name_true != None:
				self.files_list.append(splitedline[i])

# Get list of dirs with random chmod
	dirs_list_r = []  # empty list of dirs for random chmod
	def get_dirs_random_chmod(self, test_path):
		cmd = commands.getoutput("ls " + test_path)
		splitedline = cmd.split("\n")
		for i in range(len(splitedline) - 1):
			name_true = re.match("nfs_dir", splitedline[i])
			if name_true != None:
				self.files_list.append(splitedline[i])

#UNIX, LINUX file permissions random generator "rw", "rwx", "x", ..
# "r" - read permission / "w" - write permission / "x" - execute permission
	def random_rwx(self):
		out_str = ""
		while (out_str == ""):
			if random.randint(0, 1) == 1:
				out_str += "x"
			if random.randint(0, 1) == 1:
				out_str += "w"
			if random.randint(0, 1) == 1:
				out_str += "r"
		return out_str

#Print list created groups
	def print_groups_list(self,log_path="../logs/log_run.log"):
		print self.groups_list
#Print list created users
	def print_users_list(self,log_path="../logs/log_run.log"):
		print self.users_list
#Print list created files
	def print_files_list(self,log_path="../logs/log_run.log"):
		print self.files_list
#Print list created files with random chmod
	def print_files_list_r(self,log_path="../logs/log_run.log"):
		print self.files_list_r
#Print list created dirs with random chmod
	def print_dirs_list_r(self,log_path="../logs/log_run.log"):
		print self.dirs_list_r

#Print list of dirs with rights: r
	def print_dir_r(self,log_path="../logs/log_run.log"):
		print self.dir_r

#Print list of dirs with rights: rw
	def print_dir_rw(self,log_path="../logs/log_run.log"):
		print self.dir_rw

#Print list of files with rights: r
	def print_file_r(self,log_path="../logs/log_run.log"):
		print self.file_r

#Print list of files with rights: rw
	def print_file_rw(self,log_path="../logs/log_run.log"):
		print self.file_rw

#Print list of files
	def print_files(self,log_path="../logs/log_run.log"):
		print self.files

#Print list of dirs
	def print_dirs(self,log_path="../logs/log_run.log"):
		print self.dirs

#Print list of files + chmod
	def print_files_chmod(self,log_path="../logs/log_run.log"):
		print self.files_chmod

#Print list of dirs + chmod
	def print_dirs_chmod(self,log_path="../logs/log_run.log"):
		print self.dirs_chmod

	#Log execution process of tests (add info)
	def log_add(self,log_path,add):
		time = str(strftime("%Y-%m-%d %H:%M:%S"))  # time when execute code
		log = open(log_path, "a")
		log.write(time + " : " + add + "\n")		# add time and info into the log file
		log.close()

	# Log execution process of tests (del info)
	def log_del(self, log_path):
		log = open(log_path, "w+")
		log.close()


#Test the maximum number of ACEs (Access Control Entries) for dir and file (path) according to the restrictions
# standart permitions (4 ACEs):
# user::***
# group::***
# mask::*** - create after used "setfacl"
# other::***
	def test_max_aces(self, test_path, max_aces):     #test_path - to the test dir or file / max_aces - the max count of ACEs
		self.get_users()			#get users from /etc/password file
		u1 = self.users_list[:]		#get users list
		random.shuffle(u1)			#get random but non-repeating users list
		for i in range(0,len(u1)): 	#any of the created users [len(u1)] can get
			random_user = u1[i]
			random_rights = self.random_rwx()    #get random rights rw, rwx, x, ...
			cmd = commands.getoutput("/usr/bin/setfacl -m u:" + random_user + ":" + random_rights + " " + test_path)
			check = cmd.find("long")	   # check the message "Argument list too long" the limit ACEs
			if check != -1 and i+4 == max_aces:
				# i+5 = 3 (standart) + 1 (mask) + 1 (for start with 1 not 0)
				print "    ACE #",i+5,": setfacl -m u:" + random_user + ":" + random_rights + " " + test_path + " - ERROR!!!"
				print cmd
				print "    Reached the maximum number of ACEs: " + str(max_aces)
				print "    THE TEST #1 HAS BEEN PASSED!!!" 			#The test has been passed
				break
			else:
				print "    ACE #",i+5,": setfacl -m u:" + random_user + ":" + random_rights + " " + test_path

#Stress test for a large number of random operations setting ACEs [Extended ACLs for UNIX]
# Serial setup "cycles" times the option -m (--modify) to modify the ACLs of NFS server export directory
# plus
# Serial setup "cycles" times the option -x (--remove) to remove the ACLs of NFS server export directory
# In addition is exceeding the permissible value of the amount ACEs for file system
	def test_stress_acl_1(self, test_path, cycles):  # test_path - to the test dir (export dir on NFS server)  # cycles - the number of cycles
		commands.getoutput("/usr/bin/setfacl -b " + test_path) #remove all extended ACL entries before start of actions
		self.get_users()  # get users from /etc/password file
		u = self.users_list  # get users list
		for i in range(1, cycles+1):
			random_user = u[random.randint(0,len(u)-1)] #get random and may be repeating users list
			random_rights = self.random_rwx()  # get random rights rw, rwx, x, ...
			cmd1 = commands.getoutput("/usr/bin/setfacl -m u:" + random_user + ":" + random_rights + " " + test_path)
			cmd2 = commands.getoutput("/usr/bin/setfacl -x u:" + random_user + " " + test_path)
			check1 = cmd1.find("error")  # check the message "error"
			check2 = cmd2.find("error")  # check the message "error"
			if i == cycles:					#if cysles have finished and not error message that test has been PASSED
				print "    ACE #", i, ": setfacl -m u:" + random_user + ":" + random_rights + " " + test_path + " & setfacl -x u:" + random_user + " " + test_path
				print
				print "    THE TEST #2 PART 1 HAS BEEN PASSED!!!"  # The test has been passed
				break
			elif check1 != -1 or check2 != -1:  #check if error exist in process setfacl -m and setfacl -x
				print "    ACE #", i, ": setfacl -m u:" + random_user + ":" + random_rights + " " + test_path + " & setfacl -x u:" + random_user + " " + test_path
				print cmd1; print cmd2
				print "    THE TEST #2 PART 1 HAS BEEN FAILED!!!"  # The test has been failed
				break
			else:										 # Normal process setfacl -m and setfacl -x
				print "    ACE #", i, ": setfacl -m u:" + random_user + ":" + random_rights + " " + test_path + " & setfacl -x u:" + random_user + " " + test_path
			# to print every 100th element to to reduce the information on the screen
			# for e in range(1, cycles+1)[99::100]:
			# 	print e

# Stress test for a large number of random operations setting ACEs [Extended ACLs for UNIX]
# Random operations with setfacl: random options (actions)
	def test_stress_acl_2(self, test_path, files, cycles):
		print
		self.create_files(test_path,files)	# create files
		self.get_files(test_path)  			# get files from nfs export dir
		f = self.files_list  				# get files list
		self.get_users()  					# get users from /etc/password file
		u = self.users_list  				# get users list
		self.get_groups() 					# get groups from /etc/group file
		g = self.groups_list  				# get groups list
		print
		for i in range(1, cycles + 1):
			action = random.randint(1, 6)  						# get random action from 1 .. 6
			random_user = u[random.randint(0, len(u) - 1)]		# get random user from list
			random_rights = self.random_rwx()  					# get random rights rw, rwx, x, ...
			random_file = f[random.randint(0, len(f) - 1)] # get random file from list
			if action == 1:  # Create (modification) random ACE for random user for random file
				cmd = commands.getoutput("setfacl -m u:" + random_user + ":" + random_rights + " " + test_path + "/" + random_file)
				print "    ACE #", i, ": setfacl -m u:" + random_user + ':' + random_rights + " " + test_path + "/" + random_file
				if cmd != "":
					print cmd
			if action == 2:  # Remove ACE for random user for random file
				random_user = u[random.randint(0, len(u) - 1)]
				cmd = commands.getoutput("setfacl -x u:" + random_user + " " + test_path + "/" + random_file)
				print "    ACE #", i, ": setfacl -x u:" + random_user + " " + test_path + "/" + random_file
				if cmd != "":
					print cmd
			if action == 3:  # Create (modification) random ACE for random group for random file
				random_group = g[random.randint(0, len(g) - 1)][0]
				cmd = commands.getoutput("setfacl -m g:" + random_group + ":" + random_rights + " " + test_path + "/" + random_file)
				print "    ACE #", i, ": setfacl -m g:" + random_group + ":" + random_rights + " " + test_path + "/" + random_file
				if cmd != "":
					print cmd
			if action == 4:  # Remove ACE for random user for random group
				random_group = g[random.randint(0, len(g) - 1)][0]
				cmd = commands.getoutput("setfacl -x g:" + random_group + " " + test_path + "/" + random_file)
				print "    ACE #", i, ": setfacl -x g:" + random_group + " " + test_path + "/" + random_file
				if cmd != "":
					print cmd
			if action == 5:  # Copying the random ACE of one file to random ACE another file
				random_file_2 = f[random.randint(0, len(f) - 1)]
				cmd = commands.getoutput("cd " + test_path + "; getfacl " + random_file + " | setfacl --set-file=- " + test_path + "/" + random_file_2)
				print "    ACE #", i, ": getfacl " + test_path + "/" + random_file + " | setfacl --set-file=- " + test_path + "/" + random_file_2
				if cmd != "":
					print cmd
			if action == 6:  # Create random default ACEs for export dir (user,group,other)
				random_rights2 = self.random_rwx()
				random_rights3 = self.random_rwx()
				cmd = commands.getoutput("setfacl -d -m u::" + random_rights + ",g::" + random_rights2 + ",o::" + random_rights3 + " " + test_path)
				print "    ACE #", i, ": setfacl -d -m u::" + random_rights + ",g::" + random_rights2 + ",o::" + random_rights3 + " " + test_path
				if cmd != "":
					print cmd
		print
		print "    [Check the status of a NFS service on the NFSv4 server after stress test] :"
		print
		check = commands.getoutput("/usr/bin/systemctl status nfs.service") #check the status of the NFS server services after the stress test
		print check
		print
		if check.find("active (exited)") != -1:
			print "    THE TEST #2 PART 2 HAS BEEN PASSED!!!"  # The test has been passed
		else:
			print "    THE TEST #2 PART 2 HAS BEEN FAILED!!!"  # The test has been failed


# Stress test for export a large number of directories on the NFSv4 server and their subsequent mounting on the NFSv4
# client, health check NFSv4 service
# Operations with server: exportfs; client: mount, unmount.
	def test_stress_exports_1(self, server, cycles):
		print "    [Create", cycles, "directories (both), export them (server) and mount them (client)] : "
		print
		for a in range(1, cycles + 1):
# create dirs for export on server side
			print "    #" + str(a) + " STEP"
			self.expdir_r = commands.getoutput("/usr/bin/rsh " + server + " /usr/bin/mkdir -p /mnt/nfs_exp" + str(a))
			print "    [Server] : directory /mnt/nfs_exp" + str(a) + " has been created"
			if self.expdir_r != "":
				print "    [Server] : directory /mnt/nfs_exp" + str(a) + " created errors"
				print self.expdir_r
# export created dirs on server side
			self.opt_r = " /usr/sbin/exportfs -i -o rw,nohide,no_root_squash,insecure,no_subtree_check,sync '*:/mnt/nfs_exp" + str(a) + "'"
			self.exp_r = commands.getoutput("/usr/bin/rsh " + server + self.opt_r)
			print "    [Server] : directory /mnt/nfs_exp" + str(a) + " has been exported"
			if self.exp_r != "":
				print "    [Server] : directory /mnt/nfs_exp" + str(a) + " exported errors"
				print self.exp_r
# create dirs for export on client side
			self.expdir_l = commands.getoutput("/usr/bin/mkdir -p /mnt/nfs_mnt" + str(a))
			print "    [Client] : directory /mnt/nfs_mnt" + str(a) + " has been created"
			if self.expdir_l != "":
				print "    [Client] : directory /mnt/nfs_mnt" + str(a) + " created errors"
				print self.expdir_r
# mount created dirs from server to client side
			self.opt_l = " -t nfs4 " + server + ":/mnt/nfs_exp" + str(a) + " /mnt/nfs_mnt" + str(a)
			self.exp_l = commands.getoutput("/usr/bin/mount" + self.opt_l)
			print "    [Client] : directory /mnt/nfs_exp" + str(a) + " has been mounted to local /mnt/nfs_mnt" + str(a)
			if self.exp_l != "":
				print "    [Client] : directory /mnt/nfs_exp" + str(a) + " mounted errors"
				print self.exp_l
		time.sleep(3)
		print
		self.check_export = commands.getoutput("showmount -e " + server + " | grep nfs_exp" + str(cycles))
		print "    [Check the final export directory on the server] :"
		print
		print self.check_export
		print
		print "    [Check the final mount directory on the client] :"
		print
		self.check_mount = commands.getoutput("/usr/bin/mount | grep nfs_mnt" + str(cycles))
		print self.check_mount
		print
		if self.exp_r.find("error") != -1 or self.exp_l.find("error") != -1 or self.check_export == "" or self.check_mount == "":
			print "    THE TEST #3 PART 1 HAS BEEN FAILED!!!"  # The test has been failed
		else:
			print "    THE TEST #3 PART 1 HAS BEEN PASSED!!!"  # The test has been passed

# Stress test for large number random operations: exports: export/unexport (server), mount/unmount (client)
	def test_stress_exports_2(self, server, cycles):
		print "    [Execute random operations with " + str(cycles) + " exports: export/unexport (server), mount/unmount (client)] : "
		print
		for b in range(1, cycles+1):   # number of random operations cycles +1 (two times more than exports)
			self.action = random.randint(1, 4)  # get random action from 1 .. 4
			if self.action == 1:  # export random dir on server (if b > exports then can run export operations with non-existent dirs)
				cmd1 = " /usr/sbin/exportfs -i -o rw,nohide,no_root_squash,insecure,no_subtree_check,sync '*:/mnt/nfs_exp" + str(b) + "'"
				cmd = commands.getoutput("/usr/bin/rsh " + server + cmd1)
				print "    #" + str(b) + " STEP [Server] : directory /mnt/nfs_exp" + str(b) + " has been exported"
				if cmd != "":
					print "    #" + str(b) + " STEP [Server] : directory /mnt/nfs_exp" + str(b) + " exported errors"
					print cmd
			if self.action == 2:  # unexport random dir on server (if b > exports then can run unexport operations with non-existent dirs)
				cmd1 = " /usr/sbin/exportfs -u '*:/mnt/nfs_exp" + str(b) + "'"
				cmd = commands.getoutput("/usr/bin/rsh " + server + cmd1)
				print "    #" + str(b) + " STEP [Server] : directory /mnt/nfs_exp" + str(b) + " has been unexported"
				if cmd != "":
					print "    #" + str(b) + " STEP [Server] : directory /mnt/nfs_exp" + str(b) + " unexported errors"
					print cmd
			if self.action == 3:  # mount random dir on client (if b > exports then can run mount operations with non-existent dirs)
				cmd1 = " -t nfs4 " + server + ":/mnt/nfs_exp" + str(b) + " /mnt/nfs_mnt" + str(b)
				cmd = commands.getoutput("/usr/bin/mount" + cmd1)
				print "    #" + str(b) + " STEP [Client] : directory /mnt/nfs_exp" + str(b) + " has been mounted to local /mnt/nfs_mnt" + str(b)
				if cmd != "":
					print "    #" + str(b) + " STEP [Client] : directory /mnt/nfs_exp" + str(b) + " mounted errors"
					print cmd
			if self.action == 4:  # unmount random dir on client (if b > exports then can run unmount operations with non-existent dirs)
				cmd1 = " -f -l /mnt/nfs_mnt" + str(b)   #force  -f force unmount (in case of an unreachable NFS system)
				cmd = commands.getoutput("/usr/bin/umount" + cmd1)
				print "    #" + str(b) + " STEP [Client] : directory /mnt/nfs_mnt" + str(b) + " has been unmounted"
				if cmd != "":
					print "    #" + str(b) + " STEP [Client] : directory /mnt/nfs_mnt" + str(b) + " unmounted errors"
					print cmd
		print
		print "    [Check the status of a NFS service on the NFSv4 server after stress test] :"
		print
		self.check = commands.getoutput("/usr/bin/rsh " + server + " /usr/bin/systemctl status nfs.service")  # check the status of the NFS server services after the stress test
		print self.check
		print
		if self.check.find("active (exited)") != -1:
			print "    THE TEST #3 PART 2 HAS BEEN PASSED!!!"  # The test has been passed
		else:
			print "    THE TEST #3 PART 2 HAS BEEN FAILED!!!"  # The test has been failed

####################################POSIX tests#####################################################
#Get files and dirs, get chmod rights, export to lists, tuples according permissions
# u - user, g - group, o - others / r - read, w - write, x - execute
# chown, chgrp, chmod, umask
	dir_r = []			# the empty list of firs with rights: r
	dir_rw = []			# the empty list of dirs with rights: rw
	file_r = []			# the empty list of files with rights: r
	file_rw = []  		# the empty list of files with rights: rw
	files = []  		# the empty list of files in test_path
	dirs = []  			# the empty list of dirs in test_path
	dirs_chmod = {}  	# the empty tuple of dirictories with recognized access rights
	files_chmod = {}  	# the empty tuple of files with recognized access rights
	def posix_chmod_parser(self,test_path):
		log_path = "../logs/log_run.log"
		self.test_dir = test_path  # path to test dir with files and dirs (different chmod)
		print
		print "    [Get directories and files in test directory " + self.test_dir + "] :"
		self.log_add(log_path,"[Get directories and files in test directory " + self.test_dir + "] :")
		print
		for dir_n, dir_nn, file_nn in os.walk(self.test_dir):
			blank = 0
			for dir2 in dir_nn:			# Get directories
				dir_true = os.path.join(dir_n, dir2)
				mode_d = int(oct(os.stat(dir_true).st_mode)[-3:])  # get chmod (permissions) ___uga
				print "    Get dir: " + dir_true + " permissions: " + str(mode_d)
				self.log_add(log_path,"Get dir: " + dir_true + " permissions: " + str(mode_d))
				blank += 1
				self.dirs.append(dir_true)
				if mode_d in range (444,446):	#444 (r--r--r--) .. 446 (r--r--rw-)
					self.dir_r.append(dir_true)
				elif mode_d in range (666,778): #666 (rw-rw-rw-) .. 777 (rwxrwxrwx))
					self.dir_rw.append(dir_true)
			for file_n in file_nn:			# Get files
				file_true = os.path.join(dir_n, file_n)
				mode_f = int(oct(os.stat(file_true).st_mode)[-3:])			# get chmod (permissions) ___uga
				print "    Get file: " + file_true + " permissions: " + str(mode_f)
				self.log_add(log_path,"Get file: " + file_true + " permissions: " + str(mode_f))
				self.files.append(file_true) #444 = -r--r--r--  any can read  /  #666 = -rw-rw-rw-  any can read and write
				if mode_f in range(444, 446):  # 444 .. 446
					self.file_r.append(file_true)
				elif mode_f in range(666, 778):  # 666 .. 777
					self.file_rw.append(file_true)
		# add markers into the typles in order to find it in future tests
		self.files_chmod["r"] = self.file_r
		self.files_chmod["rw"] = self.file_rw
		self.dirs_chmod["r"] = self.dir_r
		self.dirs_chmod["rw"] = self.dir_rw

#Check the ability to write str to the file
	marker_w = True
	def posix_check_write_file(self, file_path, look):
		log_path = "../logs/log_run.log"
		res = look
		str = "<NFSv4 test>" #str to write into the file
		print "    Try writing " + str + " to the file " + file_path + " / Expected: " + format(look)
		self.log_add(log_path, "Try writing " + str + " to the file " + file_path + " / Expected: " + format(look))
		try:
			file = open(file_path, "w")
			file.write(str)
			file.close()
			file = open(file_path, "r")
			for txt in file: # find  "<NFSv4 test>" after writed
				if str in txt:
					self.marker_w = self.marker_w and True
				else:
					self.marker_w = self.marker_w and False
			file.close()
		except IOError:
			res = not look
		if res is True and self.marker_w is True:  # if look and real = true
			print "    Try writing " + str + " to the file " + file_path + " / Result: " + format(look)
			self.log_add(log_path, "Try writing " + str + " to the file " + file_path + " / Result: " + format(look))
		else:
			print "    Try writing " + str + " to the file " + file_path + " / Result: " + format(not look)
			self.log_add(log_path, "Try writing " + str + " to the file " + file_path + " / Result: " + format(not look))

#Check the ability to read the file
	marker_r = True
	def posix_check_read_file(self, file_path, look):
		log_path = "../logs/log_run.log"
		res = look
		print "    Try reading the file " + file_path + " / Expected: " + format(look)
		self.log_add(log_path, "Try reading the file " + file_path + " / Expected: " + format(look))
		try:
			file = open(file_path, "r")
			self.marker_r = self.marker_r and True
			file.close()
		except IOError:
			res = not look
			self.marker_r = self.marker_r and False
# print "READ" + format(look)
		if res is True and self.marker_r is True:
			print "    Try reading the file " + file_path + " / Result: " + format(look)
			self.log_add(log_path, "Try reading the file " + file_path + " / Result: " + format(not look))
		else:
			print "    Try reading the file " + file_path + " / Result: True / Test: Passed"
			self.log_add(log_path, "Try reading the file " + file_path + " / Result: True / Test: Passed")

	def posix_chmod_check_files(self,test_path):
		log_path = "../logs/log_run.log"
		self.test_dir = test_path  # path to test dir with files (different chmod)
		self.posix_chmod_parser(test_path)	#Get directories and files in test dir
		files = self.files_chmod
		print
		print "    [Check the permissions of the files in test directory " + self.test_dir + " ] :"
		print
		self.log_add(log_path,"[Check the permissions of the files in test directory " + self.test_dir + " ] :")
#FILE READ TEST
		print "    [Test to read for files with permissions: r] / Expected: PASSED"
		print
		self.log_add(log_path, "[Test to read for files with permissions: r] / Expected: PASSED")
		for r in files["r"]:
			self.posix_check_read_file(r, True)		#wait +
			self.posix_check_write_file(r, False)	#wait -
		if self.marker_r is True and self.marker_w is True:
			end_r = "PASSED"
		else:
			end_r = "FAILED"
		print
		print "    [Test to read for files with permissions: r] / Result: " + end_r
		self.log_add(log_path, "[Test to read for files with permissions: r] / Result: " + end_r)
		print
		print
#FILE READ AND WRITE TEST
		print "    [Test to read and write for files with permissions: rw] / Expected: PASSED"
		print
		self.log_add(log_path, "[Test to read and write for files with permissions: rw] / Expected: PASSED")
		for rw in files["rw"]:
			self.posix_check_read_file(rw, True)		#wait +
			self.posix_check_write_file(rw, True)		#wait +
		if self.marker_r is True and self.marker_w is True:
			end_rw = "PASSED"
		else:
			end_rw = "FAILED"
		print
		print "    [Test to read and write for files with permissions: rw] / Result: " + end_rw
		self.log_add(log_path, "[Test to read and write for files with permissions: rw] / Result: " + end_rw)
		print
		print
#Check full part 1
		if end_rw == "PASSED" and end_r == "PASSED":
			print "    THE TEST #4 PART 1 HAS BEEN PASSED!!!"  # The test has been passed
			self.log_add(log_path, "THE TEST #4 PART 1 HAS BEEN PASSED!!!")
			return True
		else:
			print "    THE TEST #4 PART 1 HAS BEEN FAILED!!!"  # The test has been failed
			self.log_add(log_path, "THE TEST #4 PART 1 HAS BEEN FAILED!!!")
			return False


	marker_dr = True
	marker_drw = True
	def posix_chmod_check_dirs(self,test_path):
		log_path = "../logs/log_run.log"
		self.test_dir = test_path  # path to test dir with files (different chmod)
		self.posix_chmod_parser(test_path)	#Get directories and files in test dir
		dirs = self.dirs_chmod
		print
		print "    [Check the permissions of the dirs in test directory " + self.test_dir + " ] :"
		print
		self.log_add(log_path,"[Check the permissions of the dirs in test directory " + self.test_dir + " ] :")
#DIR READ TEST
		print "    [Test to read for dirs with permissions: r] / Expected: PASSED"
		print
		self.log_add(log_path, "[Test to read for dirs with permissions: r] / Expected: PASSED")
		for r in dirs["r"]:
			print "    Try reading the dir " + r + " / Expected: True"
			self.log_add(log_path, "Try reading the dir " + r + " / Expected: True")
			try:
				os.listdir(r)
			except OSError:
				self.marker_dr = False
				print "    Try reading the dir " + r + " / Result: False"
				self.log_add(log_path, "Try reading the dir " + r + " / Result: False")
			else:
				print "    Try reading the dir " + r + " / Result: True"
				self.log_add(log_path, "Try reading the dir " + r + " / Result: True")
		if self.marker_dr is True:
			end_dr = "PASSED"
		else:
			end_dr = "FAILED"
		print
		print "    [Test to read for dirs with permissions: r] / Result: " + end_dr
		self.log_add(log_path, "[Test to read for dirs with permissions: r] / Result: " + end_dr)
		print
		print
#Check full part 2
		if end_dr == "PASSED":
			print "    THE TEST #4 PART 2 HAS BEEN PASSED!!!"  # The test has been passed
			self.log_add(log_path, "THE TEST #4 PART 2 HAS BEEN PASSED!!!")
			return True
		else:
			print "    THE TEST #4 PART 2 HAS BEEN FAILED!!!"  # The test has been failed
			self.log_add(log_path, "THE TEST #4 PART 2 HAS BEEN FAILED!!!")
			return False

# add options
parser = OptionParser()
parser.add_option("--gu", action="store_true", dest="gu", default=False, help="Get list of users created for testing")
parser.add_option("--gg", action="store_true", dest="gg", default=False, help="Get list of groups created for testing")
parser.add_option("--gf", action="store_true", dest="gf", default=False, help="Get list of files created for testing")
parser.add_option("-u", "--users", dest="u", type="int", help="Generate u users for testing")
parser.add_option("-g", "--groups", dest="g", type="int", help="Generate g groups for testing")
parser.add_option("-f", "--files", dest="f", type="int", help="Generate f files for testing in -d dir")
parser.add_option("-c", "--cycles", dest="c", type="int", help="The number of loops in the test")
parser.add_option("-p", "--path", dest="p", type="str", help="Path to test dir or file for set ACEs")
parser.add_option("-m", "--max", dest="m", type="int", help="Max count of ACEs for dir or file according of type of fs")
parser.add_option("-d", "--dir", dest="d", type="str", help="Path to export dir for creating -f files")
parser.add_option("--nf", dest="nf", type="int", help="Generate ff files for testing in --ddd dir")
parser.add_option("--nd", dest="nd", type="int", help="Generate dd dirs for testing in --ddd dir")
parser.add_option("--ddd", dest="ddd", type="str", help="Path to ddd dir for create files and dirs with random chmod")
parser.add_option("--posix1", dest="posix1", type="str", help="Run posix test part 1 - check files perms = test_path")
parser.add_option("--posix2", dest="posix2", type="str", help="Run posix test part 2 - check dirs perms = test_path")
(options, args) = parser.parse_args()

#use options
if options.gu is True:
	full_generator().get_users()					# --gu GET USERS

if options.gg is True:
	full_generator().get_groups()					# --gg GET GROUPS

if options.gf is True and options.d is not None:
	full_generator().get_files(options.d)					# --gf GET FILES
#If the value u > 0 and list of users have gotten (Run only after -g --gg)

if options.u > 0 and options.gg is not False:
	full_generator().create_users_n(options.u)		# -u CREATE -u USERS

if options.g > 0:
	full_generator().create_groups_n(options.g)		# -g CREATE -g GROUPS

if options.p is not None and options.m > 0:
	full_generator().test_max_aces(options.p,options.m)		# -p PATH TO TEST FILE OR DIR 	-m MAX ACEs

if options.d is not None and options.f > 0 and options.c is None:
	full_generator().create_files(options.d,options.f)		# -d PATH TO EXP DIR	-f COUNT OF FILES

if options.d is not None and options.c > 0 and options.f is None:
	full_generator().test_stress_acl_1(options.d, options.c)  # -d PATH TO EXP DIR	-c NUMBER OF LOOPS IN TEST

if options.d is not None and options.f > 0 and options.c > 0:
	full_generator().test_stress_acl_2(options.d, options.f, options.c)  #-d PATH TO EXP DIR  #-f COUNT OF FILES  #-c NUMBER OF LOOPS IN TEST

if options.nf > 0 and options.ddd is not None > 0:
	full_generator().create_files_random_chmod(options.ddd, options.nf)  #-ddd PATH TEST DIR  #-nf COUNT OF TEST FILES

if options.nd > 0 and options.ddd is not None > 0:
	full_generator().create_dirs_random_chmod(options.ddd, options.nd)  #-ddd PATH TEST DIR  #-nd COUNT OF TEST DIRS

if options.posix1 is not None:
	full_generator().posix_chmod_check_files(options.posix1)  #--posix1 PATH TO TEST DIR WITH FILES (RANDOM CHMOD)

if options.posix2 is not None:
	full_generator().posix_chmod_check_dirs(options.posix2)  #--posix2 PATH TO TEST DIR WITH DIRS (RANDOM CHMOD)