#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

import time,datetime
from unittest import TestCase
from loongtian.util.tasks.worker import ThreadWorker
from loongtian.util.tasks.task import  Task,WorkRequest

class TestThreadDelegator(TestCase):

    def setUp(self):
        print("----setUp----")
        pass # def setUp(self):

    # def testThreadDelegator(self):
    #     print("----testThreadDelegator----")
    #     # 一、测试ThreadDelegator
    #     print('----------测试ThreadDelegator----------\n')
    #
    #     #1、测试complete
    #     print('----------测试ThreadDelegator._complete----------')
    #     thread1 = ThreadWorker(None,'thread1',1, 1)
    #     thread1.start()
    #     time.sleep(3)
    #     thread1._complete()
    #
    #     #2、测试stop
    #     print('----------测试ThreadDelegator.stop----------')
    #     thread1 = ThreadWorker(None,'thread1',1, 1)
    #     thread2 = ThreadWorker(None,'thread2',2, 0.5)
    #     thread1.start()
    #     time.sleep(2)
    #     thread2.start()
    #     time.sleep(5)
    #     thread1.stop()
    #     time.sleep(8)
    #     thread2.stop()
    #
    #
    #     #3、测试pause、restore
    #     print('\n')
    #     print('----------测试ThreadDelegator.pause、restore----------')
    #     thread1 = ThreadWorker(None,'thread1',1, 1)
    #     thread2 = ThreadWorker(None,'thread2',2, 1)
    #     thread1.start()
    #     time.sleep(5)
    #     thread1.pause()
    #     thread2.start()
    #     time.sleep(8)
    #     thread2.pause()
    #
    #     thread1.restore()
    #     time.sleep(5)
    #     thread1.stop()
    #     thread2.restore()
    #     time.sleep(8)
    #     thread2.stop()
    #
    #     #4、测试ThreadDelegator.pause(5)，暂停时间，过了该时间后，线程将继续运行
    #     print('\n')
    #     print('----------测试ThreadDelegator.pause(5)，暂停时间，过了该时间后，线程将继续运行----------')
    #     thread1 = ThreadWorker(None,'thread1',1, 1)
    #     thread1.start()
    #     time.sleep(5)
    #     thread1.pause(5)
    #     print('线程休息:%s秒'%(thread1.workerStateInfos.getLastDuration()))
    #     time.sleep(8)#由于线程休息了5秒，这里主线程休息3秒，所以在stop前，还会输出3次
    #     thread1.stop()
    #
    #
    #     pass # def testThreadHelper(self)

    def testWorkerTask(self):
        print("----testWorkerTask测试Task工作项（加载的是函数及重载的Task类）----")

        #测试用函数
        def do_work(data):
            time.sleep(0.1)
            return data+1

        #返回结果调用callback
        def print_result(request,result):
            print("---Result from request id: %s data: %r time:%s" % (request.ID,result,datetime.datetime.now()))


        # thread1 = ThreadWorker(None,'thread1',1, 1)
        # for i in range(10):#创建10个任务
        #     req = WorkRequest(do_work,args=[i],kwds={},requestID=i,callback=print_result)
        #     thread1.addJob(req)
        #     print("work request #%s added." % req.id
        # thread1.start()
        # thread1.wait()
        # thread1.stop()

        #测试用类
        class ComputationTask(Task):

            def __init__(self,id):
                Task.__init__(self,id,id)
                self.inp=id
                # self.callback=print_result

            def start(self):
                time.sleep(0.5) #模拟一个大型程序的耗时
                self.inp += 1
                return  self.inp

        thread2 = ThreadWorker(None, 'thread2',2, 1)
        for i in range(10):#创建10个任务
            task = ComputationTask(i)
            thread2.addJob(task)
            print("work task #%s added." % task.id)
        thread2.start()
        thread2.wait()
        thread2._complete()


    def tearDown(self):
        print("----tearDown----")

    pass # class TestThreadDelegator(TestCase)

