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
            temp_meta=MetaData(str(i),mvalue = str(i),memory=self.memoryCentral).create()
            # temp_meta=temp_meta.create()
            self.metas.append(temp_meta)


            # 创建MetaNet
            if i>0:
                last_meta=self.metas[i - 1]
                temp_metanet=MetaNet.createByStartEnd(last_meta,temp_meta,
                                                      id=last_meta.mvalue+","+temp_meta.mvalue,
                                                      memory = self.memoryCentral)
                self.metanets.append(temp_metanet)
                temp_layer=Layer.createByStartAndEnd(temp_metanet,last_meta,
                                                     memory=self.memoryCentral)
                self.layers.append(temp_layer)

            # 创建MetaData关联的RealObject
            for j in range(4):
                temp_real=RealObject(stringHelper.arabicNumeral_to_chineseNumeral(j),
                                     memory=self.memoryCentral).create()
                # temp_real=temp_real.create()
                self.reals.append(temp_real)

                temp_layer=Layer.createByStartAndEnd(temp_meta,temp_real,weight=i*j,
                                                     memory=self.memoryCentral)
                self.layers.append(temp_layer)
                self.assertIsNotNone(temp_layer)


    def testCreateLayerByStartEnd(self):
        print("——testCreateLayerByStartEnd——")
        layer=Layer.createByStartAndEndInDB(self.metas[0],self.reals[0])
        self.assertIsNotNone(layer)

    def testGetStartItem(self):
        print("——testGetStartItem——")
        layer=Layer(self.metas[0],self.reals[0])
        upper=layer.getStartItem()
        self.assertIsNotNone(upper)

    def testGetEndItem(self):
        print("——testGetEndItem——")
        layer=Layer(self.metas[0],self.reals[0])
        lower=layer.getEndItem()
        self.assertIsNotNone(lower)

    def testGetLayerByStartAndEnd(self):
        print("——testGetLayerByStartAndEnd——")
        layer=Layer.getByStartAndEnd(self.metas[0],self.reals[0],self.memoryCentral)
        self.assertIsNotNone(layer)

    def testGetEndsByStartInDB(self):
        print("——testGetEndsByStartInDB——")

        lowers=Layer.getEndsByStartInDB(self.metas[0])
        self.assertIsNotNone(lowers)
        self.assertEqual(len(lowers),4)

    def testGetStartsByEndInDB(self):
        print("——testGetStartsByEndInDB——")

        uppers=Layer.getStartsByEndInDB(self.reals[0])
        self.assertIsNotNone(uppers)
        self.assertEqual(len(uppers),5)


    def test_getStartEntities(self):
        print("——testGetEndsByStartInDB——")

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

    def testGetTypedStartsByEndInDB(self):
        print("——testGetStartsByEndInDB——")
        typed_uppers=Layer.getTypedStartsByEndInDB(self.reals[0], ObjType.META_DATA)
        self.assertEqual(len(typed_uppers),5)

        typed_uppers=Layer.getTypedStartsByEndInDB(self.reals[0], ObjType.META_NET)
        self.assertIsNone(typed_uppers)

        typed_uppers=Layer.getTypedStartsByEndInDB(self.metas[0], ObjType.META_NET)
        self.assertEqual(type(typed_uppers),Layer)

    def test_getStartEntitiesByType(self):
        print("——test_getStartEntitiesByType——")
        typed_uppers=self.reals[2].Layers.getUpperEntitiesByType(ObjType.META_DATA)
        self.assertEqual(len(typed_uppers),5)

        typed_uppers=self.reals[2].Layers.getUpperEntitiesByType(ObjType.META_NET)
        self.assertIsNone(typed_uppers)

        typed_uppers=self.metas[2].Layers.getUpperEntitiesByType(ObjType.META_NET)
        self.assertIsNotNone(typed_uppers)
        self.assertEqual(list(typed_uppers.values())[0].obj,self.metanets[2])

    def test_getLowerEntitiesByType(self):
        print("——test_getLowerEntitiesByType——")
        typed_lowers=self.metanets[2].Layers.getLowerEntitiesByType(ObjType.META_DATA)
        self.assertEqual(len(typed_lowers),1)

        typed_lowers=self.reals[2].Layers.getLowerEntitiesByType(ObjType.META_NET)
        self.assertIsNone(typed_lowers)

        typed_lowers=self.metas[2].Layers.getLowerEntitiesByType(ObjType.REAL_OBJECT)
        self.assertIsNotNone(typed_lowers)
        self.assertEqual(typed_lowers[u"一"].obj.id,self.reals[1].id)

    def testGetTypedEndsByStartInDB(self):
        print("——testGetTypedEndsByStartInDB——")
        typed_lowers=Layer.getTypedEndsByStartInDB(self.metanets[0], ObjType.META_DATA)
        self.assertEqual(type(typed_lowers),Layer)

        typed_lowers=Layer.getTypedEndsByStartInDB(self.metas[0], ObjType.META_NET)
        self.assertIsNone(typed_lowers)

        typed_lowers=Layer.getTypedEndsByStartInDB(self.metas[0], ObjType.REAL_OBJECT)
        self.assertEqual(len(typed_lowers),4)

    def test_getAllRelatedRealObjsInMetaChain(self):
        print("——test_getAllRelatedRealObjsInMetaChain——")
        meta_chain=[self.metas[1],self.metas[2],self.metas[3]]
        realEndObjs, sorted_realsChain=MetaData.getAllRelatedRealObjsInMetaChain(meta_chain)
        self.assertIsNotNone(realEndObjs)
        self.assertIsNotNone(sorted_realsChain)
        # 未排序状态，是个dict
        self.assertEqual(realEndObjs[0][u'三'].weight,3.0)
        # 排序状态，根据权重，最大值
        self.assertEqual(sorted_realsChain[0][0].weight, 3.0)



    def testDeleteByStart(self):
        print("——testDeleteByStart——")

        affectedRowsNum=Layer.deleteByStart(self.metas[0])
        layers=Layer.getAllByConditionsInDB(memory=self.memoryCentral,status=0)
        self.   assertEqual(affectedRowsNum,4)
        self.assertEqual(len(layers),4)


    def testDeleteByEnd(self):
        print("——testDeleteByEnd——")

        affectedRowsNum=Layer.deleteByEnd(self.metas[0]) # 根据metadata删除metanet
        layers=Layer.getAllByConditionsInDB(memory=self.memoryCentral,status=0)
        self.assertEqual(affectedRowsNum,1)
        self.assertIs(type(layers),Layer)

        affectedRowsNum=Layer.deleteByEnd(self.metanets[0])
        layers=Layer.getAllByConditionsInDB(memory=self.memoryCentral,status=0)
        self.assertEqual(affectedRowsNum,0)
        self.assertIs(type(layers),Layer)

        affectedRowsNum=Layer.deleteByEnd(self.reals[0])
        layers=Layer.getAllByConditionsInDB(memory=self.memoryCentral,status=0)
        self.assertEqual(affectedRowsNum,5)
        self.assertEqual(len(layers),6)


    def testDeleteByStartAndEnd(self):
        print("——testDeleteByEnd——")

        affectedRowsNum=Layer.deleteByStartAndEnd(self.metas[0],self.reals[0])
        self.assertEqual(affectedRowsNum,1)


    def test_physicalDeleteByStart(self):
        print("——test_physicalDeleteByStart——")

        affectedRowsNum=Layer._physicalDeleteByStart(self.metas[0])
        self.assertEqual(affectedRowsNum,4)


    def test_physicalDeleteByEnd(self):
        print("——test_physicalDeleteByEnd——")

        affectedRowsNum=Layer._physicalDeleteByEnd(self.metas[0]) # 根据metadata删除metanet
        self.assertEqual(affectedRowsNum,1)

        affectedRowsNum=Layer._physicalDeleteByEnd(self.metanets[0]) # 已经删除过了
        self.assertEqual(affectedRowsNum,-1)

        affectedRowsNum=Layer._physicalDeleteByEnd(self.reals[0])
        self.assertEqual(affectedRowsNum,5)


    def test_physicalDeleteByStartAndEnd(self):
        print("——test_physicalDeleteByEnd——")

        affectedRowsNum=Layer._physicalDeleteByStartAndEnd(self.metas[0],self.reals[0])
        self.assertEqual(affectedRowsNum,1)








    def tearDown(self):
        print("----tearDown----")
        Layer._physicalDeleteAll()











