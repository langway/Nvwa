#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
新建python文件
>>> print("No Test")
No Test
"""
__author__ = 'Liuyl'
import threading
from singleton import singleton
import sys


@singleton
class Console(object):
    def __init__(self):
        self.prompt = u"nvwa"
        self.wait_for_response_lock = threading.Lock()
        self._is_listen = False

    def wait_for_response(self):
        self.wait_for_response_lock.acquire()

    def response_has_arrive(self):
        self.wait_for_response_lock.release()

    def input(self, value=None):
        if value is not None:
            return self.simulateConsole(value)
        else:
            return self.console()

    def output(self, value):
        sys.stdout.write(u"   [%s]: %s\n" % (self.prompt, value))

    def simulate_console(self, value):
        print(u"[To %s]: %s" % (self.prompt, value))
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
        user_input = ''
        while True:
            user_input = raw_input(u"[To %s]: " % prompt)
            if valid(user_input):
                break

        if user_input:
            return user_input
        else:
            return default

    def is_listen(self):
        return self._is_listen

    def enable_listen(self):
        self._is_listen = True

    def disable_listen(self):
        self._is_listen = False


if __name__ == '__main__':
    import doctest

    doctest.testmod()
