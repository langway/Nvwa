#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
翻译器基类
翻译器负责调用大脑的各个处理中枢完成外界输入向知识表示的转换及知识表示向外界输出的转换
>>> print("No Test")
No Test
"""
__author__ = 'Liuyl'


class BaseTranslator(object):
    def __init__(self):
        self._centres = {}
        pass

    def decode(self, information):
        pass

    def encode(self, knowledge):
        pass


if __name__ == '__main__':
    import doctest

    doctest.testmod()
