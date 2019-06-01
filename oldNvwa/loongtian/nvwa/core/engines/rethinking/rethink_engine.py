#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    rethink_engine 
Author:   Liuyl 
DateTime: 2014/11/17 10:24 
UpdateLog:
1、Liuyl 2014/11/17 Create this File.

rethink_engine
>>> print("No Test")
No Test
"""
import time

from loongtian.nvwa.common.threadpool.runnable import Runnable
from loongtian.nvwa.core.engines.associating import relation_subdivide
from loongtian.nvwa.core.engines.m2k.memory_to_knowledge import MemoryToKnowledge
from loongtian.nvwa.core.engines.modifying import trans, get_target_without_default, get_target
from loongtian.nvwa.core.gdef import GlobalDefine
from loongtian.nvwa.core.engines.abstracting.abstracting_engine import AbstractingEngine
from loongtian.nvwa.service import real_object_srv, fragment_srv, original_srv, knowledge_srv, fsc

__author__ = 'Liuyl'


class RethinkEngine(Runnable):
    def __init__(self):
        super(RethinkEngine, self).__init__()
        self._name = "Rethinking"
        # self.mtk = MemoryToKnowledge()
        self.rethink_queue = GlobalDefine().rethink_queue
        self.abstracting_engine = AbstractingEngine()

    def _execute(self):
        while True:
            # self.mtk.distill()
            message = self.rethink_queue.get()
            _rethink_result = self.deep_rethink(message)
            # 触发抽象
            self.abstracting_engine.abstract(_rethink_result)

            if not self.state():
                break

    def deep_rethink(self, frag):
        """
        递归反思,同时调用修限/类比/冲突引擎尝试将数据转换成顶级结构
        :param frag:
        :return:
        """
        _rep_srv = knowledge_srv
        if real_object_srv.type_check(frag.ref):
            return frag
        _start = fsc.modified.get_start(frag)
        _end = fsc.modified.get_end(frag)
        if real_object_srv.type_check(_start.ref) and real_object_srv.type_check(_end.ref):
            return fsc.modified.create_l_structure(_start, _end, _rep_srv)
        _rethought_start = self.deep_rethink(_start)
        _rethought_end = self.deep_rethink(_end)
        if _rethought_start and _rethought_end:
            _new_frag = fsc.modified.create_l_structure(_rethought_start, _rethought_end, _rep_srv)
            return self.do_rethink(_new_frag)
        return frag

    def do_rethink(self, frag):
        _r = fsc.modified.get_deep_end(frag)
        if not _r:
            return frag
        if original_srv.Equal.check(original_srv.BeModified.obj(), _r.ref):
            return trans(frag)
        else:
            _rep_srv = fragment_srv.get_new_knowledge_for_fragment_service()
            _o_frag = fragment_srv.save_to_target_service(frag, _rep_srv)
            _relation_subdivide_result_list = relation_subdivide(frag)
            _result_frag = fragment_srv.get_same_from_target_service(_o_frag, _rep_srv)
            if _relation_subdivide_result_list and len(_relation_subdivide_result_list) > 0:
                _relation_subdivide_result = _relation_subdivide_result_list[0][0]
                _r_frag = fsc.modified.get_deep_end(_relation_subdivide_result)
                _result_frag = _relation_subdivide_result
                if original_srv.Equal.check(_r_frag.ref, original_srv.InheritFrom.obj()):
                    _modified_frag = getattr(frag, 'modified_frag', frag)
                    _a_modified_frag = fsc.modified.get_deep_start(_modified_frag)
                    _b_modified_frag = fsc.modified.get_end(_modified_frag)
                    if _a_modified_frag and _b_modified_frag:
                        _target_list = get_target(_a_modified_frag, _b_modified_frag)
                        if len(_target_list) > 0:
                            _old_frag = _target_list[0][1]
                            _new_frag = fragment_srv.create_l_structure(
                                fragment_srv.get_start(_old_frag),
                                fragment_srv.get_end(_relation_subdivide_result), knowledge_srv)
                            fragment_srv.delete(_old_frag)
                            _result_frag = _new_frag
                else:
                    fragment_srv.save_to_target_service(_relation_subdivide_result, knowledge_srv)
            return _result_frag


if __name__ == '__main__':
    import doctest

    doctest.testmod()