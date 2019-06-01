#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    forget_engine.py 
Created by zheng on 2014/11/20.
UpdateLog:

"""
from loongtian.nvwa.service.repository_service.knowledge import KnowledgeService
from loongtian.nvwa.service.repository_service.real_object import RealObjectService
from loongtian.nvwa.core.engines.threshold import adjust
def forget():
    do_forget(KnowledgeService)
    do_forget(RealObjectService)

def do_forget(service):
    _service = service()
    keys = _service.get_matches()
    for key in keys:
        _obj = _service.get(key)
        threshold = _obj.Threshold
        _new = adjust.increase(threshold)
        _obj.Threshold = _new
        _service.save(_obj)
        #print 'forget '+' '+ str(service)+' '+_obj.Id+' ' + str(threshold) + " " + str(_new)