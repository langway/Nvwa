#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    ${NAME} 
Author:   fengyh 
DateTime: 2015/6/16 14:07 
UpdateLog:
1、fengyh 2015/6/16 Create this File.


"""
from unittest import TestCase
from loongtian.nvwa.core.engines.meantool.mean2action import Mean2Action
from loongtian.nvwa.core.gdef import OID
from loongtian.nvwa.service import real_object_srv, fragment_srv
from loongtian.nvwa.service import fsc

class TestMean2Action(TestCase):
    def test_do(self):
        """
        A打B
        指的是 { A抬手 下一步 （A放手 并且 B哭）}
        :return:
        """
        _rep_srv = fsc.fragment.get_new_knowledge_for_fragment_service()
        
        object_a = real_object_srv.create(Display=u'A')
        object_hit = real_object_srv.create(Display=u'打')
        object_b = real_object_srv.create(Display=u'B')
        object_refer = real_object_srv.get(OID.Refer)
        object_next = real_object_srv.get(OID.Next)
        object_and = real_object_srv.get(OID.And)
        object_raise_hands = real_object_srv.create(Display=u'抬手')
        object_down_hands = real_object_srv.create(Display=u'放手')
        object_cry = real_object_srv.create(Display=u'哭')

        k1 = _rep_srv.create_t_structure(object_a,object_hit,object_b)

        k21 = _rep_srv.create_l_structure(object_a,object_raise_hands)
        #,object_next)
        k22 = _rep_srv.create_l_structure(object_a,object_down_hands)
        k23 = _rep_srv.create_l_structure(object_b,object_cry)
        # a落手 并且 b哭
        k24 = _rep_srv.create_t_structure(k22,object_and,k23)
        #
        k25 = _rep_srv.create_t_structure(k21,object_next,k24)

        k3 = _rep_srv.create_t_structure(k1,object_refer,k25)

        _rf = fsc.refer.generate(k3,_rep_srv)

        ma = Mean2Action(_rf)
        ma.do()
        pass
    pass