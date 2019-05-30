#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Administrator'

from unittest import TestCase
import loongtian.util.helper.python2to3Helper as python2to3Helper

class TestPipHelper(TestCase):

    def setUp(self):
        print("----setUp----")

    def testConvert(self):
        print("----testConvert----")
        python2to3Helper.convert("")


    def tearDown(self):
        print("----tearDown----")