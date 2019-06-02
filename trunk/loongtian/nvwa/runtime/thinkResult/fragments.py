#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

from loongtian.util.common.generics import GenericsList
from loongtian.nvwa.runtime.systemInfo import ThinkingInfo
from loongtian.nvwa.runtime.meanings import BaseMeaning, Meanings, Meaning


class BaseFragment(object):
    """
    [运行时对象]实际对象链中已经被处理过（理解、不理解、未满足条件）的部分片段的基础类
    """

    def __init__(self, realLevelResult, reals,
                 frag_start_pos_in_reals, frag_end_pos_in_reals,
                 cur_exe_pos, exe_pattern,
                 exe_meaning, exe_meaning_value,
                 memory=None):
        """
        [运行时对象]实际对象链中已经被处理过（理解、不理解、未满足条件）的部分片段的基础类。
        :param realLevelResult: 一个实际对象链的思考结果。
        :param reals: 片段所位于的实际对象（相关对象）列表
        :param frag_start_pos_in_reals: 片段在reals中的开始位置
        :param frag_end_pos_in_reals: 片段在reals中的结束位置
        :param cur_exe_pos: 片段中动作（可执行对象）在reals中的位置
        :param exe_pattern: 动作（可执行对象）匹配的模式（由于模式可能有多个，所以记录）
        :param exe_meaning: 动作（可执行对象）匹配模式对应的意义（由于模式对应的意义可能有多个，所以记录）
        """
        self.realLevelResult = realLevelResult
        self.reals = reals
        self.frag_start_pos_in_reals = frag_start_pos_in_reals  # 片段在reals中的开始位置
        self.frag_end_pos_in_reals = frag_end_pos_in_reals  # 片段在reals中的结束位置
        self.cur_exe_pos = cur_exe_pos
        self.exe_pattern = exe_pattern  # 模式
        self.exe_meaning = exe_meaning  # 意义
        self.exe_meaning_value = exe_meaning_value  # 意义的值

        # #############################
        # 运行时数据
        # #############################
        self._frag_exe = None  # 当前的可执行对象
        self._frag_poses = None  # 当前片段在reals中所有元素的位置
        self._frag_reals = None  # 当前片段在reals中所有元素
        self._frag_klg = None  # 当前片段在reals中所有元素组成的知识链。
        self._frag_klg_meanings = None  # 当前片段在reals中所有元素组成的知识链的意义（知识链）。

        self.memory = memory

    def getCurExe(self):
        """
        取得当前的可执行对象。
        :return:
        """
        if not self._frag_exe:
            self._frag_exe = self.reals[self.cur_exe_pos]
        return self._frag_exe

    def getPosesInReals(self):
        """
        取得当前片段在reals中所有元素的位置
        :return:
        """
        if not self._frag_poses:
            self._frag_poses = range(self.frag_start_pos_in_reals,
                                     self.frag_end_pos_in_reals + 1)

        return self._frag_poses

    def getFragmentedReals(self, memory=None):
        """
        取得当前片段在reals中所有元素
        :return:
        """
        if not self._frag_reals:  # 如果不存在或是没有元素，重新取
            temp_frag_reals = self.reals[self.frag_start_pos_in_reals:self.frag_end_pos_in_reals + 1]
            self._frag_reals = []
            # 如果是Realobject、Knowledge不处理，如果是UnderstoodFragment，生成knowledge
            for matched_real in temp_frag_reals:
                if isinstance(matched_real, UnderstoodFragment):
                    klg = matched_real.getFragmentedRealsKnowledge(memory=memory)
                    if klg:
                        self._frag_reals.append(klg)
                else:  # 这里可能是realobject或Knowledge
                    self._frag_reals.append(matched_real)
        return self._frag_reals

    def getFragmentedRealsKnowledge(self, recordInDB=False,memory=None):
        """
        取得当前片段在reals中所有元素组成的知识链。
        :return:
        """
        if not self._frag_klg:
            frag_reals = self.getFragmentedReals(memory=memory)
            if frag_reals:
                from loongtian.nvwa.models.knowledge import Knowledge
                self._frag_klg = Knowledge.createKnowledgeByObjChain(frag_reals,
                                                                     recordInDB=recordInDB,
                                                                     memory=memory)  # 不记录在数据库中

        return self._frag_klg

    @classmethod
    def _createByBaseFragment(cls, baseFragment, *args):
        """
        根据基础类创建对应的片段类
        :param baseFragment:
        :return:
        """
        _fragment = cls(baseFragment.realLevelResult,
                        baseFragment.reals,
                        baseFragment.frag_start_pos_in_reals,
                        baseFragment.frag_end_pos_in_reals,
                        baseFragment.cur_exe_pos,
                        baseFragment.exe_pattern,
                        baseFragment.exe_meaning,
                        baseFragment.exe_meaning_value,
                        baseFragment.memory,
                        *args)

        # #############################
        # 拷贝运行时数据
        # #############################
        _fragment._frag_exe = baseFragment._frag_exe  # 当前的可执行对象
        _fragment._frag_poses = baseFragment._frag_poses  # 当前片段在reals中所有元素的位置
        _fragment._frag_reals = baseFragment._frag_reals  # 当前片段在reals中所有元素
        _fragment._frag_klg = baseFragment._frag_klg  # 当前片段在reals中所有元素组成的知识链。
        _fragment._frag_klg_meanings = baseFragment._frag_klg_meanings  # 当前片段在reals中所有元素组成的知识链的意义（知识链）。

        return _fragment


