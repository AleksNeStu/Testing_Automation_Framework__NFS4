#!/usr/bin/python
# -*- coding: utf-8 -*-
r"""The test data cleaner for testing NFSv4 and ACLs (run via call parameters)

Opportunities:
--gu - Get list of users created for testing
--gg - Get list of groups created for testing
--gf - Get list of files created for testing
--cu - Clean all users created for testing
--cg - Clean all groups created for testing
--cf - Clean all files created for testing
--full - Full get and clean data created for testing
-d - Path to export dir for creating files
-c - Path to dir for removing files and start action remove:  users, groups, files, ACEs

example:
LOCAL: python cleaner_r.py --gu --cu --gg --cg
REMOTE: cat ./cleaner_p.py | /usr/bin/rsh rhel python - --full

@Developed by AleksNeStu

"""

import commands	 #Execute shell commands via os.popen() and return status, output
import re		 #Support for regular expressions (RE)
from optparse import OptionParser


class full_cleaner(object):


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

#userdel - delete a user account and related files
#-f - force some actions that would fail otherwise
#-r - remove home directory and mail spool
	def clean_users(self):
		for uname in self.users_list:
			cmd = commands.getoutput("/usr/sbin/userdel -r " + uname)
			print "    User del: " + uname + " / has been done"
			if cmd != "":
				print "    User del: " + uname + " / with errors"
				print cmd
		self.users_list = []

#userdel - delete a user account and related files (hidden)
	def clean_users_h(self):
		for uname in self.users_list:
			commands.getoutput("/usr/sbin/userdel -r " + uname)
		self.users_list = []

#Clean all groups created for testing
#groupdel - delete a group
	def clean_groups(self):
		for gname in self.groups_list:
			cmd = commands.getoutput("/usr/sbin/groupdel " + gname[0])
			print "    Group del: " + gname[0] + " / has been done"
			if cmd != "":
				print "    Group del: " + gname[0] + " / with errors"
				print cmd
		self.groups_list = []

#Clean all groups created for testing (hidden)
	def clean_groups_h(self):
		for gname in self.groups_list:
			commands.getoutput("/usr/sbin/groupdel " + gname[0])
		self.groups_list = []

#Clean all files created for testing
#groupdel - delete a group
	def clean_files(self, test_path):
		for fname in self.files_list:
			cmd = commands.getoutput("/usr/bin/rm -f " + test_path + "/" + fname[0])
			print "    File del: " + test_path + "/" + fname[0] + " / has been done"
			if cmd != "":
				print "    File del: " + test_path + "/" + fname[0] + " / with errors"
				print cmd
		self.files_list = []

#Clean all files created for testing (hidden)
	def clean_files_h(self, test_path):
		for fname in self.files_list:
			commands.getoutput("/usr/bin/rm -f " + test_path + "/" + fname[0])
		self.files_list = []

#Hiden clean data (гemove users, groups, files, dirs, ACEs)
	def clean_full_h(self, clean_path): #clean_full (hidden)
		commands.getoutput("/usr/bin/setfacl -R -b " + clean_path) #ACLs del
		commands.getoutput("/usr/bin/setfacl -R -k " + clean_path)  # ACLs (defauls) del
		commands.getoutput('/usr/bin/find ' + clean_path + ' -type f -name "nfs*" -exec rm -f {} \;') #files del
		commands.getoutput('/usr/bin/find ' + clean_path + ' -type d -name "nfs*" -exec rm -rf {} \;')  # dirs del
		self.get_users()
		self.get_groups()
		self.clean_users_h()  #users del
		self.clean_groups_h() #groups del

#Hiden clean data (гemove users, groups, files, ACEs)
	def clean_full(self, clean_path): #clean_full (hidden)
		print
		commands.getoutput("/usr/bin/setfacl -R -b " + clean_path)  # ACLs del
		commands.getoutput("/usr/bin/setfacl -R -k " + clean_path)  # ACLs (defauls) del
		print "    Created ACEs have been deleted from export dir and files in it on the NFS server."
		commands.getoutput('/usr/bin/find ' + clean_path + ' -type f -name "nfs*" -exec rm -f {} \;') #files del
		print "    Created files have been deleted from export dir on the NFS server."
		self.get_users()
		self.get_groups()
		self.clean_users_h()  #users del
		self.clean_groups_h() #groups del
		print "    Created users and groups have been deleted from the NFS server."


	def clean_mounts_exports(self, server):
		print
