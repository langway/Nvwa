#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
这个是空测试，用来测试unitTestManager对标准测试文件(以test开头，以.py结尾)的区分和读取。
"""
__author__ = 'Leon'

from unittest import TestCase

class MyTestCase(TestCase):

    def setUp(self):
        print ("----setUp----")

    def testSomething(self):
        print ("----testSomething----")
        self.assertEqual(True, False)

    def tearDown(self):
        print ("----tearDown----")
