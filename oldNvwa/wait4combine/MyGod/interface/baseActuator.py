#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
执行器基类
执行器需要继承此类
handle接口:处理指令的逻辑实现
canHandle接口:判断某指令是否可以被自身处理
执行器没有自身buffer,执行器需要被绑定在一个ActuatorMind中
>>> print("No Test")
No Test
"""
__author__ = 'Liuyl'


class BaseActuator(object):
    def __init__(self):
        pass

    def handle(self, command):
        return

    def canHandle(self, command):
        return False


if __name__ == '__main__':
    import doctest

    doctest.testmod()