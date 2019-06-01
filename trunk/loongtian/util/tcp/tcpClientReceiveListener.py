#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

import threading
import queue
from loongtian.util.tasks.runnable import Runnable


class TcpClientReceiveListener(Runnable):

    def __init__(self, client, prompt=''):
        super(TcpClientReceiveListener, self).__init__()
        self.client = client
        self._name = 'TcpClientReceiveListener[%s:%s]' % (self.client._TcpClient__host,self.client._TcpClient__port)
        self.prompt = prompt
        self.output_queue =queue.Queue()
        self._lock =threading.Lock()

    def _execute(self):
        while True:
            try:
                _output = self.client.recv()
                if _output != '':
                    # 压到队列之中
                    self._lock.acquire()
                    self.output_queue.put(_output)
                    self._lock.release()
                    print(self.prompt + _output)
            except Exception as e:
                continue
            if not self.state():
                break
