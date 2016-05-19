#!/usr/bin/python
# -*- coding: utf-8 -*-

#################################################################
# Testcases for testing NFSv4 file system on linux-like systems #
# Developed by AleksNeStu                                       #
#################################################################

################Import the necessary packages and attributes#####
from os import system
from cursesmenu import *        #availible local version ./cursesmenu https://github.com/pmbarrett314/curses-menu.git
from cursesmenu.items import *  #availible local version ./cursesmenu https://github.com/pmbarrett314/curses-menu.git


################Custom functions##################################
#Function Print hello_world
def hello_world():
    print('Hello, World!')

#Function Execute command
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



#Function Get string parameter

#Function Read & Print file to display  /  print(open('./README.md').read())
#def print_txt(txt_string):
#    o = open(txt_string)
#    print(o.read())

################Custom functions##################################


################MENU##############################################
def main():
    menu = CursesMenu("<NFSv4 test suite> [Run from Client side]", "  MENU:") # Create the root menu
#   item1 = FunctionItem("Read Help", print_txt, ["./README.md"])
#   item1 = CommandItem("Read Help", "python ./test.py")
#   menu1 = FunctionItem("Read Help", execute_cmd, ["cat ./README.md | less"])   #help
#   item1 = FunctionItem("Read Help", execute_cmd, ["print(open('./README.md').read())"])
#   function_item = FunctionItem("Check test environment", execute_cmd, ["ls -lash"])
#   command_item = CommandItem("Command", "python -ui ./13-input.py")
#   submenu = SelectionMenu(["item1", "item2", "item3"])

    menu1 = FunctionItem("Read Help", execute_cmd, ["cat ./README.md | less"])   #help
    menu2 = CommandItem("Check test environment", "python -ui ./payload/test-test.py")

    menu3 = CursesMenu("<NFSv4 test suite> [Run from Client side]", "  Run test cases:")
    test1 = CommandItem("Test #1: NFSv4 test case [Limits the length of the ACLs attributes]", "python -ui ./payload/test1.py")
    test2 = CommandItem("2", "python -ui ./payload/test2.py")
    test3 = CommandItem("3", "python -ui ./payload/test3.py")
    test4 = CommandItem("4", "python -ui ./payload/test4.py")
    test5 = CommandItem("5", "python -ui ./payload/test5.py")
    tests = CommandItem("1..5", "python -ui ./payload/test1_5.py")
    menu3.append_item(test1)
    menu3.append_item(test2)
    menu3.append_item(test3)
    menu3.append_item(test4)
    menu3.append_item(test5)
    menu3.append_item(tests)
    menu4 = SubmenuItem("Run test cases", menu3, menu)

    #Add the items to the menu
    menu.append_item(menu1)
    menu.append_item(menu2)
    menu.append_item(menu4)
    menu.start()
    menu.join()
#show the menu and allow the users to interact

if __name__ == "__main__":
    main()
################MENU##############################################
