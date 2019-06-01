#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    tcp_server_test 
Author:   Liuyl 
DateTime: 2014/12/11 9:05 
UpdateLog:
1、Liuyl 2014/12/11 Create this File.

tcp_server_test
>>> print("No Test")
No Test
"""
__author__ = 'Liuyl'
from Queue import Queue
from loongtian.nvwa.common.utils.tcp import TcpServer
if __name__ == '__main__':
    _host = '127.0.0.1'
    _port = 8077
    _server_queue = Queue()
    _server = TcpServer(_host, _port, _server_queue)
    _server.run()