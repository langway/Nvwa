#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

from loongtian.util.helper import threadHelper
from loongtian.util.log.logger import *
from loongtian.util.tasks.stateController import StateController


class Task(StateController):
    """
    线程/进程的工作任务。
    纯代码逻辑（业务逻辑）部分。
    :parameter
    构造函数参数说明
    :attribute
    对象属性说明
    """

    def __init__(self, name, id):
        super(Task, self).__init__(name, id)

        self.workmanager = None  # 当前工作项的workmanager
        self._subTasksManager = None  # 子工作项的workmanager
        self.useParentWorkManager = False  # 子工作项是否使用当前Task的workmanager

        self.worker = None
        self.exception = False
        self.callback = self.callback
        self.exc_callback = self.exc_callback

        pass  # def __init__(self)

    def start(self):
        """
        线程启动方法
        """
        super(Task, self).start()

    def _prePause(self, TimeDelay=None, TimeOut=None):
        """
        [重载]暂停当前线程之前的处理程序（例如保存数据等）。
        :return:
        """
        self.SubTasksManager.pause(TimeDelay, TimeOut)
        pass  # def prePause(self)

    def _preStop(self):
        """
        [重载]停止线程之前的处理程序
        """
        # 停止其下的子任务
        self.SubTasksManager.stop()
        # if len(self._subTasks) > 0:
        #     _start = time.time()
        #     logger.info("%s try stop sub threads" % self.name)
        #     # 停止其下的子线程
        #     map(lambda _t0: _t0.stop(), self._subTasks)
        #     _end = time.time()
        #     # 等待并检测其子线程是否停止。
        #     while True:
        #         if any([_t1.isAlive() for _t1 in self._subTasks]):
        #             if _end - _start > 2:
        #                 logger.info("%s stop sub threads out recordTime" % self.name)
        #                 break
        #         else:
        #             logger.info("%s stop sub threads using %f s" % (self.name, _end - _start))
        #             break

    def _preComplete(self):
        """
        [重载]正常执行完毕，需要退出的前期调用(默认由系统执行，无需外部调用)。
        :return:
        """
        # 停止其下的子任务
        self.SubTasksManager.stop()

        pass  # def preComplete(self)

    def callback(request, *result):
        """
        建立任务请求时有两种回调函数 callback
        :rawParam request:
        :rawParam result:
        :return:
        """
        logger.debug(result)
        pass  # def callback(request,result)

    def exc_callback(request, *exc_info):
        """
        建立任务请求时有两种回调函数 exc_callback
        :rawParam request:
        :rawParam exc_info:
        :return:
        """
        logger.debug(exc_info)
        pass  # def exc_callback(request,exc_info)

    ########################################################################
    """下面为子任务操作"""

    @property
    def SubTasksManager(self):
        if self._subTasksManager is None:
            if self.useParentWorkManager and not self.workmanager is None:
                self._subTasksManager = self.workmanager
            else:
                from loongtian.util.tasks.tasksManager import TasksManager
                self._subTasksManager = TasksManager(10, "", "", auto_start=False)
        return self._subTasksManager
        pass  # def subTaskWorkManager(self)

    # @subTaskWorkManager.setter
    # def subTaskWorkManager(self, value):
    #     from loongtian.util.tasks.tasksManager import TasksManager
    #     # 如果有值但不是WorkManager实例，抛出错误。
    #     if not value is None and not isinstance(value, TasksManager):
    #         raise ValueError('you must provide a loongtian.util.tasks.workmanager.WorkManager to set!')
    #
    #     self._subTaskWorkManager = value
    #     pass  # def subTaskWorkManager(self,value)
    #
    # def addSubTask(self, task):
    #     """
    #     添加一个子任务。
    #     :rawParam task:
    #     :return:
    #     """
    #     if not task is None and isinstance(task, Task):
    #         self._subTasks[task.id] = task
    #     pass  # def addSubTask(self,task)
    #
    # def addSubTasks(self, tasks):
    #     """
    #     添加多个子任务。
    #     :rawParam tasks:
    #     :return:
    #     """
    #     if not tasks is None:
    #         if isinstance(tasks, Tasks):  # 如果是Tasks直接加入
    #             self._subTasks.update(tasks)
    #         elif isinstance(tasks, list) or isinstance(tasks, tuple) or isinstance(tasks, set):  # 如果是列表，循环加入。
    #             for item in tasks:
    #                 self.addSubTask(item)
    #     pass  # def addSubTasks(self,tasks)
    #
    # def removeSubTask(self, task):
    #     """
    #     移除一个子任务。
    #     :rawParam task:
    #     :return:
    #     """
    #     if not task is None and isinstance(task, Task):
    #         self._subTasks.pop(task.id)
    #     pass  # def addSubTask(self,task)
    #
    # def removeSubTasks(self, tasks):
    #     """
    #     移除多个子任务。
    #     :rawParam tasks:
    #     :return:
    #     """
    #     if not tasks is None:
    #         if isinstance(tasks, Tasks):  # 如果是Tasks直接删除。
    #             for id, task in self._subTasks.items():
    #                 self._subTasks.pop(id)
    #         elif isinstance(tasks, list) or isinstance(tasks, tuple) or isinstance(tasks, set):  # 如果是列表，循环删除。
    #             for item in tasks:
    #                 self.removeSubTask(item)
    #     pass  # def addSubTasks(self,tasks)
    #
    # def _startSubTasks(self):
    #     """
    #     启动子任务
    #     :return:
    #     """
    #     if self._subTasks is None:
    #         return
    #     for subtask in self._subTasks:
    #         self.subTaskWorkManager.addTask(subtask)
    #
    #     self.subTaskWorkManager.start()
    #
    #     pass  # def _startSubTasks(self)
    #
    # def _stopSubTasks(self):
    #     """
    #     停止子任务
    #     :return:
    #     """
    #     if self._subTasks is None:
    #         return
    #
    #     self.subTaskWorkManager.stop()
    #
    #     pass  # def _stopSubTasks(self)
    #
    # def _pauseSubTasks(self):
    #     """
    #     暂停子任务
    #     :return:
    #     """
    #     if self._subTasks is None:
    #         return
    #
    #     self.subTaskWorkManager.pause()
    #
    #     pass  # def _pauseSubTasks(self)
    #
    # pass  # class Task(object)


