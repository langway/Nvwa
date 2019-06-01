#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    data_structure_to_plan 
Author:   fengyh 
DateTime: 2014-10-16 14:00 
UpdateLog:
1、fengyh 2014-10-16 Create this File.


"""
from loongtian.nvwa.entities import SentenceTypeEnum, DataSourceTypeEnum, MatchDegreeTypeEnum, ConflictTypeEnum


class DataStructureFromEvaluatorToPlanner(object):
    """
    从评估中枢向计划中枢传递的结构体。
    """

    def __init__(self, **kwargs):
        """
        :param sentence_type:句子类型。使用SentenceTypeEnum判断。NotAsk=0,AskYesNo=1,AskNeedReplace=2,AskSelection=3,AskComposition=4
        :param match_source:匹配来源。使用DataSourceTypeEnum Knowledge=0,Memory=1
        :param match_degree:评估匹配程度。使用MatchDegreeTypeEnum。完全匹配0，部分匹配1，无匹配2, 匹配和冲突3 'Full=0,Partial=1,No=2,FullAndPartial=3'
        :param evaluate_result:评估结果T型结构。用嵌套的list表示。
        :param evaluate_basis:评估结果的依据，也是T型结构，用嵌套的list表示。
        :param match_by_father_object:是否通过父对象子对象等继承关系匹配的。True代表是，False代表不是，None表示不涉及。
        :param object_same:求同结果
        :param object_different:存异结果
        :return:本对象用于从评估中枢向计划中枢传递参数
        """
        self.SentenceType = kwargs.get('SentenceType', SentenceTypeEnum.NotAsk)
        self.MatchSource = kwargs.get('MatchSource', DataSourceTypeEnum.Knowledge)
        self.MatchDegree = kwargs.get('MatchDegree', MatchDegreeTypeEnum.No)
        self.EvaluateResult = kwargs.get('EvaluateResult', None)
        self.EvaluateBasis = kwargs.get('EvaluateBasis', None)
        self.MatchByFatherObject = kwargs.get('MatchByFatherObject', False)
        self.ObjectSame = kwargs.get('ObjectSame', [])
        self.Conflict = kwargs.get('Conflict', [])
        self.SentenceModel = kwargs.get('SentenceModel', None)
        self.Words=kwargs.get('Words', [])

    @staticmethod
    def trans_from_response_frag(response_frag):
        def trans_to_match_degree(evaluated_result_state):
            if evaluated_result_state == ConflictTypeEnum.FindedAndConflict:
                return MatchDegreeTypeEnum.FullAndPartial
            elif evaluated_result_state == ConflictTypeEnum.Finded:
                return MatchDegreeTypeEnum.Full
            elif evaluated_result_state == ConflictTypeEnum.Conflict:
                return MatchDegreeTypeEnum.Partial
            else:
                return MatchDegreeTypeEnum.No

        return DataStructureFromEvaluatorToPlanner(
            SentenceType=response_frag.sentence_type,
            MatchDegree=trans_to_match_degree(response_frag.state),
            EvaluateResult=response_frag,
            EvaluateBasis=response_frag.input_meaning_basis,
            Conflict=response_frag.conflict,
            #Words=response_frag.words
        )