class UnderstoodFragment(BaseFragment):
    """
    [运行时对象]实际对象链中已经被理解的部分片段
    """

    def __init__(self, realLevelResult, reals,
                 frag_start_pos_in_reals, frag_end_pos_in_reals,
                 cur_exe_pos, exe_pattern, exe_meaning, exe_meaning_value,
                 memory=None):
        """
        实际对象链中已经被理解的部分片段。
        :param reals: 片段所位于的实际对象（相关对象）列表
        :param frag_start_pos_in_reals: 片段的开始位置
        :param frag_end_pos_in_reals: 片段的结束位置
        :param cur_exe_pos: 片段中动作（可执行对象）的位置
        :param exe_pattern: 动作（可执行对象）匹配的模式（由于模式可能有多个，所以记录）
        :param exe_meaning: 动作（可执行对象）匹配模式对应的意义（由于模式对应的意义可能有多个，所以记录）
        :param meanings: 已经被迁移出来的意义（包装类。类型：runtime.meanings import Meanings）
        """
        super(UnderstoodFragment, self).__init__(realLevelResult, reals,
                                                 frag_start_pos_in_reals,
                                                 frag_end_pos_in_reals,
                                                 cur_exe_pos,
                                                 exe_pattern,
                                                 exe_meaning,
                                                 exe_meaning_value,
                                                 memory=memory)

        self.meanings = Meanings(memory=memory)

    def isRealsUnderstood(self):
        """
        根据已经理解的片段，判断是否全部实际对象链已经理解。
        :return:
        """
        return self.frag_end_pos_in_reals - self.frag_start_pos_in_reals + 1 == len(self.reals)

    @staticmethod
    def createByBaseFragment(baseFragment, meanings):
        """
        根据片段的基础类创建已经被理解的部分片段。
        :param baseFragment:
        :param meanings:
        :return:
        """
        _understoodFragment = UnderstoodFragment._createByBaseFragment(baseFragment)
        if not _understoodFragment:
            return None

        if not isinstance(meanings, Meanings):
            from loongtian.nvwa.models.knowledge import Knowledge
            if isinstance(meanings, list):
                for meaning_obj in meanings:
                    try:
                        cur_meaning = None
                        if isinstance(meaning_obj, list) or isinstance(meaning_obj, tuple):
                            cur_meaning = Meaning.createByObjChain(meaning_obj)
                        elif isinstance(meaning_obj, Knowledge):
                            cur_meaning = Meaning.createByKnowledge(meaning_obj)
                        elif isinstance(meaning_obj, BaseMeaning):
                            cur_meaning = meaning_obj

                        _understoodFragment.meanings.append(cur_meaning)
                    except Exception as ex:
                        raise Exception("给定的迁移后的意义不是runtime.meanings.Meaning类型，并且无法转换！ex:%s" % ex)
            elif isinstance(meanings, BaseMeaning):
                _understoodFragment.meanings.append(meanings)
            elif isinstance(meanings, Knowledge):
                try:
                    cur_meaning = Meaning.createByFullKnowledge(meanings)
                    _understoodFragment.meanings.append(cur_meaning)
                except Exception as ex:
                    raise Exception("给定的迁移后的意义不是runtime.meanings.Meaning类型，并且无法转换！ex:%s" % ex)
            else:
                raise Exception("给定的meanings不是runtime.meanings.Meanings类型！")
        else:
            _understoodFragment.meanings.extend(meanings)

        return _understoodFragment


