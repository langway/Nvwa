#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    nltk_test 
Author:   Liuyl 
DateTime: 2014/10/15 10:27 
UpdateLog:
1、Liuyl 2014/10/15 Create this File.

nltk_test
>>> print("No Test")
No Test
"""
__author__ = 'Liuyl'
import nltk

if __name__ == '__main__':
    tlp = nltk.LogicParser(type_check=True)
    parsed = tlp.parse('walk(angus)')
    print(parsed.argument)
    print(parsed.argument.type)
    print(parsed.function)
    print(parsed.function.type)
    sig = {'walk': '<e, t>'}
    parsed = tlp.parse('walk(angus)', sig)
    print(parsed.function.type)