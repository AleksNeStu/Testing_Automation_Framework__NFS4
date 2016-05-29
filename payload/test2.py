#!/usr/bin/python
# -*- coding: utf-8 -*-
"""

#####################################################################################################
# NFSv4 - Stress test for a large number of random operations setting ACEs [Extended ACLs for UNIX] #
# @Developed by AleksNeStu												                            #
#####################################################################################################

"""
from pinger import *         #real-time ping with 5 counts (display)
from hosts_info import *     #input, get client and server info (display)
from nfsexp_check import *   #inpunt, check exported dir (path) on server (display)
from hostname_check import * #input, check hostname resolved (display)
import time                  #for pauses
import subprocess

print """
=========================================================================

Test #2: NFSv4 - Stress test for a large number of random operations
         setting ACEs [Extended ACLs for UNIX]

    The testing of correct operation of the services of NFSv4 server
    with a large number of random operations setting ACEs
    (Access Control Entries)

    Part 1 - Emulate a large number random operations with ACEs for export
             directory on the NFSv4 server, health check NFSv4 service

    Part 2 - Emulate a large number random operations with ACEs for random
             files in export directory on the NFSv4 server, health check
             NFSv4 service

=========================================================================
"""
time.sleep(5)
# The test will be focused to NFS export dir and to the files that will be created in it"

################GET INFO###########################################

#i1 Set, check server hostname
print "In order to run the test enter the required data: \n"
print "    1) Hostname of the NFSv4 server: "
print
server = hostnamecheck()			#input, check resolved hostname of the server (display)
print "    NFSv4 server: ",server   #server - NFS server's hostname
print

#i2 Set, check (from client to server via "showmount -e server") path of exportfs on server
print "    2) Path to the exported directory on NFSv4 server (/nfsdir, /mnt/nfs, ...): "
print
nfs_exp = nfsexpcheck(server)		#nfs_exp - dir for export (will be mounted on client side)
nfs_exp_s = str(nfs_exp)
print "    NFSv4 exported dir: ",nfs_exp #view /nfs, /dirnfs, ...
print

#i3 Set the number of users and groups to be created on the NFSv4 server
print "    3) The number of users and groups to be created on the NFSv4 server: "
#Check input data (the number of users) in range [100, 1000]
print
while True:
   try:
       users_n = int(raw_input("    The number of users [50..1000] [input] : "))
       if users_n not in range(50, 1001):
           raise ValueError("    Error! Enter the correct value.")
       break
   except ValueError as err_users_n:
       print err_users_n
users = str(users_n)
#Check input data (the number of groups) in range [100, 999]
while True:
   try:
       groups_n = int(raw_input("    The number of groups [50..1000] [input] : "))
       if groups_n not in range(50, 1001):
           raise ValueError("    Error! Enter the correct value.")
       break
   except ValueError as groups_n:
       print groups_n
groups = str(groups_n)
print

#i4
print "    4) The number of files to be created in the export dir on the NFSv4 server: "

print
while True:
   try:
       files_n = int(raw_input("    The number of files [10..50] [input] : "))
       if files_n not in range(10, 51):
           raise ValueError("    Error! Enter the correct value.")
       break
   except ValueError as err_files_n:
       print err_files_n
files = str(files_n)
print

print "    5) The number of cycles to perform random operation in the test: "
#Check input data (the number of cycles) in range [500, 10000]
print
while True:
   try:
       cycles_n = int(raw_input("    The number of cycles [500..10000] [input] : "))
       if cycles_n not in range(500, 10001):
           raise ValueError("    Error! Enter the correct value.")
       break
   except ValueError as err_cycles_n:
       print err_cycles_n
cycles = str(cycles_n)


#Print test intro info

print """
Great! The input data have been received!
After 5 seconds the test will be started...

=========================================================================
"""
time.sleep(5)


################RUN TEST###########################################

#t0 Get client and server info
gethostinfo(server)
time.sleep(3)
print

#t1 Ping from client to server with 5 counts
pinger(str(server))
time.sleep(3)
print

#t2 Hidden clean the data from previous run tests
a1 = subprocess.Popen(["cat", "./cleaner_p.py", ], stdout=subprocess.PIPE)
a2 = subprocess.Popen(["/usr/bin/rsh", server, "python", "-", "-c", nfs_exp_s], stdin=a1.stdout, stdout=subprocess.PIPE)
a1.stdout.close()
hidden_clean = a2.communicate()[0]

