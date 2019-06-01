#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    question_words 
Author:   fengyh 
DateTime: 2014/11/25 9:25 
UpdateLog:
1、fengyh 2014/11/25 Create this File.


"""


class QuestionWords(object):
    def __init__(self):
        self.const_ask1_what = [u'什么', u'啥']
        self.const_ask2_where = [u'什么地方', u'哪里', u'哪儿', u'哪']
        self.const_ask3_who = [u'什么人', u'谁', u'何人']
        self.const_ask4_when = [u'什么时候', u'何时', u'什么时间']
        self.const_ask5_how_many = [u'几个', u'多少', u'几多',u'几',u'几根',u'几条']
        self.const_ask0_jamming = [u'什么玩意']

        self.all_question_words = self.const_ask1_what + self.const_ask2_where + self.const_ask3_who + self.const_ask4_when + self.const_ask5_how_many

    def judge_contain_question_word(self, str_q):
        """
        查找指定字符串序列中是否包含疑问词
        :param str_q:
        :return:
        """
        for w in self.all_question_words:
            if str_q.find(w) >= 0:
                return True
        return False


QWords = QuestionWords()