#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    real_object 
Author:   Liuyl 
DateTime: 2014/10/28 14:34 
UpdateLog:
1、Liuyl 2014/10/28 Create this File.

real_object
>>> print("No Test")
No Test
"""
from loongtian.nvwa.core.gdef import OID

__author__ = 'Liuyl'
from loongtian.nvwa.service.repository_service.base_rep_service import BaseRepService
from loongtian.nvwa.common.storage.db.entity_repository import real_object_rep
from loongtian.nvwa.entities.entity import RealObject
from loongtian.nvwa.service import knowledge_srv


class RealObjectService(BaseRepService):
    def __init__(self):
        super(RealObjectService, self).__init__(real_object_rep)

    def create(self, **kwargs):
        # 为每个object添加'is'的自引用
        _obj = super(RealObjectService, self).create(**kwargs)
        _l = knowledge_srv.create(Start=_obj.Id, End=OID.IsSelf, Display=u'({0}-{1})'.format(_obj.Display, u'自反是'))
        knowledge_srv.create(Start=_l.Id, End=_obj.Id, Display=u'({0}-{1})'.format(_l.Display, _obj.Display))
        return _obj

    def get_by_display(self,display):
        _obj = real_object_rep.get_by_index2i(display,'display_bin')
        return _obj

    @staticmethod
    def type_check(entity):
        return isinstance(entity, RealObject)


if __name__ == '__main__':
    import doctest

    doctest.testmod()