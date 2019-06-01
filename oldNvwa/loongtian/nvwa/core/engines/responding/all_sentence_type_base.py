#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    all_sentence_type_base 
Author:   fengyh 
DateTime: 2014/11/19 10:32 
UpdateLog:
1、fengyh 2014/11/19 Create this File.
2、liuyl 2014/12/5 抽取原始标签逻辑

"""
from loongtian.nvwa.core.maincenter.behavior.commands import Command_message
from loongtian.nvwa.entities import CommandJobTypeEnum, DataSourceTypeEnum
from loongtian.nvwa.service import *
import loongtian.nvwa.entities.data_structure_to_plan as dsp


class AllSentenceTypeBase:
    def __init__(self, match_degree_base, sentence):
        self.knowledge_is = metadata_srv.get_word_by_string_value(u'是')
        self.knowledge_enna = metadata_srv.get_word_by_string_value(u'嗯哪')
        self.knowledge_i_not_known = metadata_srv.get_word_by_string_value(u'不知道')
        self.knowledge_i_known = metadata_srv.get_word_by_string_value(u'知道了')
        self.knowledge_i_know = metadata_srv.get_word_by_string_value(u'知道')
        self.knowledge_but = metadata_srv.get_word_by_string_value(u'但是')
        self.not_sure = metadata_srv.get_word_by_string_value(u'不一定')
        self.not_correct = metadata_srv.get_word_by_string_value(u'不对')
        # self.knowledge_current_datetime = original_srv.create_time_real_object()

        self.sentence = sentence
        self.match_degree = match_degree_base
        self.result = []
        # 命令中片段信息的临时存储仓库
        self.frag_rep_srv = sentence.EvaluateResult.rep_srv
        # 保存接收信息
        # 接收信息的内容不会因计划后续的处理而不同，所以统一走一样的代码段。
        # 因数据流结构更改,改写下面的命令生成逻辑 liuyl 2014.11.14
        # _rep_srv = self.frag_rep_srv
        # if sentence.SentenceType < dsp.SentenceTypeEnum.AskSplit:
        #     _i_mood = original_srv.Declarative.obj()
        # elif sentence.SentenceType > dsp.SentenceTypeEnum.AskSplit:
        #     _i_mood = original_srv.Question.obj()
        # else:
        #     _i_mood = None
        # _sentence_model_frag = fragment_srv.save_to_target_service(self.sentence.sentence_word.sentence_model, _rep_srv)
        # _understand_model_frag = fragment_srv.save_to_target_service(self.sentence.EvaluateResult, _rep_srv)
        # _save_frag = fsc.memory.assemble(_rep_srv,
        #                                  sensor=original_srv.Console.obj(),
        #                                  recordTime=self.knowledge_current_datetime,
        #                                  mood=_i_mood,
        #                                  understand=_understand_model_frag.ref,
        #                                  receive=_sentence_model_frag.ref)
        # self.result = [
        #     # 保存接收信息
        #     Command_message(CommandJobTypeEnum.Save, DataSourceTypeEnum.Memory, _save_frag)
        # ]

    def gen_common_commands(self, i_send_words, i_send_words_understand):
        # 因数据流结构更改,改写下面的命令生成逻辑 liuyl 2014.11.14
        _rep_srv = self.frag_rep_srv
        # _send=fragment_srv.save_to_target_service()
        # _save_frag = fsc.memory.assemble(_rep_srv,
        #                                  send=i_send_words,
        #                                  understand=i_send_words_understand,
        #                                  mood=original_srv.Declarative.obj(),
        #                                  recordTime=self.knowledge_current_datetime,
        #                                  sensor=original_srv.Console.obj(),
        #                                  observer=original_srv.Anonymous.obj())
        # self.result.extend(
        #     [
        #         # 输出信息
        #         Command_message(CommandJobTypeEnum.Output, DataSourceTypeEnum.Console,
        #                         fragment_srv.generate(i_send_words, rep_srv=_rep_srv)),
        #         # 保存发出信息
        #         Command_message(CommandJobTypeEnum.Save, DataSourceTypeEnum.Memory, _save_frag)
        #     ]
        # )

