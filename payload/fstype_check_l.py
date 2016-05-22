#!/usr/bin/python
# -*- coding: utf-8 -*-
r"""Local check the type of the file system (call with parametr -p)


This module provides check the type of file system after entering the mount point
USE:
fstype_check.py -p /    "/" - mount point (path to directory)

#bash:
mount | grep "^$(df -Pk . | head -n 2 | tail -n 1 | cut -f 1 -d ' ') " | cut -f 5 -d ' '

@Developed by AleksNeStu

"""
import psutil
from optparse import OptionParser

#add options
parser = OptionParser()
parser.add_option("-p", "--path", dest="p",type="str",help="path to mount dir on the localhost")
(options, args) = parser.parse_args()
np = options.p

#local fs type check
def fstypecheckp(np):
    type_root = ""
    for part in psutil.disk_partitions():
        if part.mountpoint == '/':
            type_root = part.fstype
            continue
        if  np.startswith(part.mountpoint):
            return part.fstype
        return type_root

print (fstypecheckp(np))  #print for call with python ./fstype_check.py -p /