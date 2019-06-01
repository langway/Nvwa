#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    ${NAME} 
Author:   fengyh 
DateTime: 2015/5/29 10:38 
UpdateLog:
1、fengyh 2015/5/29 Create this File.


"""
from unittest import TestCase
from loongtian.nvwa.entities.collection import Collection, CollectionUtil
from loongtian.nvwa.service import metadata_srv, knowledge_srv, original_srv


class TestCollectionInitAndUtil(TestCase):
    def init_data(self):
        """
        测试数据"猪有毛"
        :return:
        """
        metadata_list = []
        metadata_list.extend([u'猪', u'有', u'毛'])
        metadata_list.extend([u'马', u'有', u'毛'])
        metadata_list.extend([u'马', u'有', u'腿'])
        for _s in metadata_list:
            metadata_srv.create(_s)

        self.object_pig = original_srv.SymbolInherit.find(right=metadata_srv.get_default_by_string_value(u'猪'))[0]
        self.object_have = original_srv.SymbolInherit.find(right=metadata_srv.get_default_by_string_value(u'有'))[0]
        self.object_hair = original_srv.SymbolInherit.find(right=metadata_srv.get_default_by_string_value(u'毛'))[0]

        self.object_horse = original_srv.SymbolInherit.find(right=metadata_srv.get_default_by_string_value(u'马'))[0]
        self.object_leg = original_srv.SymbolInherit.find(right=metadata_srv.get_default_by_string_value(u'腿'))[0]

        self.pig_have_hair = knowledge_srv.create_t_structure(self.object_pig, self.object_have,
                                                            self.object_hair)
        self.horse_have_hair = knowledge_srv.create_t_structure(self.object_horse, self.object_have,
                                                            self.object_hair)
        self.horse_have_leg = knowledge_srv.create_t_structure(self.object_horse, self.object_have,
                                                            self.object_leg)

    def test_collection_init(self):
        self.init_data()
        c1 = Collection('',self.object_pig)
        self.assertEqual(c1.result_collection.__len__(), 1)

        c2 = Collection('',[self.object_pig, self.object_hair])
        self.assertEqual(c2.result_collection.__len__(), 2)

        self.assertEqual(c2.count(), 2)
        self.assertTrue(c2.is_ordered())

    def test_find_collection_by_collection_id(self):
        self.init_data()
        c2 = Collection('',[self.object_pig, self.object_have, self.object_hair])
        collection_item_list = CollectionUtil.find_collection_by_collection_object(c2.collection_object.Id)

        self.assertEqual(c2.count(), collection_item_list.__len__())


    def test_find_item_in_which_collection(self):
        self.init_data()
        c2 = Collection('',[self.object_pig, self.object_have, self.object_hair])
        collection_contain_pig = CollectionUtil.find_collection_by_item(self.object_pig)
        collection_contain_have = CollectionUtil.find_collection_by_item(self.object_have)
        collection_contain_hair = CollectionUtil.find_collection_by_item(self.object_hair)

        self.assertEqual(c2.count(), collection_contain_pig[0][0].__len__())
        self.assertEqual(c2.count(), collection_contain_have[0][0].__len__())
        self.assertEqual(c2.count(), collection_contain_hair[0][0].__len__())

    def test_find_next_item_in_collection(self):
        self.init_data()
        c2 = Collection('',[self.object_pig, self.object_have, self.object_hair])

        item_pig_next = CollectionUtil.find_next_item_in_collection(self.object_pig)
        self.assertEqual(self.object_have.Id,item_pig_next)

        item_have_next = CollectionUtil.find_next_item_in_collection(self.object_have,c2.collection_object.Id)
        self.assertEqual(self.object_hair.Id,item_have_next)
        pass

    def test_is_sorted(self):
        self.init_data()
        c2 = Collection('',[self.object_pig, self.object_have, self.object_hair])
        self.assertTrue(CollectionUtil.is_sorted(c2.collection_object.Id))

    def test_intersection(self):
        self.init_data()
        c1 = Collection('',[self.object_pig, self.object_have, self.object_hair])
        c2 = Collection('',[self.object_horse, self.object_have, self.object_leg])
        ci = CollectionUtil.intersection(c1.collection_object.Id,c2.collection_object.Id)
        self.assertEqual(ci.__len__(),1)
        self.assertEqual(ci[0],self.object_have.Id)

    def test_union(self):
        self.init_data()
        c1 = Collection('',[self.object_pig, self.object_have, self.object_hair])
        c2 = Collection('',[self.object_horse, self.object_have, self.object_leg])
        ci = CollectionUtil.union(c1.collection_object.Id,c2.collection_object.Id)
        self.assertEqual(ci.__len__(),5)
        self.assertTrue(ci.__contains__(self.object_pig.Id))


    def test_difference(self):
        self.init_data()
        c1 = Collection('',[self.object_pig, self.object_have, self.object_hair])
        c2 = Collection('',[self.object_horse, self.object_have, self.object_leg])
        ci = CollectionUtil.difference(c1.collection_object.Id,c2.collection_object.Id)
        self.assertEqual(ci.__len__(),2)
        self.assertTrue(ci.__contains__(self.object_pig.Id))
        self.assertTrue(ci.__contains__(self.object_hair.Id))

    def test_contain(self):
        self.init_data()
        c1 = Collection('',[self.object_have])
        c2 = Collection('',[self.object_horse, self.object_have, self.object_leg])
        contain1 = CollectionUtil.contain(c2.collection_object.Id,c1.collection_object.Id)
        contain2 = CollectionUtil.contain(c1.collection_object.Id,c2.collection_object.Id)

        self.assertTrue(contain1)
        self.assertFalse(contain2)



