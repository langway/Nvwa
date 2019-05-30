#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase
from loongtian.nvwa.models.instinctEntity import InstinctEntity

class TestInstinctEntity(TestCase):
    def setUp(self):
        print("----setUp----")


    def testRefreshReals(self):
        print("----testGetRealIds----")
        result = InstinctEntity.getAllByConditionsInDB()
        print(result)

    def tearDown(self):
        print("----tearDown----")