#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
新建python文件
>>> print("No Test")
No Test
"""
__author__ = 'Liuyl'
from UserList import UserList as UserList


class Memory(UserList):
    def __init__(self):
        super(Memory, self).__init__()

if __name__ == '__main__':
    import doctest

    doctest.testmod()
