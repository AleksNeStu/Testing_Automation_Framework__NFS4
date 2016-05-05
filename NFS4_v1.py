#!/usr/bin/python
# -*- coding: utf-8 -*-

#Test cases for test NFS4 on linux systems (python, git, Pycharm)
#A.V.Nesterovich@gmail.com
#I must do it

import sys
print('')
print('''Menu [NFS4 test cases (for Linux base systems)]:
      1. Permission test [xxx]
      2. File attributes [xxx]
      3. ACL test #1 [xxx]
      4. ACL test #2 [xxx]
      5. ACL test #3 [xxx]
      6. Exit [end]
''')

choice = int(input('Your choice: [1,...,6]: '))

if choice == 1:
    print('You have chosen: -=1. Permission test [xxx]=-')
elif choice == 2:
    print('You have chosen: -=2. File attributes [xxx]=-')
elif choice == 3:
    print('You have chosen: -=3. ACL test #1 [xxx]=-')
elif choice == 4:
    print('You have chosen: -=4. ACL test #3 [xxx]=-')
elif choice == 5:
    print('You have chosen: -=5. ACL test #4 [xxx]=-')
else:
    print('Incorrect choice')

#To be continue...

print('deadline of project 01.06.2016')
print()
