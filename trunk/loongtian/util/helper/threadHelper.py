#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

import threading, threadpool
import traceback
import inspect
import ctypes  # ctypes是Python的外部函数库。


# 它提供了C兼容的数据类型，并且允许调用动态链接库/共享库中的函数。
# 它可以将这些库包装起来给Python使用。

def exceptionHandler(request, exc_info):
    """
    异常句柄处理。
    默认的异常处理函数，只是简单的打印。
    """
    if not isinstance(exc_info, tuple):
        # Something is seriously wrong...
        print(request)
        print(exc_info)
        raise SystemExit
    # print "**** Exception occured in request #%s: %s" % \
    # (request.id, exc_info)
    traceback.print_exception(*exc_info)


def run(task, pool):
    """
    外部调用Task函数
    """
    from loongtian.util.tasks.task import Task
    from loongtian.util.tasks.tasksManager import TasksManager

    if task is None or not isinstance(task, Task):
        raise ValueError('You must provide a task to start!')
    if pool is None:
        raise ValueError('You must provide a pool to deposit the task!')

    requests = threadpool.makeRequests(lambda x: x.start(), [task], exc_callback=exceptionHandler)
    if pool is None:
        pool = TasksManager(10)

    if isinstance(pool, threadpool.ThreadPool):
        [pool.putRequest(req) for req in requests]
    elif isinstance(pool, TasksManager):
        [pool.addTask(req) for req in requests]


def execute(func, obj, pool):
    """
    外部调用，给定对象和函数名称来调用。
    """
    from loongtian.util.tasks.tasksManager import TasksManager

    requests = threadpool.makeRequests(func, [obj], exc_callback=exceptionHandler)  # , exc_callback=exceptionHandler)
    if pool is None:
        pool = TasksManager(10)
    if isinstance(pool, threadpool.ThreadPool):
        [pool.putRequest(req) for req in requests]
    elif isinstance(pool, TasksManager):
        [pool.addTask(req) for req in requests]


def asyncThreadEventHandler(thread, excutionType):
    """
    线程中异步执行一些操作，例如：抛出错误，终止线程执行等。
    Raises an exception in the threads with id tid。
    使用ctypes.pythonapi.PyThreadState_SetAsyncExc()进行该操作。
    """
    # 判断提供的参数是否正确。
    if thread is None or not isinstance(thread, threading.Thread):
        raise ValueError('You must provide a thread to get Id!')

    # 判断当前thread是否存活。
    if not thread.isAlive():
        raise threading.ThreadError("the thread is not active")

    # 执行的对象必须是类(继承自object)
    if not inspect.isclass(excutionType):
        raise TypeError("Only types can be raised (not instances)")
    try:

        tid = getThreadId(thread)
        """
        Initialization, Finalization, and Threads — Python 2.7.11rc1 documentation
        参考：https://docs.python.org/2/c-api/init.html?highlight=pythreadstate_setasyncexc#c.PyThreadState_SetAsyncExc
        int PyThreadState_SetAsyncExc(long id, PyObject *exc)
        Asynchronously raise an exception in a thread.
        The id argument is the thread id of the target thread;
        exc is the exception object to be raised.
        This function does not steal any references to exc.
        To prevent naive misuse, you must write your own C extension to call this.
        Must be called with the GIL held.
        Returns the number of thread states modified;
        this is normally one, but will be zero if the thread id isn’t found.
        If exc is NULL, the pending exception (if any) for the thread is cleared.
        This raises no exceptions.
        New in version 2.3.
        """
        # 使用ctypes.pythonapi.PyThreadState_SetAsyncExc当前线程错误。
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid,
                                                         ctypes.py_object(excutionType))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            # "if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, 0)
            raise SystemError("PyThreadState_SetAsyncExc failed")
        return res
    except Exception as e:
        print (e)

        pass  #


def getThreadId(thread, thread_id_mark="id"):
    """
    取得当前线程的id。
    determines this (self's) thread id

    CAREFUL : this function is executed in the context of the caller
    thread, to get the identity of the thread represented by this
    instance.
    """
    # 判断提供的参数是否正确。
    if thread is None or not isinstance(thread, threading.Thread):
        raise ValueError('You must provide a thread to get Id!')

    # 判断当前thread是否存活。
    if not thread.isAlive():
        raise threading.ThreadError("the thread is not active")

    # do we have it cached?
    if hasattr(thread, thread_id_mark):
        return getattr(thread, thread_id_mark)
    elif not thread.ident is None:
        return thread.ident
    else:
        # no, look for it in the _active dict
        for tid, tobj in threading._active.items():
            if tobj is thread:
                setattr(thread, thread_id_mark, tid)
                return tid

    # 如果都没找到，抛出错误
    raise AssertionError("could not determine the thread's id")
    pass  # def getThreadId(thread,thread_id_mark="_thread_id")


def terminateThread(thread):
    """
    在其他线程中强制停止一个python线程。
    使用ctypes.pythonapi.PyThreadState_SetAsyncExc强制停止当前线程。
    Terminates a python thread from another thread.

    :rawParam thread: a threading.Thread instance
    """
    asyncThreadEventHandler(thread, SystemExit)
    pass  # def terminateThread(thread)


def exc_callback(excinfo):
    """
    由于发生异常时返回的 sys.exc_info() 内容并不易读，
    所以可以用如下方式定制错误回调函数，将错误信息打印出来，或者可选的输出到日志文件。
    :rawParam excinfo:
    :return:
    """
    errorstr = ''.join(traceback.format_exception(*excinfo))
    print(errorstr)


def startThread(args, func, threadNum):
    import Queue
    __q = Queue.Queue()
    __t = []
    for arg in args:
        __q.put(arg)
    for i in range(threadNum):
        __t.append(threading.Thread(target=func, args=(__q,)))
    for i in range(threadNum):
        __t[i].setDaemon(True)
        __t[i].start()
    for i in range(threadNum):
        __t[i].join(timeout=10)
