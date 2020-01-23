#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

"""
对各种记忆类型的包装类。
"""

from loongtian.util.log import logger
from loongtian.util.common.doubleKeyDict import DoubleKeyDict

from loongtian.nvwa.models.baseEntity import BaseEntity
from loongtian.nvwa.models.metaData import MetaData
from loongtian.nvwa.models.metaNet import MetaNet
from loongtian.nvwa.models.realObject import RealObject
from loongtian.nvwa.models.knowledge import Knowledge
from loongtian.nvwa.models.layer import Layer

from loongtian.nvwa.runtime.thinkResult.fragments import UnknownMetas, ProceedUnknownMetas

from loongtian.nvwa.engines import metaDataHelper


class BaseMemory(object):
    """
    记忆区的基础类
    """

    def __init__(self, memoryCentral):
        """
        记忆区的基础类
        :param memoryCentral:
        """
        self.MemoryCentral = memoryCentral

        self.WordFrequncyDict = {}  # 已经加载的元数据，其格式为{元数据（字符串）:词频（平均值）}

        self.ChainCharMetaDict = {}  # 以每个字符作为索引，[True/False,meta,frequncy,{...}]为值的字典，含义为：
        # [是否字符块末尾，元数据字符串，频率，{后续子串字典}]
        # 例如：
        # ddd={
        #     "中":[False,None,0.0,
        #         {"央":[True,"中央",5.4,{}],
        #         "国":[True,"中国",8.6,
        #             {"人":[True,"中国人",6.2,
        #                 {"好":[True,"中国人好",3.2,{}],
        #                 "民":[True,"中国人民",5.2,
        #                     {"解":[False,None,0.0,
        #                         {"放":[False,None,0.0,
        #                             {"军":[True,"中国人民解放军",6.2,{}]}]}],
        #                     "法":[False,None,0.0,
        #                         {"院":[True,"中国人民法院",6.2,{}]}]}]}]}]}]}

        self.NgramDict = {}  # n元丁字型结构的字符块链表（数据库存储丁字型结构，用的时候加载）
        # 目前使用邻接匹配法——ngram，根据“元数”，进行二元、三元关系计算，对匹配出来的字符块链进行排序

        # self.FirstCharMetaDict = {}  # 首字符元数据字典。以首字符作为索引，所有元数据（按长度倒序排列）的列表为值。
        #                              # [弃用]（2016-04-06 langway@163.com）
        #
        # self.StopMarksRexPattern = {}  # [弃用]已经完成的分解句子所需的标点符号正则pattern。

        self.MetaDataValueDict = {}  # 已经加载的元数据，其格式为{元数据的值（字符串）:元数据}{value(word):metaData}
        self.MetaDataIdDict = {}  # 已经加载的元数据，其格式为{元数据的Id（字符串）:元数据}，{id:metaData}

        # 所有已加载的元数据网，用以查询元数据的构建（双键值字典）
        self.MetaNetDict = DoubleKeyDict(key1_name="startid", key2_name="endid")
        self.MetaNetMNValueDict ={} # 已经加载的元数据网，其格式为{元数据的mnvalue（字符串）:元数据}{mnvalue(word):metaData}

        self.RealObjectIdDict = {}  # 实际对象字典{id:realObject}

        self.KnowledgeDict = DoubleKeyDict(key1_name="startid", key2_name="endid")  # 知识链对象字典（双键值字典）

        self.LayerDict = DoubleKeyDict(key1_name="startid", key2_name="endid")  # 分层对象的关系表字典（双键值字典）

        self.BaseEntityIdDict = {}
        # 测试用，生产环境下注释掉基础类对象字典{id:BaseEntity}
        self.BaseEntityDoubleKeyDict = DoubleKeyDict(key1_name="pkId", key2_name="pkUuid")

    def addInMemory(self, obj):
        """
        在内存中添加对应对象
        :param id:
        :param obj:
        :return:
        """
        if not isinstance(obj, BaseEntity):
            return

        if isinstance(obj, MetaData):
            self.addMetaInMemory(obj)
        elif isinstance(obj, MetaNet):
            self.addMetaNetInMemory(obj)
        elif isinstance(obj, RealObject):
            self.addRealObjectInMemory(obj)
        elif isinstance(obj, Knowledge):
            self.addKnowledgeInMemory(obj)
        elif isinstance(obj, Layer):
            self.addLayerInMemory(obj)
        elif isinstance(obj, BaseEntity):
            self.BaseEntityIdDict[obj.id] = obj  # 测试用，生产环境下注释掉基础类对象字典{id:BaseEntity}
            if len(obj.retrieveColumns) == 2:
                key1 = getattr(obj, obj.retrieveColumns[0])
                key2 = getattr(obj, obj.retrieveColumns[1])
                self.BaseEntityDoubleKeyDict.add(obj.id, key1, key2, obj)
        else:
            raise Exception("不支持的类型：%s" % type(obj))


    def addMetasInMemory(self, metas):
        """
        加载元数据列表到记忆中
        :param metas:
        :return:
        """
        for meta in metas:
            self.addMetaInMemory(meta)

    def addMetaInMemory(self, meta):
        """
        加载元数据到记忆中
        :param relatedMetas:
        :return:
        """
        

        self.MetaDataIdDict[meta.id] = meta
        self.MetaDataValueDict[meta.mvalue] = meta
        self.WordFrequncyDict[meta.mvalue] = meta.weight
        # 2019-02-19:不能元数据一创建就加载到ChainCharFrequncyMetaDict，否则会出现大量未识别
        if meta._isInDB:  # 必须是数据库中保存的，才加载到字典
            self.loadMetaToChainCharFrequncyMetaDict(meta)

    def loadMetaToChainCharFrequncyMetaDict(self, meta):
        """
        加载一个元数据到ChainCharFrequncyMetaDict
        :param meta:
        :return:
        """
        return metaDataHelper.loadChainCharFrequncyMetaDict({meta.mvalue: meta.weight}, self.ChainCharMetaDict)

    def loadMetasToChainCharFrequncyMetaDict(self, metas):
        """
        加载多个元数据到ChainCharFrequncyMetaDict
        :param metas:
        :return:
        """
        for meta in metas:
            metaDataHelper.loadChainCharFrequncyMetaDict({meta.mvalue: meta.weight}, self.ChainCharMetaDict)

    def addMetaNetInMemory(self, metaNet):
        """
        加载元数据网到记忆中
        :param id:
        :param metaNet:
        :return:
        """
        metaNet.getChainItems()
        self.MetaNetMNValueDict[metaNet.mnvalue]=metaNet
        return self.MetaNetDict.add(metaNet.id, metaNet.startid, metaNet.endid, metaNet)

    def addRealObjectInMemory(self, realObj):
        """
        加载实际对象到记忆中
        :param realObj:
        :return:
        """
        self.RealObjectIdDict[realObj.id] = realObj

    def addKnowledgeInMemory(self, knowledge):
        """
        加载知识链到记忆中
        :param id:
        :param knowledge:
        :return:
        """
        return self.KnowledgeDict.add(knowledge.id, knowledge.startid, knowledge.endid, knowledge)

    def addLayerInMemory(self, layer):
        """
        加载知识链到记忆中
        :param id:
        :param knowledge:
        :return:
        """
        return self.LayerDict.add(layer.id, layer.startid, layer.endid, layer)

    def getByIdsInMemory(self, ids, _type):
        """
        从内存中根据Id列表取得对象。
        :param ids:
        :param _type:
        :return:
        """
        results = []
        for id in ids:
            result = self.getByIdInMemory(id, _type)
            if result:
                results.append(result)

        if not results:
            return None
        if len(results) == 1:
            return results[0]
        return results

    def getByIdInMemory(self, id, _type):
        """
        从内存中根据Id取得对象。
        :param id:
        :param _type:
        :return:
        """
        if _type == MetaData:
            return self.getMetaByIdInMemory(id)
        elif _type == MetaNet:
            return self.getMetaNetByIdInMemory(id)
        elif _type == RealObject:
            return self.getRealObjectByIdInMemory(id)
        elif _type == Knowledge:
            return self.getKnowledgeByIdInMemory(id)
        elif issubclass(_type, Layer):  # layer、observer
            return self.getLayerByIdInMemory(id)
        elif issubclass(_type, BaseEntity):
            return self.BaseEntityIdDict.get(id)
        else:
            raise Exception("不支持的类型：" + str(_type))

    def getMetaByIdInMemory(self, id):
        """
        从内存中根据Id取得Meta对象。
        :param id:
        :return:
        """
        return self.MetaDataIdDict.get(id)

    def getMetaByMvalueInMemory(self, mvalue):
        """
        从内存中根据元数据的值取得元数据
        :param mvalue:
        :return:
        """
        return self.MetaDataValueDict.get(mvalue)

    def getMetaNetByIdInMemory(self, mnid):
        """
        从内存中根据Id取得MetaNet对象。
        :param id:
        :return:
        """
        return self.MetaNetDict.getById(mnid)

    def getMetaNetByMNValueInMemory(self, mnvalue):
        """
        从内存中根据mnvalue取得MetaNet对象。
        :param id:
        :return:
        """
        return self.MetaNetMNValueDict.get(mnvalue)

    def getRealObjectByIdInMemory(self, rid):
        """
        从内存中根据Id取得RealObject对象。
        :param id:
        :return:
        """
        return self.RealObjectIdDict.get(rid)

    def getKnowledgeByIdInMemory(self, kid):
        """
        从内存中根据Id取得Knowledge对象。
        :param id:
        :return:
        """
        return self.KnowledgeDict.getById(kid)

    def getLayerByIdInMemory(self, lid):
        """
        从内存中根据Id取得Layer对象。
        :param id:
        :return:
        """
        return self.KnowledgeDict.getById(lid)

    def getBySingleKeyInMemory(self, key, _type):
        """
        从内存中根据key1, key2取得对象。
        :param key:
        :param _type:
        :return:
        """
        if _type == MetaData:
            return self.getMetaByMvalueInMemory(key)
        elif _type == MetaNet:
            return self.getMetaNetByIdInMemory(key)
        elif _type == RealObject:
            return self.getRealObjectByIdInMemory(key)
        elif _type == Knowledge:
            return self.getKnowledgeByIdInMemory(key)
        elif issubclass(_type, Layer):  # layer、observer
            return self.getLayerByIdInMemory(key)
        elif issubclass(_type, BaseEntity):
            return self.BaseEntityIdDict.get(key)
        else:
            raise Exception("不支持的类型：" + str(_type))

    def getByDoubleKeysInMemory(self, key1, key2, _type):
        """
        从内存中根据key1, key2取得对象。
        :param key1:
        :param key2:
        :param _type:
        :return:
        """

        if _type == MetaNet:
            return self.getMetaNetByDoubleKeysInMemory(key1, key2)
        elif _type == Knowledge:
            return self.getKnowledgeByDoubleKeysInMemory(key1, key2)
        elif issubclass(_type, Layer):  # layer、observer
            return self.getLayerByDoubleKeysInMemory(key1, key2)
        elif issubclass(_type, BaseEntity):
            return self.BaseEntityDoubleKeyDict.getByKeys(key1, key2)
        else:
            raise Exception("不支持的类型：" + str(_type))

    def getMetaNetByDoubleKeysInMemory(self, startid, endid):
        """
        从内存中根据startid,endid取得MetaNet对象。
        :param id:
        :return:
        """
        return self.MetaNetDict.getByKeys(startid, endid)

    def getKnowledgeByDoubleKeysInMemory(self, startid, endid):
        """
        从内存中根据startid,endid取得Knowledge对象。
        :param id:
        :return:
        """
        return self.KnowledgeDict.getByKeys(startid, endid)

    def getLayerByDoubleKeysInMemory(self, startid, endid):
        """
        从内存中根据startid,endid取得Layer对象。
        :param id:
        :return:
        """
        return self.LayerDict.getByKeys(startid, endid)

    def deleteByIdInMemory(self, id, _type):
        """
        从内存中根据Id删除对象
        :param id:
        :param _type:
        :return:
        """
        if _type == MetaData:
            return self.deleteMetaByIdInMemory(id)
        elif _type == MetaNet:
            return self.deleteMetaNetByIdInMemory(id)
        elif _type == RealObject:
            return self.deleteRealObjectByIdInMemory(id)
        elif _type == Knowledge:
            return self.deleteKnowledgeByIdInMemory(id)
        elif issubclass(_type, Layer):  # layer、observer
            return self.deleteLayerByIdInMemory(id)
        elif issubclass(_type, BaseEntity):
            obj = self.BaseEntityIdDict.get(id)
            if obj and obj.retrieveColumns and len(obj.retrieveColumns) == 2:
                key1 = getattr(obj, obj.retrieveColumns[0])
                key2 = getattr(obj, obj.retrieveColumns[1])
                self.BaseEntityDoubleKeyDict.deleteByKeys(key1, key2)

            return self.BaseEntityIdDict.pop(id, False)
        else:
            raise Exception("不支持的类型：" + str(_type))

    def deleteMetaByIdInMemory(self, id):
        """
        从内存中根据Id删除MetaData对象
        :param id:
        :return:
        """
        meta = self.MetaDataIdDict.get(id)
        if meta:
            self.MetaDataValueDict.pop(meta.mvalue)
            return self.MetaDataIdDict.pop(id, False)

    def deleteMetaNetByIdInMemory(self, mnid):
        """
        从内存中根据Id删除MetaNet对象
        :param mnid:
        :return:
        """
        return self.MetaNetDict.deleteById(mnid)

    def deleteRealObjectByIdInMemory(self, rid):
        """
        从内存中根据Id删除RealObject对象
        :param rid:
        :return:
        """
        self.RealObjectIdDict.pop(rid, False)

    def deleteKnowledgeByIdInMemory(self, kid):
        """
        从内存中根据Id删除Knowledge对象
        :param kid:
        :return:
        """
        self.KnowledgeDict.deleteById(kid)

    def deleteLayerByIdInMemory(self, lid):
        """
        从内存中根据Id删除Layer对象
        :param lid:
        :return:
        """
        return self.LayerDict.deleteById(lid)

    def flush(self):
        """
        清除所有的内存数据
        :return:
        """
        self.flushMetaData()
        self.flushMetaNet()
        self.flushRealObject()
        self.flushKnowledge()
        self.flushLayer()

        self.BaseEntityIdDict.clear()
        # 测试用，生产环境下注释掉基础类对象字典{id:BaseEntity}
        self.BaseEntityDoubleKeyDict.clean()

    def flushMetaData(self):
        """
        清除MetaData的内存数据
        :return:
        """
        self.MetaDataIdDict.clear()
        self.MetaDataValueDict.clear()

    def flushMetaNet(self):
        """
        清除MetaNet的内存数据
        :return:
        """
        self.MetaNetDict.clean()
        self.MetaNetMNValueDict.clear()

    def flushRealObject(self):
        """
        清除RealObject的内存数据
        :return:
        """
        self.RealObjectIdDict.clear()

    def flushKnowledge(self):
        """
        清除Knowledge的内存数据
        :return:
        """
        self.KnowledgeDict.clean()

    def flushLayer(self):
        """
        清除Layer的内存数据
        :return:
        """
        self.LayerDict.clean()


