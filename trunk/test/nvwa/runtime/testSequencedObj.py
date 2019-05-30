#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Leon'


from unittest import TestCase


class TestSequencedObj(TestCase):
    def setUp(self):
        print("----setUp----")

    def testCreateMind(self):
        print("----testCreateMetaData----")
        from loongtian.nvwa.organs.mind import Mind

        cur_m = Mind(None, None, None, None, None)
        last_m = Mind(None, None, None, None, None)
        cur_m.setLast(last_m,False)

        # 只设置了cur_m
        self.assertEqual(cur_m.getLast(), last_m)
        self.assertIsNone(cur_m.getNext())
        # last_m未设置
        self.assertIsNone(last_m.getNext())
        self.assertIsNone(last_m.getLast())

        last_m.setNext(cur_m,False)
        self.assertEqual(cur_m.getLast(), last_m)
        self.assertIsNone(cur_m.getNext())
        # last_m已设置
        self.assertEqual(last_m.getNext(),cur_m)
        self.assertIsNone(last_m.getLast())


        cur_m = Mind(None, None, None, None, None)
        last_m = Mind(None, None, None, None, None)
        next_m = Mind(None, None, None, None, None)
        cur_m.setLast(last_m, True)
        self.assertEqual(cur_m.getLast(), last_m)
        self.assertIsNone(cur_m.getNext())
        # last_m已设置
        self.assertEqual(last_m.getNext(), cur_m)
        self.assertIsNone(last_m.getLast())