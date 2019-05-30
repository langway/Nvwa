#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

from SocketServer import StreamRequestHandler

class BaseStreamHandler(StreamRequestHandler):
    """
    流式输入/输出处理器。
    """

    def handle(self):
        while True:
            _msg = self._receive()
            self._send("Receive: {0}  From: {1}:{2}".format(_msg, self.client_address[0], self.client_address[1]))

    def _receive(self):

        _input = self.rfile.readline()
        if _input is None:
            return None
        _input = _input.strip()
        if _input.strip() == '':
            # print("Receive whitespace means that socket connection is closed by client.( From: {0}:{1})".format(
            #     self.client_address[0], self.client_address[1]))
            # do nothing
            pass
        else:
            print("Receive: {0}  From: {1}:{2}".format(_input, self.client_address[0], self.client_address[1]))
        return _input

    def _send(self, output):
        self.wfile.write(output)
        print("Send: {0}  To: {1}:{2}".format(output, self.client_address[0], self.client_address[1]))
