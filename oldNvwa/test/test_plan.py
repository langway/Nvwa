#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    ${NAME} 
Author:   fengyh 
DateTime: 2014-10-16 14:28 
UpdateLog:
1、fengyh 2014-10-16 Create this File.


"""



from unittest import TestCase
from loongtian.nvwa.entities.data_structure_to_plan import *
from loongtian.nvwa.service import common_srv
from loongtian.nvwa.entities.sentence import Sentence

common_srv.InitHelper.init()

from loongtian.nvwa.core.maincenter.planner.plan import *


class TestPlan(TestCase):
    def test_run(self):

        knowledge_me = common_srv.get_knowledge_by_display(u'本我')
        knowledge_is = common_srv.get_knowledge_by_display(u'是')

        knowledge_receive = common_srv.get_knowledge_by_display(u'接收')
        knowledge_send = common_srv.get_knowledge_by_display(u'发出')
        knowledge_means = common_srv.get_knowledge_by_display(u'理解为')
        knowledge_datetime = common_srv.get_knowledge_by_display(u'时间为')
        knowledge_perception_tool = common_srv.get_knowledge_by_display(u'使用的感知器')
        knowledge_source = common_srv.get_knowledge_by_display(u'来源账号')
        knowledge_target = common_srv.get_knowledge_by_display(u'目标')
        knowledge_perception_console = common_srv.get_knowledge_by_display(u'控制台')

        knowledge_i_not_known = common_srv.get_knowledge_by_display(u'不知道')
        knowledge_i_known = common_srv.get_knowledge_by_display(u'知道')
        knowledge_but = common_srv.get_knowledge_by_display(u'但是')

        input_data = DataStructureFromEvaluatorToPlanner(MatchDegree=MatchDegreeTypeEnum.Full)
        sentence_word = Sentence([u'?'])

        plan = Plan(input_data,sentence_word)
        plan.run()

        self.assertEqual(plan.CommandMessageList.__len__(), 11)

        sentence_word = Sentence([u'.'])

        plan = Plan(input_data,sentence_word)
        plan.run()

        self.assertEqual(plan.CommandMessageList.__len__(), 11)
        #plan.CommandMessageList[0].