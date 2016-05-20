![main window of program](https://github.com/AleksNeStu/NFSv4/blob/master/Screen.png)
LICENSE
=======
Free for personal use:)

1. The brief overview of the project:
=====================================
Test cases for automatic testing of NFSv4 file system on Linux-like systems.
Subject of testing: content, ACLs (Access Control Lists), etc.

2. Project description:
=======================
The structure of the project:
- "./RFC/" - the directory which contains RFC documents about NFSv4 and ACLs;
- "./cursesmenu/" - the directory which contains python module "The simple console menu system using the curses library";
- "./logs/" - the directory which contains the execution results (log-files in text format) [log_run.log, log_result.log];
- "./payload/" - the directory which contains a set of tests (each file is a separate test) *** can be supplemented;
- "./Readme.pdf" - the full description of my work with the project and useful info [Intro, NFSv4, ACLs, Test task, Test Implementation];
- "./Screen.png" - the program's appearance;
- "./run.py" - the main file [MENU: Read Help, Check test environment, Run test cases (5 tests), Exit].

Help:
-----
In order quick start run "./run.py" and and navigate on it.
-Read Help @Run to see this help:)
-Check test environment @Run to step-by-step to run the test client and server on the possibility of testing
-Run test cases (5 tests, Exit] @Run to execute test separately and all at once
 -Test #1: NFSv4 test case [Limits the length of the ACLs attributes]
 -Test #2 - ***
 -Test #3 - ***
 -Test #4 - ***
 -Test #5 - ***
 -Test #1..5 - ***
-Exit - Exit from program @Run to exit from program

The technologies of the project:
------------------------------
- Linux-like systems (e.q. Fedora 23 x86-64, RHEL 7.2 x86-64);
- Python with 2.7 interpreter with standart library + addition local modules;
- Bash-scripting (use in Python code);
- IDE (Pycharm 2016.1 + Plugins);
- Editor (Sublime Text 3).

3. Technical requirements
=========================
In order to run the tests:
- Linux-like system (preferably RedHat-base with support of NFS4);
- Tools + settings (according "Readme.pdf" file);
- Python interpreter 2.x or 3.x (preferably v.2.7) + additions modules (according "Readme.pdf" file);
In order to clone the project from git-hub: https://github.com/AleksNeStu/NFSv4.git:
- internet-connection :)
In order to view the full description documentation file "Readme.pdf":
- any pdf viewer or browser.
A little time and desire...

4. Useful references:
=====================
- RFC7530 Network File System (NFS) Version 4 Protocol: https://www.rfc-editor.org/rfc/rfc7530.txt;
- RFC7531 Network File System (NFS) Version 4 External Data Representation Standard (XDR) Description: https://www.rfc-editor.org/rfc/rfc7531.txt;
- Mapping Between NFSv4 and Posix Draft ACLs: http://www.citi.umich.edu/projects/nfsv4/rfc/draft-ietf-nfsv4-acl-mapping-05.txt;
- acl - Access Control Lists (Linux man page) *POSIX: http://linux.die.net/man/5/acl;
- exports - NFS server export table (Linux man page): http://linux.die.net/man/5/exports;
- exportfs - maintain table of exported NFS file systems(Linux man page): http://linux.die.net/man/8/exportfs;
- rpc.mountd - NFS mount daemon (Linux man page): http://linux.die.net/man/8/mountd;
- getfacl - get file access control lists (Linux man page): http://linux.die.net/man/1/getfacl;
- setfacl - set file access control lists (Linux man page)	http://linux.die.net/man/1/setfacl.

5. Contacts:
============
mail: Private
Skype: Private

CONCLUSION:
===========
Thank you all, I believe that Linux-solutions and Python are very useful technology for all people of all ages...
Enjoy and have a nice day:) 
See you soon!!!