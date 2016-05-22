#!/usr/bin/python
# -*- coding: utf-8 -*-
r"""The test data generator for testing NFSv4 and ACLs

Opportunities:
- Create a user in available groups to do the tests
- Create a users according to specified range (after input count)
- Clean all users created for tests
- Clean all groups created for tests
- Retrieve the list of user from /etc/passwd file
-
@Developed by AleksNeStu

"""

import commands
import random
import re