#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    test_base 
Author:   fengyh 
DateTime: 2015/1/14 16:11 
UpdateLog:
1、fengyh 2015/1/14 Create this File.
2、fengyh 2015/2/3 处理因继承自功能调整引起的变化。修改造数据方法。

"""
from unittest import TestCase
from loongtian.nvwa.core.gdef import OID
from loongtian.nvwa.service import metadata_srv, real_object_srv, memory_srv, fsc, original_srv, fragment_srv, \
    original_init_srv, knowledge_srv


class TestBase(TestCase):
    """
    fengyh 2015-1-15
    测试用基类，主要是为了造数据为具体测试用。
    """

    def __init_some_data_tree__(self):
        metadata_list = []
        metadata_list.extend([u'动物', u'哺乳动物', u'家畜', u'马'])
        metadata_list.extend([u'形容厉害', u'猛'])
        metadata_list.extend([u'牛'])
        metadata_list.extend([u'动词', u'存现动词', u'在', u'动作动词', u'使令动词'])
        metadata_list.extend([u'食物', u'猪蹄'])
        metadata_list.extend([u'四肢', u'胳膊'])
        metadata_list.extend([u'依靠', u'靠山', u'后台'])
        metadata_list.extend([u'腿'])
        for _s in metadata_list:
            metadata_srv.create(_s)

        # 马继承自家畜
        object1 = original_srv.SymbolInherit.find(right=metadata_srv.get_default_by_string_value(u'马'))
        object2 = original_srv.SymbolInherit.find(right=metadata_srv.get_default_by_string_value(u'家畜'))
        original_srv.InheritFrom.set(object1[0], object2[0],knowledge_srv)
        # 牛继承自家畜
        object1 = original_srv.SymbolInherit.find(right=metadata_srv.get_default_by_string_value(u'牛'))
        original_srv.InheritFrom.set(object1[0], object2[0],knowledge_srv)
        # 家畜继承自哺乳动物
        object1 = original_srv.SymbolInherit.find(right=metadata_srv.get_default_by_string_value(u'哺乳动物'))
        original_srv.InheritFrom.set(object2[0], object1[0],
                                     knowledge_srv)
        # 哺乳动物继承自动物
        object2 = original_srv.SymbolInherit.find(right=metadata_srv.get_default_by_string_value(u'动物'))
        original_srv.InheritFrom.set(object1[0], object2[0],
                                     knowledge_srv)

        # 猛继承形容厉害
        object1 = original_srv.SymbolInherit.find(right=metadata_srv.get_default_by_string_value(u'猛'))
        object2 = original_srv.SymbolInherit.find(right=metadata_srv.get_default_by_string_value(u'形容厉害'))
        original_srv.InheritFrom.set(object1[0], object2[0],
                                     knowledge_srv)

        _new_object = real_object_srv.create(Display=u'牛（猛牛）')
        # 猛牛继承自牛C
        original_srv.SymbolInherit.set(_new_object, metadata_srv.get_default_by_string_value(u'牛'), knowledge_srv)
        # 猛牛继承自形容厉害
        original_srv.InheritFrom.set(_new_object, object2[0],
                                     knowledge_srv)


        # 存现动词继承自动词
        object1 = original_srv.SymbolInherit.find(right=metadata_srv.get_default_by_string_value(u'存现动词'))
        object2 = original_srv.SymbolInherit.find(right=metadata_srv.get_default_by_string_value(u'动词'))
        original_srv.InheritFrom.set(object1[0], object2[0],
                                     knowledge_srv)

        # 动作动词继承自动词
        object1 = original_srv.SymbolInherit.find(right=metadata_srv.get_default_by_string_value(u'动作动词'))
        original_srv.InheritFrom.set(object1[0], object2[0],
                                     knowledge_srv)

        # 使令动词继承自动词
        object1 = original_srv.SymbolInherit.find(right=metadata_srv.get_default_by_string_value(u'使令动词'))
        original_srv.InheritFrom.set(object1[0], object2[0],
                                     knowledge_srv)

        # 有继承自存现动词
        object1 = original_srv.SymbolInherit.find(right=metadata_srv.get_default_by_string_value(u'有'))
        object2 = original_srv.SymbolInherit.find(right=metadata_srv.get_default_by_string_value(u'存现动词'))
        original_srv.InheritFrom.set(object1[0], object2[0],
                                     knowledge_srv)
        # 在继承自存现动词
        object1 = original_srv.SymbolInherit.find(right=metadata_srv.get_default_by_string_value(u'在'))
        original_srv.InheritFrom.set(object1[0], object2[0],
                                     knowledge_srv)

        # 胳膊继承自躯干
        object1 = original_srv.SymbolInherit.find(right=metadata_srv.get_default_by_string_value(u'胳膊'))
        object2 = original_srv.SymbolInherit.find(right=metadata_srv.get_default_by_string_value(u'四肢'))
        original_srv.InheritFrom.set(object1[0], object2[0],
                                     knowledge_srv)
        # 腿继承自躯干
        object1 = original_srv.SymbolInherit.find(right=metadata_srv.get_default_by_string_value(u'腿'))
        original_srv.InheritFrom.set(object1[0], object2[0],
                                     knowledge_srv)
        # 猪蹄继承自食物
        object1 = original_srv.SymbolInherit.find(right=metadata_srv.get_default_by_string_value(u'猪蹄'))
        object2 = original_srv.SymbolInherit.find(right=metadata_srv.get_default_by_string_value(u'食物'))
        original_srv.InheritFrom.set(object1[0], object2[0],
                                     knowledge_srv)
        # 腿继承自食物
        object1 = original_srv.SymbolInherit.find(right=metadata_srv.get_default_by_string_value(u'腿'))
        original_srv.InheritFrom.set(object1[0], object2[0],
                                     knowledge_srv)

        # 靠山继承自依靠
        object1 = original_srv.SymbolInherit.find(right=metadata_srv.get_default_by_string_value(u'靠山'))
        object2 = original_srv.SymbolInherit.find(right=metadata_srv.get_default_by_string_value(u'依靠'))
        original_srv.InheritFrom.set(object1[0], object2[0],
                                     knowledge_srv)
        # 后台继承自依靠
        object1 = original_srv.SymbolInherit.find(right=metadata_srv.get_default_by_string_value(u'后台'))
        original_srv.InheritFrom.set(object1[0], object2[0],
                                     knowledge_srv)

        _new_object = real_object_srv.create(Display=u'腿（抱大腿）')
        # 抱大腿继承自腿C
        original_srv.SymbolInherit.set(_new_object, metadata_srv.get_default_by_string_value(u'腿'), knowledge_srv)
        # 抱大腿继承自依靠
        original_srv.InheritFrom.set(_new_object, object2[0],
                                     knowledge_srv)

    def setUp(self):
        original_init_srv.init()

        # 女娲本我Id
        self.nvwa_self = real_object_srv.get(OID.InnerSelf)
        # 女娲接收Id
        self.receive = real_object_srv.get(OID.Receive)
        # 女娲理解为Id
        self.understand = real_object_srv.get(OID.UnderstoodAs)
        # 时间为
        self.timeis = real_object_srv.get(OID.TimeIs)
        # 感知器
        self.sensor = real_object_srv.get(OID.SensorIs)
        # 感知器控制台
        self.sensor_console = real_object_srv.get(OID.Console)

        self.meta_pig = metadata_srv.create(u"猪")
        self.object_unknown_pig = metadata_srv.get_default_by_string_value(u'猪')
        self.object_word_pig = metadata_srv.get_word_by_string_value(u'猪')

        self.meta_hair = metadata_srv.create(u"毛")
        self.object_unknown_hair = metadata_srv.get_default_by_string_value(u'毛')
        self.object_word_hair = metadata_srv.get_word_by_string_value(u'毛')

        self.object_unknown_have = metadata_srv.get_default_by_string_value(u'有')
        self.object_word_have = metadata_srv.get_word_by_string_value(u'有')

        self.__init_some_data_tree__()

        self.__gen_memory_one_time__()

    def __gen_memory_one_time__(self):
        self.memory_word = memory_srv.create_t_structure(self.object_word_pig, self.object_word_have,
                                                         self.object_word_hair)
        # 女娲理解为XXX意思
        self.memory_understand = memory_srv.create_t_structure(self.object_unknown_pig, self.object_unknown_have,
                                                               self.object_unknown_hair)
        _frag1 = fsc.memory.assemble(memory_srv,
                                     observer=real_object_srv.get(OID.God),
                                     sensor=original_srv.Console.obj(),
                                     time=original_srv.create_time_real_object(),
                                     mood=original_srv.Declarative.obj(),
                                     understand=self.memory_understand,
                                     receive=self.memory_word)

        fragment_srv.save_to_target_service(_frag1, memory_srv)

    def tearDown(self):
        pass
