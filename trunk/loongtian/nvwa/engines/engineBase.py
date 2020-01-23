#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
引擎的基础类
"""
__author__ = 'Leon'

from abc import ABC
from loongtian.util.log import logger

class EngineBase(ABC):
    """
    引擎的基础类
    """

    def __init__(self,memory):
        """
        引擎的基础类
        :param memory: 用来存放当前对象的内存空间（避免每次都从数据库中调用）
                       当前Engine的memory是MemoryCentral
        """
        if not memory :
            raise Exception("必须提供存放当前对象的记忆（内存）空间！MemoryCentral is None!")

        # MemoryCentral: 用来存放当前对象的内存空间（避免每次都从数据库中调用）
        # 当前Engine的memory是MemoryCentral
        self.MemoryCentral=memory

class ThinkEngineBase(EngineBase):
    """
    思维类引擎的基础类
    """

    def __init__(self, thinkingCentral):
        """
        建模引擎。
        :param memoryCentral:
        """
        if not thinkingCentral :
            try:
                from loongtian.nvwa.organs.brain import Brain
                thinkingCentral=Brain().ThinkingCentral
            except Exception as e:
                logger.critical(e)
                raise Exception("必须提供思维中枢！ThinkingCentral is None!")

        super(ThinkEngineBase, self).__init__(thinkingCentral.Brain.MemoryCentral)
        self.thinkingCentral = thinkingCentral


