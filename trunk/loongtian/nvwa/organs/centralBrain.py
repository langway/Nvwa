#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

import time

from loongtian.util.tasks.runnable import Runnable, run
from loongtian.util.tcp.baseStreamHandler import BaseStreamHandler
from loongtian.util.tcp.tcpServerDeaMon import TcpServerDeaMon

from loongtian.nvwa.settings import auth
from loongtian.nvwa.runtime.msgInfo import MsgInfo
from loongtian.nvwa.runtime.reals import AdminUser

from loongtian.nvwa.organs.centralMemory import CentralMemory
from loongtian.nvwa.organs.centralManager import CentralManager

from loongtian.nvwa.managers.schedulesManager import SchedulesManager

from loongtian.nvwa.engines.forgetEngine import ForgetEngine
from loongtian.nvwa.engines.recognizeEngine import RecognizeEngine
from loongtian.nvwa.engines.knowledgeMeaningEngine import KnowledgeMeaningEngine

import loongtian.auth.logon as logon


class CentralBrain(Runnable):
    """
    女娲中央大脑。
    由于使用了GlobalDefines的单例模式，所以可以统一调度
    每个用户登录后均有一个自己的大脑，为其处理单独的信息。
    中央大脑负责对每个用户的大脑进行管理，相当于多个大脑的管理器。
    """

    def __init__(self):
        """
        女娲中央大脑。
        """
        super(CentralBrain, self).__init__()
        self._name = "女娲中央大脑（CentralBrain）"
        # 执行子线程
        self._sub_threads = []


        # 中央大脑的记忆中枢（用来管理永久记忆）
        self.CentralMemory = CentralMemory(self)

        # 女娲中央大脑的全局变量定义管理器（这是女娲中央大脑调用的全局变量）
        self.CentralManager = CentralManager  # 单例模式,
        self.CentralManager.CentralBrain = self

        self.SchedulesManager = SchedulesManager("")  # 计划任务管理器

        # 超级管理账户。必须在女娲大脑创建并初始化了记忆中枢之后才能创建超级管理账户，否则，直觉对象等会不受管辖
        self.AdminUser = None

    def init(self):
        """
        女娲中央大脑初始化
        :return:
        """
        self.CentralMemory.init()  # 初始化记忆中枢。
        # 必须在女娲大脑创建并初始化了记忆中枢之后才能创建超级管理账户，否则，直觉对象等会不受管辖
        self.AdminUser=AdminUser.getAdminUser(self.CentralMemory)
        # self.startSchedulesManager() # 启动计划任务管理器 todo 待完成

    def startSchedulesManager(self):
        """
        启动计划任务管理器
        :return:
        :remarks:
        目前包括：
        （1）遗忘引擎
        （2）实际对象/知识链 识别率引擎
        （3）知识链意义折叠引擎
        """
        # todo 需要与SchedulesManager合并
        from apscheduler.schedulers.background import BackgroundScheduler
        sched = BackgroundScheduler()
        sched.daemonic = True
        forgetEngine = ForgetEngine(None)
        recognizeEngine = RecognizeEngine(None)
        knowledgeMeaningEngine = KnowledgeMeaningEngine(None)

        sched.add_job(forgetEngine.do_forget(), trigger='cron', day_of_week='*', hour='*', minute='*/5', second='1')
        sched.add_job(recognizeEngine.do_recognize(), trigger='cron', day_of_week='*', hour='2', minute='*', second='1')
        sched.add_job(knowledgeMeaningEngine.do_dominanceMeaningsToRecessivity(), trigger='cron', day_of_week='*',
                      hour='2', minute='*', second='1')

        self.SchedulesManager.add(forgetEngine)
        self.SchedulesManager.start()

    def _execute(self):
        """
        重写父线程方法
        """
        CentralManager.user_dispenser.register_queue(CentralManager.console_input_queue)
        CentralManager.user_dispenser.register_queue(CentralManager.console_output_queue)
        # 执行子线程
        self._sub_threads = [
            self.getAdminServerDeaMon(),
            CentralManager.user_dispenser,
            # self.init(), # 女娲中央大脑初始化
        ]
        # map(lambda t: run(t), self._sub_threads)
        # 启动子线程，并put到线程池中。
        for _sub_thread in self._sub_threads:
            run(_sub_thread)
        Runnable.pool.poll()  # 通过线程池管理子线程，poll实现异步执行模式。

        # 等待处理，如果state为False退出。
        while True:
            if not self.state():
                break
            time.sleep(0.001)


    def getAdminServerDeaMon(self):
        """
        创建管理员对应的输入输出控制台的守护/监控（服务器端）
        :return:
        """
        if hasattr(self, "admin_console_deamon"):
            return self.admin_console_deamon

        # console输入-输出控制台服务器的守护进程。
        self.admin_console_deamon = ClientServerDeaMon(auth.adminUser)  # console输入-输出控制台服务器的守护进程。

        return self.admin_console_deamon