class UnderstoodFragments(GenericsList):
    """
    [运行时对象]实际对象链中已经被理解的部分片段的列表。
    """

    def __init__(self, realLevelResult):
        """
        实际对象链中已经被理解的部分片段的列表。
        :param realLevelResult:
        """
        super(UnderstoodFragments, self).__init__(UnderstoodFragment)
        self.realLevelResult = realLevelResult

    def append(self, obj):
        """
        添加实际对象链中已经被理解的部分片段。重写append，以便能够设置realLevelResult.realLevelThinkingRecords的相关信息
        :param obj:
        :return:UnderstoodFragment
        """
        # 设置执行信息
        self.realLevelResult.realLevelThinkingRecords.setRealLevelExecuteRecord(
            ThinkingInfo.RealLevelInfo.ExecuteInfo.Processing_UnderstoodFragment, obj)

        if obj:
            super(UnderstoodFragments, self).append(obj)

            # 设置理解信息
            self.realLevelResult.realLevelThinkingRecords.setRealLevelUnderstoodRecord(
                ThinkingInfo.RealLevelInfo.UnderstoodInfo.FRAGMENT_UNDERSTOOD, obj)
        else:
            # 设置理解信息
            self.realLevelResult.realLevelThinkingRecords.setRealLevelUnderstoodRecord(
                ThinkingInfo.RealLevelInfo.UnderstoodInfo.FRAGMENT_MISUNDERSTOOD, None)


class CollectionFragment(BaseFragment):
    """
    [运行时对象]实际对象链中已经被当做集合理解的部分片段
    """

    def __init__(self, realLevelResult, reals,
                 frag_start_pos_in_reals, frag_end_pos_in_reals,
                 memory=None):
        """
        [运行时对象]实际对象链中已经被当做集合理解的部分片段
        :param realLevelResult:
        :param reals:
        :param frag_start_pos_in_reals:
        :param frag_end_pos_in_reals:
        :param memory:
        """
        super(CollectionFragment, self).__init__(realLevelResult, reals,
                                                 frag_start_pos_in_reals,
                                                 frag_end_pos_in_reals,
                                                 cur_exe_pos=None,
                                                 exe_pattern=None,
                                                 exe_meaning=None,
                                                 exe_meaning_value=None,
                                                 memory=memory)

        self.collection_klg = None
        self.collection_real = None
        self.entity_real = None  # 根据多个对象生成的实际对象，例如：中华-人民-共和国==》中华人民共和国


class CollectionFragments(GenericsList):
    """
    [运行时对象]实际对象链中已经被当做集合理解的部分片段的列表。
    """

    def __init__(self, realLevelResult):
        """
        实际对象链中已经被当做集合理解的部分片段的列表。
        :param realLevelResult:
        """
        super(CollectionFragments, self).__init__(CollectionFragment)
        self.realLevelResult = realLevelResult


