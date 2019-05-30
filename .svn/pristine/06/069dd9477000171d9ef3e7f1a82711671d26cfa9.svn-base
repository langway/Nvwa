#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    entity_repository 
Author:   Liuyl 
DateTime: 2014/9/5 15:39 
UpdateLog:
1、Liuyl 2014/9/5 Create this File.
2 Liuyl 2014/10/28 添加了RealObject/Memory/ActionDefine的仓库类定义
entity_repository
>>> print("No Test")
No Test
"""
__author__ = 'Liuyl'
from repository import Repository
import functools
from loongtian.nvwa.common.config import conf

# 通过更改Repository基类来改变女娲对象的存储方式
SuperRepository = Repository  # 以内存方式存储所有对象,用于测试
if conf['storage'] == 'memory':
    pass
elif conf['storage'] == 'riak':
    from riakrepository import RiakRepository
    SuperRepository = RiakRepository
elif conf['storage'] == 'redis':
    from redisrepository import RedisReposiroty
    SuperRepository = RedisReposiroty

class RealObjectRepository(SuperRepository):
    def __init__(self):
        from loongtian.nvwa.entities.entity import RealObject

        super(RealObjectRepository, self).__init__('RealObject', RealObject)
        self.index2i_dict['display_bin'] = 'Display'

class MetadataRepository(SuperRepository):
    def __init__(self):
        from loongtian.nvwa.entities.entity import Metadata

        super(MetadataRepository, self).__init__('Metadata', Metadata)
        self.index2i_dict['metadata_string_value_bin'] = 'StringValue'
        self.get_by_string_value = functools.partial(self.get_by_index2i, idx='metadata_string_value_bin')
        self.gets_by_string_value = functools.partial(self.gets_by_index2i, idx='metadata_string_value_bin')
        self.get_key_by_string_value = functools.partial(self.get_key_by_index2i, idx='metadata_string_value_bin')
        self.gets_key_by_string_value = functools.partial(self.gets_key_by_index2i, idx='metadata_string_value_bin')


class BaseKnowledgeRepository(SuperRepository):
    """
    knowledge存储
    """

    def __init__(self, entity_name, entity_type):
        super(BaseKnowledgeRepository, self).__init__(entity_name, entity_type)
        self.index2i_dict['start_bin'] = 'Start'
        self.index2i_dict['end_bin'] = 'End'
        self.get_by_start = functools.partial(self.get_by_index2i, idx='start_bin')
        self.gets_by_start = functools.partial(self.gets_by_index2i, idx='start_bin')
        self.get_key_by_start = functools.partial(self.get_key_by_index2i, idx='start_bin')
        self.gets_key_by_start = functools.partial(self.gets_key_by_index2i, idx='start_bin')
        self.get_by_end = functools.partial(self.get_by_index2i, idx='end_bin')
        self.gets_by_end = functools.partial(self.gets_by_index2i, idx='end_bin')
        self.get_key_by_end = functools.partial(self.get_key_by_index2i, idx='end_bin')
        self.gets_key_by_end = functools.partial(self.gets_key_by_index2i, idx='end_bin')


class KnowledgeRepository(BaseKnowledgeRepository):
    """
    knowledge存储
    """

    def __init__(self):
        from loongtian.nvwa.entities.entity import Knowledge

        super(KnowledgeRepository, self).__init__('Knowledge', Knowledge)


real_object_rep = RealObjectRepository()
knowledge_rep = KnowledgeRepository()
metadata_rep = MetadataRepository()

if __name__ == '__main__':
    # import doctest

    # doctest.testmod()
    rep = RealObjectRepository()
    print(rep.__dict__)