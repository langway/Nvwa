#!/usr/bin/env python
# coding: utf-8
"""
行为执行中枢执行器

Project:  nvwa
Title:    behave.py 
Created by zheng on 2014/10/16.
UpdateLog:

"""
from commands import *
import threading
import time
import random
import Queue
from loongtian.nvwa.entities.entity import *
from loongtian.nvwa.entities.enum import CommandJobTypeEnum,DataSourceTypeEnum

class CommandExec(threading.Thread):
    '''
    行为执行，所有命令分类对应的处理类在commands中注册
    主程序启动时创建
    
    commands 
    '''
    def __init__(self,queue):
        threading.Thread.__init__(self)
        self.commands = {CommandJobTypeEnum.Output: OutputCommand,
                         CommandJobTypeEnum.Save: SaveCommand,
                         CommandJobTypeEnum.Increase:IncreaseCommand,
                         CommandJobTypeEnum.Decrease:DecreaseCommand}
        self.queue = queue

    def create_command(self, command_type, command_target):
        return self.commands.get(command_type)(command_target)

    def run(self):
        while True:
            command_message = self.queue.get()
            if isinstance(command_message, Command_message):
                command = self.create_command(command_message.type, command_message.target)
                command.execute(command_message.t_struct)
            self.queue.task_done()


if __name__ == '__main__':
    thread_number = 2
    q_command = Queue.Queue(maxsize=0)
    execs = [CommandExec(q_command) for x in range(thread_number)]
    for item in execs:
        item.setDaemon(True)
        item.start()
    q_command.join()
    k1 = Knowledge(**{'Id':'4e37469f-37f8-11e4-b31b-00acf56dbacf'})
    k2 = Knowledge(**{'Id':'4dfb2801-37f8-11e4-911f-00acf56dbacf'})
    k3 = Knowledge(**{'Id':'4e2fa580-37f8-11e4-850b-00acf56dbacf'})
    k4 = Knowledge(**{'Id':'4e2fa580-37f8-11e4-850b-00acf56dbacf'})
    t_s = [k1,k4,[k2,k3,k3]]
    while True:
        time.sleep(1)
        q_command.put(Command_message(CommandJobTypeEnum.Save, DataSourceTypeEnum.Knowledge, str(random.randint(10000,90000))))
        q_command.put(Command_message(CommandJobTypeEnum.Output, DataSourceTypeEnum.Console, t_s))