#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    base_knowledge_service 
Author:   Liuyl 
DateTime: 2014/11/3 11:08 
UpdateLog:
1、Liuyl 2014/11/3 Create this File.

base_knowledge_service
>>> print("No Test")
No Test
"""
__author__ = 'Liuyl'
import copy

from loongtian.nvwa.service.repository_service.base_rep_service import BaseRepService


class BaseKnowledgeService(BaseRepService):
    def __init__(self, rep):
        super(BaseKnowledgeService, self).__init__(rep)

    def get(self, key):
        _r = self.rep.get(key)
        if not _r:
            from loongtian.nvwa.service import real_object_srv
            _r = real_object_srv.get(key)
        return _r

    def create(self, **kwargs):
        _k = self.generate(**kwargs)
        _exist = self.base_select_start_end(_k.Start, _k.End)
        if _exist:
            _k = _exist
        else:
            self.save(_k)
        return _k

    def base_select_start(self, start):
        """
        根据传入的start值返回对应记录
        :param start:start值
        :return:具有该start值的所有对象的列表
        """
        return self.rep.get_by_start(start)

    def base_select_start_s(self, starts):
        """
        根据传入的start列表返回对应记录
        :param starts:start值列表
        :return:start值与具有该start值的所有对象的字典
        """
        return self.rep.gets_by_start(starts)

    def base_select_end(self, end):
        """
        根据传入的end值返回对应记录
        :param end:end值
        :return:具有该end值的所有对象的列表
        """
        return self.rep.get_by_end(end)

    def base_select_end_s(self, ends):
        """
        根据传入的end列表返回对应记录
        :param ends:end值列表
        :return:end值与具有该end值的所有对象的字典
        """
        return self.rep.gets_by_end(ends)

    def base_select_start_end(self, start, end):
        """
        根据传入的start,end返回start和end值相符的对象
        :param start:start值
        :param end:end值
        :return:返回start和end值相符的对象
        """
        _temp_list = self.base_select_start(start)
        _list = [_k for _k in _temp_list if _k.End == end]
        if len(_list) == 0:
            return None
        elif len(_list) == 1:
            return _list[0]
        else:
            raise Exception("表中存在冲突数据")

    def base_select_start_end_s(self, start_end_s):
        """
        根据传入的start列表返回对应记录
        :param start_end_s:(start,end)tuple列表
        :return:(start,end)值与具有该(start,end)值的所有对象的字典
        """
        _result = {}
        for _pair in set(start_end_s):
            _result[_pair] = self.base_select_start_end(_pair[0], _pair[1])
        return _result

    def base_filter_start(self, ks, starts):
        """
        根据传入的start值列表过滤Knowledge
        :param starts:start值列表
        :return:返回传入的knowledge中start值存在于传入的start列表中的knowledge列表
        """
        if not isinstance(starts, list):
            starts = [starts]
        return [k for k in ks if k.Start in starts]

    def base_filter_end(self, ks, ends):
        """
        根据传入的end值列表过滤Knowledge
        :param ends:end值列表
        :return:返回传入的knowledge中end值存在于传入的end列表中的knowledge列表
        """
        if not isinstance(ends, list):
            ends = [ends]
        return [k for k in ks if k and hasattr(k, 'End') and k.End in ends]

    def base_filter_id(self, ks, ids):
        """
        根据传入的id值列表过滤Knowledge
        :param ids:id值列表
        :return:返回传入的knowledge中id值存在于传入的id列表中的knowledge列表
        """
        if not isinstance(ids, list):
            ids = [ids]
        return [k for k in ks if k.Id in ids]

    def base_deduce_forward(self, *ends):
        """
        根据正向关系链推导出起点
        :param ends:正向推导结构的end值序列
        :return:返回符合该限定的所有目标的knowledge列表
        """
        _r0 = self.base_select_end(ends[-1])
        for _end in ends[-2::-1]:
            _r1 = self.gets([_entity.Start for _entity in _r0 if hasattr(_entity, 'Start')])
            _r0 = self.base_filter_end(_r1, _end)
        return [_item.Start for _item in _r0]

    def base_deduce_backward(self, start, *ends):
        """
        根据逆向关系链推导出终点
        :param start:逆向推导结构的起始start值
        :param ends:逆向推导结构的end值序列
        :return:返回符合该限定的所有目标的knowledge列表
        """
        _r0 = self.base_select_start_end(start, ends[0])
        for _end in ends[1:]:
            if not _r0:
                return []
            _r0 = self.base_select_start_end(_r0.Id, _end)
        if not _r0:
            return []
        return [entity.End for entity in self.base_select_start(_r0.Id)]

    def base_verify_forward(self, value, *ends):
        """
        根据正向关系链验证给定的value是否符合限定
        :param value:给定的值
        :param ends:正向推导结构的end值序列
        :return:True表示验证通过,False为未通过
        """
        _r0 = self.base_select_start_end(value, ends[0])
        for _end in ends[1:]:
            if not _r0:
                return False
            _r0 = self.base_select_start_end(_r0.Id, _end)
        if not _r0:
            return False
        return True

    def base_verify_backward(self, value, *starts):
        """
        根据逆向关系链验证给定的value是否符合限定
        :param value:给定的值
        :param starts:逆向推导结构的start值序列
        :return:True表示验证通过,False为未通过
        """

        return False

    def select_t_structure(self, left, right, bottom):
        _r0 = self.base_select_start_end(left.Id, right.Id)
        if not _r0:
            return None
        _r1 = self.base_select_start_end(_r0.Id, bottom.Id)
        return _r1

    def select_l_structure(self, start, end):
        return self.base_select_start_end(start.Id, end.Id)

    def generate_l_structure(self, left, right):
        _first = self.generate(Start=left.Id, End=right.Id, Display=u'({0}-{1})'.format(left.Display, right.Display))
        return _first

    def create_l_structure(self, left, right):
        _first = self.create(Start=left.Id, End=right.Id, Display=u'({0}-{1})'.format(left.Display, right.Display))
        return _first

    def create_t_structure(self, left, right, bottom):
        return self.create_t_structure2(left, right, bottom)[1]

    def create_t_structure2(self, left, right, bottom):
        _first = self.create_l_structure(left, right)
        _second = self.create_l_structure(_first, bottom)
        return _first, _second

    def generate_t_structure(self, left, right, bottom):
        return self.generate_t_structure2(left, right, bottom)[1]

    def generate_t_structure2(self, left, right, bottom):
        _first = self.generate_l_structure(left, right)
        _second = self.generate_l_structure(_first, bottom)
        return _first, _second

    class StructureForSelectBridge(object):
        def __init__(self, first, second, k_type):
            self.data = []
            self.data.append(first)
            self.data.append(second)
            self.key = first.Start
            self.left = first.Start
            self.right = first.End
            self.bottom = second.End
            self.out = second.Id
            self.from_key = []
            self.next = []
            if k_type == 0:  # start
                self.next.append(self.bottom)
                self.next.append(self.out)
            elif k_type == 1:  # end
                self.next.append(self.left)
                self.next.append(self.out)
            elif k_type == 2:  # out
                self.next.append(self.left)
                self.next.append(self.bottom)

    class StructureForSelectBridgeFactory(object):
        def __init__(self):
            self.data = {}

        def generate(self, first, second, k_type):
            _key = first.Id + second.Id
            if _key not in self.data:
                self.data[_key] = BaseKnowledgeService.StructureForSelectBridge(first, second, k_type)
            return self.data[_key]

        def get(self, first, second):
            _key = first.Id + second.Id
            if _key in self.data:
                return self.data[_key]
            else:
                return None

    def base_select_bridge(self, route_dict, next_set, target, factory):
        cur_set = copy.copy(next_set)
        next_set.clear()
        for _key in cur_set:
            _r1 = self.base_select_start(_key)
            for _k1 in _r1:
                if _k1.Id == _k1.Start:
                    continue
                _r1_1 = self.base_select_start(_k1.Id)
                for _k1_1 in _r1_1:
                    _s = factory.get(_k1, _k1_1)
                    if not _s:
                        _s = factory.generate(_k1, _k1_1, 0)
                        if _key not in route_dict:
                            route_dict[_key] = []
                        route_dict[_key].append(_s)
                        if cur_set[_key]:
                            _s.from_key.extend(cur_set[_key])
                        for _n in _s.next:
                            if _n not in next_set:
                                next_set[_n] = []
                            next_set[_n].append([_key, route_dict[_key].index(_s)])
            _r2 = self.base_select_end(_key)
            for _k2 in _r2:
                _k2_1 = self.get(_k2.Start)
                _s = factory.get(_k2_1, _k2)
                if not _s:
                    _s = factory.generate(_k2_1, _k2, 1)
                    if _key not in route_dict:
                        route_dict[_key] = []
                    route_dict[_key].append(_s)
                    if cur_set[_key]:
                        _s.from_key.extend(cur_set[_key])
                    for _n in _s.next:
                        if _n not in next_set:
                            next_set[_n] = []
                        next_set[_n].append([_key, route_dict[_key].index(_s)])
            _k3 = self.get(_key)
            if (not _k3) or _k3.Start == _key:
                continue
            _k3_1 = self.get(_k3.Start)
            if _k3_1:
                _s = factory.get(_k3_1, _k3)
                if not _s:
                    _s = factory.generate(_k3_1, _k3, 2)
                    if _key not in route_dict:
                        route_dict[_key] = []
                    route_dict[_key].append(_s)
                    if cur_set[_key]:
                        _s.from_key.extend(cur_set[_key])
                    for _n in _s.next:
                        if _n not in next_set:
                            next_set[_n] = []
                        next_set[_n].append([_key, route_dict[_key].index(_s)])

    def select_bridge(self, object1_id, object2_id, limit=5):
        _factory = BaseKnowledgeService.StructureForSelectBridgeFactory()
        route_dict = {}
        next_set = {object1_id: None}
        _target = object2_id
        self.base_select_bridge(route_dict, next_set, _target, _factory)
        _result_list = []
        for _i in range(1, limit):
            if _target in next_set:
                for _from_key in next_set[_target]:
                    _route = route_dict[_from_key[0]][_from_key[1]]
                    self._get_result_for_select_bridge(_result_list, set(), _route, route_dict)
                return _result_list
            self.base_select_bridge(route_dict, next_set, _target, _factory)
        return _result_list

    def _get_result_for_select_bridge(self, result_list, pre, route, route_dict):
        pre.add(route.data[0])
        pre.add(route.data[1])
        if len(route.from_key) > 0:
            for _key in route.from_key:
                self._get_result_for_select_bridge(result_list, copy.copy(pre), route_dict[_key[0]][_key[1]],
                                                   route_dict)
        else:
            result_list.append(pre)

    def replace_all_reference_id(self, old_id, new_id):
        _s_list = self.base_select_start(old_id)
        for _s in _s_list:
            _s.Start = new_id
            self.save(_s)
        _e_list = self.base_select_end(old_id)
        for _e in _e_list:
            _e.End = new_id
            self.save(_e)


if __name__ == '__main__':
    import doctest

    doctest.testmod()