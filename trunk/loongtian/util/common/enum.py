#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'CoolSnow'

class Enum(object):
    """
    枚举基类
    :rawParam
    :attribute
    """
    @classmethod
    def getName(cls, value):
        """
        获得枚举名
        :rawParam value: 枚举值
        :return: 枚举名，类型为字符串。
        """
        enum = dict(vars(cls))
        for item in enum.items():
            if (item[1] == value):
                return item[0]
        return None

    def __setattr__(self, key, value):
        if __debug__ :
            raise ValueError('You can not set the attribute to a Enum!')
        pass