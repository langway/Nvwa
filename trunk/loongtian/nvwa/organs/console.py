#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

import Queue
import threading
import time
from loongtian.util.tcp.tcpClient import TcpClient
from loongtian.util.tcp.tcpClientReceiveListener import TcpClientReceiveListener
from loongtian.util.tasks.runnable import Runnable, run, default_shutdown_commands

from loongtian.nvwa.runtime.msgInfo import MsgInfo
from loongtian.nvwa.settings import auth


class Console(Runnable):
    """
    输入输出控制台（客户端）
    """

    def __init__(self, server_ip, server_port, prompt='[nvwa]: ', shutdown_commands=None):
        """
        输入输出控制台（客户端）
        :param user: 用户
        :param prompt: 提示词
        :param shutdown_commands:关闭控制台的输入（默认为"--","exit","shutdown"）
        """
        super(Console, self).__init__()
        self._name = 'Console(Sever [%s:%d])' % (server_ip, server_port)

        # 设置通信模块
        self._client = TcpClient(server_ip, server_port)
        self.listener = TcpClientReceiveListener(self._client, prompt)
        run(self.listener)
        Runnable.pool.poll()

        # 设置关闭线程的命令符
        if not shutdown_commands:
            shutdown_commands = default_shutdown_commands
        self.shutdown_commands = shutdown_commands

        self._msgInfo = MsgInfo()
        self._msgInfo.facility = 100  # 100-输入输出面板；200-webpage；300-Android；400-iOS

    def _execute(self):
        """
        [重载函数]重写父线程执行方法
        """
        # 首先登录
        if not self.logon():
            raise Exception("未能正确进行用户登录！")

        # 等待用户输入
        while True:
            canbreak=self.processInput()
            if canbreak:
                break
            time.sleep(0.001)


    def processInput(self):
        """
        处理用户输入
        :return:
        """
        _input = raw_input()  # ("[%s]:" % self._user.username)
        if _input is None or _input.strip() == "":  # 如果没有输入，不进行任何处理
            return False
        if _input in self.shutdown_commands:
            self.logout()
            self._client.shutdown()
            return True
        self._msgInfo.msg = _input
        # 消息发送步骤：0、客户端输入，发送往服务器端，等待ClientHandler处理
        self._client.send(self._msgInfo.toStr() + '\r\n')  # 一个下午！！！必须加'\r\n'，不知道为什么

    def logon(self):
        """
        用户登录（发送登录信息，以建立女娲大脑用于后续）
        :return:
        """
        self._msgInfo.msg = auth.message.logon_msg
        # 消息发送步骤：0、客户端输入，发送往服务器端，等待ClientHandler处理
        self._client.send(self._msgInfo.toStr() + '\r\n')  # 一个下午！！！必须加'\r\n'，不知道为什么

        return True

    def logout(self):
        """
        用户登出（发送登出信息，以销毁用户及女娲大脑）
        :return:
        """
        self._msgInfo.msg = auth.message.logout_msg
        # 消息发送步骤：0、客户端输入，发送往服务器端，等待ClientHandler处理
        self._client.send(self._msgInfo.toStr() + '\r\n')  # 一个下午！！！必须加'\r\n'，不知道为什么
        self._client.recv()
        return True

class HttpConsole(Console):
    """
    HTTP的输入输出控制台
    """

    def __init__(self, server_ip, server_port):
        super(HttpConsole, self).__init__(server_ip, server_port, prompt="")

        self.input_queue = Queue.Queue()
        self._lock = threading.Lock()
        self._msgInfo.facility = 200  # 100-输入输出面板；200-webpage；300-Android；400-iOS

    def _execute(self):
        """
        [重载函数]重写父线程执行方法
        消息传送步骤：0、客户端输入，发送往服务器端，等待ClientHandler处理
        """
        # 首先登录
        self.logon()

        # 等待用户输入
        while True:
            self._lock.acquire()
            if self.input_queue.empty():
                self._lock.release()
                continue
            _input = self.input_queue.get()
            self._lock.release()

            if self._msgInfo.msg is None or self._msgInfo.msg.strip() == "":  # 如果没有输入，不进行任何处理
                continue
            if self._msgInfo.msg in self.shutdown_commands:
                self._client.shutdown()
                break
            self._msgInfo.msg = _input
            self._client.send(self._msgInfo.toStr()+ '\r\n')  # 一个下午！！！必须加'\r\n'，不知道为什么


