#!/usr/bin/env python
# coding: utf-8
"""
原始知识操作

Project:  nvwa
Title:    original 
Author:   Liuyl 
DateTime: 2014/10/29 9:51 
UpdateLog:
1、Liuyl 2014/10/29 Create this File.

original
>>> print("No Test")
No Test
"""
import functools
import time

__author__ = 'Liuyl'
from loongtian.nvwa.common.config import conf
from loongtian.nvwa.service import knowledge_srv, real_object_srv
from loongtian.nvwa.core.gdef import OID


class ObjectOperator(object):
    def __init__(self, obj):
        self._obj = obj

    def obj(self):
        return self._obj


class RelationOperator(ObjectOperator):
    def __init__(self, relation):
        super(RelationOperator, self).__init__(relation)

    def set(self, left, right, target_srv=None):
        return OriginalService.set_relation(self.obj(), left, right, target_srv)

    def get(self, left=None, right=None, target_srv=None):
        return OriginalService.get_relation(self.obj(), left, right, target_srv)

    def check(self, left, right, target_srv=None):
        return OriginalService.check_relation(self.obj(), left, right, target_srv)

    def find(self, left=None, right=None, target_srv=knowledge_srv):
        keys = []
        if left:
            keys = target_srv.base_deduce_backward(left.Id, self.obj().Id)
        elif right:
            keys = target_srv.base_deduce_forward(self.obj().Id, right.Id)
        return [target_srv.get(_k) for _k in keys]

    def find_one(self, left=None, right=None, target_srv=knowledge_srv):
        _r = self.find(left, right, target_srv)
        if len(_r) > 0:
            return _r[0]
        return None


class RelationToObjectOperator(ObjectOperator):
    def __init__(self, real_object, relation_op):
        super(RelationToObjectOperator, self).__init__(real_object)
        self.relation_op = relation_op

    def set(self, target_real_object, target_srv=None):
        return self.relation_op.set(target_real_object, self.obj(), target_srv)

    def get(self, target_real_object, target_srv=None):
        return self.relation_op.get(target_real_object, self.obj(), target_srv)

    def check(self, target_real_object, target_srv=None):
        return self.relation_op.check(target_real_object, self.obj(), target_srv)

    def find(self, target_srv=knowledge_srv):
        return self.relation_op.find(right=self.obj(), target_srv=target_srv)

    def find_one(self, target_srv=knowledge_srv):
        return self.relation_op.find_one(right=self.obj(), target_srv=target_srv)


class InheritFromRelationOperator(RelationOperator):
    def __init__(self):
        super(InheritFromRelationOperator, self).__init__(OriginalService.get_original_object(OID.InheritFrom))
        self.Word = RelationToObjectOperator(OriginalService.get_original_object(OID.Word), self)
        self.Number = RelationToObjectOperator(OriginalService.get_original_object(OID.Number), self)
        self.NotUnderstood = RelationToObjectOperator(OriginalService.get_original_object(OID.NotUnderstood), self)
        self.PlaceHolder = RelationToObjectOperator(OriginalService.get_original_object(OID.PlaceHolder), self)
        self.DefaultClass = RelationToObjectOperator(OriginalService.get_original_object(OID.DefaultClass), self)
        self.DefaultAction = RelationToObjectOperator(OriginalService.get_original_object(OID.DefaultAction), self)
        self.Quantifier = RelationToObjectOperator(OriginalService.get_original_object(OID.Quantifier), self)
        self.Time = RelationToObjectOperator(OriginalService.get_original_object(OID.Time), self)
        self.Collection = RelationToObjectOperator(OriginalService.get_original_object(OID.Collection), self)
        self.Action = RelationToObjectOperator(OriginalService.get_original_object(OID.Action), self)


class MoodIsRelationOperator(RelationOperator):
    def __init__(self):
        super(MoodIsRelationOperator, self).__init__(OriginalService.get_original_object(OID.Mood))
        self.Question = RelationToObjectOperator(OriginalService.get_original_object(OID.Question), self)
        self.Declarative = RelationToObjectOperator(OriginalService.get_original_object(OID.Declarative), self)


class EqualRelationOperator(RelationOperator):
    def __init__(self):
        super(EqualRelationOperator, self).__init__(None)

    def set(self, left, right, target_srv=None):
        pass

    def check(self, left, right, target_srv=None):
        return left.Id == right.Id


