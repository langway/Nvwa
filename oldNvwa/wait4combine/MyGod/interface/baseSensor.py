#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
感知器基类
>>> print("No Test")
No Test
"""
__author__ = 'Liuyl'


class BaseSensor(object):
    def __init__(self, buff):
        self.buff = buff

    def _put(self, value):
        self.buff.put(value)

    def input(self):
        pass


if __name__ == '__main__':
    import doctest

    doctest.testmod()