# client side (1 - unmout , 2 - del dirs)
		c1 = commands.getoutput("/usr/bin/umount -f -l /mnt/nfs_mnt*")  # force unmout mounted dirs (client)
		print "    [Client] : Mounted directories have been unmonted on NFSv4 client."
		if c1 !="":
			print c1
		c2 = commands.getoutput("/usr/bin/rm -rf /mnt/nfs_mnt*")  # force del old mounted dirs (client)
		print "    [Client] : Old mounted directories have been deleted from NFSv4 client."
		if c2 !="":
			print c2
# server side (3 - unexport, 4 - del dirs)
		c3 = commands.getoutput("/usr/bin/rsh " + server + " /usr/sbin/exportfs -r") # unexport exported dirs (server)
		print "    [Server] : Exported directories have been unexported on the NFSv4 server."
		if c3 != "":
			print c3
		c4 = commands.getoutput("/usr/bin/rsh " + server + " /usr/bin/rm -rf /mnt/nfs_exp*")  # force del old mounted dirs (server)
		print "    [Client] : Old exported directories have been deleted from NFSv4 server."
		if c4 !="":
			print c4

	def clean_mounts_exports_h(self, server): #hidden clean
		print
# client side (1 - unmout , 2 - del dirs)
		commands.getoutput("/usr/bin/umount -f -l /mnt/nfs_mnt*")  # force unmout mounted dirs (client)
		commands.getoutput("/usr/bin/rm -rf /mnt/nfs_mnt*")  # force del old mounted dirs (client)
# server side (3 - unexport, 4 - del dirs)
		commands.getoutput("/usr/bin/rsh " + server + " /usr/sbin/exportfs -r")  # unexport exported dirs (server)
		commands.getoutput("/usr/bin/rsh " + server + " /usr/bin/rm -rf /mnt/nfs_exp*")  # force del old mounted dirs (server)


# add options in
parser = OptionParser()
parser.add_option("--gu", action="store_true", dest="gu", default=False, help="Get list of users created for testing")
parser.add_option("--gg", action="store_true", dest="gg", default=False, help="Get list of groups created for testing")
parser.add_option("--gf", action="store_true", dest="gf", default=False, help="Get list of files created for testing")
parser.add_option("--cu", action="store_true", dest="cu", default=False, help="Clean all users created for testing")
parser.add_option("--cg", action="store_true", dest="cg", default=False, help="Clean all groups created for testing")
parser.add_option("--cf", action="store_true", dest="cf", default=False, help="Clean all files created for testing")
parser.add_option("--full", action="store_true", dest="full", default=False, help="Full get and clean data created for testing")
parser.add_option("-d", "--dir", dest="d", type="str", help="Path to export dir for creating files")
parser.add_option("-c", "--clean", dest="c", type="str", help="Path to dir for removing files and start action remove users, groups, files, ACEs - Hidden")
parser.add_option("-r", "--remove", dest="r", type="str", help="Path to dir for removing files and start action remove users, groups, files, ACEs")
(options, args) = parser.parse_args()

#use options
if options.gu is True:
	full_cleaner().get_users()				# --gu GET USERS

if options.gg is True:
	full_cleaner().get_groups()				# --gg GET GROUPS

if options.gf is True and options.d is not None:
	full_cleaner().get_files(options.d)		# --gf GET FILES (-d /***)

if options.cu is True and options.gu is True:
	full_cleaner().clean_users()			# --cu CLEAN USERS (--gu)

if options.cg is True and options.gg is True:
	full_cleaner().clean_groups()			# --cg CLEAN GROUPS (--gg)

if options.cf is True and options.gf is True and options.d is not None:
	full_cleaner().clean_files(options.d)			# --cf CLEAN FILES (--gf -d /***)

if options.full is True:					# --full FULL GET and CLEAN (USERS,GROUPS)
	full_cleaner().get_users()
	full_cleaner().get_groups()
	full_cleaner().clean_users()
	full_cleaner().clean_groups()

if options.c is not None:					# -c = path to dir FULL HIDDEN CLEAN (USERS,GROUPS, ACES, FILES)
	full_cleaner().clean_full_h(options.c)

if options.r is not None:					# -r = path to dir FULL CLEAN (USERS,GROUPS, ACES, FILES)
	full_cleaner().clean_full(options.r)