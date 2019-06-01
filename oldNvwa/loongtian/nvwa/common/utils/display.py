#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    display 
Author:   Liuyl 
DateTime: 2014/11/21 15:48 
UpdateLog:
1、Liuyl 2014/11/21 Create this File.

display
>>> print("No Test")
No Test
"""
__author__ = 'Liuyl'


class DisplayHelper(object):
    count = 0

    def __init__(self):
        pass

    @staticmethod
    def get(entity, target_srv=None):
        import loongtian.nvwa.entities.entity as en
        from loongtian.nvwa.service import knowledge_srv, real_object_srv

        def deep_get(cur_id, target_srv):
            DisplayHelper.count += 1
            _obj = real_object_srv.get(cur_id)
            if _obj:
                return _obj.Display
            _cur_entity = target_srv.get(cur_id)
            if _cur_entity:
                return u'({0}-{1})'.format(deep_get(_cur_entity.Start, target_srv),
                                           deep_get(_cur_entity.End, target_srv))

        if isinstance(entity, en.RealObject):
            return entity.Display
        if target_srv:
            _r = deep_get(entity.Id, target_srv)
        elif isinstance(entity, en.Knowledge):
            _r = deep_get(entity.Id, knowledge_srv)
        elif isinstance(entity, en.Memory):
            _r = deep_get(entity.Id, memory_srv)
        elif isinstance(entity, en.ActionDefine):
            from loongtian.nvwa.service import action_define_srv

            _r = deep_get(entity.Id, action_define_srv)
        else:
            _r = getattr(entity, 'Display', u'')
        return _r


if __name__ == '__main__':
    import doctest

    doctest.testmod()