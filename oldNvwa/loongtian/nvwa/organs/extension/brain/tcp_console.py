#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    console_tcp 
Author:   Liuyl 
DateTime: 2014/12/15 10:37 
UpdateLog:
1、Liuyl 2014/12/15 Create this File.

console_tcp
>>> print("No Test")
No Test
"""
# from loongtian.nvwa.core.minds.collection_mind import CollectionCommandSplit
# from loongtian.nvwa.service.fragment_service.fragment_definition.refer import ReferBuilder

__author__ = 'Liuyl'
from loongtian.nvwa.common.utils.tcp import BaseStreamHandler, TcpServerDeaMon
from Queue import Empty
from loongtian.nvwa.common.config import conf
from loongtian.nvwa.core.gdef import GlobalDefine
import time


class ConsoleHandler(BaseStreamHandler):
    def handle(self):
        GlobalDefine().dispenser.register_socket(self.request, self.client_address)
        print('Accept connection {0}'.format(self.client_address))
        while True:
            try:
                _input = self._receive()
            except Exception, e:
                GlobalDefine().dispenser.unregister_socket(self.client_address)
                print('Lost connection {0}[{1}]'.format(self.client_address, e.args[0]))
                break
            if _input is None or _input.strip() == '':
                break
            else:
                _input = _input.decode('utf-8')
                # if ReferBuilder.ReferMark in _input:
                #     GlobalDefine().refer_input_queue.put((_input, self.client_address))
                # #elif CollectionCommandSplit(_input).input_split():
                #  #   GlobalDefine().collection_input_queue.put((_input, self.client_address))
                #     #GlobalDefine().console_input_queue.put((_input, self.client_address))
                # else:
                GlobalDefine().console_input_queue.put((_input, self.client_address))


class ConsoleServerDeaMon(TcpServerDeaMon):
    def __init__(self):
        super(ConsoleServerDeaMon, self).__init__(conf['brain']['console_ip'], conf['brain']['console_port'],
                                                  ConsoleHandler, name='Console')


if __name__ == '__main__':
    import doctest

    doctest.testmod()