#!/usr/bin/python
# -*- coding: utf-8 -*-

#######################################################################
# Test #1: NFSv4 test case [Limits the length of the ACLs attributes] #
# Developed by AleksNeStu                                             #
#######################################################################

import socket #in order get IP, hostname (remote, local)
import time
import subprocess  #in order run External Command And Get Output
from pinger import *      #real-time ping module with 5 counts
#import platform
##in order to get uname info#from socket import *
#from socket import gaierror

print("""
=========================================================================
Test #1: NFSv4 test case [Limits the length of the ACLs attributes]\n
   Limits the length of the ACLs attributes:
   - Up to 35 ACL entries per ACL page
   - Up to 6 character in attribute "user"
   - Up to 10 character in attribute "domain"
=========================================================================
""")

################GET INFO###########################################
print("<In order to run test case fill the required details...>")
print

#Get local server hostname, IP, uname
client = socket.gethostname()
client_ip = socket.gethostbyname(client)
client_uname_t = subprocess.Popen(["uname", "-a"], stdout=subprocess.PIPE)  #uname local >>> client_uname
client_uname = client_uname_t.communicate()                                 #uname local >>> client_uname
#client_uname = platform.system(), platform.release(), platform.version(), platform.machine()

#Get remote server hostname, IP
while True:
    try:
        server = str(raw_input("Please enter NFSv4 server hostname: "))
        server_ip = socket.gethostbyname(server)
        break
    except socket.gaierror:
        print "Error! Enter correct information, for example: servernfs, smain, ..."
# Get remote server uname
server_uname_t = subprocess.Popen(["rsh","-n", server, "uname -a"], stdout=subprocess.PIPE)  #uname remote >>> sever_uname
server_uname = server_uname_t.communicate()                                                  #uname remote >>> sever_uname

#Get the length of the ACLs attributes
while True:
    try:
        acl_max = int(raw_input("Please enter the length of the ACLs attributes (30..35): ")) #30 <= acl_max <= 35:
        if acl_max not in range(30, 36):
            raise ValueError("Error! Enter correct information, a value in the range: 30..35")
        break
    except ValueError as acl_err:
        print acl_err

#Print intro info
print("""
=========================================================================
""")
print "[Client]"
print "Uname    : ",client_uname
print "Hostname : ",client
print "IP       : ",client_ip
print
print "[Server]"
print "Uname    : ",server_uname
print "Hostname : ",server
print "IP       : ",server_ip
print
print("""
=========================================================================
""")
time.sleep(3)
#ping call from module pinger
print
print "[Ping Client --->>> Server]"
sserver=str(server)
pinger(sserver)
print
print("Ping is done with status OK.")
print("""
=========================================================================
""")
print('The test will be started in 10 seconds')
time.sleep(10)
print "GO!"