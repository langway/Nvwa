#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase

from loongtian.nvwa.models.enum import ObjType
from loongtian.nvwa.models.metaData import MetaData
from loongtian.nvwa.models.realObject import RealObject


class TestRealObject(TestCase):
    def setUp(self):
        print("----setUp----")

        self.real_niu=RealObject(remark ="牛", realType = ObjType.VIRTUAL).create()
        for i in range(0, 10):
            meta = MetaData(type = ObjType.WORD, mvalue = "牛%d" % i).create()
            meta.Layers.addLower(self.real_niu)
            self.real_niu.Layers.addUpper(meta, False)


    def testCreateMetaRealByValue(self):
        print("----testCreateRealObjects----")
        print("----测试根据元输入（字符串）创建实际对象----")
        meta_niu,real_niu=RealObject.createMetaRealByValue("牛")
        meta_cow=MetaData(type = ObjType.WORD, mvalue = "cow").create()
        meta_cool,real_cool=RealObject.createMetaRealByValue("厉害")

        # 实际对象:厉害 指向 元数据:牛
        real_cool.addRelatedMetaData(meta_niu)
        # 实际对象:牛 指向 元数据:cow
        real_niu.addRelatedMetaData(meta_cow)

        # 判断元数据“牛”关联的实际对象的数量，以此类推
        self.assertEqual(2, len(meta_niu.Layers.getLowerEntitiesByType(ObjType.REAL_OBJECT)))
        self.assertEqual(1, len(meta_cow.Layers.getLowerEntitiesByType(ObjType.REAL_OBJECT)))
        self.assertEqual(1, len(meta_cool.Layers.getLowerEntitiesByType(ObjType.REAL_OBJECT)))

        self.assertEqual(2, len(real_niu.Layers.getUpperEntitiesByType(ObjType.WORD)))
        self.assertEqual(2, len(real_cool.Layers.getUpperEntitiesByType(ObjType.WORD)))


        # 判断元数据“牛”与实际对象“牛”、实际对象“厉害”有关联，以此类推
        self.assertEqual(True,real_niu.Layers.hasUpper(meta_niu))
        self.assertEqual(True,real_cool.Layers.hasUpper(meta_niu))

        self.assertEqual(True,meta_cow.Layers.hasLower(real_niu))
        self.assertEqual(False,meta_cow.Layers.hasLower(real_cool))

        self.assertEqual(True,real_cool.Layers.hasRelation(meta_cool,real_cool))
        self.assertEqual(False,meta_cool.Layers.hasRelation(meta_cool,real_niu))

        reals=meta_niu.Layers.getLowerEntitiesByType(ObjType.REAL_OBJECT)
        print ("字符串‘牛’有两个realObject，分别是({0})".format([x.obj.rid + x.obj.remark for x in reals.values()]))

        reals = meta_cow.Layers.getLowerEntitiesByType(ObjType.REAL_OBJECT)
        print ("字符串‘cow’有一个realObject，是({0})".format([x.obj.rid + x.obj.remark for x in reals.values()]))

        reals = meta_cool.Layers.getLowerEntitiesByType(ObjType.REAL_OBJECT)
        print ("字符串‘cool’有一个realObject，是({0})".format([x.obj.rid + x.obj.remark for x in reals.values()]))

        # 应该是['cow', '\xe7\x89\x9b'：牛]
        metas = real_niu.Layers.getUpperEntitiesByType(ObjType.META_DATA)
        print ("实际对象‘牛’有两个metaData，分别是({0})".format([x.obj.mvalue for x in metas.values()]))

        # 应该是['\xe5\x8e\x89\xe5\xae\xb3'：厉害, '\xe7\x89\x9b'：牛]
        metas = real_cool.Layers.getUpperEntitiesByType(ObjType.META_DATA)
        print ("实际对象‘厉害’有两个metaData，分别是({0})".format([x.obj.mvalue for x in metas.values()]))


    def test_getSequenceComponents(self):
        print("----test_getSequenceComponents----")
        meta_tui,real_tui =RealObject.createMetaRealByValue(mvalue="腿")
        meta_tou, real_tou = RealObject.createMetaRealByValue(mvalue="头")
        meta_wei, real_wei = RealObject.createMetaRealByValue(mvalue="尾")

        self.real_niu.Collection.appendElements(*[real_tou,real_tui,real_wei])

        sequence_components = self.real_niu.Constitutions.getSequenceComponents()




    def test_toKnowledge(self):
        print("----test_toKnowledge----")

    def tearDown(self):
        print("----tearDown----")
        # from loongtian.nvwa.models import tables_setting