class ModificationFragment(BaseFragment):
    """
    [运行时对象]实际对象链中已经被当做修限关系对象理解的部分片段
    """

    def __init__(self, realLevelResult, reals,
                 frag_start_pos_in_reals, frag_end_pos_in_reals,
                 memory=None):
        """
        [运行时对象]实际对象链中已经被当做集合理解的部分片段
        :param realLevelResult:
        :param reals:
        :param frag_start_pos_in_reals:
        :param frag_end_pos_in_reals:
        :param memory:
        """
        super(ModificationFragment, self).__init__(realLevelResult, reals,
                                                 frag_start_pos_in_reals,
                                                 frag_end_pos_in_reals,
                                                 cur_exe_pos=None,
                                                 exe_pattern=None,
                                                 exe_meaning=None,
                                                 exe_meaning_value=None,
                                                 memory=memory)

        self.entity_real = None  # 根据多个对象生成的实际对象，例如：中华-人民-共和国==》中华人民共和国

class UnsatisfiedFragment(BaseFragment):
    """
    [运行时对象]实际对象链中动作的pattern只能部分匹配的片段。
    """

    def __init__(self, realLevelResult, reals,
                 frag_start_pos_in_reals, frag_end_pos_in_reals,
                 cur_exe_pos, exe_pattern, exe_meaning, exe_meaning_value,
                 memory,
                 unsatisfied_poses, context_satisfaction_result,
                 ):
        """
        实际对象链中动作的pattern只能部分匹配的片段。
        :param reals: 片段所位于的实际对象（相关对象）列表
        :param frag_start_pos_in_reals: 片段的开始位置
        :param frag_end_pos_in_reals: 片段的结束位置
        :param cur_exe_pos: 片段中动作（可执行对象）的位置
        :param exe_pattern: 动作（可执行对象）匹配的模式（由于模式可能有多个，所以记录）
        :param exe_meaning: 动作（可执行对象）匹配模式对应的意义（由于模式对应的意义可能有多个，所以记录）
        :param unsatisfied_poses: # 未能匹配pattern的位置（list类型，可能有多个，负数为在前，正数为在后）
        """
        super(UnsatisfiedFragment, self).__init__(realLevelResult, reals,
                                                  frag_start_pos_in_reals,
                                                  frag_end_pos_in_reals,
                                                  cur_exe_pos,
                                                  exe_pattern,
                                                  exe_meaning,
                                                  exe_meaning_value,
                                                  memory=memory)

        self.unsatisfied_poses = []  # 未能匹配pattern的位置（list类型，可能有多个，负数为在前，正数为在后）
        unsatisfied_poses_add = True
        if unsatisfied_poses:
            if isinstance(unsatisfied_poses, list) or isinstance(unsatisfied_poses, tuple):
                self.unsatisfied_poses.extend(unsatisfied_poses)
            elif isinstance(unsatisfied_poses, int):
                self.unsatisfied_poses.append(unsatisfied_poses)
            else:
                unsatisfied_poses_add = False
        else:
            unsatisfied_poses_add = False

        if not unsatisfied_poses_add:
            raise Exception("未能匹配pattern的位置（unsatisfied_poses_add.可能有多个，负数为在前，正数为在后）！")

        # 上下文满足、未满足的情况(是一个tuple)
        self.context_satisfaction_result = context_satisfaction_result
        if context_satisfaction_result:  # 拆解，分项取得上下文的检查结果
            self.aboves_satisfied, self.nexts_satisfied, self.aboves_matched_or_need_parents, self.nexts_matched_or_need_parents = context_satisfaction_result

        # self.get_context_satisfaction() # 对其设置情况进行检查

    def get_context_satisfaction(self):
        """
        取得对上下文的需要情况（同时对其设置情况进行检查）。
        :return:
        """

        need_aboves = False
        need_nexts = False
        need_aboves_num = 0
        need_nexts_num = 0

        for unsatisfied_pose in self.unsatisfied_poses:
            if unsatisfied_pose < 0:
                need_aboves = True
                need_aboves_num += 1
            if unsatisfied_pose > 0:
                need_nexts = True
                need_nexts_num += 1

        if not need_aboves and not need_nexts:
            raise Exception("当前实际对象链中动作的pattern只能部分匹配的部分片段，既不需要上文，也不需要下文，不成立！")

        return need_aboves, need_nexts, need_aboves_num, need_nexts_num

    def isAllUnsatisfied(self):
        """
        未满足pattern的片段长度大于实际对象链的长度
        :return:
        """
        if self.frag_end_pos_in_reals - self.frag_start_pos_in_reals + 1 >= len(self.reals):
            return True
        return False

    @staticmethod
    def createByBaseFragment(baseFragment, unsatisfied_poses, context_satisfaction_result):
        """
        根据片段的基础类创建只能部分匹配的部分片段。
        :param baseFragment:
        :param unsatisfied_poses:
        :return:
        """
        _unsatisfiedFragment = UnsatisfiedFragment._createByBaseFragment(baseFragment,
                                                                         *[unsatisfied_poses,
                                                                           context_satisfaction_result])

        return _unsatisfiedFragment


