#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    associating_engine 
Author:   fengyh 
DateTime: 2014/12/8 14:59 
UpdateLog:
1、fengyh 2014/12/8 Create this File.
2、fengyh 2015/2/3 增加缓存字典。如果已经查过对象的保存到字典里不用再查。

"""
import itertools

from loongtian.nvwa.core.gdef import OID
from loongtian.nvwa.entities.entity import RealObject
from loongtian.nvwa.service import real_object_srv, original_srv, knowledge_srv
from loongtian.nvwa.service import fragment_srv
from loongtian.nvwa.service.fragment_service.fragment_definition.fragment import KnowledgeForFragment


class AssociatingEngine(object):
    """
    """

    def __init__(self):
        self.analogy_rule_factor_k1 = 0
        self.analogy_rule_factor_k2 = 0
        self.fragment_pending_data = None

        pass

    def __init__(self, fragment_list):
        self.analogy_rule_factor_k1 = 0
        self.analogy_rule_factor_k2 = 0
        self.ready_frag_list = fragment_list
        self.match_object_dic = {}
        self.match_object_dic_list = []
        self.match_result_list = []
        self.match_result_distance_list = []
        self.object_possible_dic = {}
        pass

    def run(self):
        for frag in self.ready_frag_list:
            self.match_object_dic = {}
            self.match_object_dic_list = []

            self.__query_rule3__(frag)
        pass

    def __query_rule3__(self, frag):
        _object_list = filter((lambda f: isinstance(f, RealObject)), frag.data)
        _object_all_possible_list = [self.__find_all_father_and_brother(o) for o in _object_list]
        _descartes_list = [x for x in itertools.product(*_object_all_possible_list)]
        _descartes_dic_list = []
        _match_result_list = []
        for d in _descartes_list:

            _dic = {}
            for index, o in enumerate(d):
                _dic[_object_list[index]] = o
            _descartes_dic_list.append(_dic)

            knowledge_frag_peer = self.__replace_fragment_with_peer__(_dic, frag)
            if knowledge_frag_peer is not None:
                _distance = self.__judge_distance_of_frag__(_dic)
                self.match_object_dic[knowledge_frag_peer] = _distance

        self.match_object_dic_list = sorted(self.match_object_dic.iteritems(), key=lambda d: d[1])
        if self.match_object_dic_list.__len__() > 0:
            _after_sorted_object_tuple_and_value_tuple = zip(*self.match_object_dic_list)
            self.match_result_list.append(list(_after_sorted_object_tuple_and_value_tuple[0]))
            self.match_result_distance_list.append(list(_after_sorted_object_tuple_and_value_tuple[1]))
        else:
            self.match_result_list.append([])
            self.match_result_distance_list.append([])

        pass

    def __find_all_father_and_brother(self, object):
        #if self.object_possible_dic.get(object):
        # 如果字典中已有数据，则不用再数据库中再查。
        if self.object_possible_dic.has_key(object):
            return self.object_possible_dic.get(object)

        _direct_father_list = original_srv.select_direct_parent(object)

        _brother_list = []
        for o in _direct_father_list:
            _brother_list.extend(original_srv.select_direct_children(o))

        _all_father_list = original_srv.select_all_parent(object)

        return_list = list(set(_brother_list + _all_father_list))

        return_list = [_r for _r in return_list
                       if not original_srv.Equal.check(_r, original_srv.DefaultClass.obj())]
        # 如果是空列表，则自己对象加进来。
        if return_list.__len__() == 0:
            return_list.append(object)

        # 将查询结果放到字典中，再用的时候可以直接取。避免比必要的重查。fengyh 2015-2-3
        self.object_possible_dic[object] = return_list
        return return_list
        pass

    def __replace_fragment_with_peer__(self, object_dic, frag):
        """
        将输入信息片段中的所有对象，用入参字典中的对象替换。
        :param object_dic:
        :param frag:
        :return:
        """
        _rep_srv = fragment_srv.get_new_knowledge_for_fragment_service()

        # 过滤出来frag data中的所有knowledge片段
        _knowledge_frag_data_list = filter((lambda f: isinstance(f, KnowledgeForFragment)), frag.data)

        def __find_frag_in_frag_data__(frag_id):
            """
            查找指定id在frag片段data数据中的对应数据
            :param frag_id:
            :return:
            """
            find_frag = filter((lambda k: k.Id == frag_id), _knowledge_frag_data_list)
            if find_frag is not None and find_frag.__len__() > 0:
                return find_frag[0]
            else:
                return None

        def __inner_fragment_deal__(current_ref):
            """
            内部递归方法，遍历整个fragment并对其中的对象做替换。
            """
            object_start = real_object_srv.get(current_ref.Start)
            object_end = real_object_srv.get(current_ref.End)
            if object_start:
                if object_end:
                    new_knowledge = _rep_srv.create_l_structure(
                        object_dic[object_start],
                        object_dic[object_end])
                else:
                    knowledge_end = __find_frag_in_frag_data__(current_ref.End)
                    if knowledge_end is None:
                        return None

                    new_knowledge = _rep_srv.create_l_structure(
                        object_dic[object_start], __inner_fragment_deal__(knowledge_end))
            else:
                if object_end:
                    knowledge_start = __find_frag_in_frag_data__(current_ref.Start)
                    if knowledge_start is None:
                        return None
                    new_knowledge = _rep_srv.create_l_structure(__inner_fragment_deal__(knowledge_start),
                                                                object_dic[object_end])
                else:
                    knowledge_start = __find_frag_in_frag_data__(current_ref.Start)
                    knowledge_end = __find_frag_in_frag_data__(current_ref.End)
                    if knowledge_start is None or knowledge_end is None:
                        return None
                    new_knowledge = _rep_srv.create_l_structure(__inner_fragment_deal__(knowledge_start),
                                                                __inner_fragment_deal__(knowledge_end))
            return new_knowledge

        _ref = __inner_fragment_deal__(frag.ref)
        if _ref:
            _frag = fragment_srv.generate(_ref, rep_srv=_rep_srv)
            knowledge_frag = fragment_srv.get_same_from_target_service(_frag, knowledge_srv)
            return knowledge_frag
        else:
            return _ref

    def __judge_distance_of_frag__(self, like_object_dic):
        """
        判断新匹配fragment与原始fragment之间的距离，后续排序用
        1、判断是自己、兄弟还是父亲三种情况。
        判断方法：有共同父亲的是兄弟。
        2、自己加0分，兄弟加2分（目前只考虑直接近邻兄弟），父亲有几代加几分。
        :return:
        """

        def __find_n_generations_of_ancestors__(o_child, o_ancestors, i=0):
            _direct_father_list = original_srv.select_direct_parent(o_child)
            if o_ancestors in _direct_father_list:
                return i + 1
            else:
                for f in _direct_father_list:
                    temp_g = __find_n_generations_of_ancestors__(f, o_ancestors, i + 1)
                    if temp_g >= 0:
                        return temp_g
                    else:
                        _direct_children_list = original_srv.select_direct_children(f)
                        if o_ancestors in _direct_children_list:
                            return i + 2
            return -1

        temp_distance = 0
        _temp_distance_list = []
        for i in like_object_dic.iterkeys():
            if i == like_object_dic[i]:
                _temp_distance_list.append(temp_distance)
            else:
                _temp_distance_list.append(__find_n_generations_of_ancestors__(i, like_object_dic[i]))
                pass
        # 平方和开方 欧氏距离
        sum_distance = sum([a * a for a in _temp_distance_list]) ** (0.5)
        return sum_distance
