#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    ${NAME} 
Author:   fengyh 
DateTime: 2014-10-29 13:06 
UpdateLog:
1、fengyh 2014-10-29 Create this File.
                     测试eq函数好用

"""
from unittest import TestCase
from loongtian.nvwa.entities.entity import RealObject
from loongtian.nvwa.entities.t_model import TModel


class TestTModel(TestCase):
    def test___eq__(self):
        """
        测试TModel模型的Eq功能好用
        :return:
        """
        r1 = RealObject(Id='1',Display='牛')
        r2 = RealObject(Id='2',Display='有')
        r3 = RealObject(Id='3',Display='腿')


        r4 = RealObject(Id='4',Display='头')
        r5 = RealObject(Id='5',Display='无')
        r6 = RealObject(Id='6',Display='马')

        # 牛有头
        t1 = TModel(TStart=r1,TEnd=r2,TEnd2=r3)

        # 牛有腿
        t2 = TModel(TStart=r1,TEnd=r2,TEnd2=r4)
        # 马有头
        t3 = TModel(TStart=r6,TEnd=r2,TEnd2=r3)
        # 牛无头
        t4 = TModel(TStart=r1,TEnd=r5,TEnd2=r3)
        # 牛有头
        t5 = TModel(TStart=r1,TEnd=r2,TEnd2=r3)

        self.assertFalse(t1.__eq__(t2),msg=u'牛有头 vs 牛有腿')
        self.assertFalse(t1.__eq__(t3),msg=u'牛有头 vs 马有头')
        self.assertFalse(t1.__eq__(t4),msg=u'牛有头 vs 牛无头')
        self.assertTrue(t1.__eq__(t5),msg=u'牛有头 vs 牛有头')