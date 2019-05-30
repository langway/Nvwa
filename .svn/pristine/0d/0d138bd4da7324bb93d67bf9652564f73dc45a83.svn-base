#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
控制台执行器
>>> c = Console()
>>> c.execute("test")
test
"""
__author__ = 'Liuyl'
from interface.baseActuator import BaseActuator as BaseActuator
from common.console import Console as Console


class Actuator(BaseActuator):
    def __init__(self):
        super(Actuator, self).__init__()
        self.__console = Console()

    def handle(self, command):
        self.__console.output(command)
        self.__console.responseHasArrive()

    def canHandle(self, command):
        if command is str:
            return True

if __name__ == '__main__':
    import doctest

    doctest.testmod()