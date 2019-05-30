#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

from loongtian.util.common.enum import Enum
from loongtian.nvwa.engines.engineBase import ThinkEngineBase

from loongtian.nvwa.models.baseEntity import BaseEntity
from loongtian.nvwa.models.realObject import RealObject
from loongtian.nvwa.models.knowledge import Knowledge
from loongtian.nvwa.runtime.instinct import Instincts
from loongtian.nvwa.models.enum import ObjType

"""
比较引擎。用来对任意两个对象进行比较，并输出其关联关系。目前只能进行机械比较。
1、ID比较
2、模式比较：ID链比较、构成比较、集合比较。
3、构成比较：
   红的、圆的-->气球、苹果
   红的、圆的、甜的-->苹果
4、任意比较：求同存异、生成父类、生成边界。
"""
class CompareEngine(ThinkEngineBase):
    """
    比较引擎。用来对任意两个对象进行比较，并输出其关联关系。目前只能进行机械比较。
    :rawParam
    :attribute
    """

    def __init__(self, thinkingCentral):
        """
        比较引擎。用来对任意两个对象进行比较，并输出其关联关系
        :param memoryCentral: 用来存放当前对象的内存空间（避免每次都从数据库中调用）
                       当前CompareEngine的memory是MemoryCentral
        """
        super(CompareEngine, self).__init__(thinkingCentral)

    @staticmethod
    def compare(obj1, obj2):
        """
        对任意两个nvwa对象进行比较，并输出其关联关系
        :param obj1:
        :param obj2:
        :return: SameObjectResult/ConsitituentsCompareResult/KnowledgeCompareResult
        """
        if not isinstance(obj1, BaseEntity) or not isinstance(obj2, BaseEntity):
            raise Exception("只能对两个nvwa对象进行比较！")

        if CompareEngine.isIdEqual(obj1, obj2):
            result = SameObjectResult(obj1, obj2)
            return result

        elif isinstance(obj1, RealObject) and isinstance(obj2, RealObject):
            return CompareEngine.consitituentComparer(obj1, obj2)

        elif isinstance(obj1, Knowledge) and isinstance(obj2, Knowledge):
            return CompareEngine.knowledgeComparer(obj1, obj2)

        return None

    @staticmethod
    def isIdEqual(obj1, obj2):
        """
        判断两个对象是否Id相同。
        :param obj1:
        :param obj2:
        :return:
        """
        if isinstance(obj1, BaseEntity) and isinstance(obj2, BaseEntity):
            return obj1.id == obj2.id
        return False

    @staticmethod
    def consitituentComparer(realobj1, realobj2):
        """
        比较两个实际对象的构成
        :param realobj1:
        :param realobj2:
        :return:
        """
        if not isinstance(realobj1, RealObject) or not isinstance(realobj2, RealObject):
            raise Exception("只能对两个实际对象进行比较！")

        consitituents1, constituentKnowledges1 = realobj1.getSelfConstituentObjects()
        consitituents2, constituentKnowledges2 = realobj2.getSelfConstituentObjects()

        result = ConsitituentsCompareResult(realobj1, realobj2)
        total_differs = 0
        total_sames = 0

        for toprelation, related_objs1 in consitituents1.items():
            related_objs2 = consitituents2.get(toprelation)
            ccr=CompareEngine.chainComparer(related_objs1, related_objs2)
            sames = ccr.sames1
            differs =ccr.differs1
            result.consitituents_sames[toprelation] = sames
            result.consitituents_differs[toprelation] = differs

            total_differs += len(differs)
            total_sames += len(sames)
            if len(differs) == 0:  # 如果没有不同的
                if CompareEngine.isIdEqual(toprelation, Instincts.instinct_ingredient):
                    result.compareTypes.append(ConsitituentsCompareType.IngredientEqual)
                if CompareEngine.isIdEqual(toprelation, Instincts.instinct_attribute):
                    result.compareTypes.append(ConsitituentsCompareType.AttributeEqual)
                if CompareEngine.isIdEqual(toprelation, Instincts.instinct_component):
                    result.compareTypes.append(ConsitituentsCompareType.ComponentEqual)
                if CompareEngine.isIdEqual(toprelation, Instincts.instinct_parent):
                    result.compareTypes.append(ConsitituentsCompareType.ParentsEqual)
                if CompareEngine.isIdEqual(toprelation, Instincts.instinct_belongs):
                    result.compareTypes.append(ConsitituentsCompareType.BelongsEqual)
                if CompareEngine.isIdEqual(toprelation, Instincts.instinct_relevancy):
                    result.compareTypes.append(ConsitituentsCompareType.RelevancyEqual)
                if CompareEngine.isIdEqual(toprelation, Instincts.instinct_observer):
                    result.compareTypes.append(ConsitituentsCompareType.ObserverEqual)
                # if CompareEngine.isIdEqual(toprelation, _Instincts.instinct_nvwa_ai):
                #     result.compareTypes.append(ConsitituentsCompareType.ObserverEqual)

        if total_differs == 0:
            result.compareTypes.append(ConsitituentsCompareType.AllConsitituentsSame)
        if total_sames == 0:
            result.compareTypes.append(ConsitituentsCompareType.AllConsitituentsDiffer)

        result.total_differs = total_differs
        result.total_sames = total_sames

        return result

    # @staticmethod
    # def listComparer(chain1, chain2):
    #     if not isinstance(chain1, list) or not isinstance(chain2, list) or not isinstance(chain1, tuple) or not isinstance(chain2, tuple):
    #         raise Exception("只能对两个list或tuple对象进行比较！")
    #
    #     sames = []
    #     differs = []
    #     for item1 in chain1:
    #         if item1 in chain2:
    #             sames.append(item1)
    #         hasSameId = False
    #         for item2 in chain2:
    #             if CompareEngine.isIdEqual(item1, item2):
    #                 sames.append(item1)
    #                 hasSameId = True
    #         if not hasSameId:
    #             differs.append(item1)
    #
    #     return sames, differs

    @staticmethod
    def knowledgeComparer(know1, know2,compareLowerRealObject=True,):
        """
        比较两个知识链的结构（求同存异）和构成（如果有指向的实际对象）
        :param know1:
        :param know2:
        :return:
        """
        if not isinstance(know1, Knowledge) or not isinstance(know2, Knowledge):
            raise Exception("只能对两个知识链进行比较！")

        know_result = KnowledgeCompareResult(know1, know2)

        if compareLowerRealObject:
            # 如果知识链有指向的实际对象，比较其构成
            realobj1 = know1.Layers.getLowerEntitiesByType(ObjType.REAL_OBJECT)
            realobj2 = know2.Layers.getLowerEntitiesByType(ObjType.REAL_OBJECT)
            if realobj1 and realobj2:
                real_result = CompareEngine.consitituentComparer(realobj1, realobj2)
                know_result.consitituentsCompareResult = real_result

        # 比较两个知识链的结构
        reals1 = know1.getSequenceComponents()
        reals2 = know2.getSequenceComponents()
        know_result.chainCompareResult= CompareEngine.chainComparer(reals1,reals2)

        return know_result


    @staticmethod
    def chainComparer(chain1, chain2,doubleDirection=False):
        """
        比较两个链的结构，包括相同、不同（含位置信息）、链1与链2的编辑距离、转换成本
        :param chain1: 链1
        :param chain2: 链2
        :param doubleDirection: 是否进行反向比较（默认为单向）
        :return:
        """
        ccr = ChainCompareResult(chain1, chain2)

        from loongtian.util.text.edit_distance import SequenceMatcher

        sm = SequenceMatcher(chain2, chain1)
        ccr.ratio1to2 = sm.ratio()
        ccr.distance1to2= sm.distance()
        i = 0
        for opcode in sm.get_opcodes():
            if opcode[0] == "equal":
                ccr.sames1[i] = chain1[i]
                i += 1
            elif opcode[0] == "replace":
                ccr.differs1[i] = chain1[i]
                i += 1
            elif opcode[0] == "delete":
                ccr.differs1[i] = chain2[i]

            elif opcode[0] == "insert":
                ccr.differs1[i] = chain1[i]
                i += 1

        if not doubleDirection:
            return ccr

        sm = SequenceMatcher(chain1, chain2)
        ccr.ratio2to1 = sm.ratio()
        ccr.distance2to1 = sm.distance()
        i = 0
        for opcode in sm.get_opcodes():
            if opcode[0] == "equal":
                ccr.sames2[i] = chain2[i]
                i += 1
            elif opcode[0] == "replace":
                ccr.differs2[i] = chain2[i]
                i += 1
            elif opcode[0] == "delete":
                ccr.differs2[i] = chain1[i]

            elif opcode[0] == "insert":
                ccr.differs2[i] = chain2[i]
                i += 1

        return ccr


