#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""Easy to use object-oriented thread pool framework.

A thread pool is an object that maintains a pool of workmanager threads to perform
time consuming operations in parallel. It assigns jobs to the threads
by putting them in a work request queue, where they are picked up by the
next available thread. This then performs the requested operation in the
background and puts the results in another queue.

The thread pool object can then collect the results from all threads from
this queue as soon as they become available or after all threads have
finished their work. It's also possible, to define callbacks to handle
each result as it comes in.

The basic concept and some code was taken from the book "Python in a Nutshell,
2nd edition" by Alex Martelli, O'Reilly 2006, ISBN 0-596-10046-9, from section
14.5 "Threaded Program Architecture". I wrapped the main program logic in the
ThreadPool class, added the WorkRequest class and the callback system and
tweaked the code here and there. Kudos also to Florent Aide for the exception
handling mechanism.

Basic usage::

    >>> pool = ThreadPool(poolsize)
    >>> requests = makeRequests(some_callable, list_of_args, callback)
    >>> [pool.addTask(req) for req in requests]
    >>> pool.wait()
    可见使用步骤如下：

        建立线程池对象，其实是个线程管理器
        建立计算任务对象Request
        将计算任务对象放入线程池当中
        等待计算完成

See the end of the module code for a brief, annotated usage example.

Website : http://chrisarndt.de/projects/threadpool/