class UnsatisfiedFragments(GenericsList):
    """
    [运行时对象]实际对象链中动作的pattern只能部分匹配的部分片段的列表。
    """

    def __init__(self, realLevelResult):
        """
        实际对象链中动作的pattern只能部分匹配的部分片段的列表。
        :param realLevelResult:
        """
        super(UnsatisfiedFragments, self).__init__(UnsatisfiedFragment)
        self.realLevelResult = realLevelResult

    def append(self, obj):
        """
        添加实际对象链中动作的pattern只能部分匹配的部分片段。重写append，以便能够设置realLevelResult.realLevelThinkingRecords的相关信息
        :param obj:UnsatisfiedFragment
        :return:
        """
        if not obj:
            return
        super(UnsatisfiedFragments, self).append(obj)
        # 设置执行信息
        self.realLevelResult.realLevelThinkingRecords.setRealLevelExecuteRecord(
            ThinkingInfo.RealLevelInfo.ExecuteInfo.Processing_UnsatisfiedFragments, obj)

        # 取得对上下文的需要情况（同时对其设置情况进行检查）。
        need_aboves, need_nexts, need_aboves_num, need_nexts_num = obj.get_context_satisfaction()
        if need_aboves:
            if need_nexts:
                # 设置匹配信息
                self.realLevelResult.realLevelThinkingRecords.setRealLevelMatchRecord(
                    ThinkingInfo.RealLevelInfo.MatchInfo.FRAGMENT_UNSATISFIED_NEED_CONTEXTS, obj)
            else:
                # 设置匹配信息
                self.realLevelResult.realLevelThinkingRecords.setRealLevelMatchRecord(
                    ThinkingInfo.RealLevelInfo.MatchInfo.FRAGMENT_UNSATISFIED_NEED_ABOVES, obj)
        else:
            if need_nexts:
                # 设置匹配信息
                self.realLevelResult.realLevelThinkingRecords.setRealLevelMatchRecord(
                    ThinkingInfo.RealLevelInfo.MatchInfo.FRAGMENT_UNSATISFIED_NEED_NEXTS, obj)


class UnknownObj(object):
    """
    [运行时对象]在一个realObject链（笛卡尔积子集）中未能正确理解的单个对象（Knowledge）
    """

    def __init__(self, realLevelResult, unknown_obj=None, position=-1):
        if not unknown_obj:
            raise Exception("参数错误，必须提供未知realObject、knowledge，或未知relatedObject！")

        self.realLevelResult = realLevelResult
        self.unknown_obj = unknown_obj
        self.position = position

    def __repr__(self):
        return "[UnknownObj]{unknown_obj:%s,position:%d}" % (self.unknown_obj, self.position)


