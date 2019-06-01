#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    tcp 
Author:   Liuyl 
DateTime: 2014/12/10 15:27 
UpdateLog:
1、Liuyl 2014/12/10 Create this File.

tcp
>>> print("No Test")
No Test
"""
import time

__author__ = 'Liuyl'
from socket import *
from loongtian.nvwa.common.threadpool.runnable import Runnable, run
from Queue import Queue
import SocketServer

BUFFER_SIZE = 1024


class BaseHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        _msg = self._receive()
        self._send("Receive: {0}  From: {1}:{2}".format(_msg, self.client_address[0], self.client_address[1]))

    def _receive(self):
        _input = self.request.recv(BUFFER_SIZE).strip()
        print("Receive: {0}  From: {1}:{2}".format(_input, self.client_address[0], self.client_address[1]))
        return _input

    def _send(self, output):
        self.request.send(output)
        print("Send: {0}  To: {1}:{2}".format(output, self.client_address[0], self.client_address[1]))


class BaseStreamHandler(SocketServer.StreamRequestHandler):
    def handle(self):
        while True:
            _msg = self._receive()
            self._send("Receive: {0}  From: {1}:{2}".format(_msg, self.client_address[0], self.client_address[1]))

    def _receive(self):
        _input = self.rfile.readline()
        _input = _input.strip()
        if _input is None or _input.strip() == '':
            print("Receive whitespace means that socket connection is closed by client.( From: {0}:{1})".format(
                self.client_address[0], self.client_address[1]))
        else:
            print("Receive: {0}  From: {1}:{2}".format(_input, self.client_address[0], self.client_address[1]))
        return _input

    def _send(self, output):
        self.wfile.write(output)
        print("Send: {0}  To: {1}:{2}".format(output, self.client_address[0], self.client_address[1]))


class TcpServer(Runnable):
    def __init__(self, host, port, handler, name=None):
        super(TcpServer, self).__init__()
        if not name:
            self._name = 'TcpServer({0}:{1})'.format(host, port)
        else:
            self._name = 'TcpServer({0})'.format(name)
        self.server = SocketServer.ThreadingTCPServer((host, port), handler)

    def _execute(self):
        self.server.serve_forever()

    def stop(self):
        self.server.shutdown()


class TcpServerDeaMon(Runnable):
    def __init__(self, host, port, handler, server_type=TcpServer, name=None):
        super(TcpServerDeaMon, self).__init__()
        if not name:
            self._name = 'TcpServerDeaMon({0}:{1})'.format(host, port)
        else:
            self._name = 'TcpServerDeaMon({0})'.format(name)
        self.server = server_type(host, port, handler, name)

    def _execute(self):
        self._sub_threads = [self.server]
        super(TcpServerDeaMon, self)._start_sub_threads()
        while True:
            if not self.state():
                break


class TcpClient(object):
    def __init__(self, host, port):
        super(TcpClient, self).__init__()
        self.__host = host
        self.__port = port
        self._client = socket(AF_INET, SOCK_STREAM)
        self.is_connected = False
        try:
            self._client.connect((self.__host, self.__port))
            self.is_connected = True
            print('Connect to {0}'.format((self.__host, self.__port)))
        except Exception, e:
            print('Can not connect to {0}[{1}]'.format((self.__host, self.__port), e.args[0]))

    def send(self, msg):
        try:
            if not self.is_connected:
                try:
                    self._client = socket(AF_INET, SOCK_STREAM)
                    self._client.connect((self.__host, self.__port))
                    self.is_connected = True
                    print('Reconnect to {0}'.format((self.__host, self.__port)))
                except Exception, e:
                    print('Can not connect to {0}[{1}]'.format((self.__host, self.__port), e.args[0]))
                    self.is_connected = False
                    return
            self._client.send(msg)
        except Exception, e:
            print('Lost connection {0}[{1}]'.format((self.__host, self.__port), e.args[0]))
            self.is_connected = False

    def recv(self):
        try:
            if self.is_connected:
                return self._client.recv(1024)
            else:
                time.sleep(1)
                return ''
        except Exception, e:
            print('Lost connection {0}[{1}]'.format((self.__host, self.__port), e.args[0]))
            self.is_connected = False
            raise e

    def shutdown(self):
        self._client.close()


class TcpClientReceiveListener(Runnable):
    def __init__(self, client, prompt=''):
        super(TcpClientReceiveListener, self).__init__()
        self.client = client
        self._name = 'TcpClientReceiveListener'
        self.prompt = prompt
        #raw_input('>>>')

    def _execute(self):
        while True:
            try:
                _output = self.client.recv()
                if _output != '':
                    print(self.prompt + _output)
                    #raw_input('>>>')
            except Exception, e:
                continue
            if not self.state():
                break

