#!/usr/bin/env python
# -*- coding: utf-8 -*-
import __future__

from unittest import TestCase
from loongtian.nvwa.organs.brain import Brain
from loongtian.nvwa.organs.character import Character
from loongtian.nvwa.centrals.memoryCentral import MemoryCentral
from loongtian.nvwa.engines.metaEngine import TextEngine, MetaNetEngine
# from loongtian.util.log import logger
from loongtian.nvwa.models.metaData import MetaData
from loongtian.nvwa.models.metaNet import MetaNet

__author__ = 'Leon'


class TestTextEngine(TestCase):
    def setUp(self):
        print ("----setUp----")

        self.brain = Brain()
        self.MemoryCentral = self.brain.MemoryCentral
        self.TextEngine = self.MemoryCentral.WorkingMemory.TextEngine

        self.path = u"E:\\0-Nvwa\\doc\\知识库\\Other\\新浪新闻-用于自然语言处理的语料库\\"
        self.eng_path = u"E:\\0-Nvwa\\doc\\知识库\\Other\\English\\"

        self.RawInputs = [
            u"北京举办新年音乐会真棒！",
            u"音乐很动听",
            u"新年音乐会中的音乐很动听",
            u"音乐会非常成功，音乐让很多人沉醉！",
            u"音乐会陶冶情操！",
            u"音乐会有很多音乐。",
        ]

        self.MetaInputs = [u"我非常爱红苹果",
                           u"我非常爱吃红苹果",
                           u"红苹果我非常爱",
                           u"红苹果我非常爱吃",
                           u"我非常爱吃香蕉",
                           u"我非常爱咬一大口苹果"]
        self.RawMetas = {  # 自定义一个词典，有干扰因素
            u"中": 2.3, u"中国人民法院": 5.5, u"中国人民解放军": 7.5, u"中国人民": 7.0, u"中国人好": 5.0, u"中国人": 8.5, u"中国": 9.8, u"中央": 8.0,
            u"国人": 4.0, u"国家": 7.2, u"国际": 7.4,
            u"人人为我": 3.2, u"人均收入": 5.7, u"人民": 8.1, u"人类": 8.9, u"人民法院": 4.3, u"人均": 7.7,
            u"民主": 8.8, u"民法": 6.3, u"民生": 5.7, u"民法院": 3.2,
            u"法律文本": 5.6, u"法官": 7.9, u"法院": 8.7, u"法律": 9.2, u"法学": 4.3, u"法权": 2.5,
            u"有": 9.4, u"有司": 2.4, u"有钱人": 8.4, u"有钱": 9.6, u"有病": 9.3,  # u"有":9.9,
            u"司法权": 6.4, u"司机": 9.1, u"司法": 8.5,
            u"权利": 7.8, u"权力": 8.9, u"权谋": 7.6,
            u"软件": 9.7, u"软弱": 8.7, u"软蛋": 7.1,

        }
        self.inputs_with_stopmarks = [
            u"!",
            u"啊！",
            u"a!",
            u".。中国人民法院有司法权，中央强调坚决依法治国！\r\n我们希望中国成为法治国家...？；"
        ]
        self.mini_inputs = [u"音乐会很好",
                            u"音乐很好听",
                            u"北京音乐会"
                            ]

        self.inputs_with_number = [u"5月2日",
                                   u"身份证号210103197607293635是吉祥数字",
                                   u"1年天数365",
                                   u"在长达13年的学习生涯中学习了技能总数13",
                                   u"6 june有24小时"]

        # 带分词歧义
        self.inputs_with_ambiguity = [u"中",  # 0-测试单字分词
                                      u"我",  # 1-测试未识别单字
                                      u"中国",  # 2-测试单词
                                      u"我们",  # 3-测试未识别单词
                                      u"中国人民",  # 4-测试分支分词：中国人民，中国-人民，中国人-民
                                      u"有司法权",  # 5-测试分支分词：有司-法权，有-司法权，有-司法-权
                                      u"中国人懂法",  # 6-测试一半的词
                                      u"中国人民法院有司法权中央",  # 7-
                                      u"有司法权中央美",  # 8-测试未识别词
                                      u"  中国人民法院系红旗有司法权中央",  # 9-测试未识别词
                                      ]

        self.inputs_with_mix = [u"6 june有24小时,数字8.96",
                                u"\"21th Century will be the century of China!\"，这句话的意思是：“21世纪将是属于中国的世纪！"]

        self.inputs_full_english = u"Do you know what kind of animal I like most? " \
                                   u"It’s monkey. Monkey is a kind of lovely animal. " \
                                   u"Many people like monkeys very much. Generally, " \
                                   u"monkey has small body covered with fur. " \
                                   u"Some kinds of monkeys have two big eyes and ears and a long tail. " \
                                   u"I can see them on TV or the zoo. Every time I go to the zoo, " \
                                   u"I will go to see them. " \
                                   u"Monkeys often stay in trees and jump between them. " \
                                   u"They are so lively and favorable. " \
                                   u"When they are happy, they will act for visitors. It’s very funny."

    def testSegmentWithStopMarks(self):
        """
        实验以标点符号分解字符块。
        :return:
        """
        print ("----testSegmentWithStopMarks----")
        result1 = self.TextEngine.segmentWithStopMarks(self.inputs_with_stopmarks[0])
        print(result1)

        result2 = self.TextEngine.segmentWithStopMarks(self.inputs_with_stopmarks[1])
        print(result2)

        result3 = self.TextEngine.segmentWithStopMarks(self.inputs_with_stopmarks[2])
        print(result3)

        result4 = self.TextEngine.segmentWithStopMarks(self.inputs_with_stopmarks[3])
        print(result4)

    def testSegmentWithNumber(self):

        print ("----testSegmentWithNumber----")
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
        print ("----testCreateDoubleFrequancyDict----")
        # 多输入
        doubleFrequancyDict, length = self.TextEngine.createDoubleFrequancyDict(self.RawInputs)
        print(doubleFrequancyDict)

        # 同样的话又说了一遍（因为两次输入一样，其词频不应发生变化）
        doubleFrequancyDict, length = self.TextEngine.createDoubleFrequancyDict(self.RawInputs)
        print(doubleFrequancyDict)

        # 单输入，带标点
        doubleFrequancyDict, length = self.TextEngine.createDoubleFrequancyDict([self.inputs_with_stopmarks[3]])
        print(doubleFrequancyDict)

        # 英文输入
        doubleFrequancyDict, length = self.TextEngine.createDoubleFrequancyDict([self.inputs_full_english])
        print(doubleFrequancyDict)

    def testExtractRawMetaData(self):
        """
        测试根据元输入，从双字-频率字典提取元词块（可能有多个）（传入self.WordFrequncyDict）
        :return:
        """
        print ("----testExtractRawMetaData----")
        self.TextEngine.Threshold_ContinuousBlocks = 0.08
        raw_metas1, segmentedInputs1 = self.TextEngine.extractRawMetaData(self.RawInputs)

        print (raw_metas1)
        print(segmentedInputs1)

        # 同样的话又提取了一遍，还应是原来的结果！
        raw_metas2, segmentedInputs2 = self.TextEngine.extractRawMetaData(self.RawInputs)

        print (raw_metas2)
        print(segmentedInputs2)

        self.TextEngine.Threshold_ContinuousBlocks = 0.03
        raw_metas3, segmentedInputs3 = self.TextEngine.extractRawMetaData([self.inputs_full_english])

        print (raw_metas3)
        print(segmentedInputs3)

    def testLoadChainCharMetaDict(self):
        """
        测试以元数据：词频}的字典加载{首字母：元数据列表}字符链字典
        :return:
        """
        print("----testLoadChainCharMetaDict----")
        # mini_inputs=[u"中国人民法院有司法权中央",u"中"]
        raw_metas, segmentedInputs = self.TextEngine.extractRawMetaData(self.RawInputs)
        print (raw_metas)
        print(segmentedInputs)
        chainChar_MetaDict = self.TextEngine.loadChainCharMetaDict(raw_metas)

        print(chainChar_MetaDict)

        print(self.RawMetas)

        chainChar_MetaDict = self.TextEngine.loadChainCharMetaDict(self.RawMetas)

        print(chainChar_MetaDict)

    def testLoadAllMetaFromDB(self):
        print ("——testLoadAllMetaFromDB——")

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
        if __debug__:
            self.MemoryCentral.loadAllMetaFromDB()

        # 实验多字符的分词
        #  分解u"音乐会很好"，应该有下面两条结果：
        # [
        # [["音乐会",0,True],["很好",3,False]]
        # [["音乐",0,True],["会",2,False],["很好",3,False]]
        # ]
        # 每条记录的格式应为：[[word,i,True/False]]其含义为：[匹配到的单词，位置,是否元数据]的列表

        # # 0-测试单字 , u"中"
        # inputSegments0=self.TextEngine.segmentInputWithChainCharMetaDict(self.inputs_with_ambiguity[0]) #,chainCharMetaDict,self.TextWorkingMemory.NgramDict,self.Brain.Character.GramNum,self.TextWorkingMemory.StopMarks)
        # print(inputSegments0)
        #
        # # 1-测试未识别单字, u"我"
        # inputSegments1=self.TextEngine.segmentInputWithChainCharMetaDict(self.inputs_with_ambiguity[1]) #,chainCharMetaDict,self.TextWorkingMemory.NgramDict,self.Brain.Character.GramNum,self.TextWorkingMemory.StopMarks)
        # print(inputSegments1)
        #
        # # 2-测试单词, u"中国"
        # inputSegments2=self.TextEngine.segmentInputWithChainCharMetaDict(self.inputs_with_ambiguity[2])
        # print(inputSegments2)
        #
        # # 3-测试未识别单词, u"我们"
        # inputSegments3=self.TextEngine.segmentInputWithChainCharMetaDict(self.inputs_with_ambiguity[3])
        # print(inputSegments3)
        #
        # # 4-测试分支分词：中国人民，中国-人民，中国人-民，中-国-人民，中-国人-民，u"中国人民"
        # inputSegments4=self.TextEngine.segmentInputWithChainCharMetaDict(self.inputs_with_ambiguity[4])
        # print(inputSegments4)

        # 5-测试分支分词：有司-法权，有-司法权，有-司法-权 , u"有司法权",
        inputSegments5 = self.TextEngine.segmentInputWithChainCharMetaDict(self.inputs_with_ambiguity[5])
        print(inputSegments5)

        # 6-测试一半的词, u"中国人懂法"
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

        segmentedResult10 = self.TextEngine.segmentInputWithChainCharMetaDict(u"属于宣武区的编号J040800495的一位姓高的申请人")
        print(segmentedResult10)

        segmentedResult11 = self.TextEngine.segmentInputWithChainCharMetaDict(u"记者杜金明通讯员惠民")
        print(segmentedResult11)

        segmentedResult12 = self.TextEngine.segmentInputWithChainCharMetaDict(u"2018年6月9日")
        print(segmentedResult12)

        # "6 june有24小时"
        segmentedResult13 = self.TextEngine.segmentInputWithChainCharMetaDict(self.inputs_with_mix[0])
        print(segmentedResult13)

        # "21th Century will be the century of China!"，这句话的意思是：“21世纪将是属于中国的世纪！"
        segmentedResult14 = self.TextEngine.segmentInputWithChainCharMetaDict(self.inputs_with_mix[1])
        print(segmentedResult14)

        segmentedResult15 = self.TextEngine.segmentInputWithChainCharMetaDict(self.inputs_full_english)
        print(segmentedResult15)

    def testLearnFiles(self):
        print("——testLearnFiles——")

        file_lines_dict, file_raw_metas_dict = self.TextEngine.learnFiles(self.path,
                                                                          unknowns_tolerate_dgree=Character.Unknowns_Tolerate_Dgree)
        print("self.TextEngine.WordFrequncyDict Length:", len(self.MemoryCentral.NewLearnedRawMetas))

    def testUpdatAllMetaData(self):
        if __debug__:
            self.MemoryCentral.loadAllMetaFromDB()

        print("——testUpdatAllMetaData——")
        self.TextEngine.updatAllMetaData(recognized=True, createtime='2018-05-03 17:55:41.68313+08')

    def testSegmentArticle(self):
        print("——testSegmentArticle——")
        if __debug__:
            self.MemoryCentral.loadAllMetaFromDB()
        niu = self.MemoryCentral.PersistentMemory.ChainCharMetaDict.get(u"身")

        # 首先学习

        # print("self.TextEngine.WordFrequncyDict Length:",len(self.TextEngine.WordFrequncyDict))
        file = self.path + u"经适房公示人员身份证号为18个“1”遭质疑.txt"
        # self.TextEngine.learnFile(file)
        # self.TextEngine.updateNewLearnedMetaData()
        segmentedResult = self.TextEngine.segmentArticle(file, shouldLearn=True)
        # self.TextEngine.updateNewLearnedMetaData()
        print(segmentedResult)

        file = self.path + u"男子非法吸收公众存款1.91亿获刑5年.txt"
        segmentedResult = self.TextEngine.segmentArticle(file, shouldLearn=False)
        print(segmentedResult)

    def testGetMetaChainBySegmentResult(self):
        print("----testGetMetaChainBySegmentResult----")

        meta_niu = MetaData(mvalue=u"牛",memory=self.MemoryCentral).create()
        meta_you = MetaData(mvalue=u"有",memory=self.MemoryCentral).create()
        meta_tui = MetaData(mvalue=u"腿",memory=self.MemoryCentral).create()
        meta_wo = MetaData(mvalue=u"我",memory=self.MemoryCentral).create()
        meta_zhidao = MetaData(mvalue=u"知道",memory=self.MemoryCentral).create()

        self.MemoryCentral.addMetasInMemory([meta_niu, meta_you, meta_tui, meta_wo, meta_zhidao])
        segment1 = self.TextEngine.segmentInputWithChainCharMetaDict(u"牛有腿",
                                                                     unknowns_tolerate_dgree=Character.Unknowns_Tolerate_Dgree)
        print(segment1)
        rawInput, meta_chain1, unknown_metas_index = self.TextEngine.getCurMetaChainBySegmentResult(segment1)
        print(meta_chain1)

        segment2 = self.TextEngine.segmentInputWithChainCharMetaDict(u"我知道牛有腿",
                                                                     unknowns_tolerate_dgree=Character.Unknowns_Tolerate_Dgree)
        print(segment2)
        rawInput, meta_chain2, unknown_metas_index = self.TextEngine.getCurMetaChainBySegmentResult(segment2)
        print(meta_chain2)

    def testLoadNgramDict(self):
        print("----testLoadNgramDict----")

        meta_niu = MetaData(mvalue=u"牛",memory=self.MemoryCentral).create()
        meta_you = MetaData(mvalue=u"有",memory=self.MemoryCentral).create()
        meta_tui = MetaData(mvalue=u"腿",memory=self.MemoryCentral).create()
        meta_diqiu = MetaData(mvalue=u"地球",memory=self.MemoryCentral).create()
        meta_shi = MetaData(mvalue=u"是",memory=self.MemoryCentral).create()
        meta_yuande = MetaData(mvalue=u"圆的",memory=self.MemoryCentral).create()
        meta_wo = MetaData(mvalue=u"我",memory=self.MemoryCentral).create()
        meta_zhidao = MetaData(mvalue=u"知道",memory=self.MemoryCentral).create()

        self.MemoryCentral.addMetasInMemory(
            [meta_niu, meta_you, meta_tui, meta_wo, meta_zhidao, meta_diqiu, meta_shi, meta_yuande])
        segment1 = self.TextEngine.segmentInputWithChainCharMetaDict(u"牛有腿")
        print(segment1)
        rawInput, meta_chain1, unknown_metas_index = self.TextEngine.getCurMetaChainBySegmentResult(segment1)
        print(meta_chain1)

        segment2 = self.TextEngine.segmentInputWithChainCharMetaDict(u"我知道牛有腿")
        print(segment2)
        rawInput, meta_chain2, unknown_metas_index = self.TextEngine.getCurMetaChainBySegmentResult(segment2)
        print(meta_chain2)

        segment3 = self.TextEngine.segmentInputWithChainCharMetaDict(u"我知道地球是圆的")
        print(segment3)
        rawInput, meta_chain3, unknown_metas_index = self.TextEngine.getCurMetaChainBySegmentResult(segment3)
        print(meta_chain3)

        # self.TextEngine.l

    def testSegmentArticles(self):
        print("——testSegmentArticle——")

        # 加载数据库元数据
        if __debug__:
            self.MemoryCentral.loadAllMetaFromDB()

        # path=u"C:\\Users\\langway\\Desktop\\temp\\"
        segmentedResult, unsegmented = self.TextEngine.segmentArticles(self.path, shouldLearn=False)  # 首先学习
        # print(segmentedResult) 太大，不能打印
        print("segmentedResult length::", len(segmentedResult))
        print("unsegmentedResult length::", len(unsegmented))

    def testSegmentEnglish(self):
        from loongtian.util.helper import fileHelper, stringHelper

        print(stringHelper.is_all_alphabet(u"Do you know what"))

        file = self.eng_path + u"My Favorite Animal.txt"
        lines = fileHelper.readLines(file)
        for line in lines:
            print(stringHelper.contain_zh_cn(line))
        file_lines_dict, file_raw_metas_dict = self.TextEngine.learnFile(file)

        segmentedResult = self.TextEngine.segmentArticle(file)  # 首先学习

        print("segmentedResult length::", len(segmentedResult.segmentedResults))
        # print("unsegmentedResult length::",len(unsegmented))

    def tearDown(self):
        print("----tearDown----")


