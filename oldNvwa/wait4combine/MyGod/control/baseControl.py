#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
控制器基类
>>> from loongtian.nvwa.common.runnable import run as Run
>>> control = BaseControl()
>>> Run(control)
>>> Runnable.pool.wait()
Control start
Control stopping
Control stop
"""
__author__ = 'Liuyl'
import Queue

from common.runnable import Runnable as Runnable


class BaseControl(Runnable):
    def __init__(self):
        super(BaseControl, self).__init__()
        self._name = "Control"
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
