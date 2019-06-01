#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
处理中枢基类
>>> print("No Test")
No Test
"""
__author__ = 'Liuyl'


class BaseCentre(object):
    def __init__(self):
        pass

    def decode(self, information):
        pass

    def encode(self, knowledge):
        pass


if __name__ == '__main__':
    import doctest

    doctest.testmod()
