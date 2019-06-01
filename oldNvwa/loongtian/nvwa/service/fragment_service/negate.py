#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    negate 
Author:   Liuyl 
DateTime: 2014/12/22 10:30 
UpdateLog:
1、Liuyl 2014/12/22 Create this File.

negate
>>> print("No Test")
No Test
"""
from loongtian.nvwa.service import *
from loongtian.nvwa.service.fragment_service.fragment import FragmentService

__author__ = 'Liuyl'


class NegateFragmentService(FragmentService):
    def __init__(self):
        super(NegateFragmentService, self).__init__()
        pass

    def check(self, frag):
        return original_srv.Equal.check(original_srv.Negate.obj(), frag.start, target_srv=frag.rep_srv)

    def assemble(self, target_srv, *args, **kwargs):
        """
        组装
        :param target_srv:
        :param kwargs: deep_start,end
        :return:
        """
        _new_ref = original_srv.Negate.set(left=None, right=args[0], target_srv=target_srv)
        return self.generate(_new_ref, rep_srv=target_srv)

    def unassemble(self, frag):
        _result = []
        if self.check(frag):
            _result.append(frag.end)
        return _result


if __name__ == '__main__':
    import doctest

    doctest.testmod()