class ChainCompareResult(object):
    """
    两个链结构的比较结果，包括相同、不同（含位置信息）、链1与链2的编辑距离、转换成本
    """

    def __init__(self,chain1, chain2):

        if not isinstance(chain1, list) or not isinstance(chain2, list) or not isinstance(chain1, tuple) or not isinstance(chain2, tuple):
            raise Exception("只能对两个list或tuple链对象进行比较！")

        self.chain1=chain1
        self.chain2 = chain2

        self.sames1 = {} # 链1到链2结构的相同部分(实际对象,位置)
        self.differs1 = {}  # 链1到链2结构的不同部分(实际对象,位置)
        self.sames2 = {} # 链2到链1结构的相同部分(实际对象,位置)
        self.differs2 = {} # 链2到链1结构的不同部分(实际对象,位置)

        self.ratio1to2 = None  # 链1到链2的转换成本
        self.distance1to2 = None  # 链1到链2的编辑距离
        self.ratio2to1 = None
        self.distance2to1 = None  # 链2到链2的编辑距离

        self.structureCompareType = None  # 两个知识链结构的比较结果

class ConsitituentsCompareType(Enum):
    """
    两个实际对象构成比较的结果类型
    """
    Unknown = 1  # 构成相同（相等或完全是一个对象，例如：红色的、圆的气球——红色的、圆的苹果，等待合并为）
    ParentsEqual = 2  # 父对象相同（例如：牛和马）
    IngredientEqual = 3  # 成分相同（例如：碳和钻石）
    AttributeEqual = 4  # 属性相同（例如：红色的、圆的气球——红色的、圆的苹果）
    ComponentEqual = 5  # 组件相同（例如：牛有腿、头、尾等，马有腿、头、尾等；两个个集合的所有元素相同）
    BelongsEqual = 6  # 所属物相同（小明有100元，小丽也有100元）
    RelevancyEqual = 7  # 相关物相同（在两个对象建立的非其他构成关系中，所有建立关联的对象相同）
    ObserverEqual = 8  # 观察者相同（牛顿第一、第二定律的观察者均为牛顿）

    AllConsitituentsSame = 11  # 所有构成均相同
    AllConsitituentsDiffer = 12  # 所有构成均不相同（包括Id）
    # PartialDiffer = 13  # 部分构成相同、部分不同（Id肯定不同）


