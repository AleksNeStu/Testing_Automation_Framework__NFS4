#!/usr/bin/python
# -*- coding: utf-8 -*-

#######################################################################
# Ping command and display back in real-time output                   #
# Developed by AleksNeStu                                             #
#######################################################################

import subprocess
import sys

#Function of ping the host with 3 counts
def pinger(host):
    if not host:
        return
    ping_t = subprocess.Popen(["ping", "-c3", host], stderr=subprocess.PIPE)
    while True:
        out = ping_t.stderr.read(1)
        if out == '' and ping_t.poll() != None:
            break
            print ("Server: ", host, "is not available")
        if out != '':
            sys.stdout.write(out)
            sys.stdout.flush()