#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    sched 
Created by zheng on 2014/11/19.
UpdateLog:

"""

from apscheduler.schedulers.background import BackgroundScheduler
from loongtian.nvwa.core.engines.forgetting import forget_engine

class NvwaSched():
    def __init__(self,out_msg):
        self._name = "NvwaSched"
        self.outMsg = out_msg
        pass

    def start(self):
        import logging
        logging.basicConfig()
        sched = BackgroundScheduler()
        sched.daemonic =  True
        sched.add_job(forget_engine.forget,trigger='cron',day_of_week='*', hour='*', minute='*/5',second='1')
        sched.start()
        print('-------- NvwaSched started -------------')