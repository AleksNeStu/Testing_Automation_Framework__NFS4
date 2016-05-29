#!/usr/bin/python
# -*- coding: utf-8 -*-
"""

#######################################################################################################
# NFSv4 - Stress test for a large number operations: export/unexport [server], mount/unmount [client] #
# @Developed by AleksNeStu												                              #
#######################################################################################################

"""
from pinger import *         #real-time ping with 5 counts (display)
from hosts_info import *     #input, get client and server info (display)
from hostname_check import * #input, check hostname resolved (display)
import time                  #for pauses
import subprocess
from generator_p import *    #core generator for NFSv4 tests
from cleaner_p import *      #core cleaner for NFSv4 tests

print """
=========================================================================

Test #3: NFSv4 - Stress test for a large number operations:
         [NFSv4 server side] : export / unexport
         [NFSv4 client side] : mount / unmount

         Part 1 - Emulation of export a large number of directories on the
                  NFSv4 server and their subsequent mounting on the NFSv4
                  client, health check NFSv4 service

         Part 2 - Emulation of a large number of random operations with
                  exports on NFSv4 server and mounts on NFSv4 client,
                  health check NFSv4 service

         *** The test data will be created in the directory /mnt/* from
         both sides NFSv4 client and server

=========================================================================
"""
time.sleep(5)
# The test will be focused to server (exportfs util) an
# d client (mount, umount utils)

################GET INFO###########################################

#i1 Set, check server hostname
print "In order to run the test enter the required data: \n"
print "    1) Hostname of the NFSv4 server: "
print
server = hostnamecheck()			#input, check resolved hostname of the server (display)
print "    NFSv4 server: ",server   #server - NFS server's hostname
print

#i2 Set The number of exported (mounted) directories:
print "    2) The number of exported (mounted) directories: "
#Check input data (the number of rxports/mounts) in range [500, 10000]
print
while True:
   try:
       cycles_n = int(raw_input("    The number of directories [500..10000] [input] : "))
       if cycles_n not in range(3, 10001):
           raise ValueError("    Error! Enter the correct value.")
       break
   except ValueError as err_cycles_n:
       print err_cycles_n
cycles = int(cycles_n)
print

#i3 Set The number of random operations:
print "    3) The number of random operations: export/unexport (server), mount/unmount (client): "
#Check input data (the number of random operations) in range [1000, 20001]
print
while True:
   try:
       cycles2_n = int(raw_input("    The number of random operations [1000..20000] [input] : "))
       if cycles2_n not in range(3, 20001):
           raise ValueError("    Error! Enter the correct value.")
       break
   except ValueError as err_cycles2_n:
       print err_cycles2_n
cycles2 = int(cycles2_n)


#Print test intro info

print """
Great! The input data have been received!
After 5 seconds the test will be started...

=========================================================================
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
full_cleaner().clean_mounts_exports_h(str(server))

#t4 # Stress test for export a large number of directories on the NFSv4 server and their subsequent mounting on the NFSv4
# client, health check NFSv4 service
# Operations with server: exportfs; client: mount, unmount.
print """    [Part 1 - Stress test for export a large number of directories on the NFSv4 server
              and their subsequent mounting on the NFSv4 client] :
"""
time.sleep(2)
full_generator().test_stress_exports_1(str(server), cycles)
print
time.sleep(3)

check_export = commands.getoutput("showmount -e " + server + " | grep nfs_exp" + str(cycles))
check_mount = commands.getoutput("/usr/bin/mount | grep nfs_mnt" + str(cycles))
if check_export.find(str(cycles)) !="" and check_mount.find(str(cycles)) != "":
    print
    print """    [Part 2 - Stress test for large number random operations: exports:
                  export/unexport (NFSv4 server), mount/unmount (NFSv4 client)] :
    """
    time.sleep(2)
    full_generator().test_stress_exports_2(server, cycles2)
    time.sleep(3)
else:
    print "    THE TEST #3 PART 1 HAS BEEN FAILED!!!"  # The test has been passed

#c1 Clean old test data
print
print
print "    [Clean created test data from the NFSv4 client and server] : "
full_cleaner().clean_mounts_exports(server)
time.sleep(3)

#####################LOG AND PRINT RESULTS################################
#print "Test #3 [PASSED]"
####GET THE MARKER OF RESULT OF TEST

check = commands.getoutput("/usr/bin/rsh " + server + " /usr/bin/systemctl status nfs.service")
if check.find("active (exited)") != -1:
    print """
##########################################################################

Test #3 NFSv4 - Stress test for a large number operations:
        [NFSv4 server side] : export / unexport
        [NFSv4 client side] : mount / unmount

        [PASSED] [PASSED] [PASSED] [PASSED] [PASSED] [PASSED] [PASSED]

    In order to get more information:
    ./logs/log_run.log" - execution log (detailed information)
    ./logs/log_result.log - log with the results

##########################################################################
"""
else:
    print """
##########################################################################

Test #3 NFSv4 - Stress test for a large number operations:
        [NFSv4 server side] : export / unexport
        [NFSv4 client side] : mount / unmount

        [FAILED] [FAILED] [FAILED] [FAILED] [FAILED] [FAILED] [FAILED]

    In order to get more information:
    ./logs/log_run.log" - execution log (detailed information)
    ./logs/log_result.log - log with the results

##########################################################################
"""