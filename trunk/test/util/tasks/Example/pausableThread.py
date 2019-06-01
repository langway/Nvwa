#!/usr/bin/env python
# -*- coding: utf-8 -*-


#****************************************************
#  FileName: GThread.py
#  Author: ghostwwl
#  Note:
#    2008.10 add states and add Class_Timer
#****************************************************

import time
from threading import Thread,Event
from timeit import default_timer

__author__ = "ghostwwl (ghostwwl@gmail.com)"
__version__ = "1.0"

#-------------------------------------------------------------------------------
class Thread_Control(object):
    """The Control Class"""
    def __init__(self):
        self.pauseEvent = Event()
        self.pauseEvent.set()
        self.TimeOut = None

        self.CStateInfo = {-1:'STOP', 0:'READY', 1:'RUNNING', 2:'PAUSE'}
        self.CSTATES = 0



    def pause(self, TimeOut = None):
        self.TimeOut = TimeOut
        self.pauseEvent.clear()
        self.CSTATES = 2

    def restore(self):
        self.pauseEvent.set()

#-------------------------------------------------------------------------------
class mythread(Thread, Thread_Control):
    """
    BaseThread Class With Control Method[stop, pause, restore]
    time dilution of precision about 1 millisecond
    thread state {-1:'STOP', 0:'READY', 1:'RUNNING', 2:'PAUSE'}
    """

    def __init__(self, worker, ThreadName, TimeSpacing=0, TimeDelay = 0):
        """
        __init__(self, workmanager, ThreadName, TimeSpacing=0)
        workmanager         The Thread Owner
        ThreadName    The Thread Name
        TimeSpacing   Run TimeSpacing
        TimeDelay     The Thread Start TimeDelay
        """
        #初始化
        Thread_Control.__init__(self)
        Thread.__init__(self, name = ThreadName)

        self.owner = worker
        self.TimeSpacing = TimeSpacing #任务多长时间执行一次
        self.TimeDelay = TimeDelay
        self.Terminated = False

        self.setDaemon(1)

    def run(self):
        """
        This While loop stop until Terminated
        This Object Has sotp, pause(timeout = None) and restore method
        """
        if self.TimeDelay != 0:
            tstart = self.TimeDelay
        else:
            tstart = 0

        while not self.Terminated:#这里是线程的停止处理
            try:

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



    def stop(self):
        self.CSTATES = -1
        print 'WARNING [%s] Stopping Thread %-30s [ OK ]' % (time.strftime("%Y-%m-%d %H:%M:%S"),
                                                             self.name)
        self.Terminated = True

    def handle(self):
        """The Real Work Function"""
        pass

    def getstate(self):
        """check the thread state"""
        return self.CSTATES

    def getstatemsg(self):
        return self.CStateInfo[self.CSTATES]

if __name__=='__main__':

    class MyThread(mythread):

        def handle(self):
            for i in range(100):
                print 'testThread%s extended from Thread No.%s-%d'%(self.name,self.name,i)
                time.sleep(0.5)#模仿一个耗时操作

    t1 = MyThread(None,'1')
    t1.start()
    time.sleep(5)
    t1.stop()

    #这个地方会报错，因为线程只能执行一次
    try:
        t1.start()
    except Exception as e:
        print(str(e) )

    t2 = MyThread(None,'2')
    t2.start()
    time.sleep(5)
    t2.pause()
    time.sleep(10)
    t2.restore()
    time.sleep(5)
    t2.stop()







