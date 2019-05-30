#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    tcp_client_test 
Author:   Liuyl 
DateTime: 2014/12/11 9:05 
UpdateLog:
1、Liuyl 2014/12/11 Create this File.

tcp_client_test
>>> print("No Test")
No Test
"""
__author__ = 'Liuyl'
from socket import *


class TcpClient(object):
    def __init__(self, host, port):
        super(TcpClient, self).__init__()
        self.__host = host
        self.__port = port

    def send(self, msg):
        _client = socket(AF_INET, SOCK_STREAM)
        _client.connect((self.__host, self.__port))
        _client.send(msg)
        received = _client.recv(1024)
        _client.close()
        return received


if __name__ == '__main__':
    _host = '192.168.1.30'
    _port = 8077
    _client = TcpClient(_host, _port)
    while True:
        _input = raw_input('>')
        _output = _client.send(_input)
        print('>{0}'.format(_output))