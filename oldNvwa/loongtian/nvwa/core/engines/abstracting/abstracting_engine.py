#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    abstracting_engine.py 
Created by zheng on 2015/1/20.
UpdateLog:

"""
from loongtian.nvwa.service import knowledge_srv, fragment_srv, real_object_srv
from loongtian.nvwa.service import original_srv
from loongtian.nvwa.core.engines.conflicting import conflict
from loongtian.nvwa.entities import ConflictTypeEnum
from loongtian.nvwa.service.repository_service.real_object import RealObjectService

abstract_threshold = 2
CommonIsType = 0
InheritFromType = 1


class AbstractingEngine:
    '''
    抽象引擎
    对指定相同父对象的知识，进行抽象简化，相同属性挂到父对象
    如果被抽象属性被引用，保留原值
    解决抽象的属性和父对象原有属性的冲突
    '''

    def __init__(self):
        self.service = knowledge_srv

    def find_abstract(self, fragment):
        '''
        找到符合抽象条件的数据
        :return:所有符合抽象范围内的对象ID列表
        '''
        _node = self.service.get(fragment.ref.Id)
        if not _node: return []

        _start = _node.Start
        _node1 = self.service.get(_start)
        if not _node1: return []

        _end1 = _node1.End

        _list = []
        _type_list = []
        # 抽象条件是‘通用是’和‘继承自’
        # liuyl 2015.2.2 这里要对通用是 和 继承自 有所区分,以type列表形式传出
        if _end1 != original_srv.InheritFrom._obj.Id and _end1 != original_srv.CommonIs._obj.Id:
            return _type_list, _list
        _l = self.service.base_deduce_forward(original_srv.InheritFrom._obj.Id, _node.End)
        _list.extend(_l)
        _type_list.extend([InheritFromType] * len(_l))
        _l = self.service.base_deduce_forward(original_srv.CommonIs._obj.Id, _node.End)
        _list.extend(_l)
        _type_list.extend([CommonIsType] * len(_l))

        # 抽象限制，暂定5
        # todo 随时调整，可配置为常量

        if len(_list) < abstract_threshold: return [], []

        return _type_list, _list

    def get_details(self, list):
        '''
        (0,有,腿),(0,有,腿) 0：站位
        :param list:需要抽象的所有对象Id列表
        :return:dict
        '''
        ret = {}
        for _item in list:
            for _it in self.service.base_select_start(_item):
                _item1 = _it.End
                if _item1 == original_srv.InheritFrom._obj.Id or _item1 == original_srv.CommonIs._obj.Id:
                    # 继承自和通用是不抽取， 抽象的条件
                    continue
                for _it1 in self.service.base_select_start(_it.Id):
                    _item2 = _it1.End
                    detail = (0, _item1, _item2)
                    if ret.get(_item):
                        ret.get(_item).add(detail)
                    else:
                        ret[_item] = set([detail])
        return ret

    def get_commons(self, dic):
        '''
        不考虑特例 只有全部都有的属性才抽象
        :param dic:所有的待抽象对象的构成列表
        :return:共有构成
        '''
        ret = None
        for k in dic:
            value = dic[k]
            if ret == None:
                ret = value
            else:
                ret = ret.intersection(value)
        return ret

    def get_entity(self, id):
        '''
        通过Id获得entity，可能是object或knowledge
        :param id:Id
        :return:
        '''
        if self.service.get(id):
            return self.service.get(id)
        elif RealObjectService.get(id):
            return RealObjectService.get(id)

        return None


    def update_parent(self, parentId, commons):
        '''
        共有构成抽象到父对象
        :param parentId:父对象Id
        :param commons:共有构成
        :return:
        '''
        for item in commons:
            _left, _relation, _right = parentId, item[-1], item[-2]

            from loongtian.nvwa.service import fragment_srv

            _start = fragment_srv.generate(self.get_entity(_left), self.service)
            _re = fragment_srv.generate(self.get_entity(_relation), self.service)
            _end = fragment_srv.generate(self.get_entity(_right), self.service)

            _r, _c = conflict.check(_start, _re, knowledge_srv)

            # 找到牛有
            if _r == ConflictTypeEnum.Finded:
                _k, _ = conflict.check(_c[0], _end)
                if _k == ConflictTypeEnum.Conflict or _k == ConflictTypeEnum.FindedAndConflict:
                    continue

            # 没找到牛有
            # if _r == ConflictTypeEnum.NotFinded:
            # pass

            # 冲突
            if _r == ConflictTypeEnum.Conflict or _r == ConflictTypeEnum.FindedAndConflict:
                _k, _ = conflict.check(_c[1], _end)
                if _k == ConflictTypeEnum.Finded:
                    continue

            # if _r == ConflictTypeEnum.FindedAndConflict:
            #    pass

            self.service.create_t_structure(self.get_entity(_left), self.get_entity(_right), self.get_entity(_relation))


    def update_child(self, pId, type_list, list, details):
        '''
        子对象删除共有构成
        :param pId:父对象Id
        :param list:子对象id列表
        :param commons: 共有属性
        :return:
        '''
        _pProperty = self.get_details([pId])[pId]
        for _i in range(len(list)):
            # liuyl 2015.2.2 只有基于继承自的抽象才删除原对象的属性
            if type_list[_i] == CommonIsType:
                continue
            item = list[_i]
            detail = details[item]
            if not detail: continue
            common = _pProperty.intersection(detail)
            for co in common:
                _left, _relation, _right = item, co[-2], co[-1]
                _t1 = self.service.base_select_start_end(_left, _relation)
                _t2 = self.service.base_select_start_end(_t1.Id, _right)

                self.service.delete_by_key(_t2.Id)
                if not self.service.base_select_start(_t1.Id):
                    self.service.delete(_t1)

    def abstract(self, fragment):
        _frag = fragment_srv.get_same_from_target_service(fragment, self.service)
        _type_list, _list = self.find_abstract(_frag)

        # 没找到符合抽象条件的相关数据
        if len(_list) == 0: return False
        _pId = fragment.end.Id

        # 抽象对象的所有构成（一层）
        _details = self.get_details(_list)

        # 所有共有构成
        _common = self.get_commons(_details)

        # 共有构成上提
        self.update_parent(_pId, _common)

        # 整理子对象
        self.update_child(_pId, _type_list, _list, _details)

