#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    t_model 
Author:   fengyh 
DateTime: 2014/9/3 11:41 
UpdateLog:
1、fengyh 2014/9/3 Create this File.
                    创建T字模型类及字符串方法
2、fengyh 2014/10/29 修改命名等。用途不变。

"""
import hashlib
from loongtian.nvwa.service import original_srv


class TModel(object):
    """
    T型结构，交互数据用。
     'TStart', 'TEnd', 'TEnd2'
    """
    __slots__ = ('TStart', 'TEnd', 'TEnd2')

    def __init__(self, **kwargs):
        self.TStart = kwargs.get('TStart', None)
        self.TEnd = kwargs.get('TEnd', None)
        self.TEnd2 = kwargs.get('TEnd2', None)

    def __eq__(self, other):
        """
        判断两个T型结构是否相同
        :param other:
        :return:
        """
        if original_srv.Equal.check(self.TStart, other.TStart) and original_srv.Equal.check(
                self.TEnd, other.TEnd) and original_srv.Equal.check(self.TEnd2, other.TEnd2):
            return True
        else:
            return False

    def __hash__(self):
        ids = self.TStart.Id+self.TEnd.Id+self.TEnd2.Id
        return ids.__hash__()


    def __str__(self):
        return '{' + self.TStart.__str__() + ',' + self.TEnd.__str__() + ',|' + self.TEnd2.__str__() + '}'

    pass

