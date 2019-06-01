#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
新建python文件
>>> print("No Test")
No Test
"""
__author__ = 'Liuyl'
import time

from baseControl import BaseControl as BaseControl
from common.runnable import run as Run
from brain.thinkMind import ThinkMind as ThinkMind


class ThinkMindControl(BaseControl):
    def __init__(self):
        super(ThinkMindControl, self).__init__()
        self._name = "ThinkMindControl"
        self.__minds = []

    def _execute(self):
        while True:
            time.sleep(1)
            if not self.state():
                for mind in self.__minds:
                    mind.stop()
                break
            if not self._buff.empty():
                handled = False
                knowledge = self._buff.get()
                for mind in self.__minds:
                    if mind.state() is False:
                        self.__minds.remove(mind)
                        continue
                    if mind.focus(knowledge):
                        mind.put(knowledge)
                        handled = True
                        break
                if not handled:
                    newMind = ThinkMind()
                    Run(newMind)
                    self.__minds.append(newMind)
                    newMind.put(knowledge)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
