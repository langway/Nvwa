#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Leon'


class DoubleKeyDict(object):
    """
    双键字典（女娲系统的metanet、knowledge、layer的内存存储、查找都使用双键字典）
    """

    def __init__(self,key1_name=None,key2_name=None):
        self.id_dict = {}# 对象id字典{id:obj}
        self.double_key_obj_dict = {} # 对象双键字典{key1:{key2:obj}}
        self.id_keys_dict={} # 对象id-双键字典{id:{key1,key2}}

        self.key1_name = key1_name # 在对象中，键1的名称
        self.key2_name = key2_name # 在对象中，键2的名称

    def add(self, id, key1, key2, obj):
        """
        添加一个对象。
        :param id:
        :param key1:
        :param key2:
        :param obj:
        :return:
        """
        if not hasattr(obj,"id"):
            raise Exception("双键值词典存储对象必须具有id!")

        if self.key1_name and not hasattr(obj, self.key1_name):
            raise Exception("双键值词典存储对象必须具有%s属性!" % self.key1_name)

        if self.key2_name and not hasattr(obj, self.key2_name):
            raise Exception("双键值词典存储对象必须具有%s属性!" % self.key2_name)

        if self.id_dict.has_key(id): # 如果已经有了，直接返回
            return
        key2_dict = self.double_key_obj_dict.get(key1)
        if key2_dict:
            key2_dict[key2] =obj
        else:
            self.double_key_obj_dict[key1] = {key2: obj}
        self.id_dict[id] = obj
        self.id_keys_dict[id] = (key1,key2)


    def getById(self, id):
        """
        从内存中根据Id取得对象
        :param id:
        :return:
        """
        return self.id_dict.get(id)

    def getByKeys(self, key1, key2):
        """
        从内存中根据双键取得对象
        :param key1:
        :param key2:
        :return:
        """
        if not key1:
            raise Exception("必须提供key1以供查询！")
        key2_dict = self.double_key_obj_dict.get(key1)
        if key2_dict:
            if key2:
                return key2_dict.get(key2)
            else:
                return key2_dict

        return None

    def deleteById(self, id):
        """
        从内存中根据Id删除对象
        :param id:
        :return:
        """
        keys= self.id_keys_dict.get(id)
        if keys:
            key2_dict = self.double_key_obj_dict.get(keys[0])
            if key2_dict:
                key2_dict.pop(keys[1],False)

            self.id_keys_dict.pop(id,False)
            return self.id_dict.pop(id,False)

    def deleteByKeys(self, key1, key2):
        """
        从内存中根据双键删除对象
        :param key1:
        :param key2:
        :return:
        """
        key2_dict = self.double_key_obj_dict.get(key1)
        if key2_dict:
            _obj = key2_dict.get(key2)
            if _obj:
                key2_dict.pop(key2,False)
                self.id_dict.pop(_obj.id,False)
                return self.id_keys_dict.pop(_obj.id,False)
        return False


    def clean(self):
        """
        清除内存数据
        :return:
        """
        self.id_dict = {}
        self.double_key_obj_dict = {}
        self.id_keys_dict ={}
