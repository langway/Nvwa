#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    action 
Author:   Liuyl 
DateTime: 2015/5/28 15:45 
UpdateLog:
1、Liuyl 2015/5/28 Create this File.

action
>>> print("No Test")
No Test
"""
from loongtian.nvwa.entities import enum
from loongtian.nvwa.service import real_object_srv, original_srv
from loongtian.nvwa.service.fragment_service.fragment import FragmentService

__author__ = 'Liuyl'


class ActionFragmentEnum(object):
    """
    记忆结构类型。
    liuyl 2014-12-9
    """

    def __init__(self):
        enum(ActionFragmentEnum, 'Sequence=0,Steps=1,RealObject=2',
             sep=',')
        pass


ActionFragmentEnum()


class ActionFragmentService(FragmentService):
    def __init__(self):
        super(ActionFragmentService, self).__init__()

    @staticmethod
    def check(frag, rep_srv):
        return original_srv.InheritFrom.Action.check(frag.ref)

    def assemble(self, target_srv, *args, **kwargs):
        """
        组装
        :param target_srv:
        :param kwargs: sequence,steps,real_object
        :return:
        """
        sequence = kwargs.get('sequence', None)
        steps = kwargs.get('steps', [])
        real_object = kwargs.get('real_object', None)
        original_srv.InheritFrom.Action.set(real_object)
        original_srv.SequenceIs.set(real_object, sequence)
        for _s in steps:
            original_srv.StepIs.set(real_object, _s)
    def unassemble(self, frag):
        _result = dict()
        _result[ActionFragmentEnum.Sequence] = original_srv.SequenceIs.find_one(left=frag.ref)
        _result[ActionFragmentEnum.Steps] = original_srv.StepIs.find(left=frag.ref)
        return _result
    @staticmethod
    def create_placeholder(real_object, mark):
        _p = real_object_srv.create(Display=u"Act({0})的占位符{1}".format(real_object.Display, mark))
        original_srv.InheritFrom.PlaceHolder.set(_p)
        return _p


if __name__ == '__main__':
    import doctest

    doctest.testmod()