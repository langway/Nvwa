#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    command 
Author:   Liuyl 
DateTime: 2014/9/10 13:45 
UpdateLog:
1、Liuyl 2014/9/10 Create this File.

command
>>> print("No Test")
No Test
"""
__author__ = 'Liuyl'
import test_helper
from loongtian.nvwa.service import original_init_srv


class CommandService(object):
    def __init__(self):
        pass

    def execute_command(self, command, main_thread):
        if command == '-draw':
            self.draw()
        elif command == '-exit':
            self.exit_all(main_thread)
        elif command == '-re_init_db':
            self.re_init_db()

    def draw(self):
        test_helper.draw_knowledge()

    def exit_all(self, main_thread):
        main_thread.stop()

    def re_init_db(self):
        original_init_srv.init_memory(True)


if __name__ == '__main__':
    import doctest

    doctest.testmod()