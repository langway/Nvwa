#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
负责管控感知器的思维逻辑
>>> print("No Test")
No Test
"""
__author__ = 'Liuyl'
from BaseMind import BaseMind
import time


class SensorMind(BaseMind):
    thinkMindControl = None

    def __init__(self, sensorType, translatorType):
        super(SensorMind, self).__init__()
        self._name = "SensorMind"
        self._sensor = sensorType(self._buff)
        self._translator = translatorType()

    def _execute(self):
        while True:
            time.sleep(1)
            self._sensor.input()
            if not self.state():
                break
            if not self._buff.empty():
                knowledge = self._translator.decode(self._buff.get())
                SensorMind.thinkMindControl.put(knowledge)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
