#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

"""
多客户端分发模块
"""

from loongtian.util.tasks.runnable import Runnable
from loongtian.nvwa.runtime.msgInfo import MsgInfo

class UserDispenser(Runnable):
    """
    多客户端分发类。
    """
    def __init__(self):
        """
        多客户端分发类。
        :param centralManager: 全局变量定义管理器
        """
        super(UserDispenser, self).__init__()
        self._name = 'Dispenser'

        self.queue_list = list() # 客户队列列表[queue]
        self.socket_dict = dict() # Socket Dict{client_address : Socket}

        self.client_handler_dict = {}  # 已经建立连接的用户端信息处理器{client_address:clientHandler}

    def register_queue(self, queue):
        """
        增加客户队列列表中的队列
        """
        self.queue_list.append(queue)

    def unregister_queue(self, queue):
        """
        删除客户队列列表中的队列
        """
        self.queue_list.remove(queue)

    def register_socket(self, socket, client_address):
        """
        增加Socket Dict中的新数据{address : Socket}
        """
        self.socket_dict[client_address] = socket

    def unregister_socket(self, client_address):
        """
        删除Socket Dict中的key=address
        """
        self.socket_dict.pop(client_address,None)

    def register_client_handler(self, client_handler, client_address):
        """
        增加ClientHandler Dict中的新数据{address : ClientHandler}
        """
        self.client_handler_dict[client_address] = client_handler

    def unregister_client_handler(self, client_address):
        """
        删除ClientHandler Dict中的key=address
        """
        self.client_handler_dict.pop(client_address,None)

    def _execute(self):
        """
        重写线程_execute函数
        [消息传送步骤]2、从ClientHandler压入CentralManager.console_input_queue队列的消息中取得消息及用户IP地址
        查找是否已经登录，如未登录，调用登录界面（或发送登录信息）
        """
        while True:
            for _q in self.queue_list:
                while not _q.empty():
                    _input = _q.get()
                    if isinstance(_input, str):
                        _input = _input.encode('utf-8')

                    if isinstance(_input, unicode):
                        _msgInfo = MsgInfo()
                        _msgInfo.fromStr(_input)
                    elif isinstance(_input,MsgInfo):
                        _msgInfo =_input
                    else:
                        raise Exception("不支持的信息类型！")

                    _clientHandler= self.client_handler_dict.get(_msgInfo.client_address)

                    from loongtian.nvwa.organs.centralManager import CentralManager
                    brain = CentralManager.getUserBrain(_msgInfo,_clientHandler)
                    if brain:
                        brain.client_address=_msgInfo.client_address
                        brain.receive(_msgInfo.msg)


            if not self.state():
                break


