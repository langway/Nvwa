#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    worker 
Author:   fengyh 
DateTime: 2014/8/19 17:07 
UpdateLog:
1、fengyh 2014/8/19 Create this File.

http://developer.51cto.com/art/201002/185290.htm

"""

import Queue
import sys
from threading import Thread


class Worker(Thread):
    """
    Worker类是一个Python线程池，不断地从workQueue队列中获取需要执行的任务，执行之，并将结果写入到resultQueue中。
    这里的workQueue和resultQueue都是线程安全的，其内部对各个线程的操作做了互斥。
    当从workQueue中获取任务超时，则线程结束。

    函数名    功能
        run() 	如果采用方法2创建线程就需要重写该方法
        getName() 	获得线程的名称(方法2中有示例)
        setName() 	设置线程的名称
        start() 	启动线程
        join(timeout)
            在join()位置等待另一线程结束后再继续运行join()后的操作,timeout是可选项，表示最大等待时间
        setDaemon(bool)
            True:当父线程结束时，子线程立即结束；False:父线程等待子线程结束后才结束。默认为False
        isDaemon() 	判断子线程是否和父线程一起结束，即setDaemon()设置的值
        isAlive()   判断线程是否在运行
    """
    worker_count = 0

    def __init__(self, work_queue, result_queue, timeout=0, **kwds):
        Thread.__init__(self, **kwds)
        self.id = Worker.worker_count
        Worker.worker_count += 1

        # 守护线程
        self.setDaemon(True)

        self.workQueue = work_queue
        self.resultQueue = result_queue
        self.timeout = timeout

        # start会执行run
        self.start()
        self._block

    def run(self):
        """

        :return:
        """
        ''' the get-some-work, do-some-work main loop of worker threads '''
        while True:
            try:
                callable, args, kwds = self.workQueue.get(timeout=self.timeout)
                res = callable(*args, **kwds)
                print "worker[%2d]: %s" % (self.id, str(res) )
                self.resultQueue.put(res)
            except Queue.Empty:
                break
            except:
                print 'worker[%2d]' % self.id, sys.exc_info()[:2]