#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase


from loongtian.nvwa.centrals.memoryCentral import MemoryCentral
from loongtian.nvwa.models.metaData import MetaData
from loongtian.nvwa.models.metaNet import MetaNet


class TestMetaNet(TestCase):

    def setUp(self):
        print("----setUp----")


        self.memoryCentral=MemoryCentral(None)
        self.textEngine=self.memoryCentral.WorkingMemory.TextEngine
        self.meta_niu=MetaData(mvalue = u"牛").create()
        self.meta_you=MetaData(mvalue = u"有").create()
        self.meta_tui=MetaData(mvalue = u"腿").create()
        self.meta_erduo=MetaData(mvalue = u"耳朵").create()
        self.meta_yanjing=MetaData(mvalue = u"眼睛").create()
        self.meta_wo=MetaData(mvalue = u"我").create()
        self.meta_zhidao=MetaData(mvalue = u"知道").create()
        self.meta_zhongguo=MetaData(mvalue = u"中国").create()
        self.meta_renmin=MetaData(mvalue = u"人民").create()
        self.meta_jiefangjun=MetaData(mvalue = u"解放军").create()
        self.meta_shi=MetaData(mvalue = u"是").create()
        self.meta_zuibang=MetaData(mvalue = u"最棒").create()
        self.meta_de=MetaData(mvalue = u"的").create()

        self.memoryCentral.addMetasInMemory([self.meta_niu,self.meta_you,
                                            self.meta_tui,self.meta_erduo,self.meta_yanjing,
                                            self.meta_wo,self.meta_zhidao,
                                            self.meta_zhongguo,self.meta_renmin,self.meta_jiefangjun,
                                            self.meta_shi,self.meta_zuibang,self.meta_de])


        self.MetaNetEngine = MemoryCentral(None).WorkingMemory.MetaNetEngine


    def testCreateMetaNetByMetaChain(self):
        print("----testGetMetaNetByMetaChain----")

        MetaNet._physicalDeleteAll()
        # T字型1-直线型
        meta_chain1=[self.meta_wo,self.meta_zhidao,
                    self.meta_zhongguo,self.meta_renmin,self.meta_jiefangjun,
                    self.meta_shi,
                    self.meta_zuibang,self.meta_de]
        meta_nets=[]
        mni=MetaNet.createMetaNetByMetaChain(meta_chain1,meta_nets)
        self.assertEqual(len(meta_nets),7)

        MetaNet._physicalDeleteAll()

        # T字型2
        meta_chain2=[self.meta_wo,self.meta_zhidao,
                    [self.meta_zhongguo,[self.meta_renmin,self.meta_jiefangjun]],self.meta_de]
        meta_nets=[]
        mni=MetaNet.createMetaNetByMetaChain(meta_chain2,meta_nets)
        self.assertEqual(len(meta_nets),5)

        MetaNet._physicalDeleteAll()

        # T字型3
        meta_chain3=[self.meta_wo,[self.meta_zhongguo,self.meta_renmin],self.meta_zhidao,
            [self.meta_zhongguo,[self.meta_renmin,self.meta_jiefangjun]]]
        meta_nets=[]
        mni=MetaNet.createMetaNetByMetaChain(meta_chain3,meta_nets)
        self.assertEqual(len(meta_nets),6)

        MetaNet._physicalDeleteAll()

        # T字型4
        meta_chain4=[[self.meta_wo,self.meta_zhidao],self.meta_de,
            [self.meta_zhongguo,[self.meta_renmin,self.meta_jiefangjun]],self.meta_shi]
        meta_nets=[]
        mni=MetaNet.createMetaNetByMetaChain(meta_chain4,meta_nets)
        self.assertEqual(len(meta_nets),6)

        MetaNet._physicalDeleteAll()

        # T字型5
        meta_chain5=[[self.meta_wo,self.meta_zhidao],self.meta_de,
            [self.meta_zhongguo,[self.meta_renmin,self.meta_jiefangjun]],self.meta_shi,[self.meta_zuibang,self.meta_de]]
        meta_nets=[]
        mni=MetaNet.createMetaNetByMetaChain(meta_chain5,meta_nets)
        self.assertEqual(len(meta_nets),8)

        MetaNet._physicalDeleteAll()

        # T字型6
        meta_chain6=[[self.meta_wo,self.meta_zhidao],
                    [[self.meta_zhongguo,self.meta_renmin,self.meta_jiefangjun],self.meta_shi],[self.meta_zuibang,self.meta_de]]
        meta_nets=[]
        mni=MetaNet.createMetaNetByMetaChain(meta_chain6,meta_nets)
        self.assertEqual(len(meta_nets),7)


    def testGetMetaNetByMetaChain(self):
        print("----testGetMetaNetByMetaChain----")
        MetaNet._physicalDeleteAll()
        # T字型1-直线型
        meta_chain1=[self.meta_wo,self.meta_zhidao,
                    self.meta_zhongguo,self.meta_renmin,self.meta_jiefangjun,
                    self.meta_shi,
                    self.meta_zuibang,self.meta_de]
        meta_chain1_value=[[[[[[[self.meta_wo.mvalue,self.meta_zhidao.mvalue],
                            self.meta_zhongguo.mvalue],self.meta_renmin.mvalue],self.meta_jiefangjun.mvalue],
                            self.meta_shi.mvalue],
                            self.meta_zuibang.mvalue],self.meta_de.mvalue]

        # 创建
        meta_nets=[]
        mni=MetaNet.createMetaNetByMetaChain(meta_chain1,meta_nets)
        # 查看创建后的结构
        self.assertEqual(len(meta_nets),7)
        self.assertEqual(mni._word_t_chain,meta_chain1_value)

        # 从数据库中取【线性条件】，查看结构
        mni=mni.getByIdInDB()
        mni.getChainItems()
        self.assertEqual(mni._word_t_chain,meta_chain1_value)
        mni=MetaNet.getByObjectChain(meta_chain1)
        self.assertIsNotNone(mni)
        self.assertEqual(mni._word_t_chain,meta_chain1_value)

        self.memoryCentral.cleanMetaNet()
        MetaNet._physicalDeleteAll()

        # T字型2
        meta_chain2=[self.meta_wo,self.meta_zhidao,
                    [self.meta_zhongguo,[self.meta_renmin,self.meta_jiefangjun]],self.meta_de]
        meta_chain2_value=[[[self.meta_wo.mvalue,self.meta_zhidao.mvalue],
                    [self.meta_zhongguo.mvalue,[self.meta_renmin.mvalue,self.meta_jiefangjun.mvalue]]],self.meta_de.mvalue]

        meta_chain2_sequence=[self.meta_wo,self.meta_zhidao,self.meta_zhongguo,self.meta_renmin,self.meta_jiefangjun,self.meta_de]
        # 创建
        meta_nets=[]
        mni=MetaNet.createMetaNetByMetaChain(meta_chain2,meta_nets)

        # 查看创建后的结构
        self.assertEqual(len(meta_nets),5)
        self.assertEqual(mni._word_t_chain,meta_chain2_value)

        # 从数据库中取【T型条件】，查看结构
        meta_nets=[]
        unproceed=[]
        mni=MetaNet.getByObjectChain(meta_chain2,meta_nets,unproceed)
        self.assertIsNotNone(mni)
        self.assertEqual(mni._word_t_chain,meta_chain2_value)

        # 从数据库中取【线性条件】，查看结构
        meta_nets=[]
        unproceed=[]
        mni=MetaNet.getByObjectChain(meta_chain2_sequence,meta_nets,unproceed)
        self.assertIsNotNone(mni)
        self.assertEqual(mni._word_t_chain,meta_chain2_value)

        self.memoryCentral.cleanMetaNet()
        MetaNet._physicalDeleteAll()

        # T字型3
        meta_chain3=[self.meta_wo,[self.meta_zhongguo,self.meta_renmin],self.meta_zhidao,
            [self.meta_zhongguo,[self.meta_renmin,self.meta_jiefangjun]]]
        meta_chain3_value=[[[self.meta_wo.mvalue,[self.meta_zhongguo.mvalue,self.meta_renmin.mvalue]],self.meta_zhidao.mvalue],
            [self.meta_zhongguo.mvalue,[self.meta_renmin.mvalue,self.meta_jiefangjun.mvalue]]]
        meta_chain3_sequence=[self.meta_wo,self.meta_zhongguo,self.meta_renmin,self.meta_zhidao,
                                self.meta_zhongguo,self.meta_renmin,self.meta_jiefangjun]
        # 创建
        meta_nets=[]
        mni=MetaNet.createMetaNetByMetaChain(meta_chain3,meta_nets)
        # 查看创建后的结构
        self.assertEqual(len(meta_nets),6)
        self.assertEqual(mni._word_t_chain,meta_chain3_value)

        # 从数据库中取【T型条件】，查看结构
        mni=MetaNet.getByObjectChain(meta_chain3)
        self.assertIsNotNone(mni)
        self.assertEqual(mni._word_t_chain,meta_chain3_value)

        # # 从数据库中取【线性条件】，查看结构
        # mni=MetaNet.getByObjectChain(meta_chain3_sequence)
        # self.assertIsNotNone(mni)
        # self.assertEqual(mni._t_chain_words,meta_chain3_value)

        self.memoryCentral.cleanMetaNet()
        MetaNet._physicalDeleteAll()

        # T字型4
        meta_chain4=[[self.meta_wo,self.meta_zhidao],self.meta_de,
            [self.meta_zhongguo,[self.meta_renmin,self.meta_jiefangjun]],self.meta_shi]
        meta_chain4_value=[[[[self.meta_wo.mvalue,self.meta_zhidao.mvalue],self.meta_de.mvalue],
            [self.meta_zhongguo.mvalue,[self.meta_renmin.mvalue,self.meta_jiefangjun.mvalue]]],self.meta_shi.mvalue]
        meta_chain4_sequence=[self.meta_wo,self.meta_zhidao,self.meta_de,
                            self.meta_zhongguo,self.meta_renmin,self.meta_jiefangjun,self.meta_shi]
        # 创建
        meta_nets=[]
        mni=MetaNet.createMetaNetByMetaChain(meta_chain4,meta_nets)

        # 查看创建后的结构
        self.assertEqual(len(meta_nets),6)
        self.assertEqual(mni._word_t_chain,meta_chain4_value)

        # 从数据库中取【T型条件】，查看结构
        mni=MetaNet.getByObjectChain(meta_chain4)
        self.assertIsNotNone(mni)
        self.assertEqual(mni._word_t_chain,meta_chain4_value)


        # # 从数据库中取【线性条件】，查看结构
        # mni=MetaNet.getByObjectChain(meta_chain4_sequence)
        # self.assertIsNotNone(mni)
        # self.assertEqual(mni._t_chain_words,meta_chain4_value)

        self.memoryCentral.cleanMetaNet()
        MetaNet._physicalDeleteAll()

        # T字型5
        meta_chain5=[[self.meta_wo,self.meta_zhidao],self.meta_de,
            [self.meta_zhongguo,[self.meta_renmin,self.meta_jiefangjun]],self.meta_shi,[self.meta_zuibang,self.meta_de]]
        meta_chain5_value=[[[[[self.meta_wo.mvalue,self.meta_zhidao.mvalue],self.meta_de.mvalue],
            [self.meta_zhongguo.mvalue,[self.meta_renmin.mvalue,self.meta_jiefangjun.mvalue]]],self.meta_shi.mvalue],[self.meta_zuibang.mvalue,self.meta_de.mvalue]]
        meta_chain5_sequence=[self.meta_wo,self.meta_zhidao,self.meta_de,
            self.meta_zhongguo,self.meta_renmin,self.meta_jiefangjun,self.meta_shi,self.meta_zuibang,self.meta_de]
        # 创建
        meta_nets=[]
        mni=MetaNet.createMetaNetByMetaChain(meta_chain5,meta_nets)

        # 查看创建后的结构
        self.assertEqual(len(meta_nets),8)
        self.assertEqual(mni._word_t_chain,meta_chain5_value)

        # 从数据库中取【T型条件】，查看结构
        mni=MetaNet.getByObjectChain(meta_chain5)
        self.assertIsNotNone(mni)
        self.assertEqual(mni._word_t_chain,meta_chain5_value)

        # # 从数据库中取【线性条件】，查看结构
        # mni=MetaNet.getByObjectChain(meta_chain5_sequence)
        # self.assertIsNotNone(mni)
        # self.assertEqual(mni._t_chain_words,meta_chain5_value)

        self.memoryCentral.cleanMetaNet()
        MetaNet._physicalDeleteAll()

        # T字型6
        meta_chain6=[[self.meta_wo,self.meta_zhidao],
                    [[self.meta_zhongguo,self.meta_renmin,self.meta_jiefangjun],self.meta_shi],[self.meta_zuibang,self.meta_de]]
        meta_chain6_value=[[[self.meta_wo.mvalue,self.meta_zhidao.mvalue],
                    [[[self.meta_zhongguo.mvalue,self.meta_renmin.mvalue],self.meta_jiefangjun.mvalue],self.meta_shi.mvalue]],[self.meta_zuibang.mvalue,self.meta_de.mvalue]]
        meta_chain6_sequence=[self.meta_wo,self.meta_zhidao,
                            self.meta_zhongguo,self.meta_renmin,self.meta_jiefangjun,self.meta_shi,self.meta_zuibang,self.meta_de]
        # 创建
        meta_nets=[]
        mni=MetaNet.createMetaNetByMetaChain(meta_chain6,meta_nets)

        # 查看创建后的结构
        self.assertEqual(len(meta_nets),7)
        self.assertEqual(mni._word_t_chain,meta_chain6_value)

        # 从数据库中取【T型条件】，查看结构
        mni=MetaNet.getByObjectChain(meta_chain6)
        self.assertIsNotNone(mni)
        self.assertEqual(mni._word_t_chain,meta_chain6_value)

        # # 从数据库中取【线性条件】，查看结构
        # mni=MetaNet.getByObjectChain(meta_chain6_sequence)
        # self.assertIsNotNone(mni)
        # self.assertEqual(mni._t_chain_words,meta_chain6_value)

        self.memoryCentral.cleanMetaNet()
        MetaNet._physicalDeleteAll()

    def testGetMetaNetLikeMetaChain(self):
        print("----testGetMetaNetLikeMetaChain----")
        MetaNet._physicalDeleteAll()
        # T字型1-直线型
        meta_chain1=[self.meta_wo,self.meta_zhidao,
                    self.meta_zhongguo,self.meta_renmin,self.meta_jiefangjun,
                    self.meta_shi,
                    self.meta_zuibang,self.meta_de]
        meta_chain1_value=[[[[[[[self.meta_wo.mvalue,self.meta_zhidao.mvalue],
                            self.meta_zhongguo.mvalue],self.meta_renmin.mvalue],self.meta_jiefangjun.mvalue],
                            self.meta_shi.mvalue],
                            self.meta_zuibang.mvalue],self.meta_de.mvalue]

        # 创建
        meta_nets=[]
        mni=MetaNet.createMetaNetByMetaChain(meta_chain1,meta_nets)
        # 查看创建后的结构
        self.assertEqual(len(meta_nets),7)
        self.assertEqual(mni._word_t_chain,meta_chain1_value)

        # 从数据库中取【线性条件】，查看结构
        mni=mni.getByIdInDB()
        mni.getChainItems()
        self.assertEqual(mni._word_t_chain,meta_chain1_value)
        mni=MetaNet.getLikeObjChain(meta_chain1)
        self.assertIsNotNone(mni)
        self.assertEqual(mni._word_t_chain,meta_chain1_value)

        self.memoryCentral.cleanMetaNet()
        MetaNet._physicalDeleteAll()

        # T字型2
        meta_chain2=[self.meta_wo,self.meta_zhidao,
                    [self.meta_zhongguo,[self.meta_renmin,self.meta_jiefangjun]],self.meta_de]
        meta_chain2_value=[[[self.meta_wo.mvalue,self.meta_zhidao.mvalue],
                    [self.meta_zhongguo.mvalue,[self.meta_renmin.mvalue,self.meta_jiefangjun.mvalue]]],self.meta_de.mvalue]

        meta_chain2_sequence=[self.meta_wo,self.meta_zhidao,self.meta_zhongguo,self.meta_renmin,self.meta_jiefangjun,self.meta_de]
        # 创建
        meta_nets=[]
        mni=MetaNet.createMetaNetByMetaChain(meta_chain2,meta_nets)

        # 查看创建后的结构
        self.assertEqual(len(meta_nets),5)
        self.assertEqual(mni._word_t_chain,meta_chain2_value)

        # 从数据库中取【T型条件】，查看结构
        meta_nets=[]
        unproceed=[]
        mni=MetaNet.getByObjectChain(meta_chain2,meta_nets,unproceed)
        self.assertIsNotNone(mni)
        self.assertEqual(mni._word_t_chain,meta_chain2_value)

        # 从数据库中取【线性条件】，查看结构
        mni=MetaNet.getLikeObjChain(meta_chain2_sequence)
        self.assertIsNotNone(mni)
        self.assertEqual(mni._word_t_chain,meta_chain2_value)

        self.memoryCentral.cleanMetaNet()
        MetaNet._physicalDeleteAll()

        # T字型3
        meta_chain3=[self.meta_wo,[self.meta_zhongguo,self.meta_renmin],self.meta_zhidao,
            [self.meta_zhongguo,[self.meta_renmin,self.meta_jiefangjun]]]
        meta_chain3_value=[[[self.meta_wo.mvalue,[self.meta_zhongguo.mvalue,self.meta_renmin.mvalue]],self.meta_zhidao.mvalue],
            [self.meta_zhongguo.mvalue,[self.meta_renmin.mvalue,self.meta_jiefangjun.mvalue]]]
        meta_chain3_sequence=[self.meta_wo,self.meta_zhongguo,self.meta_renmin,self.meta_zhidao,
                                self.meta_zhongguo,self.meta_renmin,self.meta_jiefangjun]
        # 创建
        meta_nets=[]
        mni=MetaNet.createMetaNetByMetaChain(meta_chain3,meta_nets)
        # 查看创建后的结构
        self.assertEqual(len(meta_nets),6)
        self.assertEqual(mni._word_t_chain,meta_chain3_value)

        # 从数据库中取【T型条件】，查看结构
        mni=MetaNet.getByObjectChain(meta_chain3)
        self.assertIsNotNone(mni)
        self.assertEqual(mni._word_t_chain,meta_chain3_value)

        # 从数据库中取【线性条件】，查看结构
        mni=MetaNet.getLikeObjChain(meta_chain3_sequence)
        self.assertIsNotNone(mni)
        self.assertEqual(mni._word_t_chain,meta_chain3_value)

        self.memoryCentral.cleanMetaNet()
        MetaNet._physicalDeleteAll()

        # T字型4
        meta_chain4=[[self.meta_wo,self.meta_zhidao],self.meta_de,
            [self.meta_zhongguo,[self.meta_renmin,self.meta_jiefangjun]],self.meta_shi]
        meta_chain4_value=[[[[self.meta_wo.mvalue,self.meta_zhidao.mvalue],self.meta_de.mvalue],
            [self.meta_zhongguo.mvalue,[self.meta_renmin.mvalue,self.meta_jiefangjun.mvalue]]],self.meta_shi.mvalue]
        meta_chain4_sequence=[self.meta_wo,self.meta_zhidao,self.meta_de,
                            self.meta_zhongguo,self.meta_renmin,self.meta_jiefangjun,self.meta_shi]
        # 创建
        meta_nets=[]
        mni=MetaNet.createMetaNetByMetaChain(meta_chain4,meta_nets)

        # 查看创建后的结构
        self.assertEqual(len(meta_nets),6)
        self.assertEqual(mni._word_t_chain,meta_chain4_value)

        # 从数据库中取【T型条件】，查看结构
        mni=MetaNet.getByObjectChain(meta_chain4)
        self.assertIsNotNone(mni)
        self.assertEqual(mni._word_t_chain,meta_chain4_value)


        # 从数据库中取【线性条件】，查看结构
        mni=MetaNet.getLikeObjChain(meta_chain4_sequence)
        self.assertIsNotNone(mni)
        self.assertEqual(mni._word_t_chain,meta_chain4_value)

        self.memoryCentral.cleanMetaNet()
        MetaNet._physicalDeleteAll()

        # T字型5
        meta_chain5=[[self.meta_wo,self.meta_zhidao],self.meta_de,
            [self.meta_zhongguo,[self.meta_renmin,self.meta_jiefangjun]],self.meta_shi,[self.meta_zuibang,self.meta_de]]
        meta_chain5_value=[[[[[self.meta_wo.mvalue,self.meta_zhidao.mvalue],self.meta_de.mvalue],
            [self.meta_zhongguo.mvalue,[self.meta_renmin.mvalue,self.meta_jiefangjun.mvalue]]],self.meta_shi.mvalue],[self.meta_zuibang.mvalue,self.meta_de.mvalue]]
        meta_chain5_sequence=[self.meta_wo,self.meta_zhidao,self.meta_de,
            self.meta_zhongguo,self.meta_renmin,self.meta_jiefangjun,self.meta_shi,self.meta_zuibang,self.meta_de]
        # 创建
        meta_nets=[]
        mni=MetaNet.createMetaNetByMetaChain(meta_chain5,meta_nets)

        # 查看创建后的结构
        self.assertEqual(len(meta_nets),8)
        self.assertEqual(mni._word_t_chain,meta_chain5_value)

        # 从数据库中取【T型条件】，查看结构
        mni=MetaNet.getByObjectChain(meta_chain5)
        self.assertIsNotNone(mni)
        self.assertEqual(mni._word_t_chain,meta_chain5_value)

        # 从数据库中取【线性条件】，查看结构
        mni=MetaNet.getLikeObjChain(meta_chain5_sequence)
        self.assertIsNotNone(mni)
        self.assertEqual(mni._word_t_chain,meta_chain5_value)

        self.memoryCentral.cleanMetaNet()
        MetaNet._physicalDeleteAll()

        # T字型6
        meta_chain6=[[self.meta_wo,self.meta_zhidao],
                    [[self.meta_zhongguo,self.meta_renmin,self.meta_jiefangjun],self.meta_shi],[self.meta_zuibang,self.meta_de]]
        meta_chain6_value=[[[self.meta_wo.mvalue,self.meta_zhidao.mvalue],
                    [[[self.meta_zhongguo.mvalue,self.meta_renmin.mvalue],self.meta_jiefangjun.mvalue],self.meta_shi.mvalue]],[self.meta_zuibang.mvalue,self.meta_de.mvalue]]
        meta_chain6_sequence=[self.meta_wo,self.meta_zhidao,
                            self.meta_zhongguo,self.meta_renmin,self.meta_jiefangjun,self.meta_shi,self.meta_zuibang,self.meta_de]
        # 创建
        meta_nets=[]
        mni=MetaNet.createMetaNetByMetaChain(meta_chain6,meta_nets)

        # 查看创建后的结构
        self.assertEqual(len(meta_nets),7)
        self.assertEqual(mni._word_t_chain,meta_chain6_value)

        # 从数据库中取【T型条件】，查看结构
        mni=MetaNet.getByObjectChain(meta_chain6)
        self.assertIsNotNone(mni)
        self.assertEqual(mni._word_t_chain,meta_chain6_value)

        # 从数据库中取【线性条件】，查看结构
        mni=MetaNet.getLikeObjChain(meta_chain6_sequence)
        self.assertIsNotNone(mni)
        self.assertEqual(mni._word_t_chain,meta_chain6_value)

        self.memoryCentral.cleanMetaNet()
        MetaNet._physicalDeleteAll()

    def testCreateMetaNetBySequnceWords(self):
        print ("----testCreateMetaNetBySequnceWords----")
        meta_net1=self.MetaNetEngine.createMetaNetBySequnceWords([u"牛", u"有", u"腿"])
        meta_net2=self.MetaNetEngine.createMetaNetBySequnceWords([u"牛", u"有", u"眼睛"])
        meta_net3=self.MetaNetEngine.createMetaNetBySequnceWords([u"牛", u"有", u"耳朵"])
        meta_net4=self.MetaNetEngine.createMetaNetBySequnceWords([[u"我", u"知道"], [u"牛", u"有", u"耳朵"]])
        self.assertEqual(meta_net1._word_t_chain,[[u"牛", u"有"], u"腿"])
        self.assertEqual(meta_net2._word_t_chain,[[u"牛", u"有"], u"眼睛"])
        self.assertEqual(meta_net3._word_s_chain,[u"牛", u"有", u"耳朵"])
        self.assertEqual(meta_net4._word_t_chain,[[u"我", u"知道"], [[u"牛", u"有"], u"耳朵"]])


    def testLoadNgramDictByMetaChain(self):
        print ("----testLoadNgramDictByMetaChain[直线型3元]----")
        segment_result=self.textEngine.segmentInputWithChainCharMetaDict("我知道中国人民解放军是最棒的！")
        for meta_chain,unknown_metas_index in self.textEngine.getCurMetaChainBySegmentResults(segment_result):
            ngram_dict= self.memoryCentral.WorkingMemory.MetaNetEngine.loadNgramDictByMetaChain(meta_chain,NgramNum = 3)
            if ngram_dict.get(u"知道"):
                # self.assertEqual(ngram_dict.get(u"知道")[2][u"中国"],1.0)
                self.assertEqual(ngram_dict.get(u"知道")[3][u"中国"][u"人民"],1.0)
            self.assertIsNone(ngram_dict.get(u"!"))

        allMetaNet= self.memoryCentral.WorkingMemory.MetaNetEngine.loadNgramDictFromDB()
        if self.memoryCentral.NgramDict.get(u"知道"):
                # self.assertEqual(self.memoryCentral.NgramDict.get(u"知道")[3][u"中国"],2.0)
                self.assertEqual(self.memoryCentral.NgramDict.get(u"知道")[3][u"中国"][u"人民"],1.0)
        self.assertIsNone(self.memoryCentral.NgramDict.get(u"!"))


    def testLoadNgramDictFromDB(self):
        print("----testLoadNgramDictFromDB[直线型2元]----")
        # 直线型
        segment_result=self.textEngine.segmentInputWithChainCharMetaDict("我知道中国人民解放军是最棒的！")
        for meta_chain,unknown_metas_index in self.textEngine.getCurMetaChainBySegmentResults(segment_result):
            MetaNet.createMetaNetByMetaChain(meta_chain)
            mni=MetaNet.getByObjectChain(meta_chain)
            # self.assertIsNotNone(mni)

        allMetaNet= self.memoryCentral.WorkingMemory.MetaNetEngine.loadNgramDictFromDB()
        if self.memoryCentral.NgramDict.get(u"知道"):
                self.assertEqual(self.memoryCentral.NgramDict.get(u"知道")[2][u"中国"],2.0)
                # self.assertEqual(self.memoryCentral.NgramDict.get(u"知道")[3][u"中国"][u"人民"],2.0)
        self.assertIsNone(self.memoryCentral.NgramDict.get(u"!"))


    def testLoadNgramDictFromDB2(self):
        print("----testLoadNgramDictFromDB2[T字型]----")
        # T字型
        meta_chain=[[self.meta_wo,self.meta_zhidao],
                    [[self.meta_zhongguo,self.meta_renmin,self.meta_jiefangjun],self.meta_shi,[self.meta_zuibang,self.meta_de]]]
        MetaNet.createMetaNetByMetaChain(meta_chain)
        mni=MetaNet.getByObjectChain(meta_chain)
        self.assertIsNotNone(mni)

        allMetaNet= self.memoryCentral.WorkingMemory.MetaNetEngine.loadNgramDictFromDB()
        if self.memoryCentral.NgramDict.get(u"知道"):
                self.assertEqual(self.memoryCentral.NgramDict.get(u"知道")[2][u"中国"],1.0)
                # self.assertEqual(self.memoryCentral.NgramDict.get(u"知道")[3][u"中国"][u"人民"],2.0)
        self.assertIsNone(self.memoryCentral.NgramDict.get(u"!"))

        allMetaNet= self.memoryCentral.WorkingMemory.MetaNetEngine.loadNgramDictFromDB(3)
        if self.memoryCentral.NgramDict.get(u"知道"):
                # self.assertEqual(self.memoryCentral.NgramDict.get(u"知道")[3][u"中国"],2.0)
                self.assertEqual(self.memoryCentral.NgramDict.get(u"知道")[3][u"中国"][u"人民"],1.0)
        self.assertIsNone(self.memoryCentral.NgramDict.get(u"!"))



    def testDelete(self):
        print("----testDelete(逻辑删除)----")

        MetaNet._physicalDeleteAll()

        # 直线型
        meta_chain1=[self.meta_wo,self.meta_zhidao,
                    self.meta_zhongguo,self.meta_renmin,self.meta_jiefangjun,
                    self.meta_shi,
                    self.meta_zuibang,self.meta_de]
        meta_nets=[]
        mni=MetaNet.createMetaNetByMetaChain(meta_chain1,meta_nets)
        self.assertEqual(len(meta_nets),7)

        MetaNet.deleteByEnd(self.meta_zuibang) # 应该逻辑删除[最棒,的]
        mni=MetaNet.getByEndInDB(self.meta_zuibang)
        mni.getChainItems()
        self.assertEqual(mni.status,0)
        mni=MetaNet.getByStartInDB(self.meta_zhongguo)
        self.assertIsNone(mni)
        mni=MetaNet.getByStartInDB(self.meta_wo)
        self.assertEqual(mni.status,200)

        MetaNet.deleteByEnd(self.meta_shi) # 应该逻辑删除[MN1,是]。MN1:[我,知道,中国,人民,解放军]不会删除，不是整个链
        mni=MetaNet.getByEndInDB(self.meta_shi)
        self.assertEqual(mni.status,0)
        mni=MetaNet.getByEndInDB(self.meta_zhongguo)
        self.assertEqual(mni.status,200)
        mni=MetaNet.getByStartInDB(self.meta_wo)
        self.assertEqual(mni.status,200)

        MetaNet.deleteByStart(self.meta_zhongguo) # 没有删除
        mni=MetaNet.getByEndInDB(self.meta_zhongguo)
        self.assertEqual(mni.status,200)
        mni=MetaNet.getByStartInDB(self.meta_wo)
        self.assertEqual(mni.status,200)

        # 在此创建，将进行逻辑恢复
        mni=MetaNet.createMetaNetByMetaChain(meta_chain1)
        self.assertEqual(mni.status,200)

        MetaNet.deleteByStart(self.meta_wo) # 全链删除
        mni=MetaNet.getByEndInDB(self.meta_zhongguo)
        self.assertEqual(mni.status,0)

        MetaNet._physicalDeleteAll()

        # T字型
        meta_chain2=[[self.meta_wo,self.meta_zhidao],
                    [[self.meta_zhongguo,self.meta_renmin,self.meta_jiefangjun],self.meta_shi,[self.meta_zuibang,self.meta_de]]]
        meta_nets=[]
        mni=MetaNet.createMetaNetByMetaChain(meta_chain2,meta_nets)
        self.assertEqual(len(meta_nets),7)


        MetaNet.deleteByEnd(self.meta_de) # 应该删除Mn1::[最棒,的] ,[Mn0,Mn1] Mn0:[[我,知道],[[中国,人民,解放军]],是]]不会删除
        mni=MetaNet.getByEndInDB(self.meta_de)
        self.assertEqual(mni.status,0)
        mni=MetaNet.getByStartAndEnd(self.meta_wo,self.meta_zhidao)
        self.assertEqual(mni.status,200)
        mni=MetaNet.getByObjectChain([self.meta_zhongguo,self.meta_renmin,self.meta_jiefangjun])
        self.assertEqual(mni.status,200)
        mni=MetaNet.getByObjectChain([self.meta_zhongguo,self.meta_renmin,self.meta_jiefangjun,self.meta_shi])
        self.assertEqual(mni.status,200)

        MetaNet.deleteByStart(self.meta_wo) # 应该删除Mn2:[我,知道]，Mn3:[[中国,人民,解放军],是]不会删除
        mni=MetaNet.getByEndInDB(self.meta_zhidao)
        self.assertEqual(mni.status,0)
        mni=MetaNet.getByObjectChain([self.meta_zhongguo,self.meta_renmin,self.meta_jiefangjun])
        self.assertEqual(mni.status,200)
        mni=MetaNet.getByObjectChain([self.meta_zhongguo,self.meta_renmin,self.meta_jiefangjun,self.meta_shi])
        self.assertEqual(mni.status,200)

        MetaNet.deleteByStart(self.meta_zhongguo) # [[中国,人民,解放军],是]全部删除
        mni=MetaNet.getByObjectChain([self.meta_zhongguo,self.meta_renmin,self.meta_jiefangjun])
        self.assertEqual(mni.status,0)
        mni=MetaNet.getByObjectChain([self.meta_zhongguo,self.meta_renmin,self.meta_jiefangjun,self.meta_shi])
        self.assertEqual(mni.status,0)

        MetaNet._physicalDeleteAll()

        mni=MetaNet.createMetaNetByMetaChain(meta_chain2)
        self.assertEqual(len(MetaNet.getAllInDB()),7)

        mni=MetaNet.getByObjectChain([self.meta_zhongguo,self.meta_renmin,self.meta_jiefangjun,self.meta_shi])
        self.assertEqual(mni.status,200)
        mni.delete() # 这里仅仅逻辑删除最后一个
        self.assertEqual(mni.status,0)
        mni=MetaNet.getByObjectChain([self.meta_zhongguo,self.meta_renmin,self.meta_jiefangjun])
        self.assertEqual(mni.status,200)
        mni=MetaNet.getByObjectChain([self.meta_zhongguo,self.meta_renmin,self.meta_jiefangjun,self.meta_shi])
        self.assertEqual(mni.status,0)

        mni=MetaNet.deleteByObjChain([self.meta_zhongguo,self.meta_renmin,self.meta_jiefangjun])
        self.assertEqual(mni.status,0)
        mni=MetaNet.getByObjectChain([self.meta_zhongguo,self.meta_renmin,self.meta_jiefangjun,self.meta_shi])
        self.assertEqual(mni.status,0)



    def testZig(self):
        print("——testZig——")
        # 直线型
        meta_chain1=[self.meta_wo,self.meta_zhidao,
                    self.meta_zhongguo,self.meta_renmin,self.meta_jiefangjun]
        meta_nets=[]
        mni=MetaNet.createMetaNetByMetaChain(meta_chain1,meta_nets)
        self.assertEqual(len(meta_nets),4)

        # T字型
        meta_chain2=[[self.meta_wo,self.meta_zhidao],
                    [self.meta_zhongguo,[self.meta_renmin,self.meta_jiefangjun]]]
        mni.zig_to(meta_chain2)

        mni.Layer.addUpper(mni)








    def tearDown(self):
        print("----tearDown----")
        MetaNet._physicalDeleteAll()