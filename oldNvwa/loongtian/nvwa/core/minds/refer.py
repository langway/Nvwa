#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    refer 
Author:   Liuyl 
DateTime: 2015/6/15 15:26 
UpdateLog:
1、Liuyl 2015/6/15 Create this File.

refer
>>> print("No Test")
No Test
"""
from loongtian.nvwa.core.engines import meantool
from loongtian.nvwa.core.engines.meantool.mean2action import Mean2Action
from loongtian.nvwa.core.maincenter.evaluator.evaluator import EvaluateResult, State
from loongtian.nvwa.service import fragment_srv, fsc, knowledge_srv
from loongtian.nvwa.service.fragment_service.fragment_definition.refer import ReferBuilder

__author__ = 'Liuyl'
import datetime
import jieba

from loongtian.nvwa.common.threadpool.runnable import Runnable
from loongtian.nvwa.core.gdef import GlobalDefine
from loongtian.nvwa.core.maincenter.planner.plan import planer_center
from loongtian.nvwa.core.maincenter import *
from loongtian.nvwa.entities import CommandJobTypeEnum
from loongtian.nvwa.entities.sentence import Sentence


def word_cut(s):
    _cut_word_list = [word for word in list(jieba.cut(s, False)) if word.strip() != '']
    _word_list = []
    # 由于采用了完全分词,这里对 孙悟空-->孙悟空,悟空 和 人民银行-->人民,人民银行,银行 这样的分组结果进行筛选
    if len(_cut_word_list) > 0:
        _pre = _cut_word_list[0]
        _word_list.append(_pre)
        for _w in _cut_word_list[1:]:
            if _w.find(_pre) == -1 and _pre.find(_w) == -1:
                _word_list.append(_w)
                _pre = _w
    else:
        _word_list = _cut_word_list
    return _word_list


def move(word_list):
    _sentence = Sentence(word_list)
    # 分组
    _group_results = grouper_center.execute(word_list, _sentence)
    # 迁移
    _moved_results = mover_center.execute(_group_results, _sentence)
    # 评估
    _evaluated_result = evaluator_center.execute(_moved_results, _sentence)
    return _evaluated_result.frag


class Refer(Runnable):
    def __init__(self):
        super(Refer, self).__init__()
        self._name = "Refer"
        self.inputMsg = GlobalDefine().refer_input_queue
        self.outMsg = GlobalDefine().console_output_queue
        pass

    def _execute(self):
        while True:
            if not self.inputMsg.empty():
                _input, _client_address = self.inputMsg.get()
                _rb = ReferBuilder(_input)
                _rb.move(word_cut, move)
                _rep_srv = fragment_srv.get_new_knowledge_for_fragment_service()
                _rf = fsc.refer.assemble(_rep_srv, refer_builder=_rb)
                _s = Sentence('default')
                _es = evaluator_center.execute([[_rf]*2], _s)
                # _u = fsc.refer.unassemble(_rf)
                # _es=EvaluateResult(State.NotExist, 0, frag=_rf)
                _planed_results = planer_center.execute(_es, _s)
                # 执行
                for item in _planed_results:
                    if item.type == CommandJobTypeEnum.Output:
                        item.t_struct = (item.t_struct, _client_address)
                    GlobalDefine().command_msg.put(item)

                print knowledge_srv.rep.data.__len__()
                ma = Mean2Action(_rf)
                ma.do()
            if not self.state():
                break



if __name__ == '__main__':
    import doctest

    doctest.testmod()