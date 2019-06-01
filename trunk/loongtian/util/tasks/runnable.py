#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
继承此类并重写_execute后可以抛入线程池执行
"""
__author__ = 'Leon'

import threading
import threadpool
import time
import traceback

# 默认的关闭线程的命令符
default_shutdown_commands=["--","exit","shutdown"]

class Runnable(object):
    """
    线程
    """
    pool = threadpool.ThreadPool(10)  # 线程池
    logger = None  # 日志 todo 尚未实现。

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
        """
        线程启动方法
        :return:
        """
        self._lock.acquire()
        self._state = True
        self._lock.release()
        self.__log("%s started" % self._name)
        try:
            self._execute()
        except Exception as ex:
            traceback.print_exc()
        self.__log("%s stopped" % self._name)

    def _execute(self):
        """
        该线程不执行任何操作，如果继承该类，需要重写此方法。
        :return:
        """
        while True:
            if not self.state():
                break
            # 停止线程并更改state=False状态。
            self.stop()

    def _start_sub_threads(self):
        map(lambda t: run(t), self._sub_threads)
        Runnable.pool.poll()

    def stop(self):
        """
        停止线程
        :return:
        """
        self.__log("%s stopping..." % self._name)
        if len(self._sub_threads) > 0:
            _start = time.time()
            self.__log("%s try stop sub threads" % self._name)
            # 停止其下的子线程
            map(lambda _t0: _t0.stop(), self._sub_threads)
            _end = time.time()
            # 等待并检测其子线程是否停止。
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
        ''' 线程状态
        :return 返回当前线程是否在运行[True, False]
        '''
        self._lock.acquire()
        __state = self._state
        self._lock.release()
        return __state


def print_wrapper(msg):
    '''
    打印线程信息
    '''

    print('\r\n-------- %s -------------\r\n' % (msg))


def handle_exception(request, exc_info):
    '''
    异常句柄处理
    '''
    if not isinstance(exc_info, tuple):
        # Something is seriously wrong...
        print (request)
        print (exc_info)
        raise SystemExit
    # print "**** Exception occured in request #%s: %s" % \
    # (request.requestID, exc_info)
    traceback.print_exception(*exc_info)


def run(runnable,*args,**kwargs):
    '''
    外部调用runnable函数
    '''
    try:
        requests = threadpool.makeRequests(lambda x: x.run(*args,**kwargs), [runnable], exc_callback=handle_exception)
        [Runnable.pool.putRequest(req) for req in requests]
    except Exception as ex:
        print (ex)


# todo 需要进一步考察。
def execute(func, obj):
    '''
    外部调用，给定对象和函数名称来调用。
    '''
    requests = threadpool.makeRequests(func, [obj], exc_callback=handle_exception)  # , exc_callback=__exceptionHandler)
    [Runnable.pool.putRequest(req) for req in requests]
