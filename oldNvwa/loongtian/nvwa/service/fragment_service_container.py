#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    fragment_service_factory 
Author:   Liuyl 
DateTime: 2014/12/16 14:42 
UpdateLog:
1、Liuyl 2014/12/16 Create this File.

fragment_service_factory
>>> print("No Test")
No Test
"""
from loongtian.nvwa.service.fragment_service.action import ActionFragmentService
from loongtian.nvwa.service.fragment_service.fragment import FragmentService
from loongtian.nvwa.service.fragment_service.collection import CollectionFragmentService
from loongtian.nvwa.service.fragment_service.memory import MemoryFragmentService
from loongtian.nvwa.service.fragment_service.modified import ModifiedFragmentService
from loongtian.nvwa.service.fragment_service.refer import ReferFragmentService
from loongtian.nvwa.service.fragment_service.response import ResponseFragmentService

__author__ = 'Liuyl'


class FragmentServiceContainer(object):
    """
    片段服务的容器,由于开发阶段需要智能提示,故暂时使用属性来获取需要的服务实例
    请遵循调用规范
    from loongtian.nvwa.service import fsc
    fsc.collection.some_method()
    以便当需要依赖注入时可以替换为
    from loongtian.nvwa.service import fsc
    fsc['Collection'].some_method()
    """

    def __init__(self):
        self.__items = dict()
        self.fragment = FragmentService()
        self.__items[''] = self.fragment
        self.collection = CollectionFragmentService()
        self.__items['Collection'] = self.collection
        self.memory = MemoryFragmentService()
        self.__items['Memory'] = self.memory
        self.modified = ModifiedFragmentService()
        self.__items['Modified'] = self.modified
        self.response = ResponseFragmentService()
        self.__items['Response'] = self.response
        self.action = ActionFragmentService()
        self.__items['Action'] = self.action
        self.refer = ReferFragmentService()
        self.__items['Refer'] = self.refer
    def __getitem__(self, item):
        return self.__items.get(item)


if __name__ == '__main__':
    import doctest

    doctest.testmod()