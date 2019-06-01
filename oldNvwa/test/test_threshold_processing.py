#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    ${NAME} 
Author:   fengyh 
DateTime: 2015/1/14 9:51 
UpdateLog:
1、fengyh 2015/1/14 Create this File.


"""
from loongtian.nvwa.core.engines.threshold.processing import entity_threshold_decrease, \
    get_lowest_threshold_object_from_metadata, ThresholdProcess
from loongtian.nvwa.entities.const_values import ConstValues
from loongtian.nvwa.service import real_object_srv, original_srv, memory_srv, fragment_srv
from test.test_base import TestBase


class TestThresholdProcessing(TestBase):
    def test_set_threshold(self):
        old_threshold_value = self.object_unknown_pig.Threshold
        old_threshold_time = self.object_unknown_pig.ThresholdTime

        ### 指定对象阈值衰减调用示例
        entity_threshold_decrease(self.object_unknown_pig, 0.8)

        obj_new = real_object_srv.get(self.object_unknown_pig.Id)
        new_threshold_value = obj_new.Threshold
        new_threshold_time = obj_new.ThresholdTime

        self.assertLess(new_threshold_value, old_threshold_value)
        self.assertGreater(new_threshold_time, old_threshold_time)

        # ##
        memory_1 = original_srv.Component.set(self.object_unknown_pig, self.object_unknown_hair, memory_srv)
        old_threshold_value = memory_1.Threshold
        old_threshold_time = memory_1.ThresholdTime

        entity_threshold_decrease(memory_1, 0.2)

        obj_new = memory_srv.get(memory_1.Id)
        new_threshold_value = obj_new.Threshold
        new_threshold_time = obj_new.ThresholdTime
        self.assertLess(new_threshold_value, old_threshold_value)
        self.assertGreaterEqual(new_threshold_time, old_threshold_time)

    def test_set_fragment_threshold(self):
        object_pig_have = memory_srv.base_select_start_end(self.object_unknown_pig.Id,self.object_unknown_have.Id)
        object_pig_have_frag = fragment_srv.generate(object_pig_have, memory_srv)
        object_pig_have_frag_list = fragment_srv.select_all_outer(object_pig_have_frag)

        ready_fragment = object_pig_have_frag_list[0]
        ### fragment对象阈值衰减调用示例
        tp = ThresholdProcess(ready_fragment)
        tp.run_decrease()

        # 判断阈值衰减后是否各数据都已处理
        self.assertLess(real_object_srv.get(self.object_word_pig.Id).Threshold,ConstValues.threshold_initial_value)
        self.assertLess(real_object_srv.get(self.object_unknown_pig.Id).Threshold,ConstValues.threshold_initial_value)
        self.assertLess(real_object_srv.get(self.object_word_have.Id).Threshold,ConstValues.threshold_initial_value)
        self.assertLess(real_object_srv.get(self.object_unknown_have.Id).Threshold,ConstValues.threshold_initial_value)
        self.assertLess(real_object_srv.get(self.object_word_hair.Id).Threshold,ConstValues.threshold_initial_value)
        self.assertLess(real_object_srv.get(self.object_unknown_hair.Id).Threshold,ConstValues.threshold_initial_value)
        self.assertLess(memory_srv.get(self.memory_word.Id).Threshold,ConstValues.threshold_initial_value)
        self.assertLess(memory_srv.get(self.memory_understand.Id).Threshold,ConstValues.threshold_initial_value)

        pass

    def test_get_lowest_threshold_object_from_metadata(self):
        """
        测试metadata中RealObject衰减后，能获取到最低的object。
        为避免初始顺序的随机性，测试两次。第二次把另一个object衰减更低，仍然可以获取正确排序。
        :return:
        """
        entity_threshold_decrease(self.object_unknown_pig, 0.8)

        ### 获取metadata中阈值最低RealObject示例
        object_lower_threshold = get_lowest_threshold_object_from_metadata(self.meta_pig)

        self.assertEqual(object_lower_threshold,self.object_unknown_pig)

        entity_threshold_decrease(self.object_word_pig, 0.8)
        entity_threshold_decrease(self.object_word_pig, 0.8)
        object_lower_threshold = get_lowest_threshold_object_from_metadata(self.meta_pig)
        self.assertEqual(object_lower_threshold,self.object_word_pig)

        pass