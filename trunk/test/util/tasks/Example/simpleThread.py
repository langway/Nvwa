#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'
import datetime
import time
from threading import Thread,Event

import loongtian.util.helper.threadHelper as threadHelper
from loongtian.util.common.enum import  Enum
from loongtian.util.log.logger import  *

class WorkerStateEnum(Enum):
    """
    当前任务的工作状态。
    包括：

    """
    Unknown=-1
    #准备完毕，可以执行。
    ReadyToRun=0
    #正在捕获Token
    TokenCatching=1
    #已经捕获Token
    TokenCatched=2
    #正在运行
    Running=3
    #正常执行完毕，已经退出
    Completed=4
    #被用户（系统）暂停
    Paused=5
    #被用户（系统）暂停后继续运行
    Restarted=6
    #执行中出现异常，非正常退出
    Aborted=7
    #执行中被用户（系统）强行终止，从loop循环终止，数据比较安全
    Stopped=8
    #执行中被用户（系统）强行终止，并非从loop循环终止，可能丢失数据
    Terminated=9
    #正在捕获Token
    TokenReleasing=10
    #已经捕获Token
    TokenReleased=11

    pass#class WorkerStateEnum(Enum)

class WorkerStateInfo:
    """
    当前对象的工作状态的包装类。
    """
    def __init__(self,id,state):
        self.id=id
        self.time=datetime .datetime.now()
        self.state=state

    pass # class WorkerStateInfo

class WorkerStateInfos:
    """
    当前对象的工作状态的包装类的列表，用来记录状态的迁移过程。
    """
    def __init__(self):
        #记录当前的工作状态的列表。
        self.states=[]
        self.currentState=WorkerStateEnum.Unknown
        pass # def __init__(self)


    def setWorkerState(self,state):
        """
        记录当前的工作状态
        """
        self.currentState=state
        self.states.append(WorkerStateInfo(len(self.states),state ))

        pass # def setWorkerState(self,state)

    def getCurrentWorkerState(self):
        """
        取得当前对象的工作状态（状态列表中的最后一个）
        """
        return self.currentState
        #return self.states[len(self.states )]

        pass # def getCurrentWorkerState(self)

    def getLastDuration(self):
        """
        取得最后一次状态变化的持续时间。
        例如从暂停到恢复的时间。
        """

        timestart=self.states[len(self.states )-2].time
        timeend=self.states[len(self.states )-1].time

        # dur=(timeend - timestart).seconds+(timeend - timestart).microseconds / 1000
        return timeend - timestart
        pass # def getLastDuration(self)

    def getWorkerStateInfos(self,state):
        """
        根据指定的工作状态取得相同的对象的工作状态的包装类
        例如：可以用来查看当前对象的暂停次数。
        """
        infos=[]
        for info in self.states:
            if info.state==state:
                infos.append(info)
        return infos

        pass #def getWorkerStateInfos(self,state)

    pass # class WorkerStateInfos

class Thread_Control(object):
    """
    Thread线程类的的扩展类，增加stop、pause和restore方法。
    使线程可以暂停（pause）、恢复（restore），并可进行暂停前及恢复前的处理（例如保存数据等）。"""
    def __init__(self,ThreadName,num):
        self.pauseEvent = Event()
        self.pausedTimeOut = None
        self.__threadName=ThreadName
        self.__thread_num=num

        self.exceptionQu

        #记录状态的迁移过程
        self.workerStateInfos=WorkerStateInfos()
        #设置线程状态
        self.workerStateInfos.setWorkerState(WorkerStateEnum.ReadyToRun)

    def pause(self, TimeOut = None):
        """
        暂停当前线程。
        :rawParam TimeOut:
        :return:
        """
        self.pausedTimeOut = TimeOut
        #设置线程状态
        self.workerStateInfos.setWorkerState(WorkerStateEnum.Paused)
        #暂停之前的处理程序（例如保存数据等）。
        self.prePause()
        self.pauseEvent.set()
        logger.debug('Thread Object(%d) Paused, Time:%s' %(self.__thread_num, datetime.datetime.now()))

    def prePause(self):
        """
        暂停当前线程之前的处理程序（例如保存数据等）。
        (必须进行重载)。
        :return:
        """
        pass # def prePause(self)

    def restore(self):
        """
        暂停后恢复当前线程，继续执行当前线程的代码逻辑。
        :return:
        """
        self.pausedTimeOut=None
        #设置线程状态
        self.workerStateInfos.setWorkerState(WorkerStateEnum.Restarted)
        #恢复之前的处理程序（例如读取数据等）。
        self.preRestore()

        self.pauseEvent.clear()
        logger.debug('Thread Object(%d) Restored, Time:%s' %(self.__thread_num, datetime.datetime.now()))

    def preRestore(self):
        """
        暂停后恢复当前线程之前的处理程序（例如从缓存中读取数据等）。
        (必须进行重载)。
        :return:
        """
        pass # def preRestore(self)

    pass # class State_Controller(object)

