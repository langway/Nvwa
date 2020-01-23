#!/usr/bin/env python
# -*- coding: utf-8 -*-


from unittest import TestCase
from loongtian.nvwa.organs.brain import Brain
from loongtian.nvwa.organs.character import Character
from loongtian.nvwa.centrals.memoryCentral import MemoryCentral

from loongtian.util.helper import stringHelper
from loongtian.nvwa.models.metaData import MetaData
from loongtian.nvwa.models.metaNet import MetaNet
from test import settings
import datetime

__author__ = 'Leon'


class TestTextEngine(TestCase):
    def setUp(self):
        print("----setUp----")

        self.brain = Brain()
        self.MemoryCentral = self.brain.MemoryCentral
        self.TextEngine = self.MemoryCentral.TextEngine

        self.path = settings.file_path
        self.eng_path = settings.eng_path

        self.RawInputs = [
            "北京举办2008新年音乐会真棒！",
            "音乐很动听",
            "新年音乐会中的音乐很动听",
            "5月2日音乐会非常成功，音乐让很多人沉醉！",
            "音乐会陶冶情操！",
            "音乐会有很多音乐。",
        ]

        self.MetaInputs = ["我非常爱红苹果",
                           "我非常爱吃红苹果",
                           "红苹果我非常爱",
                           "红苹果我非常爱吃",
                           "我非常爱吃香蕉",
                           "我非常爱咬一大口苹果"]
        self.RawMetas = {  # 自定义一个词典，有干扰因素
            "中": 2.3, "中国人民法院": 5.5, "中国人民解放军": 7.5, "中国人民": 7.0, "中国人好": 5.0, "中国人": 8.5, "中国": 9.8, "中央": 8.0,
            "国人": 4.0, "国家": 7.2, "国际": 7.4,
            "人人为我": 3.2, "人均收入": 5.7, "人民": 8.1, "人类": 8.9, "人民法院": 4.3, "人均": 7.7,
            "民主": 8.8, "民法": 6.3, "民生": 5.7, "民法院": 3.2,
            "法律文本": 5.6, "法官": 7.9, "法院": 8.7, "法律": 9.2, "法学": 4.3, "法权": 2.5,
            "有": 9.4, "有司": 2.4, "有钱人": 8.4, "有钱": 9.6, "有病": 9.3,  # "有":9.9,
            "司法权": 6.4, "司机": 9.1, "司法": 8.5,
            "权利": 7.8, "权力": 8.9, "权谋": 7.6,
            "软件": 9.7, "软弱": 8.7, "软蛋": 7.1,

        }
        self.inputs_with_stopmarks = [
            "!",
            "啊！",
            "a!",
            ".。中国人民法院有司法权，中央强调坚决依法治国！\r\n我们希望中国成为法治国家...？；"
        ]
        self.mini_inputs = ["音乐会很好",
                            "音乐很好听",
                            "北京音乐会"
                            ]

        self.inputs_with_number = ["5月2日",
                                   "身份证号210103197607293635是吉祥数字",
                                   "1年天数365天",
                                   "在长达13年的学习生涯中学习了技能总数13",
                                   "6 june有24小时"]

        # 带分词歧义
        self.inputs_with_ambiguity = ["中",  # 0-测试单字分词
                                      "我",  # 1-测试未识别单字
                                      "中国",  # 2-测试单词
                                      "我们",  # 3-测试未识别单词
                                      "中国人民",  # 4-测试分支分词：中国人民，中国-人民，中国人-民
                                      "有司法权",  # 5-测试分支分词：有司-法权，有-司法权，有-司法-权
                                      "中国人懂法",  # 6-测试一半的词
                                      "中国人民法院有司法权中央",  # 7-
                                      "有司法权中央美",  # 8-测试未识别词
                                      "  中国人民法院系红旗有司法权中央",  # 9-测试未识别词
                                      ]

        self.inputs_with_mix = ["6 june有24小时,数字8.96",
                                "\"21th Century will be the century of China!\"，这句话的意思是：“21世纪将是属于中国的世纪！"]

        self.inputs_full_english = "Do you know what kind of animal I like most? " \
                                   "It’s monkey. Monkey is a kind of lovely animal. " \
                                   "Many people like monkeys very much. Generally, " \
                                   "monkey has small body covered with fur. " \
                                   "Some kinds of monkeys have two big eyes and ears and a long tail. " \
                                   "I can see them on TV or the zoo. Every time I go to the zoo, " \
                                   "I will go to see them. " \
                                   "Monkeys often stay in trees and jump between them. " \
                                   "They are so lively and favorable. " \
                                   "When they are happy, they will act for visitors. It’s very funny."

    def testSegmentWithStopMarks(self):
        """
        实验以标点符号分解字符块。
        :return:
        """
        print("----testSegmentWithStopMarks----")
        result1 = self.TextEngine.segmentWithStopMarks(self.inputs_with_stopmarks[0])
        print(result1)

        result2 = self.TextEngine.segmentWithStopMarks(self.inputs_with_stopmarks[1])
        print(result2)

        result3 = self.TextEngine.segmentWithStopMarks(self.inputs_with_stopmarks[2])
        print(result3)

        result4 = self.TextEngine.segmentWithStopMarks(self.inputs_with_stopmarks[3])
        print(result4)

    def testSegmentWithNumber(self):

        print("----testSegmentWithNumber----")
        result1 = self.TextEngine.segmentWithNumbers(self.inputs_with_number[0])
        print(result1)

        result2 = self.TextEngine.segmentWithNumbers(self.inputs_with_number[1])
        print(result2)

        result3 = self.TextEngine.segmentWithNumbers(self.inputs_with_number[2])
        print(result3)

        result4 = self.TextEngine.segmentWithNumbers(self.inputs_with_number[3])
        print(result4)

        result5 = self.TextEngine.segmentWithNumbers(self.inputs_with_number[4])
        print(result5)

    def testSegmentWithStopMarksAndNumbersAndEnglish(self):
        print("——testSegmentWithStopMarksAndNumbersAndEnglish——")

        segmentedResult1 = self.TextEngine.segmentWithStopMarksAndNumbersAndEnglish(self.inputs_with_mix[0])
        print("segmentedResult length::", len(segmentedResult1))

        segmentedResult2 = self.TextEngine.segmentWithStopMarksAndNumbersAndEnglish(self.inputs_with_mix[1])
        print("segmentedResult length::", len(segmentedResult2))

        result1 = self.TextEngine.segmentWithStopMarksAndNumbersAndEnglish(self.inputs_with_number[0])
        print(result1)

        result2 = self.TextEngine.segmentWithStopMarksAndNumbersAndEnglish(self.inputs_with_number[1])
        print(result2)

        result3 = self.TextEngine.segmentWithStopMarksAndNumbersAndEnglish(self.inputs_with_number[2])
        print(result3)

        result4 = self.TextEngine.segmentWithStopMarksAndNumbersAndEnglish(self.inputs_with_number[3])
        print(result4)

        result5 = self.TextEngine.segmentWithStopMarksAndNumbersAndEnglish(self.inputs_with_number[4])
        print(result5)

    def testCreateDoubleFrequancyDict(self):
        """
        测试创建元输入双字-频率字典
        :return:
        """
        print("----testCreateDoubleFrequancyDict----")
        # 多输入
        doubleFrequancyDict1, length = self.TextEngine.createWordDoubleFrequancyDict(self.RawInputs,
                                                                                     filters=[stringHelper.is_chinese])
        print(doubleFrequancyDict1)

        # 同样的话又说了一遍（带分隔符，因为两次输入一样，其词频不应发生变化）
        doubleFrequancyDict2, length = self.TextEngine.createWordDoubleFrequancyDict(self.RawInputs,
                                                                                     filters=[stringHelper.is_chinese],
                                                                                     key_connector="_")
        print(doubleFrequancyDict2)

        # 没有filters
        doubleFrequancyDict3, length = self.TextEngine.createWordDoubleFrequancyDict(self.RawInputs)
        print(doubleFrequancyDict3)

        # 单输入，带标点
        doubleFrequancyDict4, length = self.TextEngine.createWordDoubleFrequancyDict([self.inputs_with_stopmarks[3]],
                                                                                     filters=[stringHelper.is_chinese])
        print(doubleFrequancyDict4)

        # 英文输入
        doubleFrequancyDict5, length = self.TextEngine.createWordDoubleFrequancyDict([self.inputs_full_english],
                                                                                     filters=[stringHelper.is_chinese])
        print(doubleFrequancyDict5)

        # 没有filters
        doubleFrequancyDict6, length = self.TextEngine.createWordDoubleFrequancyDict([self.inputs_full_english])
        print(doubleFrequancyDict6)

    def testExtractRawMetaData(self):
        """
        测试根据元输入，从双字-频率字典提取元词块（可能有多个）（传入self.WordFrequncyDict）
        :return:
        """
        print("----testExtractRawMetaData----")

        raw_metas1 = self.TextEngine.extractRawMetaData(self.RawInputs, filters=[stringHelper.is_chinese])
        print(raw_metas1)

        # 同样的话又提取了一遍，还应是原来的结果！
        raw_metas2 = self.TextEngine.extractRawMetaData(self.RawInputs, filters=[stringHelper.is_chinese])
        print(raw_metas2)

        raw_metas3 = self.TextEngine.extractRawMetaData([self.inputs_full_english], filters=[stringHelper.is_chinese])
        print(raw_metas3)

    def testLoadChainCharMetaDict(self):
        """
        测试以元数据：词频}的字典加载{首字母：元数据列表}字符链字典
        :return:
        """
        print("----testLoadChainCharMetaDict----")
        # mini_inputs=["中国人民法院有司法权中央","中"]
        self.MemoryCentral.Threshold_ContinuousBlocks = 0.03
        raw_metas = self.TextEngine.extractRawMetaData(self.RawInputs)
        print(raw_metas)

        chainChar_MetaDict = self.TextEngine.loadChainCharMetaDict(raw_metas)

        print(chainChar_MetaDict)

        print(self.RawMetas)

        chainChar_MetaDict = self.TextEngine.loadChainCharMetaDict(self.RawMetas)

        print(chainChar_MetaDict)

    def testLoadAllMetaFromDB(self):
        print("——testLoadAllMetaFromDB——")

        allMetasInDB = self.MemoryCentral.loadAllMetaFromDB()
        self.assertEqual(len(self.MemoryCentral.PersistentMemory.WordFrequncyDict), len(allMetasInDB))

        # self.TextEngine.updatAllMetaData()

    def testSegmentInputByChainCharMetaDict(self):
        """
        测试全部最可能匹配进行分割输入字符串
        :return:
        """
        print("----testSegmentInputByChainCharMetaDict----")
        chainChar_MetaDict = self.TextEngine.loadChainCharMetaDict(self.RawMetas)
        print(chainChar_MetaDict)

        # # 加载字典
        # chainCharMetaDict = self.TextEngine.loadChainCharFrequncyMetaDict(self.WordFrequncyDict)
        #
        # print(chainCharMetaDict)

        self.MemoryCentral.loadAllMetaFromDB()

        # 实验多字符的分词
        #  分解"音乐会很好"，应该有下面两条结果：
        # [
        # [["音乐会",0,True],["很好",3,False]]
        # [["音乐",0,True],["会",2,False],["很好",3,False]]
        # ]
        # 每条记录的格式应为：[[word,i,True/False]]其含义为：[匹配到的单词，位置,是否元数据]的列表

        # 0-测试单字 , "中"
        inputSegments0 = self.TextEngine.segmentInputWithChainCharMetaDict(self.inputs_with_ambiguity[
                                                                               0])  # ,chainCharMetaDict,self.TextWorkingMemory.NgramDict,self.Brain.Character.GramNum,self.TextWorkingMemory.StopMarks)
        print(inputSegments0)

        # 1-测试未识别单字, "我"
        inputSegments1 = self.TextEngine.segmentInputWithChainCharMetaDict(self.inputs_with_ambiguity[
                                                                               1])  # ,chainCharMetaDict,self.TextWorkingMemory.NgramDict,self.Brain.Character.GramNum,self.TextWorkingMemory.StopMarks)
        print(inputSegments1)

        # 2-测试单词, "中国"
        inputSegments2 = self.TextEngine.segmentInputWithChainCharMetaDict(self.inputs_with_ambiguity[2])
        print(inputSegments2)

        # 3-测试未识别单词, "我们"
        inputSegments3 = self.TextEngine.segmentInputWithChainCharMetaDict(self.inputs_with_ambiguity[3])
        print(inputSegments3)

        # 4-测试分支分词：中国人民，中国-人民，中国人-民，中-国-人民，中-国人-民，"中国人民"
        inputSegments4 = self.TextEngine.segmentInputWithChainCharMetaDict(self.inputs_with_ambiguity[4])
        print(inputSegments4)

        # 5-测试分支分词：有司-法权，有-司法权，有-司法-权 , "有司法权",
        inputSegments5 = self.TextEngine.segmentInputWithChainCharMetaDict(self.inputs_with_ambiguity[5])
        print(inputSegments5)

        # 6-测试一半的词, "中国人懂法"
        inputSegments6 = self.TextEngine.segmentInputWithChainCharMetaDict(self.inputs_with_ambiguity[6])
        print(inputSegments6)

        # 7-中国人民法院有司法权中央
        inputSegments7 = self.TextEngine.segmentInputWithChainCharMetaDict(self.inputs_with_ambiguity[7])
        print(inputSegments7)

        # 8-测试未识别词u'有司法权中央美'
        inputSegments8 = self.TextEngine.segmentInputWithChainCharMetaDict(self.inputs_with_ambiguity[8])
        print(inputSegments8)

        # 9-测试未识别词 中国人民法院系红旗有司法权中央
        inputSegments9 = self.TextEngine.segmentInputWithChainCharMetaDict(
            self.inputs_with_ambiguity[9])  # ,maxMatch = True)
        print(inputSegments9)

        segmentedResult10 = self.TextEngine.segmentInputWithChainCharMetaDict("属于宣武区的编号J040800495的一位姓高的申请人")
        print(segmentedResult10)

        segmentedResult11 = self.TextEngine.segmentInputWithChainCharMetaDict("记者杜金明通讯员惠民")
        print(segmentedResult11)

        segmentedResult12 = self.TextEngine.segmentInputWithChainCharMetaDict("2018年6月9日")
        print(segmentedResult12)

        # "6 june有24小时"
        segmentedResult13 = self.TextEngine.segmentInputWithChainCharMetaDict(self.inputs_with_mix[0])
        print(segmentedResult13)

        # "21th Century will be the century of China!"，这句话的意思是：“21世纪将是属于中国的世纪！"
        segmentedResult14 = self.TextEngine.segmentInputWithChainCharMetaDict(self.inputs_with_mix[1])
        print(segmentedResult14)

        segmentedResult15 = self.TextEngine.segmentInputWithChainCharMetaDict(self.inputs_full_english)
        print(segmentedResult15)

    def testCreateArticle(self):

        # 测试单词
        s = "女娲"
        article = self.TextEngine.createArticle(s)
        real_content = article.getRealContent()
        print(s)

        # 测试单行单句
        s = "1年天数365天。"
        article = self.TextEngine.createArticle(s)
        real_content = article.getRealContent()
        print(s)

        # 测试单行多句
        s = "小明说：“1年天数365天”。6 june有24小时,数字8.96。"
        article = self.TextEngine.createArticle(s)
        real_content = article.getRealContent()
        print(s)

        # 测试复杂段落
        from test import settings
        file_path = settings.file_path + "经适房公示人员身份证号为18个“1”遭质疑.txt"
        s = None
        with open(file_path) as f:
            s = f.read()
        if s:
            article = self.TextEngine.createArticle(s)
            real_content = article.getRealContent()
            print(s)

        file_path = settings.eng_path + "My Favorite Animal.txt"
        s = None
        with open(file_path) as f:
            s = f.read()
        if s:
            article = self.TextEngine.createArticle(s)
            real_content = article.getRealContent()
            print(s)

        file_path = settings.eng_path + "SAFE spokesperson China will keep bolstering the foreign exchange regime.txt"
        s = None
        with open(file_path) as f:
            s = f.read()
        if s:
            article = self.TextEngine.createArticle(s)
            real_content = article.getRealContent()
            print(s)



    def testSegment(self):

        self.MemoryCentral.loadAllMetaFromDB()

        # 测试单词
        s = "女娲"
        segment_result = self.TextEngine.segment(s)
        print("string:",s)
        print("segment_result type:",type(segment_result))
        firstInShortPhrase = segment_result.getFirstInShortPhrase()
        print("firstInShortPhrase:",firstInShortPhrase.containedObj)

        s = "女娲伏羲水穆仞"
        segment_result = self.TextEngine.segment(s)
        print("string:", s)
        print("segment_result type:", type(segment_result))
        firstInShortPhrase = segment_result.getFirstInShortPhrase()
        print("firstInShortPhrase:", firstInShortPhrase.containedObj)

        # 测试单行单句
        s = "1年天数365天"
        segment_result = self.TextEngine.segment(s)
        print("string:", s)
        print("segment_result type:", type(segment_result))
        firstInShortPhrase = segment_result.getFirstInShortPhrase()
        print("firstInShortPhrase:", firstInShortPhrase.containedObj)

        # 测试单行单句
        s = "1年天数365天。"
        segment_result = self.TextEngine.segment(s)
        print("string:", s)
        print("segment_result type:", type(segment_result))
        firstInShortPhrase = segment_result.getFirstInShortPhrase()
        print("firstInShortPhrase:", firstInShortPhrase.containedObj)

        # 测试单行多句
        s = "小明说：“1年天数365天”。6 june有24小时,数字8.96。"
        segment_result = self.TextEngine.segment(s)
        print("string:", s)
        print("segment_result type:", type(segment_result))
        firstInShortPhrase = segment_result.getFirstInShortPhrase()
        print("firstInShortPhrase:", firstInShortPhrase.containedObj)

        s = "China\'s "
        segment_result = self.TextEngine.segment(s)
        print("string:", s)
        print("segment_result type:", type(segment_result))
        firstInShortPhrase = segment_result.getFirstInShortPhrase()
        print("firstInShortPhrase:", firstInShortPhrase.containedObj)

        s = "China\'s foreign exchange reserves rose to a six-month high of nearly $3.11 trillion by the end of December"
        segment_result = self.TextEngine.segment(s)
        print("string:", s)
        print("segment_result type:", type(segment_result))
        firstInShortPhrase = segment_result.getFirstInShortPhrase()
        print("firstInShortPhrase:", firstInShortPhrase.containedObj)

        # 测试复杂段落
        from test import settings
        file_path = settings.file_path + "经适房公示人员身份证号为18个“1”遭质疑.txt"
        s = None
        with open(file_path) as f:
            s = f.read()
        if s:
            segment_result = self.TextEngine.segment(s)
            print("string:", s)
            print("segment_result type:", type(segment_result))
            firstInShortPhrase = segment_result.getFirstInShortPhrase()
            print("firstInShortPhrase:", firstInShortPhrase.containedObj)
            while firstInShortPhrase:
                print("next InShortPhrase:", firstInShortPhrase.containedObj)
                firstInShortPhrase =firstInShortPhrase.getNext()


        file_path = settings.eng_path + "My Favorite Animal.txt"
        s = None
        with open(file_path) as f:
            s = f.read()
        if s:
            segment_result = self.TextEngine.segment(s)
            print("string:", s)
            print("segment_result type:", type(segment_result))
            firstInShortPhrase = segment_result.getFirstInShortPhrase()
            print("firstInShortPhrase:", firstInShortPhrase.containedObj)

        file_path = settings.eng_path + "SAFE spokesperson China will keep bolstering the foreign exchange regime.txt"
        s = None
        with open(file_path) as f:
            s = f.read()
        if s:
            segment_result = self.TextEngine.segment(s)
            print("string:", s)
            print("segment_result type:", type(segment_result))
            firstInShortPhrase = segment_result.getFirstInShortPhrase()
            print("firstInShortPhrase:", firstInShortPhrase.containedObj)



    def testLearnFiles(self):
        print("——testLearnFiles——")

        file_lines_dict, file_raw_metas_dict = self.TextEngine.learnFiles(self.path,
                                                                          unknowns_tolerate_dgree=Character.Unknowns_Tolerate_Dgree)
        print("self.TextEngine.WordFrequncyDict Length:", len(self.MemoryCentral.WorkingMemory.NewLearnedRawMetas))

    def testUpdatAllMetaData(self):

        self.MemoryCentral.loadAllMetaFromDB()

        print("——testUpdatAllMetaData——")
        self.TextEngine.updatAllMetaData(recognized=True, createtime=str(datetime.datetime.now()))

    def testSegmentFile(self):
        print("——testSegmentArticle——")

        self.MemoryCentral.loadAllMetaFromDB()
        # niu = self.MemoryCentral.PersistentMemory.ChainCharMetaDict.get("身")
        #
        file = self.path + "乡村女教师背着残疾女儿求学十余年(图).txt"
        segmentedResult = self.TextEngine.segmentFile(file, shouldLearn=False)
        print(segmentedResult)
        # 首先学习

        # print("self.TextEngine.WordFrequncyDict Length:",len(self.TextEngine.WordFrequncyDict))
        file = self.path + "经适房公示人员身份证号为18个“1”遭质疑.txt"
        # self.TextEngine.learnFile(file)
        # self.TextEngine.updateNewLearnedMetaData()
        segmentedResult = self.TextEngine.segmentFile(file, shouldLearn=True)
        # self.TextEngine.updateNewLearnedMetaData()
        print(segmentedResult)

        file = self.path + "男子非法吸收公众存款1.91亿获刑5年.txt"
        segmentedResult = self.TextEngine.segmentFile(file, shouldLearn=False)
        print(segmentedResult)

    def testGetMetaChainBySegmentResult(self):
        print("----testGetMetaChainBySegmentResult----")

        meta_niu = MetaData(mvalue="牛", memory=self.MemoryCentral).create()
        meta_you = MetaData(mvalue="有", memory=self.MemoryCentral).create()
        meta_tui = MetaData(mvalue="腿", memory=self.MemoryCentral).create()
        meta_wo = MetaData(mvalue="我", memory=self.MemoryCentral).create()
        meta_zhidao = MetaData(mvalue="知道", memory=self.MemoryCentral).create()

        self.MemoryCentral.addMetasInMemory([meta_niu, meta_you, meta_tui, meta_wo, meta_zhidao])
        segment1 = self.TextEngine.segmentInputWithChainCharMetaDict("牛有腿",
                                                                     unknowns_tolerate_dgree=Character.Unknowns_Tolerate_Dgree)
        print(segment1)
        rawInput, meta_chain1, unknown_metas_index = self.TextEngine.getCurMetaChainBySegmentResult(segment1)
        print(meta_chain1)

        segment2 = self.TextEngine.segmentInputWithChainCharMetaDict("我知道牛有腿",
                                                                     unknowns_tolerate_dgree=Character.Unknowns_Tolerate_Dgree)
        print(segment2)
        rawInput, meta_chain2, unknown_metas_index = self.TextEngine.getCurMetaChainBySegmentResult(segment2)
        print(meta_chain2)

    def testLoadNgramDict(self):
        print("----testLoadNgramDict----")

        meta_niu = MetaData(mvalue="牛", memory=self.MemoryCentral).create()
        meta_you = MetaData(mvalue="有", memory=self.MemoryCentral).create()
        meta_tui = MetaData(mvalue="腿", memory=self.MemoryCentral).create()
        meta_diqiu = MetaData(mvalue="地球", memory=self.MemoryCentral).create()
        meta_shi = MetaData(mvalue="是", memory=self.MemoryCentral).create()
        meta_yuande = MetaData(mvalue="圆的", memory=self.MemoryCentral).create()
        meta_wo = MetaData(mvalue="我", memory=self.MemoryCentral).create()
        meta_zhidao = MetaData(mvalue="知道", memory=self.MemoryCentral).create()

        self.MemoryCentral.addMetasInMemory(
            [meta_niu, meta_you, meta_tui, meta_wo, meta_zhidao, meta_diqiu, meta_shi, meta_yuande])
        segment1 = self.TextEngine.segmentInputWithChainCharMetaDict("牛有腿")
        print(segment1)
        rawInput, meta_chain1, unknown_metas_index = self.TextEngine.getCurMetaChainBySegmentResult(segment1)
        print(meta_chain1)

        segment2 = self.TextEngine.segmentInputWithChainCharMetaDict("我知道牛有腿")
        print(segment2)
        rawInput, meta_chain2, unknown_metas_index = self.TextEngine.getCurMetaChainBySegmentResult(segment2)
        print(meta_chain2)

        segment3 = self.TextEngine.segmentInputWithChainCharMetaDict("我知道地球是圆的")
        print(segment3)
        rawInput, meta_chain3, unknown_metas_index = self.TextEngine.getCurMetaChainBySegmentResult(segment3)
        print(meta_chain3)

        # self.TextEngine.l

    def testSegmentFiles(self):
        print("——testSegmentArticle——")

        # 加载数据库元数据
        self.MemoryCentral.loadAllMetaFromDB()

        # path="C:\\Users\\langway\\Desktop\\temp\\"
        segmentedResult, unsegmented = self.TextEngine.segmentFiles(self.path, shouldLearn=False)  # 首先学习
        # print(segmentedResult) 太大，不能打印
        print("segmentedResult length::", len(segmentedResult))
        print("unsegmentedResult length::", len(unsegmented))

    def testSegmentEnglish(self):
        from loongtian.util.helper import fileHelper, stringHelper

        print(stringHelper.is_english("Do you know what"))

        file = self.eng_path + "My Favorite Animal.txt"
        lines = fileHelper.readLines(file)
        for line in lines:
            print(stringHelper.contain_zh_cn(line))
        file_lines_dict, file_raw_metas_dict = self.TextEngine.learnFile(file)

        segmentedResult = self.TextEngine.segmentFile(file)  # 首先学习

        print("segmentedResult length::", len(segmentedResult.segmentedResults))
        # print("unsegmentedResult length::",len(unsegmented))

    def tearDown(self):
        print("----tearDown----")


