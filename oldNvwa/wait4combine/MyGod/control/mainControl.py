#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
主控制器
>>> print("No Test")
No Test
"""
__author__ = 'Liuyl'
import time

from baseControl import BaseControl as BaseControl
from sensorMindControl import SensorMindControl as SensorMindControl
from actuatorMindControl import ActuatorMindControl as ActuatorMindControl
from thinkMindControl import ThinkMindControl as ThinkMindControl
from brain.sensorMind import SensorMind as SensorMind
from brain.thinkMind import ThinkMind as ThinkMind
from common.runnable import Runnable as Runnable
from common.runnable import run as Run


class MainControl(BaseControl):
    def __init__(self):
        super(MainControl, self).__init__()
        self.__controls = []
        self._name = "MainControl"

        actuatorMindControl = ActuatorMindControl()
        ThinkMind.actuatorMindControl = actuatorMindControl
        self.__controls.append(actuatorMindControl)

        thinkMindControl = ThinkMindControl()
        SensorMind.thinkMindControl = thinkMindControl
        self.__controls.append(thinkMindControl)
        self.__controls.append(SensorMindControl())

    def _execute(self):
        for control in self.__controls:
            Run(control)
        while True:
            time.sleep(1)
            if not self.state():
                for control in self.__controls:
                    control.stop()
                break


if __name__ == '__main__':
    # import doctest

    # doctest.testmod()
    main = MainControl()
    Run(main)
    Runnable.pool.wait()