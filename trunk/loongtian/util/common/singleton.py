#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'CoolSnow'

import threading

def singleton(cls):
    """
    线程安全单例模式装饰器
    在需要是单例的类定义上标注@singleton即可
    按照单例模式的设计思想, 这里设定, 单例类无构造参数, 不允许通过类名访问静态变量和函数
    eg：
    @singleton
    class ClassName(object):
        pass
    """
    _instances = {}
    _initLock = threading.Lock()

    def _singleton(*args, **kw):
        if cls not in _instances:
            _initLock.acquire()
            try:
                if cls not in _instances:
                    _instances[cls] = cls(*args, **kw)
            finally:
                _initLock.release()
        return _instances[cls]
    return _singleton