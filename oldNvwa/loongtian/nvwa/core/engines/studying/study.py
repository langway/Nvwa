#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    study 
Author:   Liuyl 
DateTime: 2014/12/23 11:23 
UpdateLog:
1、Liuyl 2014/12/23 Create this File.

study
>>> print("No Test")
No Test
"""
import random
import itertools
from loongtian.nvwa.core.engines.associating import get_sorted_result
from loongtian.nvwa.core.engines.associating.associating_engine import AssociatingEngine
from loongtian.nvwa.service import *

__author__ = 'Liuyl'


def study(frag_list):
    associating = AssociatingEngine([_f[1] for _f in frag_list])
    associating.run()
    _study_result = frag_list[0][1]
    _frag = frag_list[0][0]
    _study_basis = None
    _result = get_sorted_result(associating)
    if len(_result) > 0:
        _study_result = _result[0][0]
        _study_basis = _result[0][1]
    for _f in frag_list:
        if _study_result.ref.Id == _f[1].ref.Id:
            _frag = _f[0]
    return _study_result, _study_basis, _frag


class StudyEngine(object):
    def __init__(self):
        pass

    def simple_study(self, frag, target_srv):
        pass

    def deep_study(self, frag, target_srv):
        _start = fragment_srv.get_start(frag)
        if not real_object_srv.get(_start.ref.Id):
            _new_start = self.deep_study(_start, target_srv)
        elif action_srv.is_action_by_real_object_id(_start.ref.Id):
            _new_start = fragment_srv.generate(_start.ref, target_srv)
        elif original_srv.InheritFrom.DefaultClass.check(_start.ref):
            _meta = metadata_srv.get_by_default_meaning_object(_start.ref)
            _new_class_object = self.create_class_object(_meta)
            _new_start = fragment_srv.generate(_new_class_object, target_srv)
        else:
            _new_start = fragment_srv.generate(_start.ref, target_srv)
        _end = fragment_srv.get_end(frag)
        if not real_object_srv.get(_end.ref.Id):
            _new_end = self.deep_study(_end, target_srv)
        elif action_srv.is_action_by_real_object_id(_end.ref.Id):
            _new_end = fragment_srv.generate(_end.ref, target_srv)
        elif original_srv.InheritFrom.DefaultClass.check(_end.ref):
            _meta = metadata_srv.get_by_default_meaning_object(_end.ref)
            _new_class_object = self.create_class_object(_meta)
            _new_end = fragment_srv.generate(_new_class_object, target_srv)
        else:
            _new_end = fragment_srv.generate(_end.ref, target_srv)
        return fragment_srv.assemble(target_srv, start=_new_start.ref, end=_new_end.ref)

    def sort(self, object_list):
        random.shuffle(object_list)

    def get_class_object(self, meta):
        _object_list = [_o for _o in [real_object_srv.get(_id) for _id in meta.RealObjectList] if
                        not original_srv.InheritFrom.DefaultClass.check(
                            _o) and not original_srv.InheritFrom.Word.check(_o)]
        if len(_object_list) > 0:
            self.sort(_object_list)
            return _object_list[0]
        else:
            return None

    def create_class_object(self, meta):
        _class_object = real_object_srv.create(Display=meta.StringValue)
        metadata_srv.link_real_object_metadata(meta.StringValue, _class_object)
        return _class_object

    def get_instance_object(self):
        pass

    def create_instance_object(self, class_object):
        _instance_object = real_object_srv.create(Display=class_object.Display)
        original_srv.InheritFrom.set(_instance_object, class_object)


if __name__ == '__main__':
    import doctest

    doctest.testmod()