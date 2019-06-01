#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    memory_fragment 
Author:   Liuyl 
DateTime: 2014/12/16 15:25 
UpdateLog:
1、Liuyl 2014/12/16 Create this File.

memory_fragment
>>> print("No Test")
No Test
"""
from loongtian.nvwa.service import original_srv, real_object_srv
from loongtian.nvwa.service.fragment_service.fragment import FragmentService
from loongtian.nvwa.entities.enum import enum

__author__ = 'Liuyl'


class MemoryFragmentEnum(object):
    """
    记忆结构类型。
    liuyl 2014-12-9
    """

    def __init__(self):
        enum(MemoryFragmentEnum, 'Time=2,Understand=5',
             sep=',')
        pass


MemoryFragmentEnum()


class MemoryFragmentService(FragmentService):
    def __init__(self):
        super(MemoryFragmentService, self).__init__()

    @staticmethod
    def check(frag, rep_srv):
        if hasattr(frag.ref, "Start"):
            _s = rep_srv.get(frag.ref.Start)
            if hasattr(_s, "End"):
                if original_srv.Equal.check(original_srv.TimeIs.obj(), real_object_srv.get(_s.End)):
                    return True
        return False

    def assemble(self, target_srv, *args, **kwargs):
        """
        组装
        :param target_srv:
        :param kwargs: recordTime,understand
        :return:
        """
        time = kwargs.get('recordTime', None)
        understand = kwargs.get('understand', None)
        if time:
            _i_cur = original_srv.TimeIs.set(understand, time, target_srv)
        else:
            _i_cur = understand
        return self.generate(_i_cur, rep_srv=target_srv)

    def unassemble(self, frag):
        def skin_one_time(cur, target):
            _deep_end_for_start = self.get_deep_end(cur)
            if _deep_end_for_start and original_srv.Equal.check(_deep_end_for_start.ref, target):
                return self.get_end(cur), self.get_deep_start(cur)
            return None, cur

        _result = dict()
        _cur = frag
        _result[MemoryFragmentEnum.Time], _result[MemoryFragmentEnum.Understand] \
            = skin_one_time(_cur, original_srv.TimeIs.obj())

        return _result


if __name__ == '__main__':
    import doctest

    doctest.testmod()