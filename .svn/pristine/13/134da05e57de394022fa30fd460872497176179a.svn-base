#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    plan 
Author:   fengyh 
DateTime: 2014-10-16 8:51 
UpdateLog:
1、fengyh 2014-10-16 Create this File.


"""
from loongtian.nvwa.core.maincenter.behavior.commands import Command_message
from loongtian.nvwa.entities.enum import *
from loongtian.nvwa.service import *
from loongtian.nvwa.core.engines.responding import respond


class Planer:
    def __init__(self):
        pass

    def make_save_plan(self, frag):
        _result = []
        _result.append(Command_message(CommandJobTypeEnum.Save, DataSourceTypeEnum.Knowledge, frag))
        return _result

    def execute(self, evaluated_result, sentence):
        _rep_srv = fragment_srv.get_new_knowledge_for_fragment_service()
        _response_frag = fsc.response.assemble(_rep_srv,
                                               sentence_type=sentence.SentenceType,
                                               state=evaluated_result.state,
                                               conflict=evaluated_result.conflict,
                                               input_word=sentence.sentence_model,
                                               input_model=evaluated_result.frag,
                                               input_meaning=getattr(evaluated_result.left_frag, 'modified_frag',
                                                                     evaluated_result.left_frag),
                                               input_meaning_basis=evaluated_result.right_frag)
        # _response_frag.words = sentence.Words
        respond(_response_frag)
        return self.generate_command(_response_frag)

    def generate_command(self, response_frag):
        # 因数据流结构更改,改写下面的命令生成逻辑 liuyl 2014.11.14
        _rep_srv = response_frag.rep_srv
        _current_datetime_object = original_srv.create_time_real_object()
        _result = []
        if response_frag.sentence_type < SentenceTypeEnum.AskSplit:
            # 去掉本段注释，保存学到的action。fengyh 2015-7-2
            if response_frag.input_meaning:
                _input_memory_frag = fsc.memory.assemble(_rep_srv,
                                                         understand=response_frag.input_meaning.ref,
                                                         time=_current_datetime_object)
                _result.append(Command_message(CommandJobTypeEnum.Save, DataSourceTypeEnum.Knowledge, _input_memory_frag))

            if response_frag.input_model:
                _input_model_frag = fsc.memory.assemble(_rep_srv,
                                                        understand=response_frag.input_model.ref,
                                                        time=_current_datetime_object)

                _result.append(Command_message(CommandJobTypeEnum.Save, DataSourceTypeEnum.Knowledge, _input_model_frag))

        for _i in range(len(response_frag.output_word)):
            _output_memory_frag = fsc.memory.assemble(_rep_srv,
                                                      understand=response_frag.output_meaning[_i].ref,
                                                      mood=original_srv.Declarative.obj(),
                                                      time=_current_datetime_object,
                                                      sensor=original_srv.Console.obj(),
                                                      observer=original_srv.Anonymous.obj())
            _output_frag = response_frag.output_word[_i]
            # 输出信息
            _result.append(Command_message(CommandJobTypeEnum.Output, DataSourceTypeEnum.Console, _output_frag))
            # 保存发出信息
            # _result.append(Command_message(CommandJobTypeEnum.Save, DataSourceTypeEnum.Memory, _output_memory_frag))

        return _result


planer_center = Planer()