class ThreadDelegator(Thread,Thread_Control):
    """
    对threading.Thread的扩展类。
    1、使线程可以停止（stop）、暂停（pause）、恢复（restore）。
    2、并可进行停止前、暂停前及恢复前的处理（例如保存数据等）。
    3、支持由其他线程（进程）调用时抛出错误
    """

    def __init__(self,worker,ThreadName, num, interval):
        #初始化
        Thread_Control.__init__(self,ThreadName,num)
        Thread.__init__(self, name = ThreadName)

        self.worker=worker
        self.thread_num = num
        self.interval = interval
        self.loopCounter=1
        #设置为守护进行，也就是线程随主线程一起结束，必须在start()之前调用。默认为False。
        self.setDaemon(True)
        #外界强制停止线程的标记
        self.__terminatedEvent = Event()


    def run(self): #Overwrite run() method, put what you want the thread do here

        #设置线程状态
        self.workerStateInfos.setWorkerState(WorkerStateEnum.Running)

        #判断线程是否停止，如果没有停止，继续工作函数的代码逻辑，否则进行其他处理
        while not self.__terminatedEvent.isSet():

            #这里是线程的暂停处理
            if self.pauseEvent.isSet():
                #带有暂停超时的处理
                if not self.pausedTimeOut is None :
                    #休眠
                    time.sleep(self.pausedTimeOut)
                    #恢复线程
                    self.restore()

                time.sleep(0.001) #暂停1毫秒 防止空跑占用过高cpu
                #如果线程暂停，不进入实际代码部分，继续空跑循环
                continue

            logger.debug('Thread Object(%d),No.%s Time:%s' %(self.thread_num,self.loopCounter, datetime.datetime.now() ))
            self.loopCounter+=1
            time.sleep(self.interval)
            try:
                #这个才是我们的工作函数
                self._handle()
                time.sleep(0.001) #暂停1毫秒 防止空跑占用过高cpu
            except Exception,e:
                #处理错误
                self.handleException(e)

            pass # while not self.__terminatedEvent.isSet()

        #在线程主要代码跑完之后的处理程序
        self.handleAfterRunning()
        #设置线程状态
        self.workerStateInfos.setWorkerState(WorkerStateEnum.Completed)

        pass # def run(self)

    def _handle(self):
        """实际的工作函数"""
        pass

    def handleException(self,exception):
        """
        线程中发生的错误的处理程序。
        :rawParam exception: 错误。
        :return:
        """
        pass #def handleException(self,exception)

    def handleAfterRunning(self):
        """
        在线程主要代码跑完之后的处理程序。
        :return:
        """
        pass #def handleAfterRunning(self)

    def stop(self):
        """
        强制停止当前线程中的loop循环，退出当前线程。数据会由用户进行处理，会比较安全。
        与terminate不同，如果中间还有已经启动的大型程序，将等待该大型程序结束，进入到下一次loop循环时才会停止。
        :return:
        """
        #强制停止线程之前的处理程序。
        self.preStop()
        logger.debug('Thread Object(%d) Stopped, Time:%s' %(self.thread_num, datetime.datetime.now()))
        self.__terminatedEvent.set()
        #设置线程状态
        self.workerStateInfos.setWorkerState(WorkerStateEnum.Stopped)
        self.join()

        pass# def stop(self)

    def terminate(self):
        """
        强制停止当前线程，退出当前线程。数据一般不会由用户进行处理，可能丢失数据
        与stop不同，如果中间还有已经启动的大型程序，不会等待该大型程序结束。
        raises SystemExit in the context of the given thread, which should
        cause the thread to exit silently (unless caught)
        """
        #设置线程状态
        self.workerStateInfos.setWorkerState(WorkerStateEnum.Terminated)
        return threadHelper.asyncThreadEventHandler(threadHelper.getThreadId(self) ,SystemExit)
        pass # def terminate(self)

    def preStop(self):
        """
        强制停止线程之前的处理程序。
        (必须进行重载)。
        :return:
        """
        pass # def preStop(self)

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
        #设置线程状态
        self.workerStateInfos.setWorkerState(WorkerStateEnum.Aborted)
        return threadHelper.asyncThreadEventHandler(threadHelper.getThreadId(self) , exceptionType)
        pass # def raiseException(self, exceptionType)

    pass # class ThreadDelegator(Thread,State_Controller)

