#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    ${NAME} 
Author:   fengyh 
DateTime: 2014-10-30 10:41 
UpdateLog:
1、fengyh 2014-10-30 Create this File.
2、fengyh 2014-11-5 修改测试。应对测试目标变化重新测试。

"""
from unittest import TestCase
import time

from loongtian.nvwa.core.engines.m2k.memory_to_knowledge import MemoryToKnowledge
from loongtian.nvwa.core.gdef import OID
from loongtian.nvwa.service import *

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

meta_pig = metadata_srv.create(u"猪")
object_unknown_pig = metadata_srv.get_unknown_by_string_value(u'猪')
object_word_pig = metadata_srv.get_word_by_string_value(u'猪')

meta_hair = metadata_srv.create(u"毛")
object_unknown_hair = metadata_srv.get_unknown_by_string_value(u'毛')
object_word_hair = metadata_srv.get_word_by_string_value(u'毛')

object_unknown_have = metadata_srv.get_unknown_by_string_value(u'有')
object_word_have = metadata_srv.get_word_by_string_value(u'有')


class TestMemoryToKnowledge(TestCase):
    """
            idInt	start	end
            0	nvwa本我	接收
第一条记录	1	0	3
            2	牛字	有字
            3	2	腿字
            4	1	理解为
            5	4	7
            6	牛未知	有未知
            7	6	腿未知
            8	5	感知器为
            9	8	XX感知器ID
            10	9	时间为
            11	10	XX时间ID

第二条记录	12	0	14
            13	牛字	有字
            14	9	头字
            15	12	理解为
            16	15	18
            17	牛未知	有未知
            18	17	头未知
            19	16	感知器为
            20	19	XX感知器ID
            21	20	时间为
            22	21	XX时间ID

    """

    def test_distill(self):
        # 第一次生成猪有毛记忆，不会生成知识。
        self.__gen_memory_one_time__(1)
        mtk = MemoryToKnowledge()
        mtk.distill()

        meta_pig = metadata_srv.get_by_string_value(u'猪')
        new_pig = [m for m in meta_pig.RealObjectList if m != object_unknown_pig.Id and m != object_word_pig.Id]
        meta_hair = metadata_srv.get_by_string_value(u'毛')
        new_hair = [m for m in meta_hair.RealObjectList if m != object_unknown_hair.Id and m != object_word_hair.Id]
        meta_have = metadata_srv.get_by_string_value(u'有')
        new_have = [m for m in meta_have.RealObjectList if m != object_unknown_have.Id and m != object_word_have.Id]

        # 系统未生成新知识，应该查不到新对象。
        self.assertEqual(new_pig.__len__(), 0)
        self.assertEqual(new_hair.__len__(), 0)
        self.assertEqual(new_have.__len__(), 0)

        self.__gen_memory_one_time__(2)

        mtk = MemoryToKnowledge()
        mtk.distill()

        meta_pig = metadata_srv.get_by_string_value(u'猪')
        new_pig = [m for m in meta_pig.RealObjectList if m != object_unknown_pig.Id and m != object_word_pig.Id]
        meta_hair = metadata_srv.get_by_string_value(u'毛')
        new_hair = [m for m in meta_hair.RealObjectList if m != object_unknown_hair.Id and m != object_word_hair.Id]
        meta_have = metadata_srv.get_by_string_value(u'有')
        new_have = [m for m in meta_have.RealObjectList if m != object_unknown_have.Id and m != object_word_have.Id]

        # 系统未生成新知识，应该查不到新对象。
        self.assertEqual(new_pig.__len__(), 1)
        self.assertEqual(new_hair.__len__(), 1)
        self.assertEqual(new_have.__len__(), 1)

        object_pig = real_object_srv.get(new_pig[0])
        object_have = real_object_srv.get(new_have[0])
        object_hair = real_object_srv.get(new_hair[0])
        knowledge_new = knowledge_srv.select_t_structure(object_pig, object_have, object_hair)
        self.assertEqual(not knowledge_new, False)


    def __gen_memory_one_time__(self, time_delay):
        # # 第一条数据

        # 女娲接收到XXX字
        memory_word = memory_srv.create_t_structure(object_word_pig, object_word_have, object_word_hair)
        nvwa_receive_m = memory_srv.create_t_structure(nvwa_self, receive, memory_word)

        # 女娲理解为XXX意思
        memory_understand = memory_srv.create_t_structure(object_unknown_pig, object_unknown_have,
                                                          object_unknown_hair)
        nvwa_receive_m_understand_as = memory_srv.create_t_structure(nvwa_receive_m, understand, memory_understand)

        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + time_delay * 100))
        nvwa_receive_m_understand_as_time = memory_srv.create_t_structure(nvwa_receive_m_understand_as, timeis,
                                                                          real_object_srv.generate(
                                                                              Display=current_time))

        nvwa_receive_m_understand_as_time_sensor = memory_srv.create_t_structure(nvwa_receive_m_understand_as_time,
                                                                                 sensor, sensor_console)

        ## 第一条数据 end