#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    test_evaluator 
Author:   Liuyl 
DateTime: 2014/11/13 10:49 
UpdateLog:
1、Liuyl 2014/11/13 Create this File.

test_evaluator
"""
from loongtian.nvwa.entities.sentence import Sentence

__author__ = 'Liuyl'
from unittest import TestCase
from loongtian.nvwa.service import *
from loongtian.nvwa.core.gdef import OID
from loongtian.nvwa.core.maincenter import evaluator_center

original_init_srv.init()


class TestEvaluator(TestCase):
    def test_evaluator(self):
        self.assertEqual(0, 0)

    def test_evaluate_full_by_knowledge(self):
        pass