class WorkingMemory(BaseMemory):
    """
    工作记忆区（也叫感官记忆、临时记忆，重启后将被擦除，类似于电脑内存，其遗忘速度非常快）
    :rawParam
    构造函数参数说明
    :attribute
    第一种记忆。感官记忆（working memory）：感官记忆的保留时间由数秒至3到5分钟，信息使用过后，很快就会被遗忘。
    我想任何人都有过这样的生活经验：当我们翻开电话簿中记住某个电话号码，至少到按完所有数字后才会忘掉它；
    但有时按完号码，对方电话恰好占线，或是铃声响了太久让你以为打错而想重拨一次，
    此时不懂得记忆诀窍的你，往往只好再查一次电话簿上的那个电话号码了。
    感官记忆的容量在5到9之间，也就是说最多可以记住5个到9个数字或词汇。
    如果我们将20个东西（如字母或数字）分成有意义的7个组块（chunk），我们就可以记住它们；
    如果没有将它们分组，很难一口气记住这20个东西。
    """

    def __init__(self, memoryCentral):
        """
        工作记忆区（也叫感官记忆、临时记忆，重启后将被擦除，类似于电脑内存，其遗忘速度非常快）
        :param memoryCentral:
        """
        super(WorkingMemory, self).__init__(memoryCentral)

        # self.TextWorkingMemory=TextWorkingMemory(self)
        self.WordDoubleFrequancyDict = {}  # 本次程序启动至今加载的双字-频率字典
        # self.RawInputsLength=0 # 本次程序启动至今加载的元输入数据所有字符的总长度

        self.NewLearnedRawMetas = {}  # 自系统启动以来新学习到的元数据{word:frequncy}
        self.UnknownMetas = UnknownMetas()  # 在一个元数据链（笛卡尔积子集）中未能正确理解的元数据对象列表
        self.ProceedUnknownMetas = ProceedUnknownMetas()  # 在一个元数据链（笛卡尔积子集）中，已经经过处理的未能正确理解的元数据对象列表


