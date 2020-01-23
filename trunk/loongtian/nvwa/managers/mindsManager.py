#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Leon'

from loongtian.nvwa.runtime.sequencedObjs import SequencedObjs
from loongtian.nvwa.runtime.article import StrContent
from loongtian.nvwa.organs.mind import Mind

class MindsManager(SequencedObjs):
    """
    多思维（Mind）管理器，产生并管理上下文。
    :rawParam
    构造函数参数说明
    :attribute
    对象属性说明
    """

    def __init__(self, thinkingCentral):
        """
        多思维（Mind）管理器，产生并管理上下文。
        :param thinkingCentral:
        """
        super(MindsManager,self).__init__(objTypes=[Mind])

        self.thinkingCentral = thinkingCentral
        self._Minds = []
        self.IdMindDict = {}

        pass

    def createMind(self,str_content:StrContent):
        """
        根据元数据链（meta_chain）创建Mind
        :param meta_chain:
        :return:
        """
        mind = Mind(self.thinkingCentral,str_content)
        self.add(mind)
        return mind

    def groupMinds(self,start=None,end=None):
        """
        根据各Mind的关注点不同，对各Mind进行分组
        :param start:
        :param end:
        :return:
        """
        if not start:
            start=0
        if not end:
            end= len(self._id_sequencedObj_dict)
        if start<end:
            raise Exception("起始点不能小于终点！")

        minds= self._sequencedObj_list[start:end] # 切片






