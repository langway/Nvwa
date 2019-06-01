#!/usr/bin/env python
# coding: utf-8
""" config
配置包
"""
__author__ = 'Liuyl'
import config_default

__all__ = ['conf']
conf = config_default.configs.copy()

try:
    import config_override

    conf.update(config_override.configs)
except ImportError:
    pass

if __name__ == '__main__':
    import doctest

    doctest.testmod()