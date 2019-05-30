#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

from loongtian.nvwa.engines.engineBase import EngineBase
from loongtian.util.log import logger


class ForgetEngine(EngineBase):
    """
    遗忘引擎
    :rawParam
    :attribute
    MEMORYTIMES 记忆次数，达到记忆次数之后，将达到记忆残留度最大值。
    FORGETDAY 遗忘天数，经过遗忘天数之后会遗忘掉。
    POWER 指数系数
    AMPLIFICATION 放大系数
    CORRECTION 修正系数
    跟RecognizeEngine一样，由系统调用
    """
    MEMORYTIMES = 3
    FORGETDAY = 100
    POWER = 0.125
    AMPLIFICATION = round(100.0 / MEMORYTIMES, 2)
    CORRECTION = 0.568 / MEMORYTIMES

    def __init__(self,memory):
        """
        情感引擎引擎。用来评估“预期”与输入、输出结果对“我”的“价值”之间的差异，以及环境对输出结果反应对“我”的“价值”
        :param memory: 用来存放当前对象的内存空间（避免每次都从数据库中调用）
                       当前ForgetEngine的memory是MemoryCentral
        """
        super(ForgetEngine, self).__init__(memory)

    @staticmethod
    def getThresholdByDifferenceDate(differenceDate):
        """
        给定相差天数获得阀值（记忆残留度）
        :rawParam differenceDate: 最后一次记忆与当前日期相差的天数
        :return: 记忆残留度
        """
        if differenceDate <= 0:
            return ForgetEngine.AMPLIFICATION
        elif differenceDate > ForgetEngine.FORGETDAY:
            return 0
        else:
            return round(ForgetEngine.AMPLIFICATION * differenceDate ** -ForgetEngine.POWER
                - ForgetEngine.CORRECTION * (differenceDate - 1), 2)

    @staticmethod
    def getDifferenceDateByThreshold(threshold):
        """
        给定阀值（记忆残留度），推算出最后记忆的天数差。
        :rawParam weight: 记忆残留度
        :return: 天数差
        """
        if threshold < 0:
            return ForgetEngine.FORGETDAY
        elif threshold > ForgetEngine.AMPLIFICATION:
            return 0
        else:
            return ForgetEngine._getDifferenceDateByThreshold(threshold, ForgetEngine.FORGETDAY, 0)

    @staticmethod
    def _getDifferenceDateByThreshold(threshold, maxDay, minDay):
        xDay = round(minDay + (maxDay-minDay)/2)
        if xDay == maxDay or xDay == minDay:
            return xDay
        temp = ForgetEngine.getThresholdByDifferenceDate(xDay)
        if temp > threshold:
            return ForgetEngine._getDifferenceDateByThreshold(threshold, maxDay, xDay)
        elif temp < threshold:
            return ForgetEngine._getDifferenceDateByThreshold(threshold, xDay, minDay)
        else:
            return xDay

    @staticmethod
    def thresholdForget(threshold, differenceDate = 1):
        """
        weight--，遗忘设定阀值（记忆残留度）
        :rawParam weight: 原记忆残留度
        :rawParam differenceDate: 最后一次记忆与当前日期相差的天数
        :return: 计算后的记忆残留度
        """
        return ForgetEngine.getThresholdByDifferenceDate(
            ForgetEngine.getDifferenceDateByThreshold(threshold)+differenceDate)

    @staticmethod
    def thresholdMemory(threshold):
        """
        weight++，记忆设定阀值（记忆残留度）
        每次记忆增加33.33%的记忆残留度（重要的事情说三遍）
        :rawParam weight: 原记忆残留度
        :return: 计算后的记忆残留度
        """
        newThreshold = threshold + ForgetEngine.AMPLIFICATION
        if newThreshold > 100:
            return 100.0
        else:
            return newThreshold

    def do_forget(self):
        raise NotImplemented