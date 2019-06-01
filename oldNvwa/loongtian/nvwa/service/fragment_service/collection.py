#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    collection_fragment 
Author:   Liuyl 
DateTime: 2014/12/16 15:01 
UpdateLog:
1、Liuyl 2014/12/16 Create this File.

collection_fragment
>>> print("No Test")
No Test
"""
from loongtian.nvwa.service import *
from loongtian.nvwa.service.fragment_service.fragment import FragmentService
from loongtian.nvwa.entities.enum import enum

__author__ = 'Liuyl'


class CollectionFragmentEnum(object):
    """
    集合结构类型。
    liuyl 2014-12-16
    """

    def __init__(self):
        enum(CollectionFragmentEnum, 'ItemInf=0,Count=1,Quantifier=2',
             sep=',')
        pass


CollectionFragmentEnum()


class CollectionFragmentService(FragmentService):
    def __init__(self):
        super(CollectionFragmentService, self).__init__()
        pass

    def check(self, frag):
        return original_srv.InheritFrom.Collection.check(frag.ref, target_srv=frag.rep_srv)

    def assemble(self, target_srv, **kwargs):
        """
        组装
        :param target_srv:
        :param kwargs: deep_start,end
        :return:
        """
        item_inf = kwargs.get('item_inf', None)
        count = kwargs.get('count', None)
        quantifier = kwargs.get('quantifier', None)
        _new_collection = real_object_srv.create(
            Display=u'{0}{1}{2}'.format(count.Display, quantifier.Display, item_inf.Display))
        original_srv.InheritFrom.Collection.set(_new_collection, knowledge_srv)
        original_srv.ItemInf.set(_new_collection, item_inf, knowledge_srv)
        original_srv.CountIs.set(_new_collection, count, knowledge_srv)
        original_srv.QuantifierIs.set(_new_collection, quantifier, knowledge_srv)
        return self.generate(_new_collection, rep_srv=target_srv)

    def unassemble(self, frag):
        _result = dict()
        _result[CollectionFragmentEnum.ItemInf] = original_srv.ItemInf.find_one(left=frag.ref)
        _result[CollectionFragmentEnum.Count] = original_srv.CountIs.find_one(left=frag.ref)
        _result[CollectionFragmentEnum.Quantifier] = original_srv.QuantifierIs.find_one(left=frag.ref)
        return _result


if __name__ == '__main__':
    import doctest

    doctest.testmod()