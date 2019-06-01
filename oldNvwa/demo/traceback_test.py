#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    traceback_test 
Author:   Liuyl 
DateTime: 2014/10/9 9:23 
UpdateLog:
1、Liuyl 2014/10/9 Create this File.

traceback_test
>>> print("No Test")
No Test
"""
__author__ = 'Liuyl'
from loongtian.nvwa.common.threadpool.runnable import run, Runnable
import traceback


class MainThread(Runnable):
    def __init__(self):
        super(MainThread, self).__init__()
        self._name = "MainThread"

    def _execute(self):
        raise IOError


if __name__ == '__main__':
    main_thread1 = MainThread()
    main_thread2 = MainThread()
    run(main_thread1)
    run(main_thread2)
    Runnable.pool.wait()