# class Tasks(dict):
#     """
#     工作项的字典（键：Task.id，值：Task）
#     """
#
#     def __setitem__(self, key, item):
#         """
#         重载的根据键设置值的函数。
#         :rawParam key:
#         :rawParam item:
#         :return:
#         """
#         if key is None:
#             return
#         if item is None:
#             self[key] = item
#         if isinstance(item, Task):
#             # raise ValueError ('you mast add a Task to Tasks!')
#             super(Tasks, self).__setitem__(key, item)
#
#     def __add__(self, other):
#         """
#         重载的添加另一个字典的函数。
#         :rawParam other:
#         :return:
#         """
#         if other is None:
#             return
#
#         if isinstance(other, Tasks):
#             self.update(other)
#         elif isinstance(other, dict):
#             for key, item in other.items():
#                 super(Tasks, self).__setitem__(key, item)
#
#         pass  # def __add__(self, other)
#
#     def __and__(self, other):
#         return self.__add__(other)
#         pass  # def __and__(self, other)
#
#     pass  # class Tasks(dict)


class WorkRequest(object):
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
                 callback=None, exc_callback=threadHelper.exceptionHandler):
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
            self.id = id(self)
        else:
            try:
                self.id = hash(requestID)
            except TypeError:
                raise TypeError("id must be hashable.")
        self.name = self.id
        self.workmanager = None  # 当前工作项的workmanager

        self.exception = False
        self.callback = callback
        self.exc_callback = exc_callback
        self.callable = callable_
        self.args = args or []
        self.kwds = kwds or {}

    def __str__(self):
        return "<WorkRequest id=%s args=%r kwargs=%r exception=%s>" % \
               (self.id, self.args, self.kwds, self.exception)


# utility functions
def makeRequests(callable_, args_list, callback=None,
                 exc_callback=threadHelper.exceptionHandler):
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
