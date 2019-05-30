#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

from loongtian.util.common.enum import Enum


class WorkStateEnum(Enum):
    """
    当前任务的工作状态。
    包括：

    """
    # 未知。
    Unknown = 0
    # 准备完毕，可以执行。
    ReadyToRun = 1
    # 正在运行
    Running = 2
    # 正常执行完毕，已经退出
    Completed = 3
    # 被用户（系统）暂停
    Paused = 4
    # 被用户（系统）暂停后继续运行
    Restarted = 5
    # 执行中出现异常，非正常退出
    Aborted = 6
    # 执行中被用户（系统）强行终止，从loop循环终止，数据比较安全
    Stopped = 7
    # 执行中被用户（系统）强行终止，并非从loop循环终止，可能丢失数据
    Terminated = 8
    # 已经捕获Token
    TokenCatched = 9
    # 已经释放Token
    TokenReleased = 10

    pass  # class WorkStateEnum(Enum)


# WorkerStateEnum的实例。
WorkStateEnum = WorkStateEnum()
