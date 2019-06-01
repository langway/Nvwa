#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    response 
Author:   Liuyl 
DateTime: 2015/1/13 15:30 
UpdateLog:
1、Liuyl 2015/1/13 Create this File.

response
>>> print("No Test")
No Test
"""
from loongtian.nvwa.service.fragment_service.fragment import FragmentService
from loongtian.nvwa.entities.enum import enum
from loongtian.nvwa.service.fragment_service.fragment_definition.response import ResponseFragment

__author__ = 'Liuyl'


class ResponseFragmentEnum(object):
    def __init__(self):
        enum(ResponseFragmentEnum,
             'SentenceType=0,State=1,Conflict=2,InputWord=3,OutputWord=4,InputMeaning=5'
             ',InputMeaningBasis=6,OutputMeaning=7,InputModel=8',
             sep=',')
        pass


ResponseFragmentEnum()


class ResponseFragmentService(FragmentService):
    def __init__(self):
        super(ResponseFragmentService, self).__init__()

    def generate(self, ref, rep_srv):
        if not ref:
            return None
        return ResponseFragment(ref, rep_srv)

    def assemble(self, target_srv, *args, **kwargs):
        """
        组装
        :param target_srv:
        :param kwargs: sentence_type,state,conflict,input_word,output_word,input_meaning,input_meaning_basis,output_meaning
        :return:
        """
        input_model = kwargs.get('input_model', None)
        _frag = self.save_to_target_service(input_model, target_srv) if input_model else None
        _frag.input_model=_frag
        input_meaning = kwargs.get('input_meaning', None)
        _frag.input_meaning = self.save_to_target_service(input_meaning, _frag.rep_srv) if input_meaning else None
        _frag.sentence_type = kwargs.get('sentence_type', None)
        _frag.state = kwargs.get('state', None)

        conflict = kwargs.get('conflict', [])
        _frag.conflict = [self.save_to_target_service(_c, _frag.rep_srv) for _c in conflict]
        input_meaning_basis = kwargs.get('input_meaning_basis', None)
        _frag.input_meaning_basis = self.save_to_target_service(input_meaning_basis,
                                                                _frag.rep_srv) if input_meaning_basis else None
        input_word = kwargs.get('input_word', None)
        _frag.input_word = self.save_to_target_service(input_word, _frag.rep_srv) if input_word else None
        output_word = kwargs.get('output_word', None)
        _frag.output_word = self.save_to_target_service(output_word, _frag.rep_srv) if output_word else []
        output_meaning = kwargs.get('output_meaning', None)
        _frag.output_meaning = self.save_to_target_service(output_meaning, _frag.rep_srv) if output_meaning else []

        return _frag

    def unassemble(self, frag):
        _result = dict()
        _result[ResponseFragmentEnum.SentenceType] = frag.sentence_type
        _result[ResponseFragmentEnum.State] = frag.state
        _result[ResponseFragmentEnum.Conflict] = frag.conflict
        _result[ResponseFragmentEnum.InputWord] = frag.input_word
        _result[ResponseFragmentEnum.OutputWord] = frag.output_word
        _result[ResponseFragmentEnum.InputMeaning] = frag.input_meaning
        _result[ResponseFragmentEnum.InputMeaningBasis] = frag.input_meaning_basis
        _result[ResponseFragmentEnum.OutputMeaning] = frag.output_meaning
        _result[ResponseFragmentEnum.InputModel] = frag.input_model
        return _result


if __name__ == '__main__':
    import doctest

    doctest.testmod()