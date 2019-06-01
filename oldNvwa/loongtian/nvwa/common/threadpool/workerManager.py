#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    workerManager 
Author:   fengyh 
DateTime: 2014/8/19 17:08 
UpdateLog:
1、fengyh 2014/8/19 Create this File.


"""
import Queue

from loongtian.nvwa.common.threadpool.worker import Worker


class WorkerManager:
    """
    WorkerManager负责初始化Python线程池，提供将任务加入队列和获取结果的接口，并能等待所有任务完成。
    """

    def __init__(self, num_of_workers=10, timeout=1):
        """

        :param num_of_workers:
        :param timeout:
        """
        self.workQueue = Queue.Queue()
        self.resultQueue = Queue.Queue()
        self.workers = []
        self.timeout = timeout
        self._recruit_threads(num_of_workers)

    def _recruit_threads(self, num_of_workers):
        """
        循环建立线程池，包含指定数量的线程
        :param num_of_workers:
        """
        for i in range(num_of_workers):
            worker = Worker(self.workQueue, self.resultQueue, self.timeout)
            self.workers.append(worker)

    def wait_for_complete(self):
        """
        等待每个线程执行完成，执行完某个线程如果等待队列里还有任务，则加入线程池执行。
        :return:
        """
        # ...then, wait for each of them to terminate:
        while len(self.workers):
            worker = self.workers.pop()
            worker.join()  # 阻塞进程直到线程执行完毕
            if worker.isAlive() and not self.workQueue.empty():
                self.workers.append(worker)
        print "All jobs are are completed."

    def wait(self):
        self.wait_for_complete()

    def add_job(self, callable, *args, **kwds):
        self.workQueue.put((callable, args, kwds))

    def get_result(self, *args, **kwds):
        return self.resultQueue.get(*args, **kwds)