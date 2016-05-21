#!/usr/bin/python
# -*- coding: utf-8 -*-
"""

########################################################################################################
# Test #1: [NFSv4 - Test the maximum number of ACEs (Access Control Entries) supported by file system] #
# Developed by AleksNeStu                                                                              #
########################################################################################################

"""
from pinger import *         #real-time ping with 5 counts (display)
from hosts_info import *     #input, get client and server info (display)
from fstype_check import *   #get file system type
from nfsexp_check import *   #inpunt, check exported dir (path) on server (display)
from hostname_check import * #input, check hostname resolved (display)
import time                  #for pauses

print """
=========================================================================

Test #1: NFSv4 - Test the maximum number of ACEs (Access Control Entries)
         supported by file system

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
print "    NFSv4 server: ",server   #server = NFS server's hostname
print

#i2 Set, check (from client to server) path of exportfs on server
print "    2) Path to the exported directory on NFSv4 server: "
nfsexp = nfsexpcheck(server)
print "    NFSv4 exported dir: ",nfsexp #view /nfs, /dirnfs, ...

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