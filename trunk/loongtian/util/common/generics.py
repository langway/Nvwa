#!/usr/bin/env python
# coding: utf-8
"""
泛型列表类

"""

__author__ = 'leon'


class GenericsList(list):
    """
    指定子元素类型的list
    """

    def __init__(self, item_type:type, id_tag="id"):
        # if not isinstance(item_type, type):
        #     raise Exception("指定子元素类型错误！当前类型为：%s" % item_type)
        super(GenericsList, self).__init__()
        self.item_type = item_type
        self.id_item_dict = {}
        self.id_tag = id_tag  # 用来标记id的字符串，例如：metadata中的mvalue

        self._cur_item_index = 0  # 不断取得子元素的索引

    def append(self, obj):
        """
        （重载函数）添加到最后
        :param obj:
        :return:
        """
        if obj is None:
            return
        if not isinstance(obj, self.item_type):
            return
        super(GenericsList, self).append(obj)
        self._addById(obj)

    def extend(self, objs:list):
        """
        合并list
        :param objs:
        :return:
        """
        try:
            self._checkType(objs)
            for obj in objs:
                self.append(obj)
        except:
            pass

    def _checkType(self, obj, raise_exception=True):
        """
        类型检查
        :param obj:单个对象、list或tuple
        :return:
        """

        error_msg = "对象的类型不匹配！GenericsList已指定子对象类型为：%s,当前对象的类型为：%s"
        if isinstance(obj, list) or isinstance(obj, tuple):
            for _obj in obj:
                if isinstance(_obj, list):
                    self._checkType(_obj)
                if not isinstance(_obj, self.item_type) and raise_exception:
                    raise Exception(error_msg % (self.item_type, type(_obj)))
        else:
            if not isinstance(obj, self.item_type) and raise_exception:
                raise Exception(error_msg % (self.item_type, type(obj)))

    def insert(self, index, obj):
        """
        插入对象
        :param index:
        :param obj:
        :return:
        """
        if not isinstance(obj, self.item_type):
            return
        super(GenericsList, self).insert(index, obj)
        self._addById(obj)

    def _addById(self, obj):
        """
        根据id添加对象（如果有的话）
        :param obj:
        :return:
        """
        if hasattr(obj, self.id_tag):
            id = getattr(obj, self.id_tag)
            if not id:
                import uuid
                id = str(uuid.uuid1()).replace("-", "")
            self.id_item_dict[id] = obj

    def getById(self, id):
        """
        根据id取得子元素（如果有的话）
        :param id:
        :return:
        """
        return self.id_item_dict.get(id)

    def getCur(self):
        """
        不断取得列表中的对象/子元素（使用索引）
        :return:
        """
        if self._cur_item_index < len(self):
            cur_item = self[self._cur_item_index]
            self._cur_item_index += 1
            return cur_item
        return None

    def restoreItemInex(self):
        """
        重置列表中的对象/子元素的索引。
        :return:
        """
        self._cur_item_index = 0

    def remove(self, obj):
        """
        (重载函数)移除一个对象
        :param obj:
        :return:
        """
        if not isinstance(obj, self.item_type):
            return
        super(GenericsList, self).remove(obj)
        if hasattr(obj, "id"):
            self.id_item_dict.pop(obj.id)
