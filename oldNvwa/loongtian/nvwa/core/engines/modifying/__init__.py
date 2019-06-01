#!/usr/bin/env python
# coding: utf-8
""" modifying
修限
"""
import loongtian.nvwa.core.engines.associating
from loongtian.nvwa.core.engines.conflicting import conflict
from loongtian.nvwa.entities import ConflictTypeEnum
from loongtian.nvwa.service import fragment_srv, fsc, knowledge_srv, original_srv, real_object_srv
from loongtian.nvwa.service.fragment_service.fragment import FragmentEnum

__author__ = 'Liuyl'


def get_modifier_target(a_frag, b_frag):
    _frag = fragment_srv.select_t_structure(
        a_frag, fragment_srv.generate(original_srv.BeModified.obj(), knowledge_srv), b_frag, knowledge_srv)
    if _frag:
        return [(a_frag, _frag)]
    # _frag = fragment_srv.select_t_structure(
    # a_frag, fragment_srv.generate(original_srv.BeModified.obj(), knowledge_srv), b_frag, memory_srv)
    # if _frag:
    #     return [(a_frag, _frag)]
    return []


def get_component_target(a_frag, b_frag):
    # 腿a 被修限 牛b 如果b组件a,返回a
    _frag = fragment_srv.select_t_structure(
        b_frag, fragment_srv.generate(original_srv.Component.obj(), knowledge_srv), a_frag, knowledge_srv)
    if _frag:
        return [(a_frag, _frag)]
    else:
        return []


def get_attribute_target(a_frag, b_frag):
    _result = []
    # 颜色a 被修限 腿b 返回颜色a的子对象v, v满足是b的属性值
    _attr_values = original_srv.relation_deep_find(original_srv.InheritFrom, right=a_frag.ref)
    _attr_values.append(a_frag.ref)
    for _v in _attr_values:
        _v_frag = fragment_srv.generate(_v, knowledge_srv)
        _frag = fragment_srv.select_t_structure(
            b_frag, fragment_srv.generate(original_srv.Attribute.obj(), knowledge_srv), _v_frag, knowledge_srv)
        if _frag:
            _result.append((_v_frag, _frag))
    # 腿a 被修限 黄色b 如果a带有属性b,返回a
    _frag = fragment_srv.select_t_structure(
        a_frag, fragment_srv.generate(original_srv.Attribute.obj(), knowledge_srv), b_frag, knowledge_srv)
    if _frag:
        _result.append((a_frag, _frag))
    return _result


get_target_method = [get_attribute_target, get_component_target]


def get_target(a_frag, b_frag):
    _result = []
    for _m in get_target_method:
        _result.extend(_m(a_frag, b_frag))
    if len(_result) == 0:
        _result.extend(get_modifier_target(a_frag, b_frag))
    return _result


def get_target_without_default(a_frag, b_frag):
    _result = []
    for _m in get_target_method:
        _result.extend(_m(a_frag, b_frag))
    return _result


def get_target_for_frag(frag):
    _result = []
    if fsc.modified.check(frag, frag.rep_srv):
        unassemble = fsc.modified.unassemble(frag)
        _a_frag = unassemble[FragmentEnum.DeepStart]
        _b_frag = unassemble[FragmentEnum.End]
        _result = get_target(_a_frag, _b_frag)
    return _result


def deep_trans(frag):
    if fsc.modified.check(frag, knowledge_srv):
        unassemble = fsc.modified.unassemble(frag)
        _new_a = deep_trans(unassemble[FragmentEnum.DeepStart])
        _new_b = deep_trans(unassemble[FragmentEnum.End])
        return do_trans(_new_a, _new_b)
    else:
        _start = fragment_srv.get_start(frag)
        _end = fragment_srv.get_end(frag)
        if _start and _end:
            _new_start = deep_trans(_start)
            _new_end = deep_trans(_end)
            return fragment_srv.generate(frag.rep_srv.create_l_structure(_new_start.ref, _new_end.ref), frag.rep_srv)
    return frag


def trans(frag):
    # _rep_srv = fragment_srv.get_new_knowledge_for_fragment_service()
    # _target_frag = fragment_srv.save_to_target_service(frag, _rep_srv)
    if fsc.modified.check(frag, knowledge_srv):
        unassemble = fsc.modified.unassemble(frag)
        _a_frag = deep_trans(unassemble[FragmentEnum.DeepStart])
        _b_frag = deep_trans(unassemble[FragmentEnum.End])
        if not _a_frag or not _b_frag:
            return frag
        _target = get_target_without_default(_a_frag, _b_frag)
        if len(_target) > 0:
            return _target[0][0]
        _result = do_trans(_a_frag, _b_frag)
        return _result or frag
    return frag


def do_trans(a_frag, b_frag):
    _rep_srv = fragment_srv.get_new_knowledge_for_fragment_service()
    _analogize_result, _trans_method = analogize(a_frag, b_frag, _rep_srv)
    if _analogize_result and _trans_method:
        _result = _trans_method(_analogize_result[0])
        return _result
    else:
        return None


def analogize(a_frag, b_frag, rep_srv):
    _result = (None, None)
    _min_distance = 1000
    for _m in analogize_method:
        _analogize_result, _trans_method = _m(a_frag, b_frag, rep_srv)
        if _analogize_result and _analogize_result[2] < _min_distance:
            _result = (_analogize_result, _trans_method)
            _min_distance = _analogize_result[2]
    return _result


def analogize_for_component(a_frag, b_frag, rep_srv):
    _frag = fsc.modified.create_t_structure(
        b_frag, fsc.modified.generate(original_srv.Component.obj(), rep_srv), a_frag, rep_srv)
    associating = loongtian.nvwa.core.engines.associating.AssociatingEngine([_frag])
    associating.run()
    _analogize_result_list = loongtian.nvwa.core.engines.associating.get_sorted_result(associating)
    return _analogize_result_list[0] if len(_analogize_result_list) > 0 else None, trans_for_component


