#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    util.py 
Created by zheng on 2014/11/20.
UpdateLog:

"""

def do_decrease(t_struct,srv):

    '''
    降低阈值
    :param key:
    :return:
    '''
    from loongtian.nvwa.core.engines.threshold import adjust
    _srv = srv()
    _temp = _srv.get(t_struct)
    threshold = _temp.Threshold
    _new = adjust.decrease(threshold)
    _temp.Threshold = _new
    _srv.save(_temp)

def do_increase(t_struct,srv):

    '''
    增加阈值
    :param key:
    :return:
    '''
    from loongtian.nvwa.core.engines.threshold import adjust
    _srv = srv()
    _temp = _srv.get(t_struct)
    threshold = _temp.Threshold
    _new = adjust.increase(threshold)
    _temp.Threshold = _new
    _srv.save(_temp)