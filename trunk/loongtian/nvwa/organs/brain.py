#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

from queue import Queue
from loongtian.util.log import logger
from loongtian.util.tasks.runnable import Runnable

from loongtian.nvwa.runtime.ipAddress import IPAddressList
from loongtian.nvwa.centrals.memoryCentral import MemoryCentral
from loongtian.nvwa.centrals.perceptionCentral import PerceptionCentral
from loongtian.nvwa.centrals.thinkingCentral import ThinkingCentral

from loongtian.nvwa.organs.character import PersonalCharacter


class Brain(Runnable):
    """
    Nvwa大脑（如果没有user，自动使用系统的超级管理员账户）。
    :rawParam
    构造函数参数说明
    :attribute
    对象属性说明
    """

    def __init__(self, user=None, centralBrain=None):
        """
        Nvwa大脑（如果没有user，自动使用系统的超级管理员账户）。
        :param user: 当前的用户（realUser）。
        :param centralBrain: 中央大脑。
        """
        super(Brain, self).__init__()

        self.CentralBrain = centralBrain  # 中央大脑
        self.User = user
        self.client_address = None

        self.inputQueue = Queue()  # 输入信息的队列，在_execute中处理
        # 性格。女娲AI的个性设置，例如：对事物的激活度（决定联想力等）、遗忘程度、分词的邻接元数等
        self.Character = PersonalCharacter(self)  # 这行代码应该放在中枢创建之前，否则会出现错误

        self.MemoryCentral = MemoryCentral(self)  # 记忆中枢
        self.PerceptionCentral = PerceptionCentral(self)  # 感知中枢
        self.ThinkingCentral = ThinkingCentral(self)  # 思维中枢

    def setClientAddress(self, client_address):
        self.client_address = client_address
        if self.User:
            if self.client_address:
                self._name = "Brain for user:%s(%s)" % (self.User.username, self.client_address)
            else:
                self._name = "Brain for user:%s" % self.User.username
        else:
            self._name = "Brain"

    def init(self):
        """
        系统初始化。
        :return:
        """
        # 初始化记忆中枢。
        self.MemoryCentral.init()
        # 初始化用户。
        self.initUser()
        # 加载个性化性格
        self.Character.init()

    def initUser(self):
        """
        初始化用户。
        :return:
        :remarks:
        1、如果已经设置了用户，直接返回
        2、如果提供了中央大脑，
        """
        if self.User:
            return
        # 必须在女娲大脑创建了记忆中枢之后才能创建超级管理账户，否则，直觉对象等会不受管辖
        from loongtian.nvwa.runtime.reals import AdminUser
        if self.CentralBrain:
            if not self.CentralBrain.AdminUser:
                self.CentralBrain.AdminUser = AdminUser.getAdminUser(self.CentralBrain.CentralMemory)
            user = self.CentralBrain.AdminUser
        else:
            user = AdminUser.getAdminUser(self.MemoryCentral)
        if not user:
            raise Exception("必须提供用户以创建女娲大脑！")

        self.User=user

    def _execute(self):
        """
        重写线程_execute函数
        """
        while True:
            while not self.inputQueue.empty():
                _input = self.inputQueue.get()
                self.PerceptionCentral.receive(_input)
            if not self.state():
                break

    def receive(self, input):
        """
        接收不同感知器官的输入，压入inputQueue，以待后续分别进行处理
        :param input:
        :return:
        """
        self._lock.acquire()
        self.inputQueue.put(input)
        self._lock.release()

    def response(self, output):
        """
        反馈对输入信息的思考结果。
        :param output:
        :return:
        """
        if isinstance(output, str):
            # 根据用户ip进行反馈
            from loongtian.nvwa.organs.centralManager import CentralManager
            CentralManager.response(output, self.client_address)
        elif isinstance(output, list):
            for _output in output:
                self.response(_output)

    def logThinkResult(self, inputs, result):
        """
        记录思考结果。
        :param inputs:
        :param result:
        :return:
        """
        logger.info("当前对‘%s’的思考结果为：%s" % (str(inputs), str(result)))
