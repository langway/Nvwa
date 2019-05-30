#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

from loongtian.nvwa.engines.engineBase import EngineBase
from loongtian.util.log import logger
from loongtian.nvwa.models.realObject import RealObject
from loongtian.nvwa.models.knowledge import Knowledge

class RecognizeEngine(EngineBase):
    """
    实际对象的识别引擎。
    取得实际对象已被识别的比率。
    如果已经有父对象（除original_object之外）+10.0，n个乘n
    有构成（顶级关系） +5.0 ，n个乘n
    无构成 +1.0，n个乘n
    跟ForgetEngine一样，由系统调用
    """

    def __init__(self,memory):
        """
        实际对象的识别引擎。
        :param memory: 用来存放当前对象的内存空间（避免每次都从数据库中调用）
                       当前GroupEngine的memory是MemoryCentral
        """
        super(RecognizeEngine, self).__init__(memory)


    def do_recognize(self):
        """
        对实际对象、知识链进行识别，取得识别（理解）率。
        :return:
        """
        reals = RealObject.getAllByConditionsInDB(memory=self.MemoryCentral)
        for real in reals:
            real.getUnderstoodRatio()
            real.updateAttributeValues(uratio=real.uratio)

        klgs =Knowledge.getAllByConditionsInDB(memory=self.MemoryCentral)
        for klg in klgs:
            klg.getUnderstoodRatio()
            klg.updateAttributeValues(uratio=klg.uratio)

