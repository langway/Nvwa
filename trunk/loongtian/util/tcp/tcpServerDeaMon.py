#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

from loongtian.util.tcp.tcpServer import TcpServer
from loongtian.util.tasks.runnable import Runnable


class TcpServerDeaMon(Runnable):

    def __init__(self, host, port, handler, server_type=TcpServer, name=None):
        super(TcpServerDeaMon, self).__init__()
        if not name:
            self._name = 'TcpServerDeaMon({0}:{1})'.format(host, port)
        else:
            self._name = 'TcpServerDeaMon({0}[{1}:{2}])'.format(name, host, port)
        self.server = server_type(host, port, handler, name)

    def _execute(self):
        self._sub_threads = [self.server]
        super(TcpServerDeaMon, self)._start_sub_threads()
        while True:
            if not self.state():
                break
