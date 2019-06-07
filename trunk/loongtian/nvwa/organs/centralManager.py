#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

from queue import Queue
from loongtian.util.common.priorityQueue import PriorityQueue
from loongtian.util.common.singleton import *


from loongtian.nvwa.organs.userDispenser import UserDispenser


@singleton
class _centralManager(object):
    """
    女娲中央大脑的全局变量定义管理器（这是女娲中央大脑调用的全局变量，单例模式）
    """

    def __init__(self):
        """
        全局变量定义管理器（这是女娲中央大脑调用的全局变量，单例模式）
        """
        self.CentralBrain = None
        self.user_dispenser = UserDispenser()
        self.console_input_queue = Queue()
        self.console_output_queue = Queue()
        self.command_msg = PriorityQueue()

        self.users = {}  # {"userip:userport":user} 已经建立连接的用户
        self.brains = {}  # {"userip:userport":brain} 已经建立连接的用户大脑

    def getUserBrain(self, msgInfo, clientHandler):
        """
        取得/创建客户对应的女娲大脑（服务器端）
        :return:
        """
        _brain = self.brains.get(msgInfo.client_address)  # 如果已经创建了，直接返回结果
        if _brain:
            return _brain

        from loongtian.nvwa.organs.brain import Brain
        # 查找已经登录的用户
        _user = self.users.get(msgInfo.client_address)
        if _user:  # 如果用户已经登录
            # 根据用户创建用户大脑
            _brain = Brain(_user, self.CentralBrain)
        else:  # 如果未登录，要求登或注册
            _user = clientHandler.logon(msgInfo)
            if not _user:
                raise Exception("未知的用户，无法创建女娲大脑以进行思考！")

            _user.client_address.add(msgInfo.client_address)

            self.users[msgInfo.client_address] = _user
            # 根据用户创建用户大脑
            _brain = Brain(_user, self.CentralBrain)

        # 初始化用户大脑
        _brain.init()
        # 添加到用户大脑列表
        self.brains[msgInfo.client_address] = _brain
        # 启动用户大脑
        from loongtian.util.tasks.runnable import run
        run(_brain)
        return _brain

    def response(self, output, client_address):
        """
        向指定的用户地址输出信息
        :param output:信息
        :param client_address:用户地址
        :return:
        """
        _socket = self.user_dispenser.socket_dict.get(client_address)
        if _socket:
            _socket.send(output.encode())
            print('Send: {0} To:{1}'.format(output, client_address))

    def _cleanDB(self, wait_for_command=True):
        """
        [慎用]完全删除数据库中的所有记录。操作将使本Nvwa智能不再具有既往知识！[慎用]
        :return:
        """
        do_clean = False
        if wait_for_command:
            if input("危险警告：本操作将完全删除数据库中的所有记录！！！\r\n" +
                         "继续操作将使本Nvwa智能不再具有既往知识！！！\r\n" +
                         "Warning:This Operation will DELETE all records in DB!\r\n " +
                         "Continue will take any knowledges away from NVWA AI!\r\n" +
                         "请输入：yes 继续！no/quit退出！！\r\n>>").lower() == "yes":
                do_clean = True
        else:
            do_clean = True

        if do_clean:
            from loongtian.nvwa.tools.db import DbPools
            from loongtian.nvwa.settings import db
            DbPools[db.db_nvwa].executeSQL([
                "delete from \"%s\"" % db.tables.tbl_metaData,
                "delete from \"%s\"" % db.tables.tbl_metaNet,
                "delete from \"%s\"" % db.tables.tbl_realObject,
                "delete from \"%s\"" % db.tables.tbl_knowledge,
                "delete from \"%s\"" % db.tables.tbl_layer,
            ])

            DbPools[db.db_auth].executeSQL([
                "delete from \"%s\"" % db.tables.tbl_users,
                "delete from \"%s\"" % db.tables.tbl_locations,

            ])


CentralManager = _centralManager()
