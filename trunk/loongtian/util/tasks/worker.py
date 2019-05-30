#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

useNvwaQueue = True

import time, datetime

if useNvwaQueue:
    import loongtian.util.tasks.queue as Queue
else:
    try:
        import Queue  # Python 2
    except ImportError:
        import queue as Queue  # Python 3
import sys
from threading import Thread
from multiprocessing import Process
from loongtian.util.tasks import WorkStateEnum
from loongtian.util.tasks.stateController import StateController
from loongtian.util.tasks.task import Task, WorkRequest
from loongtian.util.log.logger import logger
from loongtian.util.tasks.excptions import *


class ThreadWorker(Thread, StateController):
    """
    工作者的线程执行代理（是任务的真正执行者）。对threading.Thread的扩展类。
    1、使线程可以停止（stop）、暂停（pause）、恢复（restore）。
    2、并可进行停止前、暂停前及恢复前的处理（例如保存数据等）。
    3、支持由其他线程（进程）调用时抛出错误。
    供Worker内部使用，不必关注。
    后台线程，真正的工作线程，从请求队列(requestQueue)中获取work，
    并将执行后的结果添加到结果队列(resultQueue)。
    Background thread connected to the requests/results queues.

    A workmanager thread sits in the background and picks up work requests from
    one queue and puts the results in another until it is dismissed.

    """

    def __init__(self, workManager, ThreadName, id,
                 interval=0.001, poll_timeout=5, **kwds):
        # 初始化

        Thread.__init__(self, name=ThreadName, **kwds)
        StateController.__init__(self, ThreadName, id)

        self.__workManager = workManager
        if not workManager is None:  # 取得worker中的_requests_queue和_results_queue
            from loongtian.util.tasks.tasksManager import TasksManager
            if isinstance(workManager, TasksManager):
                self._taskQueue = workManager._taskQueue  # _taskQueue由worker提供
                self._resultQueue = workManager._resultQueue  # _resultQueue由worker提供
                self._taskDict = workManager._taskDict  # 工作项字典，与_taskQueue一样，但可以根据ID进行查询。由worker提供
            else:
                self._taskQueue = Queue.Queue()
                self._resultQueue = Queue.Queue()
                self._taskDict = {}  # 工作项字典，与_taskQueue一样，但可以根据ID进行查询。
        else:
            self._taskQueue = Queue.Queue()
            self._resultQueue = Queue.Queue()
            self._taskDict = {}  # 工作项字典，与_taskQueue一样，但可以根据ID进行查询。

        self.interval = interval
        self.loopCounter = 1
        self._poll_timeout = poll_timeout
        # 设置为守护进行，也就是线程随主线程一起结束，必须在start()之前调用。默认为False。
        self.setDaemon(True)

        # 原代码默认创建后即启动，不便于控制，所以注销掉
        # self.start()

    def run(self):  # Overwrite start() method, put what you want the thread do here
        """
        线程的真正执行部分。
        每个线程尽可能多的执行work，所以采用loop，
        只要线程可用，并且requestQueue有work未完成，则一直loop。
        Repeatedly process the job queue until told to exit.
        """
        # 设置线程状态
        self.workerStateInfos.setWorkerState(WorkStateEnum.Running)

        # 判断线程是否停止（stop）循环，如果没有停止，继续工作函数的代码逻辑，否则进行其他处理
        while not self._stopEvent.isSet() and not self._completeEvent.isSet():

            # 这里是线程的暂停处理
            if self._pauseEvent.isSet():
                # 带有暂停超时的处理
                if not self._pausedTimeOut is None:
                    # 休眠指定时间
                    time.sleep(self._pausedTimeOut)
                    # 恢复线程
                    self.restore()
                time.sleep(self.interval)  # 暂停1毫秒 防止空跑占用过高cpu
                # 如果线程暂停，不进入实际代码部分，继续空跑循环
                continue

            logger.debug(
                'Thread Object(%s),loopCounter：%d Time:%s' % (self.id, self.loopCounter, datetime.datetime.now()))
            self.loopCounter += 1

            # 这里需要判断是否传入了_requests_queue，如果没有，继续循环
            if not self._taskQueue:
                time.sleep(self.interval)  # 暂停1毫秒 防止空跑占用过高cpu
                # 如果_requests_queue为None，不进入实际代码部分，继续空跑循环
                continue

            # 以下才是我们的工作函数
            # 取得当前的工作请求（work request）
            _curTask = None
            try:
                # 从_requests_queue中取得下一个工作请求（work request），
                # 如果没有了，将继续下一个循环。
                # Queue.Queue队列设置了线程同步策略，并且可以设置timeout。
                # 可以一直block，直到requestQueue有值，或者超时
                _curTask = self._taskQueue.get(True, self._poll_timeout)
            except Queue.Empty:
                time.sleep(self.interval)  # 暂停1毫秒 防止空跑占用过高cpu
                continue
            except Exception as e:
                # 处理错误
                self.handleException(e)

            # 如果没有工作请求（work request），继续循环
            if _curTask is None:
                time.sleep(self.interval)  # 暂停1毫秒 防止空跑占用过高cpu
                continue

            # 之所以在这里再次判断stopped，是因为之前的timeout时间里，很有可能，该线程被stopped掉了
            if self._stopEvent.isSet():
                # 如果已经由外部进行了停止，则将工作请求（work request）放回队列，然后终止循环
                # we are dismissed, put back request in queue and exit loop
                self._taskQueue.put(_curTask)
                break

            if self.__workManager:
                # 增加正在执行操作的计数器
                self.__workManager.increase_workers_num()
                pass  # if not self.workmanager is None

            try:
                # 这里需要判断两种任务类型：Task或是Function
                if isinstance(_curTask, Task):
                    _curTask.worker = self
                    result = _curTask.start()
                    self._resultQueue.put((_curTask, result))
                    # for result in _curTask.start():
                    #     if result is not None:
                    #         self._taskQueue.put((_curTask, result))
                    #         logger.debug( 'result:%s'%(result))
                elif isinstance(_curTask, WorkRequest):
                    # 执行callable，讲请求和结果以tuple的方式放入requestQueue
                    result = _curTask.callable(*_curTask.args, **_curTask.kwds)
                    self._resultQueue.put((_curTask, result))
                    pass
            except:
                # 异常处理
                _curTask.exception = True
                exc_info = sys.exc_info()
                self._resultQueue.put((_curTask, exc_info))
                logger.debug(*exc_info)
                pass  # try

            if not self.__workManager is None:
                self.__workManager.decrease_workers_num()
                pass  # if not self.workmanager is None

                # # Stop if no workmanager is __workingWokerNum and queue is empty. It is
                # # reasonable because no new task can be generated at this point.
                # if (self.workmanager.__workingWokerNum == 0) \
                # and (self.workmanager._taskQueue.empty()):
                #     self.workmanager.stop()

            pass  # while not self._stopEvent.isSet()

        if not self._stopEvent.isSet():
            # 在线程主要代码跑完之后的处理程序
            self.handleAfterRunning()

        pass  # def start(self)

    def handleAfterRunning(self):
        """
        在线程主要代码跑完之后的处理程序。
        :return:
        """
        pass  # def handleAfterRunning(self)

    def addJob(self, job, block=True, timeout=None):
        """
        加入一个任务请求到工作队列。
        :parameter job 工作任务。包括两种Task、WorkRequest
        Put work job into work queue and save its id for later."""
        isTask = isinstance(job, Task)
        isWorkRequest = isinstance(job, WorkRequest)
        assert isTask or isWorkRequest
        # don't reuse old work requests
        assert not getattr(job, 'exception', None)
        # 当queue满了，也就是容量达到了前面设定的q_size,它将一直阻塞，直到有空余位置，或是timeout
        self._taskQueue.put(job, block, timeout)
        self._taskDict[job.id] = job

        pass  # def addJob(self, job, block=True, timeout=None)

    def poll(self, block=False):
        """
        处理队列中的新结果。也就是循环的调用各个线程结果中的回调和错误回调。
        不过，当请求队列为空时会抛出 NoResultPending 异常，以表示所有的结果都处理完了。
        这个特点对于依赖线程执行结果继续加入请求队列的方式不太适合。
        Process any new results in the queue.
        """
        while True:
            # still results pending?
            if not self._taskDict:
                raise NoResultsPending

            try:
                # 默认只要resultQueue有值，则取出，否则一直block
                # get back next results
                request, result = self._resultQueue.get(block=block)
                # has an exception occured?
                if request.exception and request.exc_callback:
                    request.exc_callback(request, result)
                # 处理外部调用的程序（callback）
                # hand results to callback, if any
                if request.callback and not \
                        (request.exception and request.exc_callback):
                    request.callback(request, result)
                del self._taskDict[request.id]

            except Queue.Empty:
                break

        pass  # def poll(self, block=False)

    def wait(self):
        """
        等待执行结果，直到所有任务完成。
        Wait for results, blocking until all have arrived."""
        while 1:
            try:
                self.poll(True)
            except NoResultsPending:
                break
        pass  # def wait(self)

    pass  # class ThreadWorker(Thread,StateController)


class ProcessWorker(Process, StateController):
    """
    工作者的进程执行代理（是任务的真正执行者）。
    """

    def __init__(self, worker, name=None):
        Process.__init__(self)
        self.queue = Queue.Queue()
        self.worker = worker
        if name is not None: self.name = name

        pass  # def __init__(self, workmanager, name=None)

    pass  # class ProcessWorker(Process)
