#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
负责管控执行器的思维逻辑
>>> print("No Test")
No Test
"""
__author__ = 'Liuyl'
from BaseMind import BaseMind
import time


class ActuatorMind(BaseMind):
    def __init__(self, actuatorType, translatorType):
        super(ActuatorMind, self).__init__()
        self._name = "ActuatorMind"
        self._actuator = actuatorType()
        self._translator = translatorType()

    def _execute(self):
        while True:
            time.sleep(1)
            if not self.state():
                break
            if not self._buff.empty():
                knowledge = self._translator.encode(self._buff.get())
                self._actuator.handle(knowledge)

    def focus(self, knowledge):
        return True


if __name__ == '__main__':
    import doctest

    doctest.testmod()
