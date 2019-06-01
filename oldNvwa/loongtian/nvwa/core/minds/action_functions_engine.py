#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    action_functions 
Author:   fengyh 
DateTime: 2015/9/8 15:20 
UpdateLog:
1、fengyh 2015/9/8 Create this File.

"""
import jieba
from loongtian.nvwa.entities.collection import CollectionUtil, Collection
from loongtian.nvwa.service import metadata_srv, original_srv, knowledge_srv

# 此文件留存函数引擎所需的所有函数，函数功能在此增加或者删改。
# todo 未来所有函数会替换成Action做活处理


def create_collection(name,item=None):
    """
    创建集合功能，传入集合名称
    :param name:
    :param item:
    :return:
    """
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
    """
    统计集合元素个数
    :param name:
    :param item:
    :return:
    """
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

def prepare_strong_relation(name,name2):
    """
    逗号函数处理功能在此。逗号包括中文逗号和英文逗号都支持。
    此函数的操作在外部有处理，内部处理内容待定。考虑放外部的特殊处理操作是否可以放函数内。
    fengyh 2015-10-13
    :param name:
    :param name2:
    :return:
    """
    knowledge_srv.generate_l_structure()
    pass

# 此处为函数字典，这里定义函数关键字和对应代码中的函数名称。
# 这一段代码现在是为了初始化数据用，将来这些数据保存到数据库以后，代码中就不需要写了。
# todo 函数处理说明：1、暂时只处理参数为1个和2个的情况，未来考虑支持不限量参数；
# todo 函数处理说明：2、参数的分隔是去掉函数关键词以后剩余文字的分词。此处会依赖分词效果。
#
function_dic = {u'创建集合': 'create_collection',
          u'计数集合':'count_collection',
          u'查找集合':'find_collection',
          u'集合添加':'collection_add',
          u'集合删除':'collection_delete',
          u'集合包含':'collection_contain',
          u'集合查询':'collection_find',
          u'交集':'collection_intersection',
          u'并集':'collection_union',
          u'补集':'collection_union',
          u'差集':'collection_different',
          u'相等':'collection_equal',
          u',':'prepare_strong_relation',
          u'，':'prepare_strong_relation',
}


class FunctionActionSplit(object):
    """
    函数作为Action处理的辅助函数，此功能做预处理，识别函数Action并提取函数和参数。
    """
    def __init__(self, input_string,function_dic):
        self.current_operator = None
        self.first_param = None
        self.second_param = None
        self.current_input_string = input_string
        self.collection_operator_list = function_dic.keys()

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

