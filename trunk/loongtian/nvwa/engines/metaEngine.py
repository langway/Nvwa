#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
文本引擎
"""
__author__ = 'Leon'

from loongtian.nvwa.engines.engineBase import EngineBase
from loongtian.nvwa.engines import metaDataHelper
from loongtian.nvwa.engines.ngramEngine import NgramEngine
from loongtian.nvwa.engines.segmentedResult import *
from loongtian.nvwa.models.metaData import MetaData
from loongtian.nvwa.models.metaNet import MetaNet
from loongtian.util.helper import stringHelper
from loongtian.util.log import logger


class MetaNetEngine(EngineBase):
    """
    元数据网处理引擎
    :rawParam
    构造函数参数说明
    :attribute
    对象属性说明
    """

    def __init__(self, memory):
        """
        元数据网处理引擎
        :param memory: 用来存放当前对象的内存空间（避免每次都从数据库中调用）
                       当前MetaNetEngine的memory是MemoryCentral
        """
        super(MetaNetEngine, self).__init__(memory)

        self._allNgramDictFromDBLoaded = False  # 是否已从MetaNet数据库加载NgramDict的标记

    def createMetaNetByMetaChain(self, metaChain):
        """
        根据MetaChain创建MetaNetItem
        :param meta_chain:[MetaData,[MetaData]]
        :return:
        """
        return MetaNet._createByObjChain(metaChain)

    def createMetaNetBySequnceWords(self, s_chain):
        """
        根据字符串列表创建元数据网络
        :param s_chain: 字符串列表
        :return:
        """
        return MetaNet.createMetaNetBySequnceWords(s_chain)

    def loadNgramDictFromDB(self, NgramNum=None, forceToReload=False):
        """
        加载所有的N元关系到内存中的NgramDict
        :return:
        """
        if self._allNgramDictFromDBLoaded and not forceToReload:
            return

        if not self.MemoryCentral:
            return False
        if not NgramNum:
            NgramNum = self.MemoryCentral.NgramNum
        try:
            import uuid
            _uuid = str(uuid.uuid1())
            logger.info("开始从MetaNet数据库加载NgramDict", timeStartMark=_uuid)
            allMetaNet = NgramEngine.loadNgramDictFromDB(self.MemoryCentral.PersistentMemory.NgramDict, NgramNum,memory=self.MemoryCentral)
            self._allNgramDictFromDBLoaded = True
            msg="从MetaNet数据库加载NgramDict完毕"
            if not allMetaNet:
                msg+="，没有可用的MetaNet"
            logger.info(msg, timeEndMark=_uuid)
        except Exception as e:
            logger.log(e)
            raise e

        return allMetaNet

    def loadNgramDictFromMetaNet(self, metaNetItem, NgramNum=2):
        """
        记录字符块之间的二元、三元关系。
        公式说明：N元关系的传统计算公式：已知 “i” 一共出现了2533次,而其后出现 “want” 的情况一共有827次,所以P(want|i)=827/2533≈0.33。
        但由于存在数据稀疏性的问题（主要是样本总数不固定，是一个无限集合，未出现的情况未考虑），导致计算结果非常不准确（与训练数据集有关）
        原方案：总出现次数/总字符块数量，即p=n/m，计算结果为小数
                如果已经存在以前的二元关系，计算公式为：(p0+p1)/2
                这一方案的思路，是“域中存活”，即按有限样本数，出现的即为一个集合，然后计算。
                但这一方案的问题，是最后都会“趋同”，也就是如果训练集足够大，其出现概率会大体一致
        新方案（2018-05-26）：简单粗暴，每出现1次，就加1
        :param chain_blocks: 链式字符块列表[位置，字符，词频，是否元数据]
        :param ngramDict: n元丁字型结构的字符块链表（数据库存储丁字型结构，用的时候加载）。
        :param NgramNum: 指定进行二元、三元关系计算的“元数”,计算到第n元关系，即对匹配出来的字符块链进行排序，目前使用邻接匹配法——ngram，
                          二元字符块（bigram）相当于有向图（为丁字形结构特例），三元字符块（trigram）及以上相当于丁字型结构的分解

        :return:
        """
        if not self.MemoryCentral:
            return False
        if not NgramNum:
            NgramNum = self.MemoryCentral.NgramNum
        try:
            return NgramEngine.loadNgramDictFromMetaNet(metaNetItem, self.MemoryCentral.NgramDict, NgramNum)
        except:
            raise

    def loadNgramDictByMetaChain(self, metaChain, NgramNum=2):
        """
        从元数据链加载NgramDic
        :param metaChain:
        :param ngramDict:
        :param gramNum:
        :return:
        """
        if not self.MemoryCentral:
            return False
        if not NgramNum:
            NgramNum = self.MemoryCentral.NgramNum
        try:
            return NgramEngine.loadNgramDictByMetaChain(metaChain, self.MemoryCentral.NgramDict, NgramNum)
        except:
            raise

    pass  # class MetaNetEngine(object):


class TextEngine(EngineBase):
    """
    文本处理引擎
    :rawParam
    构造函数参数说明
    :attribute
    对象属性说明
    """

    def __init__(self, memory):
        """
        文本处理引擎
        :param memory: 用来存放当前对象的内存空间（避免每次都从数据库中调用）
                       当前TextEngine的memory是MemoryCentral
        """
        super(TextEngine, self).__init__(memory)

        self._allMetaFromDBLoaded = False  # 是否已加载数据库元数据的标记

    def loadAllMetaFromDB(self, forceToReload=False):
        """
        从数据库加载所有的元数据。
        同时建立MetaDataIdDict、MetaDataValueDict、WordFrequncyDict、ChainCharMetaDict
        :param forceToReload: 是否强制重新加载一次
        :return:
        """
        if self._allMetaFromDBLoaded and not forceToReload:
            return

        try:
            import uuid
            _uuid = str(uuid.uuid1())
            logger.info("开始加载数据库元数据", timeStartMark=_uuid)
            allMetasInDB = MetaData.getAllInDB(memory=self.MemoryCentral)
            if not allMetasInDB:
                self._allMetaFromDBLoaded = True
                logger.info("加载数据库元数据完毕，没有可用的元数据", timeEndMark=_uuid)
                return None
            self._allMetaFromDBLoaded = True
            logger.info("加载数据库元数据完毕", timeEndMark=_uuid)
        except Exception as e:
            logger.log(e)
            raise e

        return allMetasInDB

    def segmentWithStopMarks(self, rawInput):
        """
        取得根据标点符号分解出的句子。
        :rawParam rawInput:输入的字符串。
        :return:
        """
        return metaDataHelper.segmentWithStopMarks(rawInput, self.MemoryCentral.stopMarks, self.MemoryCentral.stopMarkLevel,
                                                   self.MemoryCentral.keepStopMark)

    def segmentWithNumbers(self, rawInput):
        """
        将输入字符串与数字分开
        :param rawInput:
        :return:
        """
        return metaDataHelper.segmentWithNumbers(rawInput)

    def segmentWithStopMarksAndNumbersAndEnglish(self, rawInput, splitWithSpace=False):
        """
        将输入字符串与标点符号、数字、英文分开
        :param rawInput:
        :return:
        """
        return metaDataHelper.segmentWithStopMarksAndNumbersAndEnglish(rawInput, self.MemoryCentral.stopMarks,
                                                                       self.MemoryCentral.stopMarkLevel,
                                                                       self.MemoryCentral.keepStopMark, splitWithSpace)

    #
    # def createSingleFrequancyDict(self,rawInputs):
    #     """
    #     根据输入的元字符串，创建单字-频率字典
    #     :param rawInputs:
    #     :param CachedSingleFrequancyDict:
    #     :return:_singleFrequancyDict,total_length
    #     """
    #     # 检查参数
    #     if rawInputs is None or len(rawInputs)==0:
    #         return
    #
    #     return metaDataHelper.__createSingleFrequancyDict(rawInputs,None) # 将现有的DoubleFrequancyDict传入，以便直接把结果记载其中。

    #
    # def mergeSingleFrequancyDict(self, singleFrequancyDict):
    #     """
    #     与现有SingleFrequancyDict合并
    #     :param singleFrequancyDict:
    #     :return:
    #     """
    #     # 检查参数
    #     if singleFrequancyDict is None or len(singleFrequancyDict)==0:
    #         return False
    #     for k,v in singleFrequancyDict.items():
    #         if k in self.SingleFrequancyDict:
    #             self.SingleFrequancyDict[k] += v
    #         else:
    #             self.SingleFrequancyDict[k]=v
    #     return True
    #

    def createDoubleFrequancyDict(self, rawInputs, unknowns_tolerate_dgree=1.0):
        """
        根据输入的元数据字符串，创建双字-频率字典（合并到self.DoubleFrequancyDict）（在调用前应使用segmentWithStopMarksAndNumbersAndEnglish进行处理，得到的是应该是中文串、数字串、英文串）
        :param rawInputs: 元输入字符串（List），形式为：[[元输入字符串,是否需要先学习]]
        :param unknowns_tolerate_dgree: 对陌生事物的容忍度，由女娲的性格进行控制
        :return: doubleFrequancyDict,total_length
        """
        doubleFrequancyDict, total_length = metaDataHelper.createDoubleFrequancyDict(
            rawInputs,
            unknowns_tolerate_dgree=unknowns_tolerate_dgree)  # ,self.DoubleFrequancyDict) # 不再将现有的DoubleFrequancyDict传入，以便计算单次输入提取的元数据。
        # 与现有双字-频率字典合并
        self.mergeDoubleFrequancyDict(doubleFrequancyDict)

        return doubleFrequancyDict, total_length

    def mergeDoubleFrequancyDict(self, doubleFrequancyDict):
        """
        与现有DoubleFrequancyDict合并
        计算公式为：（原频率+新频率）/2
        :param doubleFrequancyDict:
        :return:
        """
        # 检查参数
        if doubleFrequancyDict is None or len(doubleFrequancyDict) == 0:
            return False
        for word, freq in doubleFrequancyDict.items():
            if freq <= 0:  # 如果freq为0，或是小于0，过滤掉（避免掉频）
                continue
            old_freq = self.MemoryCentral.WorkingMemory.DoubleFrequancyDict.get(word)

            if old_freq:
                freq = (freq + old_freq) / 2

            self.MemoryCentral.WorkingMemory.DoubleFrequancyDict[word] = freq

        return True

    def extractRawMetaData(self, rawInputs, segment=False, splitWithStopMarksAndNumbersAndEnglish=True,
                           unknowns_tolerate_dgree=1.0):
        """
        根据元输入，从单双字-频率字典提取元词块（可能有多个）（传入self.WordFrequncyDict）
        规则：双字-频率字典根据阀值和元输入的位置，1、如果连续词块超过指定阀值，即将其进行拼接；2、如果备选词块在元输入中独立存在，也进行提取
        :rawParam rawInputs: 元输入，用以查找其关键字出现位置
        :return:1、WordFrequncyDict：最终取得的元数据，其格式为{元输入（字符串）:词频（平均值）}
             2、segmentedBlocks：最终取得的元数据匹配分割后的根据词频连接的输入字符串（字符块），格式为：
                {"北京举办新年音乐会真棒":[["北京举办新年",0,False],["音乐会",6,True],["真棒!",9,False]]}
                含义为：{输入字符串:[第n个分割后得到的字符串,起始位置,是否是元数据]}
        """
        # 在调用前应使用segmentWithStopMarksAndNumbersAndEnglish进行处理，得到的是应该是中文串、数字串、英文串
        if splitWithStopMarksAndNumbersAndEnglish:
            splits = []
            for rawinput in rawInputs:
                # 0、将输入字符串按标点符号、数字串、英文串进行分割
                cur_splits = metaDataHelper.segmentWithStopMarksAndNumbersAndEnglish(rawinput, self.MemoryCentral.stopMarks,
                                                                                     self.MemoryCentral.stopMarkLevel,
                                                                                     self.MemoryCentral.keepStopMark,
                                                                                     splitWithSpace=True)
                splits.extend(cur_splits)
        else:
            splits = rawInputs

        # 1、根据双字-频率字典提取元词块（可能有多个）（传入self.WordFrequncyDict）
        doubleFrequancyDict, length = self.createDoubleFrequancyDict(splits,
                                                                     unknowns_tolerate_dgree=unknowns_tolerate_dgree)
        if not doubleFrequancyDict:
            return None, None
        new_raw_metas, segmentedInputs = metaDataHelper.extractRawMetaData(splits,
                                                                           doubleFrequancyDict,
                                                                           self.MemoryCentral.Threshold_ContinuousBlocks,
                                                                           self.MemoryCentral.WorkingMemory.WordFrequncyDict,
                                                                           segment)

        if new_raw_metas:
            # 添加到新元数据字典中
            for new_raw_meta, new_freq in new_raw_metas.items():
                if new_freq <= 0:  # 如果freq为0，或是小于0，过滤掉（避免掉频）
                    continue
                _freq = self.MemoryCentral.WorkingMemory.WordFrequncyDict.get(new_raw_meta)
                if _freq:
                    self.MemoryCentral.WorkingMemory.NewLearnedRawMetas[new_raw_meta] = _freq
                else:
                    self.MemoryCentral.WorkingMemory.NewLearnedRawMetas[new_raw_meta] = new_freq

        return new_raw_metas, segmentedInputs

    def loadChainCharMetaDict(self, rawMetas):
        """
        加载字符链字典。
        将{元数据：词频}的字典，转换成以每个字符作为索引，[True/False,meta,frequncy,{...}]为值，建立一个字典。
        :param rawMetas:{元数据：词频}的字典
        :param CachedChainCharMetaDict:已经加载的ChainCharMetaDict字典（默认为工作记忆区（WorkingMemory）中的ChainCharMetaDict）
        :return:以每个字符作为索引，[True/False,meta,frequncy,{...}]为值的字典，含义为：
        [是否字符块末尾，元数据字符串，频率，{后续子串字典}]
        例如：
        ddd={
            u"中":[False,None,0.0,
                {u"央":[True,u"中央",5.4,{}],
                u"国":[True,u"中国",8.6,
                    {u"人":[True,u"中国人",6.2,
                        {u"好":[True,u"中国人好",3.2,{}],
                        u"民":[True,u"中国人民",5.2,
                            {u"解":[False,None,0.0,
                                {u"放":[False,None,0.0,
                                    {u"军":[True,u"中国人民解放军",6.2,{}]}]}],
                            u"法":[False,None,0.0,
                                {u"院":[True,u"中国人民法院",6.2,{}]}]}]}]}]}]}
        WordFrequncyDict={u"中国人民解放军":5.0,u"中国人民法院":5.0,u"中国人民":5.0,u"中国人好":5.0,u"中国人":5.0,u"中国":5.0,u"中央":5.0,}
        """
        return metaDataHelper.loadChainCharFrequncyMetaDict(rawMetas, self.MemoryCentral.PersistentMemory.ChainCharMetaDict)

    def segmentInputWithChainCharMetaDict(self,
                                          rawInput,
                                          maxMatch=False,
                                          shouldLearn=False,
                                          resegmentWithUnknowns=True,
                                          unknowns_tolerate_dgree=1.0):
        """
        根据元数据分割输入字符串（列表）-根据链接字符词典进行匹配（有两种：最长顺序匹配、全部最可能匹配）。
        分解的顺序为：
        一、处理段落（todo：可能会以词频的方式处理）
        二、按标点符号分解句子（todo：可能会以词频的方式处理）
        三、匹配及分解
            （一）最长顺序匹配
            （二）全部最可能匹配
            1、所有词的匹配
            2、删除不可能（按天然连接顺序）
            3、取得链表
            4、按可能性排序
        :param rawInput: 输入的字符串，metaInput必须是unicode编码，格式为：[输入待处理的字符串，是否需要先学习]
        :param maxMatch: 是否进行最大匹配。
        :param shouldLearn : 是否需要学习之（提取rawMetas）。以后学习未知词汇尽量在整篇文章的级别，否则会导致很多连句词出现
        :return:
        """
        # 检查参数
        if rawInput is None or rawInput == "" or rawInput == u"":
            return
        if not type(rawInput) is str:
            rawInput = str(rawInput)

        # elif type(rawInput) is types.ListType:
        #     if not type(rawInput) is str:
        #         raise AttributeError("参数错误，metaInput必须是字符串或格式为[输入待处理的字符串，是否需要先学习]")

        if shouldLearn == True:  # 如果需要学习，学习之。以后学习未知词汇尽量在整篇文章的级别，否则会导致很多连句词出现
            self.learnRawInputs([rawInput], unknowns_tolerate_dgree=unknowns_tolerate_dgree)

        return metaDataHelper.segmentInputWithChainCharMetaDict(rawInput,
                                                                self.MemoryCentral.PersistentMemory.ChainCharMetaDict,
                                                                self.MemoryCentral.stopMarks,
                                                                self.MemoryCentral.Threshold_ContinuousBlocks,
                                                                maxMatch,
                                                                self.MemoryCentral.stopMarkLevel,
                                                                self.MemoryCentral.keepStopMark,
                                                                self.MemoryCentral.PersistentMemory.NgramDict,
                                                                self.MemoryCentral.NgramNum,
                                                                resegmentWithUnknowns=resegmentWithUnknowns)

    def getCurMetaChainBySegmentResults(self, segmentResults, ngram=2):
        """
        [产生式]根据当前的分割的结果创建元数据链（由于分割结果可能有多个，所以在处理时一条条调用，直到“理解”为止）
        :param segmentResults:
        :param ngram:
        :return:
        """

        if segmentResults is None or not isinstance(segmentResults, SegmentedResults):
            return

        for segmentResult in segmentResults:
            # 重置索引，以便从0开始
            segmentResult.restoreResultIndex()
            yield self.getCurMetaChainBySegmentResult(segmentResult, ngram)
            # 重置索引，以便从0开始
            segmentResult.restoreResultIndex()

    def getCurMetaChainBySegmentResult(self, segmentResult, ngram=2):
        """
        根据当前的分割的结果创建元数据链（由于分割结果可能有多个，所以在处理时一条条调用，直到“理解”为止）
        :param segmentResult:
        :return:
        """
        return metaDataHelper.getCurMetaChainBySegmentResult(segmentResult, ngram,self.MemoryCentral)

    def retrieveMetaByMvalue(self, mvalue):
        """
        根据元数据的值取得元数据
        :param mvalue:
        :return:
        """
        result = self.MemoryCentral.getMetaByMvalueInMemory(mvalue)  # 首先从内存中取
        if result:  # 取到了，直接返回
            return result
        # 从数据库中取
        result = MetaData(mvalue=mvalue, memory=self.MemoryCentral).getByColumnsInDB()
        return result

    def segmentInputsWithChainCharMetaDict(self, rawInputs, maxMatch=False, shouldLearn=True,
                                           unknowns_tolerate_dgree=1.0):
        """
        根据元数据分割输入字符串（列表）-根据链接字符词典进行匹配（有两种：最长顺序匹配、全部最可能匹配）。
        分解的顺序为：
        一、处理段落（todo：可能会以词频的方式处理）
        二、按标点符号分解句子（todo：可能会以词频的方式处理）
        三、匹配及分解
            （一）最长顺序匹配
            （二）全部最可能匹配（目前最佳方案）
            1、所有词的匹配
            2、删除不可能（按天然连接顺序）
            3、取得链表
            4、按可能性排序
        :param rawInputs: 输入的字符串，metaInput必须是unicode编码，格式为：[输入待处理的字符串，是否需要先学习]
        :param maxMatch: 是否进行最大匹配。
        :param shouldLearn : 是否需要学习之（提取rawMetas）。
        :return:
        """
        # 检查参数
        if rawInputs is None or not isinstance(rawInputs, list) or len(rawInputs) == 0:
            return

        if shouldLearn == True:  # 如果需要学习，学习之
            self.learnRawInputs(rawInputs, unknowns_tolerate_dgree=unknowns_tolerate_dgree)

        return metaDataHelper.segmentInputsWithChainCharMetaDict(rawInputs,
                                                                 self.MemoryCentral.PersistentMemory.ChainCharMetaDict,
                                                                 self.MemoryCentral.stopMarks,
                                                                 self.MemoryCentral.Threshold_ContinuousBlocks,
                                                                 maxMatch,
                                                                 self.MemoryCentral.stopMarkLevel,
                                                                 self.MemoryCentral.keepStopMark,
                                                                 self.MemoryCentral.PersistentMemory.NgramDict,
                                                                 self.MemoryCentral.NgramNum)

    # def loadFirstCharMetaDict(self,relatedMetas):
    #     """
    #     [弃用]
    #     将{元数据：词频}的字典，转换成以首字符作为索引，所有元数据（按长度倒序排列）的列表为值，建立一个字典或将其添加到CachedFirstCharMetaDict。
    #     :rawParam WordFrequncyDict:{元数据：词频}的字典
    #     :return:以首字符作为索引，所有元数据（按长度倒序排列）的列表为值，建立的字典
    #     """
    #
    #     return textHelper.loadFirstCharMetaDict(relatedMetas,self.FirstCharMetaDict)
    #
    #
    # def segmentInputWithFirstCharMetaDict(self,metaInput,maxMatch=True,learn=True):
    #     """
    #     [弃用]
    #     根据元数据分割输入字符串。
    #     :rawParam metaInput:输入字符串。metaInput必须是unicode编码
    #     :param learn:是否需要先学习
    #     :return:
    #     """
    #
    #     if learn:
    #         relatedMetas, segmentedBlocks = self.extractRawMetaData([metaInput])
    #         self.loadFirstCharMetaDict(relatedMetas)
    #     return textHelper.segmentInputWithFirstCharMetaDict(metaInput,self.FirstCharMetaDict,maxMatch)

    def segmentArticles(self, path, shouldLearn=True, suffix="txt", shouldLog=True):
        """
        分割一个目录下的所有文章（.txt文件）
        :param path:
        :return:
        """

        segments = ArticlesSegmentResults()

        unsegmented = []

        file_lines_dict = None

        # 先学习一遍
        if shouldLearn:  # 如果需要学习，学习之
            file_lines_dict, file_raw_metas_dict = self.learnFiles(path)

        if file_lines_dict and len(file_lines_dict) > 0:  # 如果已经读取过了，直接分割字符串，反之，读取并分割
            i = 0
            for filename, lines in file_lines_dict.items():
                if shouldLog:
                    logger.info("——segmenting No." + str(i) + " file:" + filename, timeStartMark=filename)
                i += 1
                cur_segments = self.segmentInputsWithChainCharMetaDict(lines, maxMatch=self.MemoryCentral.maxMatch,
                                                                       shouldLearn=False)  # 已经学习过了
                if cur_segments and len(cur_segments):
                    cur_segment_article = ArticleSegmentResult(filename)
                    cur_segment_article.segmentedResults = cur_segments
                    segments[filename] = cur_segment_article
                else:
                    logger.warning("文件未能有效分解：" + filename)
                    unsegmented.append(filename)
                if shouldLog:
                    logger.info("——segmented No." + str(i) + " file:" + filename, timeEndMark=filename)
        else:
            from loongtian.util.helper import fileHelper
            files = fileHelper.getFilesInPath(path, None, suffix, None)
            i = 0
            for filename in files:
                if shouldLog:
                    logger.info("——segmenting No." + str(i) + " file:" + filename, timeStartMark=filename)
                i += 1
                cur_segments = self.segmentArticle(filename, shouldLearn=False, shouldLog=False)  # 已经学习过了

                if cur_segments and cur_segments.segmentedResults and len(cur_segments.segmentedResults):
                    segments[filename] = cur_segments
                else:
                    logger.warning("文件未能有效分解：" + filename)
                    unsegmented.append(filename)
                if shouldLog:
                    logger.info("——segmented No." + str(i) + " file:" + filename, timeEndMark=filename)

        return segments, unsegmented

    def segmentArticle(self, filename, shouldLearn=True, shouldLog=True):
        """
        分割一篇文章
        :param filename:
        :return:
        """
        articleSegmentResult = ArticleSegmentResult(filename)
        if not isinstance(filename, str) or not filename.endswith(u".txt"):
            return None

        from loongtian.util.helper import fileHelper

        lines = fileHelper.readLines(filename)
        if shouldLog:
            logger.info("——segmenting file:" + filename, timeStartMark=filename)
        segments = self.segmentInputsWithChainCharMetaDict(lines, maxMatch=self.MemoryCentral.maxMatch,
                                                           shouldLearn=shouldLearn)
        articleSegmentResult.segmentedResults = segments
        if shouldLog:
            logger.info("——segmented file:" + filename, timeEndMark=filename)
        return articleSegmentResult

    def learnFiles(self, path, suffix="txt", shouldLog=True,unknowns_tolerate_dgree =1.0):
        """
        学习文件中的数据，提取出
        :param path:
        :param suffix:
        :param shouldLog:
        :return:
        """
        from loongtian.util.helper import fileHelper

        files = fileHelper.getFilesInPath(path, None, suffix, None)
        if not files:
            raise Exception("当前路径下没有文档，请检查后再次运行程序！")
        file_lines_dict = {}
        file_raw_metas_dict = {}

        i = 0
        for file in files:
            if shouldLog:
                logger.info("——learning No." + str(i) + " file:" + file, timeStartMark=file)
            i += 1
            self.learnFile(file, shouldLog=False, file_lines_dict=file_lines_dict,
                           file_raw_metas_dict=file_raw_metas_dict,unknowns_tolerate_dgree =unknowns_tolerate_dgree)

            if shouldLog:
                logger.info("——learned No." + str(i) + " file:" + file, timeEndMark=file)

        return file_lines_dict, file_raw_metas_dict

    def learnFile(self, filename, shouldLog=True, file_lines_dict=None, file_raw_metas_dict=None,
                  unknowns_tolerate_dgree=1.0):
        """
        学习文件中的数据，提取出
        :param filename:
        :param shouldLog:
        :return:
        """
        from loongtian.util.helper import fileHelper

        if shouldLog:
            logger.info("——learning file:" + filename, timeStartMark=filename)

        if file_lines_dict is None or not isinstance(file_lines_dict, dict):
            file_lines_dict = {}
        if file_raw_metas_dict is None or not isinstance(file_raw_metas_dict, dict):
            file_raw_metas_dict = {}
        lines = fileHelper.readLines(filename)

        raw_metas, segmentedInputs = self.learnRawInputs(lines, unknowns_tolerate_dgree=unknowns_tolerate_dgree)
        if raw_metas:
            file_lines_dict[filename] = lines
            file_raw_metas_dict[filename] = raw_metas
            if __debug__:
                print (u"我学到了：", raw_metas)

        if shouldLog:
            logger.info("——learned file:" + filename, timeEndMark=filename)

        return file_lines_dict, file_raw_metas_dict

    def learnRawInputs(self, rawInputs, splitWithStopMarksAndNumbersAndEnglish=True, unknowns_tolerate_dgree=1.0):
        """
        学习元输入的字符串
        :param rawInputs:
        :return:
        """
        raw_metas, segmentedInputs = self.extractRawMetaData(rawInputs, False, splitWithStopMarksAndNumbersAndEnglish,
                                                             unknowns_tolerate_dgree=unknowns_tolerate_dgree)
        if raw_metas:
            self.loadChainCharMetaDict(raw_metas)
        return raw_metas, segmentedInputs

    def updateNewLearnedMetaData(self):
        """
        将新学习到的元数据创建（更新）到数据库中
        :return:
        """
        for new_raw_meta, weight in self.MemoryCentral.WorkingMemory.NewLearnedRawMetas.items():
            new_meta = MetaData(mvalue=new_raw_meta, weight=weight, memory=self.MemoryCentral).create()
            # self.MemoryCentral.addMetaInMemory(new_meta) # 已经添加过了

    def updatAllMetaData(self, **attributeValues):
        """
        将所有记忆中的的元数据创建（更新）到数据库中
        :return:
        """
        for id,meta in self.MemoryCentral.PersistentMemory.MetaDataIdDict.items():
            if attributeValues:
                meta.updateAttributeValues(**attributeValues)
            else:
                meta.update()
        for id,meta in self.MemoryCentral.WorkingMemory.MetaDataIdDict.items():
            if attributeValues:
                meta.updateAttributeValues(**attributeValues)
            else:
                meta.update()
