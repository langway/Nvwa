#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Leon'

import itertools
import copy
from loongtian.util.log import logger

from loongtian.nvwa.models.enum import ObjType
from loongtian.nvwa.models.baseEntity import BaseEntity
from loongtian.nvwa.models.metaData import MetaData
from loongtian.nvwa.models.metaNet import MetaNet
from loongtian.nvwa.models.realObject import RealObject
from loongtian.nvwa.models.knowledge import Knowledge

from loongtian.nvwa.runtime.instinct import Instincts
from loongtian.nvwa.runtime.article import StrContent,InShortPhrase
from loongtian.nvwa.runtime.relatedObjects import RelatedObj
from loongtian.nvwa.runtime.collection import Collection
from loongtian.nvwa.runtime.thinkResult.thinkResult import ThinkResult
from loongtian.nvwa.runtime.thinkResult.fragments import (BaseFragment,
                                                          UnderstoodFragment,
                                                          UnsatisfiedFragment,
                                                          CollectionFragment,
                                                          ModificationFragment,
                                                          JoinedUnderstoodFragments)
from loongtian.nvwa.runtime.thinkResult.realLevelResult import RealLevelResult, RegeneratedRealLevelResult
from loongtian.nvwa.runtime.systemInfo import ThinkingInfo, SystemInfo
from loongtian.nvwa.runtime.sequencedObjs import SequencedObj
from loongtian.nvwa.runtime.specialList import RelatedRealObjs, RelatedRealChain
from loongtian.nvwa.runtime.meanings import Meaning, ExecutionInfoCreatedMeaning, ExecutionInfoCreatedMeanings, \
    SelfExplainSelfMeaning
from loongtian.nvwa.runtime.reals import AdminUser

from loongtian.nvwa.engines.metaEngine import SegmentedResult, SegmentedResults
from loongtian.nvwa.managers.attentionManager import AttentionManager
from loongtian.nvwa.organs.character import Character


class Mind(SequencedObj):
    """
    一条输入的思维空间
    :rawParam
    构造函数参数说明
    :attribute
    对象属性说明
    """

    def __init__(self, thinkingCentral, strContent: StrContent, id=None):
        """
        一条输入的思维空间（Meta层，处理元输入、MetaData、MetaNet；Real层，处理Realobject、Knowledge）
        :param thinkingCentral: 
        :param id: 
        :param strContent: 原始输入
        :param metaChain: 
        :param unknown_metas_index: 
        """
        if not strContent or not strContent.containedObj:
            raise Exception("必须提供元输入，才能创建Mind！")

        super(Mind, self).__init__(id=id, containedObj=strContent)


        self.thinkingCentral = thinkingCentral  # 思维中枢
        self.Memory = None
        if thinkingCentral:
            self.Memory = thinkingCentral.Brain.MemoryCentral

        self.strContent = strContent
        # 对输入的思维结果
        self.strContent.thinkResult = ThinkResult(strContent)

        self.metaArea = MetaArea(self)  # 每个Mind的元数据/元数据网层面的处理区
        self.realArea = RealArea(self)  # 每个Mind的实际对象/知识链层面的处理区
        # self.knowledgeArea = KnowledgeArea(self)  # 每个Mind的既往知识区

        self.AttentionManager = AttentionManager()

        Instincts.loadAllInstincts(memory=self.Memory)  # 加载所有直觉对象，避免出现错误！

    def _setLast(self, value, setNext=False):
        """
        设置Last（重写方法）
        :param value:Mind
        :return:
        """
        # 设置输入区、工作（运算）区、既往知识区的上下文
        self.metaArea.setLast(value.metaArea, setNext)
        self.realArea.setLast(value.realArea, setNext)
        # self.knowledgeArea.setLast(value.knowledgeArea, setNext)

    def _setNext(self, value, setLast=False):
        """
        重写方法
        :param value:Mind
        :return:
        """
        # 设置输入区、工作（运算）区、既往知识区的上下文
        self.metaArea.setNext(value.metaArea, setLast)
        self.realArea.setNext(value.realArea, setLast)
        # self.knowledgeArea.setNext(value.knowledgeArea, setLast)

    def execute(self):
        """
        思考执行部分。
        :return:
        """
        try:
            self._execute(self.strContent)
        except Exception as ex:
            msg = "“%s”思考出现错误，原因：%s" % (self.strContent.containedObj, ex)
            logger.info(msg)
            self.thinkingCentral.Brain.response(msg)

        return self.strContent.thinkResult

    def _execute(self,strContent:StrContent):
        """
        [核心代码]真正的思考执行部分。
        :return:
        """
        # 设置Mind的执行信息
        strContent.thinkResult.setMindExecuteRecord(ThinkingInfo.MindExecuteInfo.Start_Mind)

        # 元数据 / 元数据网处理区执行思考
        self.metaArea.execute()

        # 如果在元数据层面没有“理解”，
        # 进一步在实际对象层面处理（单个元数据也要处理，例如等待上下文等）
        if not strContent.thinkResult.isMetaLevelUnderstood():
            self.realArea.execute()

        # 对“理解”的结果进行评估
        self.thinkingCentral.evaluateUnderstood(strContent.thinkResult)

        # 对“评估”的结果进行情感计算
        self.thinkingCentral.calculateEmotion(strContent.thinkResult)

        # 根据“情感计算”的结果制定行为
        self.thinkingCentral.createPlan(strContent.thinkResult)

        # 执行行为
        self.thinkingCentral.executeBehaviour(strContent.thinkResult)

        # 设置Mind的执行信息
        strContent.thinkResult.setMindExecuteRecord(ThinkingInfo.MindExecuteInfo.Stop_Mind)

        return strContent.thinkResult

    def isUsedByAdminUser(self):
        """
        判断当前Mind是否被管理用户使用。
        :return:
        """
        _AdminUser = AdminUser.getAdminUser(memory=self.Memory)

        if self.thinkingCentral and \
                self.thinkingCentral.Brain and \
                self.thinkingCentral.Brain.User.id == _AdminUser.id:
            return True

        return False

    def registUnknownMetas(self, cur_meta, pos, metas_level_result):
        """
        注册未知元数据。等待进一步开启新的Mind处理。
        :param cur_meta:
        :param metas_level_result:
        :param pos:
        :return:
        """
        metas_level_result.unknownMetas.add(cur_meta, pos, metas_level_result)
        self.thinkingCentral.Brain.MemoryCentral.WorkingMemory.UnknownMetas.add(cur_meta, pos, metas_level_result)

    def unregistUnknownMetas(self, cur_meta, metas_level_result):
        """
        注销未知元数据。
        :param cur_meta:
        :param metas_level_result:
        :param pos:
        :return:
        """
        metas_level_result.unknownMetas.remove(cur_meta)
        self.thinkingCentral.Brain.MemoryCentral.WorkingMemory.UnknownMetas.remove(cur_meta)

    def registProceedUnknownMetas(self, cur_meta, pos, metas_level_result):
        """
        注册已处理的未知元数据。等待进一步开启新的Mind处理。
        :param cur_meta:
        :param metas_level_result:
        :param pos:
        :return:
        """
        metas_level_result.proceedUnknownMetas.add(cur_meta, pos, metas_level_result)
        self.thinkingCentral.Brain.MemoryCentral.WorkingMemory.ProceedUnknownMetas.add(cur_meta, pos,
                                                                                       metas_level_result)

    def unregistProceedUnknownMetas(self, cur_meta, metas_level_result):
        """
        注销已处理的未知元数据。
        :param cur_meta:
        :param metas_level_result:
        :param pos:
        :return:
        """
        metas_level_result.proceedUnknownMetas.remove(cur_meta)
        self.thinkingCentral.Brain.MemoryCentral.WorkingMemory.ProceedUnknownMetas.remove(cur_meta)

    def processUnderstoodFragment(self, frag, record_knowledge=False):
        """
        已经理解一句（一段）话，对其中的元数据、实际数据、知识链进行处理（记录到数据库、从未知对象中移除等）
        :param frag:
        :return:
        """
        metas = frag.realLevelResult.metaLevelResult.meta_chain
        for meta in metas[frag.frag_start_pos_in_reals:frag.frag_end_pos_in_reals]:
            if meta._isInDB:  # 如果已经在数据库中了，略过
                continue
            # 现在在内存中，保存到数据库
            db_meta = meta.create(checkExist=False, recordInDB=True)
            # 加载到内存词典
            self.thinkingCentral.Brain.MemoryCentral.WorkingMemory.loadMetaToChainCharFrequncyMetaDict(db_meta)
            # 注销未知元数据
            self.unregistUnknownMetas(meta, frag.realLevelResult.metaLevelResult)
            # 取得内存中的关联对象
            related_reals = meta.Layers.getLowerEntitiesByType(ObjType.REAL_OBJECT)
            # 逐一保存到数据库
            while True:
                related_real = related_reals.getCurObj(return_related_obj=True)
                if not related_real:
                    break
                real = related_real.obj
                if real._isInDB:  # 如果已经在数据库中了，略过
                    continue
                real.create(checkExist=False, recordInDB=True)
                real.Layers.addUpper(meta, weight=related_real.weight, recordInDB=True)

        if record_knowledge:
            if isinstance(frag, BaseFragment):
                frag_reals_klg = frag.getFragmentedRealsKnowledge(memory=self.Memory)
                if not frag_reals_klg._isInDB:  # 如果已经在数据库中了，略过
                    components = frag_reals_klg.getSequenceComponents()
                    Knowledge.createKnowledgeByObjChain(components, recordInDB=True, memory=self.Memory)
            elif isinstance(frag, JoinedUnderstoodFragments):
                frag_reals_klgs = frag.getMeaningsKnowledges()
                for frag_reals_klg in frag_reals_klgs:
                    if not frag_reals_klg._isInDB:  # 如果已经在数据库中了，略过
                        components = frag_reals_klg.getSequenceComponents()
                        Knowledge.createKnowledgeByObjChain(components, recordInDB=True, memory=self.Memory)

    def recordAllUnderstoodJoinedFragments(self, frag, record_meta=True,
                                           record_metanet=True, record_real=True,
                                           record_knowledge=False):
        """
        已经理解一句（一段）话，对其中的元数据、实际数据、知识链进行处理（记录到数据库、从未知对象中移除等）
        :param frag:
        :param record_meta:
        :param record_metanet:
        :param record_real:
        :param record_knowledge:是否保存知识链，一般用户暂不保存
        :return:
        """

        metas = frag.realLevelResult.metaLevelResult.meta_chain
        metanet = None
        for i in frag.joined_poses:
            meta = None
            try:
                meta = metas[i]
            except:
                continue

            if meta._isInDB:  # 如果已经在数据库中了，略过
                continue
            if record_meta:
                # 现在在内存中，保存到数据库
                meta.recognized = True  # 设置为已识别
                meta.MemoryCentral = self.Memory
                db_meta = meta.create(checkExist=False, recordInDB=True)
                # 加载到内存词典
                self.Memory.WorkingMemory.loadMetaToChainCharFrequncyMetaDict(db_meta)
            # 注销未知元数据
            self.unregistUnknownMetas(meta, frag.realLevelResult.metaLevelResult)
            # 在已处理的未知元数据中注册
            self.registProceedUnknownMetas(meta, i, frag.realLevelResult.metaLevelResult)
            if record_real:
                # 取得内存中的关联对象
                related_reals = meta.Layers.getLowerEntitiesByType(ObjType.REAL_OBJECT)
                # 逐一保存到数据库
                while True:
                    related_real = related_reals.getCurObj(return_related_obj=True)
                    if not related_real:
                        break
                    real = related_real.obj
                    if real._isInDB:  # 如果已经在数据库中了，略过
                        continue
                    real.create(checkExist=False, recordInDB=True)
                    real.Layers.addUpper(meta, weight=related_real.weight, recordInDB=True)

        if record_metanet:
            metanet = MetaNet.createMetaNetByMetaChain(metas, memory=self.Memory)

        if record_knowledge:
            if isinstance(frag, BaseFragment):
                # 不记录创建意义的输入
                frag_reals = frag.getFragmentedReals(memory=self.Memory)
                if Instincts.hasInstinctMeaning(frag_reals):
                    return
                frag_klg = frag.getFragmentedRealsKnowledge(recordInDB=False, memory=self.Memory)
                if not frag_klg:
                    return
                self._recordKnowledge(frag_klg, metanet)
            elif isinstance(frag, JoinedUnderstoodFragments):
                # 不记录创建意义的输入
                if Instincts.hasInstinctMeaning(frag.realLevelResult.reals):
                    return
                frag_klg = Knowledge.createKnowledgeByObjChain(frag.realLevelResult.reals, recordInDB=False,
                                                               memory=self.Memory)
                if not frag_klg:
                    return
                db_klg = self._recordKnowledge(frag_klg, metanet)
                frag_meanings_klgs = frag.getMeaningsKnowledges(recordInDB=False)
                if not frag_meanings_klgs:
                    return
                for frag_meanings_klg in frag_meanings_klgs:
                    frag_klg_components = frag_meanings_klg.getSequenceComponents()
                    if RealObject.hasAnything(frag_klg_components):  # 意义中不能有anything
                        continue
                    else:
                        frag_meanings_klg.create(checkExist=False, recordInDB=True)

    def _recordKnowledge(self, klg, metanet):
        """
        记录知识链（并添加上层元数据网）
        :param klg:
        :param metanet:
        :return:
        """
        klg_components = klg.getSequenceComponents()
        if RealObject.hasAnything(klg_components):  # 意义中不能有anything
            return None
        else:
            db_klg = klg.create(checkExist=False, recordInDB=True)
            if metanet:  # 添加上层元数据网
                metanet.Layers.addLower(db_klg)
            return db_klg

    @staticmethod
    def _getConstitution(obj, constitutionType=None):
        """
        取得对象的所有构成
        :param obj: realobject or knowledge
        :param constitutionType: 构成类别（实际对象）
        :return:
        """

    @staticmethod
    def _associationByConstitution(obj):
        """
        根据对象的一条构成进行联想
        :param obj: realobject or knowledge
        :return:
        """

    @staticmethod
    def _thinkAsSingle(obj):
        """
        考察对象的构成
        :param obj:realobject or knowledge
        :return:
        """

    @staticmethod
    def _thinkAsCollection(obj):
        """
        将knowledge作为集合来进行思考。三种：1、链中所有的对象。2、knowledge的所有后链。3、所有构成组成的集合(根据构成种类分组)
        :param obj: realobject or knowledge
        :return:
        """

    @staticmethod
    def _compareObjects(obj1, obj2):
        """
        对象比较(id，构成，作为集合)
        :param obj1:
        :param obj2:
        :return:
        """

    @staticmethod
    def _compareCollection(col1, col2):
        """
        集合比较
        :param col1:
        :param col2:
        :return:
        """

    @staticmethod
    def _createParent(*objs):
        """
        父对象提取
        :param objs: 一个或多个对象
        :return:
        """

    @staticmethod
    def _createMeaning(metaChain):
        """
        根据元数据链创建meaning（根据“意义为”进行折断，然后生成模式）
        :param metaChain:
        :return:
        """

    @staticmethod
    def _getPattern(realObject):
        """
        取得实际对象的pattern（ 左右形式及左右对象类别）
        :param realObject: 实际对象
        :return:
        """

    @staticmethod
    def _getKnowledgeMeanings(knowledges):
        """
        取得通过metanet或real_chain查找到的知识链的意义（也是知识链）
        :param knowledges:
        :return:
        """
        knowledges_meaning_klgs = {}
        for kid, related_knowledge in knowledges.items():
            # 查看当前知识链是否被“理解”（当前知识链，或下层知识链是否具有顶级关系或匹配其他模式）
            cur_knowledge = related_knowledge.obj
            is_understood, meaning_klgs = cur_knowledge.isUnderstood()
            if is_understood:  # 如果已经理解
                knowledges_meaning_klgs[related_knowledge] = meaning_klgs

        return knowledges_meaning_klgs

    @staticmethod
    def _getMeaning(realObject):
        """
        取得实际对象的meaning（ 左右形式及左右对象类别）
        :param realObject: 实际对象
        :return:
        """
    # 元对象，及生成新的元对象的替换
    #
    # 用"像"来解决泛化的问题
    #
    # 这个牛，创造牛的一个实例
    #
    # 观察两方对象的交互，例如，甲：你好！乙：你好！


