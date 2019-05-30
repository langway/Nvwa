#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    sentence_ask_need_replace 
Author:   fengyh 
DateTime: 2014/11/19 10:09 
UpdateLog:
1、fengyh 2014/11/19 Create this File.


"""
from loongtian.nvwa.core.engines.responding.all_sentence_type_base import AllSentenceTypeBase
from loongtian.nvwa.core.engines.responding import match_degree

from loongtian.nvwa.service import fragment_srv, memory_srv, original_srv


class AllSentenceType21AskWhat(AllSentenceTypeBase):
    def run(self):
        fragment_ext_what = fragment_srv.get_start(self.sentence.EvaluateResult)
        fragment_what_match = fragment_srv.get_same_from_target_service(fragment_ext_what, memory_srv)

        # 因数据流结构更改,改写下面的命令生成逻辑 liuyl 2014.11.14
        _rep_srv = self.frag_rep_srv
        _i_send = None
        if isinstance(self.match_degree, match_degree.MatchDegree0Full):
            _i_send = original_srv.Send.set(original_srv.InnerSelf.obj(), self.knowledge_is, _rep_srv)
            pass
        elif isinstance(self.match_degree, (match_degree.MatchDegree1Partial, match_degree.MatchDegree2No)):
            _i_send = original_srv.Send.set(original_srv.InnerSelf.obj(), self.knowledge_i_not_known, _rep_srv)
        pass
        i_send_words_frag = fragment_srv.generate(ref=_i_send, rep_srv=_rep_srv)
        self.gen_common_commands(i_send_words_frag)

    pass


class AllSentenceType22AskWhere(AllSentenceTypeBase):
    def run(self):
        fragment_ext_what = fragment_srv.get_start(self.sentence.EvaluateResult)

        fragment_what_match = fragment_srv.select_all_outer(fragment_ext_what)
        # 因数据流结构更改,改写下面的命令生成逻辑 liuyl 2014.11.14
        _rep_srv = self.frag_rep_srv
        _i_send = None
        if isinstance(self.match_degree, match_degree.MatchDegree0Full):
            _i_send = original_srv.Send.set(original_srv.InnerSelf.obj(), self.knowledge_is, _rep_srv)
            pass
        elif isinstance(self.match_degree, (match_degree.MatchDegree1Partial, match_degree.MatchDegree2No)):
            _i_send = original_srv.Send.set(original_srv.InnerSelf.obj(), self.knowledge_i_not_known, _rep_srv)
        pass
        i_send_words_frag = fragment_srv.generate(ref=_i_send, rep_srv=_rep_srv)
        self.gen_common_commands(i_send_words_frag)

    pass


class AllSentenceType23AskWho(AllSentenceTypeBase):
    def run(self):
        fragment_ext_what = fragment_srv.get_start(self.sentence.EvaluateResult)

        fragment_what_match = fragment_srv.select_all_outer(fragment_ext_what)
        # 因数据流结构更改,改写下面的命令生成逻辑 liuyl 2014.11.14
        _rep_srv = self.frag_rep_srv
        _i_send = None
        if isinstance(self.match_degree, match_degree.MatchDegree0Full):
            _i_send = original_srv.Send.set(original_srv.InnerSelf.obj(), self.knowledge_is, _rep_srv)
            pass
        elif isinstance(self.match_degree, (match_degree.MatchDegree1Partial, match_degree.MatchDegree2No)):
            _i_send = original_srv.Send.set(original_srv.InnerSelf.obj(), self.knowledge_i_not_known, _rep_srv)
        pass
        i_send_words_frag = fragment_srv.generate(ref=_i_send, rep_srv=_rep_srv)
        self.gen_common_commands(i_send_words_frag)

    pass


class AllSentenceType24AskWhen(AllSentenceTypeBase):
    def run(self):
        fragment_ext_what = fragment_srv.get_start(self.sentence.EvaluateResult)

        fragment_what_match = fragment_srv.select_all_outer(fragment_ext_what)
        # 因数据流结构更改,改写下面的命令生成逻辑 liuyl 2014.11.14
        _rep_srv = self.frag_rep_srv
        _i_send = None
        if isinstance(self.match_degree, match_degree.MatchDegree0Full):
            _i_send = original_srv.Send.set(original_srv.InnerSelf.obj(), self.knowledge_is, _rep_srv)
            pass
        elif isinstance(self.match_degree, (match_degree.MatchDegree1Partial, match_degree.MatchDegree2No)):
            _i_send = original_srv.Send.set(original_srv.InnerSelf.obj(), self.knowledge_i_not_known, _rep_srv)
        pass
        i_send_words_frag = fragment_srv.generate(ref=_i_send, rep_srv=_rep_srv)
        self.gen_common_commands(i_send_words_frag)

    pass


class AllSentenceType25AskHowMany(AllSentenceTypeBase):
    def run(self):
        fragment_ext_what = fragment_srv.get_start(self.sentence.EvaluateResult)

        fragment_what_match = fragment_srv.select_all_outer(fragment_ext_what)
        # 因数据流结构更改,改写下面的命令生成逻辑 liuyl 2014.11.14
        _rep_srv = self.frag_rep_srv
        _i_send = None
        if isinstance(self.match_degree, match_degree.MatchDegree0Full):
            _i_send = original_srv.Send.set(original_srv.InnerSelf.obj(), self.knowledge_is, _rep_srv)
            pass
        elif isinstance(self.match_degree, (match_degree.MatchDegree1Partial, match_degree.MatchDegree2No)):
            _i_send = original_srv.Send.set(original_srv.InnerSelf.obj(), self.knowledge_i_not_known, _rep_srv)
        pass
        i_send_words_frag = fragment_srv.generate(ref=_i_send, rep_srv=_rep_srv)
        self.gen_common_commands(i_send_words_frag)

    pass