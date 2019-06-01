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
from brain.actuatorMind import ActuatorMind as ActuatorMind
from common.runnable import run as Run
from conf.config import configs as configs

class ActuatorMindControl(BaseControl):
    def __init__(self):
        super(ActuatorMindControl, self).__init__()
        self._name = "ActuatorMindControl"
        self.__minds = []
        conf = configs['actuator']
        for item in conf:
            actuator_module = importlib.import_module(item['actuator'])
            translator_module = importlib.import_module(item['translator'])
            self.__minds.append(
                ActuatorMind(getattr(actuator_module, 'Actuator'), getattr(translator_module, 'Translator')))

    def _execute(self):
        for mind in self.__minds:
            Run(mind)
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
                    if mind.focus(knowledge):
                        mind.put(knowledge)
                        handled = True
                        break
                if not handled:
                    print("can not handle : %s" % knowledge)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
