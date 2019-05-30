#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

from unittest import TestCase
from loongtian.nvwa.organs.centralBrain import CentralBrain

class TestBrain(TestCase):

    def setUp(self):
        print ("----setUp----")
        self.central_brain=CentralBrain()
        from loongtian.nvwa.organs.centralManager import CentralManager
        CentralManager._cleanDB(wait_for_command=False)
        self.central_brain.init()
        # self.brain.initMemory()

    # def testCreateAdminConsoleServer(self):
    #     print("——testCreateAdminConsoleServer——")
    #     self.central_brain.createAdminConsoleServer()
    #
    # def testCreateAdminConsole(self):
    #     print("——testCreateAdminConsole——")
    #     self.central_brain.getAdminConsole()