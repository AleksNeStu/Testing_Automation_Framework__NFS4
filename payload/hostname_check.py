#!/usr/bin/python
# -*- coding: utf-8 -*-
r"""Check if a remote hostname is resolved to ip

def hostname_res(host):
1 - True
0 - False

def hostnamecheck():
is resolved (print)
isn't resolved (print)
Check maintain table of exported NFS file systems.
@Developed by AleksNeStu

"""
import socket

def hostnamecheck():
    while True:
        try:
            host_in = str(raw_input("    [input] : "))
####################resolve remote hostname to ip ###################
            def hostname_res(host):
                try:
                    socket.gethostbyname(host)
                    return 1
                except socket.error:
                    return 0
################################################1 - True, 0 - False####
            hr = hostname_res(host_in)

            if hr == 1:
                print "    hostname have resolved"
                return host_in
            else:
                raise ValueError ("    hostname haven't resolved")
            break
        except ValueError as check_err:
            print check_err