class MetaArea(SequencedObj):
    """
    每个Mind的元数据/元数据网处理区
    """

    def __init__(self, mind):
        """
        每个Mind的元数据/元数据网处理区
        :param mind:
        """
        super(MetaArea, self).__init__()
        self.Mind = mind
        # self.Last = None  # 上一个InputArea，与nextInputArea共同构成一个链
        # self.Next = None  # 下一个InputArea，与lastInputArea共同构成一个链

        if self.Mind and self.Mind.thinkingCentral:
            self.textEngine = self.Mind.thinkingCentral.Brain.PerceptionCentral.TextEngine  # 取得文本处理引擎

    def execute(self):
        """
        元数据/元数据网处理区执行思考
        :return:
        """
        self._processStrContent(self.Mind.strContent)


    def _processStrContent(self,strContent:StrContent):
        """
        真正的StrContent处理程序（可能会递归调用）
        :param strContent:
        :return:
        """
        if not strContent.thinkResult:
            strContent.thinkResult=ThinkResult(strContent)

        # 设置执行信息
        strContent.thinkResult.setMindExecuteRecord(ThinkingInfo.MindExecuteInfo.Processing_MetaArea)

        if len(strContent.containedObj) == 1:  # 0、如果只有一个字符：
            self._processSingleChar(strContent)
        elif len(strContent.containedObj) > 1:
            self._processMultiChars(strContent)


    def _processSingleChar(self,strContent:StrContent):
        """
        如果只有一个字符，处理之。
        :return:
        """
        # 从内存中取
        meta = self.Mind.Memory.getMetaByMvalueInMemory(strContent.containedObj)
        if meta:
            meta_chain = [meta]
            unknown_metas_index = []
        else:  # 如果内存中没有，在内存新建一个（暂不记录到数据库）
            meta = MetaData(mvalue=strContent.containedObj,
                            memory=self.Mind.Memory).create(recordInDB=False)
            meta_chain = [meta]
            unknown_metas_index = [0]

        # 对元数据链进行思考（一个字符的元数据，不需要重新分割）
        self._processMetaChain(strContent,meta_chain, unknown_metas_index, resegmentWithUnknowns=False)

    def _processMultiChars(self,strContent:StrContent):
        """
        如果有多个字符，处理之。
        :return:
        """
        # 1、使用输入字符串直接查询metaNet（可能有多个：南京市长江大桥，南京市-长江大桥，南京-市长-江大桥，可能都对）。
        meta_nets = MetaNet.getMetaNetsByStringValue(strContent.containedObj,
                                                     memory=self.Mind.Memory)

        if meta_nets:  # 2、如果使用字符串匹配到了元数据网，处理之
            if isinstance(meta_nets, list):
                for meta_net in meta_nets:
                    meta_chain = meta_net.getSequenceComponents()
                    metas_level_result = strContent.thinkResult.createNewMetaLevelResult(meta_chain, None)

                    self._processMetaNet(metas_level_result, meta_net)
            elif isinstance(meta_nets, MetaNet):
                meta_chain = meta_nets.getSequenceComponents()
                metas_level_result = strContent.thinkResult.createNewMetaLevelResult(meta_chain, None)

                self._processMetaNet(metas_level_result, meta_nets)
        else:  # 3、如果没能从元数据（元数据网）角度处理，思考进入strContent层面
            self._processMultiCharsStrContent(strContent)
            # 处理上下文
            self._processMultiCharsStrContentContext(strContent)

    def _processMultiCharsStrContent(self, str_content: StrContent):
        """
        如果没能从元数据（元数据网）角度处理，思考进入strContent层面，递归循环执行，
        :param str_content:
        :return:
        """
        if isinstance(str_content,InShortPhrase):
            # 上面已经对未知值进行了重新分割，所以这里为False
            return self._processSegmentResult(str_content,str_content.segmentedResult, resegmentWithUnknowns=False)

        if hasattr(str_content,"_getSubContents"):
            for _sub_content in str_content._getSubContents():
                self._processStrContent(_sub_content)

    def _processMultiCharsStrContentContext(self,str_content: StrContent):
        """
        在元数据层面处理上下文（查询metaNet）
        :param str_content:
        :return:
        """
        
    def _processRawInput(self,strContent:StrContent,rawinput):

        # 2、使用文本处理引擎对输入进行分割，以便进一步处理
        segment_result = self.textEngine.segmentInputWithChainCharMetaDict(
            rawinput,
            shouldLearn=False,  # 以后学习未知词汇尽量在整篇文章的级别，否则会导致很多连句词出现
            resegmentWithUnknowns=True)

        if segment_result:
            # if segment_result.isNotSegmented(): # 判断是否根本没有能够进行分割（整句输入，整句输出）
            #     pass
            # else:
            strContent.segment_result = segment_result
            # 对字符串的分割结果进行思考。
            # 上面已经对未知值进行了重新分割，所以这里为False
            self._processSegmentResult(strContent,segment_result, resegmentWithUnknowns=False)

    def _processSegmentResult(self,strContent:StrContent, segment_result, resegmentWithUnknowns=True):
        """
        对字符串的分割结果进行思考。
        :param segment_result: 字符串的分割结果
        :return:
        """

        if isinstance(segment_result, SegmentedResults):
            while True:
                # 根据当前的分割的结果创建元数据链（由于分割结果可能有多个，所以在处理时一条条调用，直到“理解”为止）
                # 内部已经重置了索引，以便从0开始
                for rawInput, meta_chain, unknown_metas_index in self.textEngine.getCurMetaChainBySegmentResults(
                        segment_result):
                    if not meta_chain:  # 如果没取到，暂停循环
                        break
                    self._processMetaChain(strContent,meta_chain, unknown_metas_index, resegmentWithUnknowns=resegmentWithUnknowns)

        elif isinstance(segment_result, SegmentedResult):
            # 重置索引，以便从0开始
            segment_result.restoreResultIndex()

            # 根据当前的分割的结果创建元数据链（由于分割结果可能有多个，所以在处理时一条条调用，直到“理解”为止）
            while True:
                cur_result = self.textEngine.getCurMetaChainBySegmentResult(segment_result)
                if not cur_result:
                    break
                rawInput, meta_chain, unknown_metas_index = cur_result
                if meta_chain:
                    self._processMetaChain(strContent,meta_chain, unknown_metas_index, resegmentWithUnknowns=resegmentWithUnknowns)

            # 重置索引，以便从0开始
            segment_result.restoreResultIndex()

    def _processMetaChain(self, strContent:StrContent,meta_chain, unknown_metas_index, resegmentWithUnknowns=True):
        """
        对元数据链进行思考
        :param meta_chain:
        :param unknown_metas_index:
        :return:
        """
        if not meta_chain:
            raise Exception("当前思维无法执行思考！metaChain is None or Empty！")

        # 创建一个元数据链的思考结果，并添加到thinkResult列表中。
        metas_level_result = strContent.thinkResult.createNewMetaLevelResult(meta_chain, unknown_metas_index)

        if metas_level_result.isSingle():  # 1、只有一个对象，取得其关联的实际对象(可能有多个)，看其是否被理解（有构成）
            # 处理单个元数据的情况
            cur_meta = meta_chain[0]
            strContent.thinkResult.isSingleMeta = True  # 单个元数据（包括理解不了的整句）
            self._processSingleMeta(cur_meta, metas_level_result, unknown_metas_index)

        else:
            self._processMultiMetas(meta_chain, metas_level_result, unknown_metas_index,
                                    resegmentWithUnknowns=resegmentWithUnknowns)

    def _processSingleMeta(self,cur_meta, metas_level_result, unknown_metas_index):
        """
        处理单个元数据的情况
        :param cur_meta:
        :param metas_level_result:
        :param unknown_metas_index:
        :return:
        """
        # 设置ObjectsExecuteRecord执行状态
        metas_level_result.metaLevelThinkingRecords.setMetaLevelExecuteRecord(
            ThinkingInfo.MetaLevelInfo.ExecuteInfo.Processing_MataData, cur_meta)

        if len(unknown_metas_index) == 1:  # 如果一个都未知，相当于什么都不知道（所有层面上）

            # 注册未知元数据。等待进一步开启新的Mind处理。
            self.Mind.registUnknownMetas(cur_meta, 0, metas_level_result)
            # 设置匹配信息
            metas_level_result.metaLevelThinkingRecords.setMetaLevelMatchRecord(
                ThinkingInfo.MetaLevelInfo.MatchInfo.SINGLE_META_UNMATCHED, cur_meta)

        else:
            # 设置ObjectsExecuteRecord执行状态
            metas_level_result.metaLevelThinkingRecords.setMetaLevelExecuteRecord(
                ThinkingInfo.MetaLevelInfo.ExecuteInfo.Processing_RelatedRealObjects, cur_meta)
            # 设置匹配信息
            metas_level_result.metaLevelThinkingRecords.setMetaLevelMatchRecord(
                ThinkingInfo.MetaLevelInfo.MatchInfo.SINGLE_META_MATCHED, cur_meta)
            # 取得meta关联的reals
            related_reals = cur_meta.Layers.getLowerEntitiesByType(ObjType.REAL_OBJECT)
            if related_reals:
                metas_level_result.meta_reals[cur_meta] = related_reals
                # 设置匹配信息
                metas_level_result.metaLevelThinkingRecords.setMetaLevelMatchRecord(
                    ThinkingInfo.MetaLevelInfo.MatchInfo.SINGLE_META_RELATED_REALS_MATCHED, related_reals)

            else:
                metas_level_result.meta_reals[cur_meta] = None
                # 设置匹配信息
                metas_level_result.metaLevelThinkingRecords.setMetaLevelMatchRecord(
                    ThinkingInfo.MetaLevelInfo.MatchInfo.SINGLE_META_RELATED_REALS_UNMATCHED, None)

    def _processMultiMetas(self, meta_chain,
                           metas_level_result,
                           unknown_metas_index,
                           resegmentWithUnknowns=True):
        """
        处理单个元数据的情况
        :param cur_meta:
        :param metas_level_result:
        :param unknown_metas_index:
        :return:
        """
        # 设置ObjectsExecuteRecord执行状态
        metas_level_result.metaLevelThinkingRecords.setMetaLevelExecuteRecord(
            ThinkingInfo.MetaLevelInfo.ExecuteInfo.Processing_MataDatas, meta_chain)

        if len(unknown_metas_index) > 0:
            # 处理有未知元数据的元数据链。
            self._processMetaChainWithUnknowns(meta_chain, metas_level_result, unknown_metas_index,
                                               resegmentWithUnknowns=resegmentWithUnknowns)

        else:  # 两个以上的元数据（全部已知），查询元数据链

            # 根据metaChain取得metaNet，然后查找是否有相关的知识链，如果找到了，并且是可以理解，直接返回
            # 0、使用完全匹配查询元数据链（只能有一个）
            unproceed = []
            metaNet = MetaNet.getByObjectChain(meta_chain, unproceed=unproceed,
                                               memory=self.Mind.Memory)  # todo 这里如果是部分匹配，应该能够处理
            # metaNet=MetaNet()
            if metaNet and not unproceed:
                if isinstance(metaNet, MetaNet) and len(metaNet.getSequenceComponents()) == len(meta_chain):
                    # 函数内会设置其理解状态为“元数据网已匹配”
                    self._processMetaNet(metas_level_result, metaNet)
                elif isinstance(metaNet, list):
                    total_lenght = 0
                    for _metaNet in metaNet:
                        total_lenght += len(_metaNet.getSequenceComponents())
                    if total_lenght != len(meta_chain):
                        raise Exception("取得的所有元数据链的长度之和不等于所有元数据的长度！")

                    for _metaNet in metaNet:
                        # 函数内会设置其理解状态为“元数据网已匹配”
                        self._processMetaNet(metas_level_result, _metaNet)

            else:
                # # 1、使用近似查询元数据链（可能有多个）
                # metaNets = MetaNet.getMetaNetLikeMetaChain(strContent.thinkResult.metaLevelResult.meta_chain)
                # if isinstance(metaNets, list) and len(metaNets) > 0:
                #     for metaNet in metaNets:
                #         self._processMetaNet(metaNet)
                #
                # elif isinstance(metaNets, MetaNet):
                #     self._processMetaNet(metaNets)
                # else:  # 3、没查到元数据网，设置其理解状态
                #     metas_level_result.setUnderstoodRecord(UnderstoodInfo.METANET_UNMATCHED)

                # 将其设置到metaLevelResult.meta_net
                # 函数内会设置其理解状态为“元数据网未匹配（等待进一步实际对象级别处理）”
                metas_level_result.set_meta_net(None)

                # 设置其匹配状态为“元数据全部匹配（等待进一步实际对象级别处理）”
                metas_level_result.metaLevelThinkingRecords.setMetaLevelMatchRecord(
                    ThinkingInfo.MetaLevelInfo.MatchInfo.META_CHAIN_MATCHED, None)
                # 不设置理解状态，等待后续处理

    def _processMetaChainWithUnknowns(self, meta_chain, metas_level_result,
                                      unknown_metas_index,
                                      resegmentWithUnknowns=True):
        """
        处理有未知元数据的元数据链。
        :param meta_chain:
        :param metas_level_result:
        :param unknown_metas_index:
        :return:
        """

        # 有未知的元数据，
        # 1、说明元数据网不可能存在，直接设置其理解状态为“元数据链部分匹配（等待进一步实际对象级别处理）”，
        # 2、注册未知元数据。等待进一步开启新的Mind处理。
        # 3、进一步使用其他已分出来的未知元数据重新处理meta，
        # 例如：牛有腿意义为牛组件为腿，初分出 牛有腿-意义为-牛-组件-腿，
        # 再次重分，分为：牛-有-腿-意义为-牛-组件-腿
        # 然后返回，等待在实际对象/知识链层面进一步处理

        if len(meta_chain) == len(unknown_metas_index):
            # 设置其匹配状态为“元数据链全部未匹配（等待进一步实际对象级别处理）”
            metas_level_result.metaLevelThinkingRecords.setMetaLevelMatchRecord(
                ThinkingInfo.MetaLevelInfo.MatchInfo.META_CHAIN_UNMATCHED, None)
            # 不设置理解状态，等待后续处理

        else:
            # 设置其匹配状态为“元数据链部分匹配（等待进一步实际对象级别处理）”
            metas_level_result.metaLevelThinkingRecords.setMetaLevelMatchRecord(
                ThinkingInfo.MetaLevelInfo.MatchInfo.META_CHAIN_PARTIAL_MATCHED, None)
            # 不设置理解状态，等待后续处理

        if resegmentWithUnknowns:
            # 进一步使用其他已分出来的未知元数据重新处理每一个meta（注册未知元数据。等待进一步开启新的Mind处理）
            self._resegmentWithUnknownMetas(metas_level_result, meta_chain, unknown_metas_index)
        else:  # 这里需要单独注册未知元数据，等待进一步开启新的Mind处理。
            for i in unknown_metas_index:
                cur_meta = meta_chain[i]
                #  注册未知元数据。等待进一步开启新的Mind处理。
                self.Mind.registUnknownMetas(cur_meta, i, metas_level_result)

    def _resegmentWithUnknownMetas(self, metas_level_result, meta_chain, unknown_metas_index):
        """
        进一步使用其他已分出来的未知元数据重新处理每一个meta（注册未知元数据。等待进一步开启新的Mind处理）
        :param metas_level_result:
        :param meta_chain:
        :param unknown_metas_index:
        :return:
        """
        import loongtian.nvwa.engines.metaDataHelper as  metaDataHelper
        for i in unknown_metas_index:
            cur_meta = meta_chain[i]

            #  注册未知元数据。等待进一步开启新的Mind处理。
            self.Mind.registUnknownMetas(cur_meta, i, metas_level_result)
            # 只有元数据，并且非单字符才需要用其他未识别的元数据进一步分割处理
            if not isinstance(cur_meta, MetaData) or not len(cur_meta.mvalue) > 1:
                continue

            # 进一步使用其他已分出来的未知元数据重新处理meta
            unknown_metas = []
            for j in metas_level_result.unknown_metas_index:  # 找到其他的未知元数据（不能用自身分割自身）
                if i == j:
                    continue
                other_meta = metas_level_result.meta_chain[j]
                if isinstance(other_meta, MetaData):  # 只有元数据，才能成为进一步分割的依据。
                    if not other_meta.mvalue == cur_meta.mvalue and \
                            cur_meta.mvalue.find(other_meta.mvalue) >= 0:  # 排除自身，并且能够找到（否则无法进一步分割）
                        unknown_metas.append(other_meta)
            if unknown_metas:  # 如果能够进行进一步分割，使用未知元数据再分割之，否则保持不变
                _resegmented_unknown_meta_chains = metaDataHelper.segmentWithUnknownMetas(
                    cur_meta, unknown_metas)
                if _resegmented_unknown_meta_chains:
                    if len(_resegmented_unknown_meta_chains) == 1:  # 扒皮
                        _resegmented_unknown_meta_chains = _resegmented_unknown_meta_chains[0]
                    if not isinstance(_resegmented_unknown_meta_chains, list):
                        metas_level_result.meta_chain[i] = _resegmented_unknown_meta_chains
                    else:
                        metas_level_result.meta_chain[i] = _resegmented_unknown_meta_chains[0]
                        k = 1
                        while k < len(_resegmented_unknown_meta_chains):
                            metas_level_result.meta_chain.insert(i + k, _resegmented_unknown_meta_chains[k])
                            k += 1

    def _processMetaNet(self, metaLevelResult, meta_net):
        """
        处理元数据网（查询其下一层knowledge）
        :param meta_net:
        :return:
        """
        # 将其设置到metaLevelResult.meta_net
        # 函数内会设置其执行状态，理解状态为“元数据网已匹配”
        metaLevelResult.set_meta_net(meta_net)

        # 取得元数据网下一层的知识链
        related_knowledges = meta_net.Layers.getLowerEntitiesByType(ObjType.KNOWLEDGE)

        # 将其设置到metaLevelResult.meta_net_matched_knowledges
        # 根据meta_net匹配的knowledges(函数内或设置其执行状态及匹配状态)
        metaLevelResult.set_meta_net_matched_knowledges(meta_net, related_knowledges)

        if related_knowledges:  # 只有在meta_net匹配出knowledges时，才进一步处理意义

            # 查看当前知识链是否被“理解”（当前知识链，或下层知识链是否具有顶级关系或匹配其他模式）
            meta_net_matched_knowledges_meaning_klgs = self.Mind._getKnowledgeMeanings(related_knowledges)

            # 设置根据meta_net匹配的knowledges向下一层取得的意义知识链
            # 函数内会设置其执行、匹配及理解状态
            metaLevelResult.set_meta_net_matched_knowledges_meaning_klgs(meta_net,
                                                                         meta_net_matched_knowledges_meaning_klgs)


