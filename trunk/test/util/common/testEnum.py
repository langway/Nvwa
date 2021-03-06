#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase


class TestEnum(TestCase):
    def setUp(self):
        print ("----setUp----")

    def testGetName(self):
        print ("----testGetName----")
        x = MyEnum.getName(1)
        print ("X =", eval("MyEnum."+x))
        self.assertEqual("X", x)
        y = MyEnum.getName("ABC")
        print ("Y =", eval("MyEnum."+y))
        self.assertEqual("Y", y)

    def testGetValue(self):
        print ("----testGetValue----")
        x = MyEnum.getValue('X')
        print ("X =", eval("MyEnum.X"))
        self.assertEqual(1, x)
        y = MyEnum.getValue("Y")
        print ("Y =", eval("MyEnum.Y"))
        self.assertEqual("ABC", y)

    def testEnum(self):
        print ("----testEnum----")
        value = "我是一个测试"
        try:
            MyEnum.Y = value
        except Exception as ex:
            print(ex)
        y = MyEnum.Y
        self.assertNotEqual(y, value)
        print (MyEnum.Y, "<>", value)

    def tearDown(self):
        print ("----tearDown----")

from loongtian.util.common.enum import Enum

class MyEnum(Enum):
    X = 1
    Y = "ABC"
MyEnum = MyEnum()