#!/usr/bin/python
# -*- coding: utf-8 -*-
r"""Ping of the remote host


This module provides get the type of file system after entering the mount point.
In order to use it need call it:
get_fs_type("/")
print(get_fs_type("/"))   >>>      ext4, xfs, ext3...
"/" - mount point (path to directory)
@Developed by AleksNeStu

"""
import psutil

def fstype(fspath):
    type_root = ""
    for part in psutil.disk_partitions():
        if part.mountpoint == '/':
            type_root = part.fstype
            continue

        if fspath.startswith(part.mountpoint):
            return part.fstype

    return type_root