class RealArea(SequencedObj):
    """
    每个Mind的实际对象/知识链工作（运算）区
    """

    def __init__(self, mind):
        """
        每个Mind的实际对象/知识链工作（运算）区
        :param mind:
        :param rawInput:
        :param inputType:
        """
        super(RealArea, self).__init__()
        self.Mind = mind

    def _get_sorted_realsChain(self,strContent:StrContent):
        """
        根据metaChain取得的realObject列表（排序状态，是个list，根据权重，最大值在前）
        :return:
        """

        for metaLevelResult in strContent.thinkResult:

            if metaLevelResult.isUndertood():  # 如果已经理解（匹配了元数据网-知识链-意义），无需进一步处理，继续下一个
                continue
            if metaLevelResult.sorted_realsChain_list:  # 如果已经取过了，继续下一个
                continue

            cur_meta_chain = metaLevelResult.meta_chain

            # 记录执行状态
            metaLevelResult.metaLevelThinkingRecords.setMetaLevelExecuteRecord(
                ThinkingInfo.RealLevelInfo.ExecuteInfo.Processing_MataDatas_To_Reals, cur_meta_chain)

            # 判断元数据链中是否包含resegmented_result对象
            if self._has_resegmented_result(cur_meta_chain):
                cur_meta_chain = self._processObjToIter(cur_meta_chain)
                # 笛卡尔积
                for child_meta_chain in itertools.product(*cur_meta_chain):
                    realLowerObjs, sorted_realsChain = MetaData.getAllRelatedRealObjsInMetaChain(child_meta_chain,
                                                                                                 recordInDB=False)  # 不记录在数据库中
                    metaLevelResult.realLowerObjs_list.append(realLowerObjs)
                    metaLevelResult.sorted_realsChain_list.append(sorted_realsChain)
            else:
                realLowerObjs, sorted_realsChain = MetaData.getAllRelatedRealObjsInMetaChain(cur_meta_chain,
                                                                                             recordInDB=False)  # 不记录在数据库中
                metaLevelResult.realLowerObjs_list.append(realLowerObjs)
                metaLevelResult.sorted_realsChain_list.append(sorted_realsChain)

    def _has_resegmented_result(self, meta_chain):
        """
        判断元数据链中是否包含resegmented_result对象
        :param meta_chain:
        :return:
        """
        from loongtian.nvwa.engines.metaDataHelper import ResegmentedUnknownMetaChains
        for meta in meta_chain:
            if isinstance(meta, ResegmentedUnknownMetaChains):
                return True
        return False

    def _processObjToIter(self, obj_chain):
        """
        将对象链（元数据、实际对象）中的元素替换为一个元素的list，例如：[meta]，以便itertools处理
        :param obj_chain:
        :return:
        """
        replaced_obj_chain = []
        for obj in obj_chain:
            if isinstance(obj, MetaData) or isinstance(obj, RealObject) or isinstance(obj, Knowledge):
                replaced_obj_chain.append([obj])
            else:  # todo 这个地方不一定对
                replaced_obj_chain.append(obj)
        return replaced_obj_chain

    def execute(self):
        """
        实际对象/知识链工作（运算）区执行思考
        :return:
        """
        return self._thinkStrContent(self.Mind.strContent)

    def _thinkStrContent(self,strContent:StrContent):
        # 设置Mind的执行信息
        strContent.thinkResult.setMindExecuteRecord(ThinkingInfo.MindExecuteInfo.Processing_RealArea)

        # 根据metaChain取得的realObject列表（排序状态，是个list，根据权重，最大值在前）
        self._get_sorted_realsChain(strContent)

        for metaLevelResult in strContent.thinkResult:
            if metaLevelResult.isUndertood():  # 如果已经理解（匹配了元数据网-知识链-意义），无需进一步处理，继续下一个
                continue

            if metaLevelResult.sorted_realsChain_list is None or len(metaLevelResult.sorted_realsChain_list) <= 0:
                raise Exception("当前思维运算区无法执行思考！realObjs is None！")

            for sorted_realsChain in metaLevelResult.sorted_realsChain_list:
                # 这里面都是RelatedRealChain，需要进一步笛卡尔积处理
                self._thinkRelatedRealChain(metaLevelResult, sorted_realsChain, think_one_by_one=True)

                # think_result=self.thinkRealLowerObjs(self.sorted_realsChain)
                # 返回的结果有以下几种类型：
                # 1、Knowledge  完全理解
                # 2、UnknownResult 完全不理解
                # 3、list，包括：
                #  （1）[UnknownResult,Knowledge] 部分理解，但理解部分都已组成了知识链
                #  （2）[UnknownResult,RealObject,Knowledge] 部分理解，但还有部分未能组成知识链

    def _thinkRelatedRealChain(self, metaLevelResult, relatedRealChain, think_one_by_one=True):
        """
        对可能嵌套的RelatedRealChain进一步拆箱
        :param relatedRealChain:
        :return:
        """
        # 对可能嵌套的RelatedRealChain进一步拆箱
        related_reals_list = []
        for related_obj in relatedRealChain:
            if isinstance(related_obj, RelatedRealObjs):
                related_reals_list.append(related_obj)
            elif isinstance(related_obj, RelatedRealChain):
                # 笛卡尔积
                cur_reals_list = []
                for cur_reals in itertools.product(*related_obj):
                    cur_reals_list.append(cur_reals)
                related_reals_list.append(cur_reals_list)

        # 笛卡尔积
        for related_reals in itertools.product(*related_reals_list):  # 这里是产生式
            # 真正的思考程序
            self._thinkRelatedReals(metaLevelResult, related_reals,
                                    think_one_by_one)  # 有可能是是knowledge，也有可能是UnknownResult

    def _thinkRelatedReals(self, metaLevelResult, related_reals, think_one_by_one=True):
        """
        思考一个实际对象(relatedObj)列表（可能嵌套）
        :param related_reals:
        :return:
        """
        if len(related_reals) == 0:  # 如果是空的，直接返回
            return
        elif len(related_reals) == 1:  # 只有一个实际对象，直接处理
            self._processSingleReal(metaLevelResult, related_reals, think_one_by_one)
        else:  # 有多个实际对象，对其进行分组，然后处理
            self._processRealChain(metaLevelResult, related_reals, think_one_by_one)

    def _processSingleReal(self, metaLevelResult, related_reals, think_one_by_one):
        """
        只有一个实际对象，直接处理
        :param metaLevelResult:
        :param related_reals:
        :param think_one_by_one:
        :return:
        """

        # 将realobject从relatedobject中拆出来
        reals_list = self._get_real_chain_from_related_real_chain(related_reals)
        # 创建一个实际对象链的思考结果，并添加到metaLevelResult中。
        _realLevelResult = metaLevelResult.createNewRealLevelResult(reals_list)

        # 设置执行信息
        _realLevelResult.realLevelThinkingRecords.setRealLevelExecuteRecord(
            ThinkingInfo.RealLevelInfo.ExecuteInfo.Processing_RealObject, reals_list[0])

        # 试图对实际对象链理解
        self._tryUnderstand(_realLevelResult, think_one_by_one)

    def _processRealChain(self, metaLevelResult, related_reals, think_one_by_one):
        """
        有多个实际对象，对其进行分组，然后处理
        :param metaLevelResult:
        :param related_reals:
        :param think_one_by_one:
        :return:
        """
        # 1、按照Action的范式及优先级进行分组（产生式，例如：我知道中国人民解放军是最棒的，小明用手拿起瓶子）
        # 例如：我知道中国人民解放军是最棒的 分组结果：[我,知道,[中国人民解放军,是,最棒的]，[[我,知道,中国人民解放军],是,最棒的]...
        # 小明用手拿起瓶子 分组结果：[小明,[[用,手],[拿,起]],瓶子],[小明,[用,[手拿,起]],瓶子]...
        # 牛有腿意义为牛组件为腿 分组结果：[[牛,有,腿],意义为,[牛,组件为,腿]],[牛,有,[腿,意义为,[牛组件为腿]]...

        # 调用分组引擎分组
        # 方法：
        # 1、查找到所有动作
        # 2、对动作按优先级排序
        # 3、查看是否符合动作的pattern
        # 4、按符合的进行分组
        # todo 下面三句代码是分组器临时替代方案
        # 调用分组器进行范式及关联度（词向量？）匹配，可能产生多种方案，笛卡尔积
        grouped_related_reals_list = self.Mind.thinkingCentral.GroupEngine.groupRealChain(related_reals)

        # 将realobject从relatedobject中拆出来
        grouped_reals_list = self._get_real_chain_from_related_real_chain(grouped_related_reals_list)

        grouped_reals_list = self._processObjToIter(grouped_reals_list)
        # 笛卡尔积
        for grouped_reals in itertools.product(*grouped_reals_list):
            # 转换成list
            grouped_reals = self.changeToList(grouped_reals)
            # 从牛有腿，牛组件腿，求同存异，推测出 possible word，牛，腿，推测出可能的动词，有
            # 创建一个实际对象链的思考结果，并添加到metaLevelResult中。
            _realLevelResult = metaLevelResult.createNewRealLevelResult(grouped_reals)

            # 设置执行信息
            _realLevelResult.realLevelThinkingRecords.setRealLevelExecuteRecord(
                ThinkingInfo.RealLevelInfo.ExecuteInfo.Processing_RealObjects, grouped_reals)

            # 0、首先查找是否有直接匹配的knowledge

            # 考虑多个匹配，例如：输入：牛有头马有尾巴，匹配到牛有头,马有尾巴
            unproceed = []  # 未能处理的对象
            matched_klgs = Knowledge.getByObjectChain(grouped_reals,
                                                      unproceed=unproceed,
                                                      memory=self.Mind.Memory)
            # 查看是否是全链匹配（有可能是部分匹配）
            if matched_klgs and not unproceed:  # 如果实际对象链匹配到知识链，查看其意义

                if not isinstance(matched_klgs, list):
                    matched_klgs = [matched_klgs]
                # 全链匹配
                # 设置根据real_chain匹配的knowledges(函数内会设置其执行状态及匹配状态)
                _realLevelResult.reals_matched_knowledges = matched_klgs

                for matched_klg in matched_klgs:
                    # 0.1 查看当前知识链是否被“理解”（当前知识链，或下层知识链是否具有顶级关系或匹配其他模式）
                    meaning_klgs = matched_klg.Meanings.getAllMeanings()  # 可能有多个

                    # 设置根据real_chain匹配的knowledges向下一层取得的意义知识链（可能没有）
                    # (函数内或设置其执行、匹配及理解状态)
                    if _realLevelResult.reals_matched_knowledges_meaning_klgs:
                        _realLevelResult.reals_matched_knowledges_meaning_klgs[matched_klg] = meaning_klgs
                    else:
                        _realLevelResult.reals_matched_knowledges_meaning_klgs = {matched_klg: meaning_klgs}
                    if not meaning_klgs:  # 如果没有意义，真正进行理解
                        self._tryUnderstand(_realLevelResult, think_one_by_one)

            else:  # 如果实际对象链没有匹配到知识链，真正进行理解
                # 设置根据real_chain匹配的knowledges(函数内会设置其执行状态及匹配状态)
                _realLevelResult.reals_matched_knowledges = None

                self._tryUnderstand(_realLevelResult, think_one_by_one)

    def changeToList(self, objs):
        li = []
        for obj in objs:
            if isinstance(obj, list) or isinstance(obj, tuple):
                li.append(self.changeToList(obj))
            else:
                li.append(obj)

        return li

    def _tryUnderstand(self, realLevelResult, think_one_by_one=True,
                       misunderstoodRethinkDepth=Character.Misunderstood_Rethink_Depth):
        """
        试图对实际对象链理解
        :param realLevelResult:
        :param think_one_by_one:
        :return:
        """
        if think_one_by_one:  # （目前使用）
            self._thinkOneByOne(realLevelResult, cur_pos=0)
        else:
            # self.thinkAsWhole(related_reals)
            pass
        # 对实际对象级别的结果进行进一步处理
        self._processRealLevelResult(realLevelResult, misunderstoodRethinkDepth)

    def _thinkOneByOne(self, realLevelResult, cur_pos=0):
        """
        【最核心的代码】模拟人的思维一个一个对象推进思维，例如：输入“牛有”，大脑会产生“牛有什么”，等待后文补充，下一个补充“腿”，就满足了条件，得到了思考结果，进一步可以进行评估等操作。
        :param realLevelResult:
        :param start_pos:
        :return:
        """
        if cur_pos < 0 or cur_pos >= len(realLevelResult.reals):  # 查看是否超出范围
            return
        cur_real = None
        try:
            cur_real = realLevelResult.reals[cur_pos]
        except:  # 有可能取不到，忽略
            return

        if not cur_real:
            return
        elif isinstance(cur_real, RelatedObj):
            cur_real = cur_real.obj
        elif isinstance(cur_real, UnderstoodFragment):
            cur_real = cur_real.getFragmentedRealsKnowledge(memory=self.Mind.Memory)
        elif (not isinstance(cur_real, RealObject) and
              not isinstance(cur_real, Knowledge)):
            return

            # 只有实际对象才能“执行”,knowledge、UnderstoodFragment直接略过
        if isinstance(cur_real, RealObject):
            if not cur_real.isExecutable():
                # 判断是否是新创建的，并且未保存到数据库（完全未知小鲜肉）
                if not cur_real._isInDB and cur_real._isNewCreated:
                    #  注册未知实际对象。等待进一步开启新的Mind处理。
                    realLevelResult.unknownObjs.add(cur_real, cur_pos)
            else:
                # 如果是动作（可执行的），查看是否匹配其pattern
                # 取得下一个(或下几个)对象，如果也是可执行的，那么放到linkedActions，不继续执行，等待进一步处理
                _action_test_pos = cur_pos + 1
                _conjugated_actions = []
                while _action_test_pos < len(realLevelResult.reals):
                    next_real = realLevelResult.reals[_action_test_pos]
                    if next_real and isinstance(next_real, RealObject) and next_real.isExecutable():
                        _conjugated_actions.append(next_real)
                        _action_test_pos += 1
                    else:
                        break

                if _conjugated_actions:
                    _conjugated_actions.insert(0, cur_real)
                    realLevelResult.linkedActions.add(cur_pos, *_conjugated_actions)  # actions
                    cur_pos = _action_test_pos - 1
                else:
                    # 根据可执行对象取得执行结果
                    # 使用模板函数操作_inner_function_process_executable
                    self.ProcessExeWithInnerFunction(cur_real, cur_pos, realLevelResult.reals,
                                                     self._inner_function_process_executable, realLevelResult)

        # 添加到注意力引擎
        if self.Mind.AttentionManager.addFocus(cur_real):
            pass

        # 继续处理下一个
        self._thinkOneByOne(realLevelResult, cur_pos + 1)

    def ProcessExeWithInnerFunction(self, cur_exe, exe_pos, reals, inner_function, *inner_function_args):
        """
        [模板函数]由于处理单个可执行对象的程序相同，将其抽取出来，制成的模板函数
        :return:
        """

        cur_exe_info = cur_exe.ExecutionInfo.getSelfLinearExecutionInfo()
        if not cur_exe_info:
            return
        if not cur_exe_info.isExecutable():
            return
        cur_exe_info.restoreCurObjIndex()  # 重置索引
        while True:
            exe_pattern, exe_meaning, exe_meaning_value = cur_exe_info.getCur()
            if not exe_pattern or not exe_meaning:  # 已经取不到了，停止循环
                break

            # 取得对可执行实际对象的pattern的检查结果。
            _exe_pattern_check_result = self._check_exe_pattern(reals, cur_exe, exe_pos, exe_pattern, exe_meaning)
            if not _exe_pattern_check_result:
                continue
            if not _exe_pattern_check_result.context_satisfaction_result:
                continue
            _exe_pattern_check_result.exe_meaning_value = exe_meaning_value

            can_break = inner_function(_exe_pattern_check_result, *inner_function_args)
            if can_break:
                break

        cur_exe_info.restoreCurObjIndex()  # 重置索引

    def _inner_function_process_executable(self, exe_pattern_check_result, realLevelResult):
        """
        （内部函数）根据可执行对象取得执行结果
        :param exe_pattern_check_result:
        :param realLevelResult:
        :return:
        """
        if not exe_pattern_check_result or not isinstance(exe_pattern_check_result, RealArea.ExePatternCheckResult):
            raise Exception("参数错误：exe_pattern_check_result，必须是RealArea._ExePatternCheckResult类型！")

        # 分项取得上下文的检查结果（context_satisfaction_result是一个tuple）
        aboves_satisfied, nexts_satisfied, aboves_matched_or_need_parents, \
        nexts_matched_or_need_parents = exe_pattern_check_result.context_satisfaction_result

        frag = BaseFragment(realLevelResult,
                            realLevelResult.reals,
                            exe_pattern_check_result.frag_start_pos_in_reals,
                            exe_pattern_check_result.frag_end_pos_in_reals,
                            exe_pattern_check_result.exe_pos,
                            exe_pattern_check_result.exe_pattern,
                            exe_pattern_check_result.exe_meaning,
                            exe_pattern_check_result.exe_meaning_value,
                            self.Mind.Memory)

        if aboves_satisfied:
            if nexts_satisfied:  # 上下文数量均能满足模式，查找数据库（对应的知识链及其意义），如果没找到，进行迁移（理解）

                self._do_fragment_context_satisfied(realLevelResult, frag)

            else:  # 如果下文的数量不满足，记录到UnsatisfiedFragment，等待下文
                if isinstance(realLevelResult, RegeneratedRealLevelResult):
                    a = 1

                unsatisfied_poses = list(range(1, exe_pattern_check_result.nexts_num_needed + 1))
                self._do_fragment_context_unsatisfied(realLevelResult,
                                                      frag,
                                                      exe_pattern_check_result.context_satisfaction_result,
                                                      unsatisfied_poses)
        else:  # 如果上文的数量不满足，记录到UnsatisfiedFragment，等待查找上文
            if isinstance(realLevelResult, RegeneratedRealLevelResult):
                a = 1

            unsatisfied_poses = list(range(-exe_pattern_check_result.aboves_num_needed, 0))  # 取得上文不满足的位置
            if not nexts_satisfied:  # 如果下文也不满足，同时记录下文不满足的位置
                unsatisfied_poses.extend(range(1, exe_pattern_check_result.nexts_num_needed + 1))

            self._do_fragment_context_unsatisfied(realLevelResult,
                                                  frag,
                                                  exe_pattern_check_result.context_satisfaction_result,
                                                  unsatisfied_poses)

    class ExePatternCheckResult(object):
        """
        对可执行实际对象的pattern的检查结果，是一个私有类
        """

        def __init__(self):
            """
            对可执行实际对象的pattern的检查结果，是一个私有类
            """
            self.reals = None

            self.cur_exe = None
            self.exe_pos = None
            self.exe_pattern = None
            self.exe_meaning = None
            self.exe_meaning_value = None

            self.aboves_num_needed = None  # 需要上文对象的数量
            # 查看现有上文的数量是否能够满足，如果满足，继续查看下文的数量；如果不满足，说明当前的pattern不能匹配，舍弃之
            self.nexts_num_needed = None
            self.frag_start_pos_in_reals = None
            self.frag_end_pos_in_reals = None

            # 判断上下文对象的数量、类型是否相符
            self.context_satisfaction_result = None

    def _check_exe_pattern(self, reals, cur_exe, exe_pos, exe_pattern, exe_meaning):
        """
        取得对可执行实际对象的pattern的检查结果。
        :param realLevelResult:
        :param exe_pattern:
        :param cur_exe:
        :param exe_pos:
        :return:
        """

        _exe_pattern_check_result = RealArea.ExePatternCheckResult()
        _exe_pattern_check_result.cur_exe = cur_exe
        _exe_pattern_check_result.exe_pos = exe_pos
        _exe_pattern_check_result.exe_pattern = exe_pattern
        _exe_pattern_check_result.exe_meaning = exe_meaning
        _exe_pattern_check_result.reals = reals

        pattern_components = exe_pattern.getSequenceComponents()

        exe_pos_in_pattern = RealArea.getIndexInlist(pattern_components, cur_exe,
                                                     raiseException=True,  # 有可能查不到会抛出错误
                                                     errorMsg="当前可执行实际对象不在其定义的pattern之中！pattern定义错误！")

        _exe_pattern_check_result.aboves_num_needed = abs(0 - exe_pos_in_pattern)  # 需要上文对象的数量
        # 查看现有上文的数量是否能够满足，如果满足，继续查看下文的数量；如果不满足，说明当前的pattern不能匹配，舍弃之
        _exe_pattern_check_result.nexts_num_needed = len(pattern_components) - 1 - exe_pos_in_pattern
        _exe_pattern_check_result.frag_start_pos_in_reals = exe_pos - _exe_pattern_check_result.aboves_num_needed
        _exe_pattern_check_result.frag_end_pos_in_reals = exe_pos + _exe_pattern_check_result.nexts_num_needed

        # 判断上下文对象的数量、类型是否相符
        _exe_pattern_check_result.context_satisfaction_result = \
            self._check_context_satisfaction(reals,
                                             _exe_pattern_check_result.aboves_num_needed,
                                             _exe_pattern_check_result.nexts_num_needed,
                                             pattern_components,
                                             exe_pos_in_pattern,
                                             exe_pos)

        return _exe_pattern_check_result

    def _check_context_satisfaction(self, reals, aboves_num_needed, nexts_num_needed,
                                    pattern_components, exe_pos_in_pattern, cur_pos):
        """
        判断上下文对象的数量、类型（父对象）是否相符
        :param realLevelResult:
        :param aboves:
        :param aboves_num_needed:
        :param nexts_num_needed:
        :param pattern_components:
        :param exe_pos_in_pattern:
        :param cur_pos:
        :return:
        """

        aboves_satisfied = False
        nexts_satisfied = False

        aboves_matched_or_need_parents = None
        nexts_matched_or_need_parents = None

        # 1、上文对象（数量）能够满足
        if cur_pos - aboves_num_needed >= 0:
            # 1.1 进一步进行类型判断
            objects_need_match = reals[cur_pos - aboves_num_needed:cur_pos]
            pattern_components_need_match = pattern_components[0:exe_pos_in_pattern]

            # i=1
            # for pattern_component_need_match in pattern_components_need_match:
            #     if not (isinstance(pattern_component_need_match,
            #                   RealObject) and pattern_component_need_match.isPlaceHolder()):
            #         i+=1
            #         continue
            #
            #     object_need_match = realLevelResult.reals[cur_pos-i]
            #     pattern_component_need_match_parents, related_ks = pattern_component_need_match.Constitutions.getSelfParentObjects()
            #     if pattern_component_need_match_parents:
            #         for pattern_component_need_match_parent in pattern_component_need_match_parents:
            #             # 如果是元知识链，特殊处理
            #             if pattern_component_need_match_parent.Constitutions.isChild(Instincts.instinct_original_knowledge):
            #                 if isinstance(object_need_match, Knowledge):
            #                     aboves_satisfied= True

            aboves_satisfied, aboves_matched_or_need_parents = self._check_each_one_matched(aboves_num_needed,
                                                                                            objects_need_match,
                                                                                            pattern_components_need_match)

        # 2、下文对象（数量）能够满足
        if nexts_num_needed <= len(reals) - cur_pos - 1:
            # 2.1 进一步进行类型判断
            objects_need_match = reals[cur_pos + 1:cur_pos + 1 + nexts_num_needed]
            pattern_components_need_match = pattern_components[exe_pos_in_pattern + 1:]
            nexts_satisfied, nexts_matched_or_need_parents = self._check_each_one_matched(nexts_num_needed,
                                                                                          objects_need_match,
                                                                                          pattern_components_need_match)

        return aboves_satisfied, nexts_satisfied, aboves_matched_or_need_parents, nexts_matched_or_need_parents

    def _check_each_one_matched(self, objs_num_needed, objects_need_match, pattern_components_need_match):
        """
        检查每一个输入对象与pattern中对应的对象类型（父对象）是否相符
        :param objs_num_needed:
        :param objects_need_match:
        :param pattern_components_need_match:
        :return:
        """
        if len(objects_need_match) != len(pattern_components_need_match):
            raise Exception("输入对象与pattern中需要对应的对象数量不相符！")
        total_matched = 0
        matched_or_need_parents = []
        for i in range(objs_num_needed):
            object_need_match = objects_need_match[i]
            pattern_component_need_match = pattern_components_need_match[i]
            # 检查父对象的匹配情况
            cur_parent_matched, pattern_component_need_match_parent = self._check_parent_match(
                pattern_component_need_match,
                object_need_match)
            if cur_parent_matched:  # 这里是匹配上了，应该只有一个父对象
                total_matched += 1
                matched_or_need_parents.append(pattern_component_need_match_parent)
            else:  # 这里是没匹配上，应该有多个父对象
                if pattern_component_need_match_parent and \
                        (isinstance(pattern_component_need_match_parent, list) or
                         isinstance(pattern_component_need_match_parent, tuple)):
                    matched_or_need_parents.extend(pattern_component_need_match_parent)

        if total_matched == objs_num_needed:
            return True, matched_or_need_parents
        return False, matched_or_need_parents

    def _check_parent_match(self, pattern_component_need_match, object_need_match):
        """
        检查要验证的对象与占位符父对象的匹配情况
        :param pattern_component_need_match:
        :param object_need_match:
        :return:
        """

        # 0、判断是否是实际对象-占位符
        if not (isinstance(pattern_component_need_match,
                           RealObject) and pattern_component_need_match.isPlaceHolder()):
            raise Exception("需要匹配的模式（pattern）对象不是实际对象-占位符！")

        # 1、取得模式（pattern）中占位符的父对象
        pattern_component_need_match_parents, related_ks = pattern_component_need_match.Constitutions.getSelfParentObjects()

        # 2、没有要求匹配的父对象，肯定是全都能够匹配了，返回True
        if not pattern_component_need_match_parents:
            return True, None

        # 3、如果实际对象本身就是动作，无需验证
        # 与动作A相连的不应该是动作B（无论前后），除非B与前后的对象组成新的对象
        if isinstance(object_need_match, RealObject):
            if object_need_match.isExecutable():
                return False, pattern_component_need_match_parents

            # 4、如果要验证的对象本身未定义父对象（新建的本就没有），直接返回True
            object_need_match_parents, related_ks = object_need_match.Constitutions.getSelfParentObjects()

            # 不知道当前对象的父对象，无需进一步验证
            if not object_need_match_parents:
                # 占位符父对象要求是知识链，返回False
                if Instincts.instinct_original_knowledge in pattern_component_need_match_parents:
                    return False, pattern_component_need_match_parents
                else:  # 占位符父对象不要求是知识链，返回True
                    return True, pattern_component_need_match_parents

        # 真正开始验证父对象的匹配情况
        # todo pattern父对象的匹配应该是一个更复杂的过程（不断抽象父对象）：
        # 例如：牛有腿 意义为 牛组件腿 应该抽象出{0}-父对象-牛
        # 马有腿 意义为 马组件腿 应该抽象出{0}-父对象-马
        # 然后，发现牛、马比较接近，抽象出牛-父对象-{1}、马-父对象-{1}
        # 最后 替换成{0}-父对象-{1}
        for pattern_component_need_match_parent in pattern_component_need_match_parents:

            # 0、如果是元知识链，特殊处理
            if pattern_component_need_match_parent.isSame(
                    Instincts.instinct_original_knowledge) or \
                    pattern_component_need_match_parent.Constitutions.isChild(
                        Instincts.instinct_original_knowledge):

                if isinstance(object_need_match, Knowledge):
                    return True, pattern_component_need_match_parent  # 不需要一一验证
                elif isinstance(object_need_match, list) or \
                        isinstance(object_need_match, tuple):
                    return True, pattern_component_need_match_parent  # 不需要一一验证
                elif isinstance(object_need_match, UnderstoodFragment):
                    return True, pattern_component_need_match_parent  # 不需要一一验证

            # 1、如果是元对象，特殊处理
            elif pattern_component_need_match_parent.isSame(
                    Instincts.instinct_original_object) or \
                    pattern_component_need_match_parent.Constitutions.isChild(
                        Instincts.instinct_original_object):
                # 这里需要一个实际对象
                if isinstance(object_need_match, RealObject):
                    # 如果要验证的对象本身未定义父对象（新建的本就没有），直接返回True
                    object_need_match_parents, related_ks = object_need_match.Constitutions.getSelfParentObjects()

                    if not object_need_match_parents:  # 不知道当前对象的父对象，没法验证
                        return True, pattern_component_need_match_parent  # 不需要一一验证

                    elif object_need_match.Constitutions.isChild(
                            pattern_component_need_match_parent):
                        return True, pattern_component_need_match_parent  # 不需要一一验证

            # 2、如果是元集合，特殊处理
            elif pattern_component_need_match_parent.isSame(
                    Instincts.instinct_original_collection) or \
                    pattern_component_need_match_parent.Constitutions.isChild(
                        Instincts.instinct_original_collection):
                if isinstance(object_need_match, RealObject):
                    # 如果要验证的对象本身未定义父对象（新建的本就没有），直接返回True
                    object_need_match_parents, related_ks = object_need_match.Constitutions.getSelfParentObjects()

                    if not object_need_match_parents:  # 不知道当前对象的父对象，没法验证
                        return True, pattern_component_need_match_parent  # 不需要一一验证

                    elif object_need_match.Constitutions.isChild(
                            pattern_component_need_match_parent):
                        return True, pattern_component_need_match_parent  # 不需要一一验证

            else:  # 只能为实际对象，判断是否是父对象相符合
                if isinstance(object_need_match, RealObject):
                    if object_need_match.Constitutions.isChild(
                            pattern_component_need_match_parent):
                        return True, pattern_component_need_match_parent  # 不需要一一验证

            # 没有能够匹配的，返回False
            return False, pattern_component_need_match_parents

    def _do_fragment_context_satisfied(self, realLevelResult, frag):
        """
        处理上下文数量均能满足模式的情况，查找数据库（对应的知识链及其意义），如果没找到，进行迁移（理解）
        :param reals:
        :param cur_real:
        :param exe_pattern:
        :param exe_meaning:
        :param exe_pos_in_pattern:
        :param aboves_num_needed:
        :param nexts_num_needed:
        :param frag_start_pos_in_reals:
        :param frag_end_pos_in_reals:
        :param cur_pos:
        :return:
        """
        # 根据位置、需要数量等信息将需要的realobject从reals中拆出来
        # （如果是Realobject、Knowledge不处理，如果是UnderstoodFragment，生成knowledge）
        frag_real_chain = frag.getFragmentedReals(memory=self.Mind.Memory)
        if not frag_real_chain:
            return

        # 首先应该查找知识库
        frag_unproceed = []
        frag_klg = Knowledge.getByObjectChain(frag_real_chain,
                                              unproceed=frag_unproceed,
                                              memory=self.Mind.Memory)
        # 查看是否是全链匹配（有可能是部分匹配）
        if frag_klg and not frag_unproceed:  # 如果在数据库中查找到实际对象链对应的知识链，继续查找其意义，如果没有，试图理解
            self._do_fragment_matched_knowledge_and_meaning(frag, frag_klg)

        else:  # 如果在数据库中查找不到实际对象链对应的知识链，直接试图理解
            self._do_fragment_unmatched_knowledge_and_meaning(frag)

    def _get_real_chain_from_related_real_chain(self, related_real_chain):
        """
        将realobject从relatedobject中拆出来
        :param related_real_chain:
        :return:
        """

        real_chain = []  # [lambda x: x.obj for x in matched_relatedreal_chain]
        for related_real in related_real_chain:
            if isinstance(related_real, RelatedObj):
                real_chain.append(related_real.obj)
            elif isinstance(related_real, list) or isinstance(related_real, tuple):
                child_real_chain = self._get_real_chain_from_related_real_chain(related_real)
                real_chain.append(child_real_chain)

        return real_chain

    def _get_matched_real_chain(self, reals, cur_real, exe_pos, aboves_num_needed, nexts_num_needed):
        """
        根据位置、需要数量等信息将需要的realobject从reals中拆出来（如果是Knowledge不处理，如果是UnderstoodFragment，生成knowledge）
        :param reals:
        :param cur_real:
        :param exe_pos:
        :param aboves_num_needed:
        :param nexts_num_needed:
        :return:
        """
        cur_aboves = reals[exe_pos - aboves_num_needed:exe_pos]  # 截取上文所需对象
        cur_nexts = reals[exe_pos + 1:exe_pos + 1 + nexts_num_needed]  # 截取下文所需对象
        matched_real_chain = []  # 拼接成list
        matched_real_chain.extend(cur_aboves)
        matched_real_chain.append(cur_real)
        matched_real_chain.extend(cur_nexts)

        final_matched_real_chain = []
        for matched_real in matched_real_chain:
            if isinstance(matched_real, UnderstoodFragment):
                klg = matched_real.getFragmentedRealsKnowledge(memory=self.Mind.Memory)
                if klg:
                    final_matched_real_chain.append(klg)
            else:  # 这里可能是realobject或Knowledge
                final_matched_real_chain.append(matched_real)

        return final_matched_real_chain

        # # 将realobject从relatedobject中拆出来
        # return self._get_real_chain_from_related_real_chain(matched_real_chain)

    def _do_fragment_matched_knowledge_and_meaning(self, base_frag, frag_klg):
        """
        如果在数据库中查找到实际对象链（片段）对应的知识链，继续查找其意义，如果没有，试图理解
        :param base_frag:
        :param frag_klg:
        :return:
        """
        base_frag._frag_klg = frag_klg
        # 设置执行信息
        base_frag.realLevelResult.realLevelThinkingRecords.setRealLevelMatchRecord(
            ThinkingInfo.RealLevelInfo.MatchInfo.FRAGMENT_KNOWLEDGE_MATCHED, base_frag)

        klg_meanings = frag_klg.Meanings.getAllMeanings()  # 取得当前知识链在数据库中的意义
        if klg_meanings:
            # 将取得的结果记录到thinkResult
            base_frag._frag_klg_meanings = klg_meanings

            # 这里已经是处理结果（或是一部分）了，记录之
            cur_understoodFragment = UnderstoodFragment.createByBaseFragment(base_frag, klg_meanings)

            # 设置匹配信息
            cur_understoodFragment.realLevelResult.realLevelThinkingRecords.setRealLevelMatchRecord(
                ThinkingInfo.RealLevelInfo.MatchInfo.FRAGMENT_KNOWLEDGE_MEANING_MATCHED, cur_understoodFragment)

            # 设置理解信息
            cur_understoodFragment.realLevelResult.realLevelThinkingRecords.setRealLevelUnderstoodRecord(
                ThinkingInfo.RealLevelInfo.UnderstoodInfo.FRAGMENT_MEANING_MATCHED_UNDERSTOOD, cur_understoodFragment)

            # 记录到thinkResult
            # 函数内会设置其执行状态，理解状态根据迁移结果判定
            cur_understoodFragment.realLevelResult.understoodFragments.append(cur_understoodFragment)

        else:  # 如果当前知识链在数据库中没有意义，试图理解
            # 设置匹配信息
            base_frag.realLevelResult.realLevelThinkingRecords.setRealLevelMatchRecord(
                ThinkingInfo.RealLevelInfo.MatchInfo.FRAGMENT_KNOWLEDGE_MEANING_UNMATCHED, base_frag)
            # 试着理解
            self._get_understoodFragment(base_frag)

    def _do_fragment_unmatched_knowledge_and_meaning(self, base_frag):
        """
        如果在数据库中查找不到实际对象链对应的知识链，试图理解
        :param realLevelResult:
        :param matched_real_chain:
        :param exe_pattern:
        :param exe_meaning:
        :param frag_start_pos_in_reals:
        :param frag_end_pos_in_reals:
        :param cur_pos:
        :return:
        """
        # 设置匹配信息
        base_frag.realLevelResult.realLevelThinkingRecords.setRealLevelMatchRecord(
            ThinkingInfo.RealLevelInfo.MatchInfo.FRAGMENT_KNOWLEDGE_UNMATCHED, base_frag)

        self._get_understoodFragment(base_frag)

    def _get_understoodFragment(self, base_frag):
        """
        试图理解（两种情况：1、查找到知识链，但在数据库中没有意义；2、查找不到知识链）
        :param matched_real_chain:
        :param exe_pattern:
        :param exe_meaning:
        :param reals:
        :param frag_start_pos_in_reals:
        :param frag_end_pos_in_reals:
        :param cur_pos:
        :return:
        """
        # 设置执行信息
        base_frag.realLevelResult.realLevelThinkingRecords.setRealLevelExecuteRecord(
            ThinkingInfo.RealLevelInfo.ExecuteInfo.Understanding_Fragment, base_frag)

        transited_meaning = self.Mind.thinkingCentral.TransitionEngine.transitByAction(
            base_frag.getFragmentedReals(), base_frag.exe_pattern, base_frag.exe_meaning, base_frag.exe_meaning_value)

        cur_understoodFragment = None

        if transited_meaning:
            # 这里已经是处理结果（或是一部分）了，记录之
            cur_understoodFragment = UnderstoodFragment.createByBaseFragment(base_frag, transited_meaning)
            # 记录到thinkResult
            # 函数内会设置其执行状态，理解状态根据迁移结果判定
            base_frag.realLevelResult.understoodFragments.append(cur_understoodFragment)
            if isinstance(transited_meaning, Meaning):
                pass
            elif isinstance(transited_meaning, SelfExplainSelfMeaning):  # 自解释意义
                # 记录理解状态（自解释）
                base_frag.realLevelResult.realLevelThinkingRecords.setRealLevelUnderstoodRecord(
                    ThinkingInfo.RealLevelInfo.UnderstoodInfo.SELF_EXPLAIN_SELF, transited_meaning)
            elif isinstance(transited_meaning, ExecutionInfoCreatedMeaning):  # 建立意义。根据意义标记，建立了左右两侧对象的意义关联
                # 记录理解状态（意义建立或已存在）
                if transited_meaning.newCreated:
                    base_frag.realLevelResult.realLevelThinkingRecords.setRealLevelUnderstoodRecord(
                        ThinkingInfo.RealLevelInfo.UnderstoodInfo.EXECUTIONINFO_CREATED, transited_meaning)
                else:
                    base_frag.realLevelResult.realLevelThinkingRecords.setRealLevelUnderstoodRecord(
                        ThinkingInfo.RealLevelInfo.UnderstoodInfo.EXECUTIONINFO_EXIST, transited_meaning)
            elif isinstance(transited_meaning,
                            ExecutionInfoCreatedMeanings):  # 建立多个动词的意义[因为...所以...]。根据意义标记，建立了左右两侧对象的意义关联
                for _transited_meaning in transited_meaning:
                    # 记录理解状态（意义建立或已存在）
                    if _transited_meaning.newCreated:
                        base_frag.realLevelResult.realLevelThinkingRecords.setRealLevelUnderstoodRecord(
                            ThinkingInfo.RealLevelInfo.UnderstoodInfo.EXECUTIONINFOS_CREATED, transited_meaning)
                        break
                    else:
                        base_frag.realLevelResult.realLevelThinkingRecords.setRealLevelUnderstoodRecord(
                            ThinkingInfo.RealLevelInfo.UnderstoodInfo.EXECUTIONINFOS_EXIST, transited_meaning)
                        break

        else:
            # 记录到thinkResult，这里为None（没有迁移结果）
            # 函数内会设置其执行状态，理解状态根据迁移结果判定
            base_frag.realLevelResult.understoodFragments.append(cur_understoodFragment)

        return cur_understoodFragment

    def _do_fragment_context_unsatisfied(self, realLevelResult,
                                         frag, context_satisfaction_result,
                                         unsatisfied_poses):
        """
        处理上下文有一方或两方数量不能满足模式的情况。对上下文要求的父对象是元知识链、元集合进行重新思考；或记录到UnsatisfiedFragment，查找上文或等待下文。
        :param realLevelResult:
        :param frag_start_pos_in_reals:
        :param frag_end_pos_in_reals:
        :param cur_exe_pos:
        :param exe_pattern:
        :param exe_meaning:
        :param unsatisfied_poses:
        :return:
        :remarks:
        1、对上下文要求的父对象是元知识链、元集合进行重新思考，如果得到思考结果，直接返回
        2、如果没得到重新思考的结果，这是真正的上下文不满足了，记录到UnsatisfiedFragment，查找上文或等待下文。
        """
        # 目前放在_regenerateRealLevelResults中进行处理
        # # 0、查看是否是位置（数量）要求的不满足
        # # 如果是要求的片段起始位置、结束位置超过了reals的范围，相当于怎么都不满足，这是真正的上下文不满足
        # # 例如：牛-组件，按组件的要求，应该有下文，但在输入中这个位置，已经超出了reals的范围，这就是位置（数量）要求的不满足
        # if frag_start_pos_in_reals >= 0 and frag_end_pos_in_reals < len(realLevelResult.reals):
        #     # 1、如果是位置（数量）要求的满足
        #     # 对上下文要求的父对象是元知识链、元集合进行重新思考，如果得到思考结果，直接返回
        #     if self._rethink_context_unsatisfied_by_originals(realLevelResult, context_satisfaction_result,
        #                                                       cur_exe_pos):
        #         return
        # 2、如果没得到重新思考的结果，这是真正的上下文不满足了
        cur_unsatisfiedFragment = UnsatisfiedFragment.createByBaseFragment(frag,
                                                                           unsatisfied_poses,
                                                                           context_satisfaction_result)
        # 记录到thinkResult
        # 函数内会设置其执行状态，理解状态
        realLevelResult.unsatisfiedFragments.append(cur_unsatisfiedFragment)

    #
    # def thinkAsWhole(self, reals):
    #     """
    #     将所有输入作为一个整体进行思考（首先思考匹配模式的小部分，逐渐往上一层返，最后匹配全部）
    #     :param reals:
    #     :return:
    #     """
    #     if self.isSimpliestReals(reals):
    #         grouped_reals_list = self.thinkSimpliestRealChain(reals)
    #
    #     else:
    #         pass
    #
    #     for grouped_reals in self.Mind.thinkingCentral.GroupEngine.groupRealChain(reals):
    #
    #         if self.isMeaningParadigm(grouped_reals):
    #             self.do_meaning_modeling(grouped_reals)
    #             continue
    #
    #         # if self.isSimpliestReals(grouped_reals):  # 是否是实际对象列表，分组后只应有一个action
    #         #     cur_action = execute_sequence.get(0)
    #         #     if not isinstance(cur_action, RealObject):
    #         #         raise Exception("当前提供的对象非实际对象！")
    #         #     # 取得模式
    #         #     pattern_knowledge, meaning_knowledges = cur_action.getSelfExecutionInfo()
    #         #     if not pattern_knowledge or not meaning_knowledges:
    #         #         raise Exception("当前提供的对象非可执行的实际对象！")
    #         #
    #         #     transit_result = self.Mind.thinkingCentral.TransitionEngine.transit(grouped_reals, pattern_knowledge,
    #         #                                                                         meaning_knowledges)
    #         #     if transit_result:
    #         #         return transit_result
    #         #     pass
    #
    #     # return knowledge,unknown_objs
    # #
    # def thinkSimpliestRealChain(self, reals):
    #     """
    #     按照Action的范式及优先级，对实际对象的序列进行分组（产生式，例如：我知道中国人民解放军是最棒的，小明用手拿起瓶子）
    #     :param reals:实际对象（realtedObj）的序列（可能嵌套）
    #     :remark: 我知道中国人民解放军是最棒的 分组结果：[我,知道,[中国人民解放军,是,最棒的]，[[我,知道,中国人民解放军],是,最棒的]...
    #               小明用手拿起瓶子 分组结果：[小明,[[用,手],[拿,起]],瓶子],[小明,[用,[手拿,起]],瓶子]...
    #               牛有腿意义为牛组件为腿 分组结果：[[牛,有,腿],意义为,[牛,组件为,腿]],[牛,有,[腿,意义为,[牛组件为腿]]...
    #     :return:
    #     """
    #     # 方法：
    #     # 1、查找到所有动作
    #     # 2、对动作按优先级排序
    #     # 3、查看是否符合动作的pattern
    #     # 4、按符合的进行分组
    #
    #     # 1、取得所有的可执行性对象，并排序（根据executables的权重重新计算执行的顺序）
    #     pos_executables = self.getExecutables(reals)
    #
    #     possible_fragments = self.thinkByPosExecutable(reals, pos_executables)

    # def getExecutables(self, reals):
    #     """
    #     递归取得实际对象链中所有的可执行性对象
    #     :param reals: 实际对象链
    #     :return: pos_executables:{pos:(real,weight)/{pos:(real,weight)}} {位置:(实际对象,权重)或pos_executables(代表着嵌套)}
    #     """
    #     # 首先取得所有的可执行性对象
    #     pos_executables = []
    #     # pos_sub_pos_executables
    #     pos = 0
    #     for real in reals:
    #         if isinstance(real, RelatedObj):
    #             if real.obj.isExecutable():  # 判断当前实际对象是否是可执行性对象
    #                 real.obj.getSelfExecutionInfo()  # 取得执行信息
    #                 pos_executables.append((pos, real))
    #         pos += 1
    #
    #     if pos_executables:
    #         # 根据(pos, real, weight)的weight/pos进行排序
    #         # todo 目前的公式为：weight/pos
    #         # 为了使用权重/位置进行排序，避免除零，所以位置加1
    #         pos_executables.sort(key=lambda x: x[1].obj.weight / float(x[0]) + 1)  # , reverse=True)
    #
    #     return pos_executables
    #
    # def thinkByPosExecutable(self, reals, pos_executables):
    #
    #     for pos, executable in pos_executables:
    #         executable = executable.obj
    #         executable.getSelfExecutionInfo()  # 取得执行信息
    #         for id, pattern in executable.ExecutionInfo.LinearExecutionInfo.pattern_knowledges.items():
    #             pattern_klg = pattern.obj
    #             meaning_klgs = executable.ExecutionInfo.LinearExecutionInfo.meaning_knowledges[pattern.id]
    #             if not meaning_klgs:
    #                 raise Exception("查找不到pattern的meaning！")
    #
    #             pattern_components = pattern_klg.getSequenceComponents()
    #             exe_pos_in_pattern = pattern_components.index(executable)
    #             if not exe_pos_in_pattern:
    #                 raise Exception("当前可执行实际对象不在其定义的pattern之中！pattern定义错误！")
    #
    #             matched_real_chains = []
    #             placeholder_pos_in_pattern = 0
    #             for pattern_component in pattern_components:
    #                 if pattern_component.isPlaceHolder():
    #                     placeholder_parents, parents_ks = pattern_component.Constitutions.getSelfParentObjects()
    #                     for placeholder_parent in placeholder_parents:
    #                         # 根据动作在实际对象列表、模式中所在的位置，模式中占位符的位置，取得占位符对应的实际对象。
    #                         placed_real = self.getRealByPosExecutable(reals, pos, exe_pos_in_pattern,
    #                                                                   placeholder_pos_in_pattern)
    #                         if placed_real:
    #                             if placed_real.obj.Constitutions.isChild(placeholder_parent):
    #                                 matched_real_chains.append([placed_real.obj])
    #                                 break
    #                         else:
    #                             raise Exception("无法取得placeholder对应的实际对象，pattern定义错误！")
    #                 else:
    #                     matched_real_chains.append([pattern_component])
    #                 placeholder_pos_in_pattern += 1
    #
    #             if matched_real_chains:
    #                 for matched_real_chain in itertools.product(*matched_real_chains):
    #                     for id, meaning_klg in meaning_klgs.items():
    #                         transit_result = self.Mind.thinkingCentral.TransitionEngine.transitByAction(
    #                             matched_real_chain, pattern_klg, meaning_klg.obj)
    #                         # 这里已经是处理结果（或是一部分）了
    #                         self.Mind.thinkingCentral.Brain.logThinkResult(transit_result)
    #
    #     pass
    #
    # def getRealByPosExecutable(self, reals, exe_pos_in_reals, exe_pos_in_pattern, placeholder_pos_in_pattern):
    #     """
    #     根据动作在实际对象列表、模式中所在的位置，模式中占位符的位置，取得占位符对应的实际对象。
    #     :param reals:
    #     :param exe_pos_in_reals:
    #     :param exe_pos_in_pattern:
    #     :param placeholder_pos_in_pattern:
    #     :return:
    #     """
    #     distance = placeholder_pos_in_pattern - exe_pos_in_pattern
    #     if distance == 0:
    #         raise Exception("占位符不能是可执行性实际对象（动作）！")
    #     index = exe_pos_in_reals + distance
    #     if index < 0 or index > len(reals):
    #         raise Exception("最终位置不能超出实际对象列表的范围：0-%d，当前位置：%d" % (len(reals), index))
    #
    #     return reals[index]
    # #
    # def isMeaningParadigm(self, grouped_reals):
    #     pass

    def _processRealLevelResult(self, realLevelResult, forceToRethink=False,
                                misunderstoodRethinkDepth=Character.Misunderstood_Rethink_Depth):
        """
        [核心代码]对实际对象级别的结果进行进一步处理。
        :param realLevelResult:
        :param forceToRethink: 是否强制重新思考（在匹配的意义可能不对的情况下）
        :return:
        :remarks:
        1、处理碎片，将其连接，进一步进行理解处理
        2、处理未满足条件的句式（本次输入的实际对象链中的上下文，本次输入的上下文）
        3、处理未知对象
        """
        if not realLevelResult:
            return
        # 记录其执行信息
        realLevelResult.realLevelThinkingRecords.setRealLevelExecuteRecord(
            ThinkingInfo.RealLevelInfo.ExecuteInfo.Processing_RealLevelResult, realLevelResult)

        if realLevelResult.isSingle():  # 1、唯一一个实际对象，特殊处理
            # 对实际对象级别的结果（单个实际对象）进行进一步处理
            return self._processRealLevelResult_Single(realLevelResult)

        else:  # 2、多个对象
            # 对实际对象级别的结果（多实际对象）进行进一步处理。
            return self._processRealLevelResult_Reals(realLevelResult, forceToRethink, misunderstoodRethinkDepth)

    def _processRealLevelResult_Single(self, realLevelResult):
        """
        [核心代码]对实际对象级别的结果（单个实际对象）进行进一步处理
        :param realLevelResult:
        :return:
        """
        # 1.0、这里肯定没有理解信息
        # 1.1、查看未知对象
        if realLevelResult.hasUnknowns():  # 只有一个，还未知，直接设置理解信息为SINGLE_MISUNDERSTOOD
            # 设置理解信息
            realLevelResult.realLevelThinkingRecords.setRealLevelUnderstoodRecord(
                ThinkingInfo.RealLevelInfo.UnderstoodInfo.SINGLE_MISUNDERSTOOD, realLevelResult.reals[0])
        else:
            # 1.2、查看pattern匹配信息
            if realLevelResult.hasUnsatisfiedFragments():  # 如果有未满足pattern的，设
                # 设置理解信息为SINGLE_UNDERSTOOD_NEED_CONTEXTS（这是个单一对象，所以后续会进行联想、等待上下文等处理）
                realLevelResult.realLevelThinkingRecords.setRealLevelUnderstoodRecord(
                    ThinkingInfo.RealLevelInfo.UnderstoodInfo.SINGLE_UNDERSTOOD_NEED_CONTEXTS,
                    realLevelResult.reals[0])
            else:
                # 设置理解信息（直接就理解了（相当于什么也没做），这是个单一对象，所以后续会进行联想等处理）
                realLevelResult.realLevelThinkingRecords.setRealLevelUnderstoodRecord(
                    ThinkingInfo.RealLevelInfo.UnderstoodInfo.SINGLE_UNDERSTOOD, realLevelResult.reals[0])

    def _processRealLevelResult_Reals(self, realLevelResult, forceToRethink=False,
                                      misunderstoodRethinkDepth=Character.Misunderstood_Rethink_Depth):
        """
        [最核心代码]对实际对象级别的结果（多实际对象）进行进一步处理。
        :param realLevelResult:
        :param forceToRethink: 是否强制重新思考（在匹配的意义可能不对的情况下）
        :return:
        :remarks:
        1、处理碎片，将其连接，进一步进行理解处理
        2、处理未满足条件的句式（本次输入的实际对象链中的上下文，本次输入的上下文）
        3、处理未知对象
        """
        # 0、查看是否通过实际对象链找到了知识链及其意义，如果已经有意义了，并且不是强制是重新思考，直接返回
        if realLevelResult.hasMatchedMeaning() and not forceToRethink:
            return
        # 1、没有直接匹配的知识链及其意义，对上面的处理结果进行分析
        if realLevelResult.hasUnderstoodFragments():  # 1.1如果有已经理解的片段

            # 对已经理解的片段进行排列组合
            allUnderstoodJoinedFrags, partitalUnderstoodJoinedFrags = realLevelResult.analysisUnderstoodFragments()

            if allUnderstoodJoinedFrags:  # 如果有全部理解的，不用考虑是否存在冲突、未知、未满足
                # 根据理解片段生成意义知识链
                understood_meaning_klg_dict = realLevelResult.createMeaningsByUnderstoodFragments()
                # 记录理解信息（忽略自解释及意义创建的知识链和元数据网）
                record_meta, record_real, record_knowledge, record_metanet = True, True, False, False

                if understood_meaning_klg_dict and \
                        not realLevelResult.isSelfExplainSelf() and \
                        not realLevelResult.isExecutionInfoCreated():
                    # 处理结果中的Anything
                    anything_matched_klgs = self._processKnowledgeDictAnything(realLevelResult,
                                                                               understood_meaning_klg_dict)

                    if not anything_matched_klgs:
                        # 如果是女娲超级管理账户，record_knowledge=True
                        if self.Mind.isUsedByAdminUser():
                            record_knowledge, record_metanet = True, True
                        realLevelResult.realLevelThinkingRecords.setRealLevelUnderstoodRecord(
                            ThinkingInfo.RealLevelInfo.UnderstoodInfo.ALL_REALS_UNDERSTOOD,
                            understood_meaning_klg_dict)

                    else:
                        realLevelResult.realLevelThinkingRecords.setRealLevelUnderstoodRecord(
                            ThinkingInfo.RealLevelInfo.UnderstoodInfo.ALL_REALS_UNDERSTOOD,
                            understood_meaning_klg_dict)
                        realLevelResult.realLevelThinkingRecords.setRealLevelUnderstoodRecord(
                            ThinkingInfo.RealLevelInfo.UnderstoodInfo.ALL_REALS_UNDERSTOOD_ANYTHING_MATCHED,
                            anything_matched_klgs)

                # 已经理解这句话，对其中的元数据、实际数据、知识链进行处理（记录到数据库、从未知对象中移除等）
                for allUnderstoodJoinedFrag in allUnderstoodJoinedFrags:
                    self.Mind.recordAllUnderstoodJoinedFragments(allUnderstoodJoinedFrag, record_meta,
                                                                 record_metanet, record_real, record_knowledge)


            elif partitalUnderstoodJoinedFrags and misunderstoodRethinkDepth >= 0:
                # todo 这里还有一种情况：取得的partitalUnderstoodJoinedFrag都是单个的，而且可能位于冲突的列表中，这时不需要生成
                # 根据已经理解的片段生成新的realChain（可能有多个）
                regenerated_real_level_results = self._regenerateRealLevelResultsByUnderstoodFrags(realLevelResult,
                                                                                                   partitalUnderstoodJoinedFrags)
                # todo 目前是笛卡尔全排序，后续应该压入队列，并可以随时停止后续，并在反馈不对的时候启动后续继续理解
                if regenerated_real_level_results:
                    error_indexes = []  # 发生错误的regeneratedRealLevelResult索引
                    i = 0
                    for regenerated_real_level_result in regenerated_real_level_results:
                        # 递归进行理解
                        try:
                            self._tryUnderstand(regenerated_real_level_result, misunderstoodRethinkDepth - 1)
                            # 如果已经全理解了，直接停止
                            if regenerated_real_level_result.isAllUnderstood():
                                break
                        except Exception as ex:  # 这里由于上下文查找的结果，可能会产生错误，忽略之
                            error_indexes.append(i)
                            logger.debug("根据已经理解的片段生成新的realChain理解错误！%s" % ex)
                        i += 1

                    # todo 这里应该将其他未处理的暂停挂起 ，等待用户反馈
                    if error_indexes:  # 如果有错误的，将其抛弃
                        from loongtian.nvwa.runtime.thinkResult.realLevelResult import \
                            RegeneratedRealLevelResults
                        final_regenerated_real_level_results = RegeneratedRealLevelResults(realLevelResult)
                        for i in range(len(regenerated_real_level_results)):
                            if i in error_indexes:
                                continue
                            final_regenerated_real_level_results.append(regenerated_real_level_results[i])
                        realLevelResult.regeneratedRealLevelResults = final_regenerated_real_level_results

                else:
                    # 考虑冲突、未知、未满足、动词交联等部分导致的未能理解
                    self._processMisunderstoodPartitions(realLevelResult)
            else:
                # 考虑冲突、未知、未满足、动词交联等部分导致的未能理解
                self._processMisunderstoodPartitions(realLevelResult)  # #

        else:
            # 考虑冲突、未知、未满足、动词交联等部分导致的未能理解
            self._processMisunderstoodPartitions(realLevelResult)

    def _regenerateRealLevelResultsByUnderstoodFrags(self, parent_realLevelResult, partitalJoinedUnderstoodFrags):
        """
        [核心代码]根据已经理解的片段生成新的realChain（可能有多个）
        :return:
        """

        for joinedUnderstoodFrags in partitalJoinedUnderstoodFrags:
            regenerated_reals = []  # 将理解片段与其他实际对象拼接在一起的列表

            cur_start_pos = 0
            for cur_understood_fragment in joinedUnderstoodFrags.understood_fragment_list:
                if cur_understood_fragment.frag_start_pos_in_reals > cur_start_pos:  # 查看前面是否还有实际对象
                    regenerated_reals.extend(
                        parent_realLevelResult.reals[cur_start_pos:cur_understood_fragment.frag_start_pos_in_reals])
                regenerated_reals.append(cur_understood_fragment)
                cur_start_pos = cur_understood_fragment.frag_end_pos_in_reals + 1
            # 最后一个理解片段可能还有后面的实际对象，加上
            last_understood_fragment = joinedUnderstoodFrags.understood_fragment_list[-1]
            if last_understood_fragment.frag_end_pos_in_reals < len(parent_realLevelResult.reals) - 1:
                regenerated_reals.extend(
                    parent_realLevelResult.reals[last_understood_fragment.frag_end_pos_in_reals + 1:])

            if regenerated_reals:
                pos_executables = self.getExecutables(regenerated_reals, sort=False)
                if not pos_executables:
                    # 创建一个新的重构的实际对象链的思考结果，并添加到regeneratedRealLevelResults列表中。
                    parent_realLevelResult.regeneratedRealLevelResults.createNewRegeneratedRealLevelResult(
                        regenerated_reals)
                else:
                    for exe_pos, cur_exe in pos_executables:
                        # 对上下文要求的父对象是元知识链、元集合进行重新聚合，并根据聚合结果创建新的重构的实际对象链的思考结果
                        # 使用模板函数操作_inner_function_create_regenerated_realLevelResult
                        self.ProcessExeWithInnerFunction(cur_exe, exe_pos, regenerated_reals,
                                                         self._inner_function_combine_context_and_create_regenerated_realLevelResult,
                                                         parent_realLevelResult, regenerated_reals
                                                         )

        return parent_realLevelResult.regeneratedRealLevelResults

    def _inner_function_combine_context_and_create_regenerated_realLevelResult(self, exe_pattern_check_result,
                                                                               parent_realLevelResult,
                                                                               regenerated_reals):
        """
        （内部函数）对上下文要求的父对象是元知识链、元集合进行重新聚合，并根据聚合结果创建新的重构的实际对象链的思考结果
        :param exe_pattern_check_result:
        :param parent_realLevelResult:
        :param regenerated_reals:
        :return:
        """

        if not exe_pattern_check_result or not isinstance(exe_pattern_check_result, RealArea.ExePatternCheckResult):
            raise Exception("参数错误：exe_pattern_check_result，必须是RealArea._ExePatternCheckResult类型！")

        # 分项取得上下文的检查结果（context_satisfaction_result是一个tuple）
        aboves_satisfied, nexts_satisfied, aboves_matched_or_need_parents, \
        nexts_matched_or_need_parents = exe_pattern_check_result.context_satisfaction_result

        # 对上下文要求的父对象是元知识链、元集合进行重新聚合
        combine_context_reals_list = []

        if aboves_satisfied and nexts_satisfied:  # 如果上、下文都能满足，直接将现有regenerated_reals赋值给combine_context_reals_list
            combine_context_reals_list.append(regenerated_reals)
        else:
            _regenerated_above_objs_list = []
            _regenerated_next_objs_list = []

            # 如果上文不能满足，对可执行对象的所有上文进行聚合（判断其父对象要求是否是knowledge、collection等，然后聚合）
            if not aboves_satisfied:
                if aboves_matched_or_need_parents:
                    # 取得可能的上下文，如果有已经理解的片段覆盖的部分，将其打包处理
                    possible_aboves_list = self._get_possible_aboves(parent_realLevelResult, regenerated_reals,
                                                                     exe_pattern_check_result.exe_pos)
                    if possible_aboves_list:
                        for aboves_need_parent in aboves_matched_or_need_parents:
                            if aboves_need_parent.isSame(Instincts.instinct_original_knowledge) or \
                                    aboves_need_parent.Constitutions.isChild(Instincts.instinct_original_knowledge):
                                for possible_aboves, poses in possible_aboves_list:

                                    _cur_regenerated_above_objs = []
                                    # 创建knowledge，然后替换原来的上文
                                    _cur_regenerated_above_obj = Knowledge.createKnowledgeByObjChain(
                                        self._processObjsToNvwaObjs(possible_aboves),
                                        memory=self.Mind.Memory)
                                    if _cur_regenerated_above_obj:
                                        _cur_regenerated_above_objs.append(_cur_regenerated_above_obj)

                                        # 可能还有一些在前面的未包含进来
                                        missed_aboves = regenerated_reals[0:poses[0]]
                                        if missed_aboves:
                                            missed_aboves.extend(_cur_regenerated_above_objs)
                                            _cur_regenerated_above_objs = missed_aboves
                                        _regenerated_above_objs_list.append(_cur_regenerated_above_objs)

                            elif aboves_need_parent.isSame(Instincts.instinct_original_collection) or \
                                    aboves_need_parent.Constitutions.isChild(Instincts.instinct_original_collection):
                                for possible_aboves, poses in possible_aboves_list:
                                    _cur_regenerated_above_objs = []
                                    # 创建collection（实际对象），然后替换原来的上文
                                    _cur_regenerated_above_obj = Collection.createRealObjectAsCollection(
                                        possible_aboves,
                                        memory=self.Mind.Memory)
                                    if _cur_regenerated_above_obj:
                                        _cur_regenerated_above_objs.append(_cur_regenerated_above_obj[0])

                                        # 可能还有一些在前面的未包含进来
                                        missed_aboves = regenerated_reals[0:poses[0]]
                                        if missed_aboves:
                                            missed_aboves.extend(_cur_regenerated_above_objs)
                                            _cur_regenerated_above_objs = missed_aboves
                                        _regenerated_above_objs_list.append(_cur_regenerated_above_objs)
            else:
                _regenerated_above_objs_list.append(regenerated_reals[0:exe_pattern_check_result.exe_pos])

            # 如果下文不能满足，对可执行对象的所有下文进行聚合
            if not nexts_satisfied:
                if nexts_matched_or_need_parents:
                    # 取得可能的上下文，如果有已经理解的片段覆盖的部分，将其打包处理
                    possible_nexts_list = self._get_possible_nexts(parent_realLevelResult, regenerated_reals,
                                                                   exe_pattern_check_result.exe_pos)
                    if possible_nexts_list:
                        for nexts_need_parent in nexts_matched_or_need_parents:
                            if nexts_need_parent.isSame(Instincts.instinct_original_knowledge) or \
                                    nexts_need_parent.Constitutions.isChild(Instincts.instinct_original_knowledge):
                                for possible_nexts, poses in possible_nexts_list:

                                    _cur_regenerated_next_objs = []
                                    # 创建knowledge，然后替换原来的上文
                                    _cur_regenerated_next_obj = Knowledge.createKnowledgeByObjChain(
                                        self._processObjsToNvwaObjs(possible_nexts),
                                        memory=self.Mind.Memory)
                                    if _cur_regenerated_next_obj:
                                        _cur_regenerated_next_objs.append(_cur_regenerated_next_obj)

                                        # 可能还有一些在前面的未包含进来
                                        missed_nexts = regenerated_reals[poses[-1] + 1:]
                                        if missed_nexts:
                                            _cur_regenerated_next_objs.extend(missed_nexts)
                                        _regenerated_next_objs_list.append(_cur_regenerated_next_objs)

                            elif nexts_need_parent.isSame(Instincts.instinct_original_collection) or \
                                    nexts_need_parent.Constitutions.isChild(Instincts.instinct_original_collection):
                                for possible_nexts, poses in possible_nexts_list:
                                    _cur_regenerated_next_objs = []
                                    # 创建collection（实际对象），然后替换原来的上文
                                    _cur_regenerated_next_obj = Collection.createRealObjectAsCollection(possible_nexts,
                                                                                                        memory=self.Mind.Memory)
                                    if _cur_regenerated_next_obj:
                                        _cur_regenerated_next_objs.append(_cur_regenerated_next_obj[0])

                                        # 可能还有一些在前面的未包含进来
                                        missed_nexts = regenerated_reals[poses[-1] + 1:]
                                        if missed_nexts:
                                            _cur_regenerated_next_objs.extend(missed_nexts)
                                        _regenerated_next_objs_list.append(_cur_regenerated_next_objs)
            else:
                _regenerated_next_objs_list.append(regenerated_reals[exe_pattern_check_result.exe_pos + 1:])

            # 重新拼合对象链
            _regenerated_objs_list = []
            _regenerated_objs_list.append(_regenerated_above_objs_list)  # 添加新生成的上文部分
            _regenerated_objs_list.append([exe_pattern_check_result.cur_exe])  # 添加动作
            _regenerated_objs_list.append(_regenerated_next_objs_list)  # 添加新生成的上文部分

            # 笛卡尔积
            # todo 这里不能挨个处理，应该按可能性排序，然后压入队列，一旦能够理解，应该可以停止
            for _regenerated_objs in itertools.product(*_regenerated_objs_list):
                combine_context_reals = []
                for _regenerated_obj in _regenerated_objs:
                    if isinstance(_regenerated_obj, list) or isinstance(_regenerated_obj, tuple):
                        combine_context_reals.extend(_regenerated_obj)
                    else:
                        combine_context_reals.append(_regenerated_obj)

                combine_context_reals_list.append(combine_context_reals)

        if combine_context_reals_list:
            for combine_context_reals in combine_context_reals_list:
                # 创建一个新的重构的实际对象链的思考结果，并添加到regeneratedRealLevelResults列表中。
                parent_realLevelResult.regeneratedRealLevelResults.createNewRegeneratedRealLevelResult(
                    combine_context_reals)

    def _processObjsToNvwaObjs(self, objs):
        """
        将传入对象（多个）转化为女娲系统对象。
        :param objs:
        :return:
        """

        nvwa_objs = []
        for obj in objs:
            if isinstance(obj, BaseEntity):
                nvwa_objs.append(obj)
                continue
            elif isinstance(obj, list):
                child_nvwa_objs = self._processObjsToNvwaObjs(obj)
                nvwa_objs.append(child_nvwa_objs)
                continue
            elif isinstance(obj, UnderstoodFragment):
                obj = obj.getFragmentedRealsKnowledge(memory=self.Mind.Memory)
                nvwa_objs.append(obj)
                continue
            else:
                raise Exception("目前不支持的类型！%s" % type(obj))

        return nvwa_objs

    def _get_possible_aboves(self, parent_realLevelResult, regenerated_reals, cur_exe_pos):
        """
        [最核心的代码]取得所有可能的上文，如果有已经理解的片段覆盖的部分，将其打包处理
        :param parent_realLevelResult:
        :param cur_exe_pos:
        :return:
        """
        _posed_possible_aboves_list = []
        i = cur_exe_pos - 2  # 前一个肯定不对，这是需要多个对象以满足上文的knowledge、collection
        while i >= 0:  # 逆推，例如：牛有腿 意义，根据意义这个可执行对象，逆推为：[有腿]、[牛有腿]
            _cur_possible_aboves = regenerated_reals[i:cur_exe_pos]
            if _cur_possible_aboves:
                if self.getExecutables(_cur_possible_aboves, sort=False):  # 到上一个动作截止
                    break
                _posed_possible_aboves_list.append(
                    (_cur_possible_aboves, range(i, cur_exe_pos)))  # (可能的对象列表,可能的位置列表)用tuple来区隔

            i -= 1

        if not _posed_possible_aboves_list:
            return

        # # 如果有已经理解的片段覆盖的部分，将其打包处理
        # _possible_aboves_matched_understood_frag_dict = {}  # {index:[understood_frag]}
        # j = 0
        # for _cur_possible_aboves, poses in _posed_possible_aboves_list:
        #     understood_frags = []
        #     for understood_frag in parent_realLevelResult.understoodFragments:
        #         if set(poses) >= set(understood_frag.getPosesInReals()):
        #             understood_frags.append(understood_frag)
        #     if understood_frags:
        #         _possible_aboves_matched_understood_frag_dict[j] = understood_frags
        #     j += 1

        _possible_aboves_list = copy.copy(_posed_possible_aboves_list)  # 复制一个
        # if _possible_aboves_matched_understood_frag_dict:  # 如果有需要用理解片段进行替换的，替换之
        #     for index, understood_frags in _possible_aboves_matched_understood_frag_dict.items():
        #         if not understood_frags:
        #             continue
        #         if len(understood_frags) == 1:
        #             understood_frags = understood_frags[0]
        #         _possible_aboves_list[index] = (understood_frags, [index])  # 替换

        # 进一步检查上下文可满足性，全未知无所谓、全理解也可以，但如有上下文不匹配的，直接抛弃之！
        _possible_aboves_index_need_remove = []
        x = 0
        for _possible_aboves, poses in _possible_aboves_list:
            if not isinstance(_possible_aboves, list) and not isinstance(_possible_aboves, tuple):
                continue
            pos_executables = self.getExecutables(_possible_aboves, sort=False)
            if not pos_executables:
                x += 1
                continue
            for exe_pos, cur_exe in pos_executables:
                # 进一步检查上下文可满足性，取得可以抛弃的上、下文
                # 使用模板函数操作_inner_function_get_possible_aboves_index_need_remove
                self.ProcessExeWithInnerFunction(cur_exe, exe_pos, _possible_aboves,
                                                 self._inner_function_get_possible_contexts_index_need_remove,
                                                 _possible_aboves_index_need_remove, x)
            x += 1

        _possible_aboves_index_need_remove = set(_possible_aboves_index_need_remove)  # 去重
        # 如有上下文不匹配的，直接抛弃
        final_possible_aboves_list = []
        y = 0
        for _possible_aboves in _possible_aboves_list:
            if y in _possible_aboves_index_need_remove:
                y += 1
                continue
            final_possible_aboves_list.append(_possible_aboves)
            y += 1

        # 倒序处理
        if final_possible_aboves_list:
            final_possible_aboves_list.reverse()
        return final_possible_aboves_list

    def _get_possible_nexts(self, parent_realLevelResult, regenerated_reals, cur_exe_pos):
        """
        [最核心的代码]取得所有可能的下文，如果有已经理解的片段覆盖的部分，将其打包处理
        :param parent_realLevelResult:
        :param cur_exe_pos:
        :return:
        """
        _posed_possible_nexts_list = []
        i = cur_exe_pos + 3  # 后一个肯定不对，这是需要多个对象以满足下文的knowledge、collection
        while i <= len(regenerated_reals):  # 正推，例如：牛有腿 意义，根据意义这个可执行对象，逆推为：[有腿]、[牛有腿]
            _cur_possible_nexts = regenerated_reals[cur_exe_pos + 1:i]
            if _cur_possible_nexts:
                if self.getExecutables(_cur_possible_nexts, sort=False):  # 到下一个动作截止
                    break
                _posed_possible_nexts_list.append(
                    (_cur_possible_nexts, range(cur_exe_pos + 1, i)))  # (可能的对象列表,可能的位置列表)用tuple来区隔

            i += 1

        if not _posed_possible_nexts_list:
            return

        # # 如果有已经理解的片段覆盖的部分，将其打包处理
        # _possible_nexts_matched_understood_frag_dict = {}  # {index:[understood_frag]}
        # j = 0
        # for _cur_possible_nexts, poses in _posed_possible_nexts_list:
        #     understood_frags = []
        #     for understood_frag in parent_realLevelResult.understoodFragments:
        #         if set(poses) >= set(understood_frag.getPosesInReals()):
        #             understood_frags.append(understood_frag)
        #     if understood_frags:
        #         _possible_nexts_matched_understood_frag_dict[j] = understood_frags
        #     j += 1
        #
        _possible_nexts_list = copy.copy(_posed_possible_nexts_list)  # 复制一个
        # if _possible_nexts_matched_understood_frag_dict:  # 如果有需要用理解片段进行替换的，替换之
        #     for index, understood_frags in _possible_nexts_matched_understood_frag_dict.items():
        #         if not understood_frags:
        #             continue
        #         if len(understood_frags) == 1:
        #             understood_frags = understood_frags[0]
        #         _possible_nexts_list[index] = (understood_frags, [index])  # 替换

        # 进一步检查上下文可满足性，全未知无所谓、全理解也可以，但如有上下文不匹配的，直接抛弃之！
        _possible_nexts_index_need_remove = []
        x = 0
        for _possible_nexts, poses in _possible_nexts_list:
            if not isinstance(_possible_nexts, list) and not isinstance(_possible_nexts, tuple):
                continue
            pos_executables = self.getExecutables(_possible_nexts, sort=False)
            if not pos_executables:
                x += 1
                continue
            for exe_pos, cur_exe in pos_executables:
                # 进一步检查上下文可满足性，取得可以抛弃的上、下文
                # 使用模板函数操作_inner_function_get_possible_nexts_index_need_remove
                self.ProcessExeWithInnerFunction(cur_exe, exe_pos, _possible_nexts,
                                                 self._inner_function_get_possible_contexts_index_need_remove,
                                                 _possible_nexts_index_need_remove, x)
            x += 1

        _possible_nexts_index_need_remove = set(_possible_nexts_index_need_remove)  # 去重
        # 如有上下文不匹配的，直接抛弃
        final_possible_nexts_list = []
        y = 0
        for _possible_nexts in _possible_nexts_list:
            if y in _possible_nexts_index_need_remove:
                y += 1
                continue
            final_possible_nexts_list.append(_possible_nexts)
            y += 1

        # 倒序处理
        if final_possible_nexts_list:
            final_possible_nexts_list.reverse()
        return final_possible_nexts_list

    def _inner_function_get_possible_contexts_index_need_remove(self, exe_pattern_check_result,
                                                                _possible_aboves_index_need_remove, index):
        """
        （内部函数）进一步检查上下文可满足性，取得可以抛弃的上、下文
        :param _exe_pattern_check_result:
        :param _possible_aboves_index_need_remove:
        :param index:
        :return:
        """
        if not exe_pattern_check_result or not isinstance(exe_pattern_check_result, RealArea.ExePatternCheckResult):
            raise Exception("参数错误：exe_pattern_check_result，必须是RealArea._ExePatternCheckResult类型！")

        # 分项取得上下文的检查结果（context_satisfaction_result是一个tuple）
        aboves_satisfied, nexts_satisfied, aboves_matched_or_need_parents, \
        nexts_matched_or_need_parents = exe_pattern_check_result.context_satisfaction_result
        can_break = False
        if not aboves_satisfied or not nexts_satisfied:
            _possible_aboves_index_need_remove.append(index)
            can_break = True

        return can_break

    def _processKnowledgeDictAnything(self, realLevelResult, klg_dict):
        """
        处理结果中的Anything,例如：已知：牛有腿，牛有角，输入：牛有什么，输出：牛有腿，牛有角
        :param realLevelResult:
        :return:
        """
        klgs = []
        for kid, klg in klg_dict.items():
            components = klg.getSequenceComponents()
            if not self._hasAnything(components):
                continue
            cur_klgs = []
            self._processAnything(components, cur_klgs)
            if cur_klgs:
                klgs.extend(cur_klgs)
        if klgs:
            realLevelResult.anything_matched_klgs = klgs
        return klgs

    def _processAnything(self, reals, result):
        """
        处理结果中的Anything，例如：已知：牛有腿，牛有角，输入：牛有什么，输出：牛有腿，牛有角
        :param reals:
        :return:
        """
        if result is None:
            result = []
        if Collection.isPlainRealChain(reals):
            if self._hasAnything(reals):
                klgs = self._getAnythingMatchedKnowledges(reals)
                if klgs:
                    result.extend(klgs)
        else:
            for real in reals:
                if isinstance(real, list):
                    self._processAnything(real, result)

    def _getAnythingMatchedKnowledges(self, reals):
        anything_indexes = []
        i = 0
        for real in reals:
            if isinstance(real, RealObject):
                if real.isAnything():
                    anything_indexes.append(i)
            i += 1
        final_reals = []  # 取得去除anything之后的各段切片
        j = 0
        for i in anything_indexes:
            cur_reals = reals[j:i]  # 切片
            if cur_reals:
                final_reals.append(cur_reals)

            j = i + 1  # 下一个切片的开始位置

        # 还要取得最后一个anything后边的所有对象
        cur_reals = reals[anything_indexes[-1] + 1:]  # 切片
        if cur_reals:
            final_reals.append(cur_reals)

        start = None
        middles = None
        end = None
        if len(final_reals) == 1:
            if len(anything_indexes) == 1 and anything_indexes[0] == 0:  # 这里考虑开始就是“什么”，例如：什么-父对象-水果
                end = final_reals[0]
            else:
                start = final_reals[0]
        elif len(final_reals) == 2:
            start = final_reals[0]
            end = final_reals[1]
        elif len(final_reals) >= 3:
            start = final_reals[0]
            middles = final_reals[1:-2]
            end = final_reals[-1]

        if start:
            start = list(start)
            start.insert(0, "[")
        else:
            start = "["

        if not middles:
            middles = [""]
        if end:
            end = list(end)
            end.append("]")
        else:
            end = "]"

        klgs = Knowledge.getAllLikeByStartMiddleEndInDB(attributeName="s_chain",
                                                        start=start, end=end, middles=middles,
                                                        seperator=",",
                                                        memory=self.Mind.Memory)

        if not klgs:
            return None
        _klgs = []
        if isinstance(klgs, list):
            for klg in klgs:
                try:
                    klg.getChainItems()
                    # todo 这里如何过滤嵌套的知识链？
                    if not Instincts.instinct_original_list in klg._s_chain_items:
                        _klgs.append(klg)
                except:
                    pass
        else:  # 单独一个knowledge
            try:
                klgs.getChainItems()
                # todo 这里如何过滤嵌套的知识链？
                if not Instincts.instinct_original_list in klgs._s_chain_items:
                    _klgs.append(klgs)
            except:
                pass
        return _klgs

    def _hasAnything(self, reals):
        """
        判断实际对象链中是否有Instincts.instinct_original_anything
        :param reals:
        :return:
        """
        for real in reals:
            if isinstance(real, list):
                child_has_anything = self._hasAnything(real)
                if child_has_anything:
                    return True
            elif isinstance(real, RealObject):
                if real.isAnything():
                    return True
        return False

    def _processMisunderstoodPartitions(self, realLevelResult):
        """
        考虑冲突、未知、未满足、动词交联等部分导致的未能理解
        :param realLevelResult:
        :return:
        """
        if realLevelResult.hasLinkedActions():
            # 如果有动词交联的情况：
            # 1、将第一个动词的前部（至前一个动词止），与第二个动词及后续部分（至第三个动词止）重新拼合
            # 2、作为集合考虑
            self._processLinkedActions(realLevelResult)
            pass

        if realLevelResult.hasUnknowns():  # 如果有未知的，判断是否全部未知，如否，将能够按位置相连的未知实际对象连接在一起，
            if realLevelResult.isAllUnknowns():
                # 记录理解信息
                realLevelResult.realLevelThinkingRecords.setRealLevelUnderstoodRecord(
                    ThinkingInfo.RealLevelInfo.UnderstoodInfo.ALL_REALS_UNKNOWN, realLevelResult.reals)

            else:
                realLevelResult.processUnknowns()

        if realLevelResult.hasUnsatisfiedFragments():  # 如果有未满足的，需要上下文才能进一步处理
            if realLevelResult.isAllNeedContext():
                # 记录理解信息
                realLevelResult.realLevelThinkingRecords.setRealLevelUnderstoodRecord(
                    ThinkingInfo.RealLevelInfo.UnderstoodInfo.REALS_NEED_CONTEXT,
                    realLevelResult.unsatisfiedFragments)

            else:
                self._processUnsatisfiedFragments(realLevelResult)

        # 如果仍未能够理解，考虑冲突
        # 理解片段的冲突处理。
        # 例如：牛组件腿属性黄，可以分解出的理解片段包括：牛组件腿，腿属性黄，
        # 这两部分存在冲突，按顺序只能满足前者，那么后者 属性黄 的上文就包括：腿、牛组件腿、牛，这需要进一步处理
        conflicted_understoodFragments = realLevelResult.getConflictedUnderstoodFragments()
        if conflicted_understoodFragments:
            # 记录理解信息
            realLevelResult.realLevelThinkingRecords.setRealLevelUnderstoodRecord(
                ThinkingInfo.RealLevelInfo.UnderstoodInfo.FRAGMENTS_CONFLICTED_MISUNDERSTOOD,
                conflicted_understoodFragments)

    def _processLinkedActions(self, realLevelResult):
        """
        处理动词交联的情况
        :return:
        :remarks:
        如果有动词交联的情况：
            1、动词的分组，例如：马有是人类，有、是均为动作，分成[马,有,[是,人类]],[[马,有],是,人类]
            将第一个动词的前部（至前一个动词止），与第二个动词及后续部分（至第三个动词止）重新拼合
            2、作为集合考虑
        """
        for linkedAction in realLevelResult.linkedActions:
            if len(linkedAction.actions) == len(realLevelResult.reals):  # 全部都是动作
                frag = CollectionFragment(realLevelResult, realLevelResult.reals, 0, len(realLevelResult.reals))
                self._thinkAsCollection(realLevelResult, frag, realsType=ObjType.COMMON_ACTION)
                if not realLevelResult.isAllUnderstood():
                    frag = ModificationFragment(realLevelResult, realLevelResult.reals, 0, len(realLevelResult.reals))
                    self._thinkAsModification(realLevelResult, frag, realsType=ObjType.COMMON_ACTION)

            else:
                return self._processLinkedAction(realLevelResult, linkedAction)

    def _processLinkedAction(self, realLevelResult, linkedAction):
        """
        处理动词交联。
        :param realLevelResult:
        :param linkedAction:
        :return:
        """
        aboves_and_nexts_list = self._get_linkedAction_action_aboves_and_nexts(
            realLevelResult.reals, linkedAction)

        new_created_reals_list = []
        for i in range(len(linkedAction.actions)):
            cur_aboves_and_nexts = aboves_and_nexts_list[i]

            cur_action = linkedAction.actions[i]
            cur_action_exe_info = cur_action.ExecutionInfo.getSelfLinearExecutionInfo()
            cur_action_index = -1
            try:
                cur_action_index = cur_aboves_and_nexts.index(cur_action)
            except:
                pass
            if cur_action_index == -1:
                raise Exception("当前动作不在上下文对象列表中！")
            # 根据动作的pattern定义来创建对象链
            if cur_action_exe_info and cur_action_exe_info.isExecutable():
                cur_action_exe_info.restoreCurObjIndex()  # 重置索引

                while True:
                    exe_pattern, exe_meaning, exe_meaning_value = cur_action_exe_info.getCur()
                    if not exe_pattern or not exe_meaning:  # 已经取不到了，停止循环
                        break
                    # 根据动作的pattern定义来创建对象链
                    cur_new_created_reals_list = self._createRealChainByPattern(cur_aboves_and_nexts,
                                                                                cur_action_index,
                                                                                cur_action,
                                                                                exe_pattern)
                    if cur_new_created_reals_list:
                        new_created_reals_list.extend(cur_new_created_reals_list)

                cur_action_exe_info.restoreCurObjIndex()  # 重置索引

        if new_created_reals_list:
            new_created_reals_list = set(new_created_reals_list)  # 去重
            _regeneratedRealLevelResults = []  # 必须建立列表，然后在下面的循环体外执行，否则将无限循环
            for new_created_reals in new_created_reals_list:
                # 创建一个新的重构的实际对象链的思考结果，并添加到regeneratedRealLevelResults列表中。
                _regeneratedRealLevelResult = realLevelResult.regeneratedRealLevelResults.createNewRegeneratedRealLevelResult(
                    new_created_reals)
                _regeneratedRealLevelResults.append(_regeneratedRealLevelResult)
            # 必须建立列表，然后在上面的循环体外执行，否则将无限循环
            for _regeneratedRealLevelResult in _regeneratedRealLevelResults:
                self._tryUnderstand(_regeneratedRealLevelResult)
                if _regeneratedRealLevelResult.isAllUnderstood():
                    pass

    def _get_linkedAction_action_aboves_and_nexts(self, reals, linkedAction):
        """
        以动词为基点，取得动词的前部（至前一个动词止），与第二个动词及后续部分（至第三个动词止）重新拼合
        :return: 
        """
        # 以第一个动词为基点，取得上文中的所有动词
        above_pos_executables = self.getExecutables(reals, sort=False, start_pos=0,
                                                    end_pos=linkedAction.first_pos)

        # 以最后一个动词为基点，取得下文中的所有动词
        next_pos_executables = self.getExecutables(reals, sort=False,
                                                   start_pos=linkedAction.first_pos + len(linkedAction.actions))

        # 当前动词的前部（至前一个动词止）
        # todo 目前未考虑怎么去除已理解的部分
        above_start_pos = 0
        if above_pos_executables and len(above_pos_executables) > 0:
            above_start_pos = above_pos_executables[-1][0]  # 元组，拆开

        aboves = list(reals[above_start_pos:linkedAction.first_pos])

        next_end_pos = len(reals)
        if next_pos_executables and len(next_pos_executables) > 0:
            next_end_pos = next_pos_executables[0][0]  # 元组，拆开

        nexts = list(reals[linkedAction.first_pos + len(linkedAction.actions):next_end_pos])

        aboves_and_nexts_list = []
        for i in range(len(linkedAction.actions)):
            cur_aboves = copy.copy(aboves)
            cur_aboves.extend(linkedAction.actions[0:i])

            cur_nexts = list(linkedAction.actions[i + 1:])
            cur_nexts.extend(nexts)
            aboves_and_nexts_list.append([cur_aboves, linkedAction.actions[i], cur_nexts])

        return aboves_and_nexts_list

    @staticmethod
    def getExecutables(objs, sort=True, start_pos=None, end_pos=None):
        """
        递归取得实际对象链中所有的可执行性对象
        :param objs: 实际对象、知识链、understoodfragment组成的链
        :return: pos_executables:{pos:(real,weight)/{pos:(real,weight)}} {位置:(实际对象,权重)或pos_executables(代表着嵌套)}
        """
        # 首先取得所有的可执行性对象
        pos_executables = []
        # pos_sub_pos_executables
        from loongtian.nvwa.models.realObject import RealObject
        from loongtian.nvwa.models.realObject import RelatedObj
        if start_pos is None:
            start_pos = 0
        if end_pos is None:
            end_pos = len(objs)
        if start_pos >= end_pos:
            return None

        cur_pos = start_pos
        while cur_pos < end_pos:
            obj = objs[cur_pos]
            if isinstance(obj, RelatedObj):
                obj = obj.obj
            if not isinstance(obj, RealObject):
                cur_pos += 1
                continue
            if obj.isExecutable():  # 判断当前实际对象是否是可执行性对象
                obj.ExecutionInfo.getSelfLinearExecutionInfo()  # 取得执行信息
                pos_executables.append((cur_pos, obj))
            cur_pos += 1

        if pos_executables and sort:
            # 根据(pos, real, weight)的weight/pos进行排序
            # todo 目前的公式为：weight/pos
            pos_executables.sort(key=lambda x: x[1].weight / float(cur_pos), reverse=True)

        return pos_executables

    def _createRealChainByPattern(self, aboves_and_nexts, exe_index_in_context, exe, exe_pattern):
        """
        根据动作的pattern定义来创建对象链
        :param action_aboves:
        :param action_nexts:
        :param exe_pattern:
        :return:
        """
        action_aboves = aboves_and_nexts[0:exe_index_in_context]
        action_nexts = aboves_and_nexts[exe_index_in_context + 1:]
        # if not action_aboves and not action_nexts:
        #     return None # 啥都没有，还找个屁！
        # 由于切片的原因，要扒一层皮
        if action_aboves:
            action_aboves = action_aboves[0]
        if action_nexts:
            action_nexts = action_nexts[0]
        new_obj_chain_list = []

        exe_pattern_components = exe_pattern.getSequenceComponents()
        exe_pos_in_pattern = RealArea.getIndexInlist(exe_pattern_components, exe,
                                                     raiseException=True,
                                                     errorMsg="当前可执行实际对象不在其定义的pattern之中！pattern定义错误！")

        # 1、取得模式（pattern）中占位符的父对象
        exe_above_pattern_components = exe_pattern_components[0:exe_pos_in_pattern]
        exe_next_pattern_components = exe_pattern_components[exe_pos_in_pattern + 1:]

        above_new_created_list_list = []
        for exe_above_pattern_component in exe_above_pattern_components:
            above_need_match_parents, related_ks = exe_above_pattern_component.Constitutions.getSelfParentObjects()
            cur_above_new_created_list_list = self._created_new_obj_by_parent(above_need_match_parents,
                                                                              action_aboves)
            above_new_created_list_list.extend(cur_above_new_created_list_list)
        next_new_created_list_list = []
        for exe_next_pattern_component in exe_next_pattern_components:
            next_need_match_parents, related_ks = exe_next_pattern_component.Constitutions.getSelfParentObjects()

            cur_next_new_created_list_list = self._created_new_obj_by_parent(next_need_match_parents,
                                                                             action_nexts)
            next_new_created_list_list.extend(cur_next_new_created_list_list)

        # 笛卡尔积
        for new_obj_chain in itertools.product(
                *[above_new_created_list_list, [exe_pattern_components[1]], next_new_created_list_list]):
            new_obj_chain_list.append(new_obj_chain)

        return new_obj_chain_list

    @staticmethod
    def getIndexInlist(list, obj, raiseException=False, errorMsg=""):
        """
        取得对象在list中的位置。
        :param list:
        :param obj:
        :param raiseException: 是否抛出错误
        :param errorMsg: 错误信息
        :return:
        """
        index = -1
        try:
            index = list.index(obj)
        except Exception as ex:
            if raiseException:
                raise Exception(errorMsg)

        return index

    def _created_new_obj_by_parent(self, need_match_parents, objs):
        """
        根据实际对象链创建知识链、代表元对象的实际对象、代表集合的实际对象
        :param need_match_parents:
        :param objs:
        :return:
        """

        new_created_list = []

        new_created = None

        if need_match_parents:
            for need_match_parent in need_match_parents:
                # 0、如果是元知识链，特殊处理
                if need_match_parent.isSame(
                        Instincts.instinct_original_knowledge) or \
                        need_match_parent.Constitutions.isChild(
                            Instincts.instinct_original_knowledge):
                    new_created = Knowledge.createKnowledgeByObjChain(objs,
                                                                      understood_ratio=Character.Inner_Thinking_Link_Weight,
                                                                      recordInDB=False,
                                                                      memory=self.Mind.Memory)
                # 1、如果是元对象，特殊处理
                elif need_match_parent.isSame(
                        Instincts.instinct_original_object) or \
                        need_match_parent.Constitutions.isChild(
                            Instincts.instinct_original_object):

                    if len(objs) > 1:
                        klg = Knowledge.createKnowledgeByObjChain(objs,
                                                                  understood_ratio=Character.Inner_Thinking_Link_Weight,
                                                                  recordInDB=False,
                                                                  memory=self.Mind.Memory)
                        new_created = klg.toEntityRealObject()
                    else:
                        new_created = objs[0]
                        if not new_created.isSame(need_match_parent) and \
                                not new_created.Constitutions.isChild(need_match_parent):
                            new_created = None

                    if new_created:
                        new_created.Constitutions.addParent(need_match_parent, recordInDB=False)

                # 2、如果是元集合，特殊处理
                elif need_match_parent.isSame(
                        Instincts.instinct_original_collection) or \
                        need_match_parent.Constitutions.isChild(
                            Instincts.instinct_original_collection):
                    if len(objs) > 1:
                        klg = Knowledge.createKnowledgeByObjChain(objs,
                                                                  understood_ratio=Character.Inner_Thinking_Link_Weight,
                                                                  recordInDB=False,
                                                                  memory=self.Mind.Memory)
                        new_created = klg.toCollectionRealObject()
                    else:
                        new_created = objs[0]
                        if not new_created.isSame(need_match_parent) and \
                                not new_created.Constitutions.isChild(need_match_parent):
                            new_created = None

                    if new_created:
                        new_created.Constitutions.addParent(need_match_parent, recordInDB=False)

                else:  # 只能为实际对象
                    new_created = RealObject(memory=self.Mind.Memory)
                    new_created.Constitutions.addParent(Instincts.instinct_original_object, recordInDB=False)
                    new_created.remark = str(objs)
            if new_created:
                new_created_list.append(new_created)
        else:  # 只能是元对象
            if len(objs) == 1:
                new_created = objs[0]
            elif len(objs) > 1:
                klg = Knowledge.createKnowledgeByObjChain(objs,
                                                          understood_ratio=Character.Inner_Thinking_Link_Weight,
                                                          recordInDB=False,
                                                          memory=self.Mind.Memory)
                new_created = klg.toEntityRealObject()

            # new_created.Constitutions.addParent(Instincts.instinct_original_object, recordInDB=False)
            new_created_list.append(new_created)

        return new_created_list

    def _thinkAsCollection(self, realLevelResult, collectionFrag, realsType=ObjType.REAL_OBJECT):
        """
        将一组实际对象（知识链等）作为集合来考虑
        :param realLevelResult:
        :param collectionFrag:
        :return:
        """
        reals = collectionFrag.getFragmentedReals(self.Mind.Memory)
        if not reals:
            return None
        _collection_klg = Collection.createKnowledgeAsCollection(reals, recordInDB=False, memory=self.Mind.Memory)
        collectionFrag.collection_klg = _collection_klg
        collectionFrag.collection_real = _collection_klg._self_realObject
        if realsType == ObjType.REAL_OBJECT:
            collectionFrag.entity_real = _collection_klg.toEntityRealObject()
        realLevelResult.collectionFragments.append(collectionFrag)

        return collectionFrag

    def _thinkAsModification(self, realLevelResult, modificationFrag, realsType=ObjType.REAL_OBJECT):
        """

        :param realLevelResult:
        :param modificationFrag:
        :param realsType:
        :return:
        """

    def _processUnsatisfiedFragments(self, realLevelResult):
        """
        如果有未满足的，需要上下文才能进一步处理
        :return:
        """
        for unsatisfiedFragment in realLevelResult.unsatisfiedFragments:
            new_obj_chain_list = self._get_unsatisfiedFragment_action_aboves_and_nexts(
                realLevelResult.reals, unsatisfiedFragment)
            if new_obj_chain_list:
                for new_obj_chain in new_obj_chain_list:
                    # 创建一个新的重构的实际对象链的思考结果，并添加到regeneratedRealLevelResults列表中。
                    _regeneratedRealLevelResult = realLevelResult.regeneratedRealLevelResults.createNewRegeneratedRealLevelResult(
                        new_obj_chain)
                    self._tryUnderstand(_regeneratedRealLevelResult)
                    if _regeneratedRealLevelResult.isAllUnderstood():
                        pass

    def _get_unsatisfiedFragment_action_aboves_and_nexts(self, reals, unsatisfiedFragment):
        """
        取得当前未满足的片段的上下文
        :param reals:
        :param unsatisfiedFragment:
        :return:
        """
        # 以动词为基点，取得上文中的所有动词
        above_pos_executables = self.getExecutables(reals, sort=False, start_pos=0,
                                                    end_pos=unsatisfiedFragment.cur_exe_pos)

        # 以动词为基点，取得下文中的所有动词
        next_pos_executables = self.getExecutables(reals, sort=False,
                                                   start_pos=unsatisfiedFragment.cur_exe_pos + 1)

        # 当前动词的前部（至前一个动词止）
        # todo 目前未考虑怎么去除已理解的部分
        above_start_pos = 0
        if above_pos_executables and len(above_pos_executables) > 0:
            above_start_pos = above_pos_executables[-1][0]  # 元组，拆开

        aboves = list(reals[above_start_pos:unsatisfiedFragment.cur_exe_pos])

        next_end_pos = len(reals)
        if next_pos_executables and len(next_pos_executables) > 0:
            next_end_pos = next_pos_executables[0][0]  # 元组，拆开

        nexts = list(reals[unsatisfiedFragment.cur_exe_pos + 1:next_end_pos])

        above_new_created_list = self._created_new_obj_by_parent(unsatisfiedFragment.aboves_matched_or_need_parents,
                                                                 aboves)
        next_new_created_list = self._created_new_obj_by_parent(unsatisfiedFragment.aboves_matched_or_need_parents,
                                                                nexts)

        new_obj_chain_list = []
        # 笛卡尔积
        for new_obj_chain in itertools.product(
                *[above_new_created_list, [reals[unsatisfiedFragment.cur_exe_pos]], next_new_created_list]):
            new_obj_chain_list.append(new_obj_chain)

        return new_obj_chain_list
#
# class KnowledgeArea(SequencedObj):
#     """
#     每个Mind的既往知识区
#     """
#
#     def __init__(self, mind):
#         super(KnowledgeArea, self).__init__()
#         self.Mind = mind
