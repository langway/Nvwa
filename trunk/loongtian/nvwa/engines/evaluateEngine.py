#!/usr/bin/env python
# -*- coding: utf-8 -*-


from loongtian.nvwa.engines.engineBase import EngineBase
import copy
from loongtian.util.log import logger
from loongtian.nvwa.models.realObject import RealObject
from loongtian.nvwa.models.metaData import MetaData
from loongtian.nvwa.models.metaNet import MetaNet
from loongtian.nvwa.models.knowledge import Knowledge
from loongtian.nvwa.runtime.relatedObjects import RelatedObj
from loongtian.nvwa.runtime.thinkResult.realLevelResult import RealLevelResult
from loongtian.nvwa.runtime.thinkResult.fragments import UnknownMeta, UnknownObj
from loongtian.nvwa.runtime.meanings import Meaning
from loongtian.nvwa.runtime.systemInfo import ThinkingInfo
from loongtian.nvwa.runtime.instinct import Instincts

class EvaluateEngine(EngineBase):
    """
    评估引擎。用来评估输入、输出结果对“我”的“价值”
    :rawParam
    :attribute
    """

    def __init__(self, memory):
        """
        评估引擎。用来评估输入、输出结果对“我”的“价值”
        :param memory: 用来存放当前对象的内存空间（避免每次都从数据库中调用）
                       当前EvaluateEngine的memory是MemoryCentral
        """
        super(EvaluateEngine, self).__init__(memory)

    def evaluate(self, thinkResult):
        """
        对“理解”思维的结果进行评估（评估输入、输出结果对“我”的“价值”）。
        :param thinkResult:
        :return:
        """
        self._simplistProcessThinkResult(thinkResult)

    def _simplistProcessThinkResult(self, thinkResult):
        """
        最简单化处理思考结果（啰啰嗦嗦，要尽量体现内部处理细节）。
        :param msg:
        :return:
        """

        for metaLevelResult in thinkResult:
            msg = ""
            # 0、查看元数据级别的匹配结果
            if metaLevelResult.isSingle():  # 单元数据
                if metaLevelResult.metaLevelThinkingRecords.curMetaLevelMatchInfo == ThinkingInfo.MetaLevelInfo.MatchInfo.SINGLE_META_UNMATCHED:
                    msg = "我不记得“%s”这个字符，也不知道是什么！" % thinkResult.rawInput

                elif metaLevelResult.metaLevelThinkingRecords.curMetaLevelMatchInfo == ThinkingInfo.MetaLevelInfo.MatchInfo.SINGLE_META_RELATED_REALS_UNMATCHED:
                    msg = "我记得“%s”这个字符，但不知道是什么！" % thinkResult.rawInput

                elif metaLevelResult.metaLevelThinkingRecords.curMetaLevelMatchInfo == ThinkingInfo.MetaLevelInfo.MatchInfo.SINGLE_META_RELATED_REALS_MATCHED:
                    msg = "我记得“%s”这个字符，记得其对应的实际对象有：%s" % (
                        thinkResult.rawInput,
                        self._getNatureLanguage(
                            metaLevelResult.metaLevelThinkingRecords.curMetaLevelMatchRecord.thinkingObj))
            else:  # 多元数据
                if metaLevelResult.metaLevelThinkingRecords.curMetaLevelMatchInfo == ThinkingInfo.MetaLevelInfo.MatchInfo.METANET_KNOWLEDGE_MEANING_MATCHED:
                    msg = "我记得“%s”这句话,记得意义为：%s" % self._getNatureLanguage(
                        metaLevelResult.meta_chain), self._getNatureLanguage(
                        metaLevelResult.meta_net_matched_knowledges_meaning_klgs)
                elif metaLevelResult.metaLevelThinkingRecords.curMetaLevelMatchInfo == ThinkingInfo.MetaLevelInfo.MatchInfo.META_CHAIN_UNMATCHED:
                    msg = "“%s”这句话中，所有的字符我都不知道是什么:“%s”！" % (
                        self._getNatureLanguage(metaLevelResult.meta_chain),
                        self._getNatureLanguage(metaLevelResult.unknownMetas))
                elif metaLevelResult.metaLevelThinkingRecords.curMetaLevelMatchInfo == ThinkingInfo.MetaLevelInfo.MatchInfo.META_CHAIN_PARTIAL_MATCHED:
                    msg = "“%s”这句话中，" % (self._getNatureLanguage(metaLevelResult.meta_chain))
                    if len(metaLevelResult.unknownMetas) > 0:
                        msg += "有%d个字符我不知道是什么:“%s”！" % (
                            len(metaLevelResult.unknownMetas), self._getNatureLanguage(metaLevelResult.unknownMetas))
                    if len(metaLevelResult.proceedUnknownMetas) > 0:
                        msg += "有%d个字符，虽然我不知道是什么，但已经过理解处理:“%s”！" % (
                            len(metaLevelResult.proceedUnknownMetas),
                            self._getNatureLanguage(metaLevelResult.proceedUnknownMetas))
                else:
                    msg = "我知道“%s”。" % self._getNatureLanguage(metaLevelResult.meta_chain)

            # 1、查看实际对象级别的理解、匹配结果
            realLevelResults = copy.copy(metaLevelResult)  # 这里必须复制一个，否则就pop没有了
            cur_msg = self._getRealLevelResultsMsgs(realLevelResults)
            if cur_msg:
                msg += cur_msg
            elif not metaLevelResult.isSingle():
                msg += "\r\n       这句话我没能理解！"

            msg = msg.lstrip("\r\n       ")
            self._simplistProcessMsg(msg)

    def _getRealLevelResultsMsgs(self, realLevelResults):

        if not realLevelResults:
            return

        msg = ""
        realLevelResults.reverse()  # 倒序，否则pop会从最后一个开始
        while True:
            cur_realLevelResult = None
            try:
                cur_realLevelResult = realLevelResults.pop()
            except:
                pass
            if not cur_realLevelResult:  # 如果没有了，停机
                break
            msg += self._getRealLevelResultMsg(cur_realLevelResult)
            if cur_realLevelResult.regeneratedRealLevelResults:
                # 不断递归，查看是否有下一级理解信息，直到结束。
                # 这里必须复制一个，否则就pop没有了
                sub_msg = self._getRealLevelResultsMsgs(
                    copy.copy(cur_realLevelResult.regeneratedRealLevelResults))  # 复制一个
                msg += sub_msg

        return msg

    def _getRealLevelResultMsg(self, realLevelResult):
        """

        :param realLevelResult:
        :return:
        """
        if not realLevelResult or not isinstance(realLevelResult, RealLevelResult):
            return ""
        msg = ""
        if realLevelResult.isSingle():
            if realLevelResult.realLevelThinkingRecords.curRealLevelUnderstoodInfo == ThinkingInfo.RealLevelInfo.UnderstoodInfo.SINGLE_MISUNDERSTOOD:
                # 跟上面MetaLevelInfo.MatchInfo.SINGLE_META_RELATED_REALS_UNMATCHED重复
                pass
            elif realLevelResult.realLevelThinkingRecords.curRealLevelUnderstoodInfo == ThinkingInfo.RealLevelInfo.UnderstoodInfo.SINGLE_UNDERSTOOD:
                # 跟上面MetaLevelInfo.MatchInfo.SINGLE_META_RELATED_REALS_MATCHED重复
                pass
            elif realLevelResult.realLevelThinkingRecords.curRealLevelUnderstoodInfo == ThinkingInfo.RealLevelInfo.UnderstoodInfo.SINGLE_UNDERSTOOD_NEED_CONTEXTS:
                msg += self._getContextMsg(realLevelResult.unsatisfiedFragments[0], realLevelResult)
        else:
            if realLevelResult.realLevelThinkingRecords.curRealLevelUnderstoodInfo == ThinkingInfo.RealLevelInfo.UnderstoodInfo.ALL_REALS_UNKNOWN:
                unknow_reals = realLevelResult.realLevelThinkingRecords.curRealLevelUnderstoodRecord.thinkingObj

                msg += "\r\n       并且这%d个实际对象我都不知道是什么：%s" % (len(unknow_reals), self._getNatureLanguage(unknow_reals))

            elif realLevelResult.realLevelThinkingRecords.curRealLevelUnderstoodInfo == ThinkingInfo.RealLevelInfo.UnderstoodInfo.REALS_NEED_CONTEXT:
                for unsatisfiedFragment in realLevelResult.unsatisfiedFragments:
                    msg += self._getContextMsg(unsatisfiedFragment, realLevelResult)
            elif realLevelResult.realLevelThinkingRecords.curRealLevelUnderstoodInfo == ThinkingInfo.RealLevelInfo.UnderstoodInfo.MEANING_MATCHED_UNDERSTOOD:
                msg += "\r\n       这句话我匹配到了已理解的知识链为：%s" % self._getNatureLanguage(
                    realLevelResult.realLevelThinkingRecords.curRealLevelUnderstoodRecord.thinkingObj)
            elif realLevelResult.realLevelThinkingRecords.curRealLevelUnderstoodInfo == ThinkingInfo.RealLevelInfo.UnderstoodInfo.ALL_REALS_UNDERSTOOD:

                if len(realLevelResult.understood_meaning_klg_dict) == 1:
                    klg = realLevelResult.understood_meaning_klg_dict.values()[0]
                    msg += "\r\n       这句话我理解为：%s" % self._getNatureLanguage(klg)
                else:
                    i = 1
                    for id, klg in realLevelResult.understood_meaning_klg_dict.iteritems():
                        msg += "\r\n       这句话我的第%s种理解为：%s" % (i, self._getNatureLanguage(klg))
                        i += 1

            elif realLevelResult.realLevelThinkingRecords.curRealLevelUnderstoodInfo == ThinkingInfo.RealLevelInfo.UnderstoodInfo.ALL_REALS_UNDERSTOOD_ANYTHING_MATCHED:

                if len(realLevelResult.understood_meaning_klg_dict) == 1:
                    klg = realLevelResult.understood_meaning_klg_dict.values()[0]
                    msg += "\r\n       这句话我理解为：%s" % self._getNatureLanguage(klg)
                else:
                    i = 1
                    for id, klg in realLevelResult.understood_meaning_klg_dict.iteritems():
                        msg += "\r\n       这句话我的第%s种理解为：%s" % (i, self._getNatureLanguage(klg))
                        i += 1

                msg += "\r\n       系统处理的结果为：\r\n       ["

                anything_indexes=[]
                i = 0
                for real in realLevelResult.reals:
                    if isinstance(real, RealObject):
                        if real.isAnything():
                            anything_indexes.append(i)
                    i += 1


                if realLevelResult.anything_matched_klgs:
                    for klg in realLevelResult.anything_matched_klgs:
                        components=klg.getSequenceComponents()
                        for anything_index in anything_indexes:
                            component=components[anything_index]
                            if component.id == Instincts.instinct_original_anything.id or\
                                component.Constitutions.isChild(Instincts.instinct_original_anything):
                                continue
                            msg += self._getNatureLanguage(component) + ","
                    msg = msg.rstrip(",")
                    msg += "]"

            elif realLevelResult.realLevelThinkingRecords.curRealLevelUnderstoodInfo == ThinkingInfo.RealLevelInfo.UnderstoodInfo.FRAGMENTS_CONFLICTED_MISUNDERSTOOD:
                msg += "\r\n       这句话有冲突，"
                for conflicted_understoodFragment in realLevelResult.realLevelThinkingRecords.curRealLevelUnderstoodRecord.thinkingObj:
                    msg += "到底是：%s，还是：%s" % (
                        self._getNatureLanguage(conflicted_understoodFragment[0].getFragmentedReals()),
                        self._getNatureLanguage(conflicted_understoodFragment[1].getFragmentedReals()))
            elif realLevelResult.realLevelThinkingRecords.curRealLevelUnderstoodInfo == ThinkingInfo.RealLevelInfo.UnderstoodInfo.SELF_EXPLAIN_SELF:
                msg += "\r\n       这句是车轱辘话，自己解释自己！"
            elif realLevelResult.realLevelThinkingRecords.curRealLevelUnderstoodInfo == ThinkingInfo.RealLevelInfo.UnderstoodInfo.EXECUTIONINFO_CREATED:
                thinking_obj = realLevelResult.realLevelThinkingRecords.curRealLevelUnderstoodRecord.thinkingObj
                msg += "\r\n       这句话创建了“%s”的意义！" % self._getNatureLanguage(thinking_obj.action)
            elif realLevelResult.realLevelThinkingRecords.curRealLevelUnderstoodInfo == ThinkingInfo.RealLevelInfo.UnderstoodInfo.EXECUTIONINFO_EXIST:
                thinking_obj = realLevelResult.realLevelThinkingRecords.curRealLevelUnderstoodRecord.thinkingObj
                msg += "\r\n       这句话匹配到了“%s”的意义！" % self._getNatureLanguage(thinking_obj.action)
        return msg

    def _getContextMsg(self, unsatisfiedFragment, realLevelResult):
        # 取得对上下文的需要情况（同时对其设置情况进行检查）。
        need_aboves, need_nexts, need_aboves_num, need_nexts_num = unsatisfiedFragment.get_context_satisfaction()

        msg = None
        if realLevelResult.realLevelThinkingRecords.curRealLevelMatchInfo == ThinkingInfo.RealLevelInfo.MatchInfo.FRAGMENT_UNSATISFIED_NEED_ABOVES:
            msg = "\r\n       想要理解这句话，“%s”这个对象需要%d个上文！" % (
                self._getNatureLanguage(unsatisfiedFragment.getCurExe()), need_aboves_num)
        elif realLevelResult.realLevelThinkingRecords.curRealLevelMatchInfo == ThinkingInfo.RealLevelInfo.MatchInfo.FRAGMENT_UNSATISFIED_NEED_NEXTS:
            msg = "\r\n       想要理解这句话，“%s”这个对象需要%d个下文！" % (
                self._getNatureLanguage(unsatisfiedFragment.getCurExe()), need_nexts_num)
        elif realLevelResult.realLevelThinkingRecords.curRealLevelMatchInfo == ThinkingInfo.RealLevelInfo.MatchInfo.FRAGMENT_UNSATISFIED_NEED_CONTEXTS:
            msg = "\r\n       想要理解这句话，“%s”这个对象需要%d个上文，%d个下文！" % (
                self._getNatureLanguage(unsatisfiedFragment.getCurExe()), need_aboves_num, need_nexts_num)

        return msg

    def _simplistProcessMsg(self, msg):
        """
        最简单化处理信息
        :param msg:
        :return:
        """
        if __debug__:
            print ("\r\n[nvwa]:%s" % msg)
        self.MemoryCentral.Brain.response(msg)

    def _getNatureLanguage(self, obj):
        """
        取得对象的自然语言
        :param obj:
        :return:
        """
        if isinstance(obj, RealObject):
            return obj.remark
        elif isinstance(obj, MetaData):
            return obj.mvalue
        elif isinstance(obj, MetaNet):
            obj.getSequenceComponents()
            return obj._t_chain_words
        elif isinstance(obj, Knowledge):
            components = obj.getSequenceComponents()
            return self._getNatureLanguage(components)
        elif isinstance(obj, RelatedObj):
            return self._getNatureLanguage(obj.obj)
        elif isinstance(obj, UnknownMeta):
            return self._getNatureLanguage(obj.unknown_meta)
        elif isinstance(obj, UnknownObj):
            return self._getNatureLanguage(obj.unknown_obj)
        elif isinstance(obj, Meaning):
            return self._getNatureLanguage(obj.toObjChain())
        elif isinstance(obj, list):
            nl = "["
            for _obj in obj:
                nl += self._getNatureLanguage(_obj) + ","
            nl = nl.rstrip(",")
            nl += "]"
            return nl
        elif isinstance(obj, dict):
            nl = "{"
            for id, _obj in obj.iteritems():
                nl += self._getNatureLanguage(_obj) + ","
            nl = nl.rstrip(",")
            nl += "}"
            return nl
