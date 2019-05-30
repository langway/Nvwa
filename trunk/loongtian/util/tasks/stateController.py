#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

useNvwaQueue = True

if useNvwaQueue:
    import loongtian.util.tasks.queue as Queue
else:
    try:
        import Queue  # Python 2
    except ImportError:
        import queue as Queue  # Python 3
import time, datetime
from threading import Event
import threading

from loongtian.util.log.logger import logger
from loongtian.util.tasks.workStateInfo import WorkStateRecordable
from loongtian.util.tasks import WorkStateEnum
import loongtian.util.helper.threadHelper  as threadHelper


class StateController(WorkStateRecordable):
    """
    WorkStateRecordable的扩展类，增加stop、pause和restore方法。
    使线程可以暂停（pause）、恢复（restore），并可进行暂停前及恢复前的处理（例如保存数据等）。"""

    def __init__(self, name, id):

        super(StateController, self).__init__(name, id)

        # 线程安全锁
        self._locker = threading.Lock()
        # 是否正在运行的标记
        self._isAlive = False


        # 外界暂停线程循环的标记
        self._pauseEvent = Event()
        # 外界指定的暂停线程后的恢复时间，这里的逻辑是：可以指定延时多长时间进行暂停操作，暂停之后，多长时间自动运行
        self._pausedTimeOut = None
        # 外界强制停止线程循环的标记，设置一个flag信号，用来表示该线程是否被stopped
        self._stopEvent = Event()
        # 继承类停止线程循环的标记，设置一个flag信号，用来表示该线程是否已经正常执行完毕，需要complete
        self._completeEvent = Event()
        # 错误队列
        self._exceptionQueue = Queue.Queue()

    def start(self):
        """
        开始当前工作。
        :return:
        """
        self._locker.acquire()
        self._isAlive = True
        self._locker.release()
        try:
            self._executeOnce()
            # 设置线程状态
            self.workerStateInfos.setWorkerState(WorkStateEnum.Running)
            logger.info("%s started" % self.id)
            self._executeCirculate()
        except:
            import traceback
            traceback.print_exc()
            self.stop()



    def _executeOnce(self):
        """
        [必须重写此方法]单次执行程序的入口。
        该线程不执行任何操作，如果继承该类，必须重写此方法。
        """
        raise NotImplementedError

        pass  # def _executeOnce(self)

    def _executeCirculate(self):
        """
        [必须重写此方法]循环执行程序的入口。
        该线程不执行任何操作，如果继承该类，必须重写此方法。
        """
        while True:
            if not self.isAlive():
                break
            # 停止线程并更改state=False状态。
            self.stop()


    def pause(self, TimeDelay=None, TimeOut=None):
        """
        暂停当前线程。
        这里的逻辑是：可以指定延时多长时间进行暂停操作，暂停之后，多长时间自动运行
        :rawParam TimeDelay 延时暂停。seconds（秒）
        :rawParam TimeOut:seconds（秒）。暂停指定时间后，可以继续运行。
        :return:
        """
        if TimeDelay:
            # 休眠指定时间
            time.sleep(TimeDelay)
        if TimeOut:
            # 计时开始
            timeStart = time.time()

        self._pausedTimeOut = TimeOut

        # 暂停之前的处理程序（例如保存数据等）。
        self._prePause()
        self._pauseEvent.set()

        # 设置线程状态
        self.workerStateInfos.setWorkerState(WorkStateEnum.Paused)

        if TimeOut:
            # 休眠指定时间
            time.sleep(TimeOut)
            # 恢复程序运行
            self.restore()

    def _prePause(self,TimeDelay=None, TimeOut=None):
        """
        暂停当前线程之前的处理程序（例如保存数据等）。
        (必须进行重载)。
        :return:
        """
        pass  # def prePause(self)

    def restore(self, TimeDelay=None):
        """
        暂停后恢复当前线程，继续执行当前线程的代码逻辑。
        :rawParam TimeDelay 延时恢复。seconds（秒）
        :return:
        """
        if TimeDelay:
            # 休眠指定时间
            time.sleep(TimeDelay)
        # 清空指定的暂停后的恢复时间
        self._pausedTimeOut = None
        # 设置线程状态
        self.workerStateInfos.setWorkerState(WorkStateEnum.Restarted)
        # 恢复之前的处理程序（例如读取数据等）。
        self._preRestore()

        self._pauseEvent.clear()
        logger.debug('%s Object(%s) Restored, Time:%s' % (self.__class__, self.id, datetime.datetime.now()))

    def _preRestore(self):
        """
        暂停后恢复当前线程之前的处理程序（例如从缓存中读取数据等）。
        (必须进行重载)。
        :return:
        """
        pass  # def preRestore(self)

    def sleep(self, seconds):
        """
        让当前worker休眠指定的时间（秒）
        """
        time.sleep(seconds)
        pass  # def sleep(self,seconds)

    def _complete(self):
        """
        正常执行完毕，需要退出(默认由系统执行，无需外部调用)。
        由继承类用来通知线程当前程序逻辑已经执行完毕，强制停止当前线程中的loop循环，退出当前线程。
        :return:
        """
        self._preComplete()
        self._completeEvent.set()
        # 设置线程状态
        self.workerStateInfos.setWorkerState(WorkStateEnum.Completed)

        logger.debug('%s Object(%s) completed, Time:%s' % (self.__class__, self.id, datetime.datetime.now()))
        # self.join()

        pass  # def stop(self)

    def _preComplete(self):
        """
        正常执行完毕，需要退出的前期调用(默认由系统执行，无需外部调用)。
        :return:
        """

        pass  # def preComplete(self)

    def stop(self):
        """
        强制停止当前线程中的loop循环，退出当前线程。数据会由用户进行处理，会比较安全。
        与terminate不同，如果中间还有已经启动的大型程序，将等待该大型程序结束，进入到下一次loop循环时才会停止。
        :return:
        """
        # 强制停止线程之前的处理程序。
        self._preStop()
        self._stopEvent.set()
        # 设置线程状态
        self.workerStateInfos.setWorkerState(WorkStateEnum.Stopped)
        logger.debug('%s Object(%s) Stopped, Time:%s' % (self.__class__, self.id, datetime.datetime.now()))

        # self.join()
        self._locker.acquire()
        self._isAlive = False
        self._locker.release()

        pass  # def stop(self)

    def terminate(self):
        """
        强制停止当前线程，退出当前线程。数据一般不会由用户进行处理，可能丢失数据
        与stop不同，如果中间还有已经启动的大型程序，不会等待该大型程序结束。
        raises SystemExit in the context of the given thread, which should
        cause the thread to exit silently (unless caught)
        """
        # 强制停止线程之前的处理程序。
        self._preStop()
        # 设置线程状态
        self.workerStateInfos.setWorkerState(WorkStateEnum.Terminated)
        return threadHelper.asyncThreadEventHandler(threadHelper.getThreadId(self), SystemExit)
        pass  # def terminate(self)

    def _preStop(self):
        """
        强制停止线程之前的处理程序。
        (必须进行重载)。
        :return:
        """
        pass  # def preStop(self)


    def isAlive(self):
        """
        线程状态
        :return 返回当前线程是否在运行[True, False]
        """
        self._locker.acquire()
        __state = self._isAlive
        self._locker.release()
        return __state
        pass  # def isAlive(self)

    def handleException(self, excption, raiseExcption=False):
        """
        错误处理程序。
        :rawParam excption: 要处理的错误
        :rawParam raiseExcption: 将终止线程执行，注意：尽量不要使用！
        :return:
        """
        # todo 要更多处理错误
        logger.exception(excption)
        # 记录错误到错误队列
        self._exceptionQueue.put(excption)

        if raiseExcption:
            self.raiseException(type(excption))

        pass  # def handleException(self,excption)

    def raiseException(self, exceptionType):
        """
        线程内部抛出错误(将终止线程执行)。
        注意：尽量不要使用！请使用def handleException(self,exception)
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
        # 强制停止线程之前的处理程序。
        self._preStop()
        # 设置线程状态
        self.workerStateInfos.setWorkerState(WorkStateEnum.Aborted)
        return threadHelper.asyncThreadEventHandler(threadHelper.getThreadId(self), exceptionType)
        pass  # def raiseException(self, exceptionType)

    pass  # class StateController(object)
