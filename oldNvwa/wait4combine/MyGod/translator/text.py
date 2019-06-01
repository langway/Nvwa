#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
新建python文件
>>> print("No Test")
No Test
"""
__author__ = 'Liuyl'
from baseTranslator import BaseTranslator as BaseTranslator
import centre.language


class Translator(BaseTranslator):
    def __init__(self):
        super(Translator, self).__init__()
        self._centres["lan"] = centre.language.GetCentre()
        pass

    def decode(self, input):
        return self._centres["lan"].decode(input)

    def encode(self, output):
        return self._centres["lan"].encode(output)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
