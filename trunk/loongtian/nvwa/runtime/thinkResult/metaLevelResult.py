#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Leon'

from loongtian.nvwa.runtime.thinkResult.thinkingRecords.metaLevelRecords import MetaLevelThinkingRecords

from loongtian.nvwa.runtime.systemInfo import ThinkingInfo
from loongtian.util.common.generics import GenericsList
from loongtian.nvwa.runtime.thinkResult.realLevelResult import RealLevelResult
from loongtian.nvwa.runtime.thinkResult.fragments import UnknownMetas,ProceedUnknownMetas
class MetaLevelResult(GenericsList):
    """
    [运行时对象]对一个元数据链的思维结果（包括：理解的结果、情感处理的结果）
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

    def __init__(self, thinkResult,meta_chain,unknown_metas_index):
        """
        对一个元数据链的思维结果（包括：理解的结果、情感处理的结果等）（本身是RealsResult的列表）
        :param thinkResult:思维结果
        """
        super(MetaLevelResult, self).__init__(RealLevelResult) # 是一个RealLevelResult的列表

        self.thinkResult =thinkResult # 当前MetaLevelResult的父辈thinkResult

        self.meta_chain = meta_chain  # 根据当前元输入的分割的结果创建元数据链（由于分割结果可能有多个，所以在处理时一条条调用，直到“理解”为止）
        self.unknown_metas_index = unknown_metas_index  # 未识别的元数据的索引（位置列表）

        self.meta_reals={} # 取得的元数据-实际对象（多个） {metadata:related_reals}

        self._meta_nets = [] # 根据meta_chain取得的元数据网
        self._meta_net_matched_knowledges = {}
        self._meta_net_matched_knowledges_meaning_klgs = {}

        self.unknownMetas = UnknownMetas()  # 未知的元数据 {mvalue:meta}。等待进一步开启新的Mind处理
        self.proceedUnknownMetas = ProceedUnknownMetas() # 在一个元数据链（笛卡尔积子集）中，已经经过处理的未能正确理解的元数据对象列表

        self.realLowerObjs_list = []  # 根据metaChain取得的LowerObjs列表（未排序状态，是个dict）
        self.sorted_realsChain_list = []  # 根据metaChain取得的realObject列表（排序状态，是个list，根据权重，最大值在前）

        self.metaLevelThinkingRecords = MetaLevelThinkingRecords(self)  # 关于思考状态的信息记录（这些状态在思维处理中不断被改变，是单向、互斥的）。

    # 2019-02-08 之所以取消设置值的时候，设置执行状态和匹配状态，是因为这里面涉及的判断较多，放在mind中处理
    # def setMetaChain_UnknownMetasIndex(self, meta_chain, unknown_metas_index):
    #     """
    #     设置# 根据当前元输入的分割的结果创建元数据链（由于分割结果可能有多个，所以在处理时一条条调用，直到“理解”为止）
    #     :param meta_chain:
    #     :return:
    #     """
    #     # 设置ObjectsExecuteRecord执行状态
    #     self.metaLevelThinkingRecords.setObjectsExecuteRecord(
    #         ThinkingInfo.ObjectsExecuteInfo.Processing_MataDatas, meta_chain)
    #
    #     if meta_chain:
    #         if unknown_metas_index: # 如果还有未知的，设置其匹配状态为META_CHAIN_PARTIAL_MATCHED
    #             self.metaLevelThinkingRecords.setObjectMatchRecord(ThinkingInfo.ObjectMatchInfo.META_CHAIN_PARTIAL_MATCHED,
    #                                                              (meta_chain,unknown_metas_index))
    #         else:
    #             # 设置匹配状态为METAS_MATCHED
    #             self.metaLevelThinkingRecords.setObjectMatchRecord(ThinkingInfo.ObjectMatchInfo.META_CHAIN_MATCHED,
    #                                                             meta_chain)
    #     else:
    #         # 设置匹配状态为METAS_UNMATCHED
    #         self.metaLevelThinkingRecords.setObjectMatchRecord(ThinkingInfo.ObjectMatchInfo.META_CHAIN_UNMATCHED,
    #                                                          None)
    #
    #     self.meta_chain = meta_chain

    @property
    def meta_nets(self):
        """
        根据字符串或元数据链匹配的meta_net(函数内会设置其执行状态及匹配状态)
        :return:
        """
        return self._meta_nets

    def set_meta_net(self,value):
        """
        根据字符串或元数据链匹配的meta_net(函数内会设置其执行状态及匹配状态)
        :param value:
        :return:
        """
        # 设置ObjectsExecuteRecord执行状态
        self.metaLevelThinkingRecords.setMetaLevelExecuteRecord(
            ThinkingInfo.MetaLevelInfo.ExecuteInfo.Processing_MetaNet, value)

        if value:
            from loongtian.nvwa.models.metaNet import MetaNet
            if not isinstance(value,MetaNet):
                raise Exception("提供的值不是MetaNet类型！")
            # 设置匹配状态为METANET_MATCHED
            self.metaLevelThinkingRecords.setMetaLevelMatchRecord(ThinkingInfo.MetaLevelInfo.MatchInfo.METANET_MATCHED,
                                                                  value)
        else:
            # 设置匹配状态为METANET_UNMATCHED
            self.metaLevelThinkingRecords.setMetaLevelMatchRecord(ThinkingInfo.MetaLevelInfo.MatchInfo.METANET_UNMATCHED,
                                                                  None)

        self._meta_nets.append(value)


    @property
    def meta_net_matched_knowledges(self):
        """
        根据meta_net匹配的knowledges
        :return:
        """
        return self._meta_net_matched_knowledges


    def set_meta_net_matched_knowledges(self, meta_net, matched_knowledges):
        """
        根据meta_net匹配的knowledges(函数内会设置其执行状态及匹配状态)
        :param matched_knowledges:
        :return:
        """
        # 设置ObjectsExecuteRecord执行状态
        self.metaLevelThinkingRecords.setMetaLevelExecuteRecord(
            ThinkingInfo.MetaLevelInfo.ExecuteInfo.Processing_MetaNet_Matched_Knowledges, (meta_net,matched_knowledges))

        if matched_knowledges:
            # 设置匹配状态为KNOWLEDGE_MATCHED
            self.metaLevelThinkingRecords.setMetaLevelMatchRecord(ThinkingInfo.MetaLevelInfo.MatchInfo.METANET_KNOWLEDGE_MATCHED,
                                                                  (meta_net,matched_knowledges))
        else:
            # 设置匹配状态为KNOWLEDGE_UNMATCHED
            self.metaLevelThinkingRecords.setMetaLevelMatchRecord(ThinkingInfo.MetaLevelInfo.MatchInfo.METANET_KNOWLEDGE_UNMATCHED,
                                                                  None)

        self._meta_net_matched_knowledges[meta_net] = matched_knowledges

    @property
    def meta_net_matched_knowledges_meaning_klgs(self):
        """
        根据meta_net匹配的knowledges向下一层取得的意义知识链(函数内或设置其执行、匹配及理解状态)
        :return:
        """
        return self._meta_net_matched_knowledges_meaning_klgs


    def get_meta_net_matched_knowledges_meaning_klgs(self):
        """
        取得元数据网匹配到的知识链的意义。
        :return:
        """
        if not self.meta_nets:
            return None
        total_meaning_klgs=[]
        for meta_net in self.meta_nets:
            matched_knowledges_meaning_klgs=self.meta_net_matched_knowledges_meaning_klgs[meta_net]
            cur_meaning_klgs=[]
            for matched_knowledge, meaning_klgs in matched_knowledges_meaning_klgs.items():
                if isinstance(meaning_klgs,list) or isinstance(meaning_klgs,tuple):
                    cur_meaning_klgs.extend(meaning_klgs)
                else:
                    cur_meaning_klgs.append(meaning_klgs)
            total_meaning_klgs.append(cur_meaning_klgs)
        final_meaning_klgs=[]
        import itertools
        for meaning_klgs in itertools.product(*total_meaning_klgs):
            final_meaning_klgs.append(meaning_klgs)

        return final_meaning_klgs

    def set_meta_net_matched_knowledges_meaning_klgs(self, meta_net, matched_knowledges_meaning_klgs):
        """
        根据meta_net匹配的knowledges向下一层取得的意义知识链(函数内会设置其执行、匹配及理解状态)
        :param matched_knowledges_meaning_klgs:{meta_net_matched_knowledge:meaning_klgs}
        :return:
        """
        # 设置ObjectsExecuteRecord执行状态
        self.metaLevelThinkingRecords.setMetaLevelExecuteRecord(
            ThinkingInfo.MetaLevelInfo.ExecuteInfo.Processing_MetaNet_Matched_Knowledges_Meaning, (meta_net,matched_knowledges_meaning_klgs))

        if matched_knowledges_meaning_klgs:
            # 设置匹配状态为MEANING_MATCHED
            self.metaLevelThinkingRecords.setMetaLevelMatchRecord(ThinkingInfo.MetaLevelInfo.MatchInfo.METANET_KNOWLEDGE_MEANING_MATCHED,
                                                                  (meta_net,matched_knowledges_meaning_klgs))

        else:
            # 设置匹配状态为MEANING_UNMATCHED
            self.metaLevelThinkingRecords.setMetaLevelMatchRecord(ThinkingInfo.MetaLevelInfo.MatchInfo.METANET_KNOWLEDGE_MEANING_UNMATCHED,
                                                                  None)
            # 不设置其理解状态（等待后续进一步处理）

        self._meta_net_matched_knowledges_meaning_klgs[meta_net] = matched_knowledges_meaning_klgs

    def createNewRealLevelResult(self, reals):
        """
        创建一个实际对象链的思考结果，并添加到当前列表中。
        :param reals:
        :return:
        """
        _realLevelResult = RealLevelResult(reals, self)
        self.append(_realLevelResult)
        return _realLevelResult


    def get_understood_knowledges(self):
        """
        取得经过理解的知识链
        :return:
        """
        understood_knowledges = []
        for realsThinkResult in self:
            understood_knowledges.append(realsThinkResult.getAllUnderstoodKnowledges())
        return understood_knowledges

    def isSingle(self):
        """
        判断当前输入是否匹配出了一个实际对象（meta已知，实际对象已知）
        :return:
        """
        return len(self.meta_chain) == 1

    def isAllUnknown(self):
        """
        判断元数据链是否全都未知。
        :return:
        """
        if len(self.meta_chain) == len(self.unknown_metas_index):
            return True
        return False

    def canForwardToRealLevel(self):
        """

        :return:
        """

    def isUndertood(self):
        """
        元数据级别对思考结果进行判断，是否已经理解（匹配了元数据网-知识链-意义）
        :return:
        """
        # 单元数据
        if self.metaLevelThinkingRecords.curMetaLevelMatchInfo == ThinkingInfo.MetaLevelInfo.MatchInfo.SINGLE_META_RELATED_REALS_MATCHED:
            return True
        elif self.metaLevelThinkingRecords.curMetaLevelMatchInfo == ThinkingInfo.MetaLevelInfo.MatchInfo.METANET_KNOWLEDGE_MEANING_MATCHED:
            return True

        return False

    def getMetaMatchedReals(self):

        meta_reals = {}
        for meta, related_reals in self.meta_reals.items():
            related_reals_ids = []
            for id,related_real in related_reals.items():
                related_reals_ids.append(id)
            meta_reals[meta.mvalue] = related_reals_ids

        return meta_reals
