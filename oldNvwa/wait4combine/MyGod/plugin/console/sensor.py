#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
控制台感知器
>>> import Queue

>>> buff = Queue.Queue()
>>> c = Sensor(buff)
>>> c.input(1)
nvwa >>> 1
>>> print(buff.get())
1
"""
__author__ = 'Liuyl'

from interface.baseSensor import BaseSensor as BaseSensor
from common.console import Console as Console


class Sensor(BaseSensor):
    def __init__(self, buff):
        super(Sensor, self).__init__(buff)
        self.__console = Console()

    def input(self):
        self.__console.waitForResponse()
        self._put(self.__console.input())


if __name__ == '__main__':
    import doctest

    doctest.testmod()


