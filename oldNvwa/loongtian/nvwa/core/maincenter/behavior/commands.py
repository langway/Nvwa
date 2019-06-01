#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    commands.py 
Created by zheng on 2014/10/16.
UpdateLog:

"""
from organs import *
from loongtian.nvwa.entities.enum import CommandJobTypeEnum,DataSourceTypeEnum
# command message [type,target,t_struct]
class Command_message(object):
    def __init__(self, type, target, t_struct):
        self.type = type
        self.target = target
        self.t_struct = t_struct


#command
class Command(object):
    def __init__(self, target):
        self.target = target

    def execute(self, t_struct):
        #print self
        if self.organs.has_key(self.target):
            self.organs[self.target](t_struct)


class SaveCommand(Command):
    def __init__(self, target):
        Command.__init__(self, target)
        self.organs = {DataSourceTypeEnum.Knowledge: Knowledge.save}
        pass

    def __str__(self):
        return 'save command:' + self.target


class OutputCommand(Command):
    def __init__(self, target):
        Command.__init__(self, target)
        self.organs = {DataSourceTypeEnum.Console: Console.output}

    def __str__(self):
        return 'output command:' + self.target

class IncreaseCommand(Command):
    def __init__(self, target):
        Command.__init__(self, target)
        self.organs = {
                       DataSourceTypeEnum.Knowledge: Knowledge.increase,
                       DataSourceTypeEnum.RealObject: RealObject.increase}

    def __str__(self):
        return 'output command:' + self.target

class DecreaseCommand(Command):
    def __init__(self, target):
        Command.__init__(self, target)
        self.organs = {DataSourceTypeEnum.Memory: Memory.decrease,
                       DataSourceTypeEnum.Knowledge: Knowledge.decrease,
                       DataSourceTypeEnum.RealObject: RealObject.decrease}

    def __str__(self):
        return 'output command:' + self.target