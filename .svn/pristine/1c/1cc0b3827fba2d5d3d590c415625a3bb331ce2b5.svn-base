from .repository import Repository
import uuid
import sys
import json
import redis
from loongtian.nvwa.common.config import conf
from loongtian.nvwa.entities.entity import Metadata, RealObject, Knowledge


class ClientFactory(object):
    @classmethod
    def get_client(cls, entity_name):
        host = conf['redis']['host']
        port = conf['redis']['port']
        typedic = {'Metadata': 0, 'RealObject': 1, 'Knowledge': 2, 'starts': 7, 'ends': 8, 'strings': 9, 'display': 10,
                   'tmp': 15}
        client = redis.StrictRedis(host=host, port=port, db=typedic.get(entity_name))
        return client


class RedisReposiroty(Repository):
    def __init__(self, entity_name, entity_type, client=None):
        super(RedisReposiroty, self).__init__(entity_name, entity_type)
        self.entity_name = entity_name
        self.TYPE = entity_type
        if client is None:
            self.client = ClientFactory.get_client(entity_name)
        else:
            self.client = client

        self.client_dic = {'start_bin': ClientFactory.get_client('starts'),
                           'end_bin': ClientFactory.get_client('ends'),
                           'metadata_string_value_bin': ClientFactory.get_client('strings'),
                           'display_bin': ClientFactory.get_client('display')}


    def is_initiated(self):
        client = ClientFactory.get_client('tmp')
        _tmp = client.get('0000000000')
        if _tmp:
            return True
        return False

    def initial(self):
        client = ClientFactory.get_client('tmp')
        client.set('0000000000', '0000000000')

    def save(self, entity):
        if entity.Id == None:
            entity.Id = str(uuid.uuid1())
        self.client.set(entity.Id, entity.to_json())
        if isinstance(entity, RealObject):
            self.add_index2i('display_bin', entity.Display, entity.Id)
            return
        if isinstance(entity, Metadata):
            self.add_index2i('metadata_string_value_bin', entity.StringValue, entity.Id)
            return
        self.add_index2i('start_bin', entity.Start, entity.Id)
        self.add_index2i('end_bin', entity.End, entity.Id)

    def delete(self, obj):
        self.delete_by_key(obj.Id)

    def delete_by_key(self, key):
        self.client.delete(key)

    def get_keys(self):
        return self.client.keys()

    def get(self, key):
        if key == '' or key is None:
            return None
        _tmp = self.client.get(key)
        if _tmp is None:
            return None
        d = json.loads(_tmp)
        return self.TYPE(**d)

    def gets(self, keys):
        _ent = self.client.mget(keys)
        return [self.TYPE(**json.loads(item)) for item in _ent if item is not None]

    def add_index2i(self, index2i, key, value):
        _client = self.client_dic.get(index2i)
        _client.sadd(key, value)

    def get_by_index2i(self, value, idx):

        _client = self.client_dic.get(idx)
        _tmplist = _client.smembers(value)
        if len(_tmplist) == 0:
            return []
        _ent = self.client.mget([item for item in _tmplist])
        return [self.TYPE(**json.loads(item)) for item in _ent if item is not None]

    def get_key_by_index2i(self, value, idx):
        _client = self.index2i_dic.get(idx)
        _tmplist = _client.sinter(value)
        return _tmplist

    def clear(self):
        self.client.flushall()

    def get_matches(self):
        return self.get_keys()