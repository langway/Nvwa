#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase
from loongtian.nvwa.models.enum import ObjType
from loongtian.nvwa.models.metaData import MetaData
from loongtian.nvwa.models.metaNet import MetaNet
from loongtian.nvwa.models.realObject import RealObject
from loongtian.nvwa.models.layer import Layer
from loongtian.util.helper import stringHelper
from loongtian.nvwa.centrals.memoryCentral import MemoryCentral

class TestLayer(TestCase):

    def setUp(self):
        print("----setUp----")

        self.memoryCentral=MemoryCentral(None)
        Layer._physicalDeleteAll()
        self.metas=[]
        self.reals=[]
        self.metanets=[]
        self.layers=[]
        for i in range(5):
            # 创建MetaData
            temp_meta=MetaData(str(i),mvalue = str(i))
            # temp_meta=temp_meta.create()
            self.metas.append(temp_meta)
            self.memoryCentral.addMetaInMemory(temp_meta)

            # 创建MetaNet
            if i>0:
                last_meta=self.metas[i - 1]
                temp_metanet=MetaNet.createMetaNetByStartEnd(last_meta,temp_meta,mnid=last_meta.mvalue+","+temp_meta.mvalue)
                self.metanets.append(temp_metanet)
                temp_layer=Layer.createLayerByUpperAndLowerInDB(temp_metanet,last_meta)
                self.layers.append(temp_layer)

            # 创建MetaData关联的RealObject
            for j in range(4):
                temp_real=RealObject(stringHelper.arabicNumeral_to_chineseNumeral(j))
                # temp_real=temp_real.create()
                self.reals.append(temp_real)
                self.memoryCentral.WorkingMemory.addInMemory(temp_real)

                temp_layer=Layer.createLayerByUpperAndLowerInDB(temp_meta,temp_real,weight=i*j)
                self.layers.append(temp_layer)
                self.assertIsNotNone(temp_layer)


    def testCreateLayerByUpperLower(self):
        print("——testCreateLayerByUpperLower——")
        layer=Layer.createLayerByUpperAndLowerInDB(self.metas[0],self.reals[0])
        self.assertIsNotNone(layer)

    def testGetUpperItem(self):
        print("——testGetUpperItem——")
        layer=Layer(self.metas[0],self.reals[0])
        upper=layer.getUpperItem()
        self.assertIsNotNone(upper)

    def testGetLowerItem(self):
        print("——testGetLowerItem——")
        layer=Layer(self.metas[0],self.reals[0])
        lower=layer.getLowerItem()
        self.assertIsNotNone(lower)

    def testGetLayerByUpperAndLower(self):
        print("——testGetLayerByUpperAndLower——")
        layer=Layer.getLayerByUpperAndLower(self.metas[0],self.reals[0],self.memoryCentral)
        self.assertIsNotNone(layer)

    def testGetLowersByUpperInDB(self):
        print("——testGetLowersByUpperInDB——")

        lowers=Layer.getLowersByUpperInDB(self.metas[0])
        self.assertIsNotNone(lowers)
        self.assertEqual(len(lowers),4)

    def testGetUppersByLowerInDB(self):
        print("——testGetUppersByLowerInDB——")

        uppers=Layer.getUppersByLowerInDB(self.reals[0])
        self.assertIsNotNone(uppers)
        self.assertEqual(len(uppers),5)


    def test_getUpperEntities(self):
        print("——testGetLowersByUpperInDB——")

        uppers=self.reals[2].Layers.getUpperEntities()
        self.assertIsNotNone(uppers)
        self.assertEqual(len(uppers),5)
        self.assertEqual(uppers["3"].weight, 6.0)

    def test_getLowerEntities(self):
        print("——test_getLowerEntities——")

        lowers=self.metas[3].Layers.getLowerEntities()
        self.assertIsNotNone(lowers)
        self.assertEqual(len(lowers),4)
        self.assertEqual(lowers[u"三"].weight, 9.0)

    def testGetTypedUppersByLowerInDB(self):
        print("——testGetUppersByLowerInDB——")
        typed_uppers=Layer.getTypedUppersByLowerInDB(self.reals[0], ObjType.META_DATA)
        self.assertEqual(len(typed_uppers),5)

        typed_uppers=Layer.getTypedUppersByLowerInDB(self.reals[0], ObjType.META_NET)
        self.assertIsNone(typed_uppers)

        typed_uppers=Layer.getTypedUppersByLowerInDB(self.metas[0], ObjType.META_NET)
        self.assertEqual(type(typed_uppers),Layer)

    def test_getUpperEntitiesByType(self):
        print("——test_getUpperEntitiesByType——")
        typed_uppers=self.reals[2].Layers.getUpperEntitiesByType(ObjType.META_DATA)
        self.assertEqual(len(typed_uppers),5)

        typed_uppers=self.reals[2].Layers.getUpperEntitiesByType(ObjType.META_NET)
        self.assertIsNone(typed_uppers)

        typed_uppers=self.metas[2].Layers.getUpperEntitiesByType(ObjType.META_NET)
        self.assertIsNotNone(typed_uppers)
        self.assertEqual(typed_uppers.values()[0].obj,self.metanets[2])

    def test_getLowerEntitiesByType(self):
        print("——test_getLowerEntitiesByType——")
        typed_lowers=self.metanets[2].Layers.getLowerEntitiesByType(ObjType.META_DATA)
        self.assertEqual(len(typed_lowers),1)

        typed_lowers=self.reals[2].Layers.getLowerEntitiesByType(ObjType.META_NET)
        self.assertIsNone(typed_lowers)

        typed_lowers=self.metas[2].Layers.getLowerEntitiesByType(ObjType.REAL_OBJECT)
        self.assertIsNotNone(typed_lowers)
        self.assertEqual(typed_lowers[u"一"].obj.rid,self.reals[1].rid)

    def testGetTypedLowersByUpperInDB(self):
        print("——testGetTypedLowersByUpperInDB——")
        typed_lowers=Layer.getTypedLowersByUpperInDB(self.metanets[0], ObjType.META_DATA)
        self.assertEqual(type(typed_lowers),Layer)

        typed_lowers=Layer.getTypedLowersByUpperInDB(self.metas[0], ObjType.META_NET)
        self.assertIsNone(typed_lowers)

        typed_lowers=Layer.getTypedLowersByUpperInDB(self.metas[0], ObjType.REAL_OBJECT)
        self.assertEqual(len(typed_lowers),4)

    def test_getAllRelatedRealObjsInMetaChain(self):
        print("——test_getAllRelatedRealObjsInMetaChain——")
        meta_chain=[self.metas[1],self.metas[2],self.metas[3]]
        realLowerObjs, sorted_realsChain=MetaData.getAllRelatedRealObjsInMetaChain(meta_chain)
        self.assertIsNotNone(realLowerObjs)
        self.assertIsNotNone(sorted_realsChain)
        # 未排序状态，是个dict
        self.assertEqual(realLowerObjs[0][u'三'].weight,3.0)
        # 排序状态，根据权重，最大值
        self.assertEqual(sorted_realsChain[0][0].weight, 3.0)



    def testDeleteByUpper(self):
        print("——testDeleteByUpper——")

        affectedRowsNum=Layer.deleteByUpper(self.metas[0])
        layers=Layer.getAllByConditionsInDB(memory=self.memoryCentral,isdel=True)
        self.   assertEqual(affectedRowsNum,4)
        self.assertEqual(len(layers),4)


    def testDeleteByLower(self):
        print("——testDeleteByLower——")

        affectedRowsNum=Layer.deleteByLower(self.metas[0]) # 根据metadata删除metanet
        layers=Layer.getAllByConditionsInDB(memory=self.memoryCentral,isdel=True)
        self.assertEqual(affectedRowsNum,1)
        self.assertIs(type(layers),Layer)

        affectedRowsNum=Layer.deleteByLower(self.metanets[0])
        layers=Layer.getAllByConditionsInDB(memory=self.memoryCentral,isdel=True)
        self.assertEqual(affectedRowsNum,0)
        self.assertIs(type(layers),Layer)

        affectedRowsNum=Layer.deleteByLower(self.reals[0])
        layers=Layer.getAllByConditionsInDB(memory=self.memoryCentral,isdel=True)
        self.assertEqual(affectedRowsNum,5)
        self.assertEqual(len(layers),6)


    def testDeleteByUpperAndLower(self):
        print("——testDeleteByLower——")

        affectedRowsNum=Layer.deleteByUpperAndLower(self.metas[0],self.reals[0])
        self.assertEqual(affectedRowsNum,1)


    def test_physicalDeleteByUpper(self):
        print("——test_physicalDeleteByUpper——")

        affectedRowsNum=Layer._physicalDeleteByUpper(self.metas[0])
        self.assertEqual(affectedRowsNum,4)


    def test_physicalDeleteByLower(self):
        print("——test_physicalDeleteByLower——")

        affectedRowsNum=Layer._physicalDeleteByLower(self.metas[0]) # 根据metadata删除metanet
        self.assertEqual(affectedRowsNum,1)

        affectedRowsNum=Layer._physicalDeleteByLower(self.metanets[0])
        self.assertEqual(affectedRowsNum,0)

        affectedRowsNum=Layer._physicalDeleteByLower(self.reals[0])
        self.assertEqual(affectedRowsNum,5)


    def test_physicalDeleteByUpperAndLower(self):
        print("——test_physicalDeleteByLower——")

        affectedRowsNum=Layer._physicalDeleteByUpperAndLower(self.metas[0],self.reals[0])
        self.assertEqual(affectedRowsNum,1)








    def tearDown(self):
        print("----tearDown----")
        Layer._physicalDeleteAll()











