#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    modified 
Author:   Liuyl 
DateTime: 2015/2/9 9:31 
UpdateLog:
1、Liuyl 2015/2/9 Create this File.

modified
>>> print("No Test")
No Test
"""
from loongtian.nvwa.service.fragment_service.fragment_definition.fragment import Fragment

__author__ = 'Liuyl'


class ModifiedFragment(Fragment):
    def __init__(self, ref, rep_srv):
        super(ModifiedFragment, self).__init__(ref, rep_srv)
        self.__modified_frag = self

    @property
    def modified_frag(self):
        return self.__modified_frag

    @modified_frag.setter
    def modified_frag(self, value):
        if not self._rep_srv.get(value.ref.Id):
            value.save_to_target_rep_srv(self._rep_srv)
        self.__modified_frag = value


if __name__ == '__main__':
    import doctest

    doctest.testmod()