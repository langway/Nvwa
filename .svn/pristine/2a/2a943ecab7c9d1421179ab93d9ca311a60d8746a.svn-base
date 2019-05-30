#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    response 
Author:   Liuyl 
DateTime: 2015/1/13 15:13 
UpdateLog:
1、Liuyl 2015/1/13 Create this File.

response
>>> print("No Test")
No Test
"""
from loongtian.nvwa.service import original_srv
from loongtian.nvwa.service.fragment_service.fragment_definition.fragment import Fragment
from loongtian.nvwa.entities.enum import SentenceTypeEnum

__author__ = 'Liuyl'


class ResponseFragment(Fragment):
    def __init__(self, ref, rep_srv):
        super(ResponseFragment, self).__init__(ref, rep_srv)
        self.sentence_type = SentenceTypeEnum.NotAsk
        self.state = "Match"
        self.conflict = []
        self.input_word = None
        self.input_meaning = None
        self.output_word = []
        self.output_meaning = []


if __name__ == '__main__':
    import doctest

    doctest.testmod()