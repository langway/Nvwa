#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    processing 
Author:   fengyh 
DateTime: 2015/1/15 10:32 
UpdateLog:
1、fengyh 2015/1/15 Create this File.
                    将阈值相关基础功能迁移到此文件.
                    创建综合阈值处理类Processing，在其中做阈值计算和处理，外部不用关心阈值率。.

"""
import datetime
import operator
from loongtian.nvwa.core.engines.threshold.adjust import decrease
from loongtian.nvwa.core.gdef import OID
from loongtian.nvwa.entities.entity import RealObject, Knowledge
from loongtian.nvwa.service import real_object_srv, knowledge_srv, metadata_srv, fsc
from loongtian.nvwa.service.fragment_service.memory import MemoryFragmentEnum


def entity_threshold_decrease(obj, rate):
    """
    fengyh 2015-1-14

    对传入的realobject/memory/knowledge按照指定rate进行阈值衰减，并设置阈值调整时间。
    然后对存储数据做update save。

    阈值减少规则：（此处规则为暂定，未来可能变得更多更复杂）
    1、metadata被查询引用一次，rate值为0.01
    2、形成组件构成关系，rate值为0.1
    3、形成集合归纳，rate值为0.4
    4、形成构成属性，rate值为0.8

    :param obj:
    :param rate:
    :return:
    """
    obj.Threshold = decrease(obj.Threshold, rate)
    obj.ThresholdTime = datetime.datetime.now().__str__()

    if isinstance(obj, RealObject):
        real_object_srv.save(obj)
    elif isinstance(obj, Knowledge):
        knowledge_srv.save(obj)
    elif isinstance(obj, Memory):
        memory_srv.save(obj)


def entity_list_each_threshold_decrease(obj_list, rate):
    """
    fengyh 2015-1-15
    对输入对象列表按照指定衰减率处理。输入列表可以是object，memory，knowledge混合列表。
    :param obj_list:
    :param rate:
    :return:
    """
    for d in obj_list:
        entity_threshold_decrease(d, rate)


def get_lowest_threshold_object_from_metadata(meta):
    """
    fengyh 2015-1-15
    根据传入metadata找到其中阈值最低的RealObject
    :param meta: 传入metadata
    :return:阈值最低RealObject
    """
    object_list = [real_object_srv.get(id) for id in meta.RealObjectList]
    object_list.sort(key=operator.attrgetter("Threshold"))
    return object_list[0]


def get_lowest_threshold_object_from_string_of_metadata(str):
    """
    fengyh 2015-1-15
    根据传入字符串找到其对应metadata中阈值最低的RealObject
    :param str: 输入字符串
    :return:阈值最低RealObject
    """
    meta = metadata_srv.get_by_string_value(str)
    return get_lowest_threshold_object_from_metadata(meta)


class ThresholdProcess(object):
    """
    fengyh 2015-1-15
    此类负责对fragment整体做阈值衰减。
    根据数据内容情况实现衰减算法。
    """
    def __init__(self, frag):
        self.ready_fragment = frag
        self.rate = 0.01

    def set_fragment(self, frag):
        self.ready_fragment = frag
        self.rate = 0.01
        pass

    def run_decrease(self):
        """
        fengyh 2015-1-15
        执行阈值衰减任务：
        1、数据准备。把fragment拆解。
        2、算法初步。调整阈值率。
        3、执行衰减。对字面对象和理解为对象分别处理。
        :return:
        """
        self.__data_ready__()
        self.__judge_threshold_decrease_rate_algorithm__()
        # 处理“字”的衰减
        entity_list_each_threshold_decrease(self.current_data.data, self.rate)
        # 处理“理解为”内容的衰减
        entity_list_each_threshold_decrease(self.understand_data.data, self.rate)

        pass

    def __data_ready__(self):
        ready_list = fsc.memory.unassemble(self.ready_fragment)
        self.observer_data = ready_list[MemoryFragmentEnum.Observer]
        self.sensor_data = ready_list[MemoryFragmentEnum.Sensor]
        self.time_data = ready_list[MemoryFragmentEnum.Time]
        self.send_data = ready_list[MemoryFragmentEnum.Send]
        self.receive_data = ready_list[MemoryFragmentEnum.Receive]
        self.understand_data = ready_list[MemoryFragmentEnum.Understand]
        self.mood_data = ready_list[MemoryFragmentEnum.Mood]
        self.current_data = None

    def __judge_threshold_decrease_rate_algorithm__(self):
        # 不同的预期，其阈值衰减程度不同
        if self.mood_data.ref.Id == OID.Declarative:
            self.rate *= 1.1
        elif self.mood_data.ref.Id == OID.Question:
            self.rate *= 0.9

        # 发送还是接收，衰减程度不同
        if self.send_data is None:
            self.rate *= 1.5
            self.current_data = self.receive_data
        elif self.receive_data is None:
            self.rate *= 0.5
            self.current_data = self.send_data

        # 不同的感知器对阈值的衰减影响不同
        if self.observer_data.ref.Id == OID.God:
            self.rate *= 5
        elif self.observer_data.ref.Id == OID.InnerSelf:
            self.rate *= 1

        pass

