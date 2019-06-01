#!/usr/bin/env python
# coding: utf-8
"""
多客户端分发模块

Project:  nvwa
Title:    dispenser 
Author:   Liuyl 
DateTime: 2014/12/12 16:07 
UpdateLog:
1、Liuyl 2014/12/12 Create this File.

brain输出的分发线程
>>> print("No Test")
No Test
"""
__author__ = 'Liuyl'
from loongtian.nvwa.common.threadpool.runnable import Runnable


class Dispenser(Runnable):
    '''
    多客户端分发类
    
    queue_list 客户队列列表[queue]
    socket_dict Socket Dict{address : Socket}
    '''
    def __init__(self):
        super(Dispenser, self).__init__()
        self._name = 'Dispenser'
        self.queue_list = list()
        self.socket_dict = dict()

    def unregister_queue(self, queue):
        '''
        删除客户队列列表中的队列
        '''
        self.queue_list.remove(queue)

    def unregister_socket(self, address):
        '''
        删除Socket Dict中的key=address
        '''
        self.socket_dict.pop(address)

    def register_queue(self, queue):
        '''
        增加客户队列列表中的队列
        '''
        self.queue_list.append(queue)

    def register_socket(self, socket, address):
        '''
        增加Socket Dict中的新数据{address : Socket}
        '''
        self.socket_dict[address] = socket

    def _execute(self):
        '''
        重写线程_execute函数
        '''
        while True:
            for _q in self.queue_list:
                while not _q.empty():
                    _output, address = _q.get()
                    _socket = self.socket_dict[address]
                    if isinstance(_output, unicode):
                        _output = _output.encode('utf-8')
                    _socket.send(_output)
                    print('Send: {0} To:{1}'.format(_output,address))
            if not self.state():
                break


if __name__ == '__main__':
    import doctest
    doctest.testmod()