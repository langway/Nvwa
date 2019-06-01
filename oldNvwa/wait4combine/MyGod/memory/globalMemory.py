#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
新建python文件
>>> print("No Test")
No Test
"""
__author__ = 'Liuyl'
from common.singleton import singleton as Singleton
import threading


@Singleton
class GlobalMemory(object):
    def __init__(self):
        # super(GlobalMemory, self).__init__()
        self.memory = []
        self._id_seed = 0
        self._id_seed_lock = threading.Lock()
        self.__initBaseMemory()

    def generate_id(self):
        self._id_seed_lock.acquire()
        _id = self._id_seed
        self._id_seed += 1
        self._id_seed_lock.release()
        return _id

    def __initBaseMemory(self):
        # 用于表示世界的金字塔模型
        # 第一层 源点
        self.hard_append(0, 0, 0)  # 0 源点

        # 第二层 根本源
        self.hard_append(1, 1, 0)  # 1 源存在
        self.hard_append(2, 2, 0)  # 2 源关系
        self.hard_append(3, 3, 0)  # 3 源变化
        self.hard_append(4, 4, 0)  # 4 源时间
        self.hard_append(5, 5, 0)  # 5 源状态

        # 第三层 根本源衍生
        # 根存在
        self.hard_append(11, 11, 1)  # 11 逻辑存在
        self.hard_append(12, 12, 1)  # 12 现实存在
        self.hard_append(13, 13, 1)  # 13 机器存在
        self.hard_append(14, 14, 1)  # 14 不存在
        # 根关系
        self.hard_append(21, 21, 2)  # 21 is关系
        self.hard_append(22, 22, 2)  # 22 属性关系
        self.hard_append(23, 23, 2)  # 23 实例关系
        self.hard_append(24, 24, 2)  # 24 机器表示关系
        self.hard_append(25, 25, 2)  # 25 未知关系
        self.hard_append(26, 26, 2)  # 26 构成关系
        self.hard_append(27, 27, 2)  # 27
        self.hard_append(28, 28, 2)  # 28 组件关系
        self.hard_append(29, 29, 2)  # 29 继承关系
        self.hard_append(30, 30, 2)  # 30 状态描述关系
        self.hard_append(31, 31, 2)  # 31 变化描述关系
        self.hard_append(32, 32, 2)  # 32 变化前限定关系
        self.hard_append(33, 33, 2)  # 33 变化前限定关系
        self.hard_append(34, 34, 2)  # 34 序列关系
        self.hard_append(35, 35, 2)  # 35 空或任意关系
        # 根变化
        self.hard_append(61, 61, 3)  # 61 状态动词
        self.hard_append(62, 62, 3)  # 62 实际动词

        # 第四层 依赖存在 预定义的机器本身理解的知识
        # 以下用于语言中枢
        # 词
        self.hard_append(1001, 1001, 11)  # 1001 词 (逻辑存在)
        # 表示
        self.hard_append(1002, 1002, 11)  # 1002 表示 (逻辑存在)
        # 预定义一些机器表示对象
        self.hard_append(6001, 6001, 13)  # "牛"
        self.hard_append(6002, 6002, 13)  # "名字"
        self.hard_append(6003, 6003, 13)  # "的"
        self.hard_append(6004, 6004, 13)  # "是"
        self.hard_append(6005, 6005, 13)  # "有"
        # self.hard_append(6006, 6006, 13)
        # self.hard_append(6007, 6007, 13)
        #self.hard_append(6008, 6008, 13)

        # 第五层 存在
        self._id_seed = 10000

        # 定义'牛'这个词并关联机器表示
        _id0 = self.deep_append(-1, 12, 23, 1001)  # 定义"牛"这个词,"牛"属于词
        self.deep_append(_id0, 24, 6001)  # "牛"这个词的机器表示是6001
        # 定义牛且牛的表示是'牛'
        self.deep_append(-1, 11, 22, 1002, 21, _id0)

        # 将表示 这个逻辑存在与"名字"相关联
        _id0 = self.deep_append(-1, 12, 23, 1001)
        self.deep_append(_id0, 24, 6002)
        self.deep_append(1002, 22, 1002, 21, _id0)

        # 将属性关系的表示与"的"相连
        _id0 = self.deep_append(-1, 12, 23, 1001)
        self.deep_append(_id0, 24, 6003)
        self.deep_append(22, 22, 1002, 21, _id0)

        # 将is关系,实例关系,继承关系的表示与'是'相连
        _id0 = self.deep_append(-1, 12, 23, 1001)
        self.deep_append(_id0, 24, 6004)
        self.deep_append(21, 22, 1002, 21, _id0)
        self.deep_append(23, 22, 1002, 21, _id0)
        self.deep_append(29, 22, 1002, 21, _id0)
        # 状态动词(是-is)的表示与'是'相连
        _id1 = self.deep_append(-1, 61, 22, 1002, 21, _id0)
        _id2 = self.deep_append(-1, 12)  # 定义占位对象1
        _id3 = self.deep_append(-1, 12)  # 定义占位对象2
        self.deep_append(_id1, 32, _id2)  # 关联前限定
        self.deep_append(_id1, 33, _id3)  # 关联后限定
        _id4 = self.deep_append(-1, 5, 30, _id2, 21, _id3)  # 定义状态动词(是-is)的状态,X是Y,这个人是小明
        self.deep_append(_id1, 31, _id4)  # 定义动词的描述
        # 状态动词(是-实例)的表示与'是'相连
        _id1 = self.deep_append(-1, 61, 22, 1002, 21, _id0)
        _id2 = self.deep_append(-1, 12)  # 定义占位对象1
        _id3 = self.deep_append(-1, 11)  # 定义占位对象2
        self.deep_append(_id1, 32, _id2)  # 关联前限定
        self.deep_append(_id1, 33, _id3)  # 关联后限定
        _id4 = self.deep_append(-1, 5, 30, _id2, 23, _id3)  # 定义状态动词(是-实例)的状态,X是Y的实例,如小明是人
        self.deep_append(_id1, 31, _id4)  # 定义动词的描述
        # 状态动词(是-继承)的表示与'是'相连
        _id1 = self.deep_append(-1, 61, 22, 1002, 21, _id0)
        _id2 = self.deep_append(-1, 11)  # 定义占位对象1
        _id3 = self.deep_append(-1, 11)  # 定义占位对象2
        self.deep_append(_id1, 32, _id2)  # 关联前限定
        self.deep_append(_id1, 33, _id3)  # 关联后限定
        _id4 = self.deep_append(-1, 5, 30, _id2, 29, _id3)  # 定义状态动词(是-继承)的状态,X是Y的一种,如牛是动物
        self.deep_append(_id1, 31, _id4)  # 定义状态动词(是-继承)的描述

        # 定义"有"这个词
        _id0 = self.deep_append(-1, 12, 23, 1001)
        self.deep_append(_id0, 24, 6005)
        # 状态动词(有)
        _id1 = self.deep_append(-1, 61, 22, 1002, 21, _id0)
        _id2 = self.deep_append(-1, 11)  # 定义占位对象1
        _id3 = self.deep_append(-1, 11)  # 定义占位对象2
        self.deep_append(_id1, 32, _id2)  # 关联前限定
        self.deep_append(_id1, 33, _id3)  # 关联后限定
        _id4 = self.deep_append(-1, 5, 30, _id2, 28, _id3)  # 定义状态动词(有)的状态,Y是X的组件,如牛有腿
        self.deep_append(_id1, 31, _id4)  # 定义状态动词(有)的描述

        # 实际动词(给-obj把obj给obj) 示例
        _id1 = self.deep_append(-1, 61, 22, 1002, 21, _id0)
        _id2 = self.deep_append(-1, 12)  # 定义占位对象1
        _id3 = self.deep_append(-1, 12)  # 定义占位对象2
        _id4 = self.deep_append(-1, 12)  # 定义占位对象3
        self.deep_append(_id1, 32, _id2, 34, "把", 34, _id3)  # 关联前限定 obj把obj -->obj1->未知关系->"把"->未知关系->obj2
        self.deep_append(_id1, 33, _id4)  # 关联后限定
        _id5 = self.deep_append(-1, 5, 30, _id2, 26, _id3)  # 定义状态1-1,obj2是obj1的构成
        _id6 = self.deep_append(-1, 5, 30, _id4, 35, _id3)  # 定义状态1-2,obj2与obj3无关系
        _id7 = self.deep_append(-1, 5, 30, _id5, 34, _id6)  # 定义状态1,状态1-1和1-2
        _id8 = self.deep_append(-1, 5, 30, _id2, 35, _id3)  # 定义状态2-1,obj2与obj1无关系
        _id9 = self.deep_append(-1, 5, 30, _id4, 26, _id3)  # 定义状态2-2,obj2是obj3的构成
        _id10 = self.deep_append(-1, 5, 30, _id8, 34, _id9)  # 定义状态2,状态1-1和1-2
        self.deep_append(_id1, 31, _id4)  # 定义状态动词(有)的描述

    def _append(self, key, value):
        self.memory.append({'key': key, 'value': value})

    def hard_append(self, key, start, end):
        self._id_seed_lock.acquire()
        try:
            if key < self._id_seed:
                raise Exception("Memory key error!")
            else:
                self.memory.append({'key': key, 'value': {"start": start, "end": end}})
                self._id_seed = key + 1
        finally:
            self._id_seed_lock.release()

    def deep_append(self, start, *ends):
        _key = self.append(start, ends[0])
        if len(ends) > 1:
            self.deep_append(_key, *ends[1:])
        return _key

    def append(self, start, end):
        key = self.generate_id()
        if start == -1:
            start = key
        self.memory.append({'key': key, 'value': {"start": start, "end": end}})
        return key


def remember(start, end):
    return GlobalMemory().append(start, end)


def deep_remember(start, *ends):
    return GlobalMemory().deep_append(start, *ends)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