def analogize_for_attribute_forward(a_frag, b_frag, rep_srv):
    """
    a-被修限-b 转为 a-属性-b (如 苹果-被修限-黄色 转为 苹果-属性-黄色)
    :param a_frag:
    :param b_frag:
    :param rep_srv:
    :return:
    """
    _r_frag = fsc.modified.generate(original_srv.Attribute.obj(), rep_srv)
    _frag = fsc.modified.create_t_structure(a_frag, _r_frag, b_frag, rep_srv)
    associating = loongtian.nvwa.core.engines.associating.AssociatingEngine([_frag])
    associating.run()
    _analogize_result_list = loongtian.nvwa.core.engines.associating.get_sorted_result(associating)
    return _analogize_result_list[0] if len(_analogize_result_list) > 0 else None, trans_for_attribute_forward


def analogize_for_attribute_backward(a_frag, b_frag, rep_srv):
    """
    a-被修限-b 转为 b-属性-a (如 颜色-被修限-苹果 转为 苹果-属性-颜色)
    :param a_frag:
    :param b_frag:
    :param rep_srv:
    :return:
    """
    _r_frag = fsc.modified.generate(original_srv.Attribute.obj(), rep_srv)
    _frag = fsc.modified.create_t_structure(b_frag, _r_frag, a_frag, rep_srv)
    associating = loongtian.nvwa.core.engines.associating.AssociatingEngine([_frag])
    associating.run()
    _analogize_result_list = loongtian.nvwa.core.engines.associating.get_sorted_result(associating)
    return _analogize_result_list[0] if len(_analogize_result_list) > 0 else None, trans_for_attribute_backward


analogize_method = [analogize_for_component, analogize_for_attribute_forward, analogize_for_attribute_backward]


def trans_for_attribute_forward(frag):
    """
    a-被修限-b 转为 a-属性-b (如 苹果-被修限-黄色 转为 苹果-属性-黄色) 如冲突,分裂出新的a,返回a
    :param frag:
    :return:
    """
    _a_frag = fsc.modified.get_deep_start(frag)
    _r_frag = fsc.modified.generate(original_srv.BeModified.obj(), frag.rep_srv)
    _b_frag = fsc.modified.get_end(frag)
    _modified_frag = fsc.modified.select_t_structure(_a_frag, _r_frag, _b_frag, knowledge_srv)
    _conflict = conflict.deep_check(frag, knowledge_srv)
    if len(_conflict) > 0 and _conflict[0].state == ConflictTypeEnum.Conflict:
        _new_a_frag = fsc.modified.generate(original_srv.clone_real_object(_a_frag.ref), knowledge_srv)
        for _c in _conflict:
            if _conflict[0].state == ConflictTypeEnum.Conflict:
                _new_conflict_frag = fsc.modified.select_t_structure(
                    _new_a_frag, fragment_srv.get_deep_end(_c.conflict_frag),
                    fragment_srv.get_end(_c.conflict_frag), knowledge_srv)
                fragment_srv.delete(_new_conflict_frag)
        fragment_srv.delete(_modified_frag, knowledge_srv)
        _new_modified_frag = fsc.modified.create_t_structure(_new_a_frag, _r_frag, _b_frag, knowledge_srv)
        _new_frag = fsc.modified.create_t_structure(
            _new_a_frag, fsc.modified.generate(original_srv.Attribute.obj(), knowledge_srv), _b_frag, knowledge_srv)
        _new_a_frag.modified_frag = _new_modified_frag
        return _new_a_frag
    else:
        fragment_srv.save_to_target_service(frag, knowledge_srv)
        _a_frag.modified_frag = _modified_frag
        return _a_frag


def trans_for_attribute_backward(frag):
    """
    a-被修限-b 转为 b-属性-a (如 颜色-被修限-苹果 转为 苹果-属性-颜色)
    :param frag:
    :return:
    """
    _a_frag = fsc.modified.get_deep_start(frag)
    _r_frag = fsc.modified.generate(original_srv.BeModified.obj(), frag.rep_srv)
    _b_frag = fsc.modified.get_end(frag)
    _modified_frag = fsc.modified.select_t_structure(_b_frag, _r_frag, _a_frag, knowledge_srv)
    _conflict = conflict.deep_check(frag, knowledge_srv)
    if len(_conflict) > 0 and _conflict[0].state == ConflictTypeEnum.Conflict:
        fsc.modified.delete(_modified_frag, knowledge_srv)
        return None
    else:
        fragment_srv.save_to_target_service(frag, knowledge_srv)
        _b_frag.modified_frag = _modified_frag
        return _b_frag


def trans_for_component(frag):
    _a_frag = fsc.modified.get_deep_start(frag)
    _r_frag = fsc.modified.generate(original_srv.BeModified.obj(), frag.rep_srv)
    _b_frag = fsc.modified.get_end(frag)
    _modified_frag = fsc.modified.select_t_structure(_b_frag, _r_frag, _a_frag, knowledge_srv)
    _conflict = conflict.deep_check(frag, knowledge_srv)
    if len(_conflict) > 0 and _conflict[0].state == ConflictTypeEnum.Conflict:
        fsc.modified.delete(_b_frag.modified_frag, knowledge_srv)
        return None
    else:
        fragment_srv.save_to_target_service(frag, knowledge_srv)
        _b_frag.modified_frag = _modified_frag
        return _b_frag


if __name__ == '__main__':
    import doctest

    doctest.testmod()