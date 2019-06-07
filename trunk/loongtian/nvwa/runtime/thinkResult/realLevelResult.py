#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

import uuid
import itertools
from loongtian.nvwa.runtime.systemInfo import ThinkingInfo
from loongtian.nvwa.runtime.instinct import Instincts
from loongtian.nvwa.runtime.thinkResult.thinkingRecords.realLevelRecords import RealLevelThinkingRecords
from loongtian.nvwa.runtime.thinkResult.fragments import (UnderstoodFragments,
                                                          CollectionFragments,
                                                          UnsatisfiedFragments,
                                                          UnknownObjs,
                                                          JoinedUnderstoodFragments,
                                                          JoinedUnderstoodFragmentsList,
                                                          LinkedActions)
from loongtian.nvwa.runtime.thinkResult.otherResults import (ParadigmResult,
                                                             AsCollectionResult,
                                                             InSightResult,
                                                             AssociationResult,
                                                             EvaluationResult,
                                                             EmotionResult,
                                                             PlanResult,
                                                             BehaviourResult)
from loongtian.util.common.generics import GenericsList


class RealLevelResult(object):
    """
    一个实际对象链的思考结果。
    """

    def __init__(self, reals, metaLevelResult):
        """
        一个实际对象链的思考结果。
        :param id:
        :param reals:
        """
        self.id = str(uuid.uuid1()).replace("-", "")
        self.metaLevelResult = metaLevelResult  # 当前RealLevelResult的父辈MetaLevelResult

        self.reals = list(reals)

        self._reals_matched_knowledges = None  # 直接根据real_chain匹配出来的知识链
        self._reals_matched_knowledges_meaning_klgs = None  # 根据real_chain匹配的knowledges向下一层取得的意义知识链

        # 1、对一条实际对象列表的理解（数据库查找、比较；迁移、线性排列规律(regulation)）的结果
        self.understoodFragments = UnderstoodFragments(self)  # 已经被理解的部分片段的列表。
        self.collectionFragments = CollectionFragments(self)
        self.unsatisfiedFragments = UnsatisfiedFragments(self)  # pattern只能部分匹配的部分片段的列表。
        self.unknownObjs = UnknownObjs(self)  # 在一个realObject链（笛卡尔积）中未能正确理解的对象。
        self.linkedActions = LinkedActions(self)  # 在一个realObject链（笛卡尔积）中前后相连的两个动作的包装类的列表

        self.realLevelThinkingRecords = RealLevelThinkingRecords(self)  # 关于思考状态的信息记录（这些状态在思维处理中不断被改变，是单向、互斥的）。

        self.understood_meaning_klg_dict = {}  # 由realChain查询到或最终迁移生成的知识链的字典{kid:knowledge}
        self.kid_possiblity_dict = {}  # 由realChain查询到或最终生成的知识链及其可能性的字典{kid:knowledge}

        self.anything_matched_klgs =None # 如果understood_meaning_klg_dict，里面有anything，进一步匹配出来的结果，例如：已知：牛有腿，牛有角，输入：牛有什么，输出：牛有腿，牛有角

        self.regeneratedRealLevelResults = RegeneratedRealLevelResults(self)  # 根据RealLevelResult的结果重新生成的子实际对象链的思考结果。

        # # 2、一条实际对象列表中未知对象的结果
        # self.unknownResult = UnknownResult

        # 3、一条实际对象列表根据范式(上下文)产生的的结果。
        self.paradigmResult = ParadigmResult(self)
        # 4、作为集合的思维结果，例如：建立索引，观察顺序，等。
        self.asCollectionResult = AsCollectionResult(self)
        # 5、系统操作(内观)的结果。
        self.inSightResult = InSightResult(self)
        # 6、联想的结果。
        self.associationResult = AssociationResult(self)
        # 7、对“理解”的结果进行评估分析的结果。
        self.evaluationResult = EvaluationResult(self)
        # 8、对“评估”结果进行情感计算的情感分析结果。
        self.emotionResult = EmotionResult(self)
        # 9、计划的结果（时间、地点、动作等）。
        self.planResult = PlanResult(self)
        # 10、根据“情感计算”的结果制定出的行为的执行结果。
        self.behaviourResult = BehaviourResult(self)

    @property
    def reals_matched_knowledges(self):
        """
        根据real_chain匹配的knowledges
        :return:
        """
        return self._reals_matched_knowledges

    @reals_matched_knowledges.setter
    def reals_matched_knowledges(self, value):
        """
        根据real_chain匹配的knowledges(函数内会设置其执行状态及匹配状态)
        :param value:
        :return:
        """
        # 设置ObjectsExecuteRecord执行状态
        self.realLevelThinkingRecords.setRealLevelExecuteRecord(
            ThinkingInfo.RealLevelInfo.ExecuteInfo.Processing_Matching_Knowledge, value)

        if value:
            # 设置匹配状态为KNOWLEDGE_MATCHED
            self.realLevelThinkingRecords.setRealLevelMatchRecord(
                ThinkingInfo.RealLevelInfo.MatchInfo.REAL_CHAIN_KNOWLEDGE_MATCHED,
                value)
        else:
            # 设置匹配状态为KNOWLEDGE_UNMATCHED
            self.realLevelThinkingRecords.setRealLevelMatchRecord(
                ThinkingInfo.RealLevelInfo.MatchInfo.REAL_CHAIN_KNOWLEDGE_UNMATCHED,
                None)

        self._reals_matched_knowledges = value

    @property
    def reals_matched_knowledges_meaning_klgs(self):
        """
        根据real_chain匹配的knowledges向下一层取得的意义知识链(函数内或设置其执行、匹配及理解状态)
        :return:
        """
        return self._reals_matched_knowledges_meaning_klgs

    @reals_matched_knowledges_meaning_klgs.setter
    def reals_matched_knowledges_meaning_klgs(self, value):
        """
        根据real_chain匹配的knowledges向下一层取得的意义知识链(函数内会设置其执行、匹配及理解状态)
        :param value:{reals_matched_knowledge:meaning_klgs}
        :return:
        """
        # 设置ObjectsExecuteRecord执行状态
        self.realLevelThinkingRecords.setRealLevelExecuteRecord(
            ThinkingInfo.RealLevelInfo.ExecuteInfo.Processing_Matched_Knowledge_Meaning, value)

        if value:
            # 设置匹配状态为MEANING_MATCHED
            self.realLevelThinkingRecords.setRealLevelMatchRecord(
                ThinkingInfo.RealLevelInfo.MatchInfo.REAL_CHAIN_KNOWLEDGE_MEANING_MATCHED,
                value)

            # 设置其理解状态
            self.realLevelThinkingRecords.setRealLevelUnderstoodRecord(
                ThinkingInfo.RealLevelInfo.UnderstoodInfo.MEANING_MATCHED_UNDERSTOOD,
                value)

        else:
            # 设置匹配状态为MEANING_UNMATCHED
            self.realLevelThinkingRecords.setRealLevelMatchRecord(
                ThinkingInfo.RealLevelInfo.MatchInfo.REAL_CHAIN_KNOWLEDGE_MEANING_UNMATCHED,
                None)
            # 不设置其理解状态（等待后续进一步处理）

        self._reals_matched_knowledges_meaning_klgs = value

    def hasUnderstoodFragments(self):
        """
        查看是否有已经理解的片段。
        :return:
        """
        return len(self.understoodFragments) > 0

    def getConflictedUnderstoodFragments(self):
        """
        取得理解片段的冲突部分（根据位置是否有交集，判断是否存在在冲突）。
        :return:[(understoodFragment1,understoodFragment2),(understoodFragment3,understoodFragment5)...]
        :remarks:
        例如：牛组件腿属性黄，可以分解出的理解片段包括：牛组件腿，腿属性黄，这就存在理解冲突
        这两部分存在冲突，按顺序只能满足前者，那么后者 “属性黄” 的上文就包括：腿、牛组件腿、牛，这需要进一步处理
        """
        conflictedUnderstoodFragments = []
        i = 0
        while i < len(self.understoodFragments):
            cur_understoodFragment = self.understoodFragments[i]
            cur_poses = range(cur_understoodFragment.frag_start_pos_in_reals,
                              cur_understoodFragment.frag_end_pos_in_reals + 1)

            if cur_understoodFragment.isRealsUnderstood():  # 已经全部理解，无需再继续向下寻找存在冲突的已理解片段
                i += 1  # 增加外层计数器
                continue

            j = i + 1
            while j < len(self.understoodFragments):
                next_understoodFragment = self.understoodFragments[j]
                next_poses = range(next_understoodFragment.frag_start_pos_in_reals,
                                   next_understoodFragment.frag_end_pos_in_reals + 1)
                # 求交集
                if set(cur_poses) & set(next_poses):
                    # 如果位置有交集，说明存在在冲突
                    conflictedUnderstoodFragments.append((cur_understoodFragment, next_understoodFragment))
                j += 1  # 增加里层计数器
            i += 1  # 增加外层计数器
        return conflictedUnderstoodFragments

    def hasUnsatisfiedFragments(self):
        """
        查看是否有尚需满足上下文的片段。
        :return:
        """
        return len(self.unsatisfiedFragments) > 0

    def hasUnknowns(self):
        """
        查看是否有未知对象（实际对象或知识链）。
        :return:
        """
        return len(self.unknownObjs) > 0

    def hasMatchedMeaning(self):
        """
        是否实际对象链直接在数据库中找到了知识链及其意义
        :return:
        """
        return self._reals_matched_knowledges and self._reals_matched_knowledges_meaning_klgs

    def hasLinkedActions(self):
        """
        判断是否有动词交联的情况
        :return:
        """
        return len(self.linkedActions) > 0

    def isAllUnderstood(self):
        """
        根据已经理解的片段，判断是否全部实际对象链已经理解。
        :return:
        :remarks:
        应该进一步根据各片段的终、始点进行连接，
        例如：牛有腿牛父对象动物，这句话分出两个理解片段：牛有腿，牛父对象动物
        但加在一起就是全部reals，相当于reals已经全部理解
        """
        allJoinedUnderstoodFragmentsList = self.getAllJoinedUnderstoodFragments()

        for joinedUnderstoodFragments in allJoinedUnderstoodFragmentsList:
            if len(joinedUnderstoodFragments.joined_poses) == len(self.reals):
                return True

        _curRealLevelUnderstoodInfo = self.realLevelThinkingRecords.curRealLevelUnderstoodInfo
        if _curRealLevelUnderstoodInfo == ThinkingInfo.RealLevelInfo.UnderstoodInfo.ALL_REALS_UNDERSTOOD or \
                _curRealLevelUnderstoodInfo == ThinkingInfo.RealLevelInfo.UnderstoodInfo.MEANING_MATCHED_UNDERSTOOD or \
                _curRealLevelUnderstoodInfo == ThinkingInfo.RealLevelInfo.UnderstoodInfo.EXECUTIONINFO_CREATED or \
                _curRealLevelUnderstoodInfo == ThinkingInfo.RealLevelInfo.UnderstoodInfo.EXECUTIONINFO_EXIST or \
                _curRealLevelUnderstoodInfo == ThinkingInfo.RealLevelInfo.UnderstoodInfo.EXECUTIONINFOS_CREATED or \
                _curRealLevelUnderstoodInfo == ThinkingInfo.RealLevelInfo.UnderstoodInfo.EXECUTIONINFOS_EXIST or \
                _curRealLevelUnderstoodInfo == ThinkingInfo.RealLevelInfo.UnderstoodInfo.SELF_EXPLAIN_SELF or \
                _curRealLevelUnderstoodInfo == ThinkingInfo.RealLevelInfo.UnderstoodInfo.SINGLE_UNDERSTOOD:
            return True

        return False

    def analysisUnderstoodFragments(self, addOnlyOne=True):
        """
        根据已经理解的片段，分析实际对象链的理解情况。
        :return:allUnderstood,partitalUnderstood（全部理解的，部分理解的）
        :remarks:
        应该进一步根据各片段的终、始点进行连接，
        例如：牛有腿牛父对象动物，这句话分出两个理解片段：牛有腿，牛父对象动物
        但加在一起就是全部reals，相当于reals已经全部理解
        """
        allJoinedUnderstoodFragmentsList = self.getAllJoinedUnderstoodFragments(addOnlyOne=addOnlyOne)

        allUnderstoodJoinedFrags = []  # 全部理解的
        partitalUnderstoodJoinedFrags = []  # 部分理解的
        for joinedUnderstoodFragments in allJoinedUnderstoodFragmentsList:
            if len(joinedUnderstoodFragments.joined_poses) == len(self.reals):
                allUnderstoodJoinedFrags.append(joinedUnderstoodFragments)
            else:
                partitalUnderstoodJoinedFrags.append(joinedUnderstoodFragments)

        return allUnderstoodJoinedFrags, partitalUnderstoodJoinedFrags

    def getAllJoinedUnderstoodFragments(self, addOnlyOne=True):
        """
        取得所有已经理解的片段可连接部分的位置列表
        :return:
        :remarks:
        应该进一步根据各片段的终、始点进行连接，
        例如：牛有腿牛父对象动物，这句话分出两个理解片段：牛有腿，牛父对象动物
        但加在一起就是全部reals，相当于reals已经全部理解
        """
        i = 0
        pose_frags = {}  # {(位置):understoodFragments}
        while i < len(self.understoodFragments):
            cur_understoodFragment = self.understoodFragments[i]
            cur_poses = tuple(cur_understoodFragment.getPosesInReals())
            if cur_poses in pose_frags:
                frags = pose_frags[cur_poses]
                if frags:
                    frags.append(cur_understoodFragment)
                else:
                    pose_frags[cur_poses] = [cur_understoodFragment]
            else:
                pose_frags[cur_poses] = [cur_understoodFragment]
            i +=1

        if not pose_frags:
            return None
        frags_list = []
        pose_list = list(pose_frags.keys())
        pose_list.sort()
        for pose in pose_list:
            frags_list.append(pose_frags[pose])

        regen_frags_list = []
        # 笛卡尔积
        for regen_frags in itertools.product(*frags_list):
            has_conjioned = False
            # 剔除位置有交叉的
            joined_poses = []
            for frag in regen_frags:
                # 求交集
                if not set(joined_poses) & set(frag.getPosesInReals()):
                    # 如果位置没有有交集，说明可以进行拼接（求并集）
                    joined_poses = set(joined_poses) | set(frag.getPosesInReals())
                else: # 如果有交集，直接停止
                    has_conjioned = True
                    break
            if not has_conjioned: # 剔除位置有交叉的
                regen_frags_list.append(regen_frags)

        allJoinedUnderstoodFragmentsList = JoinedUnderstoodFragmentsList()

        for regen_frags in regen_frags_list:
            curJoinedUnderstoodFragments = JoinedUnderstoodFragments(self)
            for frag in regen_frags:
                curJoinedUnderstoodFragments.add(frag.getPosesInReals(), [frag])
            allJoinedUnderstoodFragmentsList.append(curJoinedUnderstoodFragments)

        return allJoinedUnderstoodFragmentsList

    #
    # def getAllJoinedUnderstoodPoses(self):
    #     """
    #     取得所有已经理解的片段可连接部分的位置列表
    #     :return:
    #     :remarks:
    #     应该进一步根据各片段的终、始点进行连接，
    #     例如：牛有腿牛父对象动物，这句话分出两个理解片段：牛有腿，牛父对象动物
    #     但加在一起就是全部reals，相当于reals已经全部理解
    #     """
    #     allUnderstoodJoinedPoses = []
    #     i = 0
    #     while i < len(self.understoodFragments):
    #         cur_understoodFragment = self.understoodFragments[i]
    #         cur_poses = range(cur_understoodFragment.frag_start_pos_in_reals,
    #                           cur_understoodFragment.frag_end_pos_in_reals + 1)
    #
    #         if cur_understoodFragment.isRealsUnderstood():  # 已经全部理解，无需再继续向下寻找能够拼接的已理解片段
    #             allUnderstoodJoinedPoses.append(tuple(cur_poses))
    #             i += 1  # 增加外层计数器
    #             continue
    #
    #         joined_poses = []
    #         j = i + 1
    #         while j < len(self.understoodFragments):  # 继续向下寻找能够拼接的已理解片段
    #
    #             next_understoodFragment = self.understoodFragments[j]
    #             next_poses = range(next_understoodFragment.frag_start_pos_in_reals,
    #                                next_understoodFragment.frag_end_pos_in_reals + 1)
    #             # 求交集
    #             if not set(cur_poses) & set(next_poses):
    #                 # 如果位置没有有交集，说明可以进行拼接（求并集）
    #                 joined_poses.extend(set(cur_poses) | set(next_poses))
    #             j += 1  # 增加里层计数器
    #         i += 1  # 增加外层计数器
    #
    #         if joined_poses:  # 如果有拼接后的位置列表
    #             allUnderstoodJoinedPoses.append(tuple(joined_poses))
    #
    #     return allUnderstoodJoinedPoses

    def createMeaningsByUnderstoodFragments(self):
        """
        根据理解片段生成意义知识链
        :return:
        """
        allJoinedUnderstoodFragmentsList = self.getAllJoinedUnderstoodFragments()

        for joinedUnderstoodFragments in allJoinedUnderstoodFragmentsList:
            if not len(joinedUnderstoodFragments.joined_poses) == len(self.reals):  # 全理解
                continue
            cur_meanings_klgs = joinedUnderstoodFragments.getMeaningsKnowledge()
            self.understood_meaning_klg_dict[cur_meanings_klgs.id] = cur_meanings_klgs

        return self.understood_meaning_klg_dict

    def isAllUnknowns(self):
        """
        判断是否全部实际对象均未知。
        :return:
        """
        return len(self.unknownObjs) == len(self.reals)

    def isAllNeedContext(self):
        """
        未满足pattern的片段长度大于实际对象链的长度
        :return:
        """
        # todo 这个地方不对，待处理
        need_context_num = 0
        for unsatisfiedFragment in self.unsatisfiedFragments:
            if unsatisfiedFragment.isAllUnsatisfied():
                need_context_num += 1

        return need_context_num == len(self.unsatisfiedFragments)

    def isSelfExplainSelf(self):
        """
        当前的理解状态，是否是自解释（自己解释自己，例如：牛组件腿意义为牛组件腿，牛有腿就是牛有腿）。这种情况，只允许在“意义为”及其衍生对象中出现
        :return:
        """
        return self.realLevelThinkingRecords.curRealLevelUnderstoodInfo == ThinkingInfo.RealLevelInfo.UnderstoodInfo.SELF_EXPLAIN_SELF

    def isExecutionInfoCreated(self):
        """
        当前的理解状态，是否是生成意义。这种情况，只允许在“意义为”及其衍生对象中出现
        :return:
        """
        _curRealLevelUnderstoodInfo = self.realLevelThinkingRecords.curRealLevelUnderstoodInfo
        return _curRealLevelUnderstoodInfo == ThinkingInfo.RealLevelInfo.UnderstoodInfo.EXECUTIONINFO_CREATED or \
               _curRealLevelUnderstoodInfo == ThinkingInfo.RealLevelInfo.UnderstoodInfo.EXECUTIONINFO_EXIST or \
               _curRealLevelUnderstoodInfo == ThinkingInfo.RealLevelInfo.UnderstoodInfo.EXECUTIONINFOS_CREATED or \
               _curRealLevelUnderstoodInfo == ThinkingInfo.RealLevelInfo.UnderstoodInfo.EXECUTIONINFOS_EXIST

    def processUnknowns(self):
        """
        如果有未知的（实际对象或知识链），判断是否全部未知，如否，将能够按位置相连的未知实际对象连接在一起，
        :return:
        """

    def getAllUnderstoodKnowledges(self):
        """
        取得经过理解的知识链
        :return:
        """
        meaning_knowledges = []
        if self.understood_meaning_klg_dict:
            meaning_knowledges.extend(self.understood_meaning_klg_dict.values())
        if self.reals_matched_knowledges_meaning_klgs:
            meaning_knowledges.extend(self.reals_matched_knowledges_meaning_klgs)

        return meaning_knowledges

    def isSingle(self):
        """
        判断当前输入是否匹配出了一个实际对象（meta已知，实际对象已知）
        :return:
        """
        return len(self.reals) == 1


class RegeneratedRealLevelResult(RealLevelResult):
    """
    根据RealLevelResult的结果重新生成的子实际对象链的思考结果。
    """

    def __init__(self, reals, parent_realLevelResult):
        """
        一个实际对象链的思考结果。
        :param id:
        :param reals:
        """
        super(RegeneratedRealLevelResult, self).__init__(reals, parent_realLevelResult.metaLevelResult)
        # 父思考结果，子思考结果，孙思考结果，不断向下延伸
        self.parent_realLevelResult = parent_realLevelResult


class RegeneratedRealLevelResults(GenericsList):
    """
    根据RealLevelResult的结果重新生成的子实际对象链的思考结果。
    """

    def __init__(self, parent_realLevelResult):
        super(RegeneratedRealLevelResults, self).__init__(RegeneratedRealLevelResult)
        self.parent_realLevelResult = parent_realLevelResult

    def createNewRegeneratedRealLevelResult(self, reals):
        """
        创建一个新的重构的实际对象链的思考结果，并添加到当前列表中。
        :param reals:
        :return:
        """
        _regeneratedRealLevelResult = RegeneratedRealLevelResult(reals, self.parent_realLevelResult)
        self.append(_regeneratedRealLevelResult)
        return _regeneratedRealLevelResult