class UnknownObjs(GenericsList):
    """
    [运行时对象]在一个realObject链（笛卡尔积子集）中未能正确理解的对象的列表。
    """

    def __init__(self, realLevelResult):
        """
        [运行时对象]在一个realObject链（笛卡尔积子集）中未能正确理解的对象的列表。
        :param realLevelResult:
        """
        super(UnknownObjs, self).__init__(UnknownObj)
        self.realLevelResult = realLevelResult

    def add(self, unknown_obj, pos):
        """
        添加一个未知对象
        :param unknown_obj:
        :param pos:
        :return:
        """
        _unknownObj = UnknownObj(self.realLevelResult, unknown_obj, pos)
        return self.append(_unknownObj)

    def __repr__(self):
        _str = ""
        for _unknownObj in self:
            _str += str(_unknownObj)
        return "[UnknownObjs]{%s}" % (_str)


import datetime


class UnknownMeta(object):
    """
    [运行时对象]在一个元数据链（笛卡尔积子集）中未能正确理解的单个对象
    """

    def __init__(self, metaLevelResult, unknown_meta=None, position=-1):
        """
        [运行时对象]在一个元数据链（笛卡尔积子集）中未能正确理解的单个对象
        :param metaLevelResult:
        :param unknown_meta:
        :param position:
        """
        if not unknown_meta:
            raise Exception("参数错误，必须提供未知metaData！")

        self.metaLevelResult = metaLevelResult
        self.unknown_meta = unknown_meta
        self.position = position
        self.timestamp = datetime.datetime.utcnow()

    @property
    def id(self):
        if self.unknown_meta:
            return self.unknown_meta.id
        return None

    def __repr__(self):
        return "[UnknownMeta]{unknown_meta:%s,position:%d}" % (self.unknown_meta, self.position)


class UnknownMetas(GenericsList):
    """
    [运行时对象]在一个元数据链（笛卡尔积子集）中未能正确理解的元数据对象列表
    """

    def __init__(self, item_type=UnknownMeta, id_tag="mvalue"):
        """
        [运行时对象]在一个元数据链（笛卡尔积子集）中未能正确理解的元数据对象列表
        :param item_type:
        :param id_tag:
        """
        super(UnknownMetas, self).__init__(item_type, id_tag)
        self.meta_times_dict = {}  # 记录未知元数据的出现次数{metadata:times}

    def add(self, unknown_meta, pos, metaLevelResult):
        """
        添加一个未知元数据对象，元字符串、出现时间、位置等值，记录未知元数据的出现次数
        :param unknown_meta:
        :param pos:
        :return:
        """
        _unknownMeta = UnknownMeta(metaLevelResult, unknown_meta, pos)
        # 记录未知元数据的出现次数
        self.increase_unknown_meta_apperence_times(unknown_meta)
        return self.append(_unknownMeta)

    def increase_unknown_meta_apperence_times(self, unknown_meta):
        """
        增加未知元数据的出现次数1次。
        :param unknown_meta:
        :return:
        """
        if unknown_meta.id in self.meta_times_dict:
            self.meta_times_dict[unknown_meta.id] += 1
        else:
            self.meta_times_dict[unknown_meta.id] = 1

    def get_unknown_meta_apperence_times(self, unknown_meta):
        """
        未知元数据的出现次数
        :param unknown_meta:
        :return:
        """
        return self.meta_times_dict.get(unknown_meta.id, 0)

    def remove(self, meta):
        """
        移除已经经过理解处理的元数据
        :param meta:
        :return:
        """
        need_remain_metas = []
        need_remove_metas_num = 0
        for unknownMeta in self:
            if unknownMeta.id == meta.id:
                need_remove_metas_num += 1
                continue
            need_remain_metas.append(unknownMeta)

        if need_remove_metas_num == 0:
            return

        try:
            self.meta_times_dict.pop(meta.id)
        except:
            pass

        self.__init__()

        for need_remain_meta in need_remain_metas:
            self.append(need_remain_meta)

    def __repr__(self):
        _str = ""
        for _unknown_meta in self:
            _str += str(_unknown_meta)
        return "[UnknownMetas]{%s}" % (_str)


