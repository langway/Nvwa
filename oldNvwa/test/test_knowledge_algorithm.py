#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    ${NAME} 
Author:   fengyh 
DateTime: 2014-10-29 12:57 
UpdateLog:
1、fengyh 2014-10-29 Create this File.


"""
from unittest import TestCase

from loongtian.nvwa.core.engines.m2k.knowledge_algorithm_base import *
from loongtian.nvwa.entities.entity import RealObject
from loongtian.nvwa.entities.t_model import TModel


"""
测试数据区
"""
r1 = RealObject(Id='1', Display='牛')
r2 = RealObject(Id='2', Display='有')
r3 = RealObject(Id='3', Display='腿')

r4 = RealObject(Id='4', Display='头')
r5 = RealObject(Id='5', Display='无')
r6 = RealObject(Id='6', Display='马')

# 牛有头
t1 = TModel(TStart=r1, TEnd=r2, TEnd2=r3)

# 牛有腿
t2 = TModel(TStart=r1, TEnd=r2, TEnd2=r4)
# 马有头
t3 = TModel(TStart=r6, TEnd=r2, TEnd2=r3)
# 牛无头
t4 = TModel(TStart=r1, TEnd=r5, TEnd2=r3)
# 牛有头
t11 = TModel(TStart=r1, TEnd=r2, TEnd2=r3)
t12 = TModel(TStart=r1, TEnd=r2, TEnd2=r3)
t13 = TModel(TStart=r1, TEnd=r2, TEnd2=r3)
t14 = TModel(TStart=r1, TEnd=r2, TEnd2=r3)

# 牛有腿
t21 = TModel(TStart=r1, TEnd=r2, TEnd2=r4)
t22 = TModel(TStart=r1, TEnd=r2, TEnd2=r4)


class TestKnowledgeAlgorithm(TestCase):
    def test_distill_simple_exist_n_times(self):
        memory_list = [t1, t2, t11, t3, t4, t12]
        knowledge_result = []
        ka = KnowledgeAlgorithmSimpleExistNTimes(memory_list, 3)
        knowledge_result = ka.distill()

        # 测试连续出现不小于3次的结果，可以搜索到牛有腿
        self.assertEqual(knowledge_result.__len__(), 1)
        self.assertEqual(knowledge_result[0], t1)

    def test_distill_simple_exist_n_one_by_one(self):
        memory_list = [t1, t2, t11, t12, t3, t4, t12, t13, t14]
        knowledge_result = []
        ka = KnowledgeAlgorithmSimpleExistNOneByOne(memory_list, 2)
        knowledge_result = ka.distill()

        # 测试连续出现不小于2次的结果，可以搜索到牛有腿
        self.assertEqual(knowledge_result.__len__(), 1)
        self.assertEqual(knowledge_result[0], t1)

        # 测试连续出现不小于5次的结果，搜索不到信息，返回list为空
        ka = KnowledgeAlgorithmSimpleExistNOneByOne(memory_list, 5)
        knowledge_result = ka.distill()
        self.assertEqual(knowledge_result.__len__(), 0)

    def test_algorithm_manage(self):
        # 判断出现次数可以得到 牛有腿和牛有头，判断连续性可以得到 牛有腿 交集只有一个牛右腿
        memory_list = [t1, t2, t21, t11, t12, t3, t4, t12, t13, t14]
        kam = KnowledgeAlgorithmManage(KnowledgeAlgorithmSimpleExistNTimes(memory_list, 2),
                                       KnowledgeAlgorithmSimpleExistNOneByOne(memory_list, 3))

        knowledge_result = kam.distill_and()
        self.assertEqual(knowledge_result.__len__(), 1)
        self.assertEqual(knowledge_result[0], t1)

        # 牛有头出现3次，但没有连续。牛有腿出现两次，是连续。交际应该为0，并集应该为2.
        memory_list = [t2, t3,t21,  t4, t12, t13, t22]
        kam = KnowledgeAlgorithmManage(KnowledgeAlgorithmSimpleExistNTimes(memory_list, 3),
                                       KnowledgeAlgorithmSimpleExistNOneByOne(memory_list,2))
        knowledge_result = kam.distill_and()
        self.assertEqual(knowledge_result.__len__(), 0)

        knowledge_result = kam.distill_or()
        self.assertEqual(knowledge_result.__len__(), 2)
