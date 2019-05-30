# /usr/bin/python
# coding: utf-8
__author__ = 'Leon'

"""
nvwa的情感模型（封装类）
"""
from loongtian.util.common.enum import Enum
from loongtian.nvwa.runtime.situation import Situation
from loongtian.nvwa.runtime.myself import Myself
from loongtian.nvwa.runtime.behaviours import Behaviours
from loongtian.nvwa.runtime.sequencedObjs import SequencedObj
from loongtian.util.common.generics import GenericsList

class CoreValueType(Enum):
    """
    [运行时对象]核心价值的类型（留存和发展）
    """

    Preservation = 0  # 留存。留存自身构成

    Propagate = 1  # 繁衍。繁衍下一代（复制下一代）

    Develop = 2  # 发展。附加自身构成，例如：想要飞，学习知识、赚更多的钱、掌握更多的权利等

    ReduceComputation = 3  # 减少计算量


class Emotion(SequencedObj):
    """
    [运行时对象]nvwa的情感基础模型（是实际对象的包装类）。
    情感应该有一个单独列表，记录：不同的本我（self）——任何非情感的实际对象——四种核心价值——奖、惩值——距离……之间的关系
    """

    def __init__(self):
        """
        [运行时对象]nvwa的情感基础模型（是实际对象的包装类）。
        """
        super(Emotion,self).__init__()

        # 核心价值的类型
        self.coreValueType = CoreValueType.Preservation
        # 从状态A到状态B对核心价值的贡献度（价值大小），例如吃饭对Preservation的价值，要大于吃水果
        # 正数代表有益，负数代表有害
        # 相当于情感理论中 的愉悦度（快感），系统尽量使其等于1
        self.benifit = 1.0  # 取值范围[0,1]
        self.punishment = 0.0  # 取值范围[-1,0]

        # 与核心价值的距离，与核心价值越远，激活度越差。例如：洗澡对留存的激活度，要小于吃饭对留存的激活度。
        # 取值范围[0,1]
        # 相当于情感理论中 的激活度
        self.distance = 0.0

        # 系统对与核心价值的距离的置信度（确认度）
        self.confidence = 1.0

        # ########################
        # 运行时数据
        # ########################
        self.target_obj =None # 情感的作用对象，可以是实际对象、动作、知识链

        # 当前个体（我"，是实际对象的包装类，包括本我、他我、泛我）
        self.Myself = Myself()
        # 当前个体所处的情境（是多个实际对象的包装类）
        self.situation = Situation()

        # 在当前情感下可能会采取的行动
        self.actions = Behaviours()

    def getStrength(self):
        """
        当前情感的强度（根据situation、coreValueType、contribution、distance、confidence）
        系统尽量使大于0的尽量等于1，小于0的等于0
        :return:
        """
        strength = 0

        return 1 - strength

class Emotions(GenericsList):
    """
    [运行时对象]nvwa的情感基础模型（是实际对象的包装类）的列表。
    """
    def __init__(self):
        super(Emotions,self).__init__(Emotion)