#t3 Create groups on the NFSv4 server
print "    [Create", groups, "groups on the NFSv4 server] : "
print
b1 = subprocess.Popen(["cat", "./generator_p.py", ], stdout=subprocess.PIPE)
b2 = subprocess.Popen(["/usr/bin/rsh", server, "python", "-", "-g", groups], stdin=b1.stdout, stdout=subprocess.PIPE)
b1.stdout.close()
groups_new = b2.communicate()[0]			#creating groups
print groups_new							#display the process of creating groups
time.sleep(3)

#t4 Create users on the NFSv4 server
print "    [Create", users, "users on the NFSv4 server] : "
print
c1 = subprocess.Popen(["cat", "./generator_p.py", ], stdout=subprocess.PIPE)
c2 = subprocess.Popen(["/usr/bin/rsh", server, "python", "-", "--gg", "-u", users], stdin=c1.stdout, stdout=subprocess.PIPE)
c1.stdout.close()
users_new = c2.communicate()[0]				#creating users
print users_new								#display the process of creating users
time.sleep(3)

#t5 Run the part 1 of test #2 Stress test for a large number of random operations setting ACEs [Extended ACLs for UNIX]
# Serial setup "cycles" times the option -m (--modify) to modify the ACLs of NFS server export directory
# plus
# Serial setup "cycles" times the option -x (--remove) to remove the ACLs of NFS server export directory
# In addition is exceeding the permissible value of the amount ACEs for file system
print "    [Part 1 - Stress test for a large number random ACEs for export directory on the NFSv4 server] :"
print
d1 = subprocess.Popen(["cat", "./generator_p.py", ], stdout=subprocess.PIPE)
d2 = subprocess.Popen(["/usr/bin/rsh", server, "python", "-", "-d", nfs_exp_s,"-c", cycles], stdin=d1.stdout, stdout=subprocess.PIPE)
d1.stdout.close()
test1 = d2.communicate()[0]				#execution of the test actions
print test1								#display the process of testing
time.sleep(3)

#t6 # Stress test for a large number of random operations setting ACEs [Extended ACLs for UNIX]
# Random operations with setfacl: random options (actions)
print "    [Part 2 - Stress test for a large number random ACEs for random files in export directory on the NFSv4 server] :"
print
e1 = subprocess.Popen(["cat", "./generator_p.py", ], stdout=subprocess.PIPE)
e2 = subprocess.Popen(["/usr/bin/rsh", server, "python", "- ", "-d", nfs_exp_s, "-f", files, "-c", cycles], stdin=e1.stdout, stdout=subprocess.PIPE)
e1.stdout.close()
test2 = e2.communicate()[0]         #execution of the test actions
print test2		                    #display the process
time.sleep(3)

#c1 Clean created files on the NFSv4 server
print "    [Clean created test data from the NFSv4 server] : "
z1 = subprocess.Popen(["cat", "./cleaner_p.py", ], stdout=subprocess.PIPE)
z2 = subprocess.Popen(["/usr/bin/rsh", server, "python", "-", "-r", nfs_exp_s], stdin=z1.stdout, stdout=subprocess.PIPE)
z1.stdout.close()
full_del = z2.communicate()[0]
print full_del								#display the process of cleaning the previously created data
time.sleep(3)

#####################LOG AND PRINT RESULTS################################
#print "Test #1 [PASSED]"
####GET THE MARKER OF RESULT OF TEST
if test1.find("HAS BEEN PASSED") and test2.find("HAS BEEN PASSED"):
    print """
##########################################################################

Test #2 NFSv4 - Stress test for a large number of random operations
        setting ACEs [Extended ACLs for UNIX] [PASSED]

    In order to get more information:
    ./logs/log_run.log" - execution log (detailed information)
    ./logs/log_result.log - log with the results (PASSED, FAILED)

##########################################################################
"""
else:
    print """
##########################################################################

Test #2 NFSv4 - Stress test for a large number of random operations
        setting ACEs [Extended ACLs for UNIX] [FAILED]

    In order to get more information:
    ./logs/log_run.log" - execution log (detailed information)
    ./logs/log_result.log - log with the results (PASSED, FAILED)

##########################################################################
"""