#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    collection 
Author:   fengyh 
DateTime: 2015/5/28 10:39 
UpdateLog:
1、fengyh 2015/5/28 Create this File.


"""

from loongtian.nvwa.core.gdef import OID
from loongtian.nvwa.entities.entity import RealObject, Knowledge
from loongtian.nvwa.service import metadata_srv, original_srv, real_object_srv, knowledge_srv


class Collection(object):
    def __init__(self, name,item=None):
        self.collection_base_object = real_object_srv.get(OID.Collection)
        self.collection_contain_item_object = real_object_srv.get(OID.CollectionContainItem)
        self.next_item_object = real_object_srv.get(OID.NextItem)

        # 生成新集合对象
        metadata_srv.create(name)
        self.collection_object = original_srv.SymbolInherit.find(right=metadata_srv.get_default_by_string_value(name))[0]
        #self.collection_object = real_object_srv.create(Display=name)
        # 新集合对象父对象是集合基类
        original_srv.InheritFrom.set(self.collection_object, self.collection_base_object, knowledge_srv)

        self.object_list = []
        # 生成的结果集合，里面保存的每个元素都是关系。
        self.result_collection = []
        # 集合之间的顺序关系
        self.result_collection_relations = []

        self.item = item
        if type(self.item) == list:
            self.object_list = self.item
            self.__gen_collection_from_item_list__()
            pass
        elif self.item is not None:
            self.object_list.append(self.item)
            self.__gen_collection_from_item_single__()
        else:
            pass

    def __gen_collection_from_item_list__(self):
        """
        0 A 继承自
        1 0 集合

        2 A 元素包含
        3 2 a
        4 2 b

        5 3 下一个
        6 5, 4

        :return:
        """
        for item_a in self.item:
            item_in_collection_memory = self.__gen_collection_from_item__(item_a)
            self.result_collection.append(item_in_collection_memory)
        for index, item_a in enumerate(self.result_collection):
            if index == 0:
                continue
            item_relation_in_collection_memory = self.__gen_collection_relation_next__(
                self.result_collection[index - 1], item_a)
            self.result_collection_relations.append(item_relation_in_collection_memory)

        pass

    def __gen_collection_from_item_single__(self):
        item_in_collection_memory = self.__gen_collection_from_item__(self.item)
        self.result_collection.append(item_in_collection_memory)

    def is_ordered(self):
        """
        判断是有序集合True还是无序集合False
        :return:
        """
        if self.result_collection_relations.__len__() > 0:
            return True
        else:
            return False

    def count(self):
        return self.result_collection.__len__()

    def __eq__(self, other):
        if self.is_ordered():
            pass

        pass

    def __hash__(self):
        pass

    def __gen_collection_from_item__(self, item):
        item_in_collection_memory = knowledge_srv.create_t_structure(self.collection_object,
                                                                     self.collection_contain_item_object,
                                                                     item)
        return item_in_collection_memory

    def __gen_collection_relation_next__(self, item1, item2):
        item_in_collection_memory = knowledge_srv.create_t_structure(item1, self.next_item_object, item2)
        return item_in_collection_memory

    pass


class CollectionUtil(object):
    """
    汇集集合操作各种方法。
    """

    @staticmethod
    def intersection(c1_id, c2_id):
        """
        获取两个集合的交集。
        :param c1_id:第一个集合的id。
        :param c2_id:第二个集合的id。
        :return:交集组成的list。
        """
        c1 = CollectionUtil.find_collection_by_collection_object(c1_id)
        c2 = CollectionUtil.find_collection_by_collection_object(c2_id)
        return list(set(c1).intersection(set(c2)))

    @staticmethod
    def union(c1_id, c2_id):
        """
        获取两个集合的并集。
        :param c1_id:第一个集合的id。
        :param c2_id:第二个集合的id。
        :return:并集组成的list。
        """
        c1 = CollectionUtil.find_collection_by_collection_object(c1_id)
        c2 = CollectionUtil.find_collection_by_collection_object(c2_id)
        return list(set(c1).union(set(c2)))


    @staticmethod
    def difference(c1_id, c2_id):
        """
        c1中有而c2中没有
        :param c1_id:第一个集合的id。
        :param c2_id:第二个集合的id。
        :return:c1有c2没有的差集组成的list。
        """
        c1 = CollectionUtil.find_collection_by_collection_object(c1_id)
        c2 = CollectionUtil.find_collection_by_collection_object(c2_id)
        return list(set(c1).difference(set(c2)))  # c1中有而c2中没有的

    @staticmethod
    def contain(c1_id, c2_id):
        """
        集合c1包含集合c2，c2中的元素在c1中都有
        :param c1_id:第一个集合的id。
        :param c2_id:第二个集合的id。
        :return:Ture False
        """
        c1 = CollectionUtil.find_collection_by_collection_object(c1_id)
        c2 = CollectionUtil.find_collection_by_collection_object(c2_id)
        for i in c2:
            if not c1.__contains__(i):
                return False
        return True

    @staticmethod
    def find_collection_by_collection_object(collection_object):
        """
        根据指定集合id查找到该集合，返回集合元素（就是id）构成的list。
        :param idInt:
        :return:
        """
        collection_id = None
        if type(collection_object) is RealObject:
            collection_id = collection_object.Id
        elif type(collection_object) is Knowledge:
            collection_id = collection_object.Start

        collection_contain_item_object = real_object_srv.get(OID.CollectionContainItem)
        collection_contain = knowledge_srv.base_select_start_end(collection_id, collection_contain_item_object.Id)
        if collection_contain is None:
            return []
        items = knowledge_srv.base_select_start(collection_contain.Id)
        item_ids = [real_object_srv.get(i.End) for i in items]
        return item_ids

    @staticmethod
    def find_collection_by_collection_name(collection_name):
        """
        根据指定集合id查找到该集合，返回集合元素（就是id）构成的list。
        :param idInt:
        :return:
        """
        #collection_object = metadata_srv.get_default_by_string_value(collection_name)
        collection_object = original_srv.SymbolInherit.find(right=metadata_srv.get_default_by_string_value(collection_name))[0]
        return collection_object,CollectionUtil.find_collection_by_collection_object(collection_object)

    @staticmethod
    def find_collection_by_item(item_object):
        """
        根据指定元素item查找到其所属的集合，返回集合元素（就是id）构成的list。
        :param item_object:
        :return:
        """
        # 找到所有以指定元素id为end的数据
        item_in_collection = knowledge_srv.base_select_end(item_object.Id)

        collection_list_list = []
        collection_id_list = []
        # 过滤其中start不是集合的情况
        for i in item_in_collection:
            c_object = knowledge_srv.get(i.Start)
            collection = CollectionUtil.find_collection_by_collection_object(c_object)
            if collection is not None:
                collection_list_list.append(collection)
                collection_id_list.append(c_object.Start)

        return collection_list_list, collection_id_list

    @staticmethod
    def find_next_item_in_collection(current_item_object, collection_object=None):
        """
        根据传入的元素对象（不是id）查找该元素所在集合的下一个元素。
        如果传入了第二个参数集合id，则在该集合中找，否则，则先找元素所属集合，如果有多个集合，则默认选第一个集合。
        :param current_item:
        :param collection_id:
        :return:如果找到则返回下一个元素，否则返回None。
        """
        c = None
        c_id = None
        if collection_object is None:
            c, c_id = CollectionUtil.find_collection_by_item(current_item_object)
            if c is None:
                return None
            elif c.__len__() > 0:
                c = c[0]
                c_id = c_id[0]
            else:
                return None
        else:
            c = CollectionUtil.find_collection_by_collection_object(collection_object)
            c_id = collection_object.Id

        next_relation = real_object_srv.get(OID.NextItem)
        item_next_data = knowledge_srv.base_select_start_end(
            CollectionUtil.get_item_id_in_collection(current_item_object.Id, c_id).Id, next_relation.Id)
        if item_next_data is not None:
            item_next_relation = item_next_data
            item_next_list = knowledge_srv.base_select_start(item_next_relation.Id)
            item_next_list2 = [CollectionUtil.get_item_id_out_collection(i.End) for i in item_next_list]
            next_item_list = list(set(c).intersection(set(item_next_list2)))
            if next_item_list.__len__() > 0:
                return next_item_list[0]
        return None

    @staticmethod
    def get_item_id_in_collection(item_id, collection_id):
        c = knowledge_srv.base_select_start_end(collection_id, OID.CollectionContainItem)
        item_in_collection = knowledge_srv.base_select_start_end(c.Id, item_id)
        return item_in_collection

    @staticmethod
    def get_item_id_out_collection(item_id):
        return knowledge_srv.get(item_id).End


    @staticmethod
    def is_sorted(collection_object):
        """
        判断指定集合是否是有序的。
        规定所有元素之间均表示了下一个关系，则为有序；不完整或没有标记则为无序。
        允许最后一个元素没有下一个元素。一个集合只允许有一个元素无下一个元素。
        :param collection_object:
        :return:
        """
        c1 = CollectionUtil.find_collection_by_collection_object(collection_object)
        next_none_count = 0
        for i in c1:
            next_item = CollectionUtil.find_next_item_in_collection(i, collection_object)
            if next_item is None:
                next_none_count += 1
            if next_none_count > 1:
                return False
        return True


    @staticmethod
    def contain_item(collection_object,item_object):
        item_ids = CollectionUtil.find_collection_by_collection_object(collection_object)
        return item_ids.__contains__(item_object)

    @staticmethod
    def find_sorted_collection_by_collection_object(collection_object):
        """
        根据指定集合Id，判断如果是有序集合，则返回排好序的元素结果列表，无序则返回无序列表。
        :param collection_object:
        :return:
        """
        c1 = CollectionUtil.find_collection_by_collection_object(collection_object)
        if CollectionUtil.is_sorted(collection_object):
            new_c1 = []
            last_item = None
            while c1.__len__()>0:
                current_item = c1[0]
                next_item = CollectionUtil.find_next_item_in_collection(current_item, collection_object)
                while next_item != last_item:
                    current_item = next_item
                    next_item = CollectionUtil.find_next_item_in_collection(next_item, collection_object)
                new_c1.insert(0,current_item)
                c1.remove(current_item)
                last_item = new_c1[0]
            return new_c1
        else:
            return c1

    @staticmethod
    def append(collection_object,item):
        #collection_object = real_object_srv.get(collection_id)
        collection_contain_item_object = real_object_srv.get(OID.CollectionContainItem)
        next_item_object = real_object_srv.get(OID.NextItem)

        collection = CollectionUtil.find_sorted_collection_by_collection_object(collection_object)
        if collection.__len__() > 0:
            last_item = collection[-1]
            append_item = knowledge_srv.create_t_structure(collection_object,collection_contain_item_object,item)
            knowledge_srv.create_t_structure(CollectionUtil.get_item_id_in_collection(last_item.Id,collection_object.Id), next_item_object, append_item)
        else:
            # 这是第一个元素的情况
            append_item = knowledge_srv.create_t_structure(collection_object,collection_contain_item_object,item)
        pass