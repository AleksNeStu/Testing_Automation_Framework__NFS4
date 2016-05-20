#!/usr/bin/python
# -*- coding: utf-8 -*-
r"""Get info about local host and remote host (manual input)


This module provides the geting information (Uname, Hostname, IP) from local host and remote host with display it.
local host - auto
remote host - after input hostname
In order to use it need call:
get_hosts_info(rmhost)
rmhost - hostname of the remote hosst
@Developed by AleksNeStu

"""
import socket           #in order get IP, hostname (remote, local)
import subprocess       #in order run External Command And Get Output
#import platform        #uname + other

def get_hosts_info(rmhost):
    if not rmhost:
        return
#Get local server hostname, IP, uname
    client = socket.gethostname()
    client_ip = socket.gethostbyname(client)
    client_uname_t = subprocess.Popen(["uname", "-a"], stdout=subprocess.PIPE)  #uname local >>> client_uname
    client_uname = client_uname_t.communicate()                                 #uname local >>> client_uname
    #client_uname = platform.system(), platform.release(), platform.version(), platform.machine()

#Get remote server hostname, IP
    while True:
        try:
#           server = str(raw_input("Please enter the hostname of the remote host: "))  #rmserver
            server_ip = socket.gethostbyname(rmhost)
            break
        except socket.gaierror:
            print "Error! Enter correct information, for example: servename, smain, ..."
# Get remote server uname
    server_uname_t = subprocess.Popen(["rsh","-n", rmhost, "uname -a"], stdout=subprocess.PIPE)  #uname remote >>> sever_uname
    server_uname = server_uname_t.communicate()                                                  #uname remote >>> sever_uname

#Print the received info
    print("""
=============================================================================
    """)
    print "[Client]"
    print "Uname    : ",client_uname
    print "Hostname : ",client
    print "IP       : ",client_ip
    print
    print "[Server]"
    print "Uname    : ",server_uname
    print "Hostname : ",rmhost
    print "IP       : ",server_ip
    print("""
=============================================================================
    """)