class TestMetaNetEngine(TestCase):

    def setUp(self):
        print("----setUp----")
        self.MemoryCentral = MemoryCentral(None)
        self.WorkingMemory = self.MemoryCentral.WorkingMemory
        self.MetaNetEngine = self.WorkingMemory.MetaNetEngine
        self.TextEngine = self.WorkingMemory.TextEngine

        self.meta_niu = MetaData(mvalue="牛", memory=self.MemoryCentral).create()
        self.meta_you = MetaData(mvalue="有", memory=self.MemoryCentral).create()
        self.meta_tui = MetaData(mvalue="腿", memory=self.MemoryCentral).create()
        self.meta_wo = MetaData(mvalue="我", memory=self.MemoryCentral).create()
        self.meta_zhidao = MetaData(mvalue="知道", memory=self.MemoryCentral).create()
        self.meta_zhongguo = MetaData(mvalue="中国", memory=self.MemoryCentral).create()
        self.meta_renmin = MetaData(mvalue="人民", memory=self.MemoryCentral).create()
        self.meta_jiefangjun = MetaData(mvalue="解放军", memory=self.MemoryCentral).create()
        self.meta_shi = MetaData(mvalue="是", memory=self.MemoryCentral).create()
        self.meta_zuibang = MetaData(mvalue="最棒", memory=self.MemoryCentral).create()
        self.meta_de = MetaData(mvalue="的", memory=self.MemoryCentral).create()

        # self.MemoryCentral.addMetasInMemory([self.meta_niu, self.meta_you, self.meta_tui,
        #                                      self.meta_wo, self.meta_zhidao,
        #                                      self.meta_zhongguo, self.meta_renmin, self.meta_jiefangjun,
        #                                      self.meta_shi, self.meta_zuibang, self.meta_de])

    def testCreateMetaNetByStartEnd(self):
        print("----testCreateMetaNetByStartEnd----")

        metaNetItem1 = MetaNet.createByStartEnd(self.meta_zhongguo, self.meta_renmin)  # "中国-人民"
        metaNetItem2 = MetaNet.createByStartEnd(metaNetItem1, self.meta_jiefangjun)  # "中国-人民"-"解放军"
        metaNetItem3 = MetaNet.createByStartEnd(metaNetItem2, self.meta_shi)  # "中国-人民"-"解放军" -"是"
        metaNetItem4 = MetaNet.createByStartEnd(self.meta_zuibang, self.meta_de)  # 最棒-的
        metaNetItem5 = MetaNet.createByStartEnd(metaNetItem3, metaNetItem4)  # 中国-人民"-"解放军" -"是"--最棒-的
        metaNetItem6 = MetaNet.createByStartEnd(self.meta_wo, self.meta_zhidao)  # 我-知道
        metaNetItem7 = MetaNet.createByStartEnd(metaNetItem6, metaNetItem5)

        self.assertEqual(metaNetItem1.startid, self.meta_zhongguo.id)
        self.assertEqual(metaNetItem1.endid, self.meta_renmin.id)

        self.assertEqual(metaNetItem2.startid, metaNetItem1.id)
        self.assertEqual(metaNetItem2.endid, self.meta_jiefangjun.id)

        self.assertEqual(metaNetItem3.startid, metaNetItem2.id)
        self.assertEqual(metaNetItem3.endid, self.meta_shi.id)

        self.assertEqual(metaNetItem4.startid, self.meta_zuibang.id)
        self.assertEqual(metaNetItem4.endid, self.meta_de.id)

        self.assertEqual(metaNetItem5.startid, metaNetItem3.id)
        self.assertEqual(metaNetItem5.endid, metaNetItem4.id)

        self.assertEqual(metaNetItem6.startid, self.meta_wo.id)
        self.assertEqual(metaNetItem6.endid, self.meta_zhidao.id)

        self.assertEqual(metaNetItem7.startid, metaNetItem6.id)
        self.assertEqual(metaNetItem7.endid, metaNetItem5.id)

    def testCreateMetaNetByChainItems(self):
        print("----testCreateMetaNetByChainItems----")

        metaNetItem1 = MetaNet.createMetaNetByMetaChain([
            [self.meta_wo, self.meta_zhidao], [
                [
                    [
                        [self.meta_zhongguo, self.meta_renmin], self.meta_jiefangjun
                    ], self.meta_shi
                ], [self.meta_zuibang, self.meta_de]
            ]
        ])  # "中国-人民"

    def testGetChainItems(self):
        print("----testGetChainItems----")
        metaNetItem1 = MetaNet.createByStartEnd(self.meta_zhongguo, self.meta_renmin)  # "中国-人民"
        metaNetItem2 = MetaNet.createByStartEnd(metaNetItem1, self.meta_jiefangjun)  # "中国-人民"-"解放军"
        metaNetItem3 = MetaNet.createByStartEnd(metaNetItem2, self.meta_shi)  # "中国-人民"-"解放军" -"是"
        metaNetItem4 = MetaNet.createByStartEnd(self.meta_zuibang, self.meta_de)  # 最棒-的
        metaNetItem5 = MetaNet.createByStartEnd(metaNetItem3, metaNetItem4)  # 中国-人民"-"解放军" -"是"--最棒-的
        metaNetItem6 = MetaNet.createByStartEnd(self.meta_wo, self.meta_zhidao)  # 我-知道
        metaNetItem7 = MetaNet.createByStartEnd(metaNetItem6, metaNetItem5)
        print(metaNetItem1)
        metaNetItem5.getChainItems()
        metaNetItem7.getChainItems()
        print(metaNetItem5)
        print(metaNetItem7)

        print("testGetChainItems succeed!!")

    def testTemp(self):
        a = "a"
        b = "b"
        li1 = [a, b]
        s = str(li1)
        li2 = (s)

        print(li2)

    def tearDown(self):
        print("----tearDown----")
