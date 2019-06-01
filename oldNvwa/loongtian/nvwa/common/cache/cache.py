#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    cache 
Author:   Liuyl 
DateTime: 2015/1/7 16:07 
UpdateLog:
1、Liuyl 2015/1/7 Create this File.

cache
>>> print("No Test")
No Test
"""
import functools
from loongtian.nvwa.core.gdef import GlobalDefine

__author__ = 'Liuyl'


def i_cache(cache_buffer, key_lambda):
    """
    可以指定生命周期的缓存
    :param cache_buffer: 传入一个用于缓存数据存储的字典,该字典失效时缓存也同时失效
    :param key_lambda: 一个表达式用于从目标函数的参数中计算缓存的key
    :return:
    """

    def outer_wrapper(func):
        @functools.wraps(func)
        def inner_wrapper(*args, **kwargs):
            _target_cache = cache_buffer
            key = key_lambda(args, kwargs)
            if key not in _target_cache:
                _target_cache[key] = func(*args, **kwargs)
            return _target_cache[key]

        return inner_wrapper

    return outer_wrapper


def cache(name, key_lambda):
    """
    缓存装饰器
    :param name: 缓存名称
    :param key_lambda: 一个表达式用于从目标函数的参数中计算缓存的key
    :return:
    """

    def outer_wrapper(func):
        @functools.wraps(func)
        def inner_wrapper(*args, **kwargs):
            _target_cache = GlobalDefine().cache_dict.get(name, None)
            if not _target_cache:
                _target_cache = {}
                GlobalDefine().cache_dict[name] = _target_cache
            key = key_lambda(args, kwargs)
            if key not in _target_cache:
                _target_cache[key] = func(*args, **kwargs)
            return _target_cache[key]

        return inner_wrapper

    return outer_wrapper


if __name__ == '__main__':
    import doctest

    doctest.testmod()