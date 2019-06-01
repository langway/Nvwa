#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Project:  nvwa
Title:    metadata 
Author:   liuyl 
DateTime: 2014/9/5 10.59 
UpdateLog:
1、liuyl 2014/9/5 Create this File.
1、liuyl 2014/12/5 创建meta时不再创建未知对象,但将新创建一个默认实意对象

metadata服务层
>>> print("No Test")
No Test
"""
__author__ = 'Liuyl'
from loongtian.nvwa.service.repository_service.base_rep_service import BaseRepService
from loongtian.nvwa.common.storage.db.entity_repository import metadata_rep
from loongtian.nvwa.service import real_object_srv, original_srv


class MetadataService(BaseRepService):
    def __init__(self):
        super(MetadataService, self).__init__(metadata_rep)

    def create(self, string_value, is_create_first_class=True):
        """
        创建metadata,将同时创建一个词,一个未知含义对象
        :param string_value:
        :return:
        """
        _m = self.generate(StringValue=string_value)
        _obj_word = real_object_srv.create(Metas=[_m.Id], Display=string_value + u'[W]')
        _obj_default_class = real_object_srv.create(Metas=[_m.Id], Display=string_value + u'[C]')
        if is_create_first_class:
            _obj_first_class = real_object_srv.create(Metas=[_m.Id], Display=string_value)
            original_srv.SymbolInherit.set(_obj_first_class, _obj_default_class)
        original_srv.InheritFrom.Word.set(_obj_word)
        original_srv.InheritFrom.DefaultClass.set(_obj_default_class)
        #_m.RealObjectList.update([_obj_word.Id, _obj_default_class.Id])
        _m.RealObjectList.extend([_obj_word.Id, _obj_default_class.Id])
        self.save(_m)
        return _m

    def get_word(self, meta):
        if meta:
            return [_o for _o in real_object_srv.gets(meta.RealObjectList) if original_srv.InheritFrom.Word.check(_o)][0]
        return None

    def get_default(self, meta):
        if meta:
            return [_o for _o in real_object_srv.gets(meta.RealObjectList) if not original_srv.InheritFrom.Word.check(_o)]
        return None

    def get_default_class(self, meta):
        if meta:
            return [_o for _o in real_object_srv.gets(meta.RealObjectList) if original_srv.InheritFrom.DefaultClass.check(_o)]
        return None

    def get_default_action(self, meta):
        if meta:
            return [_o for _o in real_object_srv.gets(meta.RealObjectList) if original_srv.InheritFrom.DefaultAction.check(_o)]
        return None

    def create_default_action(self, meta):
        _obj_default_action = real_object_srv.create(Metas=[meta.Id], Display=meta.StringValue + u'[A]')
        original_srv.InheritFrom.DefaultAction.set(_obj_default_action)
        meta.RealObjectList.append(_obj_default_action.Id)
        self.save(meta)
        return _obj_default_action

    def get_by_string_value(self, string_value):
        _m_list = self.rep.get_by_string_value(string_value)
        if len(_m_list) == 0:
            return None
        else:
            return _m_list[0]

    def link_real_object_metadata(self, string_value, real_object):
        _m = self.get_by_string_value(string_value)
        if not _m:
            _m = self.create(string_value)
        _m.RealObjectList.append(real_object.Id)
        self.save(_m)
        real_object.Metas.append(_m.Id)
        real_object_srv.save(real_object)

    def get_by_default_meaning_object(self, default_meaning_object):
        _id = list(default_meaning_object.Metas)[0]
        return self.get(_id)

    def get_default_by_string_value(self, string_value):
        _m = self.get_by_string_value(string_value)
        if _m:
            _k_list = real_object_srv.gets(_m.RealObjectList)
            for _k in _k_list:
                if original_srv.InheritFrom.DefaultClass.check(_k):
                    return _k
        return None

    def get_word_by_string_value(self, string_value):
        _m = self.get_by_string_value(string_value)
        if _m:
            _k_list = real_object_srv.gets(_m.RealObjectList)
            for _k in _k_list:
                if original_srv.InheritFrom.Word.check(_k):
                    return _k
        return None


if __name__ == '__main__':
    import doctest

    doctest.testmod()
