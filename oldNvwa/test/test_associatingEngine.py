#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    ${NAME} 
Author:   fengyh 
DateTime: 2014/12/8 16:48 
UpdateLog:
1、fengyh 2014/12/8 Create this File.
2、fengyh 2015/1/25 按新的类比算法测试
3、fengyh 2015/1/26 将原来旧的类比规则测试迁移出去成单独的测试

"""
import operator
from loongtian.nvwa.core.engines.associating.associating_engine import AssociatingEngine
from loongtian.nvwa.service import metadata_srv, original_srv, knowledge_srv
from loongtian.nvwa.service import fragment_srv
from test.test_base import TestBase


class TestAssociatingEngine(TestBase):
    def test_associate_rule3_1(self):
        _rep_srv = fragment_srv.get_new_knowledge_for_fragment_service()

        cow_object = metadata_srv.get_default_by_string_value(u'牛')
        cow_children = original_srv.SymbolInherit.find(right=cow_object)
        # 按生成时间排序，保证顺序不随机
        cow_children.sort(key=operator.attrgetter("ThresholdTime"), reverse=False)
        # available
        # cow_children =  sorted(cow_children,key=operator.attrgetter("ThresholdTime"),reverse=True)

        # 第一组先测试“动物牛”
        cow_object = cow_children[0]
        have_object = metadata_srv.get_default_by_string_value(u'有')
        have_object = original_srv.SymbolInherit.find(right=have_object)[0]
        leg_object = metadata_srv.get_default_by_string_value(u'腿')
        leg_object_children = original_srv.SymbolInherit.find(right=leg_object)
        leg_object_children.sort(key=operator.attrgetter("ThresholdTime"), reverse=False)
        leg_object = leg_object_children[0]

        cow_have_leg = _rep_srv.create_t_structure(cow_object, have_object, leg_object)
        cow_have_leg_frag = fragment_srv.generate(cow_have_leg, _rep_srv)
        frag_list = [cow_have_leg_frag]
        associating = AssociatingEngine(frag_list)

        associating.run()
        # 系统中没有任何原始知识，类比结果为0
        self.assertEqual(0, associating.match_result_list[0].__len__())

        # 增加第一条原始数据之后，可以找到一条命中记录
        fragment_srv.save_to_target_service(cow_have_leg_frag, knowledge_srv)
        associating = AssociatingEngine(frag_list)
        associating.run()
        self.assertEqual(1, associating.match_result_list[0].__len__())

        # 增加第二条原始数据后，可以找到两条命中记录
        cow_object = metadata_srv.get_default_by_string_value(u'哺乳动物')
        cow_object = original_srv.SymbolInherit.find(right=cow_object)[0]
        have_object = metadata_srv.get_default_by_string_value(u'有')
        have_object = original_srv.SymbolInherit.find(right=have_object)[0]
        leg_object = metadata_srv.get_default_by_string_value(u'四肢')
        leg_object = original_srv.SymbolInherit.find(right=leg_object)[0]
        cow_have_leg = _rep_srv.create_t_structure(cow_object, have_object, leg_object)
        cow_have_leg_frag = fragment_srv.generate(cow_have_leg, _rep_srv)

        fragment_srv.save_to_target_service(cow_have_leg_frag, knowledge_srv)
        associating = AssociatingEngine(frag_list)
        associating.run()
        self.assertEqual(2, associating.match_result_list[0].__len__())
        pass

    def test_associate_rule3_2(self):
        _rep_srv = fragment_srv.get_new_knowledge_for_fragment_service()

        cow_object = metadata_srv.get_default_by_string_value(u'牛')
        cow_children = original_srv.SymbolInherit.find(right=cow_object)
        # 按生成时间排序，保证顺序不随机
        cow_children.sort(key=operator.attrgetter("ThresholdTime"), reverse=False)
        # available
        # cow_children =  sorted(cow_children,key=operator.attrgetter("ThresholdTime"),reverse=True)

        # 第一组先测试“厉害牛”
        cow_object = cow_children[1]
        have_object = metadata_srv.get_default_by_string_value(u'有')
        have_object = original_srv.SymbolInherit.find(right=have_object)[0]
        leg_object = metadata_srv.get_default_by_string_value(u'腿')
        leg_object = original_srv.SymbolInherit.find(right=leg_object)[0]

        cow_have_leg = _rep_srv.create_t_structure(cow_object, have_object, leg_object)
        cow_have_leg_frag = fragment_srv.generate(cow_have_leg, _rep_srv)
        frag_list = [cow_have_leg_frag]
        associating = AssociatingEngine(frag_list)

        associating.run()
        # 系统中没有任何原始知识，类比结果为0
        self.assertEqual(0, associating.match_result_list[0].__len__())

        # 增加第一条原始数据之后，可以找到一条命中记录
        fragment_srv.save_to_target_service(cow_have_leg_frag, knowledge_srv)
        associating = AssociatingEngine(frag_list)
        associating.run()
        self.assertEqual(1, associating.match_result_list.__len__())

        # 增加第二条原始数据后，可以找到两条命中记录
        cow_object = metadata_srv.get_default_by_string_value(u'哺乳动物')
        cow_object = original_srv.SymbolInherit.find(right=cow_object)[0]
        have_object = metadata_srv.get_default_by_string_value(u'有')
        have_object = original_srv.SymbolInherit.find(right=have_object)[0]
        leg_object = metadata_srv.get_default_by_string_value(u'四肢')
        leg_object = original_srv.SymbolInherit.find(right=leg_object)[0]
        cow_have_leg = _rep_srv.create_t_structure(cow_object, have_object, leg_object)
        cow_have_leg_frag = fragment_srv.generate(cow_have_leg, _rep_srv)

        fragment_srv.save_to_target_service(cow_have_leg_frag, knowledge_srv)
        associating = AssociatingEngine(frag_list)
        associating.run()
        self.assertEqual(1, associating.match_result_list[0].__len__())
        pass

    def test_associate_rule3_3(self):
        _rep_srv = fragment_srv.get_new_knowledge_for_fragment_service()

        cow_object = metadata_srv.get_default_by_string_value(u'牛')
        cow_children = original_srv.SymbolInherit.find(right=cow_object)
        # 按生成时间排序，保证顺序不随机
        cow_children.sort(key=operator.attrgetter("ThresholdTime"), reverse=False)
        # available
        # cow_children =  sorted(cow_children,key=operator.attrgetter("ThresholdTime"),reverse=True)

        # 第一组先测试“动物牛”
        cow_object = cow_children[0]
        have_object = metadata_srv.get_default_by_string_value(u'有')
        have_object = original_srv.SymbolInherit.find(right=have_object)[0]
        leg_object = metadata_srv.get_default_by_string_value(u'腿')
        leg_object_children = original_srv.SymbolInherit.find(right=leg_object)
        leg_object_children.sort(key=operator.attrgetter("ThresholdTime"), reverse=False)
        leg_object = leg_object_children[0]

        cow_have_leg = _rep_srv.create_t_structure(cow_object, have_object, leg_object)
        cow_have_leg_frag = fragment_srv.generate(cow_have_leg, _rep_srv)
        frag_list = [cow_have_leg_frag]
        # 增加第一条原始数据之后，可以找到一条命中记录
        fragment_srv.save_to_target_service(cow_have_leg_frag, knowledge_srv)
        # 增加第二条原始数据
        animal_object = metadata_srv.get_default_by_string_value(u'动物')
        animal_object = original_srv.SymbolInherit.find(right=animal_object)[0]
        have_object = metadata_srv.get_default_by_string_value(u'有')
        have_object = original_srv.SymbolInherit.find(right=have_object)[0]
        leg_object = metadata_srv.get_default_by_string_value(u'胳膊')
        leg_object = original_srv.SymbolInherit.find(right=leg_object)[0]
        cow_have_leg = _rep_srv.create_t_structure(animal_object, have_object, leg_object)
        cow_have_leg_frag = fragment_srv.generate(cow_have_leg, _rep_srv)
        fragment_srv.save_to_target_service(cow_have_leg_frag, knowledge_srv)

        # 增加第三条原始数据
        mammal_object = metadata_srv.get_default_by_string_value(u'哺乳动物')
        mammal_object = original_srv.SymbolInherit.find(right=mammal_object)[0]
        have_object = metadata_srv.get_default_by_string_value(u'有')
        have_object = original_srv.SymbolInherit.find(right=have_object)[0]
        leg_object = metadata_srv.get_default_by_string_value(u'四肢')
        leg_object = original_srv.SymbolInherit.find(right=leg_object)[0]
        cow_have_leg = _rep_srv.create_t_structure(mammal_object, have_object, leg_object)
        cow_have_leg_frag = fragment_srv.generate(cow_have_leg, _rep_srv)
        fragment_srv.save_to_target_service(cow_have_leg_frag, knowledge_srv)

        associating = AssociatingEngine(frag_list)
        associating.run()
        self.assertEqual(3, associating.match_result_list[0].__len__())
        self.assertTrue(cow_object in associating.match_result_list[0][0].data)
        self.assertTrue(mammal_object in associating.match_result_list[0][1].data)
        self.assertTrue(animal_object in associating.match_result_list[0][2].data)
        pass

