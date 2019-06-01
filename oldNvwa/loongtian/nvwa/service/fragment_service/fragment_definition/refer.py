#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    refer 
Author:   Liuyl 
DateTime: 2015/6/15 16:03 
UpdateLog:
1、Liuyl 2015/6/15 Create this File.

refer
>>> print("No Test")
No Test
"""
from loongtian.nvwa.service.fragment_service.fragment_definition.fragment import Fragment

__author__ = 'Liuyl'


class ReferBuilder(object):
    ReferMark = u'指的是'
    StepMark = u'然后'
    AndMark = u'并且'

    def __init__(self, input_string):
        self.pre_refer_string = None
        self.post_refer_string = None
        self.step_string_list = []
        self.input_string = input_string
        self.input_split(input_string)
        self.move_result = {}

    def input_split(self, input_string):
        self.pre_refer_string, self.post_refer_string = input_string.split(self.ReferMark)
        for _step in self.post_refer_string.split(self.StepMark):
            self.step_string_list.append(_step.split(self.AndMark))

    def move(self, cut_func, move_func):
        self.move_result[self.pre_refer_string] = move_func(cut_func(self.pre_refer_string))
        for _step in self.step_string_list:
            for _item in _step:
                if _item not in self.move_result:
                    self.move_result[_item] = move_func(cut_func(_item))


class ReferFragment(Fragment):
    def __init__(self, ref, rep_srv):
        super(ReferFragment, self).__init__(ref, rep_srv)


if __name__ == '__main__':
    import doctest

    doctest.testmod()