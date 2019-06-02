#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

"""
[运行时对象]对一个输入的思维结果（包括：理解的结果、情感处理的结果）
思维结果的层次：
    1、理解的结果，
        （1）排列规律的结果
        （2）迁移的结果
    2、未知对象的结果
    3、范式(上下文)的结果
    4、作为集合的思维结果，建立索引，观察顺序，等
    作为单个实际对象的构成结果
    建立索引，例如：牛有1、2、3、4，四条腿，就是输入了4个牛有腿(不同的腿)，然后建立索引，然后输出总数的过程

    5、联想的结果
    6、系统操作的结果(内观)
    7、评估的结果：与“我”的构成的价值进行评估
    8、情感处理的结果
    9、计划的结果
    10、行为的结果

"""


from loongtian.util.common.generics import GenericsList
from loongtian.nvwa.runtime.thinkResult.metaLevelResult import MetaLevelResult
from loongtian.nvwa.runtime.systemInfo import ThinkingInfo
from loongtian.nvwa.runtime.thinkResult.thinkingRecords.mindExecutingRecords import MindExecutingRecords


class ThinkResult(GenericsList):
    """
    [运行时对象]对一个字符串输入的思维结果（包括：理解的结果、情感处理的结果）（本身是MetasResult的列表）
    思维结果的层次：
        1、理解的结果，
            （1）线性排列规律(regulation)的结果
            （2）迁移（transition）的结果
        2、未知对象的结果
        3、根据范式(上下文)产生的的结果。
        4、作为集合的思维结果，建立索引，观察顺序，等
        作为单个实际对象的构成结果
        建立索引，例如：牛有1、2、3、4，四条腿，就是输入了4个牛有腿(不同的腿)，然后建立索引，然后输出总数的过程

        5、联想的结果
        6、系统操作的结果(内观)
        7、评估的结果：与“我”的构成的价值进行评估
        8、情感处理的结果
        9、计划的结果（时间、地点、动作等）
        10、行为的结果
    """

    def __init__(self, mind, rawInput):
        """
        对一个字符串输入的思维结果（包括：分割等），是一个MetaLevelResult的列表
        :param thinkResult:思维结果
        :remarks :
        实际包含了两部分：
        1、MindThinkingRecords 记录Mind的活动情况
        2、MetaLevelResults 记录元数据级别的思考结果（其中MetaLevelResult包含RealLevelResult）
        """
        if not rawInput or \
                not isinstance(rawInput, str)or \
                len(rawInput.strip()) == 0:
            raise Exception("必须提供元输入，才能创建ThinkResult！")
        super(ThinkResult, self).__init__(MetaLevelResult)  # 是一个MetaLevelResult的列表
        self.mind = mind
        self.rawInput = rawInput.strip()  # 元输入
        self.segment_result = None
        self.mindExecutingRecords = MindExecutingRecords()  # [(状态的枚举信息,实施的对象)]

        self.isSingleMeta =False # 是否是单个元数据的标记（包括理解不了的整句）

    def createNewMetaLevelResult(self, metas, unknown_metas_index):
        """
        创建一个元数据链的思考结果，并添加到当前列表中。
        :param metas:
        :return:
        """
        _metasLevelResult = MetaLevelResult(self, metas, unknown_metas_index)
        self.append(_metasLevelResult)
        return _metasLevelResult

    def setMindExecuteRecord(self, mindExecuteInfo, throw_exception=False):
        """
        设置执行状态信息。
        :param mindExecuteInfo:
        :return:
        """
        if self._canMindExecuteInfoTransfer(mindExecuteInfo):
            self.mindExecutingRecords.createNewMindThinkingRecord(mindExecuteInfo)
        else:
            if throw_exception:
                raise Exception("不能从一种执行状态（%s）转到当前执行状态（%s）" % (self.curMindExecuteInfo, mindExecuteInfo))

    def _canMindExecuteInfoTransfer(sel, mindExecuteInfo):
        """
        判断能从上一种执行状态转到当前执行状态。
        :param mindExecuteInfo:
        :return:
        """
        # todo 需要进行执行状态信息的判断（参考stateController）
        return True

    @property
    def curMindThinkingRecord(self):
        """
        取得最新的执行状态信息
        :return:
        """
        try:
            return self.mindExecutingRecords[-1]
        except:  # 有可能取不到 ，忽略错误
            pass

    @property
    def curMindExecuteInfo(self):
        """

        :return:
        """
        _curMindThinkingRecord =self.curMindThinkingRecord
        if _curMindThinkingRecord:
            return _curMindThinkingRecord.mindExecuteInfo

        return ThinkingInfo.MindExecuteInfo.UNKNOWN

    def isMetaLevelUnderstood(self):
        """
        判断是否在元数据层面理解（元输入/元数据链 匹配了 知识链，找到了知识链的意义）
        :return:
        """
        for metaLevelResult in self:
            if not metaLevelResult.isUndertood():
                return False

        return True



    def isAllUnknown(self):
        all_unknown_num = 0
        for metaLevelResult in self:
            if metaLevelResult.isAllUnknown():
                all_unknown_num += 1

        return all_unknown_num == len(self)
