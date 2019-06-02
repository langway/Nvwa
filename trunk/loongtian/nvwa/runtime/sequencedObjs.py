#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Leon'

"""
[运行时对象]在一个特定类型的序列中的对象的基类。例如：Mind、Focus
"""
import uuid
import datetime


class SequencedObj(object):
    """
    [运行时对象]在一个特定类型的序列中的对象的基类（可以查找上下文）。例如：Mind、Focus
    """

    def __init__(self, id=None, containedObj=None):
        """
        [运行时对象]在一个特定类型的序列中的对象的基类（可以查找上下文）。例如：Mind、Focus
        :param id:
        :param containedObj:
        """
        super(SequencedObj, self).__init__()
        if id:
            self.id = id
        else:
            self.id = str(uuid.uuid1()).replace("-", "")

        self.containedObj = containedObj  # 将SequencedObj作为装载对象的车厢


        self._last = None  # 上一个，与next共同构成一个链
        self._next = None  # 下一个，与last共同构成一个链
        # self.sequenceType = SequencedObj  # 序列中的对象类型（必须重写）

    def isContainer(self):
        """
        判断SequencedObj是否作为装载对象的车厢
        :return:
        """
        return self.containedObj is None

    def getLast(self):
        """
        取上一个，与next共同构成一个链
        :return:
        """
        return self._last

    def setLast(self, value, setNext=False):
        """
        设置上一个，与next共同构成一个链
        :param value:
        :return:
        """
        if value and isinstance(value, type(self)):
            self._last = value
            if setNext:
                value.setNext(self)
            self._setLast(value, setNext)

    def _setLast(self, value, setNext=True):
        """
        设置Last（必须重写方法）
        :param value:
        :return:
        """

    def getNext(self):
        """
        取下一个，与last共同构成一个链
        :return:
        """
        return self._next

    def setNext(self, value, setLast=True):
        """
        下一个，与last共同构成一个链
        :param value:
        :return:
        """
        if value and isinstance(value, type(self)):
            self._next = value
            if setLast:
                value.setLast(self)
            self._setNext(value, setLast)

    def _setNext(self, value, setLast=False):
        """
        设置Next（必须重写方法）
        :param value:
        :return:
        """

    def isHead(self):
        """
        是否是头部对象（有下文，没有上文）
        :return:
        """
        return self._last is None

    def isTail(self):
        """
        是否是尾部对象（有上文，没有下文）
        :return:
        """
        return self._next is None

    def isOrphan(self):
        """
        是否是孤儿对象（没有上下文）
        :return:
        """
        return self._last is None and self._next is None