"""
__docformat__ = "restructuredtext en"

__all__ = [
    'makeRequests',
    'NoResultsPending',
    'NoWorkersAvailable',
    'ThreadPool',
    'WorkRequest',
    'ThreadDelegator'
]

__author__ = "Christopher Arndt"
__version__ = '1.3.2'
__license__ = "MIT license"


# standard library modules
import sys
import threading

import loongtian.util.helper.threadHelper  as threadHelper

try:
    import Queue            # Python 2
except ImportError:
    import queue as Queue   # Python 3


# exceptions
# 定义一些Exception，用于自定义异常处理
class NoResultsPending(Exception):
    """All work requests have been processed."""
    pass

class NoWorkersAvailable(Exception):
    """No workmanager threads available to process remaining requests."""
    pass


# internal module helper functions


# utility functions
def makeRequests(callable_, args_list, callback=None,
        exc_callback= threadHelper.exceptionHandler):
    """
    创建多个计算请求，并允许有不同的参数。
    参数列表中的每一个元素是两个元素的元组，分别是位置参数列表和关键字参数字典。
    Create several work requests for same callable with different arguments.

    Convenience function for creating several work requests for the same
    callable where each invocation of the callable receives different values
    for its arguments.

    ``args_list`` contains the parameters for each invocation of callable.
    Each item in ``args_list`` should be either a 2-item tuple of the list of
    positional arguments and a dictionary of keyword arguments or a single,
    non-tuple argument.

    See docstring for ``WorkRequest`` for info on ``callback`` and
    ``exc_callback``.

    """
    requests = []
    for item in args_list:
        if isinstance(item, tuple):
            requests.append(
                WorkRequest(callable_, item[0], item[1], callback=callback,
                    exc_callback=exc_callback)
            )
        else:
            requests.append(
                WorkRequest(callable_, [item], None, callback=callback,
                    exc_callback=exc_callback)
            )
    return requests


# classes
class ThreadDelegator(threading.Thread):
    """
    工作者的线程执行代理（是任务的真正执行者）。供Worker内部使用，不必关注。
    后台线程，真正的工作线程，从请求队列(requestQueue)中获取work，
    并将执行后的结果添加到结果队列(resultQueue)。
    Background thread connected to the requests/results queues.

    A workmanager thread sits in the background and picks up work requests from
    one queue and puts the results in another until it is dismissed.

    """

    def __init__(self, requests_queue, results_queue, poll_timeout=5, **kwds):
        """
        :parameter requestQueue 从请求队列(requestQueue)中获取work。
        :parameter resultQueue 将执行后的结果添加到结果队列(resultQueue)
        Set up thread in daemonic mode and start it immediatedly.

        ``requests_queue`` and ``results_queue`` are instances of
        ``Queue.Queue`` passed by the ``ThreadPool`` class when it creates a
        new workmanager thread.

        """
        threading.Thread.__init__(self, **kwds)
        #设置为守护进行
        self.setDaemon(1)
        self._requests_queue = requests_queue
        self._results_queue = results_queue
        self._poll_timeout = poll_timeout
        #设置一个flag信号，用来表示该线程是否还被dismiss,默认为false
        self._dismissed = threading.Event()
        self.start()

    def run(self):
        """
        线程的真正执行部分。
        每个线程尽可能多的执行work，所以采用loop，
        只要线程可用，并且requestQueue有work未完成，则一直loop。
        Repeatedly process the job queue until told to exit."""
        while True:
            if self._dismissed.isSet():
                # we are dismissed, break out of loop
                break
            # get next work request. If we don't get a new request from the
            # queue after self._poll_timout seconds, we jump to the start of
            # the while loop again, to give the thread a chance to exit.
            try:
                # Queue.Queue队列设置了线程同步策略，并且可以设置timeout。
                # 一直block，直到requestQueue有值，或者超时
                request = self._requests_queue.get(True, self._poll_timeout)
            except Queue.Empty:
                continue
            else:
                # 之所以在这里再次判断dimissed，是因为之前的timeout时间里，很有可能，该线程被dismiss掉了
                if self._dismissed.isSet():
                    # we are dismissed, put back request in queue and exit loop
                    self._requests_queue.put(request)
                    break
                try:
                    # 执行callable，讲请求和结果以tuple的方式放入requestQueue
                    result = request.callable(*request.args, **request.kwds)
                    self._results_queue.put((request, result))
                except:
                    # 异常处理
                    request.exception = True
                    self._results_queue.put((request, sys.exc_info()))

    def dismiss(self):
        """
        设置一个标志，表示完成当前work之后，退出。
        Sets a flag to tell the thread to exit when done with current job.
        """
        self._dismissed.set()


class WorkRequest:
    """
    外部函数的代理程序，通过WorkRequest，执行该外部函数。
    :parameter callable_:，可定制的，执行work的函数
    :parameter args: 列表参数
    :parameter kwds: 字典参数
    :parameter id: id
    :parameter callback: 可定制的，处理resultQueue队列元素的函数
    :parameter exc_callback:可定制的，处理异常的函数
    建立任务请求时有两种回调函数 callback 和 exc_callback ，他们的回调接口为:
    callback(request,result)
    exc_callback(request,sys.exc_info())
    其中 request 为 WorkRequest 对象。而 result 则是调用线程函数正确的返回结果。 sys.exc_info() 为发生异常时返回的信息。 sys.exc_info() 是一个拥有3个元素的元组。分别为：

    异常类 ：发生异常的类
    异常实例 ：如上异常类的实例，包含更多详细信息
    跟踪信息 ：traceback对象，可以显示错误的行号等等具体的错误信息
    注意：如果没有设置 exc_callback 则发生异常时会将异常信息写入 callback 回调函数。如果同时没有设置 callback 和 exc_callback 则发生任何异常都不会有提示，根本无法调试。

    A request to execute a callable for putting in the request queue later.

    See the module function ``makeRequests`` for the common case
    where you want to build several ``WorkRequest`` objects for the same
    callable but with different arguments for each call.

    """

    def __init__(self, callable_, args=None, kwds=None, requestID=None,
            callback=None, exc_callback= threadHelper.exceptionHandler):
        """Create a work request for a callable and attach callbacks.

        A work request consists of the a callable to be executed by a
        workmanager thread, a list of positional arguments, a dictionary
        of keyword arguments.

        A ``callback`` function can be specified, that is called when the
        results of the request are picked up from the result queue. It must
        accept two anonymous arguments, the ``WorkRequest`` object and the
        results of the callable, in that order. If you want to pass additional
        information to the callback, just stick it on the request object.

        You can also give custom callback for when an exception occurs with
        the ``exc_callback`` keyword parameter. It should also accept two
        anonymous arguments, the ``WorkRequest`` and a tuple with the exception
        details as returned by ``sys.exc_info()``. The default implementation
        of this callback just prints the exception info via
        ``traceback.print_exception``. If you want no exception handler
        callback, just pass in ``None``.

        ``id``, if given, must be hashable since it is used by
        ``ThreadPool`` object to store the results of that work request in a
        dictionary. It defaults to the return value of ``id(self)``.

        """
        if requestID is None:
            self.requestID = id(self)
        else:
            try:
                self.requestID = hash(requestID)
            except TypeError:
                raise TypeError("id must be hashable.")
        self.exception = False
        self.callback = callback
        self.exc_callback = exc_callback
        self.callable = callable_
        self.args = args or []
        self.kwds = kwds or {}

    def __str__(self):
        return "<WorkRequest id=%s args=%r kwargs=%r exception=%s>" % \
            (self.requestID, self.args, self.kwds, self.exception)

class ThreadPool:
    """
    线程池类，发布工作请求并收集结果。
    @rawParam num_workers:初始化的线程数量
    @rawParam q_size,resq_size: requestQueue和result队列的初始大小
    @rawParam poll_timeout: 设置工作线程WorkerThread的timeout，也就是等待requestQueue的timeout
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
        1、线程池管理器（ThreadPool），用于启动、停用，管理线程池
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

    def __init__(self, num_workers, q_size=0, resq_size=0, poll_timeout=5):
        """
        构造函数，设置线程池工作线程数量和最大任务队列长度。
        __workers_num 是初始化时的线程数量。
        如果 q_size>0 则会限制工作队列的长度，并且在工作队列满时阻塞继续插入工作请求的任务。
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
            ``ThreadPool.addJob()`` and catch ``Queue.Full`` exceptions.

        """
        self._requests_queue = Queue.Queue(q_size)
        self._results_queue = Queue.Queue(resq_size)
        self.workers = []
        self.dismissedWorkers = []
        self.workRequests = {}#设置个字典，方便使用
        self.createWorkers(num_workers, poll_timeout)

    def createWorkers(self, num_workers, poll_timeout=5):
        """
        创建num_workers个WorkThread,默认timeout为5
        Add __workers_num workmanager threads to the pool.

        ``poll_timout`` sets the interval in seconds (int or float) for how
        often threads should check whether they are dismissed, while waiting for
        requests.

        """
        for i in range(num_workers):
            self.workers.append(ThreadDelegator(self._requests_queue,
                self._results_queue, poll_timeout=poll_timeout))

    def dismissWorkers(self, num_workers, do_join=False):
        """
        停用num_workers数量的线程，并加入dismiss_list。
        Tell __workers_num workmanager threads to quit after their current task."""
        dismiss_list = []
        for i in range(min(num_workers, len(self.workers))):
            worker = self.workers.pop()
            worker.dismiss()
            dismiss_list.append(worker)

        if do_join:
            for worker in dismiss_list:
                worker.join()
        else:
            self.dismissedWorkers.extend(dismiss_list)

    def joinAllDismissedWorkers(self):
        """
        join 所有停用的thread
        Perform Thread.join() on all workmanager threads that have been dismissed.
        """
        for worker in self.dismissedWorkers:
            worker.join()
        self.dismissedWorkers = []

    def putRequest(self, request, block=True, timeout=None):
        """
        加入一个任务请求到工作队列。
        Put work request into work queue and save its id for later."""
        assert isinstance(request, WorkRequest)
        # don't reuse old work requests
        assert not getattr(request, 'exception', None)
        # 当queue满了，也就是容量达到了前面设定的q_size,它将一直阻塞，直到有空余位置，或是timeout
        self._requests_queue.put(request, block, timeout)
        self.workRequests[request.requestID] = request

    def poll(self, block=False):
        """
        处理队列中的新结果。也就是循环的调用各个线程结果中的回调和错误回调。
        不过，当请求队列为空时会抛出 NoResultPending 异常，以表示所有的结果都处理完了。
        这个特点对于依赖线程执行结果继续加入请求队列的方式不太适合。
        Process any new results in the queue.
        """
        while True:
            # still results pending?
            if not self.workRequests:
                raise NoResultsPending
            # are there still workers to process remaining requests?
            elif block and not self.workers:
                raise NoWorkersAvailable
            try:
                # 默认只要resultQueue有值，则取出，否则一直block
                # get back next results
                request, result = self._results_queue.get(block=block)
                # has an exception occured?
                if request.exception and request.exc_callback:
                    request.exc_callback(request, result)
                # hand results to callback, if any
                if request.callback and not \
                       (request.exception and request.exc_callback):
                    request.callback(request, result)
                del self.workRequests[request.requestID]
            except Queue.Empty:
                break

    def wait(self):
        """
        等待执行结果，直到所有任务完成。
        Wait for results, blocking until all have arrived."""
        while 1:
            try:
                self.poll(True)
            except NoResultsPending:
                break

    def workersize(self):
        return len(self.workers)

    def stop(self):
        """join 所有的thread,确保所有的线程都执行完毕"""
        self.dismissWorkers(self.workersize(),True)
        self.joinAllDismissedWorkers()


