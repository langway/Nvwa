#!/usr/bin/env python
# coding: utf-8

from unittest import TestCase
from loongtian.util.common.singleton import singleton


class TestSingleton(TestCase):
    def setUp(self):
        print ("----setUp----")

    def testSingleton(self):
        print ("----testSingleton----")
        s1 = SingletonClass()
        s1.name = "Singleton1"
        self.assertEqual("Singleton1", s1.name)

        s2 = SingletonClass()
        s2.name = "Singleton2"
        self.assertEqual("Singleton2", s2.name)

        self.assertEqual("Singleton2", s1.name)
        m1 = MultipleClass()
        m2 = MultipleClass()
        self.assertEqual(s1, s2)
        self.assertNotEqual(m1, m2)

    def tearDown(self):
        print ("----tearDown----")
        
@singleton
class SingletonClass(object):
    pass

class MultipleClass(object):
    pass
