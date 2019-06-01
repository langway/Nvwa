#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
新建python文件
>>> print("No Test")
No Test
"""
__author__ = 'Liuyl'
import threading
from singleton import singleton as Singleton


@Singleton
class Console(object):
    def __init__(self):
        self.prompt = "nvwa"
        self.waitForResponseLock = threading.Lock()

    def waitForResponse(self):
        self.waitForResponseLock.acquire()

    def responseHasArrive(self):
        self.waitForResponseLock.release()

    def input(self, value=None):
        if value is not None:
            return self.simulateConsole(value)
        else:
            return self.console()

    def output(self, value):
        print("%s >>> %s" % (self.prompt, value))

    def simulateConsole(self, value):
        print("%s <<< %s" % (self.prompt, value))
        return value

    def console(self,
                prompt=None,
                default=None,
                intro=None,
                valid=lambda x: True):
        if not prompt:
            prompt = self.prompt
        if intro:
            print(intro)
        while True:
            user_input = raw_input("%s <<< " % prompt)
            if valid(user_input):
                break

        if user_input:
            return user_input
        else:
            return default


if __name__ == '__main__':
    import doctest

    doctest.testmod()