class KnowledgeStructureCompareType(Enum):
    """
    两个知识链结构比较的结果类型
    """

    AllEqual = 21  # 知识链的结构（含顺序）完全相同
    AllDiffer = 22  # 知识链的结构（含顺序）完全不相同
    SameFromTop = 23  # 从知识链的头部开始相同，但后面有不相同的（例如：牛-有-腿，牛-有-腿-吗）
    SameFromMiddle = 24  # 从知识链的中间开始相同，但前后有不相同的（例如：牛-有-腿，我-怎么-知道-牛-有-腿-吗）
    SameFromBottom = 25  # 从知识链的尾部开始相同，但后面有不相同的（例如：牛-有-腿，我-知道-牛-有-腿）
    PartialEqual = 26  # 部分元素相同、部分不同（Id肯定不同）


class SameObjectResult(object):
    """
    两个对象Id相同（完全相同）。
    """

    def __init__(self, obj1, obj2):
        if not isinstance(obj1, BaseEntity) or not isinstance(obj2, BaseEntity):
            raise Exception("只能对两个nvwa对象进行比较！")
        self.obj1 = obj1
        self.obj2 = obj2

    pass


class KnowledgeCompareResult(object):
    """
    两个知识链的比较结果，包括结构和构成（如果有指向的实际对象）
    """

    def __init__(self, know1, know2):

        if not isinstance(know1, Knowledge) or not isinstance(know2, Knowledge):
            raise Exception("只能对两个知识链进行比较！")
        self.know1 = know1
        self.know2 = know2

        self.consitituentsCompareResult = None  # 两个知识链的构成比较结果（如果有指向的实际对象）
        self.chainCompareResult = None # 两个知识链的结构比较结果

    def getSamesAndDiffers(self):
        if isinstance(self.chainCompareResult,ChainCompareResult):
            return self.chainCompareResult.sames1, self.chainCompareResult.differs1, \
                   self.chainCompareResult.sames2, self.chainCompareResult.differs2

class ConsitituentsCompareResult(object):
    """
    两个nvwa实际对象构成的比较结果
    """

    def __init__(self, obj1, obj2):
        if not isinstance(obj1, RealObject) or not isinstance(obj2, RealObject):
            raise Exception("只能对两个nvwa实际对象进行比较！")
        self.obj1 = obj1
        self.obj2 = obj2

        self.compareTypes = []
        self.consitituents_sames = {}
        self.consitituents_differs = {}

        self.total_differs = -1
        self.total_sames = -1
