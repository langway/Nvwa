#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

from loongtian.nvwa.engines.engineBase import ThinkEngineBase

class AbstractEngine(ThinkEngineBase):
    """
    抽象引擎。将n个对象的构成归纳合并，具有相同的，将生成一个相同的父对象。
    """

    def __init__(self, thinkingCentral):
        """
        抽象引擎。将n个对象的构成归纳合并，具有相同的，将生成一个相同的父对象。
        :param memoryCentral: 用来存放当前对象的内存空间（避免每次都从数据库中调用）
                       当前GroupEngine的memory是MemoryCentral
        """
        super(AbstractEngine, self).__init__(thinkingCentral)

    def abstract(self,*objs):
        """
        将n个对象的构成归纳合并，具有相同的，将生成一个相同的父对象。
        :param objs:
        :return:
        """