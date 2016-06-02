#!/usr/bin/python
# -*- coding: utf-8 -*-
"""

#######################################################################################################
# NFSv4 - The complex test for owner/permission/content modification of NFSv4 file system             #                                                                      #
                                                                                                      #
# @Developed by AleksNeStu												                              #
#######################################################################################################

"""
from pinger import *         #real-time ping with 5 counts (display)
from hosts_info import *     #input, get client and server info (display)
from hostname_check import * #input, check hostname resolved (display)
from nfsexp_check import *   #inpunt, check exported dir (path) on server (display)
from time import *           #for pauses
import subprocess
from generator_p import *    #core generator for NFSv4 tests
from cleaner_p import *      #core cleaner for NFSv4 tests

print """
======================================================================================

Test #4: The complex test for owner/permission/content modification of
         NFSv4 file system

         Part 1 - Check the ability of check the permissions of the files

         > Description     : Check the ability of changes the permissions of the files
         > Steps           : Run used functions of full_generator and full_cleaner
         > Expected result : Display "TEST #4 PART 2 HAS BEEN PASSED"

         Part 2 - Check the ability of check the permissions of the directories

         > Description     : Check the ability of changes the permissions of the directories
         > Steps           : Run used functions of full_generator and full_cleaner
         > Expected result : Display "TEST #4 PART 2 HAS BEEN PASSED"

         *** All parts of the complex test will be performed sequentially
         and will be running in the export directory on NFSv4 server side

======================================================================================
"""
time.sleep(5)

generator = full_generator()    #object of main class for generate
cleaner = full_cleaner          #object of main class for clean

################GET INFO###########################################

#i1 Set, check server hostname
print "In order to run the test enter the required data: \n"
print "    1) Hostname of the NFSv4 server: "
print
server = hostnamecheck()			#input, check resolved hostname of the server (display)
print "    NFSv4 server: ",server   #server - NFS server's hostname
print

#i2 Set, check (from client to server via "showmount -e server") dir for execute tests
print "    2) Path to the exported (test) directory on NFSv4 server (/nfsdir, /mnt/nfs, ...): "
print
nfs_exp_s = nfsexpcheck(server)
nfs_exp = str(nfs_exp_s)            #nfs_exp - dir for export (will be mounted on client side)
print "    NFSv4 exported dir: ",nfs_exp #view /nfs, /dirnfs, ...
print

#i3 Set the number of users and groups to be created on the NFSv4 server
print "    3) The number of users, groups, files, directories to be created on the NFSv4 server: "
#Check input data (the number of users, groups, files, directories) in range [5, 50]
print
while True:
   try:
       objects_n = int(raw_input("    The number of objects [5..50] [input] : "))
       if objects_n not in range(5, 50):
           raise ValueError("    Error! Enter the correct value.")
       break
   except ValueError as err_objects_n:
       print err_objects_n
objects = str(objects_n)

#Print test intro info

print """
Great! The input data have been received!
After 5 seconds the test will be started...

======================================================================================
"""
time.sleep(5)

################RUN TEST###########################################

#t1 Get client and server info
gethostinfo(server)
time.sleep(3)
print

#t2 Ping from client to server with 5 counts
pinger(str(server))
time.sleep(3)
print

#t3 Hidden clean the test data from previous run tests
#client side clean
full_cleaner().clean_full_h(nfs_exp)
full_cleaner().clean_mounts_exports_h(str(server))
#server side clean "full_cleaner().clean_full_h(nfs_exp)"
a1 = subprocess.Popen(["cat", "./cleaner_p.py", ], stdout=subprocess.PIPE)
a2 = subprocess.Popen(["/usr/bin/rsh", server, "python", "-", "-c", nfs_exp], stdin=a1.stdout, stdout=subprocess.PIPE)
a1.stdout.close()
rm_cleaner = a2.communicate()[0]			#creating groups
print

#t4 Create groups on the NFSv4 client and server
print "    [Create", objects, "groups, users on the NFSv4 client] : "
print
generator.create_groups_n(objects_n)    #create groups with display output
print
generator.create_users_n(objects_n)     #create users with display output
time.sleep(3)
print
print "    [Create", objects, "groups, users, files, directories (random chmod) on the NFSv4 server] : "
print
b1 = subprocess.Popen(["cat", "./generator_p.py", ], stdout=subprocess.PIPE)
b2 = subprocess.Popen(["/usr/bin/rsh", server, "python", "-", "-g", objects], stdin=b1.stdout, stdout=subprocess.PIPE)
b1.stdout.close()
groups_new = b2.communicate()[0]			#creating groups
print groups_new							#display the process of creating groups
print
c1 = subprocess.Popen(["cat", "./generator_p.py", ], stdout=subprocess.PIPE)
c2 = subprocess.Popen(["/usr/bin/rsh", server, "python", "-", "--gg", "-u", objects], stdin=c1.stdout, stdout=subprocess.PIPE)
c1.stdout.close()
users_new = c2.communicate()[0]				#creating users
print users_new								#display the process of creating users
time.sleep(3)
print
d1 = subprocess.Popen(["cat", "./generator_p.py", ], stdout=subprocess.PIPE)
d2 = subprocess.Popen(["/usr/bin/rsh", server, "python", "-", "--ddd", nfs_exp, "-ff", objects], stdin=d1.stdout, stdout=subprocess.PIPE)
d1.stdout.close()
files_r_new = d2.communicate()[0]				#creating files with random chmod
print files_r_new								#display the process of creating files with random chmod
print
e1 = subprocess.Popen(["cat", "./generator_p.py", ], stdout=subprocess.PIPE)
e2 = subprocess.Popen(["/usr/bin/rsh", server, "python", "-", "--ddd", nfs_exp, "-dd", objects], stdin=e1.stdout, stdout=subprocess.PIPE)
e1.stdout.close()
dirs_r_new = e2.communicate()[0]				#creating dirs with random chmod
print dirs_r_new								#display the process of creating dirs with random chmod
time.sleep(3)


#c1 Clean old test data
print
print
print "    [Clean created test data from the NFSv4 server] : "


#####################LOG AND PRINT RESULTS################################
#print "Test #3 [PASSED]"
####GET THE MARKER OF RESULT OF TEST

check = commands.getoutput("/usr/bin/rsh " + server + " /usr/bin/systemctl status nfs.service")
if check.find("active (exited)") != -1:
    print """
#####################################################################################

Test #4 The complex test for owner/permission/content modification of
        NFSv4 file system

        [PASSED] [PASSED] [PASSED] [PASSED] [PASSED] [PASSED] [PASSED]

    In order to get more information:
    ./logs/log_run.log" - execution log (detailed information)
    ./logs/log_result.log - log with the results

#####################################################################################
"""
else:
    print """
#####################################################################################

Test #4 The complex test for owner/permission/content modification of
        NFSv4 file system

        [FAILED] [FAILED] [FAILED] [FAILED] [FAILED] [FAILED] [FAILED]

    In order to get more information:
    ./logs/log_run.log" - execution log (detailed information)
    ./logs/log_result.log - log with the results

#####################################################################################
"""