#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

useNvwaQueue = True

import threading, time

if useNvwaQueue:
    import loongtian.util.tasks.queue as Queue
else:
    try:
        import Queue  # Python 2
    except ImportError:
        import queue as Queue  # Python 3

from loongtian.util.tasks.worker import ThreadWorker
from loongtian.util.tasks.task import Task,WorkRequest
from loongtian.util.tasks.stateController import StateController
from loongtian.util.tasks.excptions import *


class TasksManager(StateController):
    """
    多任务的执行者。
    线程池类的扩展，发布工作请求并收集结果。
    :rawParam workers_num:初始化的线程数量
    :rawParam q_size,resq_size: requestQueue和resultQueue队列的初始大小
    :rawParam __result_poll_timeout: 设置工作线程WorkerThread的timeout，也就是等待requestQueue的timeout
    A thread pool, distributing work requests and collecting results.

    See the module docstring for more information.
    Notes:
    一、线程池的原理：
        线程池是预先创建线程的一种技术。
        线程池在还没有任务到来之前，创建一定数量的线程，放入空闲队列中。
        这些线程都是处于睡眠状态，即均为启动，不消耗CPU，而只是占用较小的内存空间。
        当请求到来之后，缓冲池给这次请求分配一个空闲线程，把请求传入此线程中运行，进行处理。
        当预先创建的线程都处于运行状态，即预制线程不够，线程池可以自由创建一定数量的新线程，
        用于处理更多的请求。当系统比较闲的时候，也可以通过移除一部分一直处于停用状态的线程。

    二、线程池管理器的机制：
        线程池管理器，通过添加请求的方法（addJob）向请求队列（RequestQueue）添加请求，
        这些请求事先需要实现请求接口，即传递工作函数、参数、结果处理函数、以及异常处理函数。
        之后初始化一定数量的工作线程，这些线程通过轮询的方式不断查看请求队列（RequestQueue），
        只要有请求存在，则会提取出请求，进行执行。
        然后，线程池管理器调用方法（poll）查看结果队列（resultQueue）是否有值，
        如果有值，则取出，调用结果处理函数执行。
        不难发现，这个系统的核心资源在于请求队列和结果队列，
        工作线程通过轮询requestQueue获得人物，主线程通过查看结果队列，获得执行结果。
        因此，对这个队列的设计，要实现线程同步，以及一定阻塞和超时机制的设计，
        以防止因为不断轮询而导致的过多cpu开销。

    三、简单线程池的设计

        一个典型的线程池，应该包括如下几个部分：
        1、线程池管理器（WorkManager），用于启动、停用，管理线程池
        2、工作线程（WorkThread），线程池中的线程
        3、请求接口（WorkRequest），创建请求对象，以供工作线程调度任务的执行
        4、请求队列（RequestQueue）,用于存放和提取请求
        5、结果队列（ResultQueue）,用于存储请求执行后返回的结果

    四、线程池的注意事项
        虽然线程池是构建多线程应用程序的强大机制，但使用它并不是没有风险的。
        在使用线程池时需注意线程池大小与性能的关系，注意并发风险、死锁、资源不足和线程泄漏等问题。

        （1）线程池大小。多线程应用并非线程越多越好，需要根据系统运行的软硬件环境以及应用本身的特点决定线程池的大小。一般来说，如果代码结构合理的话，线程数目与CPU 数量相适合即可。如果线程运行时可能出现阻塞现象，可相应增加池的大小；如有必要可采用自适应算法来动态调整线程池的大小，以提高CPU 的有效利用率和系统的整体性能。

        （2）并发错误。多线程应用要特别注意并发错误，要从逻辑上保证程序的正确性，注意避免死锁现象的发生。

        （3）线程泄漏。这是线程池应用中一个严重的问题，当任务执行完毕而线程没能返回池中就会发生线程泄漏现象。

    五、Python的多线程问题:

        python 的GIL规定每个时刻只能有一个线程访问python虚拟机，
        所以你要用python的多线程来做计算是很不合算的，
        但是对于IO密集型的应用，例如网络交互来说，python的多线程还是非常给力的。
        如果你是一个计算密集型的任务，非要用python来并行执行的话，有以下几个方法：
        1 使用python的multiprocessing 模块，能够发挥多核的优势。
        2 使用ironPython，但是这个只能在windows下用
        3 使用pypy，这个可以实现真正的多线程。
    """

    def __init__(self, workers_num=10, name=None, id=None,
                 taskQueue_size=0, resultQueue_size=0, result_poll_timeout=5,
                 auto_start=True):
        """
        构造函数，设置线程池工作线程数量和最大任务队列长度。
        :parameter workers_num 是初始化时的线程数量。
        :parameter taskQueue_size 工作请求（Task、WorkRequest）的队列的数量，超过该数量，后进入的工作请求将被阻塞。
        如果 q_size>0 则会限制工作队列的长度，并且在工作队列满时阻塞继续插入工作请求的任务。
        :parameter resultQueue_size 执行结果的队列的数量，超过该数量，后进入的工作结果将被阻塞。
        :parameter result_poll_timeout 提取结果的超时设置
        :parameter auto_start 是否自动开始运行所有线程。

        Set up the thread pool and start __workers_num workmanager threads.
        ``__workers_num`` is the number of workmanager threads to start initially.

        If ``q_size > 0`` the size of the work *request queue* is limited and
        the thread pool blocks when the queue is full and it tries to put
        more work requests in it (see ``addJob`` method), unless you also
        use a positive ``timeout`` value for ``addJob``.

        If ``resq_size > 0`` the size of the *results queue* is limited and the
        workmanager threads will block when the queue is full and they try to put
        new results in it.

        .. warning:
            If you set both ``q_size`` and ``resq_size`` to ``!= 0`` there is
            the possibilty of a deadlock, when the results queue is not pulled
            regularly and too many jobs are put in the work requests queue.
            To prevent this, always set ``timeout > 0`` when calling
            ``WorkManager.addJob()`` and catch ``Queue.Full`` exceptions.

        """
        super(TasksManager, self).__init__(name, id)

        self._taskQueue = Queue.Queue(taskQueue_size)
        self._resultQueue = Queue.Queue(resultQueue_size)
        self._taskDict = {}  # 工作项字典，与_taskQueue一样，但可以根据ID进行查询，方便使用和管理
        self.__lock = threading.Lock()  # 线程锁

        self.__threadWorkers = []  # 已经创建的线程代理。
        self.__dismissedWorkers = []  # 已经停止的线程代理。
        self.__pausedThreadWorkers = []  # 已经暂停的线程代理。

        # 是否已根据num_threadWorkers创建指定数量的线程代理
        self.__workers_num = workers_num
        self.__result_poll_timeout = result_poll_timeout
        self.__auto_start = auto_start
        self.__threadWorkersCreated = False
        self.__workingWokerNum = 0  # 正在执行的线程

        if self.__auto_start:  # 如果是自动执行，执行之。
            self.start()

        pass  # def __init__(self, workers_num, taskQueue_size=0, resultQueue_size=0, result_poll_timeout=5,auto_start=True)

    @property
    def lock(self):
        return self.__lock

    def increase_workers_num(self):
        """
        增加正在执行操作的计数器
        :return:
        """
        self.__lock.acquire()
        self.__workers_num += 1
        self.__lock.release()

    def decrease_workers_num(self):
        """
        增加正在执行操作的计数器
        :return:
        """
        self.__lock.acquire()
        self.__workers_num -= 1
        self.__lock.release()


    """
    以下为当前workManager的操作（调用线程、进程、远程操作等）。
    """

    def start(self):
        """
        开始当前工作。
        :return:
        """
        if self.__threadWorkersCreated == False:
            # 根据num_threadWorkers创建指定数量的线程代理
            self.createThreadWorkers(self.__workers_num, self.__result_poll_timeout, False)
        self.startThreadWorkers()
        # pass def start(self)

    def addTask(self, task, block=True, timeout=None):
        """
        加入一个任务请求到工作队列。
        Put work request into work queue and save its id for later.
        :param task: Task或WorkRequest
        :param block:
        :param timeout:
        :return:
        """
        assert isinstance(task, Task) or isinstance(task, WorkRequest)
        # don't reuse old work requests
        assert not getattr(task, 'exception', None)
        task.workmanager = self
        # 当queue满了，也就是容量达到了前面设定的q_size,它将一直阻塞，直到有空余位置，或是timeout
        self._taskQueue.put(task, block, timeout)
        if getattr(task, "id") is None:
            import uuid
            setattr(task, "id", uuid.uuid1())
            self._taskDict[task.id] = task
        else:
            self._taskDict[task.id] = task
        pass  # def addJob(self, request, block=True, timeout=None)

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
            # are there still __threadWorkers to process remaining requests?
            elif block and not self.__threadWorkers:
                raise NoDelegatorsAvailable
            try:
                # 默认只要resultQueue有值，则取出，否则一直block
                # get back next results
                request, result = self._resultQueue.get(block=block)
                # has an exception occured?
                if request.exception and request.exc_callback:
                    request.exc_callback(request, result)
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
        阻塞外部调用，等待执行结果，直到所有任务完成。
        Wait for results, blocking until all have arrived."""
        while 1:
            try:
                self.poll(True)
            except NoResultsPending:
                break
        pass  # def wait(self)

    def sleep(self, seconds):
        """
        让当前worker休眠指定的时间（秒）
        """
        time.sleep(seconds)
        pass  # def sleep(self,seconds)

    def stop(self, do_join=True):
        """
        停止并join 所有的thread,确保所有的线程都执行完毕
        """
        super(TasksManager, self).stop()
        self.stopThreadWorkers(len(self.__threadWorkers))
        if do_join:
            self.joinAllDismissedThreadWorkers()
        pass  # def stop(self, do_join=True)

    def pause(self, TimeDelay=None, TimeOut=None):
        """
        暂停当前所有的线程、进程操作。
        """
        super(TasksManager, self).pause(TimeOut)
        if self._pauseEvent.is_set:
            self.pauseThreadWorkers()
        pass  # def pause(self, TimeOut = None)

    def resotre(self, TimeDelay=None):
        """
        恢复已暂停的当前所有的线程、进程操作。
        """
        if not self._pauseEvent.is_set:
            return
        super(TasksManager, self).restore(TimeDelay)
        self.restoreThreadWorkers()
        pass  # def resotre(self, TimeDelay = None)

    """
    以下为worker对线程的操作。
    """

    def createThreadWorkers(self, num_threadWorkers, poll_timeout=5, autostart=False):
        """
        创建num_workers个WorkThread,默认timeout为5
        Add __workers_num workmanager threads to the pool.

        ``poll_timout`` sets the interval in seconds (int or float) for how
        often threads should check whether they are dismissed, while waiting for
        requests.
        :parameter autostart 是否在创建线程代理的同时就启动它（默认为True）

        """
        start = len(self.__threadWorkers)
        for i in range(start, num_threadWorkers + start):
            # 创建线程代理，指定其worker为当前Worker
            _threadWorker = ThreadWorker(self, None, i, poll_timeout=poll_timeout)
            self.__threadWorkers.append(_threadWorker)
            if autostart:
                # 启动线程
                _threadWorker.start()
        pass  # def createThreadWorkers(self, __workers_num, __result_poll_timeout=5,autostart=True)

    def threadWorkerSize(self):
        """
        当前worker的所有线程的数量。
        :return:
        """
        return len(self.__threadWorkers)
        pass  # def threadWorkerSize(self)

    def startThreadWorkers(self):
        """
        开始运行所有线程。
        :return:
        """
        for _threadWorker in self.__threadWorkers:
            # 启动线程
            _threadWorker.start()
        # map(lambda t: t.start(), self.__threadWorkers)
        pass  # def startThreadWorkers(self)

    def stopThreadWorkers(self, num_threadWorkers=0):
        """
        停用num_workers数量的线程，并加入dismiss_list。
        Tell __workers_num workmanager threads to quit after their current task."""
        totalNum = len(self.__threadWorkers)
        if num_threadWorkers == 0:
            num_threadWorkers = totalNum
        for i in range(min(num_threadWorkers, totalNum)):
            _threadWorker = self.__threadWorkers.pop()
            if _threadWorker.isAlive():
                _threadWorker.stop()
                self.__dismissedWorkers.append(_threadWorker)
        pass  # def stopThreadWorkers(self, __workers_num)

    def pauseThreadWorkers(self, num_threadWorkers=0):
        """
        暂停num_workers数量的线程。
        如果num_threadWorkers==0，将暂停所有线程。
        Tell __workers_num workmanager threads to quit after their current task."""
        totalNum = len(self.__threadWorkers)
        if num_threadWorkers == 0:
            num_threadWorkers = totalNum
        num_threadWorkers = min(num_threadWorkers, totalNum)

        for _threadWorker in self.__threadWorkers:
            if num_threadWorkers > 0 and _threadWorker.isAlive:
                _threadWorker.pause()
                self.__pausedThreadWorkers.append(_threadWorker)
                num_threadWorkers -= 1

        pass  # def pauseThreadWorkers(self, __workers_num)

    def restoreThreadWorkers(self, num_workers=0):
        """
        重启num_workers数量的线程。
        如果num_threadWorkers==0，将暂停所有线程。
        Tell __workers_num workmanager threads to quit after their current task."""
        totalNum = len(self.__threadWorkers)
        if num_workers == 0:
            num_workers = totalNum
        for _threadWorker in self.__pausedThreadWorkers:
            if _threadWorker.isAlive:
                _threadWorker.restore()
                self.__pausedThreadWorkers.remove(_threadWorker)
        pass  # def pauseThreadWorkers(self, __workers_num)

    def joinAllDismissedThreadWorkers(self):
        """
        join 所有停用的thread
        Perform Thread.join() on all workmanager threads that have been dismissed.
        """
        for worker in self.__dismissedWorkers:
            worker.join()
        self.__dismissedWorkers = []
        pass  # def joinAllDismissedThreadWorkers(self)

    def getThreadWorkersStates(self):
        """
        取得所有线程内Worker的状态。
        :return:
        """

        from loongtian.util.tasks import WorkStateEnum
        states = {}
        for curthread in self.__threadWorkers:
            states[curthread.id] =WorkStateEnum.getName(curthread.workerStateInfos.getCurrentWorkerState())

