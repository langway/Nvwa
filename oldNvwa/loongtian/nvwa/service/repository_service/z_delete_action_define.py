#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    action_define 
Author:   Liuyl 
DateTime: 2014/12/19 15:04 
UpdateLog:
1、Liuyl 2014/12/19 Create this File.

action_define
>>> print("No Test")
No Test
"""
from loongtian.nvwa.common.storage.db.entity_repository import action_define_rep
from loongtian.nvwa.service import real_object_srv, original_srv
from loongtian.nvwa.service.repository_service.base_knowledge_service import BaseKnowledgeService

__author__ = 'Liuyl'


class ActionDefineService(BaseKnowledgeService):
    def __init__(self):
        super(ActionDefineService, self).__init__(action_define_rep)

    @staticmethod
    def create_placeholder(real_object, mark):
        _p = real_object_srv.create(Display=u"Act({0})的占位符{1}".format(real_object.Display, mark))
        original_srv.InheritFrom.PlaceHolder.set(_p)
        return _p


if __name__ == '__main__':
    import doctest

    doctest.testmod()