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
from loongtian.nvwa.service import original_srv
from loongtian.nvwa.service.fragment_service.fragment_definition.fragment import Fragment

__author__ = 'Liuyl'


class NegateFragment(Fragment):
    def __init__(self, ref, rep_srv):
        super(NegateFragment, self).__init__(ref, rep_srv)
        if original_srv.Negate.check(left=None, right=self.ref, target_srv=rep_srv):
            _ref = original_srv.Negate.get(left=None, right=self.ref, target_srv=rep_srv)
            self.rep_srv.save(_ref)
            self._ref = _ref


if __name__ == '__main__':
    import doctest

    doctest.testmod()