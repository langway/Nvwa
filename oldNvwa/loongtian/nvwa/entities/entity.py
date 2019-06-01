#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" 女娲实体模块
"""
import json
import datetime
from loongtian.nvwa.common.utils.display import DisplayHelper
from loongtian.nvwa.entities.const_values import ConstValues

class Entity(object):
    ''' 实体基类
    '''
    __slots__ = ()

    def __init__(self):
        pass

    def to_json(self):
        ''' 将实体转换成JSON
        :return JSON字符串
        '''
        _dict = {item: getattr(self, item) for item in self.__slots__}
        _a = _dict.get('Metas',None)
        if  _a != None and len(_a)!=0:
            pass
        return json.dumps(_dict)

    @property
    def Display(self):
        ''' 获得Display属性值
        :return 返回Display属性值
        '''
        return DisplayHelper.get(self)

    def __str__(self):
        return self.Display


class RealObject(Entity):
    """ RealObject
    :attributes 
        Id 唯一标识，要考虑上亿级数据的不重复。
        Metas 关联到Metadata表的Id列表。
        Threshold 阈值。本条知识的访问限制值。反思自学过程中，阈值会不停地刷新。阈值降低的更加牢固，阈值升高的逐渐等同断开。
        ThresholdTime 阈值计算和更新时间。（梁：2014-8-28）
        Display 旁路调试显示文字用。
    """
    __slots__ = ('Id', 'Metas', 'Threshold', 'ThresholdTime', 'Display')

    def __init__(self, **kwargs):
        super(RealObject, self).__init__()
        self.Id = str(kwargs.get('Id', None))
        self.Metas = kwargs.get('Metas', [])
        self.Threshold = kwargs.get('Threshold', ConstValues.threshold_initial_value)
        self.ThresholdTime = kwargs.get('ThresholdTime', datetime.datetime.now().__str__())
        self.Display = kwargs.get('Display', '')

    def __eq__(self, other):
        return self.Id == other.Id

    def __hash__(self):
        ids = self.Id
        return ids.__hash__()

# a=RealObject()
#
# a.abc=123
#
# print a.abc


class Metadata(Entity):
    """ MetaData
    :attributes 
        Id 唯一标识，要考虑上亿级数据的不重复。
        StringValue Meta文字信息。例如“牛”，“苹果”，“简爱”等。
        RealObjectList 以List形式保存Metadata对外关联的Id列表。可能是一个或多个Realobject的Id，可以代表Action，Modifier等。
            其中必然会有一个Id代表“未知含义”。将未理解的词创建“未知含义对象”后关联此Id，为了能保存这种未知的信息便于后续推导和理解。
    """
    __slots__ = ('Id', 'StringValue', 'RealObjectList')

    def __init__(self, **kwargs):
        super(Metadata, self).__init__()
        self.Id = str(kwargs.get('Id', None))
        self.StringValue = kwargs.get('StringValue', '')
        self.RealObjectList = kwargs.get('RealObjectList', [])

    def __str__(self):
        return self.StringValue

class Knowledge(Entity):
    """ 知识实体
    所有记忆信息（含观察者，时间等信息）都在这个表中，提炼的知识信息也在这个表中。RealObject本身也放这个表中（End为空的就是RealObject）
    （梁：不同意RealObject放此表，建议单独列个表。）
    :attributes 
        Id 唯一标识，要考虑上亿级数据的不重复。
        Start 丁字形结构的开始节点，记录的是Id。
        End 丁字形结构的右上角节点，记录的是Id。
        Threshold 阈值。本条知识的访问限制值。
            反思自学过程中，阈值会不停地刷新。阈值降低的更加牢固，阈值升高的逐渐等同断开。
        ThresholdTime 阈值计算和更新时间。（梁：2014-8-28）
    """
    __slots__ = ('Id', 'Start', 'End', 'Threshold', 'ThresholdTime')

    def __init__(self, **kwargs):
        super(Knowledge, self).__init__()
        self.Id = str(kwargs.get('Id', None))
        self.Start = kwargs.get('Start', '')
        self.End = kwargs.get('End', '')
        self.Threshold = kwargs.get('Threshold', ConstValues.threshold_initial_value)
        self.ThresholdTime = kwargs.get('ThresholdTime', datetime.datetime.now().__str__())