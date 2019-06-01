#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Project:  nvwa
Title:    riakrepository 
Author:   zheng 
DateTime: 2014/9/1 14:03 
UpdateLog:
1、zheng 2014/9/1 Create this File.
2、Liuyl 2014/9/5 将repository基类进行了抽取,将entity的repository移出文件

riakrepository
>>> print("No Test")
No Test
"""
import riak
import uuid
import sys
import json
from repository import Repository
from loongtian.nvwa.common.config import conf

class ClientFactory(object):
    @classmethod
    def get_client(cls):
        host = conf['riak']['host']
        port = conf['riak']['port']
        client = riak.RiakClient(host=host, pb_port=port, protocol='pbc')
        return client


class RiakRepository(Repository):
    def __init__(self, bucket, type, client=None):
        super(RiakRepository, self).__init__(bucket, type)
        reload(sys)
        sys.setdefaultencoding('utf-8')
        self.BUCKET = bucket
        self.TYPE = type
        if client is None:
            self.client = ClientFactory.get_client()
        else:
            self.client = client

    def is_initiated(self):
        riak_obj = self.client.bucket('RealObject').get('0000000000')
        if riak_obj.data:
            return True
        return False

    def initial(self):
        riak_obj = self.client.bucket('RealObject').new('0000000000', '0000000000')
        riak_obj.store()

    def save(self, entity):
        if entity.Id == None:
            entity.Id = str(uuid.uuid1())
            riak_obj = self.client.bucket(self.BUCKET).new(entity.Id, entity)
        else:
            riak_obj = self.client.bucket(self.BUCKET).get(entity.Id)
            self.client.bucket
        riak_obj.data = entity.to_json()
        self.add_index2i(riak_obj, entity)
        riak_obj.store()

    def delete(self, obj):
        self.delete_by_key(obj.Id)

    def delete_by_key(self, key):
        entity = self.client.bucket(self.BUCKET).get(key)
        entity.delete()

    def get_keys(self):
        return self.client.bucket(self.BUCKET).get_keys()

    def get(self, key):
        if key == '' or key is None:
            return None
        _tmp = self.client.bucket(self.BUCKET).get(key).data
        if _tmp is None:
            return None
        d = json.loads(_tmp)
        return self.TYPE(**d)

    def gets(self, keys):
        if len(keys) == 0:
            return []
        _ents = self.client.bucket(self.BUCKET).multiget(keys)
        return [self.TYPE(**json.loads(item.data)) for item in _ents if item is not None and item.data is not None]

    def add_index2i(self, riak_obj, entity):
        for key in self.index2i_dict:
            riak_obj.add_index(key, getattr(entity, self.index2i_dict[key]))

    def get_by_index2i(self, value, idx):
        """
        通过二级索引查询对象列表
        :param idx:二级索引名称
        :param value: 值
        :return:索引列表
        """
        _keys = self.client.bucket(self.BUCKET).get_index(idx, value).results
        if len(_keys) == 0:
            return []
        return self.gets(_keys)
        # _ents = self.client.bucket(self.BUCKET).multiget(_keys)
        # return [self.TYPE(**json.loads(item.data)) for item in _ents if item is not None]
        # return [self.get(key) for key in self.client.bucket(self.BUCKET).get_index(idx, value).results]

    def get_key_by_index2i(self, value, idx):
        """
        通过二级索引查询key列表
        :param idx:二级索引名称
        :param value: 值
        :return:索引列表
        """
        return self.client.bucket(self.BUCKET).get_index(idx, value).results

    def clear(self):
        for key in self.client.bucket(self.BUCKET).get_keys():
            self.client.bucket(self.BUCKET).delete(key)

    def get_matches(self):
        '''
        随机数据，遗忘用 riak
        :return:
        '''
        query = self.client.add(self.BUCKET)
        import util

        query.add_key_filter("matches", util.get_match_string())
        return [item[1] for item in query.run()]


if __name__ == "__main__":
    import doctest

    doctest.testmod()