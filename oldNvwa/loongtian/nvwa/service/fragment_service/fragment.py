#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    fragment
Author:   Liuyl 
DateTime: 2014/11/3 13:33 
UpdateLog:
1、Liuyl 2014/11/3 Create this File.
2、fengyh 2014/11/4 为KnowledgeForFragment和Fragment添eq和hash方法实现。

fragment
>>> print("No Test")
No Test
"""
from loongtian.nvwa.service import real_object_srv, knowledge_srv, original_srv
from loongtian.nvwa.core.gdef import OID
from loongtian.nvwa.service.fragment_service.fragment_definition.collection import CollectionFragment
from loongtian.nvwa.service.fragment_service.fragment_definition.fragment import Fragment, KnowledgeForFragmentService, \
    KnowledgeForFragmentRepository
from loongtian.nvwa.entities.enum import enum

__author__ = 'Liuyl'


class FragmentEnum(object):
    """
    片段结构类型。
    liuyl 2014-12-16
    """

    def __init__(self):
        enum(FragmentEnum, 'DeepStart=0,DeepEnd=1,Start=2,End=3',
             sep=',')
        pass


FragmentEnum()


class FragmentFactory(object):
    def __init__(self):
        pass

    @staticmethod
    def create(ref, rep_srv):
        if real_object_srv.get(ref.Id):
            if original_srv.InheritFrom.Collection.check(ref, rep_srv):
                return CollectionFragment(ref, rep_srv)

        return Fragment(ref, rep_srv)


class FragmentService(object):
    """

    """

    def __init__(self):
        pass

    @staticmethod
    def check(frag, rep_srv):
        pass

    def create_t_structure(self, left_frag, right_frag, bottom_frag, rep_srv):
        _left = left_frag.ref if rep_srv.get(left_frag.ref.Id) else left_frag.save_to_target_rep_srv(rep_srv)
        _right = right_frag.ref if rep_srv.get(right_frag.ref.Id) else right_frag.save_to_target_rep_srv(rep_srv)
        _bottom = bottom_frag.ref if rep_srv.get(bottom_frag.ref.Id) else bottom_frag.save_to_target_rep_srv(
            rep_srv)
        return self.generate(rep_srv.create_t_structure(_left, _right, _bottom), rep_srv)

    def create_l_structure(self, left_frag, right_frag, rep_srv):
        _left = left_frag.ref if rep_srv.get(left_frag.ref.Id) else left_frag.save_to_target_rep_srv(rep_srv)
        _right = right_frag.ref if rep_srv.get(right_frag.ref.Id) else right_frag.save_to_target_rep_srv(rep_srv)
        return self.generate(rep_srv.create_l_structure(_left, _right), rep_srv)

    def select_t_structure(self, left_frag, right_frag, bottom_frag, rep_srv):
        _left = left_frag.ref if rep_srv.get(left_frag.ref.Id) else fragment_srv.get_same_from_target_service(
            left_frag, rep_srv)
        _right = right_frag.ref if rep_srv.get(right_frag.ref.Id) else fragment_srv.get_same_from_target_service(
            right_frag, rep_srv)
        _bottom = bottom_frag.ref if rep_srv.get(bottom_frag.ref.Id) else fragment_srv.get_same_from_target_service(
            bottom_frag, rep_srv)
        return self.generate(rep_srv.select_t_structure(_left, _right, _bottom), rep_srv)

    def select_l_structure(self, left_frag, right_frag, rep_srv):
        _left = left_frag.ref if rep_srv.get(left_frag.ref.Id) else fragment_srv.get_same_from_target_service(
            left_frag, rep_srv)
        _right = right_frag.ref if rep_srv.get(right_frag.ref.Id) else fragment_srv.get_same_from_target_service(
            right_frag, rep_srv)
        return self.generate(rep_srv.select_l_structure(_left, _right), rep_srv)

    def generate(self, ref, rep_srv):
        """
        创建一个片段对象
        :param ref: 指定片段信息的最外层对象
        :param rep_srv: 指定片段的数据仓库
        :return:
        """
        if not ref:
            return None
        return FragmentFactory.create(ref, rep_srv)

    def delete(self, frag, target_srv=None):
        if not target_srv:
            target_srv = frag.rep_srv
        # print(u'Remove: {}'.format(frag.ref.Display))
        target_srv.delete(frag.ref)


    def assemble(self, target_srv, *args, **kwargs):
        """
        组装
        :param target_srv:
        :param kwargs: deep_start,deep_end,start,end
        :return:
        """
        deep_start = kwargs.get('deep_start', None)
        deep_end = kwargs.get('deep_end', None)
        start = kwargs.get('start', None)
        end = kwargs.get('end', None)
        _ref = None
        if deep_start and deep_end and end:
            _ref = target_srv.create_t_structure(deep_start, deep_end, end)
        elif start and end:
            _ref = target_srv.create_l_structure(start, end)
        if _ref:
            return self.generate(_ref, rep_srv=target_srv)
        else:
            return None

    def unassemble(self, frag):
        """
        拆解
        :param frag:
        :return:
        """

        _result = dict()
        _result[FragmentEnum.DeepStart] = frag.deep_start()
        _result[FragmentEnum.DeepEnd] = frag.deep_end()
        _result[FragmentEnum.Start] = frag.start()
        _result[FragmentEnum.End] = frag.end()
        return _result

    def add_extra_ref(self, frag, extra_frag):
        self.save_to_target_service(extra_frag, frag.rep_srv)
        frag.extra_ref.append(extra_frag.ref)

    def trans_to_not_be_modifier_for_modifier(self, frag):
        _rep_srv = self.get_new_knowledge_for_fragment_service()
        _frag = self.save_to_target_service(frag, _rep_srv)

        def get_real_object_for_be_modifier(cur):
            _left = self.get_deep_start(cur)
            _right = self.get_end(cur)
            _not_modifier_left = trans_to_not_be_modifier(_left)
            _not_modifier_right = trans_to_not_be_modifier(_right)
            # 查找是否已为该修限结构创建了新对象
            # 查找_left的所有子对象
            _all_children_id_for_left = original_srv.select_all_children(_not_modifier_left.ref.Id)
            _exist_id = None
            for _child_id in _all_children_id_for_left:
                # 判断left的子对象是否与right存在未知双向关系
                _verify_fun = knowledge_srv.base_verify_forward
                if _verify_fun(_not_modifier_right.ref.Id,
                               OID.UnknownBiRelation, _child_id) or _verify_fun(_child_id, OID.UnknownBiRelation,
                                                                                _not_modifier_right.ref.Id):
                    _exist_id = _child_id
                    break
            if _exist_id:
                _new_left = real_object_srv.get(_exist_id)
                return self.generate(_new_left, rep_srv=_rep_srv)
            # 如果不存在 则创建left的新对象new_left,并有new_left-父对象-left的关系
            else:
                return cur

        def trans_to_not_be_modifier(cur):
            if real_object_srv.get(cur.ref.Id):
                return cur
            if self.is_be_modifier(cur):
                return get_real_object_for_be_modifier(cur)
            else:
                _start = self.get_start(cur)
                _end = self.get_end(cur)
                _not_modifier_start = trans_to_not_be_modifier(_start)
                _not_modifier_end = trans_to_not_be_modifier(_end)
                _temp = _rep_srv.create_l_structure(_not_modifier_start.ref, _not_modifier_end.ref)
                return self.generate(_temp, rep_srv=_rep_srv)

        return trans_to_not_be_modifier(_frag)

    def trans_to_not_be_modifier_for_rethink(self, frag):
        _rep_srv = self.get_new_knowledge_for_fragment_service()
        _frag = self.save_to_target_service(frag, _rep_srv)

        def create_new_real_object_for_be_modifier(cur):
            _left = self.get_deep_start(cur)
            _right = self.get_end(cur)
            _not_modifier_left = trans_to_not_be_modifier(_left)
            _not_modifier_right = trans_to_not_be_modifier(_right)
            # 查找是否已为该修限结构创建了新对象
            # 查找_left的所有子对象
            _all_children_id_for_left = original_srv.select_all_children(_not_modifier_left.ref.Id)
            _exist_id = None
            for _child_id in _all_children_id_for_left:
                # 判断left的子对象是否与right存在未知双向关系
                _verify_fun = knowledge_srv.base_verify_forward
                if _verify_fun(_not_modifier_right.ref.Id,
                               OID.UnknownBiRelation, _child_id) or _verify_fun(_child_id, OID.UnknownBiRelation,
                                                                                _not_modifier_right.ref.Id):
                    _exist_id = _child_id
                    break
            if _exist_id:
                _new_left = real_object_srv.get(_exist_id)
            # 如果不存在 则创建left的新对象new_left,并有new_left-父对象-left的关系
            else:
                _new_left = real_object_srv.create(
                    Display=u'{0}de{1}'.format(_not_modifier_right.ref.Display, _not_modifier_left.ref.Display))
                original_srv.InheritFrom.set(_new_left, _not_modifier_left.ref)
                original_srv.UnknownBiRelation.set(_new_left, _not_modifier_right.ref)
            return self.generate(_new_left, rep_srv=_rep_srv)

        def trans_to_not_be_modifier(cur):
            if real_object_srv.get(cur.ref.Id):
                return cur
            if self.is_be_modifier(cur):
                return create_new_real_object_for_be_modifier(cur)
            else:
                _start = self.get_start(cur)
                _end = self.get_end(cur)
                _not_modifier_start = trans_to_not_be_modifier(_start)
                _not_modifier_end = trans_to_not_be_modifier(_end)
                _temp = _rep_srv.create_l_structure(_not_modifier_start.ref, _not_modifier_end.ref)
                return self.generate(_temp, rep_srv=_rep_srv)

        return trans_to_not_be_modifier(_frag)

    def trans_to_be_modifier(self, frag):
        """
        将正常结构的片段转换成被修限结构
        :param frag:
        :return:
        """
        _new_deep_start_for_start = self.clone_to_independent_fragment(self.get_end(frag))
        _new_end = self.save_to_target_service(self.get_start(frag), _new_deep_start_for_start.rep_srv)
        _new_ref = _new_deep_start_for_start.rep_srv.create_t_structure(_new_deep_start_for_start.ref,
                                                                        real_object_srv.get(OID.BeModified),
                                                                        _new_end.ref)
        return self.generate(ref=_new_ref, rep_srv=_new_deep_start_for_start.rep_srv)

    def is_be_modifier(self, frag):
        """
        判断片段是否为被修限结构
        :param frag:
        :return:
        """
        _deep_end_for_start = self.get_deep_end(frag)
        if _deep_end_for_start:
            return original_srv.Equal.check(_deep_end_for_start.ref, real_object_srv.get(OID.BeModified))
        return False

    def is_quantity_is(self, frag):
        _deep_end_for_start = self.get_deep_end(frag)
        if _deep_end_for_start:
            return original_srv.Equal.check(_deep_end_for_start.ref, real_object_srv.get(OID.QuantityIs))
        return False

    def remove_be_modifier(self, frag):
        """
        将被修限结构的片段反转回原结构
        :param frag:
        :return:
        """
        _new_deep_start_for_start = self.clone_to_independent_fragment(self.get_deep_start(frag))
        _new_end = self.save_to_target_service(self.get_end(frag), _new_deep_start_for_start.rep_srv)
        _new_ref = _new_deep_start_for_start.rep_srv.create_l_structure(_new_end.ref, _new_deep_start_for_start.ref)
        return self.generate(ref=_new_ref, rep_srv=_new_deep_start_for_start.rep_srv)

    def replace_real_object_and_create_new_frag(self, source_frag, replace_dict):
        """
        传入一个字典和一个片段,将片段中出现的字典key替换成对应value中片段的ref.Id,并将所有相关数据合并到新的独立片段中
        :param source_frag:
        :param replace_dict:
        :return: 生成一个独立rep的frag,
        """
        _rep_srv = self.get_new_knowledge_for_fragment_service()

        def replace_deep_inner(cur):
            if cur.ref.Id in replace_dict:
                _frag = replace_dict[cur.ref.Id]
                self.save_to_target_service(_frag, _rep_srv)
                return _frag, _frag.ref.Display
            if real_object_srv.type_check(cur.ref):
                return cur, cur.ref.Display
            _new_start, _new_start_display = replace_deep_inner(self.get_start(cur))
            _new_end, _new_end_display = replace_deep_inner(self.get_end(cur))
            _new_cur = self.create_l_structure(_new_start, _new_end, _rep_srv)
            return _new_cur, _new_cur.ref.Display

        _f, _ = replace_deep_inner(source_frag)
        for _extra in source_frag._extra_ref:
            replace_deep_inner(_extra.Id)
        return _f

    @staticmethod
    def get_new_knowledge_for_fragment_service():
        return KnowledgeForFragmentService(KnowledgeForFragmentRepository())

    def clone_to_independent_fragment(self, source_frag):
        """
        将指定的片段中的信息克隆到一个独立片段中
        :param source_frag:
        :return:
        """
        _rep_srv = self.get_new_knowledge_for_fragment_service()
        return self.save_to_target_service(source_frag, _rep_srv)

    def get_same_from_target_service(self, fragment, target_srv):
        """
        传入一个依赖于任意仓库的片段,获取传入目标仓库中的完全符合该片段中信息结构的片段
        :param fragment: 依赖于任意仓库的片段
        :param target_srv: 目标仓库服务
        :return: 如目标仓库中存在该结构的片段,则返回依赖于目标仓库的该片段,否则返回None
        """

        def deep_get_target_id(cur_frag_id):
            if real_object_srv.get(cur_frag_id):
                return cur_frag_id
            _cur = fragment.rep_srv.get(cur_frag_id)
            if _cur:
                _target_start_id = deep_get_target_id(_cur.Start)
                _target_end_id = deep_get_target_id(_cur.End)
                if _target_end_id and _target_start_id:
                    _next_cur = target_srv.base_select_start_end(_target_start_id, _target_end_id)
                    if _next_cur:
                        return _next_cur.Id
                return None
            else:
                raise Exception('片段内数据不完整,无法保存')

        _target_id = deep_get_target_id(fragment.ref.Id)
        if not _target_id:
            return None
        _r = real_object_srv.get(_target_id)
        if _r:
            return self.generate(_r, rep_srv=target_srv)
        return self.generate(target_srv.get(_target_id), rep_srv=target_srv)

    def save_to_target_service(self, fragment, target_srv):
        """
        将片段的完整信息保存到目标仓库服务中.
        :param fragment:需要保存的片段
        :param target_srv:目标仓库服务
        :return: 返回片段在目标仓库中的新实例
        """
        return self.generate(fragment.save_to_target_rep_srv(target_srv), rep_srv=target_srv)

    def get_start(self, fragment):
        """
        获取片段ref的start值所指向的片段,生成的片段与传入的片段共用仓库
        :param fragment:
        :return:
        """
        return self.generate(fragment.start, rep_srv=fragment.rep_srv)

    def get_end(self, fragment):
        """
        获取片段ref的end值所指向的片段,生成的片段与传入的片段共用仓库
        :param fragment:
        :return:
        """
        return self.generate(fragment.end, rep_srv=fragment.rep_srv)

    def get_deep_start(self, fragment):
        """
        获取片段的直接start片段的start片段
        :param fragment:
        :return:
        """
        return self.generate(fragment.deep_start, rep_srv=fragment.rep_srv)

    def get_deep_end(self, fragment):
        """
        获取片段的直接start片段的end片段
        :param fragment:
        :return:
        """
        return self.generate(fragment.deep_end, rep_srv=fragment.rep_srv)

    def select_all_outer(self, fragment):
        """
        查找在传入片段的依赖仓库中查找直接包含了片段的所有外层片段
        :param fragment: 被包含的片段
        :return: 返回所有外层片段组成的list
        """
        _result = []

        def select_deep_outer(cur_fragment):
            _cur_outer_result = self.base_select_outer(cur_fragment)
            if len(_cur_outer_result) == 0:
                _result.append(cur_fragment)
            else:
                for _outer in _cur_outer_result:
                    select_deep_outer(_outer)

        select_deep_outer(fragment)
        return self.base_filter_repetition(_result)

    @staticmethod
    def base_filter_repetition(fragment_list):
        """
        去除重复片段
        :param fragment_list:
        :return:
        """
        _result = []
        _key_set = set()
        for _frag in fragment_list:
            if _frag.ref.Id not in _key_set:
                _result.append(_frag)
                _key_set.add(_frag.ref.Id)
        return _result

    def base_select_outer(self, fragment):
        """
        查找片段的直接外层片段
        :param fragment:
        :return:
        """
        _result = []
        _rep_srv = fragment.rep_srv

        def base_select_outer_for_start():
            _ref_in_start = _rep_srv.base_select_start(fragment.ref.Id)
            for _r in _ref_in_start:
                _result.append(self.generate(_r, rep_srv=_rep_srv))

        def base_select_outer_for_end():
            _ref_in_end = _rep_srv.base_select_end(fragment.ref.Id)
            for _r in _ref_in_end:
                _result.append(self.generate(_r, rep_srv=_rep_srv))

        base_select_outer_for_start()
        base_select_outer_for_end()
        return self.base_filter_repetition(_result)


if __name__ == '__main__':
    # import doctest
    #
    # doctest.testmod()

    from loongtian.nvwa.service import original_init_srv, fragment_srv

    original_init_srv.init()
    g_frag = fragment_srv.generate(real_object_srv.get(OID.InheritFrom), rep_srv=knowledge_srv)
    g_list = fragment_srv.select_all_outer(g_frag)
    for _f in g_list:
        print(_f.__str__())