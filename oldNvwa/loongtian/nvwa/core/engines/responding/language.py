#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    language 
Author:   Liuyl 
DateTime: 2015/1/13 14:34 
UpdateLog:
1、Liuyl 2015/1/13 将计划中枢中对陈述句和疑问句的评估结果生成反馈语句的功能逻辑迁移至此

language
>>> print("No Test")
No Test
"""
from loongtian.nvwa.core.engines.responding.match_degree import MatchDegreeFactory
from loongtian.nvwa.entities.data_structure_to_plan import DataStructureFromEvaluatorToPlanner
from loongtian.nvwa.service import fragment_srv

__author__ = 'Liuyl'


def respond(frag):
    match_degree = MatchDegreeFactory.create_match_degree(
        DataStructureFromEvaluatorToPlanner.trans_from_response_frag(frag))
    match_degree.run()
    for _r in match_degree.result:
        frag.output_word.append(fragment_srv.save_to_target_service(_r, frag.rep_srv))
        frag.output_meaning.append(fragment_srv.save_to_target_service(_r, frag.rep_srv))
    pass


if __name__ == '__main__':
    import doctest

    doctest.testmod()