################
# USAGE EXAMPLE
################

if __name__ == '__main__':
    import random
    import time,datetime

    # # the work the threads will have to do (rather trivial in our example)
    # def do_something(data):
    #     time.sleep(random.randint(1,5))
    #     result = round(random.random() * data, 5)
    #     # just to show off, we throw an exception once in a while
    #     if result > 5:
    #         raise RuntimeError("Something extraordinary happened!")
    #     return result
    #
    # # this will be called each time a result is available
    # def print_result(request, result):
    #     print("**** Result from request #%s: %r" % (request.requestID, result))
    #
    # # this will be called when an exception occurs within a thread
    # # this example exception handler does little more than the default handler
    # def handle_exception(request, exc_info):
    #     if not isinstance(exc_info, tuple):
    #         # Something is seriously wrong...
    #         print(request)
    #         print(exc_info)
    #         raise SystemExit
    #     print("**** Exception occured in request #%s: %s" % \
    #       (request.requestID, exc_info))
    #
    # # assemble the arguments for each job to a list...
    # data = [random.randint(1,10) for i in range(20)]
    # # ... and build a WorkRequest object for each item in data
    # requests = makeRequests(do_something, data, print_result, handle_exception)
    # # to use the default exception handler, uncomment next line and comment out
    # # the preceding one.
    # #requests = makeRequests(do_something, data, print_result)
    #
    # # or the other form of args_lists accepted by makeRequests: ((,), {})
    # data = [((random.randint(1,10),), {}) for i in range(20)]
    # requests.extend(
    #     makeRequests(do_something, data, print_result, handle_exception)
    #     #makeRequests(do_something, data, print_result)
    #     # to use the default exception handler, uncomment next line and comment
    #     # out the preceding one.
    # )
    #
    # # we create a pool of 3 workmanager threads
    # print("Creating thread pool with 3 workmanager threads.")
    # main = ThreadPool(3)
    #
    # # then we put the work requests in the queue...
    # for req in requests:
    #     main.putRequest(req)
    #     print("Work request #%s added." % req.requestID)
    # # or shorter:
    # # [main.putRequest(req) for req in requests]
    #
    # # ...and wait for the results to arrive in the result queue
    # # by using ThreadPool.wait(). This would block until results for
    # # all work requests have arrived:
    # # main.wait()
    #
    # # instead we can poll for results while doing something else:
    # i = 0
    # while True:
    #     try:
    #         time.sleep(0.5)
    #         main.poll()
    #         print("Main thread __workingWokerNum...")
    #         print("(active workmanager threads: %i)" % (threading.activeCount()-1, ))
    #         if i == 10:
    #             print("**** Adding 3 more workmanager threads...")
    #             main.createWorkers(3)
    #         if i == 20:
    #             print("**** Dismissing 2 workmanager threads...")
    #             main.dismissWorkers(2)
    #         i += 1
    #     except KeyboardInterrupt:
    #         print("**** Interrupted!")
    #         break
    #     except NoResultsPending:
    #         print("**** No pending results.")
    #         break
    # if main.__dismissedWorkers:
    #     print("Joining all dismissed workmanager threads...")
    #     main.joinAllDismissedWorkers()

    def do_work(data):
        time.sleep(random.randint(1,3))
        res = str(datetime.datetime.now()) + "" +str(data)
        return res

    def print_result(request,result):
        print "---Result from request %s : %r" % (request.requestID,result)

    threadPool = ThreadPool(3)
    for i in range(40):
        req = WorkRequest(do_work,args=[i],kwds={},callback=print_result)
        threadPool.putRequest(req)
        print "work request #%s added." % req.requestID

    print '-'*20, threadPool.workersize(),'-'*20

    counter = 0
    while True:
        try:
            time.sleep(0.5)
            threadPool.poll()
            if(counter==5):
                print "Add 3 more workers threads"
                threadPool.createWorkers(3)
                print '-'*20, threadPool.workersize(),'-'*20
            if(counter==10):
                print "dismiss 2 workers threads"
                threadPool.dismissWorkers(2)
                print '-'*20, threadPool.workersize(),'-'*20
            counter+=1
        except NoResultsPending:
            print "no pending results"
            break

    threadPool.stop()
    print "Stop"
