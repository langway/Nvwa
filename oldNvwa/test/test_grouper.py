#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    ${NAME} 
Author:   fengyh 
DateTime: 2014/9/3 9:29 
UpdateLog:
1、fengyh 2014/9/3  Create this File.
                    编写test_group方法，未完待续。todo
2、fengyh 2014/9/9  调整测试分组功能的测试方法。
                    删除调试过程中的临时代码。
3、fengyh 2014/9/10 增加测试‘虚无’anything关系创建功能的代码
                    test_do_group增加连续词语中间无action的情况。
4、liuyl 2015/6/8 重写测试

"""
from unittest import TestCase
from loongtian.nvwa.core.maincenter.modeler.grouper import grouper_center
from loongtian.nvwa.service import *


class TestGrouper(TestCase):
    def test_do_group(self):
        original_init_srv.init()
        from loongtian.nvwa.entities.sentence import Sentence

        g_word_list = [u'牛', u'有', u'黄色', u'的', u'腿']
        # g_word_list = [u'有', u'的', u'有']
        g_sentence = Sentence(g_word_list)
        g_result = grouper_center.execute(g_word_list, g_sentence)
        # for _f in g_result:
        # print(_f.__str__())
        self.assertEqual(g_result.__len__(), 5)

    def test_do_group_more(self):
        original_init_srv.init()
        from loongtian.nvwa.entities.sentence import Sentence

        g_word_list = [u'小丽', u'是', u'美丽', u'善良', u'的', u'姑娘']
        # g_word_list = [u'有', u'的', u'有']
        g_sentence = Sentence(g_word_list)
        g_result = grouper_center.execute(g_word_list, g_sentence)
        for _f in g_result:
            print(_f.__str__())
        self.assertEqual(g_result.__len__(), 5)
