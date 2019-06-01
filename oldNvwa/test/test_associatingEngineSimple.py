#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    ${NAME} 
Author:   fengyh 
DateTime: 2015/1/27 10:42 
UpdateLog:
1、fengyh 2015/1/27 Create this File.
   将就的简单规则类比功能测试代码迁移出来到此处

"""
from unittest import TestCase
from loongtian.nvwa.core.engines.associating.associating_engine_simple import AssociatingEngineSimple
from loongtian.nvwa.core.gdef import OID
from loongtian.nvwa.service import metadata_srv, memory_srv, fragment_srv, original_srv, real_object_srv, \
    original_init_srv

"""
问题定义：
系统已知“牛组件腿”“桌子组件腿”，输入“羊有腿”时满足什么条件可以抽取为“羊组件腿”？

规则：
1、规则r1：系统已知“牛父对象动物”“羊父对象动物”“牛组件XXX”。类似“XXX父对象动物”且“XXX组件XXX”的出现次数k1。占权重w1。
2、规则r2：系统已知“XXX组件腿”出现次数k2。占权重w2。
3、类比值计算：V = k1*w1+k2*w2
4、V大于类比门槛值T则为类比成功，符合条件。
说明：
1、w1和w2权重总和为1，可设置各规则占比，程序可设置。
2、K1和k2是查询出来的数据。
3、门槛值T可设置。
"""



# 以下制造数据
original_init_srv.init()

# 女娲本我Id
nvwa_self = real_object_srv.get(OID.InnerSelf)
# 女娲接收Id
receive = real_object_srv.get(OID.Receive)
# 女娲理解为Id
understand = real_object_srv.get(OID.UnderstoodAs)
# 时间为
timeis = real_object_srv.get(OID.TimeIs)
# 感知器
sensor = real_object_srv.get(OID.SensorIs)
# 感知器控制台
sensor_console = real_object_srv.get(OID.Console)
# 观察者
observer = real_object_srv.get(OID.Console)

# 组件
component = real_object_srv.get(OID.Component)

meta_pig = metadata_srv.create(u"猪")
object_unknown_pig = metadata_srv.get_default_by_string_value(u'猪')
object_word_pig = metadata_srv.get_word_by_string_value(u'猪')

meta_hair = metadata_srv.create(u"毛")
object_unknown_hair = metadata_srv.get_default_by_string_value(u'毛')
object_word_hair = metadata_srv.get_word_by_string_value(u'毛')

object_unknown_have = metadata_srv.get_default_by_string_value(u'有')
object_word_have = metadata_srv.get_word_by_string_value(u'有')
object_component_have = metadata_srv.get_word_by_string_value(u'有')

meta_animal = metadata_srv.create(u"动物")
object_unknown_animal = metadata_srv.get_default_by_string_value(u'动物')
object_word_animal = metadata_srv.get_word_by_string_value(u'动物')

meta_cattle = metadata_srv.create(u"牛")
object_unknown_cattle = metadata_srv.get_default_by_string_value(u'牛')
object_word_cattle = metadata_srv.get_word_by_string_value(u'牛')

meta_horse = metadata_srv.create(u"马")
object_unknown_horse = metadata_srv.get_default_by_string_value(u'马')
object_word_horse = metadata_srv.get_word_by_string_value(u'马')

meta_leg = metadata_srv.create(u"腿")
object_unknown_leg = metadata_srv.get_default_by_string_value(u'腿')
object_word_leg = metadata_srv.get_word_by_string_value(u'腿')


class TestAssociatingEngineSimple(TestCase):
    def test_associate_rules(self):
        self.__gen_data__(u'猪', u'有', u'毛')
        self.__gen_data__(u'牛', u'有', u'腿')
        self.__gen_data__(u'猪', u'是', u'动物')
        self.__gen_data__(u'牛', u'是', u'动物')
        self.__gen_data__(u'马', u'是', u'动物')
        self.__gen_data__(u'马', u'有', u'腿',0)

        # 获得“女娲”“接收”的数据Id（Knowledge），此是所有查询的开始源头
        nvwa_receive_memory = memory_srv.base_select_start_end(nvwa_self.Id, receive.Id)
        # 根据“女娲”“接收”的start和end为条件，查询到女娲接收哪些数据，来自所有记忆信息。
        frag = fragment_srv.generate(nvwa_receive_memory, memory_srv)
        all_frags = fragment_srv.select_all_outer(frag)

        horse_object = metadata_srv.get_default_by_string_value(u'马')
        horse_have = memory_srv.base_select_start_end(horse_object.Id, object_unknown_have.Id)
        horse_have_frag = fragment_srv.generate(horse_have,memory_srv)
        horse_have_legs_frag = fragment_srv.select_all_outer(horse_have_frag)
        associating = AssociatingEngineSimple(horse_have_legs_frag[0])
        associating.run()

        # 判断类比规则是否已符合条件，类比成功
        self.assertEqual(3,associating.analogy_rule_factor_k1)
        self.assertEqual(2,associating.analogy_rule_factor_k2)

    def test_gen_data(self):
        horse_object = metadata_srv.get_default_by_string_value(u'马')
        # 判断是否生成了类比后的新数据
        horse_component = memory_srv.base_select_start_end(horse_object.Id,component.Id)
        self.assertIsNotNone(horse_component)

    def __gen_data__(self, left_str, middle_str, right_str,unknown_flag=1):
        #meta1 = metadata_srv.create(left_str)
        object_unknown1 = metadata_srv.get_default_by_string_value(left_str)
        object_word1 = metadata_srv.get_word_by_string_value(left_str)

        #meta2 = metadata_srv.create(right_str)
        object_unknown2 = metadata_srv.get_default_by_string_value(right_str)
        object_word2 = metadata_srv.get_word_by_string_value(right_str)

        object_unknown3 = metadata_srv.get_default_by_string_value(middle_str)
        object_word3 = metadata_srv.get_word_by_string_value(middle_str)
        object_component_have = metadata_srv.get_word_by_string_value(middle_str)

        # 女娲接收到XXX字  猪有毛
        memory_word = memory_srv.create_t_structure(object_word1, object_word3, object_word2)
        nvwa_receive_m = original_srv.Receive.set(nvwa_self, memory_word, memory_srv)

        # 女娲理解为XXX意思 猪组件毛
        memory_understand = original_srv.Component.set(object_unknown1, object_unknown2, memory_srv)
        if middle_str == u'是':
            memory_understand = original_srv.InheritFrom.set(object_unknown1, object_unknown2, memory_srv)
        if unknown_flag == 0:
            memory_understand = memory_srv.create_t_structure(object_unknown1, object_unknown_have,
                                                          object_unknown2)
        nvwa_receive_m_understand_as = original_srv.UnderstoodAs.set(nvwa_receive_m, memory_understand, memory_srv)

        # 记录时间为
        time_delay = 2
        current_time = original_srv.create_time_real_object()
        nvwa_receive_m_understand_as_time = original_srv.TimeIs.set(nvwa_receive_m_understand_as, current_time,
                                                                    memory_srv)

        # 感知器为
        nvwa_receive_m_understand_as_time_sensor = original_srv.SensorIs.set(nvwa_receive_m_understand_as_time,
                                                                             sensor_console, memory_srv)
        # 观察者为
        nvwa_receive_m_understand_as_time_sensor_observer = original_srv.ObserverIs.set(
            nvwa_receive_m_understand_as_time_sensor, observer, memory_srv)