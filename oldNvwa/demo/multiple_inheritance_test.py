#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    multiple_inheritance_test 
Author:   Liuyl 
DateTime: 2014/10/31 16:25 
UpdateLog:
1、Liuyl 2014/10/31 Create this File.

multiple_inheritance_test
>>> print("No Test")
No Test
"""
__author__ = 'Liuyl'


class A(object):
    def foo(self):
        print('A-foo')


class B(A):
    def foo(self):
        print('B-foo')


C = A


class D(C):
    def goo(self):
        self.foo()


class E(A,D):
    pass


if __name__ == '__main__':
    e = E()
    e.goo()