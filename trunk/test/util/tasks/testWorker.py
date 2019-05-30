#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

from unittest import TestCase
from loongtian.util.tasks.tasksManager import *
from loongtian.util.tasks.task import Task,WorkRequest

import loongtian.util.tasks.queue as Queue

class TestWorker(TestCase):

    def setUp(self):
        print ("----setUp----")
        pass # def setUp(self):

    def testWorkerRequest(self):
        print(123)
        print ("----testWorkerRequest测试WorkRequest工作项（加载的是函数）----")
        import random
        import time,datetime



        #测试用函数
        def do_work(data):
            time.sleep(2)
            return data+1

        #返回结果调用callback
        def print_result(request,result):
            print ("---Result from request id: %s data: %r time:%s" % (request.id,result,datetime.datetime.now()))

        _worker = TasksManager(3, 'worker1', 1, auto_start =False)
        for i in range(20):#先创建20个任务
            req = WorkRequest(do_work,args=[i],kwds={},requestID=i,callback=print_result)
            _worker.addTask(req)
            print ("work request #%s added." % req.id)

        print ('-'*20,'workmanager.threadWorkerSize:', _worker.threadWorkerSize(), '-' * 20)

        #开始执行所有的工作请求
        _worker.start()

        print ('-'*20,'after start workmanager.threadWorkerSize:', _worker.threadWorkerSize(), '-' * 20)

        counter = 0
        while True:
            try:
                time.sleep(0.5)
                _worker.poll()
                if(counter==5):
                    print ("Add 3 more __threadWorkers threads")
                    _worker.createThreadWorkers(3)
                    print ('-'*20,'after Add 3 more,workmanager.threadWorkerSize:', _worker.threadWorkerSize(), '-' * 20)
                if(counter==10):
                    print ("dismiss 2 __threadWorkers threads")
                    _worker.stopThreadWorkers(2)
                    print ('-'*20,'after dismiss 2,workmanager.threadWorkerSize:', _worker.threadWorkerSize(), '-' * 20)
                if (counter==15):
                    print ("Add 10 more WorkRequest.")
                    for i in range(20,30):#再创建10个任务
                        req = WorkRequest(do_work,args=[i],kwds={},requestID=i,callback=print_result)
                        print ("work request #%s added." % req.id)
                        _worker.addTask(req)

                    print (_worker.getThreadWorkersStates())

                    time.sleep(2)
                counter+=1
            except NoResultsPending:
                print ("no pending results")
                break
            except Queue.Empty:
                print ('queue empty')
                break

        _worker.stop()
        print ("Stop")
        pass # def testWorkerRequest(self)

    def testWorkerTask(self):
        print ("----testWorkerTask测试Task工作项（加载的是重载的Task类）----")

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

        class InitializeTask(Task):
            def start(self):
                for i in range(200):
                    self.workmanager.putTask(ComputationTask, i)
                yield None

        _worker = TasksManager(3, 'worker2', 2, auto_start =False)
        for i in range(50):#先创建20个任务
            task=ComputationTask(i)
            _worker.addTask(task)
            print ("ComputationTask #%s added." % task.id)

        print ('-'*20,'workmanager.threadWorkerSize:', _worker.threadWorkerSize(), '-' * 20)

        #开始执行所有的工作请求
        _worker.start()

        counter = 0
        while True:
            try:
                # time.sleep(0.5)
                _worker.poll()
                if(counter==5):
                    print ("Add 3 more __threadWorkers threads")
                    _worker.createThreadWorkers(3)
                    print ('-'*20,'after Add 3 more,workmanager.threadWorkerSize:', _worker.threadWorkerSize(), '-' * 20)
                if(counter==10):
                    print ("dismiss 2 __threadWorkers threads")
                    _worker.stopThreadWorkers(2)
                    print ('-'*20,'after dismiss 2,workmanager.threadWorkerSize:', _worker.threadWorkerSize(), '-' * 20)
                if (counter==15):
                    print ("Add 10 more ComputationTask.")
                    for i in range(50,60):#再创建10个任务
                        task=ComputationTask(i)
                        _worker.addTask(task)
                        print ("ComputationTask #%s added." % task.id)
                    time.sleep(2)

                counter+=1
            except NoResultsPending:
                print ("no pending results")
                break
            except Queue.Empty:
                print ('queue empty')
                break

        _worker.stop()
        print ("Stop")



    def tearDown(self):
        print ("----tearDown----")

    pass # class TestWorker(TestCase)




