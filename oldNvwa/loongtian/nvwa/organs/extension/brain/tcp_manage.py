#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    tcp_manage 
Author:   Liuyl 
DateTime: 2014/12/15 10:38 
UpdateLog:
1、Liuyl 2014/12/15 Create this File.

tcp_manage
>>> print("No Test")
No Test
"""
__author__ = 'Liuyl'
from loongtian.nvwa.core.gdef import GlobalDefine
from loongtian.nvwa.common.utils.tcp import TcpServerDeaMon, BaseStreamHandler
from loongtian.nvwa.common.config import conf


class ManageHandler(BaseStreamHandler):
    def handle(self):
        GlobalDefine().dispenser.register_socket(self.request, self.client_address)
        print('accept connection {0}'.format(self.client_address))
        while True:
            try:
                _input = self._receive()
            except Exception, e:
                GlobalDefine().dispenser.unregister_socket(self.client_address)
                print('lost connection {0}[{1}]'.format(self.client_address, e.args[0]))
                break
            if _input is None or _input.strip() == '':
                continue
            else:
                _input = _input.decode('utf-8')
                GlobalDefine().manage_input_queue.put((_input, self.client_address))


class ManageServerDeaMon(TcpServerDeaMon):
    def __init__(self):
        super(ManageServerDeaMon, self).__init__(conf['brain']['manage_ip'], conf['brain']['manage_port'],
                                                 ManageHandler, name='Manage')


if __name__ == '__main__':
    import doctest

    doctest.testmod()