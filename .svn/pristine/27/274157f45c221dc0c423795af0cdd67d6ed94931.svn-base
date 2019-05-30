#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    placeholder 
Author:   fengyh 
DateTime: 2015/6/16 10:24 
UpdateLog:
1、fengyh 2015/6/16 Create this File.


"""
from loongtian.nvwa.core.gdef import OID
from loongtian.nvwa.service import real_object_srv, knowledge_srv, original_srv


class PlaceHolder(object):
    @staticmethod
    def get_n_placeholder(num):
        place_holder = real_object_srv.get(OID.PlaceHolder)
        ph_list = []

        ph_list = knowledge_srv.base_select_end(place_holder.Id)

        if ph_list.__len__() > 0:
            ph_list = [real_object_srv.get(knowledge_srv.get(p.Start).Start) for p in ph_list]
            if ph_list.__contains__(place_holder):
                ph_list.remove(place_holder)
        list_len = ph_list.__len__()
        if list_len < num:
            for i in range(list_len, num):
                _p = real_object_srv.create(Display=u"占位符{0}".format(i))
                original_srv.InheritFrom.PlaceHolder.set(_p)
                ph_list.append(_p)
            return ph_list
        else:
            return ph_list[:num]
