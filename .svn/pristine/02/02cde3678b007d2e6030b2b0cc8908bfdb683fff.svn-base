#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

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

