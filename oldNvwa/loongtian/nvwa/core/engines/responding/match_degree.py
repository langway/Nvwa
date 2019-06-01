#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    match_degree 
Author:   fengyh 
DateTime: 2014-10-16 9:01 
UpdateLog:
1、fengyh 2014-10-16 Create this File.


"""
from loongtian.nvwa.core.engines.responding.sentence import *
import loongtian.nvwa.entities.data_structure_to_plan as dsp


class MatchDegreeBase(object):
    def __init__(self, data_structure_to_plan):
        self.sentence = data_structure_to_plan
        self.result = []

    def run(self):
        pass


class MatchDegree0Full(MatchDegreeBase):
    def run(self):
        sentence1 = SentenceFactory.create_sentence(self.sentence, self)
        sentence1.run()
        self.result = sentence1.result


class MatchDegree1Partial(MatchDegreeBase):
    def run(self):
        sentence1 = SentenceFactory.create_sentence(self.sentence, self)
        sentence1.run()
        self.result = sentence1.result


class MatchDegree2No(MatchDegreeBase):
    def run(self):
        sentence1 = SentenceFactory.create_sentence(self.sentence, self)
        sentence1.run()
        self.result = sentence1.result


class MatchDegree3FullAndPartial(MatchDegreeBase):
    def run(self):
        sentence1 = SentenceFactory.create_sentence(self.sentence, self)
        sentence1.run()
        self.result = sentence1.result


class MatchDegreeFactory:
    def __init__(self):
        pass

    @staticmethod
    def create_match_degree(sentence):
        try:
            return {
                dsp.MatchDegreeTypeEnum.Full: MatchDegree0Full(sentence),
                dsp.MatchDegreeTypeEnum.Partial: MatchDegree1Partial(sentence),
                dsp.MatchDegreeTypeEnum.No:MatchDegree2No(sentence),
                dsp.MatchDegreeTypeEnum.FullAndPartial:MatchDegree3FullAndPartial(sentence)
            }[MatchDegreeFactory.judge_match_degree(sentence)]
        except KeyError:
            return None
        pass

    @staticmethod
    def judge_match_degree(data_structure_to_plan):
        # todo 此处对问句判断现在直接用外层调用关键字判断的结果，未来要调整算法。
        return data_structure_to_plan.MatchDegree