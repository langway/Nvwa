#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    manage 
Author:   Liuyl 
DateTime: 2014/12/12 13:31 
UpdateLog:
1、Liuyl 2014/12/12 Create this File.

manage
>>> print("No Test")
No Test
"""
import getopt
import sys

__author__ = 'Liuyl'
from loongtian.nvwa.common.utils.tcp import TcpClient, TcpClientReceiveListener
from loongtian.nvwa.common.config import conf
from loongtian.nvwa.common.threadpool.runnable import Runnable, run

def handle_input(input_msg):
    if input_msg.startswith("--god"):
        return do_god(input_msg)
    elif input_msg.startswith("--import "):
        _path = input_msg.lstrip("--import ").strip()
        return do_import(_path)
    else:
        return manage_client.send(_input + '\n')


def handle_opts(opts):
    for name, value in opts:
        if name in ("-g", "--god"):
            handle_input("--god")
        if name in ("-i", "--import"):
            handle_input("--import={0}".format(value))


def do_import(path):
    import codecs
    try:
        #windows下GBK编码文本文件
        _file = codecs.open(path,'r','GBK')
        for line in _file:
            manage_client.send(codecs.encode(line,'UTF-8'))
        print 'imported ' + path
    except IOError,e:
        print('无法打开文件（{0}）'.format((path)))
        return
    finally:
        _file.close()

def do_god(input_msg):

    print('start god')


if __name__ == '__main__':
    manage_client = TcpClient(conf['brain']['manage_ip'], conf['brain']['manage_port'])
    run(TcpClientReceiveListener(manage_client, '[nvwa]: '))
    Runnable.pool.poll()
    try:
        options, args = getopt.getopt(sys.argv[1:], "gi:", ["god", "import="])
    except getopt.GetoptError:
        sys.exit()
    handle_opts(options)
    while True:
        _input = raw_input()
        _output = handle_input(_input)