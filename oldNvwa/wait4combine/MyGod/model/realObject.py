#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
新建python文件
>>> print("No Test")
No Test
"""
__author__ = 'Liuyl'
from baseObject import BaseObject as BaseObject


class RealObject(BaseObject):
    def __init__(self):
        super(RealObject, self).__init__()


if __name__ == '__main__':
    import doctest

    doctest.testmod()
