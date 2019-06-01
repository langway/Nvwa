#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    mover 
Author:   Liuyl 
DateTime: 2014/9/9 17:11 
UpdateLog:
1、Liuyl 2014/9/9 Create this File.

mover
>>> print("No Test")
No Test
"""
import itertools
from loongtian.nvwa.common.cache.cache import i_cache
from loongtian.nvwa.core.engines import modifying
from loongtian.nvwa.core.engines.modifying import get_target_for_frag
from loongtian.nvwa.core.engines.threshold.sort import threshold_sort, threshold_distance_sort
from loongtian.nvwa.service.fragment_service.action import ActionFragmentEnum

__author__ = 'Liuyl'

from loongtian.nvwa.service import *
from loongtian.nvwa.core.gdef import OID


class ActionMoverHelper(object):
    """
    action的迁移辅助类,每个action在执行迁移前构造一个该对象,用于导入action的各种定义并负责执行action的迁移逻辑
    """

    def __init__(self, real_object):
        self.real_object = real_object
        self.act = fsc.action.generate(self.real_object, knowledge_srv)
        _unassemble = fsc.action.unassemble(self.act)
        self.sequence = [_unassemble[ActionFragmentEnum.Sequence]]
        self.steps = [_unassemble[ActionFragmentEnum.Steps]]
        self.place_holder_set = set()
        self.step_frag_list = []
        self.check_frag_list = []
        self.FRestrict = real_object_srv.get(OID.FRestrict)
        self.BRestrict = real_object_srv.get(OID.BRestrict)
        self.ActOuterPH = real_object_srv.get(OID.ActOuterPH)
        self.outer_frag_list = []
        # 对step列表中每个step中的限定结构,外部挂接结构和迁移结果结构的定义进行提取,构造成fragment对象,放入各自列表
        for _step in self.steps:
            _step_frag = []
            _check_frag = []
            _out_frag = []
            for _s in _step:
                _frag = fragment_srv.generate(_s, rep_srv=knowledge_srv)
                _deep_end_for_start_frag = fragment_srv.get_deep_end(_frag)
                _deep_start_for_start_frag = fragment_srv.get_deep_start(_frag)
                # 提取限定结构
                if _deep_end_for_start_frag \
                        and (original_srv.Equal.check(_deep_end_for_start_frag.ref, self.FRestrict)
                             or original_srv.Equal.check(_deep_end_for_start_frag.ref, self.BRestrict)):
                    _check_frag.append(_frag)
                # 提取外部挂接结构
                elif _deep_start_for_start_frag and original_srv.Equal.check(_deep_start_for_start_frag.ref,
                                                                             self.ActOuterPH):
                    _out_frag.append(_frag)
                # 提取迁移结果结构
                else:
                    _step_frag.append(_frag)

            self.step_frag_list.append(_step_frag)
            self.check_frag_list.append(_check_frag)
            self.outer_frag_list.append(_out_frag)

    def check_place_holder(self, entity):
        """
        判断一个object是不是一个占位符
        """
        if entity.Id not in self.place_holder_set:
            if not original_srv.InheritFrom.PlaceHolder.check(entity):
                return False
            self.place_holder_set.add(entity.Id)
        return True

    def generate_sequence_frag(self, pl_dict):
        _frag = fragment_srv.replace_real_object_and_create_new_frag(
            fragment_srv.generate(self.sequence[0], knowledge_srv),
            pl_dict)
        return _frag

    def sequence_check(self, frag):
        """
        序列验证,并将占位符与对应的内部结构以字典形式返回给上层
        """

        def do_sequence_check(seq_frag, target_frag):
            _place_holder_to_frag_dict = dict()

            def deep_sequence_check(seq_deep_frag, target_deep_frag):
                if not seq_deep_frag or not target_deep_frag:
                    return False
                if original_srv.Equal.check(seq_deep_frag.ref, target_deep_frag.ref):
                    return True
                if original_srv.Equal.check(seq_deep_frag.ref, self.real_object):
                    return True
                if self.check_place_holder(seq_deep_frag.ref):
                    _place_holder_to_frag_dict[seq_deep_frag.ref.Id] = target_deep_frag
                    return True
                _end_frag_for_seq_frag = fragment_srv.get_end(seq_deep_frag)
                _end_frag_for_target_frag = fragment_srv.get_end(target_deep_frag)
                if not deep_sequence_check(_end_frag_for_seq_frag, _end_frag_for_target_frag):
                    return False
                _start_frag_for_seq_frag = fragment_srv.get_start(seq_deep_frag)
                _start_frag_for_target_frag = fragment_srv.get_start(target_deep_frag)
                if not deep_sequence_check(_start_frag_for_seq_frag, _start_frag_for_target_frag):
                    return False
                return True

            if deep_sequence_check(seq_frag, target_frag):
                return _place_holder_to_frag_dict
            else:
                return None

        for _seq in self.sequence:
            # todo 暂时只取了每个序列的第一个
            _seq_frag = fragment_srv.generate(_seq, rep_srv=knowledge_srv)
            _result = do_sequence_check(_seq_frag, frag)
            if _result:
                return _result
        return None

    def step_check(self, pl_dict):
        """
        限定验证,如action定义了对其占位符的限定,则检验占位符对应的内部结构是否满足该占位符的限定
        """

        def check_forward_restrict(target_frag, check_frag):
            """
            正向限定,如占位符--继承自--动物类
            """
            _deep_end_for_start_frag = fragment_srv.get_end(
                fragment_srv.get_start(check_frag))
            _end_frag = fragment_srv.get_end(check_frag)
            return knowledge_srv.base_verify_forward(target_frag.ref.Id, _deep_end_for_start_frag.ref.Id,
                                                     _end_frag.ref.Id)

        def check_backward_restrict(target_frag, check_frag):
            """
            逆向限定,如动物类--组件--占位符
            """
            _end_frag = fragment_srv.get_end(check_frag)
            return knowledge_srv.base_verify_forward(target_frag.ref.Id, _end_frag.ref.Id)

        if len(self.check_frag_list) == 0:
            return True
        # todo 暂时只取了第一个限定
        for _check in self.check_frag_list[0]:
            _start_frag = fragment_srv.get_start(_check)
            _pl_frag = fragment_srv.get_start(_start_frag)
            _restrict_frag = fragment_srv.get_end(_start_frag)
            _check_frag = fragment_srv.get_end(_check)
            _target_frag = pl_dict[_pl_frag.ref.Id]
            if original_srv.Equal.check(_restrict_frag.ref, self.FRestrict):
                if not check_forward_restrict(_target_frag, _check_frag):
                    return False
            elif original_srv.Equal.check(_restrict_frag.ref, self.BRestrict):
                if not check_backward_restrict(_target_frag, _check_frag):
                    return False
        return True

    def move(self, pl_dict):
        # todo 暂时只取了第一个step
        _step = self.step_frag_list[0][0]
        _res = fsc.modified.replace_real_object_and_create_new_frag(_step, pl_dict)
        for _outer in self.outer_frag_list[0]:
            _new_outer = fsc.modified.replace_real_object_and_create_new_frag(_outer, pl_dict)
            fragment_srv.save_to_target_service(_new_outer, _res.rep_srv)
        return _res

    @staticmethod
    def is_action(entity_id):
        return fsc.action.check(fragment_srv.generate(real_object_srv.get(entity_id), knowledge_srv))


class Mover(object):
    """
    分组执行类
    """
    # todo 当start,end都为action时,一个分组结果会得到两个迁移结果,这种情况的处理没有实现,因为递归迁移后一个分组结果会分裂出多个迁移结果,导致算法复杂,留待后续解决

    obj_id = ''

    @staticmethod
    def execute(group_results, sentence):
        _action_dict = dict()
        _result_list = []
        _children_dict = dict()

        def get_sorted_children(real_object):
            if real_object not in _children_dict:
                _children_with_distance = original_srv.relation_deep_find_with_distance(original_srv.SymbolInherit,
                                                                                        right=real_object)
                _children_with_distance.sort(cmp=threshold_distance_sort)
                _children = [_cd[0] for _cd in _children_with_distance]
                _children_dict[real_object] = _children
            else:
                _children = _children_dict[real_object]
            return _children

        class ActionMoverHelperList(list):
            def __init__(self, default_action):
                super(ActionMoverHelperList, self).__init__([])
                self.default_action = default_action
                for _c in get_sorted_children(default_action):
                    self.append(ActionMoverHelper(_c))

        def get_action_helper_list(real_object):
            if not real_object:
                return None
            _action_helper_list = _action_dict.get(real_object.Id, None)
            if not _action_helper_list:
                if original_srv.InheritFrom.DefaultAction.check(real_object):
                    _action_helper_list = ActionMoverHelperList(real_object)
                    _action_dict[real_object.Id] = _action_helper_list
            return _action_helper_list

        _buffer = {}

        @i_cache(_buffer, lambda x, y: x[1].ref.Id)
        def deep_move(action_helper_list, frag):
            _r_list = []
            _temp_list = []
            for _h in action_helper_list:
                _place_holder_to_frag_dict = _h.sequence_check(frag)
                if _place_holder_to_frag_dict:
                    _temp_list.append([_h, _place_holder_to_frag_dict])
            for _t in _temp_list:
                for _record in _t[1].items():
                    _deep_result = do_move(_record[1])
                    if len(_deep_result) == 0:
                        return None
                    _t[1][_record[0]] = _deep_result
                _list = itertools.product(*[itertools.product([_r[0]], _r[1]) for _r in _t[1].items()])
                for _l in _list:
                    _d = {_l[0][0]: _l[0][1][1], _l[1][0]: _l[1][1][1]}
                    _d1 = {_l[0][0]: _l[0][1][0], _l[1][0]: _l[1][1][0]}
                    if _t[0].step_check(_d):
                        _result_frag_list = _t[0].move(_d)
                        # _r_list.extend(get_target_for_frag(_result_frag_list))
                        _frag = _t[0].generate_sequence_frag(_d1)
                        _r_list.append((_frag, _result_frag_list))
            return _r_list

        _modifier_buffer = {}

        @i_cache(_modifier_buffer, lambda x, y: x[0].ref.Id)
        def deep_modifier_move(frag):
            _class_object_list = []

            def append_to_list(c_object, de_meta=metadata_srv.get_by_string_value(u'的')):
                # liuyl 2015.2.6 处理被修限时直接忽略'的'
                # if c_object.Id in de_meta.RealObjectList:
                # return
                _class_object_list.append(
                    [fsc.modified.generate(_o, frag.rep_srv) for _o in get_sorted_children(c_object)])

            _start_frag = fragment_srv.get_start(frag)
            if real_object_srv.get(_start_frag.ref.Id):
                append_to_list(_start_frag.ref)
            _end_frag = fragment_srv.get_end(frag)
            while not real_object_srv.get(_end_frag.ref.Id):
                _start_frag = fragment_srv.get_start(_end_frag)
                if real_object_srv.get(_start_frag.ref.Id):
                    append_to_list(_start_frag.ref)
                _end_frag = fragment_srv.get_end(_end_frag)
            if real_object_srv.get(_end_frag.ref.Id):
                append_to_list(_end_frag.ref)

            def deep_modifier_move_for_matrix(matrix):
                _dim = len(matrix)
                _r = []
                if _dim == 2:
                    for _a in matrix[1]:
                        for _b in matrix[0]:
                            _r.extend(do_modifier_move(_a, _b))
                else:
                    for _i in range(0, _dim - 1):
                        _new_matrix = []
                        _new_matrix.extend(matrix[0:_i])
                        _dr = deep_modifier_move_for_matrix(matrix[_i:_i + 2])
                        if len(_dr) == 0:
                            continue
                        _new_matrix.append(_dr)
                        _new_matrix.extend(matrix[_i + 2:_dim])
                        _r.extend(deep_modifier_move_for_matrix(_new_matrix))
                return _r

            def do_modifier_move(a_frag, b_frag):
                _rep_srv = a_frag.rep_srv
                _a_modified_frag = getattr(a_frag, 'modified_frag', None)
                if not _a_modified_frag:
                    _a_modified_frag = a_frag
                _b_modified_frag = getattr(b_frag, 'modified_frag', None)
                if not _b_modified_frag:
                    _b_modified_frag = b_frag
                _modified_frag = fragment_srv.generate(
                    fragment_srv.create_l_structure(_b_modified_frag, _a_modified_frag, _rep_srv).ref,
                    rep_srv=_rep_srv)
                _r_list = [_r[0] for _r in modifying.get_target(a_frag, b_frag)]
                for _r in _r_list:
                    _r.modified_frag = _modified_frag
                return _r_list

            _result = deep_modifier_move_for_matrix(_class_object_list)
            if len(_result) == 0:
                if not all([len(_l) > 0 for _l in _class_object_list]):
                    return _result
                _index = range(len(_class_object_list)-1)
                _left = _class_object_list[0][0].ref
                for _i in _index:
                    _right = _class_object_list[_i + 1][0].ref
                    _left = frag.rep_srv.create_l_structure(_left, _right)
                _result.append(fragment_srv.generate(_left, rep_srv=frag.rep_srv))
            return [(_r.modified_frag if hasattr(_r, 'modified_frag') else _r, _r) for _r in _result]

        def do_move(frag):
            _result = []
            # 如果end为action,进行分组
            _end = frag.end
            _end_action_helper_list = get_action_helper_list(_end)
            if _end_action_helper_list:
                _r = deep_move(_end_action_helper_list, frag)
                if _r:
                    _result.extend(_r)
            # 如果start为action,进行分组
            _start = frag.start
            _start_action_helper_list = get_action_helper_list(_start)
            if _start_action_helper_list:
                _r = deep_move(_start_action_helper_list, frag)
                if _r:
                    _result.extend(_r)
            if _start_action_helper_list or _end_action_helper_list:
                return _result
            # 如果start不为空,且start不是action,查找start内部的end,如果为action,进行分组
            _deep_end = frag.deep_end
            _deep_end_action_helper_list = get_action_helper_list(_deep_end)
            if _deep_end_action_helper_list:
                _r = deep_move(_deep_end_action_helper_list, frag)
                if _r:
                    _result.extend(_r)
                return _result
            # 如果start和end都为空,frag为real_object,迁移结果为传入的frag本身
            if not _start and not _end:
                _result.extend([[fragment_srv.generate(_o, frag.rep_srv)] * 2 for _o in get_sorted_children(frag.ref)])
            # 如果start和end都不为空且都不是action,并且deeper_end_for_start也不是action,
            # 则执行修限相关逻辑的迁移
            if _start and _end and not _start_action_helper_list \
                    and not _deep_end_action_helper_list and not _deep_end_action_helper_list:
                _result.extend(deep_modifier_move(frag))

            return _result

        for _frag in group_results:
            _result_list.extend(do_move(_frag))
        # sentence.unknown_model = do_move(sentence.unknown_model)[0][1]
        return _result_list


mover_center = Mover()
if __name__ == '__main__':
    import doctest

    doctest.testmod()