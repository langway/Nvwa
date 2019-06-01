#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
新建python文件
>>> print("No Test")
No Test
"""
__author__ = 'Liuyl'
from BaseMind import BaseMind
import time


class ThinkMind(BaseMind):
    actuatorMindControl = None

    def __init__(self):
        super(ThinkMind, self).__init__()
        self._name = "ThinkMind"

    def _execute(self):
        while True:
            time.sleep(1)
            if not self.state():
                break
            if not self._buff.empty():
                knowledge = self._buff.get()
                ThinkMind.actuatorMindControl.put(knowledge)

    def focus(self, knowledge):
        if self.__relateFilter__(knowledge):
            return True
        else:
            return False


    def __relateFilter__(self, knowledge):
        return True

    def __ruleFilter__(self):
        pass

    def __factFilter__(self):
        pass


if __name__ == '__main__':
    import doctest

    doctest.testmod()
