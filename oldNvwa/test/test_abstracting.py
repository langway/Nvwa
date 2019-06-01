#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    test_abstracting.py 
Created by zheng on 2015/1/22.
UpdateLog:

"""
from unittest import TestCase
from loongtian.nvwa.service import metadata_srv, original_srv, real_object_srv, knowledge_srv
from loongtian.nvwa.core.engines.abstracting.abstracting_engine import AbstractingEngine


class TestAbstracting(TestCase):
    def __init_some_data__(self):
        metadata_list = []
        list1 = [u'牛', u'羊', u'猪', u'马', u'狗']
        list2 = [u'动物']
        list3 = [u'颜色', u'体型', u'', u'速度']
        list4 = [u'毛', u'头', u'腿']
        list5 = [u'弱小', u'强壮']
        list6 = [u'快', u'慢']
        list7 = [u'红', u'黄', u'绿']

        metadata_list.extend(list1)
        metadata_list.extend(list2)
        metadata_list.extend(list3)
        metadata_list.extend(list4)
        metadata_list.extend(list5)
        metadata_list.extend(list6)
        metadata_list.extend(list7)

        objDic = {}
        for _s in metadata_list:
            metadata_srv.create(_s)
            objDic[_s] = original_srv.InheritFrom.find(right=metadata_srv.get_default_by_string_value(_s))

        for _s in list1:
            # list1继承自动物
            original_srv.InheritFrom.set(objDic[_s][0], objDic[u'动物'][0], knowledge_srv)

            original_srv.Component.set(objDic[_s][0], objDic[u'腿'][0], knowledge_srv)
            original_srv.Component.set(objDic[_s][0], objDic[u'头'][0], knowledge_srv)

        for _s in list1[:3]:
            original_srv.Component.set(objDic[_s][0], objDic[u'毛'][0], knowledge_srv)


    def setUp(self):
        self.__init_some_data__()

    def testAb(self):
        metadata_srv.create(u'猫')
        object1 = original_srv.InheritFrom.find(right=metadata_srv.get_default_by_string_value(u'动物'))
        object2 = original_srv.InheritFrom.find(right=metadata_srv.get_default_by_string_value(u'猫'))
        object3 = original_srv.InheritFrom.find(right=metadata_srv.get_default_by_string_value(u'腿'))

        o1 = original_srv.InheritFrom.set(object2[0], object1[0], knowledge_srv)
        o2 = original_srv.Component.set(object2[0], object3[0], knowledge_srv)

        from loongtian.nvwa.service import fragment_srv

        fragment = fragment_srv.generate(o1, knowledge_srv)
        AbstractingEngine().abstract(fragment)
        pass
