#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Leon"

"""
女娲中央大脑启动器
"""
from loongtian.nvwa.organs.centralBrain import CentralBrain

def startCentralBrain():
    from loongtian.nvwa.organs.centralManager import CentralManager

    CentralManager._cleanDB(wait_for_command=True)

    _CentralBrain = CentralBrain()
    _CentralBrain.init()
    _CentralBrain.run()

if __name__ == "__main__":
    startCentralBrain()
