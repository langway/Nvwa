#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

from loongtian.nvwa.runtime.thinkResult.realLevelResult import RealLevelResult

class MeaningLevelResult():

    def __init__(self, patten_klg,meaning_klg, realsThinkResult):
        """
        一个实际对象链的思考结果。
        :param id:
        :param reals:
        """
        self.patten_klg = patten_klg
        self.meaning_klg = meaning_klg
        self.realsThinkResult = realsThinkResult


