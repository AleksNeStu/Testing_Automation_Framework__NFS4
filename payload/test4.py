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
import time                  #for pauses
import subprocess
from generator_p import *    #core generator for NFSv4 tests
from cleaner_p import *      #core cleaner for NFSv4 tests

print """
======================================================================================

Test #4: The complex test for owner/permission/content modification of
         NFSv4 file system

         Part 1 - Check the ability of copy, delete, move the files

         > Description     : Check the ability of copy, delete, move the files
         > Steps           : Run used functions of full_generator and full_cleaner
         > Expected result : Display "TEST #4 PART 1 HAS BEEN PASSED"

         Part 2 - Check the ability of changes the permissions of the files

         > Description     : Check the ability of changes the permissions of the files
         > Steps           : Run used functions of full_generator and full_cleaner
         > Expected result : Display "TEST #4 PART 2 HAS BEEN PASSED"

         Part 3 - Check the ability of changes the permissions of the directories

         > Description     : Check the ability of changes the permissions of the directories
         > Steps           : Run used functions of full_generator and full_cleaner
         > Expected result : Display "TEST #4 PART 3 HAS BEEN PASSED"

         Part 4 - Check the ability of check the permissions of the files

         > Description     : Check the ability of changes the permissions of the files
         > Steps           : Run used functions of full_generator and full_cleaner
         > Expected result : Display "TEST #4 PART 4 HAS BEEN PASSED"

         Part 5 - Check the ability of check the permissions of the directories

         > Description     : Check the ability of changes the permissions of the directories
         > Steps           : Run used functions of full_generator and full_cleaner
         > Expected result : Display "TEST #4 PART 5 HAS BEEN PASSED"

         Part 6 - Check the ability of changes the content of the txt files

         > Description     : Check the ability of changes the content of the txt files
         > Steps           : Run used functions of full_generator and full_cleaner
         > Expected result : Display "TEST #3 PART 5 HAS BEEN PASSED"

         Part 7 - Check the ability of check the owner of the files

         > Description     : Check the ability of check the owner of the files
         > Steps           : Run used functions of full_generator and full_cleaner
         > Expected result : Display "TEST #3 PART 3 HAS BEEN PASSED"


         *** All parts of the complex test will be performed sequentially
         and will be running in the export directory on NFSv4 server side

======================================================================================
"""
time.sleep(5)
# The test will be focused to server (owner/permission/content modification of NFSv4 file system

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
nfs_exp_s = nfsexpcheck(server)
nfs_exp = str(nfs_exp_s)            #nfs_exp - dir for export (will be mounted on client side)
print "    NFSv4 exported dir: ",nfs_exp #view /nfs, /dirnfs, ...
print

#i3 Set the number of users and groups to be created on the NFSv4 server
print "    3) The number of users, groups, files, directories to be created on the NFSv4 server: "
#Check input data (the number of users, groups, files, directories) in range [5, 20]
print
while True:
   try:
       objects_n = int(raw_input("    The number of users [5..20] [input] : "))
       if objects_n not in range(5, 21):
           raise ValueError("    Error! Enter the correct value.")
       break
   except ValueError as err_objects_n:
       print err_objects_n
objects = str(objects_n)

print "    4) The number of cycles to perform the tests: "
#Check input data (the number of cycles) in range [1, 10]
print
while True:
   try:
       loops_n = int(raw_input("    The number of cycles [1..10] [input] : "))
       if loops_n not in range(1, 11):
           raise ValueError("    Error! Enter the correct value.")
       break
   except ValueError as err_loops_n:
       print err_loops_n
loops = str(loops_n)


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
full_cleaner().clean_full_h(nfs_exp_s)
full_cleaner().clean_mounts_exports_h(str(server))
full_cleaner().clean_files_h(nfs_exp_s)


#t4 #



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