#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    base_service 
Author:   Liuyl 
DateTime: 2014/10/28 14:54 
UpdateLog:
1、Liuyl 2014/10/28 Create this File.

base_service
>>> print("No Test")
No Test
"""
__author__ = 'Liuyl'


class BaseRepService(object):
    def __init__(self, rep):
        self.rep = rep

    def save(self, obj):
        self.rep.save(obj)

    def get_keys(self):
        return self.rep.get_keys()

    def get(self, key):
        return self.rep.get(key)

    def gets(self, keys):
        return self.rep.gets(keys)

    def clear(self):
        self.rep.clear()

    def delete(self,obj):
        self.rep.delete(obj)

    def delete_by_key(self,key):
        self.rep.delete_by_key(key)

    def generate(self, **kwargs):
        return self.rep.generate(**kwargs)

    def create(self, **kwargs):
        _entity = self.rep.generate(**kwargs)
        self.rep.save(_entity)
        return _entity

    def get_matches(self):
        '''
        自然遗忘的key列表
        :return:
        '''
        return self.rep.get_matches()


if __name__ == '__main__':
    import doctest

    doctest.testmod()