class ClientHandler(BaseStreamHandler):
    """
    客户端信息处理器
    """

    def handle(self):
        """
        [消息传送步骤]1、服务器端接收Console客户端输入，
        放入CentralManager.console_input_queue消息队列（已在UserDispenser中注册），
        等待UserDispenser处理
        :return:
        """
        _str_address="%s:%s" % (self.client_address[0],self.client_address[1])
        # 由于dispenser是CentralBrain的类属性，所以可以统一调度
        CentralManager.user_dispenser.register_socket(self.request,_str_address )
        CentralManager.user_dispenser.register_client_handler(self, _str_address)

        print('Accept connection {0}'.format(self.client_address))

        # 等待用户输入
        while True:
            # 循环以等待接受信息（返回的是MsgInfo）。
            _receive = self.waitForReceive(returnMsgInfo=True)
            if not _receive:
                time.sleep(0.001)
                continue
            if _receive.msg==auth.message.logon_msg:
                # 首先登录
                real_user = self.logon(_receive)
                if not real_user:
                    raise Exception("未能正确登录或创建用户后登录！")

                # 注册用户到CentralManager
                CentralManager.users[_str_address]=real_user
            elif _receive.msg==auth.message.logout_msg:
                # 登出用户,CentralManager
                real_user =CentralManager.users.pop(_str_address,None)
                CentralManager.brains.pop(_str_address, None)
                CentralManager.user_dispenser.unregister_socket(_str_address)
                CentralManager.user_dispenser.unregister_client_handler(_str_address)
                if real_user:
                    self._send("用户%s已成功退出..." % real_user.getShowName())
                else:
                    self._send("用户已成功退出...")
                break
            else:
                # 1.1、放入消息队列，等待UserDispenser处理
                CentralManager.console_input_queue.put(_receive)
            time.sleep(0.001)

    def waitForReceive(self,returnMsgInfo=True):
        """
        等待接受信息。
        :param returnMsgInfo:True-返回信息包装类,False-返回信息本身
        :return:
        """
        try:
            _receive = self._receive()
        except Exception as e:
            CentralManager.user_dispenser.unregister_socket(self.client_address)
            CentralManager.user_dispenser.unregister_client_handler(self.client_address)

            print('Lost connection {0}[{1}]'.format(self.client_address, e.args[0]))
            return None
        if _receive is None or _receive.strip() == '':
            return None
        _receive = _receive.strip()
        _msgInfo = None
        try:
            _msgInfo = MsgInfo()
            _msgInfo.fromStr(_receive)
            _msgInfo.client_address = "%s:%s" % (self.client_address[0],self.client_address[1])
        except Exception as ex:
            raise Exception("传入的数据并非客户端与服务器端通信信息的包装类！" + str(ex))
        if returnMsgInfo: # 返回信息包装类
            return _msgInfo
        if _msgInfo: # 返回信息本身
            _receive = _msgInfo.msg
        return _receive

    def logon(self,msgInfo):
        """
        进行用户登录
        :return:
        """
        _memory=None
        if CentralManager.CentralBrain:
            _memory=CentralManager.CentralBrain.CentralMemory
        real_user = logon.logon(msgInfo,self,memory=_memory)
        if real_user:
            # 设置用户地址
            real_user.client_address.add(msgInfo.client_address)
        return real_user

class ClientServerDeaMon(TcpServerDeaMon):
    """
    客户端输入-输出服务器的守护进程。
    """

    def __init__(self, user):
        if not user or not getattr(user, "server_ip") or not getattr(user, "server_port"):
            raise Exception("必须提供对应的nvwa大脑及用户信息！")
        super(ClientServerDeaMon, self).__init__(user.server_ip, user.server_port,
                                                 ClientHandler,
                                                 name='Client DeaMon for %s' % user.user_name)
