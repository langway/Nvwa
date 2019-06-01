#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    evaluator 
Author:   Liuyl 
DateTime: 2014/9/19 10:39 
UpdateLog:
1、Liuyl 2014/9/19 Create this File.

evaluator
>>> print("No Test")
No Test
"""
import itertools
from loongtian.nvwa.service import *
import loongtian.nvwa.entities.data_structure_to_plan as dsp
import copy
from loongtian.nvwa.entities import ConflictTypeEnum, SentenceTypeEnum
from loongtian.nvwa.core.gdef import OID
from loongtian.nvwa.common.cache.cache import i_cache
import loongtian.nvwa.core.engines.studying
from loongtian.nvwa.core.engines.conflicting.conflict import check
from loongtian.nvwa.service.fragment_service.memory import MemoryFragmentEnum
from loongtian.nvwa.core.engines.threshold.processing import ThresholdProcess

__author__ = 'Liuyl'


class State(object):
    MatchAndConflict = ConflictTypeEnum.FindedAndConflict
    Match = ConflictTypeEnum.Finded
    Conflict = ConflictTypeEnum.Conflict
    NotExist = ConflictTypeEnum.NotFinded


class CheckResult(object):
    def __init__(self, state=State.NotExist, match_frag=None, conflict_frag=None):
        self.state = state
        self.match_frag = match_frag
        self.conflict_frag = conflict_frag

    @staticmethod
    def trans(conflict_engine_result, target_srv):
        return CheckResult(conflict_engine_result[0], fragment_srv.generate(conflict_engine_result[1][0], target_srv),
                           fragment_srv.generate(conflict_engine_result[1][1], target_srv))


# def check(start_frag, end_frag, target_srv):
# match = target_srv.base_select_start_end(start_frag.ref.Id, end_frag.ref.Id)
# if match:
# return CheckResult(State.Match, fragment_srv.generate(match, target_srv))
# else:
# return CheckResult(State.NotExist)


Score = {State.MatchAndConflict: 15, State.Match: 10, State.Conflict: 5, State.NotExist: 0}


class EvaluateResult(object):
    def __init__(self, state=State.NotExist, score=0, left_frag=None, right_frag=None, conflict=None, frag=None):
        self.state = state
        self.score = score
        if not conflict:
            conflict = []
        self.conflict = conflict
        self.right_frag = right_frag
        self.left_frag = left_frag
        self.frag = frag


class Evaluator(object):
    def __init__(self):
        pass

    def execute(self, moved_list, sentence):
        _cache = {}
        _key_lambda = lambda args, kwargs: '{0},{1}'.format(args[0].ref.Id, str(args[1].__class__))
        _rep_srv = fragment_srv.get_new_knowledge_for_fragment_service()

        def combine_evaluate_result(left_frag, cur_check_result, start_evaluate_result, end_evaluate_result):
            deep_score = start_evaluate_result.score + end_evaluate_result.score
            deep_conflict = start_evaluate_result.conflict + end_evaluate_result.conflict
            # 不存在,结果为不存在
            if cur_check_result.state == State.NotExist:
                return [EvaluateResult(State.NotExist, deep_score)]
            # 符合+冲突, 分裂为两个结果
            if cur_check_result.state == State.MatchAndConflict:
                if start_evaluate_result.state == State.Conflict or end_evaluate_result.state == State.Conflict:
                    return [EvaluateResult(State.Conflict,
                                           Score[State.MatchAndConflict] + deep_score,
                                           left_frag,
                                           cur_check_result.conflict_frag,
                                           [cur_check_result.conflict_frag] + deep_conflict),
                            EvaluateResult(State.Conflict,
                                           Score[State.MatchAndConflict] + deep_score,
                                           left_frag,
                                           cur_check_result.match_frag,
                                           deep_conflict)]
                else:
                    return [EvaluateResult(State.Conflict,
                                           Score[State.MatchAndConflict] + deep_score,
                                           left_frag,
                                           cur_check_result.conflict_frag,
                                           [cur_check_result.conflict_frag]),
                            EvaluateResult(State.Match,
                                           Score[State.MatchAndConflict] + deep_score,
                                           left_frag,
                                           cur_check_result.match_frag,
                                           None)]
            # 冲突 ,返回的结果为冲突
            if cur_check_result.state == State.Conflict:
                return [EvaluateResult(State.Conflict,
                                       Score[State.Conflict] + deep_score,
                                       left_frag,
                                       cur_check_result.conflict_frag,
                                       [cur_check_result.conflict_frag] + deep_conflict)]
            # 符合 ,如start和end不冲突,返回的结果为符合,否则返回冲突
            if cur_check_result.state == State.Match:
                if start_evaluate_result.state == State.Conflict or end_evaluate_result.state == State.Conflict:
                    return [EvaluateResult(State.Conflict,
                                           Score[State.Match] + deep_score,
                                           left_frag,
                                           cur_check_result.match_frag,
                                           deep_conflict)]
                else:
                    return [EvaluateResult(State.Match,
                                           Score[State.Match] + deep_score,
                                           left_frag,
                                           cur_check_result.match_frag,
                                           None)]

        @i_cache(_cache, _key_lambda)
        def deep_evaluate(frag, target_srv):
            _start = fragment_srv.get_start(frag)
            _end = fragment_srv.get_end(frag)
            if _start and _end:
                _start_evaluate_result_list = deep_evaluate(_start, target_srv)
                _end_evaluate_result_list = deep_evaluate(_end, target_srv)
                _result_pair_list = itertools.product(_start_evaluate_result_list, _end_evaluate_result_list)
                _deep_result = []
                for _pair in _result_pair_list:
                    _start_evaluate_result = _pair[0]
                    _end_evaluate_result = _pair[1]
                    if _start_evaluate_result.state == State.NotExist or _end_evaluate_result.state == State.NotExist:
                        _deep_result.extend([
                            EvaluateResult(State.NotExist, _start_evaluate_result.score + _end_evaluate_result.score,
                                           frag, None)])
                    else:
                        _check_result = check(_start_evaluate_result.right_frag,
                                              _end_evaluate_result.right_frag, target_srv)
                        _deep_result.extend(combine_evaluate_result(frag, CheckResult.trans(_check_result, target_srv),
                                                                    _start_evaluate_result, _end_evaluate_result))
                return _deep_result
            else:
                if real_object_srv.get(frag.ref.Id):
                    return [EvaluateResult(State.Match, 0, frag, frag)]
                return [EvaluateResult(State.NotExist, 0, frag, None)]

        def filter_memory(evaluate_result_list):
            _f_result = []
            for _r in evaluate_result_list:
                if _r.right_frag:
                    _outer = fragment_srv.select_all_outer(_r.right_frag)
                    for _o in _outer:
                        _ms = fsc.memory.unassemble(_o)
                        if _ms[MemoryFragmentEnum.Mood] and not original_srv.Equal.check(
                                _ms[MemoryFragmentEnum.Mood].ref,
                                original_srv.Question.obj()):
                            _f_result.append(_r)
            return _f_result

        def handle_match_and_conflict(evaluate_result_list):
            if len(evaluate_result_list) == 0:
                return None
            elif len(evaluate_result_list) == 1:
                return evaluate_result_list[0]
            else:
                evaluate_result_list.sort(key=lambda x: (x.state, x.score), reverse=True)
                if evaluate_result_list[0].state == State.Match:
                    _conflict = []
                    for _i in range(1, len(evaluate_result_list)):
                        if evaluate_result_list[_i].state == State.Conflict:
                            _conflict.append(evaluate_result_list[_i].right_frag)
                    if len(_conflict) > 0:
                        return EvaluateResult(State.MatchAndConflict, evaluate_result_list[0].score,
                                              evaluate_result_list[0].left_frag,
                                              evaluate_result_list[0].right_frag,
                                              _conflict)
                return evaluate_result_list[0]

        _result = []
        moved_list = [(_m[0], fsc.modified.save_to_target_service(_m[1], _rep_srv)) for _m in moved_list]
        for _m in moved_list:
            _r = handle_match_and_conflict(
                deep_evaluate(_m[1], knowledge_srv))
            if _r:
                _r.frag = _m[0]
                _result.append(_r)

                #todo 考虑在此处增加对A，B重复后的专项阈值衰减。 此功能未调试完成。 fengyh 2015-10-19
#                 if _r.conflict.__len__() == 0:
#                     tp = ThresholdProcess(_r.frag)
#                     tp.run_decrease()

        _result.sort(key=lambda x: (x.state, x.score), reverse=True)
        if len(_result) > 0:
            if _result[0].state != State.NotExist:
                return _result[0]

        if sentence.SentenceType == SentenceTypeEnum.NotAsk:
            _studied_result = loongtian.nvwa.core.engines.studying.study(moved_list)
            return EvaluateResult(State.NotExist, 0, _studied_result[0], _studied_result[1], frag=_studied_result[2])
        else:
            return EvaluateResult(State.NotExist, 0, moved_list[0][0], moved_list[0][1], frag=moved_list[0][0])

    @staticmethod
    def choose(structure_list):
        return structure_list[0]


evaluator_center = Evaluator()

if __name__ == '__main__':
    import doctest

    doctest.testmod()