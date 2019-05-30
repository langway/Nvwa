#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    sentence 
Author:   Liuyl 
DateTime: 2014/10/17 9:18 
UpdateLog:
1、Liuyl 2014/10/17 Create this File.

sentence
>>> print("No Test")
No Test
"""
from loongtian.nvwa.service.question_words import QWords

__author__ = 'Liuyl'
import loongtian.nvwa.entities.data_structure_to_plan as dsp


class Sentence(object):
    """
    用于传递原始句子信息的类
    """

    def __init__(self, word_split_list):
        if word_split_list[-1] == u'?' or word_split_list[-1] == u'？':
            # todo 此处增加对指代问句的判断。未来此种判断方式有可能采用机器学习方式，或其它算法。也有可能不放在这里判断。
            # fengyh 2014-11-18
            if list(set(QWords.const_ask1_what).intersection(set(word_split_list))).__len__() > 0 >= list(
                    set(QWords.const_ask0_jamming).intersection(set(word_split_list))).__len__():
                # 本条件比较关键词同时考虑干扰词的情况。排除掉干扰词不算问句。未来干扰词要用其它算法。
                self.SentenceType = dsp.SentenceTypeEnum.AskNeedReplaceWhat
            elif list(set(QWords.const_ask2_where).intersection(set(word_split_list))).__len__() > 0:
                self.SentenceType = dsp.SentenceTypeEnum.AskNeedReplaceWhere
            elif list(set(QWords.const_ask3_who).intersection(set(word_split_list))).__len__() > 0:
                self.SentenceType = dsp.SentenceTypeEnum.AskNeedReplaceWho
            elif list(set(QWords.const_ask4_when).intersection(set(word_split_list))).__len__() > 0:
                self.SentenceType = dsp.SentenceTypeEnum.AskNeedReplaceWhen
            elif list(set(QWords.const_ask5_how_many).intersection(set(word_split_list))).__len__() > 0:
                self.SentenceType = dsp.SentenceTypeEnum.AskNeedReplaceHowMany
            else:
                self.SentenceType = dsp.SentenceTypeEnum.AskYesNo
            self.Words = word_split_list[:-1]
            del word_split_list[-1]
        elif word_split_list[-1] == u'!' or word_split_list[-1] == u'！':
            self.SentenceType = dsp.SentenceTypeEnum.Command
            self.Words = word_split_list[:-1]
        else:
            self.SentenceType = dsp.SentenceTypeEnum.NotAsk
            self.Words = word_split_list[:]
        self.sentence_model = None


if __name__ == '__main__':
    import doctest

    doctest.testmod()