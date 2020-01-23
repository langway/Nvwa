#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

from loongtian.util.common.generics import GenericsList
from loongtian.nvwa.models.enum import ObjType

from loongtian.nvwa.runtime.innerOperation import InnerOperations


# 小明的手机的范式：
# pattern=Pattern(["placeholder1","的","placeholder2"])
# real=pattern.generate("小明的手机意义小明的手机是手机小明有小明的手机")
# 预期结果：
# real-父对象-手机，小明-所属物-real
#
# 四头牛的范式：
# pattern=Pattern(["placeholder-数字","头","牛"])
# real=pattern.generate("四头牛")
# 预期结果：
# real-父对象-集合，real-元素-牛，real-集合数量-四
#
# 中华人民共和国的范式：
# pattern=Pattern(["placeholder1","placeholder2","..."])
# real=pattern.generate("中华人民共和国")
# 预期结果：
# real-父对象-国家，real-名称-中华人民共和国

#     模式包括：
#         顺序  模式  结果及存储             匹配规则    是否迁移   eg
#         1     RRR   R(知识链，新实际对象)   由后向前      否       中国人民建设银行
#         2     AAA   A(新动词)              由前向后      否       打跑了  跑了  走了
#         3     RAR   R(知识链)              优先级        是       小明打小丽  小明给小丽花


class LinearPattern(object):
    """
    线性输入女娲对象的序列类型的模板。例如：中华-人民-共和国==》中华人民共和国
    """

    def __init__(self, objTypes: GenericsList = None, operations: {} = None):
        """
        线性输入女娲对象的序列类型。例如：中华-人民-共和国==》中华人民共和国
        目前发现的线性pattern包括：
        1、修限型
        （1）R1-...Rn，例如：中国人民银行
        （2）A1A2，例如：跑了
        （3）A1A2R1，例如：跑是动作，跑了一圈
        （4）R1A1A2，例如：动作包含跑
        2、集合型（一般为同一父对象）
        （1）R1-...Rn，例如：四五六七
        （2）A1A2...An，例如：跑跳蹲
        :param operations:
        :param objTypes:
        """
        self.objTypes = objTypes  # 线性输入女娲对象的序列类型

        self.operations = operations  # 对应的操作方法，可能有多个{operation:frequncy}


class LinearPatterns(GenericsList):

    def __init__(self):
        super(LinearPatterns, self).__init__(LinearPattern)
        self.objTypes_dict={}



    # class Confusion(Enum):
    #     """
    #     带来思考混乱的问题枚举
    #     """
    #
    #
    # Confusion=Confusion()


class ContextPattern(GenericsList):
    """
    多条线性输入的范式（上下文）。例如：
    """

    def __init__(self):
        super(ContextPattern, self).__init__(LinearPattern)
        pass
