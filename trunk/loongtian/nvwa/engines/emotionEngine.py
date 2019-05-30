#!/usr/bin/env python
# -*- coding: utf-8 -*-
from loongtian.nvwa.models.realObject import RealObject
from loongtian.nvwa.models.metaData import MetaData
from loongtian.nvwa.engines.engineBase import EngineBase
from loongtian.util.log import logger

__author__ = 'Leon'

class EmotionEngine(EngineBase):
    """
    情感引擎引擎。用来评估“预期”与输入、输出结果对“我”的“价值”之间的差异，以及环境对输出结果反应对“我”的“价值”
    :rawParam
    :attribute
    """

    def __init__(self,memory):
        """
        情感引擎引擎。用来评估“预期”与输入、输出结果对“我”的“价值”之间的差异，以及环境对输出结果反应对“我”的“价值”
        :param memory: 用来存放当前对象的内存空间（避免每次都从数据库中调用）
                       当前EmotionEngine的memory是MemoryCentral
        """
        super(EmotionEngine, self).__init__(memory)

    def calculate(self,thinkResult):
        """
        对“评估”的结果进行情感计算
        :param thinkResult:
        :return:
        """
        return None



