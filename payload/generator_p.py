#!/usr/bin/python
# -*- coding: utf-8 -*-
r"""The test data generator for testing NFSv4 and ACLs (run via call parameters)

Opportunities:
--gu - Get list of users created for testing
--gg - Get list of groups created for testing
--cu - Clean all users created for testing
--cg - Clean all groups created for testing

example: python ./generator_p.py -g 60 --gg -u 76

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


########################Get list of groups created for testing############################
# List of groups
	groups_list = []  # empty list of groups for start
	groups_list_len = len(groups_list)

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

	def get_groups_n(self, gg):
		fin = open("/etc/group","r")
		strs = fin.readlines()
		n = 0
		for str in strs:
			splitedline = str.split(':')
			gname = splitedline[0]
			gid = splitedline[2]
			name_true = re.match("nfs_group", gname)
			if name_true != None:
				self.groups_list.append([gname, gid])
				n = n + 1
			if n == gg:
				break
		fin.close()

########################Get list of users created for testing############################
#Get the list of all users from file /etc/passwd
# List of users
	users_list = []  # empty list of users for start
	users_list_len = len(users_list)

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

	def get_users_n(self, gu):
		f = open("/etc/passwd", "r")
		strs = f.readlines()
		n = 0
		for str in strs:
			splitedline = str.split(":")
			uname = splitedline[0]
			gid = splitedline[3]
			name_true = re.match("nfs_user", uname)			#nfs_userxxx - created by generator
			if name_true != None:
				self.users_list.append(uname)
				n = n + 1
			if n == gu:
				break
		f.close()

############UNIX, LINUX file permissions random generator "rw", "rwx", "x", ..
# "r" - read permission / "w" - write permission / "x" - execute permission
	def random_rwx(self):
		out_str = ""
		while (out_str == ""):
			if random.randint(0, 1) == 1:
				out_str += 'x'
			if random.randint(0, 1) == 1:
				out_str += 'w'
			if random.randint(0, 1) == 1:
				out_str += 'r'
		return out_str

#####Test the maximum number of ACEs (Access Control Entries) for dir and file (path) according to the restrictions############################
# standart permitions (4 ACEs):
# user::***
# group::***
# mask::*** - create after used "setfacl"
# other::***
	def test_max_aces(self, test_path, max_aces):     #test_path - to the test dir or file / max_aces - the max count of ACEs
		self.get_users()			#get users from /ets/password file
		u1 = self.users_list[:]		#get users list
		random.shuffle(u1)			#get random but non-repeating users list
		for i in range(0,len(u1)): 	#any of the created users [len(u1)] can get
			random_user = u1[i]
			random_rights = self.random_rwx()    #get random rights rw, rwx, x, ...
			cmd = commands.getoutput("/usr/bin/setfacl -m u:" + random_user + ":" + random_rights + " " + test_path)
			check = cmd.find("long")	   # check the message "Argument list too long" the limit ACEs
			if check != -1 and i+4 == max_aces:
				print				#  i+5 = 3 (standart) + 1 (mask) + 1 (for start with 1 not 0)
				print "    ACE #",i+5,": setfacl -m u:" + random_user + ":" + random_rights + " " + test_path
				print cmd
				print "    Reached the maximum number of ACEs: " + str(max_aces)
				return True			#The test has been passed
			else:
				print "    ACE #",i+5,": setfacl -m u:" + random_user + ":" + random_rights + " " + test_path
				# return False		#The test has been failed


# add options
parser = OptionParser()
parser.add_option("--gu", action="store_true", dest="gu", default=False, help="Get list of users created for testing")
parser.add_option("--gg", action="store_true", dest="gg", default=False, help="Get list of groups created for testing")
parser.add_option("-u", "--users", dest="u", type="int", help="Generate u users for testing")
parser.add_option("-g", "--groups", dest="g", type="int", help="Generate g groups for testing")
# parser.add_option("-d", "--dir", dest="d", type="str", help="Create the dir in the given NFS exp dir for testing")
# parser.add_option("-f", "--file", dest="f", type="str", help="Create the file in the given NFS exp dir for testing")
parser.add_option("-p", "--path", dest="p", type="str", help="Path to test dir or file for set ACEs")
parser.add_option("-m", "--max", dest="m", type="int", help="Max count of ACEs for dir or file according of type of fs")
(options, args) = parser.parse_args()

#use options
if options.gu is True:
	full_generator().get_users()					# --gu GET USERS
if options.gg is True:
	full_generator().get_groups()					# --gg GET GROUPS
#If the value u > 0 and list of users have gotten (Run only after -g --gg)
if options.u > 0 and options.gg is not False:
	full_generator().create_users_n(options.u)		# -u CREATE USERS
if options.g > 0:
	full_generator().create_groups_n(options.g)		# -g CREATE GROUPS
# if options.d is not int:
# 	full_generator().create_nfs_dir(options.d)				# -d CREATE DIR in EXP DIR
# if options.f is not  int:
# 	full_generator().create_nfs_file(options.f)				# -f CREATE FILE in EXP DIR
if options.p is not None and options.m is not None:
	full_generator().test_max_aces(options.p,options.m)		# -p PATH OF TEST FILE OR DIR 	-m MAX ACEs