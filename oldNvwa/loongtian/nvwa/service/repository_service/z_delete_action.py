#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Project:  nvwa
Title:    action 
Author:   liuyl 
DateTime: 2014/9/5 10.59 
UpdateLog:
1、liuyl 2014/9/5 Create this File.


action服务层
>>> print("No Test")
No Test
"""
__author__ = 'Liuyl'
from loongtian.nvwa.service.repository_service.base_rep_service import BaseRepService
from loongtian.nvwa.service import real_object_srv, metadata_srv, original_srv, action_define_srv
from loongtian.nvwa.common.storage.db.entity_repository import action_rep
import copy


class ActionService(BaseRepService):
    def __init__(self):
        super(ActionService, self).__init__(action_rep)

    def create(self, **kwargs):
        if not kwargs.get('RealObjectId', None):
            return None
        _a = self.generate(**kwargs)
        self.save(_a)
        return _a

    def create_negate(self, source_action, **kwargs):
        _real_object_id = kwargs.get('RealObjectId', None)
        if not kwargs.get('RealObjectId', None):
            return None
        _steps = kwargs.get('Steps', copy.deepcopy(source_action.Steps))
        _step_intervals = kwargs.get('StepIntervals', copy.deepcopy(source_action.StepIntervals))
        _sequence = kwargs.get('Sequence', copy.deepcopy(source_action.Sequence))
        _s = _steps[0][0]
        _steps[0][0] = original_srv.Negate.set(None, action_define_srv.get(_s), action_define_srv).Id
        self.create(Display=kwargs.get('Display', None),
                    RealObjectId=_real_object_id,
                    Sequence=_sequence,
                    Steps=_steps,
                    StepIntervals=_step_intervals)

    def get_by_real_object_id(self, real_object_id):
        return self.rep.get_by_real_object_id(real_object_id)

    def is_action_by_real_object_id(self, real_object_id):
        """
        输入real_object_id判断其是否是Action。
        :param real_object_id:
        :return:true or false
        """
        return True if self.get_by_real_object_id(real_object_id).__len__() != 0 else False

    def gets_by_real_object_id(self, real_object_ids):
        return self.rep.gets_by_real_object_id(real_object_ids)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
