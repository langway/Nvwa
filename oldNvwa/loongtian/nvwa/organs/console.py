#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    console 
Author:   Liuyl 
DateTime: 2014/12/10 15:20 
UpdateLog:
1、Liuyl 2014/12/10 Create this File.

console
>>> print("No Test")
No Test
"""
__author__ = 'Liuyl'
from loongtian.nvwa.common.utils.tcp import TcpClient, TcpClientReceiveListener
from loongtian.nvwa.common.config import conf
from loongtian.nvwa.common.threadpool.runnable import Runnable, run
from loongtian.nvwa.organs.brain import Brain
import threading
if __name__ == '__main__':
    # brain = Brain()
    # brain.run()
    #
    # threading ._sleep(20000)

    _client = TcpClient(conf['brain']['console_ip'], conf['brain']['console_port'])
    run(TcpClientReceiveListener(_client, '[nvwa]: '))
    Runnable.pool.poll()
    while True:
        _input = raw_input()
        if _input == '--':
            _client.shutdown()
            break
        _client.send(_input + '\n')