class WorkRequest:
    """
    外部函数的代理程序，通过WorkRequest，执行该外部函数
    :parameter callable_:，可定制的，执行work的函数
    :parameter args: 列表参数
    :parameter kwds: 字典参数
    :parameter id: id
    :parameter callback: 可定制的，处理resultQueue队列元素的函数
    :parameter exc_callback:可定制的，处理异常的函数
    """
    def __init__(self,callable_,args=None,kwds=None,requestID=None,
                 callback=None,exc_callback= threadHelper.exceptionHandler):
        if requestID == None:
            self.requestID = id(self)
        else:
            try:
                self.requestID = hash(requestID)
            except TypeError:
                raise TypeError("requestId must be hashable")
        self.exception = False
        self.callback = callback
        self.exc_callback = exc_callback
        self.callable = callable_
        self.args = args or []
        self.kwds = kwds or {}

    def __str__(self):
        return "WorkRequest id=%s args=%r kwargs=%r exception=%s" % \
            (self.requestID,self.args,self.kwds,self.exception)


def test():


    # # 一、测试ThreadDelegator
    # print '----------测试ThreadDelegator----------\n'
    # #1、测试stop
    # print '----------测试ThreadDelegator.stop----------'
    # thread1 = ThreadDelegator(None,'thread1',1, 1)
    # thread2 = ThreadDelegator(None,'thread2',2, 0.5)
    # thread1.start()
    # time.sleep(2)
    # thread2.start()
    # time.sleep(5)
    # thread1.stop()
    # time.sleep(8)
    # thread2.stop()
    #
    #
    # #2、测试pause、restore
    # print '\n'
    # print '----------测试ThreadDelegator.pause、restore----------'
    # thread1 = ThreadDelegator(None,'thread1',1, 1)
    # thread2 = ThreadDelegator(None,'thread2',2, 1)
    # thread1.start()
    # time.sleep(5)
    # thread1.pause()
    # thread2.start()
    # time.sleep(8)
    # thread2.pause()
    #
    # thread1.restore()
    # time.sleep(5)
    # thread1.stop()
    # thread2.restore()
    # time.sleep(8)
    # thread2.stop()

    #3、测试暂停时间，过了该时间后，线程将继续运行
    print '\n'
    print '----------测试ThreadDelegator.pause(5)，暂停时间，过了该时间后，线程将继续运行----------'
    thread1 = ThreadDelegator(None,'thread1',1, 1)
    thread1.start()
    time.sleep(5)
    timestart=datetime.datetime.now()
    timeend=datetime.datetime.now()
    thread1.pause(5)
    print('线程休息:%s秒'%(thread1.workerStateInfos.getLastDuration()))
    time.sleep(8)#由于线程休息了5秒，这里主线程休息3秒，所以在stop前，还会输出3次
    thread1.stop()



    return

if __name__ == '__main__':
    test()