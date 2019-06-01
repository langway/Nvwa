#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
思维逻辑
>>> from loongtian.nvwa.common.runnable import run as Run
>>> mind = BaseMind()
>>> Run(mind)
>>> Runnable.pool.wait()
BaseMind start
BaseMind stopping
BaseMind stop
"""
__author__ = 'Liuyl'
import Queue

from common.runnable import Runnable as Runnable
from loongtian.nvwa.service.repository_service.memory.globalMemory import GlobalMemory as GlobalMemory


class BaseMind(Runnable):
    globalMemory = GlobalMemory()

    def __init__(self):
        super(BaseMind, self).__init__()
        self._name = "BaseMind"
        self._buff = Queue.Queue()

    def _execute(self):
        while True:
            if not self.state():
                break
            self.stop()

    def put(self, knowledge):
        self._buff.put(knowledge)


if __name__ == '__main__':
    import doctest

    doctest.testmod()