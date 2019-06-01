#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

""" Thread Distributor
Ver     : 0.1
Author  : Trung Huynh
"""
from Queue import Queue
from threading import Thread, Lock,Event
from multiprocessing import Process
import types
import time
from datetime import datetime
from timeit import default_timer

class Thread_Control(object):
    """
    Thread的扩展类，增加stop、pause和restore方法。
    """
    def __init__(self):
        #当线程停止时用来阻塞线程的事件
        self.pauseEvent = Event()
        self.pauseEvent.set()
        self.TimeOut = None
        #线程是否被人为终止的标记
        self.Terminated = False
        self.CStateInfo = {-1:'STOP', 0:'READY', 1:'RUNNING', 2:'PAUSE'}
        self.CSTATES = 0

    def stop(self):
        self.CSTATES = -1
        print 'WARNING [%s] Stopping Thread %-30s [ OK ]' % (datetime.now(), self.name)
        self.Terminated = True

    def pause(self, TimeOut = None):
        self.TimeOut = TimeOut
        self.pauseEvent.clear()
        self.CSTATES = 2

    def restore(self):
        self.pauseEvent.set()

class ThreadDelegator(Thread, Thread_Control):
    """
    工作者的线程执行代理（是任务的真正执行者）。
    """
    def __init__(self, worker, ThreadName=None, TimeSpacing=0, TimeDelay = 0):
        #初始化
        Thread_Control.__init__(self)
        Thread.__init__(self, name = ThreadName)
        self.queue = Queue()
        self.worker = worker
        if ThreadName is not None: self.name = ThreadName

        self.owner = worker
        self.TimeSpacing = TimeSpacing #任务多长时间执行一次
        self.TimeDelay = TimeDelay

        self.setDaemon(True)

    def run(self):
        """
        This While loop stop until Terminated
        This Object Has sotp, pause(timeout = None) and restore method
        """
        if self.TimeDelay != 0:
            tstart = self.TimeDelay
        else:
            tstart = 0

        while True:
            try:
                #这里是线程的停止处理
                if self.Terminated:
                    break

                #这里是线程的暂停处理
                if self.TimeOut is not None:
                    #带有暂停超时的处理
                    self.pauseEvent.wait(self.TimeOut)
                    self.TimeOut = None
                    self.pauseEvent.set()
                else:
                    #不带超时 那么必须等到线程恢复
                    self.pauseEvent.wait()

                CUR_TIMING = default_timer()
                if CUR_TIMING - tstart > self.TimeSpacing:
                    tstart = CUR_TIMING
                    #这个才是我们的工作函数
                    self.CSTATES = 1
                    self.handle()

                time.sleep(0.001) #暂停1毫秒 防止空跑占用过高cpu
            except Exception, e:
                print "ERROR %s] %s Error: %s" % (time.strftime("%H:%M:%S"), self.getName(), str(e))

            pass #while True

        self.stop()

    def handle(self):
        """The Real Work Function"""
        #如果是传递两个参数给 iter() ，它会重复地调用 func ，直到迭代器的下个值等于sentinel。
        for task in iter(self.worker.taskQueue.get, "STOP"):
            task.delegator = self

            #增加正在执行操作的计数器
            self.worker.lock.acquire()
            self.worker.working += 1
            self.worker.lock.release()

            #这里需要判断两种任务类型：Task或是Function
            if isinstance(task,Task):
                for result in task.run():
                    if result is not None:
                        self.worker.resultQueue.put(result)
                        print 'result:%s'%(result)
            elif type(task) is types.FunctionType:
                pass


            self.worker.lock.acquire()
            self.worker.working -= 1
            self.worker.lock.release()

            # Stop if no workmanager is __workingWokerNum and queue is empty. It is
            # reasonable because no new task can be generated at this point.
            if (self.worker.working == 0) \
            and (self.worker.taskQueue.empty()):
                self.worker.stop()
        pass

    def getstate(self):
        """check the thread state"""
        return self.CSTATES

    def getstatemsg(self):
        return self.CStateInfo[self.CSTATES]



    def send(self, msg, to):
       self.worker.send(msg, to)


class ProcessDelegator(Process):
    """
    工作者的进程执行代理（是任务的真正执行者）。
    """

    def __init__(self, worker, name=None):
        Process.__init__(self)
        self.queue = Queue()
        self.worker = worker
        if name is not None: self.name = name


class Task(object):
    """
    任务，必须重载。
    """
    def __init__(self):
        self.worker = None
        self.delegator=None
        self.inp = None

    def run(self):
        raise NotImplementedError


class Worker:
    """
    任务的执行者
    """

    class StopTask(Task):

        def run(self):
            self.worker.resultQueue.put("STOP")
            yield None


    def __init__(self, n_delegators=0):
        """

        :rawParam n_delegators: 工作者执行代理的最大数量。
        :return:
        """
        self.taskQueue = Queue()
        self.resultQueue = Queue()
        self.name_id_map = {}
        self.numOfDelegators = n_delegators
        self.delegators = []
        self.working = 0
        self.lock = Lock()
        for i in xrange(n_delegators):
            self.addThreadDelegator()

    def send(self, msg, to):
        if type(to) is int:
            self.delegators[to].queue.put(msg)
        elif type(to) is str:
            self.delegators[self.name_id_map[to]].queue.put(msg)

    def addThreadDelegator(self, name=None):
        """
        添加线程执行代理。
        :rawParam name: 给定的执行代理的名称（可选）。
        :return:
        """
        if name is not None: self.name_id_map[name] = self.numOfDelegators
        self.delegators.append(ThreadDelegator(self, name))
        self.numOfDelegators += 1

    def addProcessDelegator(self, name=None):
        """
        添加线程执行代理。
        :rawParam name: 给定的执行代理的名称（可选）。
        :return:
        """
        if name is not None: self.name_id_map[name] = self.numOfDelegators
        self.delegators.append(ProcessDelegator(self, name))
        self.numOfDelegators += 1

    def run(self):
        for t in self.delegators: t.start()
        for t in self.delegators: t.join()

    def addTask(self, task_class, data=None):
        """

        :rawParam task_class:
        :rawParam data:
        :return:
        """
        curtask = task_class()
        curtask.worker = self
        curtask.inp = data
        self.taskQueue.put(curtask)

    def stop(self):
        self.addTask(Worker.StopTask)
        for i in xrange(self.numOfDelegators):
            self.taskQueue.put("STOP")

    def results(self):
        for item in iter(self.resultQueue.get, "STOP"):
            yield item


class ComputationTask(Task):

    def run(self):
        time.sleep(1) #模拟一个大型程序的耗时
        yield self.inp+1;


class InitializeTask(Task):

    def run(self):
        for i in xrange(200):
            self.worker.addTask(ComputationTask, i)

        yield None


if __name__ == "__main__":
    #Test dead __lock
    # for i in xrange(200):
    #     # print i
    #     workmanager = WorkManager(20)
    #     workmanager.addTask(InitializeTask)
    #     workmanager.start()

    # workmanager = WorkManager(20)
    # workmanager.addTask(InitializeTask)
    # workmanager.start()

    t1 = Worker(20)
    t1.addTask(InitializeTask)
    t1.run()
    time.sleep(5)
    t1.stop()

    # #这个地方会报错，因为线程只能执行一次
    # try:
    #     t1.start()
    # except Exception,e:
    #     print(str(e) )
    #
    # t2 = MyThread(None,'2')
    # t2.start()
    # time.sleep(5)
    # t2.pause()
    # time.sleep(10)
    # t2.restore()
    # time.sleep(5)
    # t2.stop()