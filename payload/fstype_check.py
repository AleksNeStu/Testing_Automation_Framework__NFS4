#!/usr/bin/python
# -*- coding: utf-8 -*-
r"""Check the type of the file system


This module provides check the type of file system after entering the mount point
In order to use it need call it:
fstypecheck("/")
print(fstypecheck("/"))   >>>      ext4, xfs, ext3...
"/" - mount point (path to directory)
@Developed by AleksNeStu

"""
import psutil
# from optparse import OptionParser
#
# parser = OptionParser()
# parser.add_option("-p", "--path", dest="rpath",type="str",help="path to mount dir")
# (options, args) = parser.parse_args()

def fstypecheck(path):
    type_root = ""
    for part in psutil.disk_partitions():
        if part.mountpoint == '/':
            type_root = part.fstype
            continue
        if path.startswith(part.mountpoint):
             return part.fstype
    return type_root