class SequencedObjs(object):
    """
    [运行时对象]特定类型的序列。
    """

    def __init__(self, objType=SequencedObj):
        """
        [运行时对象]特定类型的序列。
        :param objType:
        """

        self.objType = objType # 限定被管理对象的类型

        self._containedObj_sequenceObjs_dict ={} # 将SequencedObj作为装载车厢时，对象与SequencedObj.id的映射关系
        self._id_containedObj_dict ={}# 将SequencedObj作为装载车厢时，SequencedObj.id与对象的映射关系

        self._id_obj_dict = {}
        self._obj_times_dict = {}  # 元输入及时间，格式为：{元输入:[时间1,时间2,...]}
        self._sequence_obj_list = []  # 按顺序的元输入及时间，格式为：[(元输入:时间),...]}
        self._time_obj_dict = {}  # 按时间的元输入及时间，格式为：{时间:元输入,...]}
        self._obj_poses_dict = {}  # 元输入及位置，格式为：{元输入:[位置1,位置2,...]}

    def add(self, obj):
        """
        添加对象
        :param obj:
        :return:
        """
        if obj is None:
            return False
        if not isinstance(obj, self.objType):
            raise Exception("添加的对象类型错误，当前类型%s，目标类型%s" % (str(type(obj)), str(self.objType)))

        # 如果添加的对象不是SequencedObj类型，将SequencedObj作为装载车厢
        if not isinstance(obj, SequencedObj):
            obj = SequencedObj(containedObj=obj)
            if not obj.containedObj in self._containedObj_sequenceObjs_dict:
                self._containedObj_sequenceObjs_dict[obj.containedObj] =[obj]
            else:
                self._containedObj_sequenceObjs_dict[obj.containedObj].append(obj)

        self._id_obj_dict[obj.id] =obj

        if len(self._sequence_obj_list) > 0:
            last = self._sequence_obj_list[-1]
            obj.setLast(last)

        if obj.isContainer():
            key = obj.containedObj
        else:
            key = obj.id
        _times = self._obj_times_dict.get(key)
        cur_utctime = datetime.datetime.utcnow()
        if _times:
            _times.append(cur_utctime)
        else:
            self._obj_times_dict[key] = [cur_utctime]

        self._sequence_obj_list.append((obj, cur_utctime))
        self._time_obj_dict[cur_utctime] = obj

        _poses = self._obj_poses_dict.get(key)
        if _poses:
            _poses.append(len(self._sequence_obj_list))
        else:
            self._obj_poses_dict[key] = [len(self._sequence_obj_list)]

        return self._add(obj)

    def _add(self, obj):
        """
        添加对象(必须进行重载)
        :param obj:
        :return:
        """
        return True

    def getById(self, id):
        """
        根据Id取得Mind
        :param Id:
        :return:
        """
        return self._id_obj_dict.get(id)

    def getByTime(self, utctime):
        """
        根据输入时间取得序列中的对象
        :param utctime:
        :return:
        """
        return self._time_obj_dict.get(utctime)

    def getByPos(self, pos):
        """
        根据输入顺序取得序列中的对象
        :param pos:
        :return:
        """
        return self._sequence_obj_list[pos]

    def getAddTimes(self, obj):
        """
        根据序列中的对象取得输入时间（可能有多个）
        :param obj:
        :return:
        """
        return self._obj_times_dict.get(obj)

    def getObjPoses(self, obj):
        """
        根据序列中的对象取得输入位置（可能有多个）
        :param obj:
        :return:
        """
        return self._obj_poses_dict.get(obj)

    def getLastContext(self, time):
        """
        取得上一时间的序列中的对象
        :param time:
        :return:
        """
        raise NotImplemented

    def getNextContext(self, time):
        """
        取得下一时间的序列中的对象
        :param time:
        :return:
        """
        raise NotImplemented

    def flush(self, start_time=None, end_time=None):
        """
        清除时间段内的序列中的对象（如果没有，全部清除）
        :param start_time:
        :param end_time:
        :return:
        """

        if start_time:
            if end_time:
                time_to_eliminate = []
                for temp_time in self._time_obj_dict.keys():
                    if start_time <= temp_time <= end_time:
                        time_to_eliminate.append(temp_time)
                self._eliminate_by_time(time_to_eliminate)
            else:
                time_to_eliminate = []
                for temp_time in self._time_obj_dict.keys():
                    if start_time <= temp_time:
                        time_to_eliminate.append(temp_time)
                self._eliminate_by_time(time_to_eliminate)
        elif end_time:
            time_to_eliminate = []
            for temp_time in self._time_obj_dict.keys():
                if temp_time <= end_time:
                    time_to_eliminate.append(temp_time)
            self._eliminate_by_time(time_to_eliminate)
        else:  # 没有时间段，全部清除
            self._obj_times_dict = {}  # 元输入及时间，格式为：{元输入:[时间1,时间2,...]}
            self._sequence_obj_list = []  # 按顺序的元输入及时间，格式为：[(元输入:时间),...]}
            self._time_obj_dict = {}  # 按时间的元输入及时间，格式为：{时间:元输入,...]}
            self._obj_poses_dict = {}  # 元输入及位置，格式为：{元输入:[位置1,位置2,...]}

    def _eliminate_by_time(self, time_to_eliminate):
        """
        将指定时间的输入删除
        :param time_to_eliminate:
        :return:
        """
        if not time_to_eliminate:
            return
        for temp_time in time_to_eliminate:
            temp_input = self._time_obj_dict.get(temp_time)
            # 处理self.time_inputs
            self._time_obj_dict.pop(temp_time)
            # 处理self._inputs_times
            for _input, times in self._obj_times_dict.items():
                if _input == temp_input:
                    times.remove(temp_time)
            # 处理self.sequence_inputs
            sequence_inputs_pos_to_eliminate = []
            pos = 0
            for sequence_input in self._sequence_obj_list:
                if sequence_input[1] == temp_time:
                    sequence_inputs_pos_to_eliminate.append((sequence_input, pos))
                pos += 1
            for sequence_input_to_eliminate, pos in sequence_inputs_pos_to_eliminate:
                self._sequence_obj_list.remove(sequence_input_to_eliminate)
                poses = self._obj_poses_dict.get(sequence_input_to_eliminate)
                if poses:
                    poses.remove(pos)
