#!/usr/bin/python
# -*- coding: utf-8 -*-
r"""The test data cleaner for testing NFSv4 and ACLs (run via call parameters)

Opportunities:
--gu - Get list of users created for testing
--gg - Get list of groups created for testing
--cu - Clean all users created for testing
--cg - Clean all groups created for testing
--full - Full get and clean data created for testing

example:
LOCAL: python cleaner_r.py --gu --cu --gg --cg
REMOTE: cat ./cleaner_p.py | rsh rhel python - --full

@Developed by AleksNeStu

"""

import commands	 #Execute shell commands via os.popen() and return status, output
import re		 #Support for regular expressions (RE)
from optparse import OptionParser


#add options in
parser = OptionParser()
parser.add_option("--gu", action="store_true", dest="gu", default=False, help="Get list of users created for testing")
parser.add_option("--gg", action="store_true", dest="gg", default=False, help="Get list of groups created for testing")
parser.add_option("--cu", action="store_true", dest="cu", default=False, help="Clean all users created for testing")
parser.add_option("--cg", action="store_true", dest="cg", default=False, help="Clean all groups created for testing")
parser.add_option("--full", action="store_true", dest="full", default=False, help="Full get and clean data created for testing")
(options, args) = parser.parse_args()

class full_cleaner(object):


#####################Clean all users or groups created for testing########################
#userdel - delete a user account and related files
#-f - force some actions that would fail otherwise
#-r - remove home directory and mail spool
	def clean_users(self):
		for uname in self.users_list:
			cmd = commands.getoutput('/usr/sbin/userdel -r ' + uname)
			print "    User del: " + uname + " / has been done"
			if cmd != "":
				print "    User del: " + uname + " / with errors"
		self.users_list = []

#####################Clean all groups created for testing########################
#groupdel - delete a group
	def clean_groups(self):
		for gname in self.groups_list:
			cmd = commands.getoutput('/usr/sbin/groupdel ' + gname[0])
			print "    Group del: " + gname[0] + " / has been done"
			if cmd != "":
				print "    Group del: " + gname[0] + " / with errors"
		self.groups_list = []


# List of groups
	groups_list = []  # empty list of groups for start
	groups_list_len = len(groups_list)
# List of files
	users_list = []  # empty list of users for start
	users_list_len = len(users_list)

########################Get list of groups created for testing############################
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

#use options
if options.gu is True:
	full_cleaner().get_users()		# --gu GET USERS
if options.gg is True:
	full_cleaner().get_groups()		# --gg GET GROUPS
if options.cu is True:
	full_cleaner().clean_users()	# --cu CLEAN USERS
if options.cg is True:
	full_cleaner().clean_groups()	# --cg CLEAN GROUPS
if options.full is True:
	full_cleaner().get_users()
	full_cleaner().get_groups()
	full_cleaner().clean_users()
	full_cleaner().clean_groups()
exit()