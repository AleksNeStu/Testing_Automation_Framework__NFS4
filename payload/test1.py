#!/usr/bin/python
# -*- coding: utf-8 -*-
"""

#######################################################################
# Test #1: NFSv4 test case [Limits the length of the ACLs attributes] #
# Developed by AleksNeStu                                             #
#######################################################################

"""
from pinger import *        #real-time ping module with 5 counts
from hosts_info import *    #client and server info print
import time                     #pauses
#import platform            #in order to get uname info#from socket import *

print("""
=========================================================================
\nTest #1: NFSv4 test case [Limits the length of the ACLs attributes]
   Limits the length of the ACLs attributes:
   - Up to 35 ACL entries per ACL page
   - Up to 6 character in attribute "user"
   - Up to 10 character in attribute "domain"\n
=========================================================================
""")
################GET INFO###########################################
print("In order to run test case fill the required details:")
#Get from the local client and the remote server info (hostname, IP, uname) and print
server = str(raw_input("    1) Hostname of the remote NFSv4 server: "))
print "   ",server
#Get the length of the ACLs attributes for testing
while True:
    try:
        acl_max = int(raw_input("    2) Length of the ACLs attributes (30..35): ")) #30 <= acl_max <= 35:
        if acl_max not in range(30, 36):
            raise ValueError("Error! Enter correct information, a value in the range: 30..35")
        break
    except ValueError as acl_err:
        print acl_err
print "   ",acl_max
#Print intro info
time.sleep(1)
print("""
=========================================================================

Great! The input data had been received! After 5 seconds the test will be started...
""")
################GET INFO###########################################
time.sleep(5)
################RUN TEST CASE###########################################
#Get client and server info, display it
get_hosts_info(server)
time.sleep(1)
#Ping via pinger of NFSv4 server
pinger(str(server))

print """
##########################################################################
Test #1 [PASSED]
In order to get more information:
./logs/log_run.log" - execution log (detailed information)
./logs/log_result.log - log with the results (PASSED, FAILED)
##########################################################################
"""
#print "Test #1 [FAILED]"