#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    ${NAME} 
Author:   fengyh 
DateTime: 2014/9/3 9:51 
UpdateLog:
1、fengyh 2014/9/3 Create this File.
2、fengyh 2014/9/3 测试endtype枚举方法

"""
from unittest import TestCase
from loongtian.nvwa.entities.enum import EndTypeEnum


class TestEndTypeEnum(TestCase):
    def test_endtypenum(self):
        """
        测试endtype的枚举值好用。
        fengyh 2014-9-3
        :return:
        """
        self.assertEqual(EndTypeEnum.UnKnown, 0)
        self.assertEqual(EndTypeEnum.RealObject, 1)
        self.assertEqual(EndTypeEnum.Relation, 2)
        self.assertEqual(EndTypeEnum.Action, 3)
        self.assertEqual(EndTypeEnum.Modifier, 4)
        self.assertEqual(EndTypeEnum.Anything, 5)
        self.assertEqual(EndTypeEnum.Empty, 6)

