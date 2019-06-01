#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

from unittest import TestCase

from loongtian.nvwa.models.enum import ObjType
from loongtian.nvwa.models.knowledge import Knowledge
from loongtian.nvwa.models.realObject import RealObject
from loongtian.nvwa.models.metaData import MetaData
from loongtian.nvwa.centrals.memoryCentral import MemoryCentral

class TestKnowledge(TestCase):

    def setUp(self):
        print("----setUp----")
        self.memoryCentral = MemoryCentral(None)

    def test_createKnowledgeByObjChain(self):
        print("----test_createKnowledgeByObjChain----")
        # 一个对象
        # [a]
        meta_a,real_a = RealObject.createMetaRealByValue("a",memory=self.memoryCentral)
        obj_chain =[real_a]
        klg = Knowledge.createKnowledgeByObjChain(obj_chain,memory=self.memoryCentral)
        components = klg.getSequenceComponents()
        self.assertEqual (len(components),1)
        self.assertEqual(components[0].remark, "a")

        # [[a]]
        obj_chain =[[real_a]]
        klg = Knowledge.createKnowledgeByObjChain(obj_chain,memory=self.memoryCentral)
        components = klg.getSequenceComponents()
        self.assertEqual(len(components), 1)
        self.assertEqual(len(components[0]), 1)
        self.assertEqual(components[0][0].remark, "a")

        # [a,None]
        obj_chain = [real_a, None]
        klg = Knowledge.createKnowledgeByObjChain(obj_chain)
        components = klg.getSequenceComponents()
        self.assertEqual(len(components), 2)
        self.assertEqual(components[0].remark, "a")
        self.assertEqual(components[1].remark, "无")
        

        # [[a,None]]
        obj_chain = [[real_a, None]]
        klg = Knowledge.createKnowledgeByObjChain(obj_chain,memory=self.memoryCentral)
        components = klg.getSequenceComponents()
        self.assertEqual(len(components), 1)
        self.assertEqual(len(components[0]), 2)
        self.assertEqual(components[0][0].remark, "a")
        self.assertEqual(components[0][1].remark, "无")

        # [a,b]
        meta_b,real_b = RealObject.createMetaRealByValue("b",memory=self.memoryCentral)
        obj_chain = [real_a,real_b]
        klg = Knowledge.createKnowledgeByObjChain(obj_chain,memory=self.memoryCentral)
        components = klg.getSequenceComponents()
        self.assertEqual(len(components), 2)
        self.assertEqual(components[0].remark, "a")
        self.assertEqual(components[1].remark, "b")

        # [a,b,c]
        meta_c,real_c = RealObject.createMetaRealByValue("c",memory=self.memoryCentral)
        obj_chain = [real_a, real_b, real_c]
        klg = Knowledge.createKnowledgeByObjChain(obj_chain,memory=self.memoryCentral)
        components=klg.getSequenceComponents()
        self.assertEqual(len(components), 3)
        self.assertEqual(components[0].remark, "a")
        self.assertEqual(components[1].remark, "b")
        self.assertEqual(components[2].remark, "c")

        # [[a,b],c]
        obj_chain = [[real_a, real_b], real_c]
        klg = Knowledge.createKnowledgeByObjChain(obj_chain,memory=self.memoryCentral)
        components = klg.getSequenceComponents()
        self.assertEqual(len(components), 2)
        self.assertEqual(len(components[0]), 2)
        self.assertEqual(components[0][0].remark, "a")
        self.assertEqual(components[0][1].remark, "b")
        self.assertEqual(components[1].remark, "c")

        # [a,[b,c]]
        obj_chain = [real_a, [real_b, real_c]]
        klg = Knowledge.createKnowledgeByObjChain(obj_chain,memory=self.memoryCentral)
        components = klg.getSequenceComponents()
        self.assertEqual(len(components), 2)
        self.assertEqual(len(components[1]), 2)
        self.assertEqual(components[0].remark, "a")
        self.assertEqual(components[1][0].remark, "b")
        self.assertEqual(components[1][1].remark, "c")

        # [[a,b],[c,d]]
        meta_d,real_d = RealObject.createMetaRealByValue("d",memory=self.memoryCentral)
        obj_chain = [[real_a, real_b], [real_c,real_d]]
        klg = Knowledge.createKnowledgeByObjChain(obj_chain,memory=self.memoryCentral)
        components = klg.getSequenceComponents()
        self.assertEqual(len(components), 2)
        self.assertEqual(len(components[0]), 2)
        self.assertEqual(len(components[1]), 2)
        self.assertEqual(components[0][0].remark, "a")
        self.assertEqual(components[0][1].remark, "b")
        self.assertEqual(components[1][0].remark, "c")
        self.assertEqual(components[1][1].remark, "d")

        # [[a,b],e,[c,d]]
        meta_e,real_e = RealObject.createMetaRealByValue("e",memory=self.memoryCentral)
        obj_chain = [[real_a, real_b],real_e, [real_c,real_d]]
        klg = Knowledge.createKnowledgeByObjChain(obj_chain,memory=self.memoryCentral)
        components = klg.getSequenceComponents()
        self.assertEqual(len(components), 3)
        self.assertEqual(len(components[0]), 2)
        self.assertEqual(len(components[2]), 2)
        self.assertEqual(components[0][0].remark, "a")
        self.assertEqual(components[0][1].remark, "b")
        self.assertEqual(components[1].remark, "e")
        self.assertEqual(components[2][0].remark, "c")
        self.assertEqual(components[2][1].remark, "d")

        # [None,[a,b],e,[c,d],e]
        obj_chain = [None,[real_a, real_b], real_e, [real_c, real_d],real_e]
        klg = Knowledge.createKnowledgeByObjChain(obj_chain,memory=self.memoryCentral)
        components = klg.getSequenceComponents()
        print (components)
        self.assertEqual(len(components), 5)
        self.assertEqual(len(components[1]), 2)
        self.assertEqual(len(components[3]), 2)

        self.assertEqual(components[0].remark, "无")
        self.assertEqual(components[1][0].remark, "a")
        self.assertEqual(components[1][1].remark, "b")
        self.assertEqual(components[2].remark, "e")
        self.assertEqual(components[3][0].remark, "c")
        self.assertEqual(components[3][1].remark, "d")
        self.assertEqual(components[4].remark, "e")

        self.meta_xiaoming = MetaData(mvalue=u"小明",memory=self.memoryCentral).create()
        self.meta_da = MetaData(mvalue=u"打",memory=self.memoryCentral).create()
        self.meta_xiaoli = MetaData(mvalue=u"小丽",memory=self.memoryCentral).create()

        self.meta_shouluo = MetaData(mvalue=u"手落",memory=self.memoryCentral).create()
        self.meta_taishou = MetaData(mvalue=u"抬手",memory=self.memoryCentral).create()

        self.meta_shouteng = MetaData(mvalue=u"手疼",memory=self.memoryCentral).create()
        self.meta_ku = MetaData(mvalue=u"哭",memory=self.memoryCentral).create()
        self.real_xiaoming = RealObject.createRealByMeta(self.meta_xiaoming, realType=ObjType.VIRTUAL)
        self.real_da = RealObject.createRealByMeta(self.meta_da, realType=ObjType.ACTION)
        self.real_xiaoli = RealObject.createRealByMeta(self.meta_xiaoli, realType=ObjType.VIRTUAL)
        self.real_shouteng = RealObject.createRealByMeta(self.meta_shouteng, realType=ObjType.VIRTUAL)

        self.real_taishou = RealObject.createRealByMeta(self.meta_taishou, realType=ObjType.VIRTUAL)
        self.real_shouluo = RealObject.createRealByMeta(self.meta_shouluo, realType=ObjType.VIRTUAL)

        self.real_ku = RealObject.createRealByMeta(self.meta_ku, realType=ObjType.VIRTUAL)

        obj_chain = [  # meaning对应的knowledge知识链
            [  # steps：knowledge知识链的每一步的转换模式（可以有多个状态转换）
                [self.real_xiaoming, self.real_taishou], [self.real_xiaoming, self.real_shouluo],
                [self.real_xiaoming, self.real_shouteng], [self.real_xiaoli, self.real_ku],
                # status：knowledge知识链每一步中包含的每一个状态knowledge
            ],
        ]

        klg = Knowledge.createKnowledgeByObjChain(obj_chain,memory=self.memoryCentral)
        components = klg.getSequenceComponents()
        print (components)


    # def test_createKnowledgeByObjChain(self):
    #     print("----test_createKnowledgeByObjChain----")




    def tearDown(self):
        print("----tearDown----")
        # Knowledge._physicalDeleteAll()