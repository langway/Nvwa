#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    original_relation 
Created by zheng on 2014/12/11.
UpdateLog:

"""
from loongtian.nvwa.service import *
class Mapper(object):
    def __init__(self):
        service = original_srv
        self.mapper = {u'继承自':service.InheritFrom,
                       u'父对象':service.InheritFrom,
                       u'组件':service.Component}

    def getOriginalRelation(self,word):
        return self.mapper.get(word)
