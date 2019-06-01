#!/usr/bin/env python
# coding: utf-8
"""
数据仓库基类模块

Project:  nvwa
Title:    repository 
Author:   Liuyl 
DateTime: 2014/9/5 14:03 
UpdateLog:
1、Liuyl 2014/9/5 Create this File.

repository
>>> class T(object):
...     def __init__(self, tid, value):
...         self.Id = tid
...         self.Value = value
>>> res = Repository()
>>> res.index2i_dict["value_index2i"] = 'Value'
>>> res.save(T(1, 2))
>>> print(res.gets_key_by_index2i([2], "value_index2i"))
{2: [1]}
"""
__author__ = 'Liuyl'
import uuid
from loongtian.nvwa.entities.entity import RealObject, Metadata

class Repository(object):
    '''
    数据仓库
    
    data   id为key 数据仓库中的数据
    starts start为key  entity列表为value的字典
    ends   end为key  entity列表为value的字典
    strings  汉字为key  entity列表为value的字典
    index2i_dict  二级索引字典
    Type 
    other 临时保存初始化标记
    '''
    def __init__(self, entity_name, entity_type, *args, **kwargs):
        self.data = {}
        self.starts = {}
        self.ends = {}
        self.strings = {}
        self.index2i_dict = {}
        self.Type = entity_type
        self.other = {}  # 临时保存初始化标记

    def generate(self, **kwargs):
        kwargs['Id'] = kwargs.get('Id', uuid.uuid1())
        return self.Type(**kwargs)

    def is_initiated(self):
        return self.other.__contains__('0000000000')

    def initial(self):
        self.other['0000000000'] = '0'

    def save(self, obj):
        self.data[obj.Id] = obj
        if isinstance(obj, RealObject):
            return
        if isinstance(obj, Metadata):
            if self.strings.has_key(obj.StringValue):
                self.strings[obj.StringValue].add(obj)
            else:
                self.strings[obj.StringValue] = set([obj])
            return
        if self.starts.has_key(obj.Start):
            self.starts[obj.Start].add(obj)
        else:
            self.starts[obj.Start] = set([obj])

        if self.ends.has_key(obj.End):
            self.ends[obj.End].add(obj)
        else:
            self.ends[obj.End] = set([obj])

    def delete(self, obj):
        self.delete_by_key(obj.Id)

    def delete_by_key(self, key):

        start = self.get(key)
        end = self.get(key)
        if start:
            self.starts[start.Id].remove(start)
        if end:
            self.ends[end.Id].remove(end)

        del (self.data[key])

    def get_keys(self):
        return self.data.keys()

    def get(self, key):
        return self.data.get(key, None)

    def gets(self, keys):
        return [self.get(key) for key in keys]

    def clear(self):
        self.data.clear()
        self.starts.clear()
        self.ends.clear()

    def get_by_index2i(self, value, idx):
        """
        通过二级索引查询对象列表
        :param idx:二级索引名称
        :param value: 值
        :return:对象列表
        """
        return [self.get(key) for key in self.get_key_by_index2i(value, idx)]

    def get_key_by_index2i(self, value, idx):
        """
        通过二级索引查询key列表
        :param idx:二级索引名称
        :param value: 值
        :return:key列表
        """
        index2i = self.index2i_dict.get(idx, None)
        if index2i is None:
            return []
        # return [entity.Id for entity in self.data.itervalues() if getattr(entity, index2i) == value]
        if index2i == 'Start':
            return [item.Id for item in self.starts.get(value, [])]
        if index2i == 'End':
            return [item.Id for item in self.ends.get(value, [])]
        # return [self.data[_key].Id for _key in self.data.keys() if getattr(self.data[_key], index2i) == value]
        if index2i == 'StringValue':
            return [item.Id for item in self.strings.get(value, [])]

    def gets_by_index2i(self, values, idx):
        """
        通过多个二级索引查询值对象
        :param idx:二级索引名称
        :param values: 值列表
        :return:返回以每个值为key,对象列表为value的字典
        """
        result = {}
        for value in set(values):
            result[value] = self.get_by_index2i(value, idx)
        return result

    def gets_key_by_index2i(self, values, idx):
        """
        通过多个二级索引查询key
        :param idx:二级索引名称
        :param values: 值列表
        :return:返回以每个值为key,对象的key列表为value的字典
        """
        result = {}
        for value in set(values):
            result[value] = self.get_key_by_index2i(value, idx)
        return result

    def get_matches(self):
        return self.get_keys()


if __name__ == '__main__':
    import doctest

    doctest.testmod()