class ProceedUnknownMeta(UnknownMeta):
    """
    [运行时对象]在一个元数据链（笛卡尔积子集）中，已经经过处理的未能正确理解的元数据对象
    """

    def __repr__(self):
        return "[ProceedUnknownMeta]{unknown_meta:%s,position:%d}" % (self.unknown_meta, self.position)


class ProceedUnknownMetas(UnknownMetas):
    """
    [运行时对象]在一个元数据链（笛卡尔积子集）中，已经经过处理的未能正确理解的元数据对象列表
    """

    def __init__(self):
        """
        [运行时对象]在一个元数据链（笛卡尔积子集）中，已经经过处理的未能正确理解的元数据对象列表
        :param item_type:
        :param id_tag:
        """
        super(ProceedUnknownMetas, self).__init__(ProceedUnknownMeta, id_tag="mvalue")

    def add(self, unknown_meta, pos, metaLevelResult):
        """
        添加一个未知元数据对象，元字符串、出现时间、位置等值，记录未知元数据的出现次数
        :param unknown_meta:
        :param pos:
        :return:
        """
        _unknownMeta = ProceedUnknownMeta(metaLevelResult, unknown_meta, pos)
        # 记录未知元数据的出现次数
        self.increase_unknown_meta_apperence_times(unknown_meta)
        return self.append(_unknownMeta)

    def __repr__(self):
        _str = ""
        for _unknown_meta in self:
            _str += str(_unknown_meta)
        return "[ProceedUnknownMetas]{%s}" % (_str)


class LinkedAction(object):
    """
    交联的两个动作的包装类
    """

    def __init__(self, realLevelResult, first_pos, *actions):
        """
        交联的两个动作的包装类
        :param realLevelResult:
        :param first_action:
        :param second_action:
        :param first_pos:
        """

        self.realLevelResult = realLevelResult
        self.actions = actions
        self.first_pos = first_pos


class LinkedActions(GenericsList):
    """
    在一个realObject链（笛卡尔积）中交联的两个动作的包装类的列表
    """

    def __init__(self, realLevelResult):
        """
        在一个realObject链（笛卡尔积）中交联的两个动作的包装类的列表
        """
        super(LinkedActions, self).__init__(LinkedAction)
        self.realLevelResult = realLevelResult

    def add(self, first_pos, *actions):
        _linkedAction = LinkedAction(self.realLevelResult, first_pos, *actions)
        return self.append(_linkedAction)


class JoinedUnderstoodFragments():
    """
    所有已经理解的片段可连接部分的列表（包括位置信息）
    """

    def __init__(self, realLevelResult):
        self.realLevelResult = realLevelResult
        self.joined_poses = []
        self.understood_fragment_list = []

    def add(self, frag_poses, understood_fragments):
        """
        添加已经理解的片段
        :param frag_poses:已经理解的片段中的元素位置列表[1,2,...n]
        :param understood_fragments:已经理解的片段列表[UnderstoodFragment]
        :return:
        """
        self.joined_poses.extend(frag_poses)
        self.understood_fragment_list.extend(understood_fragments)
        # ####################################
        #      下面为运行时数据
        # ####################################
        self._meanings_klgs = None  # 列表中所有的意义取得的知识链（多个）
        self._meanings_klg = None  # 根据列表中所有的意义创建的知识链（一个）

    def getMeaningsKnowledges(self,recordInDB=False, memory=None):
        """
        （注意与getMeaningsKnowledge的区别）取得列表中所有的意义取得的知识链（多个）
        :return:
        """
        if self._meanings_klgs:
            return self._meanings_klgs
        self._meanings_klgs = []
        for understoodFragment in self.understood_fragment_list:
            cur_meaning_klg = understoodFragment.meanings.getMeaningsKnowledge(recordInDB=recordInDB)
            self._meanings_klgs.append(cur_meaning_klg)
        return self._meanings_klgs

    def getMeaningsKnowledge(self,recordInDB=False):
        """
        （注意与getMeaningsKnowledges的区别）取得根据列表中所有的意义创建的知识链（一个）
        :return:
        """
        if self._meanings_klg:
            return self._meanings_klg
        _meanings_klgs = self.getMeaningsKnowledges()
        if _meanings_klgs:
            from loongtian.nvwa.models.knowledge import Knowledge
            self._meanings_klg = Knowledge.createKnowledgeByObjChain(_meanings_klgs,
                                                                     recordInDB=recordInDB)

        return self._meanings_klg


