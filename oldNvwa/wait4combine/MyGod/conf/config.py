#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
全局配置项对象
>>> print("No Test")
No Test
"""
__author__ = 'Liuyl'
import config_default
configs = config_default.configs.copy()

try:
    import config_override
    configs.update(config_override.configs)
except ImportError:
    pass
if __name__ == '__main__':
    import doctest

    doctest.testmod()
