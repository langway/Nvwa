#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

from loongtian.util.common.generics import GenericsList
from loongtian.nvwa.models.enum import ObjType

# 我的手机的范式：
# paradigm=Paradigm(["placeholder1","的","placeholder2"])
# real=paradigm.generate("我的手机")
# 预期结果：
# 我的手机-父对象-手机，我-所属物-我的手机
#
# 四头牛的范式：
# paradigm=Paradigm(["placeholder-数字","头","牛"])
# real=paradigm.generate("四头牛")
# 预期结果：
# real-父对象-集合，real-元素-牛，real-集合数量-四
#
# 中华人民共和国的范式：
# paradigm=Paradigm(["placeholder1","placeholder2","..."])
# real=paradigm.generate("中华人民共和国")
# 预期结果：
# real-父对象-共和国，real-名称-中华人民共和国

class Paradigm(object):
    """
    一条线性输入的范式。例如：中华-人民-共和国==》中华人民共和国
    """

    def __init__(self, operations=None, realsType=ObjType.REAL_OBJECT):
        if operations:
            if not isinstance(operations, list):
                raise Exception("必须提供线性输入的实际对象！")
            self.operations =operations
        else:
            self.operations=[]
        pass

        self.systemOperations=[] # 系统定义的操作


class ContextParadigm(GenericsList):
    """
    一条线性输入的范式。例如：中华-人民-共和国==》中华人民共和国
    """

    def __init__(self):
        super(ContextParadigm,self).__init__(Paradigm)
        pass
