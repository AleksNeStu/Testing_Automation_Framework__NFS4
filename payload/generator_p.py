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

import time
import random  						#Random variable generators
import commands	 					#Execute shell commands via os.popen() and return status, output
import re		 					#Support for regular expressions (RE)
from optparse import OptionParser	#Parser for command line options

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
		print self.files_list

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
				print "    ACE #", i, ": setfacl -m u:" + random_user + ":" + random_rights + " " + test_path
				print "                setfacl -x u:" + random_user + " " + test_path
				print
				print "    THE TEST #2 PART 1 HAS BEEN PASSED!!!"  # The test has been passed
				break
			elif check1 != -1 or check2 != -1:  #check if error exist in process setfacl -m and setfacl -x
				print "    ACE #", i, ": setfacl -m u:" + random_user + ":" + random_rights + " " + test_path
				print "                setfacl -x u:" + random_user + " " + test_path
				print cmd1; print cmd2
				print "    THE TEST #2 PART 1 HAS BEEN FAILED!!!"  # The test has been failed
				break
			else:										 # Normal process setfacl -m and setfacl -x
				print "    ACE #", i, ": setfacl -m u:" + random_user + ":" + random_rights + " " + test_path
				print "                setfacl -x u:" + random_user + " " + test_path
			# to print every 100th element to to reduce the information on the screen
			# for e in range(1, cycles+1)[99::100]:
			# 	print e

# Stress test for a large number of random operations setting ACEs [Extended ACLs for UNIX]
# Random operations with setfacl: random options (actions),
	def test_stress_acl_2(self, test_path, files, cycles):
		self.create_files(test_path,files)	# create files
		self.get_files(test_path)  			# get files from nfs export dir
		f = self.files_list  				# get files list
		self.get_users()  					# get users from /etc/password file
		u = self.users_list  				# get users list
		self.get_groups() 					# get groups from /etc/group file
		g = self.groups_list  				# get groups list
		for i in range(1, cycles + 1):
			action = random.randint(1, 6)  						# get random action from 1 .. 6
			random_user = u[random.randint(0, len(u) - 1)]		# get random user from list
			random_rights = self.random_rwx()  					# get random rights rw, rwx, x, ...
			random_file = f[random.randint(0, len(f) - 1)] # get random file from list
			if action == 1:  # Create (modification) random ACE for random user for random file
				cmd = commands.getoutput("setfacl -m u:" + random_user + ":" + random_rights + " " + test_path + "/" + random_file)
				print "    setfacl -m u:" + random_user + ':' + random_rights + " " + test_path + "/" + random_file
				if cmd != "":
					print cmd
			if action == 2:  # Remove ACE for random user for random file
				random_user = u[random.randint(0, len(u) - 1)]
				cmd = commands.getoutput("setfacl -x u:" + random_user + " " + test_path + "/" + random_file)
				print "    setfacl -x u:" + random_user + " " + test_path + "/" + random_file
				if cmd != "":
					print cmd
			if action == 3:  # Create (modification) random ACE for random group for random file
				random_group = g[random.randint(0, len(g) - 1)][0]
				cmd = commands.getoutput("setfacl -m g:" + random_group + ":" + random_rights + " " + test_path + "/" + random_file)
				print "    setfacl -m g:" + random_group + ":" + random_rights + " " + test_path + "/" + random_file
				if cmd != "":
					print cmd
			if action == 4:  # Remove ACE for random user for random group
				random_group = g[random.randint(0, len(g) - 1)][0]
				cmd = commands.getoutput("setfacl -x g:" + random_group + " " + test_path + "/" + random_file)
				print "    setfacl -x g:" + random_group + " " + test_path + "/" + random_file
				if cmd != "":
					print cmd
			if action == 5:  # Copying the random ACE of one file to random ACE another file
				random_file_2 = f[random.randint(0, len(f) - 1)]
				cmd = commands.getoutput("getfacl " + test_path + "/" + random_file + " | setfacl --set-file=- " + test_path + "/" + random_file_2)
				print "    getfacl " + test_path + "/" + random_file + " | setfacl --set-file=- " + test_path + "/" + random_file_2
				if cmd != "":
					print cmd
			if action == 6:  # Create random default ACEs for export dir (user,group,other)
				random_rights2 = self.random_rwx()
				random_rights3 = self.random_rwx()
				cmd = commands.getoutput("setfacl -d -m u::" + random_rights + ",g::" + random_rights2 + ",o::" + random_rights3 + " " + test_path)
				print "    setfacl -d -m u::" + random_rights + ",g::" + random_rights2 + ",o::" + random_rights3 + " " + test_path
				if cmd != "":
					print cmd

# add options
parser = OptionParser()
parser.add_option("--gu", action="store_true", dest="gu", default=False, help="Get list of users created for testing")
parser.add_option("--gg", action="store_true", dest="gg", default=False, help="Get list of groups created for testing")
parser.add_option("--gf", action="store_true", dest="gf", default=False, help="Get list of files created for testing")
parser.add_option("-u", "--users", dest="u", type="int", help="Generate u users for testing")
parser.add_option("-g", "--groups", dest="g", type="int", help="Generate g groups for testing")
parser.add_option("-f", "--files", dest="f", type="int", help="Generate f files for testing in -d dir")
parser.add_option("-c", "--cycles", dest="c", type="int", help="The number of loops in the test")
# parser.add_option("-d", "--dir", dest="d", type="str", help="Create the dir in the given NFS exp dir for testing")
# parser.add_option("-f", "--file", dest="f", type="str", help="Create the file in the given NFS exp dir for testing")
parser.add_option("-p", "--path", dest="p", type="str", help="Path to test dir or file for set ACEs")
parser.add_option("-m", "--max", dest="m", type="int", help="Max count of ACEs for dir or file according of type of fs")
parser.add_option("-d", "--dir", dest="d", type="str", help="Path to export dir for creating -f files")
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

if options.d is not None and options.f > 0:
	full_generator().create_files(options.d,options.f)		# -d PATH TO EXP DIR	-f COUNT OF FILES

if options.d is not None and options.c > 0:
	full_generator().test_stress_acl_1(options.d, options.c)  # -d PATH TO EXP DIR	-c NUMBER OF LOOPS IN TEST

if options.d is not None and options.f > 0 and options.c > 0:
	full_generator().test_stress_acl_2(options.d, options.f, options.c)  #-d PATH TO EXP DIR  #-f COUNT OF FILES  #-c NUMBER OF LOOPS IN TEST

# test.getNUserList(options.nbusers)
# test.getNGroupList(options.nbgroups)
# for i in range (options.nloop):
# 	test.randomOp(options.path)