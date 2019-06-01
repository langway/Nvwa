#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    ${NAME} 
Author:   fengyh 
DateTime: 2015/6/16 11:12 
UpdateLog:
1、fengyh 2015/6/16 Create this File.


"""
from unittest import TestCase
from loongtian.nvwa.core.engines.meantool.placeholder import PlaceHolder
from loongtian.nvwa.service import original_init_srv


class TestPlaceHolder(TestCase):
    def test_get_n_placeholder(self):
        original_init_srv.init(for_test=True)

        ph_list1,ph_list2,ph_list3 = [],[],[]
        ph_list1 = PlaceHolder.get_n_placeholder(1)
        self.assertEqual(ph_list1.__len__(),1)
        ph_list2 = PlaceHolder.get_n_placeholder(3)
        self.assertEqual(ph_list2.__len__(),3)
        self.assertTrue(ph_list2.__contains__(ph_list1[0]))
        ph_list3 = PlaceHolder.get_n_placeholder(2)
        self.assertEqual(ph_list3.__len__(),2)
        self.assertTrue(ph_list2.__contains__(ph_list3[0]))
        self.assertTrue(ph_list2.__contains__(ph_list3[1]))