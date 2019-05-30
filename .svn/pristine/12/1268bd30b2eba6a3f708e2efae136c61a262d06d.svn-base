#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    test 
Author:   fengyh 
DateTime: 2014/8/19 17:09 
UpdateLog:
1、fengyh 2014/8/19 Create this File.


"""
import sys

from loongtian.nvwa.common.threadpool.workerManager import WorkerManager


def test_job(id, sleep=0.001):
    try:
        print ('task here doing...[%4d]' % id)
    except:
        print '[%4d]' % id, sys.exc_info()[:2]
    return id


def test():
    import socket

    socket.setdefaulttimeout(10)
    print 'start testing'
    wm = WorkerManager(10)
    for i in range(500):
        wm.add_job(test_job, i, i * 0.001)
    wm.wait_for_complete()
    print 'end testing'


test()