# class TextWorkingMemory(object):
#     """
#     专为文本处理开辟的工作记忆区（临时记忆，重启后将被擦除，类似于电脑内存）
#     :rawParam
#     构造函数参数说明
#     :attribute
#     对象属性说明
#     """
#
#     def __init__(self, workingMemory):
#         self.WorkingMemory = workingMemory
#
#         pass
#
#     def updateMetasToPersistenceMemory(self, metas):
#         """
#         将现有的元数据（频率已更新）更新到持久记忆中。
#         :rawParam WordFrequncyDict:
#         :return:
#         """
#         self.WorkingMemory.MemoryCentral.PersistentMemory.updateMetas(metas)


class PersistentMemory(BaseMemory):
    """
    持久记忆区（长久记忆，重启后不会被被擦除，需从电脑硬盘数据或数据库加载，其遗忘速度较慢）
    第三种记忆。也称之为long-term memory，也就是我们必须锻炼的“长期记忆”能力，
    “长期记忆”特别擅长记忆一些需要经常使用的资料。
    你有没有发觉常用的一些电话号码、好朋友的姓名生日，一旦需要，这些资料就能够很自然的、随时随地从你的脑海中浮现？
    基本上，“长期记忆”是很难消失的，它可以长久保留记忆，
    就好像我们记得身份证号码、生日、家中电话号码一样。
    只是很多长期记忆的内容，因为没有清楚归档，往往找不到。
    只要通过一些回忆技巧、催眠、自我暗示等，你会发现，你记下的东西比你知道的要多不少。
    """

    def __init__(self, memoryCentral):
        super(PersistentMemory, self).__init__(memoryCentral)

        pass

    def updateMetas(self, metas):
        """
        将现有的元数据（频率已更新）更新到持久记忆中。
        :rawParam WordFrequncyDict:
        :return:
        """
        # todo 未实现
        pass


