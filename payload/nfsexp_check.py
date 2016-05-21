#!/usr/bin/python
# -*- coding: utf-8 -*-
r"""Check mount information on NFS server according with inserted path: /nfs, /dirnfs, ...

@Developed by AleksNeStu

"""
import subprocess

def nfsexpcheck(host):
    if not host:
        return
    while True:
        try:
            mount_point_in = str(raw_input("    [input] : "))  #wait inserting of export dir on server side /nfs, /dir/mount ..
######################Get triger value about existing mount directory on the server side (request from client side)
            p = subprocess.Popen(["showmount", "-e", host], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            pp, err = p.communicate()
            check = pp.find(mount_point_in)
            if check != -1:
                print "    NFS server's exported directory is existing"
                return mount_point_in
            else:
                raise ValueError("    NFS server's exported directory isn't existing")
            break
        except ValueError as check_err:
            print check_err