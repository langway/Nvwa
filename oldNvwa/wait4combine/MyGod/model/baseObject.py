#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
万物之源
>>> print("No Test")
No Test
"""
__author__ = 'Liuyl'
import uuid


class BaseObject(object):
    def __init__(self):
        self.uuid = uuid.uuid1()


if __name__ == '__main__':
    import doctest

    doctest.testmod()
