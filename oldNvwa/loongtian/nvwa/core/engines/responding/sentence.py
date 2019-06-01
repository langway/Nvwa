#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    sentence 
Author:   fengyh 
DateTime: 2014-10-16 9:01 
UpdateLog:
1、fengyh 2014-10-16 Create this File.
2、liuyl 2014-11-14 因数据流结构更改,改写命令生成逻辑

"""
from loongtian.nvwa.core.engines.responding.all_sentence_type_base import AllSentenceTypeBase
from loongtian.nvwa.service.fragment_service.memory import MemoryFragmentEnum
from loongtian.nvwa.service.question_words import QWords
import loongtian.nvwa.entities.data_structure_to_plan as dsp
from loongtian.nvwa.service import *
from loongtian.nvwa.core.gdef import OID


class AllSentenceType0NotAsk(AllSentenceTypeBase):
    def run(self):
        import loongtian.nvwa.core.engines.responding.match_degree as match_degree
        # 因数据流结构更改,改写下面的命令生成逻辑 liuyl 2014.11.14
        _rep_srv = self.frag_rep_srv
        _i_send = None
        # 默认给个是，实际是各种回答词对象代表的实际含义对象。暂时用词对象代表含义对象。
        _i_understand = self.knowledge_is
        if isinstance(self.match_degree, match_degree.MatchDegree0Full):
            # 输出内容“是”
            _i_send = self.knowledge_enna
            _i_understand = self.knowledge_enna
            pass
        elif isinstance(self.match_degree, match_degree.MatchDegree1Partial):
            # 输出内容为“我不知道***，但是我知道***”
            _i_not_known = _rep_srv.create_t_structure(original_srv.InnerSelf.obj(), self.knowledge_i_not_known,
                                                       self.sentence.EvaluateResult.ref)
            _i_known = _rep_srv.create_t_structure(original_srv.InnerSelf.obj(), self.knowledge_i_know,
                                                   self.sentence.EvaluateBasis.ref)
            _i_but = _rep_srv.create_t_structure(_i_not_known, self.knowledge_but, _i_known)
            _i_send = _i_but
            _i_understand = _i_but
            pass
        elif isinstance(self.match_degree, match_degree.MatchDegree2No):
            # 输出内容“知道了”
            _i_send = self.knowledge_i_known
            _i_understand = self.knowledge_i_known
            pass
        elif isinstance(self.match_degree, match_degree.MatchDegree3FullAndPartial):
            # 输出内容“不一定”
            _i_send = self.not_sure
            _i_understand = self.not_sure
            pass
        self.result = [fragment_srv.generate(_i_send, _rep_srv)]


class AllSentenceType1AskYesNo(AllSentenceTypeBase):
    def run(self):
        import loongtian.nvwa.core.engines.responding.match_degree as match_degree
        # 因数据流结构更改,改写下面的命令生成逻辑 liuyl 2014.11.14
        _rep_srv = self.frag_rep_srv
        _i_send = None
        # 默认给个是，实际是各种回答词对象代表的实际含义对象。暂时用词对象代表含义对象。
        _i_understand = self.knowledge_is
        if isinstance(self.match_degree, match_degree.MatchDegree0Full):
            _i_send = self.knowledge_is
            _i_understand = self.knowledge_is
            pass
        elif isinstance(self.match_degree, match_degree.MatchDegree2No):
            _i_send = self.knowledge_i_not_known
            _i_understand = self.knowledge_i_not_known
        elif isinstance(self.match_degree, match_degree.MatchDegree1Partial):
            _i_send = self.not_correct
            _i_understand = self.not_correct
        elif isinstance(self.match_degree, match_degree.MatchDegree3FullAndPartial):
            # 输出内容“不一定”
            _i_send = self.not_sure
            _i_understand = self.not_sure
            pass
        self.result = [fragment_srv.generate(_i_send, _rep_srv)]

    pass


class AllSentence2AskNeedReplaceTypeBase(AllSentenceTypeBase):
    def __init__(self, match_degree_base, sentence):
        AllSentenceTypeBase.__init__(self, match_degree_base, sentence)
        self._i_send_understand_dic = {}

    def try_answer_directly(self):
        """
        对于所有指代问句类型，第一步都首先尝试去掉指代词后的直接命中匹配
        要分别试探指代词左边和右边有什么
        :return:
        """

        _rep_srv = self.frag_rep_srv
        _i_send = None
        _i_send_list = []
        # 默认给个是，实际是各种回答词对象代表的实际含义对象。暂时用词对象代表含义对象。
        _i_understand = self.knowledge_is
        _i_understand_list = []

        ext_what_ahead_start_id = None
        is_left_match, is_right_match = False, False

        question_word_at_left, question_word_at_right, question_word_in_middle = False, False, False

        # 判断疑问替代是左侧还是右侧？即：是问“牛有什么”还是“什么有腿”。
        first_word = self.sentence.Words[0]
        last_word = self.sentence.Words[self.sentence.Words.__len__() - 1]
        if QWords.judge_contain_question_word(last_word):
            question_word_at_right = True
        if QWords.judge_contain_question_word(first_word):
            question_word_at_left = True
        if not QWords.judge_contain_question_word(last_word) and not QWords.judge_contain_question_word(first_word):
            question_word_at_left = True
            question_word_at_right = True

        if question_word_at_right:
            # ## 1、处理牛有什么。什么有右边的情况，用左边“牛有”去匹配搜索。
            # 牛有什么？ 去掉什么之后的部分。（牛有）
            fragment_ext_what_posterior = fragment_srv.get_start(self.sentence.EvaluateResult)

            # 牛有 在知识中查询，获得知识中的牛有相关Id
            fragment_ext_what_posterior_in_knowledge = fragment_srv.get_same_from_target_service(
                fragment_ext_what_posterior, knowledge_srv)

            fragment_what_match_posterior = None

            # 知识中找不到则在记忆中找
            if fragment_ext_what_posterior_in_knowledge is None:
                pass
                # fragment_ext_what_posterior_in_memory = fragment_srv.get_same_from_target_service(
                #     fragment_ext_what_posterior,
                #     memory_srv)
                # if fragment_ext_what_posterior_in_memory is None or QWords.judge_contain_question_word(
                #         fragment_ext_what_posterior_in_memory.ref.Display):
                #     # 找到包含疑问词的话不算。
                #     # 记忆中也找不到不做任何处理，不处理匹配标记则保留默认false标记。
                #     pass
                # else:
                #     ext_what_ahead_start_id = fragment_ext_what_posterior_in_memory.ref.End
                #     fragment_what_match_posterior = fragment_srv.select_all_outer(fragment_ext_what_posterior_in_memory)
                    # is_left_match = True
            else:
                ext_what_ahead_start_id = fragment_ext_what_posterior_in_knowledge.ref.End
                fragment_what_match_posterior = fragment_srv.select_all_outer(fragment_ext_what_posterior_in_knowledge)

            if fragment_what_match_posterior is not None:
                self.__wipe_out_some_layer_gen_understand_dic__(_rep_srv, fragment_what_match_posterior)
                is_left_match = True

        if question_word_at_left:
            result_list = []
            # ## 2、处理什么是腿。用右边“是腿”去匹配搜索。
            fragment_ext_what_ahead = fragment_srv.get_end(self.sentence.EvaluateResult)

            # 后面多处推导用。
            fragment_ext_what_posterior = fragment_srv.get_start(self.sentence.EvaluateResult)

            fragment_ext_what_ahead_in_knowledge = None
            # 从知识中查找“是腿”片段
            fragment_ext_what_ahead_in_knowledge = fragment_srv.get_same_from_target_service(fragment_ext_what_ahead,
                                                                                             knowledge_srv)

            # 如果在知识中找到则进行推导查询，找到“牛有，马有”
            if fragment_ext_what_ahead_in_knowledge is not None:
                right_structure_id = fragment_ext_what_ahead_in_knowledge.ref.Id
                fragment_ext_what_ahead_in_knowledge = knowledge_srv.base_deduce_forward(
                    fragment_ext_what_posterior.ref.End,
                    fragment_ext_what_ahead_in_knowledge.ref.Id)

            fragment_what_match_ahead = None

            if fragment_ext_what_ahead_in_knowledge is None or fragment_ext_what_ahead_in_knowledge.__len__() == 0:
                # 知识中找不到则在记忆中找
                # fragment_ext_what_ahead_in_memory = None
                # fragment_ext_what_ahead_in_memory = fragment_srv.get_same_from_target_service(fragment_ext_what_ahead,
                #                                                                               memory_srv)
                # # 如果在记忆中找到则进行推导查询，找到“牛有，马有”
                # if fragment_ext_what_ahead_in_memory is not None:
                #     right_structure_id = fragment_ext_what_ahead_in_memory.ref.Id
                #     fragment_ext_what_ahead_in_memory = memory_srv.base_deduce_forward(
                #         fragment_ext_what_posterior.ref.End,
                #         fragment_ext_what_ahead_in_memory.ref.Id)
                #
                # if fragment_ext_what_ahead_in_memory is None or fragment_ext_what_ahead_in_memory.__len__() == 0:
                #     # 记忆中也找不到不做任何处理，不处理匹配标记则保留默认false标记。
                #     pass
                # else:
                #     # 记忆中找到“牛有”则以“马有”等数据
                #     start_list = memory_srv.base_select_start_end_s(
                #         [(f, fragment_ext_what_posterior.ref.End) for f in fragment_ext_what_ahead_in_memory])
                #     # 查到“牛有腿”“牛有毛”等片段
                #     result_list = memory_srv.base_select_start_end_s(
                #         [(s.Id, right_structure_id) for s in start_list.values()])
                #     self.__gen_understand_dic__(_rep_srv, result_list, memory_srv, question_word_in_middle)
                pass
            else:
                # 知识中找到“牛有”则以“马有”等数据
                start_list = knowledge_srv.base_select_start_end_s(
                    [(f, fragment_ext_what_posterior.ref.End) for f in fragment_ext_what_ahead_in_knowledge])
                # 查到“牛有腿”“牛有毛”等片段
                result_list = knowledge_srv.base_select_start_end_s(
                    [(s.Id, right_structure_id) for s in start_list.values()])
                self.__gen_understand_dic__(_rep_srv, result_list, knowledge_srv, question_word_in_middle)

            if result_list is not None and result_list.__len__() > 0:
                is_right_match = True
                # self.gen_common_commands(i_send_words_frag,_i_understand)

        # 如果左右两种匹配都不成功，则输出不知道。
        # 匹配成功，但是过滤疑问词等之后如果结果为空，也处理为不知道。
        if (not is_left_match and not is_right_match) or self._i_send_understand_dic.__len__() == 0:
            _i_send = self.knowledge_i_not_known
            _i_understand = self.knowledge_i_not_known
            self.result.append(fragment_srv.generate(_i_send, _rep_srv))

        for _send in self._i_send_understand_dic:
            if QWords.judge_contain_question_word(_send.Display):
                continue
            self.result.append(fragment_srv.generate(self._i_send_understand_dic[_send], _rep_srv))
            # self.gen_common_commands(_send, self._i_send_understand_dic[_send])
        pass

    def run(self):
        self.try_answer_directly()

    def __wipe_out_some_layer_gen_understand_dic__(self, _rep_srv, fragment_what_match_posterior):
        for f in fragment_what_match_posterior:
            # 去掉包含疑问词的情况
            if QWords.judge_contain_question_word(f.ref.Display):
                continue
            frag = fragment_srv.save_to_target_service(f, self.frag_rep_srv)
            if not fsc.memory.check(f, knowledge_srv):
                self._i_send_understand_dic[frag.ref] = frag.ref
            else:
                # 以下4步骤，去掉“时间为”和“感知器为”外层数据，准备提取真正的“理解为”数据。

                _memory_structure = fsc.memory.unassemble(frag)

                _i_understand = _memory_structure[MemoryFragmentEnum.Understand].ref
                self._i_send_understand_dic[_i_understand] = _i_understand

    def __gen_understand_dic__(self, _rep_srv, result_list, knowledge_or_memory_srv, is_middle_question):
        for r in result_list.values():
            f = fragment_srv.generate(r, knowledge_or_memory_srv)
            _outer = fragment_srv.select_all_outer(f)
            _b = all(
                [any([_data.Id == OID.Send or _data.Id == OID.Question for _data in _item.data]) for _item in _outer])
            if not _b:
                _new_f = fragment_srv.save_to_target_service(f, _rep_srv)
                _i_send = _new_f.ref
                _i_understand = _new_f.ref
                self._i_send_understand_dic[_i_send] = _i_understand
        return self._i_send_understand_dic

    def __get_frag_list_by_start_list__(self, start_list_dic):
        """
        fengyh 2014-11-20
        start_list_dic.values() 示例如下：
        [[frag1],[frag2],...]
        :param start_list_dic:
        :return:
        """
        f_list = []
        for s in start_list_dic.values():
            if QWords.judge_contain_question_word(s[0].Display):
                continue
            f_list.append(fragment_srv.generate(s[0], memory_srv))
        return f_list

    pass

    def __get_frag_and_merge_frag_list__(self, start_list):
        frag_list = self.__get_frag_list_by_start_list__(start_list)
        if frag_list.__len__() != 0:
            frag_match_list = []
            # 合并每个片段查询的结果，待后面统一循环处理
            for f in frag_list:
                frag_match_list.extend(fragment_srv.select_all_outer(f))
            fragment_what_match_ahead = frag_match_list
        return fragment_what_match_ahead


class AllSentence5Command(AllSentenceTypeBase):
    def run(self):
        _rep_srv = self.frag_rep_srv
        _i_send = self.sentence.EvaluateBasis.ref
        self.result = [fragment_srv.generate(_i_send, _rep_srv)]
    pass


class SentenceFactory:
    def __init__(self):
        pass

    @staticmethod
    def create_sentence(sentence, match_degree):
        sentence_type = SentenceFactory.judge_sentence_type(sentence)
        if sentence_type == dsp.SentenceTypeEnum.NotAsk:
            return AllSentenceType0NotAsk(match_degree, sentence)
        elif sentence_type == dsp.SentenceTypeEnum.AskYesNo:
            return AllSentenceType1AskYesNo(match_degree, sentence)
        elif sentence_type == dsp.SentenceTypeEnum.AskNeedReplaceWhat:
            return AllSentence2AskNeedReplaceTypeBase(match_degree, sentence)
        elif sentence_type == dsp.SentenceTypeEnum.AskNeedReplaceWhere:
            return AllSentence2AskNeedReplaceTypeBase(match_degree, sentence)
        elif sentence_type == dsp.SentenceTypeEnum.AskNeedReplaceWho:
            return AllSentence2AskNeedReplaceTypeBase(match_degree, sentence)
        elif sentence_type == dsp.SentenceTypeEnum.AskNeedReplaceWhen:
            return AllSentence2AskNeedReplaceTypeBase(match_degree, sentence)
        elif sentence_type == dsp.SentenceTypeEnum.AskNeedReplaceHowMany:
            return AllSentence2AskNeedReplaceTypeBase(match_degree, sentence)
        elif sentence_type == dsp.SentenceTypeEnum.Command:
            return AllSentence5Command(match_degree, sentence)

    @staticmethod
    def judge_sentence_type(data_structure_to_plan):
        return data_structure_to_plan.SentenceType