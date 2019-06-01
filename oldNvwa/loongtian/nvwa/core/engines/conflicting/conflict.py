#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    conflict.py 
Created by zheng on 2015/1/7.
UpdateLog:

"""
import itertools
from loongtian.nvwa.service import *
from loongtian.nvwa.entities import ConflictTypeEnum


def is_self_check(start_fragment, end_fragment, target_srv):
    """
    自反是矛盾判断，如果找到A-IsSelf-B为符合,如A,B有公共父对象,且A和B不相同,则为冲突,其他为未找到
    :param start:A-IsSelf
    :param end:B
    """
    _a_ref = start_fragment.start
    _b_ref = end_fragment.ref
    if real_object_srv.type_check(_a_ref) and real_object_srv.type_check(_b_ref):
        _ex_current = target_srv.select_l_structure(start_fragment.ref, end_fragment.ref)
        if _ex_current:
            return ConflictTypeEnum.Finded, (_ex_current, None)
        else:
            _a_p = set([_p.Id for _p in original_srv.relation_deep_find(original_srv.InheritFrom,left=_a_ref)])
            _b_p = set([_p.Id for _p in original_srv.relation_deep_find(original_srv.InheritFrom,left=_b_ref)])
            if len(_a_p.intersection(_b_p))>0:
                _a_ref = start_fragment.start
                return ConflictTypeEnum.Conflict, (None, knowledge_srv.select_t_structure(
                    _a_ref, original_srv.IsSelf.obj(), _a_ref))
    return ConflictTypeEnum.NotFinded, (None, None)


def inherit_from_check(start_fragment, end_fragment, target_srv):
    """
    继承自矛盾判断，如果找到嵌套的A-InheritFrom-B为符合,
    如果找到嵌套的B-InheritFrom-A为冲突,否则为未找到
    :param start:A-InheritFrom
    :param end:B
    """
    # todo: 考虑传递的处理
    _a_ref = start_fragment.start
    _b_ref = end_fragment.ref
    if real_object_srv.type_check(_a_ref) and real_object_srv.type_check(_b_ref):
        _ex = original_srv.InheritFrom.get(_a_ref, _b_ref)
        if _ex:
            return ConflictTypeEnum.Finded, (_ex, None)
        _co = original_srv.InheritFrom.get(_b_ref, _a_ref)
        if _co:
            return ConflictTypeEnum.Conflict, (None, _co)
    return ConflictTypeEnum.NotFinded, (None, None)


def non_check(start_fragment, end_fragment, target_srv):
    """
    直接矛盾判断，牛有腿和牛没有腿的冲突
    :param start:
    :param end:
    """
    _ex_current = target_srv.select_l_structure(start_fragment.ref, end_fragment.ref)
    # start end 都是realobject
    _negate_start = None
    _negate_end = None
    _ex_non = None
    if real_object_srv.get(start_fragment.ref.Id):
        _negate_start = original_srv.Negate.find_one(start_fragment.ref)
    if real_object_srv.get(end_fragment.ref.Id):
        _negate_end = original_srv.Negate.find_one(end_fragment.ref)
    if _negate_end:
        _ex_non = target_srv.select_l_structure(start_fragment.ref, _negate_end)
    elif _negate_start:
        _ex_non = target_srv.select_l_structure(_negate_start, end_fragment.ref)
    if _ex_current and _ex_non:
        return ConflictTypeEnum.FindedAndConflict, (_ex_current, _ex_non)

    if _ex_current and not _ex_non:
        return ConflictTypeEnum.Finded, (_ex_current, None)

    if not _ex_current and _ex_non:
        return ConflictTypeEnum.Conflict, (None, _ex_non)

    if not _ex_current and not _ex_non:
        return ConflictTypeEnum.NotFinded, (None, None)


def single_value_check(start_fragment, end_fragment, target_srv):
    """
    单值属性矛盾,暂时没有引入多值标签，简单的直接父对象判断
    :param start:对象
    :param end:关系
    :return:
    """

    ret, links = ConflictTypeEnum.NotFinded, (None, None)
    if real_object_srv.get(start_fragment.ref.Id):
        return ret, links
    if original_srv.Equal.check(start_fragment.end, original_srv.Attribute.obj()):
        _all_attribute = original_srv.Attribute.find(left=start_fragment.start, target_srv=target_srv)
        _parents_for_end = original_srv.relation_deep_find(original_srv.InheritFrom,left=end_fragment.ref)
        for _a in _all_attribute:
            _parents_for_a =original_srv.relation_deep_find(original_srv.InheritFrom,left=_a)
            _inter = set([en.Id for en in _parents_for_end]).intersection(set([en.Id for en in _parents_for_a]))
            for _i in _inter:
                if not knowledge_srv.base_select_start_end(_i, original_srv.Multi.obj().Id):
                    ret, links = ConflictTypeEnum.Conflict, (
                        None, target_srv.select_t_structure(start_fragment.start, original_srv.Attribute.obj(), _a))

    return ret, links


def find_parents(obj):
    _ep = knowledge_srv.base_select_start_end(obj, original_srv.InheritFrom)
    if _ep:
        parents = knowledge_srv.base_select_start(_ep)
    else:
        parents = []
    return parents


def check(start_fragment, end_fragment, target_srv):
    """
    判断是否与知识库中的知识冲突,按层次从低到高check,调用过程来保证
    :param start_fragment:需要判断的输入start
    :param end_fragment:需要判断的输入end
    :return:
    """
    # 是非冲突判断
    ret, links = non_check(start_fragment, end_fragment, target_srv)
    if ret == ConflictTypeEnum.NotFinded and hasattr(start_fragment.ref, 'End'):
        _r_ref = start_fragment.end
        if original_srv.Equal.check(original_srv.IsSelf.obj(), _r_ref):
            ret, links = is_self_check(start_fragment, end_fragment, target_srv)
        elif original_srv.Equal.check(original_srv.InheritFrom.obj(), _r_ref):
            ret, links = inherit_from_check(start_fragment, end_fragment, target_srv)
        # 属性冲突判断
        else:
            ret, links = single_value_check(start_fragment, end_fragment, target_srv)

    return ret, links


Score = {ConflictTypeEnum.FindedAndConflict: 15, ConflictTypeEnum.Finded: 10, ConflictTypeEnum.Conflict: 5,
         ConflictTypeEnum.NotFinded: 0, "RealObject": 0}


class CheckResult(object):
    def __init__(self, state, match_frag, conflict_frag, score):
        self.state = state
        self.match_frag = match_frag
        self.conflict_frag = conflict_frag
        self.score = score

    @staticmethod
    def trans(result, inner_state, inner_score, target_srv):
        _match_frag = fragment_srv.generate(result[1][0], target_srv)
        _conflict_frag = fragment_srv.generate(result[1][1], target_srv)
        if result[0] == ConflictTypeEnum.Finded:
            if inner_state == ConflictTypeEnum.Finded:
                return [CheckResult(ConflictTypeEnum.Finded, _match_frag, None,
                                    inner_score + Score[ConflictTypeEnum.Finded])]
            elif inner_state == ConflictTypeEnum.Conflict:
                return [CheckResult(ConflictTypeEnum.Conflict, None, _match_frag,
                                    inner_score + Score[ConflictTypeEnum.Conflict])]
        elif result[0] == ConflictTypeEnum.Conflict:
            if inner_state == ConflictTypeEnum.Finded or inner_state == ConflictTypeEnum.Conflict:
                return [CheckResult(ConflictTypeEnum.Conflict, None, _conflict_frag,
                                    inner_score + Score[ConflictTypeEnum.Conflict])]
        elif result[0] == ConflictTypeEnum.FindedAndConflict:
            if inner_state == ConflictTypeEnum.Finded:
                return [CheckResult(ConflictTypeEnum.Finded, _match_frag, None,
                                    inner_score + Score[ConflictTypeEnum.Finded]),
                        CheckResult(ConflictTypeEnum.Conflict, None, _conflict_frag,
                                    inner_score + Score[ConflictTypeEnum.Conflict])]
            elif inner_state == ConflictTypeEnum.Conflict:
                return [CheckResult(ConflictTypeEnum.Conflict, None, _match_frag,
                                    inner_score + Score[ConflictTypeEnum.Finded]),
                        CheckResult(ConflictTypeEnum.Conflict, None, _conflict_frag,
                                    inner_score + Score[ConflictTypeEnum.Conflict])]
        return []


def deep_check(frag, target_srv):
    if real_object_srv.get(frag.ref.Id):
        return [CheckResult(ConflictTypeEnum.Finded, frag, None, 0)]
    _start = fragment_srv.get_start(frag)
    _end = fragment_srv.get_end(frag)
    _start_real_object = real_object_srv.get(_start.ref.Id)
    _end_real_object = real_object_srv.get(_end.ref.Id)
    if _start_real_object and _end_real_object:
        return CheckResult.trans(check(_start, _end, target_srv), ConflictTypeEnum.Finded, 0, target_srv)
    if not _start_real_object:
        _start_check_result = deep_check(_start, target_srv)
    else:
        _start_check_result = [CheckResult(ConflictTypeEnum.Finded, _start, None, 0)]
    if not _end_real_object:
        _end_check_result = deep_check(_end, target_srv)
    else:
        _end_check_result = [CheckResult(ConflictTypeEnum.Finded, _end, None, 0)]
    _result_pair_list = itertools.product(_start_check_result, _end_check_result)
    _result = []
    for _p in _result_pair_list:
        # start end 中任意一个未找到
        if _p[0].state == ConflictTypeEnum.NotFinded or _p[1].state == ConflictTypeEnum.NotFinded:
            continue
        # start end 都找到
        elif _p[0].state == ConflictTypeEnum.Finded and _p[1].state == ConflictTypeEnum.Finded:
            _result.extend(
                CheckResult.trans(check(_p[0].match_frag, _p[1].match_frag, target_srv), ConflictTypeEnum.Finded,
                                  _p[0].score + _p[1].score, target_srv))
        elif _p[0].state == ConflictTypeEnum.Finded and _p[1].state == ConflictTypeEnum.Conflict:
            _result.extend(
                CheckResult.trans(check(_p[0].match_frag, _p[1].conflict_frag, target_srv), ConflictTypeEnum.Conflict,
                                  _p[0].score + _p[1].score, target_srv))
        elif _p[0].state == ConflictTypeEnum.Conflict and _p[1].state == ConflictTypeEnum.Finded:
            _result.extend(
                CheckResult.trans(check(_p[0].conflict_frag, _p[1].match_frag, target_srv), ConflictTypeEnum.Conflict,
                                  _p[0].score + _p[1].score, target_srv))
        elif _p[0].state == ConflictTypeEnum.Conflict and _p[1].state == ConflictTypeEnum.Conflict:
            _result.extend(
                CheckResult.trans(check(_p[0].conflict_frag, _p[1].conflict_frag, target_srv),
                                  ConflictTypeEnum.Conflict,
                                  _p[0].score + _p[1].score, target_srv))
    _result.sort(key=lambda x: (x.state, x.score), reverse=True)
    return _result


def remove_conflict(frag, conflict_frag):
    knowledge_srv.delete_by_key(conflict_frag.ref.Id)


def handle_conflict(frag, conflict_frag):
    pass