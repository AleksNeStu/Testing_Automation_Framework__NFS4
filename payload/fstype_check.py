#!/usr/bin/python
# -*- coding: utf-8 -*-
r"""Check the type of the file system


This module provides check the type of file system after entering the mount point

LOCAL USE:
a) without -p
from fstype_check import *
fstypecheck("/")
print(fstypecheck("/"))   >>>      ext4, xfs, ext3...
"/" - mount point (path to directory)
b) with -p
fstype_check.py -p /    "/" - mount point (path to directory)

REMOTE USE:
# In order to execute on remote host from localhost need rsh:
a) without -p
cat ./fstype_check.py | rsh server python -

b) with -p
cat ./fstype_check.py | rsh server python - -p / >>>      ext4, xfs, ext3...

@Developed by AleksNeStu

"""
import psutil
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-p", "--path", dest="rpath",type="str",help="path to mount dir")
(options, args) = parser.parse_args()


def fstypecheck(path):
    type_root = ""
    for part in psutil.disk_partitions():
        if part.mountpoint == '/':
            type_root = part.fstype
            continue
        if path.startswith(part.mountpoint):
             return part.fstype
    return type_root