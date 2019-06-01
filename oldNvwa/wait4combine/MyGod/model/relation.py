#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
新建python文件
>>> print("No Test")
No Test
"""
__author__ = 'Liuyl'
from baseObject import BaseObject as BaseObject


class Relation(BaseObject):
    def __init__(self):
        super(Relation, self).__init__()
        self.__left = None  # 应该是一个RealObject对象
        self.__right = None  # 应该是一个RealObject对象


if __name__ == '__main__':
    import doctest

    doctest.testmod()