class ShortTermMemory(BaseMemory):
    """
    短期记忆区（也叫中短期记忆）。
    第二种记忆力为short.term memory，一般称之为“短期记忆”。
    现在请你闭上眼睛，回到挑灯夜战的学生时代。
    你是否也曾通宵达旦、绞尽脑汁地准备堆积如山的笔记，
    “背多芬”式地重点copy（复制）进脑中？
    但请问你在考试结束铃声响起的那一刹那，那些临时抱佛脚的内容是否一点一滴地流失，
    到最后全部还给书本呢？别觉得奇怪，这就是“短期记忆”的特色，
    你的大脑也会把这些考试资料储存在所谓的“短期记忆”中，它也是我们最常用的记忆部分。
    可惜这种记忆不太可靠。因为“短期记忆”的记忆时间即便在人脑的巅峰期，
    也只能维持12个小时至36个小时，而且持续衰减。
    过了这段时间，忘掉“抱佛脚” 的内容是不变的真理。
    但短期记忆也绝不像刀切豆腐一样，所有资料马上消失无踪，
    而是随着时间递增而逐渐消失。
    """

    def __init__(self, memoryCentral):
        super(ShortTermMemory, self).__init__(memoryCentral)

        pass


# class ShortTermKnowledge(Knowledge):
#     """
#     海马知识链（临时知识链，在HimaKnowledge中保存，由反思引擎调用）
#     """
#     __tablename__ = tables_setting.tbl_short_term_knowledge


