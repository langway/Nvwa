#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
>>> cacheInstance = RedisCache().cache()
>>> cacheInstance2 = RedisCache().cache()
>>> cacheInstance.set("key","hello world")
True
>>> cacheInstance2.get("key")
'hello world'
>>> cacheInstance.delete("key")
1
>>> @cache("key")
... def get():
...     print("no cache")
...     return "cache text"
>>> print(get())
no cache
cache text
>>> print(get())
cache text
"""
from conf.config import configs as configs

__author__ = 'Liuyl'
import functools
import pickle
import redis
import singleton


@singleton.singleton
class RedisCache(object):
    """
    基于Redis的Cache连接池
    """

    def __init__(self, *args, **kw):
        conf = configs['redis']['cache']
        self.host = conf['host']
        self.port = conf['port']
        self.db = conf['db']
        self.max_connections = conf['max_connections']
        self.__pool = redis.ConnectionPool(host=self.host, port=self.port, db=self.db,
                                           max_connections=self.max_connections)

    def cache(self):
        return redis.StrictRedis(connection_pool=self.__pool)


def cache(key):
    _cache = RedisCache().cache()

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            value = _cache.get(key)
            if value:
                return pickle.loads(value)
            else:
                value = func(*args, **kw)
                _cache.set(key, pickle.dumps(value))
                return value

        return wrapper

    return decorator


if __name__ == '__main__':
    import doctest

    doctest.testmod()