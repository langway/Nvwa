#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Leon'

from loongtian.nvwa.runtime.sequencedObjs import SequencedObjs
from apscheduler.schedulers.background import BackgroundScheduler


class SchedulesManager(SequencedObjs):
    """
    系统执行的计划任务管理器。
    """

    def __init__(self,out_msg):
        super(SchedulesManager, self).__init__(objType=BackgroundScheduler)
        self._name = "NvwaSched"
        self.outMsg = out_msg
        pass

    def start(self):

        for sched,utc_time in self._sequence_obj_list:
            sched.start()
        print('-------- NvwaSched started -------------')


    def shutdown(self):

        for sched, utc_time in self._sequence_obj_list:
            sched.shutdown()
        print('-------- NvwaSched shutdown -------------')



