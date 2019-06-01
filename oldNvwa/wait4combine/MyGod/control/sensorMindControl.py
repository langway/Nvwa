#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
新建python文件
>>> print("No Test")
No Test
"""
__author__ = 'Liuyl'
import time
import importlib

from baseControl import BaseControl as BaseControl
from brain.sensorMind import SensorMind as SensorMind
from common.runnable import run as Run
from conf.config import configs as configs


class SensorMindControl(BaseControl):
    def __init__(self):
        super(SensorMindControl, self).__init__()
        self._name = "SensorMindControl"
        self.__minds = []
        conf = configs['sensor']
        for item in conf:
            sensor_module = importlib.import_module(item['sensor'])
            translator_module = importlib.import_module(item['translator'])
            self.__minds.append(SensorMind(getattr(sensor_module, 'Sensor'), getattr(translator_module, 'Translator')))

    def _execute(self):
        for mind in self.__minds:
            Run(mind)
        while True:
            time.sleep(1)
            if not self.state():
                for mind in self.__minds:
                    mind.stop()
                break


if __name__ == '__main__':
    import doctest

    doctest.testmod()
