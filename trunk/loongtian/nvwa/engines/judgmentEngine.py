#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Leon'

from loongtian.nvwa.engines.engineBase import ThinkEngineBase

class JudgmentEngine(ThinkEngineBase):
    """
    判别引擎。（单体实际对象与单体实际对象，单体对象与知识链，知识链与知识链，参见BOO）
    """


    def __init__(self, thinkingCentral):
        """
        迁移引擎。按照步骤-状态的顺序迁移成结果。
        :param memoryCentral: 用来存放当前对象的内存空间（避免每次都从数据库中调用）
                       当前TansitionEngine的memory是MemoryCentral
        """
        super(JudgmentEngine, self).__init__(thinkingCentral)


