#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Leon'


from unittest import TestCase
import datetime
from loongtian.nvwa.runtime.sequencedObjs import SequencedObjs


class TestSequencedObj(TestCase):
    def setUp(self):
        print("----setUp----")

    def testCreateMind(self):
        print("----testCreateMetaData----")
        from loongtian.nvwa.organs.mind import Mind

        cur_m = Mind(None, "牛", None)
        last_m = Mind(None, "马", None)
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


        cur_m = Mind(None, "头", None)
        last_m = Mind(None, "角", None)
        next_m = Mind(None, "尾巴", None)
        cur_m.setLast(last_m, True)
        self.assertEqual(cur_m.getLast(), last_m)
        self.assertIsNone(cur_m.getNext())
        # last_m已设置
        self.assertEqual(last_m.getNext(), cur_m)
        self.assertIsNone(last_m.getLast())


class TestSequencedObjs(TestCase):
    def setUp(self):
        print("----setUp----")

    def testCreateSequencedObjs(self):
        print("----testCreateSequencedObjs----")

        seq=SequencedObjs(objTypes=[str,int])
        self.assertEqual(len(seq.objTypes),1)
        self.assertEqual(seq.objTypes, [str])
        self.assertEqual(seq.typesNum,1)

        seq = SequencedObjs(objTypes=[str, int],typesNum=2)
        self.assertEqual(seq.objTypes, [str, int])
        self.assertEqual(len(seq.objTypes), 2)
        self.assertEqual(seq.typesNum, 2)

        seq = SequencedObjs(objTypes=[str, int], typesNum=3)
        self.assertEqual(seq.objTypes, [str, int])
        self.assertEqual(len(seq.objTypes), 2)
        self.assertEqual(seq.typesNum, 2)



    def testAddSequencedObjs(self):
        print("----testAddSequencedObjs----")
        import time
        seq=SequencedObjs(objTypes=[str,int],typesNum=2)

        obj_niu=seq.add("牛")
        print(obj_niu)
        time.sleep(0.1) # 需要休息一下，否则时间会相同
        self.assertEqual(obj_niu.containedObj, "牛")
        self.assertEqual(obj_niu.isContainer(),True)
        self.assertEqual(obj_niu.isHead(), True)
        self.assertEqual(obj_niu.isTail(), True)
        self.assertEqual(obj_niu.isOrphan(), True)

        self.assertEqual(obj_niu.getLast(), None)
        self.assertEqual(obj_niu.getNext(), None)

        obj_ma=seq.add("马")
        print(obj_ma)
        time.sleep(0.1)

        self.assertEqual(obj_ma.containedObj, "马")
        self.assertEqual(obj_ma.isContainer(),True)
        self.assertEqual(obj_ma.isHead(), False)
        self.assertEqual(obj_niu.isHead(), True)
        self.assertEqual(obj_ma.isTail(), True)
        self.assertEqual(obj_ma.isOrphan(), False)
        self.assertEqual(obj_niu.isOrphan(), False)

        self.assertEqual(obj_ma.getLast(), obj_niu)
        self.assertEqual(obj_ma.getNext(), None)

        obj_123=seq.add(123)
        print(obj_123)
        time.sleep(0.1)

        self.assertEqual(obj_123.containedObj, 123)
        self.assertEqual(obj_123.isContainer(),True)
        self.assertEqual(obj_123.isHead(), False)
        self.assertEqual(obj_niu.isHead(), True)
        self.assertEqual(obj_ma.isHead(), False)

        self.assertEqual(obj_niu.isTail(), False)
        self.assertEqual(obj_ma.isTail(), False)
        self.assertEqual(obj_123.isTail(), True)

        self.assertEqual(obj_niu.isOrphan(), False)
        self.assertEqual(obj_ma.isOrphan(), False)
        self.assertEqual(obj_123.isOrphan(), False)

        self.assertEqual(obj_niu.getLast(), None)
        self.assertEqual(obj_niu.getNext(), obj_ma)

        self.assertEqual(obj_123.getLast(), obj_ma)
        self.assertEqual(obj_123.getNext(), None)

        try: # 添加错误类型
            seq.add(["test"])
        except Exception as ex:
            print(ex)

        obj_niu1 = seq.add("牛") # 再次添加“牛”，以便进行时间、位置等的查询
        print(obj_niu1)
        time.sleep(0.1)

        obj_by_id = seq.getById(obj_ma.id)
        self.assertEqual(obj_by_id, obj_ma)

        ids = seq.getObjIds("牛")
        self.assertEqual(ids, [obj_niu.id, obj_niu1.id])

        times=seq.getAddTimes("牛")
        self.assertEqual(times,[obj_niu.utc_time,obj_niu1.utc_time])

        obj_by_time = seq.getByTime(obj_123.utc_time)
        self.assertTrue(obj_by_time,[obj_123])

        print(seq._sequencedObj_list)
        time=datetime.datetime.utcnow()
        print(time)
        obj_by_time = seq.getByTime(time)
        self.assertEqual(obj_by_time, None)

        start_time=obj_ma.utc_time
        end_time=obj_niu1.utc_time
        seq_objs=seq.getByDuration(start_time,end_time)
        self.assertEqual(seq_objs, [obj_ma,obj_123,obj_niu1])

        obj_by_pos = seq.getByPos(1)
        self.assertEqual(obj_by_pos,obj_ma)

        obj_by_pos = seq.getByPos(5)
        self.assertEqual(obj_by_pos, None)

        obj_by_poses = seq.getByPoses([0,3,5])
        self.assertEqual(obj_by_poses, {0:obj_niu,3:obj_niu1,5:None})

        seq.add("羊")

        seq.add("猪")
        seq.add(789)

        seq.flush(start_time,end_time)
        self.assertEqual(seq.getAllContainedObj(),["牛","羊","猪",789])

        seq.flush()

        print(seq.getAll())
        self.assertEqual(seq.getAllContainedObj(),[])











