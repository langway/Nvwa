#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    admin_learn 
Created by zheng on 2014/12/11.
UpdateLog:

"""
import string
from loongtian.nvwa.core.engines.admin.original_relation_mapping import Mapper
from loongtian.nvwa.core.engines.threshold.sort import threshold_distance_sort
from loongtian.nvwa.core.gdef import OID, GlobalDefine
from loongtian.nvwa.core.maincenter.evaluator.evaluator import EvaluateResult
from loongtian.nvwa.core.maincenter.planner.plan import planer_center
from loongtian.nvwa.entities import CommandJobTypeEnum
from loongtian.nvwa.entities.sentence import Sentence
from loongtian.nvwa.service import *


def learn(input, address):
    _fragment, _sentence = genFragment(input)
    if not _fragment:
        return False
    _d = EvaluateResult()
    _d.left_frag = _fragment
    _planed_results = planer_center.execute(_d, _sentence)
    for item in _planed_results:
        if item.type == CommandJobTypeEnum.Output:
            item.t_struct = (item.t_struct, address)
        GlobalDefine().command_msg.put(item)
    return True


def get_sorted_children(real_object):
    _children_with_distance = original_srv.relation_deep_find_with_distance(
        original_srv.SymbolInherit, right=real_object)
    _children_with_distance.sort(cmp=threshold_distance_sort)
    _children = [_cd[0] for _cd in _children_with_distance]
    return _children


def genFragment(input):
    _strs = string.split(input)
    if len(_strs) <> 3: return None, None

    _l, _m, _r = _strs[0], _strs[1], _strs[2]

    # 获得顶级关系 如果取不到 返回None
    _relation = Mapper().getOriginalRelation(_strs[1])
    if _relation == None: return None, None

    # 左侧对象
    _templ = metadata_srv.get_by_string_value(_l)
    if not _templ:
        metadata_srv.create(_l)
    _left = get_sorted_children(metadata_srv.get_default_by_string_value(_l))[0]

    #右侧对象
    _tempr = metadata_srv.get_by_string_value(_r)
    if not _tempr:
        metadata_srv.create(_r)

    _right = get_sorted_children(metadata_srv.get_default_by_string_value(_r))[0]
    _rep_srv = fragment_srv.get_new_knowledge_for_fragment_service()

    _sentence = Sentence(_strs)
    _sentence.sentence_model = fragment_srv.generate(real_object_srv.get(OID.God), rep_srv=_rep_srv)

    _o = _rep_srv.create_t_structure(_left, _relation._obj, _right)
    _fragment = fragment_srv.generate(_o, _rep_srv)
    return _fragment, _sentence