class OriginalService(object):
    original_object_dict = dict()

    @staticmethod
    def get_original_object(object_id):
        """
        建立一个原始对象的缓存,避免大量的重复查找
        :param object_id:
        :return:
        """
        if object_id not in OriginalService.original_object_dict:
            OriginalService.original_object_dict[object_id] = real_object_srv.get(object_id)
        return OriginalService.original_object_dict[object_id]

    def __init__(self):
        """
        原始标签的初始化及id字典的生成移入original服务的构造函数
        :return:
        """
        # if conf['storage'] == 'memory':
        object_list = OID.get_all_name()
        from loongtian.nvwa.common.storage.db.entity_repository import real_object_rep
        flag = conf['storage'] == 'memory' or not real_object_rep.is_initiated()
        for _s in object_list:
            if flag:
                _entity = real_object_srv.create(Display=OID.get_display(_s))
            else:
                _entity = real_object_srv.get_by_display(OID.get_display(_s))[0]
            OID.set_id_by_name(_s, _entity.Id)
            OriginalService.original_object_dict[_entity.Id] = _entity
        #elif conf['storage'] == 'riak':
        # else:
        #
        #     object_list = OID.get_all_name()
        #     for _s in object_list:
                #_entity = real_object_srv.create(Display=OID.get_display(_s))
                # _entity = real_object_srv.get_by_display(OID.get_display(_s))[0]
                # OID.set_id_by_name(_s, _entity.Id)
                # OriginalService.original_object_dict[_entity.Id] = _entity


        self.InnerSelf = ObjectOperator(self.get_original_object(OID.InnerSelf))
        self.Console = ObjectOperator(self.get_original_object(OID.Console))
        self.Declarative = ObjectOperator(self.get_original_object(OID.Declarative))
        self.Question = ObjectOperator(self.get_original_object(OID.Question))
        self.Anonymous = ObjectOperator(self.get_original_object(OID.Anonymous))
        self.DefaultClass = ObjectOperator(self.get_original_object(OID.DefaultClass))
        self.IsSelf = RelationOperator(self.get_original_object(OID.IsSelf))
        self.Equal = EqualRelationOperator()
        self.InheritFrom = InheritFromRelationOperator()
        self.UnknownBiRelation = RelationOperator(self.get_original_object(OID.UnknownBiRelation))
        self.FRestrict = RelationOperator(self.get_original_object(OID.FRestrict))
        self.BRestrict = RelationOperator(self.get_original_object(OID.BRestrict))
        self.QuantityIs = RelationOperator(self.get_original_object(OID.QuantityIs))
        self.BeModified = RelationOperator(self.get_original_object(OID.BeModified))
        self.ItemInf = RelationOperator(self.get_original_object(OID.ItemInf))
        self.CountIs = RelationOperator(self.get_original_object(OID.CountIs))
        self.QuantifierIs = RelationOperator(self.get_original_object(OID.QuantifierIs))
        self.Negate = RelationOperator(self.get_original_object(OID.Negate))
        self.Attribute = RelationOperator(self.get_original_object(OID.Attribute))
        self.Multi = RelationOperator(self.get_original_object(OID.Multi))
        self.CommonIs = RelationOperator(self.get_original_object(OID.CommonIs))
        self.HasAttribute = RelationOperator(self.get_original_object(OID.HasAttribute))
        self.SymbolInherit = RelationOperator(self.get_original_object(OID.SymbolInherit))
        self.Receive = RelationOperator(self.get_original_object(OID.Receive))
        self.Send = RelationOperator(self.get_original_object(OID.Send))
        self.UnderstoodAs = RelationOperator(self.get_original_object(OID.UnderstoodAs))
        self.TimeIs = RelationOperator(self.get_original_object(OID.TimeIs))
        self.SensorIs = RelationOperator(self.get_original_object(OID.SensorIs))
        self.ObserverIs = RelationOperator(self.get_original_object(OID.ObserverIs))
        self.MoodIs = MoodIsRelationOperator()
        self.Component = RelationOperator(self.get_original_object(OID.Component))
        self.SequenceIs = RelationOperator(self.get_original_object(OID.SequenceIs))
        self.StepIs = RelationOperator(self.get_original_object(OID.StepIs))
        self.Next = RelationOperator(self.get_original_object(OID.Next))
        self.And = RelationOperator(self.get_original_object(OID.And))
        self.Refer = RelationOperator(self.get_original_object(OID.Refer))
        self.CollectionContainItem = RelationOperator(self.get_original_object(OID.CollectionContainItem))
        self.FunctionBase = RelationOperator(self.get_original_object(OID.FunctionBase))
        self.FunctionName = RelationOperator(self.get_original_object(OID.FunctionName))

    # 关系建立/检查的根函数
    @staticmethod
    def set_relation(relation, left, right, target_srv):
        """
        根据关系对象将左右对象进行关联
        :param relation: 关系对象,即t型结构右上角的对象
        :param left: 关系左对象
        :param right: 关系右对象
        :return: 返回形成的关系
        """
        if not target_srv:
            target_srv = knowledge_srv
        if not left:
            return target_srv.create_l_structure(relation, right)
        elif not right:
            return target_srv.create_l_structure(left, relation)
        else:
            return target_srv.create_t_structure(left, relation, right)

    @staticmethod
    def get_relation(relation, left, right, target_srv):
        """
        根据关系对象将左右对象进行关联
        :param relation: 关系对象,即t型结构右上角的对象
        :param left: 关系左对象
        :param right: 关系右对象
        :return: 返回形成的关系
        """
        if not target_srv:
            target_srv = knowledge_srv
        if not left and not right:
            return relation
        elif not right:
            return target_srv.select_l_structure(left, relation)
        elif not left:
            return target_srv.select_l_structure(relation, right)
        else:
            return target_srv.select_t_structure(left, relation, right)

    @staticmethod
    def check_relation(relation, left, right, target_srv):
        """
        检查左右对象是否具有指定的关系
        :param relation: 关系对象,即t型结构右上角的对象
        :param left: 关系左对象
        :param right: 关系右对象
        :return: 返回True/False
        """
        if not target_srv:
            target_srv = knowledge_srv
        if not left:
            return target_srv.base_verify_forward(relation.Id, right.Id)
        elif not right:
            return target_srv.base_verify_forward(left.Id, relation.Id)
        else:
            return target_srv.base_verify_forward(left.Id, relation.Id, right.Id)

    def create_time_real_object(self):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        _t = real_object_srv.create(Display=current_time)
        self.InheritFrom.Time.set(_t)
        return _t

    def get_children(self, class_object):
        return [real_object_srv.get(_id) for _id in self.select_all_children(class_object.Id)]

    def relation_deep_find(self, relation, left=None, right=None, target_srv=knowledge_srv):
        _result = set(relation.find(left, right, target_srv))
        if len(_result) == 0:
            return []
        _list = _result
        _temp = set()
        while len(_list) != 0:
            for _p in _list:
                _temp.update(relation.find(_p if left else None, _p if right else None, target_srv))
            _list = _temp - _result
            _result.update(_list)
        return list(_result)

    def relation_deep_find_with_distance(self, relation, left=None, right=None, target_srv=knowledge_srv):
        _result = dict()
        _distance = 1
        _seed = relation.find(left, right, target_srv)
        for _o in _seed:
            _result[_o.Id] = (_o, _distance)
        _new_seed = list()
        while len(_seed) != 0:
            _distance += 1
            for _p in _seed:
                _new_seed.extend(relation.find(_p if left else None, _p if right else None, target_srv))
            for _n_p in _new_seed:
                _result[_n_p.Id] = (_n_p, _distance)
            _seed = _new_seed
            _new_seed = list()
        return _result.values()

    def select_direct_parent(self, child_object):
        """
        查找child_object的所有直接父类
        :param child_object:需要查找父类的实体
        :return:父类
        """
        return self.InheritFrom.find(left=child_object) + self.CommonIs.find(left=child_object)

    def select_all_parent(self, child_object):
        """
        child_object的所有父类
        :param child_object:需要查找父类的实体
        :return:父类列表
        """
        _result = set(self.select_direct_parent(child_object))
        if len(_result) == 0:
            return []
        _list = _result
        _temp = set()
        while len(_list) != 0:
            for _p in _list:
                _temp.update(self.select_direct_parent(_p))
            _list = _temp - _result
            _result.update(_list)
        return list(_result)

    def select_direct_children(self, parent_object):
        """
        查找parent_object的所有直接子类
        :param parent_object:需要查找子类的实体
        :return:子类列表
        """
        return self.InheritFrom.find(right=parent_object) + self.CommonIs.find(right=parent_object)

    def select_all_children(self, parent_object):
        """
        查找parent_object的所有子类
        :param parent_object:需要查找子类的实体
        :return:子类列表
        """
        _result = set(self.select_direct_children(parent_object))
        if len(_result) == 0:
            return []
        _list = _result
        _temp = set()
        while len(_list) != 0:
            for _c in _list:
                _temp.update(self.select_direct_children(_c))
            _list = _temp - _result
            _result.update(_list)
        return list(_result)

    def clone_real_object(self, real_object):
        _parent_object = self.InheritFrom.find(left=real_object)
        _new_real_object = real_object_srv.create(Display=real_object.Display + u'1')
        print(u'Create new object {}'.format(_new_real_object.Display))
        _old_start_list = knowledge_srv.base_select_start(real_object.Id)
        for _old_start in _old_start_list:
            if _old_start.End == self.IsSelf.obj().Id:
                continue
            elif _old_start.End == self.SymbolInherit.obj().Id and len(_parent_object) == 0:
                self.SymbolInherit.set(_new_real_object, real_object)
            else:
                _new_start = knowledge_srv.create_l_structure(_new_real_object, knowledge_srv.get(_old_start.End))
                _old_start_ref_list = knowledge_srv.base_select_start(_old_start.Id)
                for _old_start_ref in _old_start_ref_list:
                    knowledge_srv.create_l_structure(_new_start, knowledge_srv.get(_old_start_ref.End))
        if len(_parent_object) == 0:
            self.InheritFrom.set(_new_real_object, real_object)
        return _new_real_object


if __name__ == '__main__':
    import doctest

    doctest.testmod()