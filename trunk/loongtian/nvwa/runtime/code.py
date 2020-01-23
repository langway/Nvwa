#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

from loongtian.nvwa.runtime.instinct import Instincts
from loongtian.nvwa.models.metaData import MetaData
from loongtian.nvwa.models.realObject import RealObject
from loongtian.nvwa.models.enum import ObjType
from loongtian.nvwa.runtime.relatedObjects import RelatedObj
class Code(object):
    """
    [运行时对象]所有代码类的实际对象操作的封装类（不在数据库中存储）。
    输入：有一段代码："print("Hello World!")"，代码语言为python，执行
    输出：Hello World!

    """

    def __init__(self,real):
        """
        [运行时对象]所有代码类的实际对象操作的封装类（不在数据库中存储）。
        :param real:
        """

        if not real or not isinstance(real,RealObject):
            raise Exception("必须提供实际对象！")
        if not real.isCode():
            raise Exception("必须提供代码类的实际对象！")
        self.real = real
        # 找到实际的代码
        self.real_code=self.getCode()

        # 取得代码的运行语言
        self.language=self.getLanguage()



    def getCode(self):
        """
        实际的代码
        :return:
        """
        temp_code = self.real.Layers.getUpperEntitiesByType(ObjType.META_DATA)
        if not isinstance(temp_code, RelatedObj):
            raise Exception("无法找到实际对象对应的代码元数据")
        temp_code = temp_code.obj
        if not isinstance(temp_code, MetaData):
            raise Exception("无法找到实际对象对应的代码元数据")
        temp_code = temp_code.mvalue
        if temp_code is None or not isinstance(temp_code, str) or temp_code == "":
            raise Exception("实际对象对应的元数据代码为空！")
        return temp_code


    def getLanguage(self):
        """
        取得代码的运行语言
        :return:
        """
        temp_language = self.real.Constitutions.getRelatedObjects(Instincts.instinct_original_code_language)

        return temp_language
    def runCode(self):
        """
        实际运行代码。
        :return:
        """

    @staticmethod
    def createCode(code,language):
        """
        根据代码段、运行语言创建女娲世界的代码元数据、实际对象等。
        :param code:
        :param language:
        :return:
        """



