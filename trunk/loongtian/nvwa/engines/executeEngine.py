#!/usr/bin/env python
# coding=utf-8

"""
动作执行引擎。
"""


from loongtian.nvwa.engines.engineBase import EngineBase


__author__ = 'Leon'


class ExecuteEngine(EngineBase):
    """
    动作执行引擎。
    :rawParam
    :attribute
    """

    def __init__(self, memory):
        """
        动作执行引擎。
        :param memory: 用来存放当前对象的内存空间（避免每次都从数据库中调用）
                       当前AtionEngine的memory是MemoryCentral
        """
        super(ExecuteEngine, self).__init__(memory)

    def execute(self, thinkResult):
        """

        :param thinkResult:
        :return: 
        """
