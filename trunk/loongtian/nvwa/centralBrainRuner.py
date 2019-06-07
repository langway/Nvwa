#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Leon"

"""
女娲中央大脑启动器
"""
from loongtian.nvwa.organs.centralBrain import CentralBrain

if __name__ == "__main__":
    from loongtian.nvwa.organs.centralManager import CentralManager

    CentralManager._cleanDB(wait_for_command=True)

    _CentralBrain = CentralBrain()
    _CentralBrain.init()
    _CentralBrain.run()
