#!/usr/bin/python
# -*- coding: utf-8 -*-
r"""Get info from client and server


info: uname, hostname, IP
client info - auto
server info - after receive server hostname
@Developed by AleksNeStu

"""
import socket           #IP, hostname (remote, local)
import subprocess       #parsing and display external commands

def gethostinfo(host):
    if not host:
        return
#Get client info (hostname, IP, uname)
    client = socket.gethostname()
    client_ip = socket.gethostbyname(client)
    client_uname_t = subprocess.Popen(["uname", "-srp"], stdout=subprocess.PIPE)  #uname local >>> client_uname
    client_uname = client_uname_t.communicate()                                 #uname local >>> client_uname
    #client_uname = platform.system(), platform.release(), platform.version(), platform.machine()

#Get server info (hostname, IP, uname)
    server_uname_t = subprocess.Popen(["/usr/bin/rsh","-n", host, "uname -srp"], stdout=subprocess.PIPE)  #uname remote >>> sever_uname
    server_uname = server_uname_t.communicate()
    server_ip = socket.gethostbyname(host)

#Print the received from client and server info
    print "    Client   : ",client_uname
    print "    Hostname : ",client
    print "    IP       : ",client_ip
    print
    print "    Server   : ",server_uname
    print "    Hostname : ",host
    print "    IP       : ",server_ip