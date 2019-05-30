#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

import time
from socket import socket, AF_INET, SOCK_STREAM


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
                time.sleep(0.001)
                return ''
        except Exception, e:
            print('Lost connection {0}[{1}]'.format((self.__host, self.__port), e.args[0]))
            self.is_connected = False
            raise e

    def shutdown(self):
        self._client.close()
