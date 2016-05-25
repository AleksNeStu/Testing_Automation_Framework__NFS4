#!/usr/bin/python
# -*- coding: utf-8 -*-
r"""Check the type of the file system (call with parametr -p)


This module provides check the type of file system after entering the mount point

LOCAL USE:
fstype_check.py -p /    "/" - mount point (path to directory)

REMOTE USE:
with -p
cat ./fstype_check.py | /usr/bin/rsh server python - -p / >>>      ext4, xfs, ext3...

#bash:
mount | grep "^$(df -Pk . | head -n 2 | tail -n 1 | cut -f 1 -d ' ') " | cut -f 5 -d ' '

@Developed by AleksNeStu

"""
import psutil
from optparse import OptionParser
import subprocess

#add options
parser = OptionParser()
parser.add_option("-s", "--server", dest="s",type="str",help="hostname of the server")
parser.add_option("-p", "--path", dest="p",type="str",help="path to mount dir on the server")
(options, args) = parser.parse_args()
ns = options.s
np = options.p

#remote fs type check
def fstypecheckprem(ns,np):
    if not ns or np:
        return
    r1 = subprocess.Popen(['cat','./fstype_check_l.py',], stdout=subprocess.PIPE)
    r2 = subprocess.Popen(['/usr/bin/rsh',ns,'python','-','-p',np], stdin=r1.stdout, stdout=subprocess.PIPE)
    r1.stdout.close()
    res = r2.communicate()[0]
    if res !=[]:
        print res
        return res

fstypecheckprem(ns,np)