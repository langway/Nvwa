#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

from loongtian.nvwa.centrals.centralBase import CentralBase
from loongtian.nvwa.engines.metaEngine import TextEngine,\
                    SegmentedResult,SegmentedResults,ArticleSegmentResult,ArticlesSegmentResults

class PerceptionCentral(CentralBase):


    def __init__(self,brain):
        """
        感知中枢。
        :param brain:
        :remark
        需调用文本处理引擎
        声音处理引擎
        图像处理引擎
        皮肤处理引擎
        味道处理引擎等对输入进行处理
        """
        super(PerceptionCentral, self).__init__(brain)
        self.TextEngine=TextEngine(self.Brain.MemoryCentral) # 文本处理引擎



        pass

    def receive(self,raw_input):
        """
        接收不同感知器官的输入，分别进行处理 todo 需防sql注入
        :param input:可以包括文本、声音、图像等
        :return:
        """
        if not raw_input:
            return None
        if isinstance(raw_input, str):
            raw_input=str(raw_input)

        # 记录系统的输入信息
        self.Brain.MemoryCentral.InputsManager.add(raw_input)

        # 送入思维中枢，开始思考
        if isinstance(raw_input,str):
            return self.Brain.ThinkingCentral.thinkStringInput(raw_input)
        else:
            raise Exception("当前程序不能处理其他类型的数据！")

