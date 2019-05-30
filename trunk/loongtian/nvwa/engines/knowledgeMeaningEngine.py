#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

from loongtian.nvwa.engines.engineBase import EngineBase
from loongtian.util.log import logger
from loongtian.nvwa.models.knowledge import Knowledge

class KnowledgeMeaningEngine(EngineBase):
    """
    知识链意义折叠引擎。将知识链所有的显性意义转换为隐性意义（压缩知识库的规模，以减少查找等操作的管理）。
    """

    def __init__(self,memory):
        """
        知识链意义折叠引擎。将知识链所有的显性意义转换为隐性意义（压缩知识库的规模，以减少查找等操作的管理）。
        :param memory: 用来存放当前对象的内存空间（避免每次都从数据库中调用）
                       当前GroupEngine的memory是MemoryCentral
        """
        super(KnowledgeMeaningEngine, self).__init__(memory)


    def do_dominanceMeaningsToRecessivity(self):
        """
        对实际对象、知识链进行识别，取得识别（理解）率。
        :return:
        """
        klgs =Knowledge.getAllByConditionsInDB(memory=self.MemoryCentral)
        if klgs:
            for klg in klgs:
                if not isinstance(klg,Knowledge):
                    raise Exception("klg不是Knowledge类型")
                klg.Meanings.convertDominanceMeaningsToRecessivity()


