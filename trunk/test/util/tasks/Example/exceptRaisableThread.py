#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

import threading
import inspect
import ctypes#ctypes是Python的外部函数库。
             # 它提供了C兼容的数据类型，并且允许调用动态链接库/共享库中的函数。
             # 它可以将这些库包装起来给Python使用。

def asyncThreadEventHandler(thread, excutionType):
    """
    线程中异步执行一些操作，例如：抛出错误，终止线程执行等。
    Raises an exception in the threads with id tid。
    使用ctypes.pythonapi.PyThreadState_SetAsyncExc()进行该操作。
    """
    #判断提供的参数是否正确。
    if thread is None or not isinstance(thread,threading.Thread):
        raise ValueError('You must provide a thread to get Id!')

    #判断当前thread是否存活。
    if not thread.isAlive():
        raise threading.ThreadError("the thread is not active")

    #执行的对象必须是类(继承自object)
    if not inspect.isclass(excutionType):
        raise TypeError("Only types can be raised (not instances)")
    try:

        tid=getThreadId(thread)
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
        #使用ctypes.pythonapi.PyThreadState_SetAsyncExc当前线程错误。
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
    except Exception, e:
        print e

        pass #


def getThreadId(thread,thread_id_mark="thread_id"):
    """
    取得当前线程的id。
    determines this (self's) thread id

    CAREFUL : this function is executed in the context of the caller
    thread, to get the identity of the thread represented by this
    instance.
    """
    #判断提供的参数是否正确。
    if thread is None or not isinstance(thread,threading.Thread):
        raise ValueError('You must provide a thread to get Id!')

    #判断当前thread是否存活。
    if not thread.isAlive():
        raise threading.ThreadError("the thread is not active")

    # TODO: in python 2.6, there's a simpler way to do : thread.ident
    if not thread.ident is None:
        return thread.ident

    # do we have it cached?
    if hasattr(thread, thread_id_mark):
        return getattr(thread,thread_id_mark)

    # no, look for it in the _active dict
    for tid, tobj in threading._active.items():
        if tobj is thread:
            setattr(thread,thread_id_mark,tid)
            return tid

    #如果都没找到，抛出错误
    raise AssertionError("could not determine the thread's id")
    pass # def getThreadId(thread,thread_id_mark="_thread_id")

def terminateThread(thread):
    """
    在其他线程中强制停止一个python线程。
    使用ctypes.pythonapi.PyThreadState_SetAsyncExc强制停止当前线程。
    Terminates a python thread from another thread.

    :rawParam thread: a threading.Thread instance
    """
    asyncThreadEventHandler(thread,SystemExit)
    pass # def terminateThread(thread)

class ThreadWithExc(threading.Thread):
    """A thread class that supports raising exception in the thread from
       another thread.
    """

    def run(self):
        # self.raiseException(NotImplementedError)
        for i in range(100):
            print i
            time.sleep(1)
        pass


    def raiseException(self, exceptionType):
        """
        线程内部抛出错误。
        Raises the given exception type in the context of this thread.

        If the thread is busy in a system call (time.sleep(),
        socket.accept(), ...), the exception is simply ignored.

        If you are sure that your exception should terminate the thread,
        one way to ensure that it works is:

            t = ThreadWithExc( ... )
            ...
            t.raiseException( SomeException )
            while t.isAlive():
                time.sleep( 0.1 )
                t.raiseException( SomeException )

        If the exception is to be caught by the thread, you need a way to
        check that your thread has caught it.

        CAREFUL : this function is executed in the context of the
        caller thread, to raise an excpetion in the context of the
        thread represented by this instance.
        """
        return asyncThreadEventHandler( getThreadId(self) , exceptionType )

    def terminate(self):
      """raises SystemExit in the context of the given thread, which should
      cause the thread to exit silently (unless caught)"""
      return  self.raiseException(SystemExit)

    def raiseNotImplementedError(self):
      """raises SystemExit in the context of the given thread, which should
      cause the thread to exit silently (unless caught)"""
      return self.raiseException(NotImplementedError )

if __name__ == '__main__':
    import time

    thread1=ThreadWithExc()
    try:
        thread1.start()
        time.sleep(3)

        res=thread1 .raiseNotImplementedError()
        print 'NotImplementedError result:', res
        res=thread1 .terminate()
        print  'SystemExit result:', res
    except Exception ,e:
        print e

    for i in range(30): #这里模仿当前线程的其他程序，说明子线程抛出错误后不影响后续执行
        print 'a-%d'%(i),i+1
        time .sleep(0.5)





