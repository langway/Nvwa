#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase

import loongtian.util.pip.pipHelper   as pipHelper


class TestPipHelper(TestCase):

    def setUp(self):
        print("----setUp----")

    def testInstallAll(self):
        print("----testInstallAll----")
        COMPONENTS=["pip","wheel"]
        pipHelper.installAll(COMPONENTS)

    def testUpdateAll(self):
        print("----testUpdateAll----")
        pipHelper.updateAll()


    def tearDown(self):
        print("----tearDown----")