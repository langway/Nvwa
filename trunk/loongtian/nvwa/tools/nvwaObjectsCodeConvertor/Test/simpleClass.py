#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon（梁冰）'
"""
创建日期：2015-09-30
"""


class TestA:
    # _PropertyA=''

    PropertyB = 123

    @property
    def PropertyA(self):
        return self._PropertyA

    @PropertyA.setter
    def PropertyA(self, value):
        self._PropertyA = value

    def FuncA(self):
        print(5 == 1 + 1)
        print(6 == 4)
        pass

    pass


class TestB():

    def FuncB(self):
        pass

    pass


class TestC(object):

    def FuncC(self):
        pass

    pass


class TestD(TestB):
    # 属性的重载
    PropertyB = 234

    # 函数的重载
    def FuncB(self):
        pass

    pass

# a=TestA()
#
# a.FuncA()