# 海马体（hippo—campus）来处理的。“海马体”就像电脑键盘一样，在记忆的过程中，充当转换站的功能。当大脑皮质中的神经元接收到各种感官或知觉讯息时，它们会把讯息传递给海马体，假如海马体有所反应，神经元就会开始形成持久的网络；但是假如没有通过这种认可模式，那么脑部接收到的经验就会自动消逝无踪，自然也就没有记忆可言了。

import loongtian.util.helper.stringHelper as  stringHelper
from loongtian.nvwa.runtime.instinct import Instincts
from loongtian.nvwa.runtime.innerOperation import InnerOperations
from loongtian.nvwa.engines.metaEngine import TextEngine, MetaNetEngine
from loongtian.nvwa.organs.character import Character


class GeneralMemoryBase(object):
    """
    具有工作记忆区与持久记忆区的通用记忆中枢的基础类
    """

    def __init__(self):
        """
        具有工作记忆区与持久记忆区的通用记忆中枢的基础类
        """

        # 文本处理引擎，传入当前WorkingMemory以初始化元数据相关对象
        self.TextEngine = TextEngine(self)

        # 元数据网处理引擎，传入当前WorkingMemory以初始化元数据网相关对象
        self.MetaNetEngine = MetaNetEngine(self)

        self.stopMarks = stringHelper.StopMarks  # 标点符号的字典，包括0：段落标记:1：句子间标点符号:2：句子内标点符号
        # 格式为：{标点符号:[标点符号类别,词频]}

        self.stopMarkLevel = 3  # 按标点符号的划分级别（0：段落级别，1：段落级别+句子级别，2：段落级别+句子级别+句内级别）。
        self.keepStopMark = True  # 是否保留分割的标点。
        self.checkStopMark = True  # 是否检查标点。

        # 从DoubleFrequancyDict根据阀值和元输入的位置提取元数据（可能有多个）的频率阀值（超过该阀值才提取），包括：独立成字符块的阀值，连续连接成词的阀值。
        # MetaDataExtractThreshold_SingleBlock =0.09 # 从DoubleFrequancyDict根据阀值和元输入的位置提取元数据（可能有多个）的频率阀值（超过该阀值才提取），随着理解的元数据的增多，其阀值应该逐渐增加
        # 从metaNet根据阀值和元输入的位置提取元数据（可能有多个）的频率阀值（超过该阀值才提取）
        self.Threshold_ContinuousBlocks = Character.MetaDataExtractThreshold_ContinuousBlocks

        self.maxMatch = False  # 分割字符串时，是否使用最长匹配，默认为否（使用全匹配）

        # 二元字符块（bigram）相当于有向图（为丁字形结构特例），三元字符块（trigram）及以上相当于丁字型结构的分解
        self.NgramNum = Character.GramNum  # 指定进行二元、三元关系计算的“元数”,对匹配出来的字符块链进行排序，目前使用邻接匹配法——ngram，

        # 工作记忆区（也叫感官记忆、临时记忆，重启后将被擦除，类似于电脑内存，其遗忘速度非常快）
        self.WorkingMemory = WorkingMemory(self)

        # 持久记忆区（长久记忆，重启后不会被被擦除，类似于电脑硬盘数据或数据库，其遗忘速度较慢）
        self.PersistentMemory = None # 目前不创建实例，由继承类对其进行实例化

    def getByIdInMemory(self, id, _type):
        """
        从内存中根据Id取得对象。
        :param id:
        :param _type:
        :return:
        """
        result = self.WorkingMemory.getByIdInMemory(id, _type)
        if result:
            result._isInWorkingMemory = True
            return result
        result = self.PersistentMemory.getByIdInMemory(id, _type)
        if result:
            result._isInPersistentMemory = True
        return result

    def getByIdsInMemory(self, ids, _type):
        """
        从内存中根据Id列表取得对象。
        :param ids:
        :param _type:
        :return:
        """
        results = []
        for id in ids:
            result = self.getByIdInMemory(id, _type)
            if result:
                results.append(result)

        if not results:
            return None
        if len(results) == 1:
            return results[0]
        return results

    def getBySingleKeyInMemory(self, key, _type):
        """
        从内存中根据key1, key2取得对象。
        :param key:
        :param _type:
        :return:
        """
        result = self.WorkingMemory.getBySingleKeyInMemory(key, _type)
        if result:
            result._isInWorkingMemory = True
            return result
        result = self.PersistentMemory.getBySingleKeyInMemory(key, _type)
        if result and isinstance(result,BaseEntity):
            result._isInPersistentMemory = True
        return result

    def getByDoubleKeysInMemory(self, key1, key2, _type):
        """
        从内存中根据key1, key2取得对象。
        :param key1:
        :param key2:
        :param _type:
        :return:
        """
        result = self.WorkingMemory.getByDoubleKeysInMemory(key1, key2, _type)
        if result:
            if isinstance(result, BaseEntity):
                result._isInWorkingMemory = True
            return result
        result = self.PersistentMemory.getByDoubleKeysInMemory(key1, key2, _type)
        if result and isinstance(result,BaseEntity):
            result._isInPersistentMemory = True
        return result

    def deleteByIdInMemory(self, id, _type):
        """
        从内存中根据Id删除对象
        :param id:
        :param _type:
        :return:
        """
        result = self.WorkingMemory.deleteByIdInMemory(id, _type)
        if not result:
            result = self.PersistentMemory.deleteByIdInMemory(id, _type)
        return result

    def getMetaByMvalueInMemory(self, mvalue):
        """
        从内存中根据元数据的值取得元数据
        :param mvalue:
        :return:
        """
        result = self.WorkingMemory.getMetaByMvalueInMemory(mvalue)
        if result:
            result._isInWorkingMemory = True
            return result
        result = self.PersistentMemory.getMetaByMvalueInMemory(mvalue)
        if result:
            result._isInPersistentMemory = True
        return result

    def getMetaNetByMNValueInMemory(self, mnvalue):
        """
        从内存中根据mnvalue取得MetaNet对象。
        :param id:
        :return:
        """
        result = self.WorkingMemory.getMetaNetByMNValueInMemory(mnvalue)
        if result:
            result._isInWorkingMemory = True
            return result
        result = self.PersistentMemory.getMetaNetByMNValueInMemory(mnvalue)
        if result:
            result._isInPersistentMemory = True
        return result

    def flush(self):
        """
        清除所有的内存数据
        :return:
        """
        logger.info("开始清除记忆中枢（内存）所有的数据...")
        logger.info("开始清除临时记忆区（内存）所有的数据...")
        self.WorkingMemory.flush()
        logger.info("开始清除持久记忆区（内存）所有的数据...")
        self.PersistentMemory.flush()
        logger.info("清除所有的记忆中枢（内存）数据完毕。")

    def init(self, forceToReload=False):
        """
        系统初始化记忆中枢。
        :return:
        :remarks:
        1、加载元数据到内存。
        2、从MetaNet加载NgramDict到内存。
        3、加载所有直觉（包括属性、组件等顶级关系，意思是等分层“标签”）
        4、加载所有女娲系统内部操作对象的实际对象
        """
        self.loadAllMetaFromDB(forceToReload=forceToReload)  # 加载元数据到内存
        self.loadNgramDictFromDB(forceToReload=forceToReload)  # 从MetaNet加载NgramDict到内存
        self.loadAllInstincts(forceToReload=forceToReload)  # 加载所有直觉（包括属性、组件等顶级关系，意思是等分层“标签”）
        self.loadAllInnerOperations(forceToReload=forceToReload)  # 加载所有女娲系统内部操作对象的实际对象

    def loadAllMetaFromDB(self, forceToReload=False):
        """
        从数据库加载所有的元数据。
        同时建立MetaDataIdDict、MetaDataValueDict、WordFrequncyDict、ChainCharMetaDict
        :param forceToReload: 是否强制重新加载一次
        :return:
        """
        return self.TextEngine.loadAllMetaFromDB(forceToReload)

    def loadAllInstincts(self, forceToReload=False):
        """
        加载所有直觉（包括属性、组件等顶级关系，意思是等分层“标签”）
        :param forceToReload:
        :return:
        """
        Instincts.loadAllInstincts(forceToReload, memory=self)

    def loadAllInnerOperations(self, forceToReload=False):
        """
        加载所有女娲系统内部操作对象的实际对象
        :param forceToReload:
        :return:
        """
        InnerOperations.loadAllInnerOperations(forceToReload, memory=self)
        InnerOperations.createMeaningExecutionInfo(memory=self)
        InnerOperations.createTopRelationExecutionInfo(memory=self)
        InnerOperations.createRealsSynchronizer(memory=self)

    def loadNgramDictFromDB(self, NgramNum=None, forceToReload=False):
        """
        加载所有的N元关系到内存中的NgramDict
        :return:
        """
        return self.MetaNetEngine.loadNgramDictFromDB(NgramNum, forceToReload)