class JoinedUnderstoodFragmentsList(GenericsList):
    """
    所有已经理解的片段可连接部分的列表（包括位置信息）的列表。
    """

    def __init__(self):
        """
        所有已经理解的片段可连接部分的列表（包括位置信息）的列表。
        """
        super(JoinedUnderstoodFragmentsList, self).__init__(JoinedUnderstoodFragments)

    def append(self, obj):
        """
        （重载函数）添加到最后，需要考察是否被其他已连接的片段包含，如包含，不添加
        :param obj:
        :return:
        """
        if not obj or not isinstance(obj, JoinedUnderstoodFragments):
            return
        # 考察是否被其他已连接的片段包含，如包含，不添加
        for joinedUnderstoodFragments in self:
            if set(joinedUnderstoodFragments.joined_poses) > set(obj.joined_poses):
                return
        return super(JoinedUnderstoodFragmentsList, self).append(obj)

    def removeOtherContained(self):
        """
        去除被其他包含的已经理解的片段可连接部分的列表
        :return:
        :remarks: 例如：
        """
        need_remove_poses = []

        i = 0
        while i < len(self):
            pass


# ######################################
# 以下对象情况未知
# ######################################
class UnknownResult(list):
    """
    [运行时对象]在多个realObject链（笛卡尔积）中未能正确理解的对象。
    [UnknownObjs,UnknownResult]
    """

    def getRealUnknownResult(self):
        # 避免一个对象的层层递进
        unknown_result = self
        while True:
            if len(unknown_result) == 1 and isinstance(unknown_result[0], UnknownResult):
                unknown_result = unknown_result[0]
            else:
                break
        return unknown_result

    def getUnknownFirst(self):
        """
        取得完全未知对象(两个以上)组成的知识链，或是第一个未知对象
        :return:知识链，
        """
        first = self.__getitem__(0)
        # if first and isinstance(first,Knowledge):
        #     return first

        return first

    def __repr__(self):
        str = super(UnknownResult, self).__repr__()
        return "[UnknownResult]{%s}" % (str)

    pass


class Unknowns(list):
    """
    [运行时对象]在多个realObject链（笛卡尔积）中未能正确理解的对象。
    [UnknownObjs,UnknownResult]
    """

    def __init__(self):
        """
        [运行时对象]在多个realObject链（笛卡尔积）中未能正确理解的对象。
        """
        super(Unknowns, self).__init__()

    def getRealUnknown(self):
        # 避免一个对象的层层递进
        unknown_result = self
        while True:
            if len(unknown_result) == 1 and isinstance(unknown_result[0], Unknowns):
                unknown_result = unknown_result[0]
            else:
                break
        return unknown_result

    def getUnknownFirst(self):
        """
        取得完全未知对象(两个以上)组成的知识链，或是第一个未知对象
        :return:知识链，
        """
        first = self.__getitem__(0)
        # if first and isinstance(first,Knowledge):
        #     return first

        return first

    def __repr__(self):
        str = super(Unknowns, self).__repr__()
        return "[UnknownResult]{%s}" % (str)

    pass
