#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'CoolSnow'

class Enum(object):
    """
    枚举基类
    :rawParam
    :attribute
    """

    _value_name_dict = {}
    _name_value_dict = {}
    _value_types=[int,str] # 限定枚举值的类型，默认为整型、字符串类型。

    def __init__(self):
        for attr_name in dir(self):
            if attr_name.startswith('_'):
                continue
            attr_value = getattr(self, attr_name)
            if type(attr_value) in self._value_types:
                self._value_name_dict[attr_value] = attr_name
                self._name_value_dict[attr_name] = attr_value

    @classmethod
    def getName(cls, value):
        """
        获得枚举名
        :rawParam value: 枚举值
        :return: 枚举名，类型为字符串。
        """
        # enum = dict(vars(cls))
        # for item in enum.items():
        #     if (item[1] == value):
        #         return item[0]
        # return None
        name = cls._value_name_dict.get(value)
        if name is None:
            return "UNKNOWN"
        return name

    @classmethod
    def getValue(cls,name):

        value = cls._name_value_dict.get(name)
        return value

    def __setattr__(self, key, value):
        if __debug__ :
            raise ValueError('You can not set the attribute to a Enum!')
        pass