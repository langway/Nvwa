#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
继承此类并重写_execute后可以抛入线程池执行
>>> print("No Test")
No Test
"""
__author__ = 'Liuyl'
import threading
import threadpool


class Runnable(object):
    pool = threadpool.ThreadPool(10)
    logger = None

    def __init__(self):
        self._name = "runnable"
        self._lock = threading.Lock()
        self._lock.acquire()
        self._state = False
        self._lock.release()
        if Runnable.logger is not None:
            self.__log = Runnable.logger.info
        else:
            self.__log = printwrapper

    def run(self):
        self._lock.acquire()
        self._state = True
        self._lock.release()
        self.__log("%s start" % self._name)
        self._execute()
        self.__log("%s stop" % self._name)

    def _execute(self):
        while True:
            if not self.state():
                break
            self.stop()

    def stop(self):
        self.__log("%s stopping" % self._name)
        self._lock.acquire()
        self._state = False
        self._lock.release()

    def state(self):
        self._lock.acquire()
        __state = self._state
        self._lock.release()
        return __state


def printwrapper(msg):
    print(msg)


def run(runnable):
    requests = threadpool.makeRequests(lambda x: x.run(), [runnable])
    [Runnable.pool.putRequest(req) for req in requests]


if __name__ == '__main__':
    import doctest

    doctest.testmod()
