#!/usr/bin/env python
# coding: utf-8

from unittest import TestCase

from loongtian.nvwa.models.enum import ObjType
from loongtian.nvwa.models.metaData import MetaData
from loongtian.nvwa.models.realObject import RealObject
from loongtian.nvwa.models.layer import Layer


class TestMetaData(TestCase):
    def setUp(self):
        print("----setUp----")
        Layer._physicalDeleteAll()
        self.meta = MetaData(type = ObjType.WORD, mvalue = "牛").create()
        for i in range(0, 10):
            real = RealObject().create()
            self.meta.Layers.addLower(real)


    def testCreateMetaData(self):
        print("----testCreateMetaData----")
        print("----测试创建元数据----")
        self.meta_niu = MetaData(type = ObjType.WORD, mvalue = "牛").create()
        self.meta_cow = MetaData(type = ObjType.WORD, mvalue = "cow").create()
        self.meta_cool = MetaData(type = ObjType.WORD, mvalue = "厉害").create()


    def testGetRelatedRealObjsFromDB(self):
        print("----testGetRelatedMetasInDB----")
        reals=self.meta.Layers.getLowerEntitiesByType(ObjType.REAL_OBJECT)
        self.assertEqual(10, len(reals))
        # todo Json.obj2json出错
        # print(Json.obj2json(self.meta, False))

    def testAddRealObject_And_RemoveRealObject(self):
        print("----testAddRealObject_And_RemoveRealObject----")
        reals=self.meta.Layers.getLowerEntitiesByType(ObjType.REAL_OBJECT)
        real = RealObject()
        real.create()
        self.meta.Layers.addLower(real)
        self.meta.Layers.addLower(real)
        self.assertTrue(len(self.meta.Layers.getLowerEntitiesByType(ObjType.REAL_OBJECT)) == 11)
        m = MetaData.getOneInDB(id = self.meta.id)
        reals=m.Layers.getLowerEntitiesByType(ObjType.REAL_OBJECT)
        self.assertEqual(11, len(reals))

        self.meta.Layers.removeLower(real)
        self.assertEqual(10, len(self.meta.Layers.getLowerEntitiesByType(ObjType.REAL_OBJECT)))
        m = MetaData.getOneInDB(id = self.meta.id)
        reals=m.Layers.getLowerEntitiesByType(ObjType.REAL_OBJECT)
        self.assertTrue(len(reals) > 0)
        # todo Json.obj2json出错
        # print(Json.obj2json(m, False))

    def testGetType(self):
        print("----testGetType----")
        # # 创建有 - Has
        # self.metaHas = MetaData(type = ObjType.WORD, mvalue = "有", weight = 999).create()
        # realHas1 = RealObject(pattern = "{0}有{1}", meaning = "{0}组件{1}", remark = "组件有", type = ObjType.ACTION).create()
        # realHas2 = RealObject(pattern = "{0}有{1}", meaning = "{0}属性{1}", remark = "属性有", type = ObjType.ACTION).create()
        # self.metaHas.addRelatedRealObject(realHas1, 0.2)
        # self.metaHas.addRelationWithRealObjInDB(realHas1, 0.2)
        # self.metaHas.addRelatedRealObject(realHas2, 0.3)
        # self.metaHas.addRelationWithRealObjInDB(realHas2, 0.3)
        #
        # # 测试
        # print("%s : %s" % (self.meta.mvalue, self.meta.getTypeNames()))
        # print("%s : %s" % (self.metaHas.mvalue, self.metaHas.getTypeNames()))
        # self.assertTrue(self.meta.isUnclassifiedRealObject())
        # self.assertFalse(self.meta.isAction())
        # self.assertTrue(self.metaHas.isUnclassifiedRealObject())
        # self.assertTrue(self.metaHas.isAction())
        # # 清理有 - Has
        # for real,threshold in self.metaHas.realObjs.values():
        #     real.delete()
        # self.metaHas.delete()

    def tearDown(self):
        print("----tearDown----")

        MetaData._physicalDeleteAll()
        RealObject._physicalDeleteAll()
        Layer._physicalDeleteAll()