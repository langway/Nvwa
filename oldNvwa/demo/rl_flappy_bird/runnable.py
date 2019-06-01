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
import time
import traceback


class Runnable(object):
    pool = threadpool.ThreadPool(10)
    logger = None

    def __init__(self):
        self._name = "runnable"
        self._sub_threads = []
        self._lock = threading.Lock()
        self._lock.acquire()
        self._state = False
        self._lock.release()
        if Runnable.logger is not None:
            self.__log = Runnable.logger.info
        else:
            self.__log = print_wrapper

    def run(self):
        self._lock.acquire()
        self._state = True
        self._lock.release()
        self.__log("%s started" % self._name)
        try:
            self._execute()
        except:
            traceback.print_exc()
        self.__log("%s stopped" % self._name)

    def _execute(self):
        while True:
            if not self.state():
                break
            self.stop()

    def _start_sub_threads(self):
        map(lambda t: run(t), self._sub_threads)
        Runnable.pool.poll()

    def stop(self):
        self.__log("%s stopping..." % self._name)
        if len(self._sub_threads) > 0:
            _start = time.time()
            self.__log("%s try stop sub threads" % self._name)
            map(lambda _t0: _t0.stop(), self._sub_threads)
            _end = time.time()
            while True:
                if any([_t1.state() for _t1 in self._sub_threads]):
                    if _end - _start > 2:
                        self.__log("%s stop sub threads out recordTime" % self._name)
                        break
                else:
                    self.__log("%s stop sub threads using %f s" % (self._name, _end - _start))
                    break

        self._lock.acquire()
        self._state = False
        self._lock.release()

    def state(self):
        self._lock.acquire()
        __state = self._state
        self._lock.release()
        return __state


def print_wrapper(msg):
    print('-------- {0} -------------'.format(msg))


def handle_exception(request, exc_info):
    if not isinstance(exc_info, tuple):
        # Something is seriously wrong...
        print request
        print exc_info
        raise SystemExit
    # print "**** Exception occured in request #%s: %s" % \
    # (request.requestID, exc_info)
    traceback.print_exception(*exc_info)


def run(runnable):
    requests = threadpool.makeRequests(lambda x: x.run(), [runnable], exc_callback=handle_exception)  # )
    [Runnable.pool.putRequest(req) for req in requests]


def execute(func, obj):
    requests = threadpool.makeRequests(func, [obj], exc_callback=handle_exception)  # , exc_callback=__exceptionHandler)
    [Runnable.pool.putRequest(req) for req in requests]


if __name__ == '__main__':
    import doctest

    doctest.testmod()
