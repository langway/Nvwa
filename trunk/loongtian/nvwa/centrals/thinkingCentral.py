# /usr/bin/python
# coding: utf-8
__author__ = 'Leon'

from loongtian.util.log import logger
from loongtian.nvwa.centrals.centralBase import CentralBase
from loongtian.nvwa.engines.modelingEngine import ModelingEngine
from loongtian.nvwa.engines.transitionEngine import TransitionEngine
from loongtian.nvwa.engines.groupEngine import GroupEngine
from loongtian.nvwa.engines.compareEngine import CompareEngine
from loongtian.nvwa.engines.abstractEngine import AbstractEngine
from loongtian.nvwa.managers.mindsManager import MindsManager
from loongtian.nvwa.runtime.systemInfo import ThinkingInfo


# todo 下面的引擎/中枢暂时先放在这里，未来需要考虑是否需要放在brain之中
from loongtian.nvwa.engines.evaluateEngine import EvaluateEngine
from loongtian.nvwa.engines.emotionEngine import EmotionEngine
from loongtian.nvwa.engines.planEngine import PlanEngine
from loongtian.nvwa.engines.executeEngine import ExecuteEngine

"""
思维中枢
"""


class ThinkingCentral(CentralBase):
    """
    思维中枢
    """

    def __init__(self, brain):
        """
        思维中枢
        :param brain:
        """
        super(ThinkingCentral, self).__init__(brain)

        self.ModelingEngine = ModelingEngine(self)  # 建模引擎
        self.GroupEngine = GroupEngine(self)  # 分组引擎
        self.TransitionEngine = TransitionEngine(self)  # 迁移引擎
        self.MindsManager = MindsManager(self)  # 多思维的管理器，产生并管理上下文
        self.CompareEngine = CompareEngine(self)  # 比较引擎。用来对任意两个对象进行比较，并输出其关联关系
        self.AbstractEngine = AbstractEngine(self)  # 抽象引擎。将n个对象的构成归纳合并，具有相同的，将生成一个相同的父对象。

        # todo 下面的引擎/中枢暂时先放在这里，未来需要考虑是否需要放在brain之中
        self.EvaluateEngine = EvaluateEngine(self.Brain.MemoryCentral)
        self.EmotionEngine = EmotionEngine(self.Brain.MemoryCentral)
        self.PlanEngine = PlanEngine(self.Brain.MemoryCentral)
        self.ExecuteEngine = ExecuteEngine(self.Brain.MemoryCentral)

    def thinkStringInput(self,str_input):
        """
        对字符串输入进行思考。
        :param str_input:
        :return:
        """
        if not str_input or (not isinstance(str_input,str) and not isinstance(str_input,unicode)):
            raise Exception("必须提供字符串以进行思考！")

        # 创建Mind，真正开始思考
        mind = self.MindsManager.createMind(str_input)
        thinkResult = mind.execute()
        return thinkResult




    def thinkParentsConfusion(self, *parentsConfusion):
        """
        将父对象困惑送入nvwa大脑进行进一步思维（当前思维线程暂停，等待结果）
        :param parentsConfusion:
        :return:
        """
        raise NotImplementedError

    def evaluateUnderstood(self, thinkResult):
        """
        对“理解”思维的结果进行评估
        :param thinkResult:
        :return:
        """
        # 设置Mind的执行信息
        thinkResult.setMindExecuteRecord(ThinkingInfo.MindExecuteInfo.Evaluating_Undertood)

        return self.EvaluateEngine.evaluate(thinkResult)

    def calculateEmotion(self, thinkResult):
        """
        对“评估”的结果进行情感计算
        :param thinkResult:
        :return:
        """
        # 设置Mind的执行信息
        thinkResult.setMindExecuteRecord(ThinkingInfo.MindExecuteInfo.Calculating_Emotion)

        return self.EmotionEngine.calculate(thinkResult)

    def createPlan(self, thinkResult):
        """
        根据“情感计算”的结果制定行为计划
        :param thinkResult:
        :return:
        """
        # 设置Mind的执行信息
        thinkResult.setMindExecuteRecord(ThinkingInfo.MindExecuteInfo.Creating_Plan)

        return self.PlanEngine.plan(thinkResult)

    def executeBehaviour(self, thinkResult):
        """
        执行行为
        :param thinkResult:
        :return:
        """
        # 设置Mind的执行信息
        thinkResult.setMindExecuteRecord(ThinkingInfo.MindExecuteInfo.Executing_Behaviour)

        return self.ExecuteEngine.execute(thinkResult)
