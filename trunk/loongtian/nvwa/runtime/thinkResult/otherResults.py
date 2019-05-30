#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Leon'

"""
其他的思考结果，暂时先放在这里等待进一步处理
"""

class ParadigmResult(object):
    """
    [运行时对象]根据范式(上下文)产生的的结果。
    """

    def __init__(self, thinkResult):
        """
        范式(上下文)的结果
        :param thinkResult:思维结果
        """
        self.thinkResult = thinkResult


class AsCollectionResult(object):
    """
    作为集合的思维结果，建立索引，观察顺序，等
    作为单个实际对象的构成结果
    建立索引，例如：牛有1、2、3、4，四条腿，就是输入了4个牛有腿(不同的腿)，然后建立索引，然后输出总数的过程
    """

    def __init__(self, thinkResult):
        """
        作为集合的思维结果，例如：建立索引，观察顺序，等
        :param thinkResult:思维结果
        """
        self.thinkResult = thinkResult


class InSightResult(object):
    """
    系统操作(内观)的结果。
    """

    def __init__(self, thinkResult):
        """
        系统操作(内观)的结果。
        :param thinkResult:思维结果
        """
        self.thinkResult = thinkResult


class AssociationResult(object):
    """
    联想的结果。
    """

    def __init__(self, thinkResult):
        """
        联想的结果。
        :param thinkResult:思维结果
        """
        self.thinkResult = thinkResult


class EvaluationResult(object):
    """
    对“理解”的结果进行评估分析的结果。
    """

    def __init__(self, thinkResult):
        """
        对“理解”的结果进行评估分析的结果。
        :param thinkResult:思维结果
        """
        self.thinkResult = thinkResult


class EmotionResult(object):
    """
    对“评估”结果进行情感计算的情感分析结果。
    """

    def __init__(self, thinkResult):
        """
        对“评估”结果进行情感计算的情感分析结果。
        :param thinkResult:思维结果
        """
        self.thinkResult = thinkResult


class PlanResult(object):
    """
    计划的结果（时间、地点、动作等）。
    """

    def __init__(self, thinkResult):
        """
        计划的结果（时间、地点、动作等）。
        :param thinkResult:思维结果
        """
        self.thinkResult = thinkResult


class BehaviourResult(object):
    """
    根据“情感计算”的结果制定出的行为的执行结果。
    """

    def __init__(self, thinkResult):
        """
        根据“情感计算”的结果制定出的行为的执行结果。
        """
        self.thinkResult = thinkResult
