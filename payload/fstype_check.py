#!/usr/bin/python
# -*- coding: utf-8 -*-
r"""Check the type of the file system (call with function)


This module provides check the type of file system after entering the mount point

USE:
from fstype_check import *
fstypecheck("/")
print(fstypecheck("/"))   >>>      ext4, xfs, ext3...
"/" - mount point (path to directory)

#bash:
mount | grep "^$(df -Pk . | head -n 2 | tail -n 1 | cut -f 1 -d ' ') " | cut -f 5 -d ' '

@Developed by AleksNeStu

"""
import psutil
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-p", "--path", dest="rpath",type="str",help="path to mount dir")
(options, args) = parser.parse_args()
p = options.rpath

def fstypecheck(path):
    type_root = ""
    for part in psutil.disk_partitions():
        if part.mountpoint == '/':
            type_root = part.fstype
            continue
        if path.startswith(part.mountpoint):
            return part.fstype
        return type_root