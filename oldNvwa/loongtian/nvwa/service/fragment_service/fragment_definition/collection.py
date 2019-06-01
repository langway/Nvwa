#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    collection 
Author:   Liuyl 
DateTime: 2014/12/18 10:18 
UpdateLog:
1、Liuyl 2014/12/18 Create this File.

collection
>>> print("No Test")
No Test
"""
from loongtian.nvwa.service import original_srv
from loongtian.nvwa.service.fragment_service.fragment_definition.fragment import Fragment

__author__ = 'Liuyl'


class CollectionFragment(Fragment):
    def __init__(self, ref, rep_srv):
        super(CollectionFragment, self).__init__(ref, rep_srv)
        self._extra_ref.append(
            self.rep_srv.select_t_structure(
                self.ref, original_srv.ItemInf.obj(),
                original_srv.ItemInf.find_one(left=self.ref, target_srv=self.rep_srv)))
        self._extra_ref.append(
            self.rep_srv.select_t_structure(
                self.ref, original_srv.CountIs.obj(),
                original_srv.CountIs.find_one(left=self.ref, target_srv=self.rep_srv)))
        self._extra_ref.append(
            self.rep_srv.select_t_structure(
                self.ref, original_srv.QuantifierIs.obj(),
                original_srv.QuantifierIs.find_one(left=self.ref, target_srv=self.rep_srv)))


if __name__ == '__main__':
    import doctest

    doctest.testmod()