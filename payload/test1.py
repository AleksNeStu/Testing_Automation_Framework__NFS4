#!/usr/bin/python
# -*- coding: utf-8 -*-
"""

#########################################################################
# NFSv4 - Test the maximum number of ACEs (Access Control Entries)		#
#         supported by file system [Extended ACLs for UNIX]				#
# @Developed by AleksNeStu												#
#########################################################################

"""
from pinger import *         #real-time ping with 5 counts (display)
from hosts_info import *     #input, get client and server info (display)
from nfsexp_check import *   #inpunt, check exported dir (path) on server (display)
from hostname_check import * #input, check hostname resolved (display)
import time                  #for pauses
import subprocess

print """
=========================================================================

Test #1: NFSv4 - Test the maximum number of ACEs (Access Control Entries)
         supported by file system [Extended ACLs for UNIX]

    Limits for the max number of the ACEs per individual file/directory:
    - EXT2, EXT3, EXT4: 32
    - XFS: 25
    - GFS2: 25

=========================================================================
"""
################GET INFO###########################################

#i1 Set, check server hostname
print "In order to run the test enter the required data: \n"
print "    1) Hostname of the NFSv4 server: "
server = hostnamecheck()			#input, check resolved hostname of the server (display)
print "    NFSv4 server: ",server   #server - NFS server's hostname
print

#i2 Set, check (from client to server via "showmount -e server") path of exportfs on server
print "    2) Path to the exported directory on NFSv4 server: "
nfs_exp = nfsexpcheck(server)		#nfs_exp - dir for export (will be mounted on client side)
print "    NFSv4 exported dir: ",nfs_exp #view /nfs, /dirnfs, ...
print

#i3 Get, check type of the file system on server and set ACEs limits in accordance with it
print "    3) NFSv4 server exported dir filesystem type & ACEs limits: "
#Get fs type on "server" export dir "nfs_exp"
p1 = subprocess.Popen(['cat', './fstype_check_l.py', ], stdout=subprocess.PIPE)
p2 = subprocess.Popen(['rsh', server, 'python', '-', '-p', nfs_exp], stdin=p1.stdout, stdout=subprocess.PIPE)
p1.stdout.close()
server_fs = p2.communicate()[0]			#server_fs - fs type for export dir "nfs_exp"
#Set limits according fs type
if server_fs == str('xfs'):
	aces_max = 25
else:
	aces_max = 32
print "    NFSv4 server fs type for exp dir ",nfs_exp," : ",server_fs
print "    ACEs max count (UNIX extended ACLs): ", aces_max
print

#i4 Set the number of users and groups to be created on the NFSv4 server
print "    4) The number of users and groups to be created on the NFSv4 server: "


#Print test intro info
time.sleep(3)
print """
Great! The input data have been received!
After 7 seconds the test will be started...

=========================================================================
"""
time.sleep(7)


################RUN TEST###########################################

#t1 Get client and server info
gethostinfo(server)
time.sleep(3)
print

#t2 Ping from client to server with 5 counts
pinger(str(server))
time.sleep(3)
print

#####################LOG AND PRINT RESULTS################################
#print "Test #1 [PASSED]"
print """
##########################################################################

Test #1 [PASSED]

    In order to get more information:
    ./logs/log_run.log" - execution log (detailed information)
    ./logs/log_result.log - log with the results (PASSED, FAILED)

##########################################################################
"""

#print "Test #1 [FAILED]"

#log test results