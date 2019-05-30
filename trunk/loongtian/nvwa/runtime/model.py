#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

ignore_attribs = ["database_name", "table_name", "constrain", "tags"]


class Model(object):
    """
    [运行时对象]数据模型的封装类（是女娲世界与类、数据库沟通的桥梁。例如：UserModel，能够将女娲世界定义的用户与用户表一一对应）
    """

    def __init__(self):

        self.database_name = None  # 对应数据库的表的名称
        self.table_name = None  # 对应数据库的表的名称
        self.structure = {}  # 数据的结构{列名:数据类型}。
        self.constrain = Constrain()
        self.tags = {}
        self.attrs = []
        self.getAttribute()

    def getAttribute(self):
        """
        取得当前模型的所有定义出来的属性
        :return:
        """
        li = dir(self)
        self.attrs = []
        for item in li:
            if item.startswith("__") or item in ignore_attribs:  # 略过私有变量及女娲系统定义的属性
                continue

            if hasattr(self, item):
                self.attrs.append(item)
        return self.attrs

    def addAttribsByStructure(self):
        for attrib_name in self.structure.keys():
            self.__setattr__(attrib_name,None)

    def add_column(self, column_name, column_type):
        """
        添加一列
        :param column_name: 列名
        :param column_type: 数据类型
        :return:
        """
        self.structure[column_name] = column_type

    def get_column_type(self, column_name):
        """
        取得一列的数据类型
        :param column_name: 列名
        :return:
        """
        return self.structure.get(column_name)

    def pop_column(self, column_name):
        """
        删除一列。
        :param column_name: 列名
        :return:
        """
        return self.structure.pop(column_name)


class Constrain():
    """
    [运行时对象]对数据模型的约束
    """

    def __init__(self):
        self.valueType = {}  # 数据类型（主要对数据库）

        self.primary = []  # 主属性
        self.unique = []  # 值唯一的属性
        self.mutex = []  # 互斥属性（成对出现）
        self.shouldHaveOne = []  # 必须有一个（例如：用户名、email、电话）
