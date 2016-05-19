#!/usr/bin/python
# -*- coding: utf-8 -*-

import platform   #in order to get uname info
import socket #in order get IP, hostname (remote, local)
import time
#from socket import *
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
client_uname = platform.system(), platform.release(), platform.version(), platform.machine()

#Get remote server hostname, IP
while True:
    try:
        server = str(raw_input("Please enter NFSv4 server hostname: "))
        server_ip = socket.gethostbyname(server)
        break
    except socket.gaierror:
        print "Error, Enter correct information, for example: servernfs, smain, ..."

#Get ACL attributes
acl_max = int(raw_input("Please enter server hostname | max=35 |: "))


print("""
=========================================================================
""")
print "[Client]"
print "uname    : ",client_uname
print "hostname : ",client
print "ip       : ",client_ip
print
print "[Server]"
print "hostname : ",client
print "ip       : ",client_ip
print("""
=========================================================================
""")
print("Test")
time.sleep(60)
print