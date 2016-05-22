#!/usr/bin/python
# -*- coding: utf-8 -*-
r"""Check the type of the file system (call with parametr -p)


This module provides check the type of file system after entering the mount point

LOCAL USE:
fstype_check.py -p /    "/" - mount point (path to directory)

REMOTE USE:
with -p
cat ./fstype_check.py | rsh server python - -p / >>>      ext4, xfs, ext3...

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

def fstypecheckp(p):
    type_root = ""
    for part in psutil.disk_partitions():
        if part.mountpoint == '/':
            type_root = part.fstype
            continue
        if  p.startswith(part.mountpoint):
            return part.fstype
        return type_root

print (fstypecheckp(p))  #print for call with python ./fstype_check.py -p /