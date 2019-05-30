#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
默认配置项
>>> print("No Test")
No Test
"""
__author__ = 'Liuyl'
configs = {
    'path': {
        'root': 'F:/LylWorkspace/nvwa/wait4combine/MyGod/',
        'log_conf': 'conf/logging.properties'
    },
    'redis': {
        'cache': {
            'host': '192.168.1.100',
            'port': 6380,
            'db': 0,
            'max_connections': 10
        },
        'store': {
            'host': '192.168.1.100',
            'port': 6379,
            'db': 0,
            'max_connections': 10
        }
    },
    'sensor': [
        {
            'sensor': 'plugin.console.sensor',
            'translator': 'translator.text'
        },
    ],
    'actuator': [
        {
            'actuator': 'plugin.console.actuator',
            'translator': 'translator.text'
        },
    ]
}
if __name__ == '__main__':
    import doctest

    doctest.testmod()
