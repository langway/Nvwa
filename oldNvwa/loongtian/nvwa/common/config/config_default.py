#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
默认配置项
>>> print("No Test")
No Test
"""
__author__ = 'Liuyl'
configs = {
    #memory redis   riak
    'storage': 'memory',
    'init': {
    },
    'brain': {
        'console_ip': '127.0.0.1',
        'console_port': 8077,
        'manage_ip': '127.0.0.1',
        'manage_port': 8078
    },
    'redis': {
        'host': '192.168.1.157',
        'port': 6379
    },
    'riak': {
        'host': '192.168.1.157',
        'port': 8087
    }
}
if __name__ == '__main__':
    import doctest

    doctest.testmod()
