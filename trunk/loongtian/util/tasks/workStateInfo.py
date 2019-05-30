#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

import uuid
import datetime
from loongtian.util.tasks import WorkStateEnum
from loongtian.util.log.logger import logger


class WorkStateInfo:
    """
    当前对象的工作状态的包装类。
    """

    def __init__(self, id, state):
        self.id = id
        self.time = datetime.datetime.now()
        self.state = state

    pass  # class WorkStateInfo


class WorkerStateNotTransferrableError(Exception):
    """
    工作项状态不可转换的错误。
    """
    pass  # class WorkerStateNotTransferrableError(Exception )


class WorkerStateInfos:
    """
    当前对象的工作状态的包装类的列表，用来记录状态的迁移过程。
    """
    # 工作状态可转换的字典，用来记录某种状态到另一种状态转换的可能性，例如不能从Running转换为ReadyToRun
    StateTransferMap = {WorkStateEnum.ReadyToRun: [WorkStateEnum.Running,
                                                   WorkStateEnum.Paused,
                                                   WorkStateEnum.Stopped,
                                                   WorkStateEnum.Terminated,
                                                   WorkStateEnum.TokenCatched],
                        WorkStateEnum.Running: [WorkStateEnum.Paused,
                                                WorkStateEnum.Completed,
                                                WorkStateEnum.Aborted,
                                                WorkStateEnum.Stopped,
                                                WorkStateEnum.Terminated],
                        WorkStateEnum.Paused: [WorkStateEnum.Restarted,
                                               WorkStateEnum.Stopped,
                                               WorkStateEnum.Terminated],
                        WorkStateEnum.Restarted: [WorkStateEnum.Paused,
                                                  WorkStateEnum.Completed,
                                                  WorkStateEnum.Aborted,
                                                  WorkStateEnum.Stopped,
                                                  WorkStateEnum.Terminated],
                        WorkStateEnum.Completed: None,
                        WorkStateEnum.Aborted: None,
                        WorkStateEnum.Stopped: None,
                        WorkStateEnum.Terminated: None,
                        WorkStateEnum.Unknown: [WorkStateEnum.ReadyToRun],
                        WorkStateEnum.TokenCatched: [WorkStateEnum.Running],
                        WorkStateEnum.TokenReleased: [WorkStateEnum.Completed,
                                                      WorkStateEnum.Aborted,
                                                      WorkStateEnum.Stopped,
                                                      WorkStateEnum.Terminated]}

    def __init__(self,name, id):

        self.work_name = name
        self.work_id = id

        # 记录当前的工作状态的列表。
        self.states = []
        self.currentState = WorkStateEnum.Unknown
        pass  # def __init__(self)

    def setWorkerState(self, stateValue):
        """
        记录当前的工作状态
        """
        # 检查状态是否能够进行转换，如果不能，将抛出错误
        if self.canTransferState(stateValue):
            state_name = WorkStateEnum.getName(stateValue)
            if state_name is None:
                raise ValueError('WorkStateEnum has no such value!')
            logger.debug("%s(%s) %s, Time:%s" % (self.work_name,self.work_id, state_name, datetime.datetime.now()))

            # 记录当前状态
            self.currentState = stateValue
            # 追加当前状态到记录表
            self.states.append(WorkStateInfo(len(self.states), stateValue))

        pass  # def setWorkerState(self,stateValue)

    def canTransferState(self, targetState, raiseExcption=True):
        """
        检查状态是否能够进行转换，如果不能，将返回False或抛出错误
        :rawParam targetState:要转换的状态。
        :rawParam raiseExcption:是否抛出错误(默认为True)。
        :return:
        """
        curState = self.getCurrentWorkerState()  # 取得当前状态
        states = self.StateTransferMap.get(curState, None)  # 查看当前状态可转换的状态列表
        if states:
            if targetState in states:
                return True  # 如果在可转换状态列表中，返回True

        if raiseExcption:  # 如果不在可转换状态列表中，并且需要抛出错误，抛出
            raise WorkerStateNotTransferrableError('Can not tranfer current workmanager state %s to %s' % \
                                                   (
                                                   WorkStateEnum.getName(curState), WorkStateEnum.getName(targetState)))

        return False

        pass  # def  canTransferState(self,targetState,raiseExcption=True)

    def getCurrentWorkerState(self):
        """
        取得当前对象的工作状态（状态列表中的最后一个）
        """
        return self.currentState
        # return self.states[len(self.states )]

        pass  # def getCurrentWorkerState(self)

    def getLastDuration(self):
        """
        取得最后一次状态变化的持续时间。
        例如从暂停到恢复的时间。
        """

        if len(self.states) < 2:
            return 0

        time_start = self.states[len(self.states) - 2].time
        time_end = self.states[len(self.states) - 1].time

        # dur=(timeend - timestart).seconds+(timeend - timestart).microseconds / 1000
        return time_end - time_start
        pass  # def getLastDuration(self)

    def getWorkerStateInfos(self, state):
        """
        根据指定的工作状态取得相同的对象的工作状态的包装类
        例如：可以用来查看当前对象的暂停次数。
        """
        infos = []
        for info in self.states:
            if info.state == state:
                infos.append(info)
        return infos

        pass  # def getWorkerStateInfos(self,state)

    pass  # class WorkerStateInfos


class WorkStateRecordable(object):
    """
    可以记录对象运行状态的基础类（必须重载或继承）。
    """

    def __init__(self, name, id):
        if not name:
            if not id:
                id = str(uuid.uuid1()).replace("-", "")
            name = id
        elif not id:
            id = name
        self.name = name
        self.id = id
        # 记录状态的迁移过程
        self.workerStateInfos = WorkerStateInfos(self.name,self.id)
        # 设置线程状态
        self.workerStateInfos.setWorkerState(WorkStateEnum.ReadyToRun)

        pass  # def __init__(self)

    pass  # class WorkStateRecordable(object)
