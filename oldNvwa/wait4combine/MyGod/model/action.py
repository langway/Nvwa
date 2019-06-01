#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
新建python文件
>>> print("No Test")
No Test
"""
__author__ = 'Liuyl'
from baseObject import BaseObject as BaseObject


class Action(BaseObject):
    def __init__(self):
        super(Action, self).__init__()
        self.__pre = None  # 应该是一个Relation对象
        self.__post = None  # 应该是一个Relation对象


if __name__ == '__main__':
    import doctest

    doctest.testmod()
