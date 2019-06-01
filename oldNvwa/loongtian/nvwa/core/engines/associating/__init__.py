#!/usr/bin/env python
# coding: utf-8
""" associating
联想引擎
"""
import itertools
from loongtian.nvwa.core.engines.associating.associating_engine import AssociatingEngine
from loongtian.nvwa.service import original_srv, fsc, fragment_srv, knowledge_srv


def get_sorted_result(associating):
    """
    对类比结果进行整理和排序,返回三元组(传入frag,类比出的frag,距离值)的列表,并按距离值升序排序
    :param associating:
    :return:
    """
    _result = []
    for _i in range(len(associating.ready_frag_list)):
        _result.extend(itertools.izip([associating.ready_frag_list[_i]] * len(associating.match_result_list[_i]),
                                      associating.match_result_list[_i], associating.match_result_distance_list[_i]))
    _result.sort(key=lambda x: x[2])
    return _result


def relation_subdivide(frag):
    """
    关系细分,A-R-B结构,查找R的子对象Ri,构造A-Ri-B,进行类比
    如有结果,对结果进行排序和分值筛选,取最优解为关系细分结果
    例如,用于有[通用]向组件的细分
    :param frag:
    :return:
    """
    _rep_srv = fragment_srv.get_new_knowledge_for_fragment_service()
    _a = fragment_srv.get_deep_start(frag)
    _r = fragment_srv.get_deep_end(frag)
    _b = fragment_srv.get_end(frag)
    _o_frag = fragment_srv.save_to_target_service(frag, _rep_srv)

    if not (_a and _b and _r):
        return None

    _r_children = original_srv.InheritFrom.find(right=_r.ref)
    _frag_list = [fragment_srv.create_t_structure(_a, fragment_srv.generate(_ri, _rep_srv), _b, _rep_srv) for _ri in
                  _r_children]
    if len(_frag_list) == 0:
        return None
    fragment_srv.delete(frag, knowledge_srv)
    associating = AssociatingEngine(_frag_list)
    associating.run()
    _result = get_sorted_result(associating)
    fragment_srv.save_to_target_service(_o_frag, knowledge_srv)
    return _result
