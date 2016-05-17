#!/usr/bin/python
# -*- coding: utf-8 -*-

#Testcases for testing NFSv4 file system on linux-like systems
#Developed by AleksNeStu
#A.V.Nesterovich@gmail.com

import sys
import socket
from os import *
import curses


#------------------MENU-----------------------------------
def get_param(prompt_string):
     screen.clear()
     screen.border(0)
     screen.addstr(2, 2, prompt_string)
     screen.refresh()
     input = screen.getstr(10, 10, 60)
     return input

def execute_cmd(cmd_string):
     system("clear")
     a = system(cmd_string)
     print ""
     if a == 0:
          print "Command executed correctly"
     else:
          print "Command terminated with error"
     raw_input("Press enter")
     print ""

x = 0

while x != ord('4'):
     screen = curses.initscr()

     screen.clear()
     screen.border(0)
     screen.addstr(2, 2, "<NFSv4 test suite> [Run on client-side!!!]")
     screen.addstr(4, 4, "1 - Check the test environment")
     screen.addstr(5, 4, "2 - Run test #1 {ACls with long length}")
     screen.addstr(6, 4, "3 - Run test #2 {ACLs ...}")
     screen.addstr(7, 4, "4 - Run test #3 {ACLs ...}")
     screen.addstr(8, 4, "5 - Run test #4 {xxx}")
     screen.addstr(9, 4, "6 - Run test #5 {yyy}")
     screen.addstr(10, 4, "7 - Run test #1-5 {Complex}")
     screen.addstr(11, 4, "8 - Exit")
     screen.refresh()

     x = screen.getch()

     if x == ord('1'):
          curses.endwin()
          execute_cmd("uname -a")

     if x == ord('2'):
          curses.endwin()
          execute_cmd("df -h")

     if x == ord('3'):
          curses.endwin()
          execute_cmd("pwd -P")

     if x == ord('4'):
          curses.endwin()
          execute_cmd("cat /etc/hosts")

     if x == ord('5'):
          curses.endwin()
          execute_cmd("fdisk -l")

     if x == ord('6'):
          curses.endwin()
          execute_cmd("time")

     if x == ord('7'):
          print("NFSv4")


curses.endwin()
#------------------MENU-----------------------------------