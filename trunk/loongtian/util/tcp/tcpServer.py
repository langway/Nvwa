#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

import socketserver
from loongtian.util.tasks.runnable import Runnable

class TcpServer(Runnable):
    def __init__(self, host, port, handler, name=None):
        super(TcpServer, self).__init__()
        if not name:
            self._name = 'TcpServer({0}:{1})'.format(host, port)
        else:
            self._name = 'TcpServer({0}[{1}:{2}])'.format(name,host, port)
        self.server = socketserver.ThreadingTCPServer((host, port), handler)


    def _execute(self):
        self.server.serve_forever()

    def stop(self):
        self.server.shutdown()