class TestMetaNetEngine(TestCase):

    def setUp(self):
        print ("----setUp----")
        self.MemoryCentral = MemoryCentral(None)
        self.WorkingMemory = self.MemoryCentral.WorkingMemory
        self.MetaNetEngine = self.WorkingMemory.MetaNetEngine
        self.TextEngine = self.WorkingMemory.TextEngine

        self.meta_niu = MetaData(mvalue=u"牛",memory=self.MemoryCentral).create()
        self.meta_you = MetaData(mvalue=u"有",memory=self.MemoryCentral).create()
        self.meta_tui = MetaData(mvalue=u"腿",memory=self.MemoryCentral).create()
        self.meta_wo = MetaData(mvalue=u"我",memory=self.MemoryCentral).create()
        self.meta_zhidao = MetaData(mvalue=u"知道",memory=self.MemoryCentral).create()
        self.meta_zhongguo = MetaData(mvalue=u"中国",memory=self.MemoryCentral).create()
        self.meta_renmin = MetaData(mvalue=u"人民",memory=self.MemoryCentral).create()
        self.meta_jiefangjun = MetaData(mvalue=u"解放军",memory=self.MemoryCentral).create()
        self.meta_shi = MetaData(mvalue=u"是",memory=self.MemoryCentral).create()
        self.meta_zuibang = MetaData(mvalue=u"最棒",memory=self.MemoryCentral).create()
        self.meta_de = MetaData(mvalue=u"的",memory=self.MemoryCentral).create()

        # self.MemoryCentral.addMetasInMemory([self.meta_niu, self.meta_you, self.meta_tui,
        #                                      self.meta_wo, self.meta_zhidao,
        #                                      self.meta_zhongguo, self.meta_renmin, self.meta_jiefangjun,
        #                                      self.meta_shi, self.meta_zuibang, self.meta_de])

    def testCreateMetaNetByStartEnd(self):
        print("----testCreateMetaNetByStartEnd----")

        metaNetItem1 = MetaNet.createMetaNetByStartEnd(self.meta_zhongguo, self.meta_renmin)  # "中国-人民"
        metaNetItem2 = MetaNet.createMetaNetByStartEnd(metaNetItem1, self.meta_jiefangjun)  # "中国-人民"-"解放军"
        metaNetItem3 = MetaNet.createMetaNetByStartEnd(metaNetItem2, self.meta_shi)  # "中国-人民"-"解放军" -"是"
        metaNetItem4 = MetaNet.createMetaNetByStartEnd(self.meta_zuibang, self.meta_de)  # 最棒-的
        metaNetItem5 = MetaNet.createMetaNetByStartEnd(metaNetItem3, metaNetItem4)  # 中国-人民"-"解放军" -"是"--最棒-的
        metaNetItem6 = MetaNet.createMetaNetByStartEnd(self.meta_wo, self.meta_zhidao)  # 我-知道
        metaNetItem7 = MetaNet.createMetaNetByStartEnd(metaNetItem6, metaNetItem5)

        self.assertEqual(metaNetItem1.startid, self.meta_zhongguo.mid)
        self.assertEqual(metaNetItem1.endid, self.meta_renmin.mid)

        self.assertEqual(metaNetItem2.startid, metaNetItem1.mnid)
        self.assertEqual(metaNetItem2.endid, self.meta_jiefangjun.mid)

        self.assertEqual(metaNetItem3.startid, metaNetItem2.mnid)
        self.assertEqual(metaNetItem3.endid, self.meta_shi.mid)

        self.assertEqual(metaNetItem4.startid, self.meta_zuibang.mid)
        self.assertEqual(metaNetItem4.endid, self.meta_de.mid)

        self.assertEqual(metaNetItem5.startid, metaNetItem3.mnid)
        self.assertEqual(metaNetItem5.endid, metaNetItem4.mnid)

        self.assertEqual(metaNetItem6.startid, self.meta_wo.mid)
        self.assertEqual(metaNetItem6.endid, self.meta_zhidao.mid)

        self.assertEqual(metaNetItem7.startid, metaNetItem6.mnid)
        self.assertEqual(metaNetItem7.endid, metaNetItem5.mnid)

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
        metaNetItem1 = MetaNet.createMetaNetByStartEnd(self.meta_zhongguo, self.meta_renmin)  # "中国-人民"
        metaNetItem2 = MetaNet.createMetaNetByStartEnd(metaNetItem1, self.meta_jiefangjun)  # "中国-人民"-"解放军"
        metaNetItem3 = MetaNet.createMetaNetByStartEnd(metaNetItem2, self.meta_shi)  # "中国-人民"-"解放军" -"是"
        metaNetItem4 = MetaNet.createMetaNetByStartEnd(self.meta_zuibang, self.meta_de)  # 最棒-的
        metaNetItem5 = MetaNet.createMetaNetByStartEnd(metaNetItem3, metaNetItem4)  # 中国-人民"-"解放军" -"是"--最棒-的
        metaNetItem6 = MetaNet.createMetaNetByStartEnd(self.meta_wo, self.meta_zhidao)  # 我-知道
        metaNetItem7 = MetaNet.createMetaNetByStartEnd(metaNetItem6, metaNetItem5)
        print(metaNetItem1)
        metaNetItem5.getChainItems()
        metaNetItem7.getChainItems()
        print(metaNetItem5)
        print(metaNetItem7)

        print("testGetChainItems succeed!!")

    def testTemp(self):
        a = u"a"
        b = "b"
        li1 = [a, b]
        s = str(li1)
        li2 = (s)

        print(li2)

    def tearDown(self):
        print("----tearDown----")
