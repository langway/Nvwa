#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Leon'

from loongtian.nvwa.engines.engineBase import EngineBase
from loongtian.util.log import logger
from loongtian.nvwa.models.realObject import RealObject
from loongtian.nvwa.models.metaData import MetaData


class PlanEngine(EngineBase):
    """
    计划引擎。根据“情感计算”的结果制定行为计划
    :rawParam
    :attribute
    """
    def __init__(self,memory):
        """
        计划引擎。根据“情感计算”的结果制定行为计划
        :param memory: 用来存放当前对象的内存空间（避免每次都从数据库中调用）
                       当前GroupEngine的memory是MemoryCentral
        """
        super(PlanEngine, self).__init__(memory)

    def plan(self,thinkResult):
        """
        根据“情感计算”的结果制定行为计划。
        :param thinkResult:
        :return:
        """
