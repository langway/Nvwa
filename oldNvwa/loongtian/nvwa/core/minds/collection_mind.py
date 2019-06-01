#!/usr/bin/env python
# coding: utf-8
"""
集合关键字管理器

Project:  nvwa
Title:    collection 
Author:   fengyh 
DateTime: 2015/7/21 14:00 
UpdateLog:
1、fengyh 2015/7/21 Create this File.
"""
import jieba
from loongtian.nvwa.common.threadpool.runnable import Runnable
from loongtian.nvwa.core.gdef import GlobalDefine
from loongtian.nvwa.core.maincenter import evaluator_center
from loongtian.nvwa.core.maincenter.evaluator.evaluator import EvaluateResult, State
from loongtian.nvwa.core.maincenter.planner.plan import planer_center
from loongtian.nvwa.entities import CommandJobTypeEnum
from loongtian.nvwa.entities.collection import Collection, CollectionUtil
from loongtian.nvwa.entities.sentence import Sentence
from loongtian.nvwa.service import metadata_srv, original_srv, fragment_srv, fsc, real_object_srv

_rep_srv = fragment_srv.get_new_knowledge_for_fragment_service()


def create_collection(name,item=None):
    if item is None:
        c = Collection(name)
    else:
        metadata_srv.create(item)
        item_object = original_srv.SymbolInherit.find(right=metadata_srv.get_default_by_string_value(item))[0]
        c = Collection(name,item_object)
    print 'create collection '+name
    knowledge_i_known = u'创建'+name+u'成功。'
    return knowledge_i_known

def count_collection(name,item=None):
    c_object, items = CollectionUtil.find_collection_by_collection_name(name)
    knowledge_i_known = u''+name+u'有'+str(items.__len__())+u'个元素。'
    return knowledge_i_known

def find_collection(name,item=''):
    c_object, items = CollectionUtil.find_collection_by_collection_name(name)
    knowledge_i_known = ",".join([item.Display for item in items])
    # knowledge_i_known = '找到'+name+u'。包含元素['+",".join([item.Display for item in items])+']。'
    return knowledge_i_known

def collection_add(name,item=None):
    c_object,items = CollectionUtil.find_collection_by_collection_name(name)
    if metadata_srv.get_default_by_string_value(item) is None:
        metadata_srv.create(item)
    item_object = original_srv.SymbolInherit.find(right=metadata_srv.get_default_by_string_value(item))[0]
    CollectionUtil.append(c_object,item_object)
    knowledge_i_known = u'添加成功。'
    return knowledge_i_known

def collection_delete(name,item=None):# todo 未实现
    c_object,items = CollectionUtil.find_collection_by_collection_name(name)
    item_object = original_srv.SymbolInherit.find(right=metadata_srv.get_default_by_string_value(item))[0]
    CollectionUtil.append(c_object,item_object)
    pass

def collection_contain(name,item=None):
    c_object,items = CollectionUtil.find_collection_by_collection_name(name)
    item_object = original_srv.SymbolInherit.find(right=metadata_srv.get_default_by_string_value(item))[0]
    if CollectionUtil.contain_item(c_object,item_object):
        knowledge_i_known = name+u'包含'+item
    else:
        knowledge_i_known = name+u'不包含'+item
    return knowledge_i_known


def collection_find(name,item=None):
    c_object,items = CollectionUtil.find_collection_by_collection_name(name)
    return items

def collection_intersection(name,name2):
    c_object,items = CollectionUtil.find_collection_by_collection_name(name)
    c_object2,items2 = CollectionUtil.find_collection_by_collection_name(name2)
    int_list = CollectionUtil.intersection(c_object,c_object2)
    knowledge_i_known = ",".join([item.Display for item in int_list])
    return knowledge_i_known


def collection_union(name,name2):
    c_object,items = CollectionUtil.find_collection_by_collection_name(name)
    c_object2,items2 = CollectionUtil.find_collection_by_collection_name(name2)
    int_list = CollectionUtil.union(c_object,c_object2)
    knowledge_i_known = ",".join([item.Display for item in int_list])
    return knowledge_i_known
    pass

def collection_different(name,name2):
    c_object,items = CollectionUtil.find_collection_by_collection_name(name)
    c_object2,items2 = CollectionUtil.find_collection_by_collection_name(name2)
    diff_list = CollectionUtil.difference(c_object,c_object2)
    knowledge_i_known = ",".join([item.Display for item in diff_list])
    return knowledge_i_known

def collection_equal(name,name2):
    c_object,items = CollectionUtil.find_collection_by_collection_name(name)
    c_object2,items2 = CollectionUtil.find_collection_by_collection_name(name2)
    if CollectionUtil.difference(c_object,c_object2).__len__() == 0:
        return u'相等'
    else:
        return u'不相等'


collection_command = {u'创建集合':create_collection,
                      u'计数集合':count_collection,
                      u'查找集合':find_collection,
                      u'集合添加':collection_add,
                      u'集合删除':collection_delete,
                      u'集合包含':collection_contain,
                      u'集合查询':collection_find,
                      u'交集':collection_intersection,
                      u'并集':collection_union,
                      u'补集':collection_union,
                      u'差集':collection_union,
                      u'相等':collection_equal,
}


class CollectionCommandSplit(object):
    collection_operator_list = collection_command.keys()

    def __init__(self, input_string):
        self.current_operator = None
        self.first_param = None
        self.second_param = None
        self.current_input_string = input_string

    def input_split(self):
        for opt in self.collection_operator_list:
            if self.current_input_string.startswith(opt):
                self.current_operator = opt
                str_without_operator = ",".join(jieba.cut(self.current_input_string[self.current_input_string.find(self.current_operator)+self.current_operator.__len__():]))
                params = str_without_operator.split(",")
                if params.__len__() == 1:
                    params.append(None)
                self.first_param, self.second_param = params[0],params[1]
                return True
            elif self.current_input_string.find(opt) != -1:
                self.current_operator = opt
                self.first_param, self.second_param = self.current_input_string.split(self.current_operator)
                return True
        return False



class CollectionMind(Runnable):
    def __init__(self):
        super(CollectionMind, self).__init__()
        self._name = "Collection"
        self.inputMsg = GlobalDefine().collection_input_queue
        self.outMsg = GlobalDefine().console_output_queue
        pass

    def _execute(self):
        while True:
            if not self.inputMsg.empty():
                _input, _client_address = self.inputMsg.get()
                _rb = CollectionCommandSplit(_input)
                _rb.input_split()
                if _rb.current_operator is not None:
                    rt_str = collection_command.get(_rb.current_operator)(_rb.first_param,_rb.second_param)
                    rt_frag = real_object_srv.create(Display = rt_str)

                    _rf = fsc.fragment.generate(rt_frag,_rep_srv)

                _s = Sentence(['非常好','!'])
                # _es = evaluator_center.execute([[_rf]*2], _s)
                _es = EvaluateResult(State.NotExist, 0, left_frag=_rf, right_frag=_rf, frag=_rf)
                _planed_results = planer_center.execute(_es, _s)
                # 执行
                for item in _planed_results:
                    if item.type == CommandJobTypeEnum.Output:
                        item.t_struct = (item.t_struct, _client_address)
                    GlobalDefine().command_msg.put(item)

            if not self.state():
                break


