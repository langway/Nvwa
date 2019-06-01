#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    manage_mind 
Author:   Liuyl 
DateTime: 2014/12/12 16:37 
UpdateLog:
1、Liuyl 2014/12/12 Create this File.

manage_mind
>>> print("No Test")
No Test
"""
__author__ = 'Liuyl'
from loongtian.nvwa.common.threadpool.runnable import Runnable
from loongtian.nvwa.core.gdef import GlobalDefine

class Manage(Runnable):
    def __init__(self):
        super(Manage, self).__init__()
        self._name = "Manage"
        pass

    def _execute(self):
        _input_queue = GlobalDefine().manage_input_queue
        _output_queue = GlobalDefine().manage_output_queue
        while True:
            if not _input_queue.empty():
                _input, _address = _input_queue.get()
                #_output = str(_input).upper()
                _msg = _input.lstrip("--god").strip()
                from loongtian.nvwa.core.engines.admin import admin_learn
                _r = admin_learn.learn(_msg,_address)
                if not _r:
                    _output_queue.put(('数据格式错误[O,顶级R,O]', _address))
            if not self.state():
                break


if __name__ == '__main__':
    import doctest

    doctest.testmod()