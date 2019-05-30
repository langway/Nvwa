#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

from unittest import TestCase

from loongtian.nvwa.models.enum import ObjType
from loongtian.nvwa.models.knowledge import Knowledge
from loongtian.nvwa.models.realObject import RealObject
from loongtian.nvwa.models.metaData import MetaData
class TestKnowledge(TestCase):

    def setUp(self):
        print("----setUp----")

    def test_createKnowledgeByObjChain(self):
        print("----test_createKnowledgeByObjChain----")
        # 一个对象
        # [a]
        real_a = RealObject.createMetaRealByValue("a")
        obj_chain =[real_a[1]]
        klg = Knowledge.createKnowledgeByObjChain(obj_chain)
        components = klg.getSequenceComponents()
        print (components)

        # [[a]]
        obj_chain =[[real_a[1]]]
        klg = Knowledge.createKnowledgeByObjChain(obj_chain)
        components = klg.getSequenceComponents()
        print (components)

        # [a,None]
        obj_chain = [real_a[1], None]
        klg = Knowledge.createKnowledgeByObjChain(obj_chain)
        components = klg.getSequenceComponents()
        print (components)

        # [[a,None]]
        obj_chain = [[real_a[1], None]]
        klg = Knowledge.createKnowledgeByObjChain(obj_chain)
        components = klg.getSequenceComponents()
        print (components)

        # [a,b]
        real_b = RealObject.createMetaRealByValue("b")
        obj_chain = [real_a[1],real_b[1]]
        klg = Knowledge.createKnowledgeByObjChain(obj_chain)
        components = klg.getSequenceComponents()
        print (components)

        # [a,b,c]
        real_c = RealObject.createMetaRealByValue("c")
        obj_chain = [real_a[1], real_b[1], real_c[1]]
        klg = Knowledge.createKnowledgeByObjChain(obj_chain)
        components=klg.getSequenceComponents()
        print (components)

        # [[a,b],c]
        obj_chain = [[real_a[1], real_b[1]], real_c[1]]
        klg = Knowledge.createKnowledgeByObjChain(obj_chain)
        components = klg.getSequenceComponents()
        print (components)

        # [a,[b,c]]
        obj_chain = [real_a[1], [real_b[1], real_c[1]]]
        klg = Knowledge.createKnowledgeByObjChain(obj_chain)
        components = klg.getSequenceComponents()
        print (components)

        # [[a,b],[c,d]]
        real_d = RealObject.createMetaRealByValue("d")
        obj_chain = [[real_a[1], real_b[1]], [real_c[1],real_d[1]]]
        klg = Knowledge.createKnowledgeByObjChain(obj_chain)
        components = klg.getSequenceComponents()
        print (components)

        # [[a,b],e,[c,d]]
        real_e = RealObject.createMetaRealByValue("e")
        obj_chain = [[real_a[1], real_b[1]],real_e[1], [real_c[1],real_d[1]]]
        klg = Knowledge.createKnowledgeByObjChain(obj_chain)
        components = klg.getSequenceComponents()
        print (components)

        obj_chain = [None,[real_a[1], real_b[1]], real_e[1], [real_c[1], real_d[1]],real_e[1]]
        klg = Knowledge.createKnowledgeByObjChain(obj_chain)
        components = klg.getSequenceComponents()
        print (components)

        self.meta_xiaoming = MetaData(mvalue=u"小明").create()
        self.meta_da = MetaData(mvalue=u"打").create()
        self.meta_xiaoli = MetaData(mvalue=u"小丽").create()

        self.meta_shouluo = MetaData(mvalue=u"手落").create()
        self.meta_taishou = MetaData(mvalue=u"抬手").create()

        self.meta_shouteng = MetaData(mvalue=u"手疼").create()
        self.meta_ku = MetaData(mvalue=u"哭").create()
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

        klg = Knowledge.createKnowledgeByObjChain(obj_chain)
        components = klg.getSequenceComponents()
        print (components)


    # def test_createKnowledgeByObjChain(self):
    #     print("----test_createKnowledgeByObjChain----")




    def tearDown(self):
        print("----tearDown----")
        # Knowledge._physicalDeleteAll()