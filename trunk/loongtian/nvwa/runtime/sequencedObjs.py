#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Leon'

"""
[运行时对象]在一个特定类型的序列中的对象的基类。例如：Mind、Focus
"""
import uuid
import datetime
from collections import Iterable


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
        # super(SequencedObj, self).__init__()
        if id:
            self.id = id
        else:
            self.id = str(uuid.uuid1()).replace("-", "")

        self.containedObj = containedObj  # 将SequencedObj作为装载对象的车厢

        self.create_time = datetime.datetime.now()  # 对象进入序列的时间
        self._last = None  # 上一个，与next共同构成一个链
        self._next = None  # 下一个，与last共同构成一个链
        # self.sequenceType = SequencedObj  # 序列中的对象类型（必须重写）

    def isContainer(self):
        """
        判断SequencedObj是否作为装载对象的车厢
        :return:
        """
        return not self.containedObj is None

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
        if value:
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
        pass

    def getNext(self):
        """
        取下一个，与last共同构成一个链
        :return:
        """
        return self._next

    def setNext(self, value, setLast=False):
        """
        下一个，与last共同构成一个链
        :param value:
        :return:
        """
        if value:
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
        pass

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

    def __repr__(self):
        return "SequencedObj:{containedObj:%s,create_time:%s}" % (self.containedObj, self.create_time)


class SequencedObjs(object):
    """
    [运行时对象]特定类型的序列。
    """

    def __init__(self, objTypes: [], typesNum=1):
        """
        [运行时对象]特定类型的序列。
        :param objTypes:对象的类型（可能有多个）
        :param typesNum:对象的类型的数量（默认是一种类型）
        """

        if len(objTypes) > typesNum:  # 截取中指定数量的类型
            self.objTypes = objTypes[0:typesNum]
            self.typesNum = typesNum
        else:
            self.objTypes = objTypes  # 限定被管理对象的类型
            self.typesNum = len(objTypes)

        self._sequencedObj_list = []  # 按顺序的SequencedObj，格式为：[SequencedObj1,...]

        self._containedObj_sequencedObjs_dict = {}  # {元输入:[SequencedObj,...]}

        self._id_sequencedObj_dict = {}  # {id:SequencedObj}
        self._containedObj_ids_dict = {}  # {containedObj:[id1,...]}
        self._containedObj_times_dict = {}  # 元输入及时间，格式为：{元输入:[时间1,时间2,...]}
        self._time_sequncedObjs_dict = {}  # 按时间的元输入及时间，格式为：{时间:元输入,...]}
        self._containedObj_poses_dict = {}  # 元输入及位置，格式为：{元输入:[位置1,位置2,...]}

    def add(self, obj):
        """
        添加对象
        :param obj:
        :return:
        """
        if obj is None:
            return False

        wrong_type_num = 0
        for obj_type in self.objTypes:
            if isinstance(obj, obj_type):
                break
            wrong_type_num += 1
        if wrong_type_num == len(self.objTypes):
            raise Exception("添加的对象类型错误，当前类型%s，目标类型%s" % (str(type(obj)), str(self.objTypes)))

        # 如果添加的对象不是SequencedObj类型，将SequencedObj作为装载车厢
        if not isinstance(obj, SequencedObj):
            id = None
            if hasattr(obj, "id"):
                id = obj.id

            obj = SequencedObj(id=id, containedObj=obj)

        # 实际装载序列
        if len(self._sequencedObj_list) > 0:
            last = self._sequencedObj_list[-1]
            obj.setLast(last, True)

        self._sequencedObj_list.append(obj)

        contained_obj = obj.containedObj

        sequencedObj_list = self._containedObj_sequencedObjs_dict.get(contained_obj)

        # 装载序列的对象管理。装载的实际对象与装载车厢的关联管理，例如，多次输入“苹果”，可直接查找“苹果”输入序列
        if sequencedObj_list:
            sequencedObj_list.append(obj)
        else:
            self._containedObj_sequencedObjs_dict[contained_obj] = [obj]

        self._id_sequencedObj_dict[obj.id] = obj

        # 装载序列的id管理
        ids = self._containedObj_ids_dict.get(contained_obj)
        if ids:
            ids.append(obj.id)
        else:
            self._containedObj_ids_dict[contained_obj] = [obj.id]

        # 装载序列的时间管理
        _times = self._containedObj_times_dict.get(contained_obj)

        if _times:
            _times.append(obj.create_time)
        else:
            self._containedObj_times_dict[contained_obj] = [obj.create_time]

        timed_objs = self._time_sequncedObjs_dict.get(obj.create_time)
        if timed_objs:
            timed_objs.append(obj)
        else:
            self._time_sequncedObjs_dict[obj.create_time] = [obj]

        # 装载序列的位置管理
        _poses = self._containedObj_poses_dict.get(contained_obj)
        if _poses:
            _poses.append(len(self._sequencedObj_list))
        else:
            self._containedObj_poses_dict[contained_obj] = [len(self._sequencedObj_list) - 1]

        self._add(obj)

        return obj

    def _add(self, obj):
        """
        添加对象(必须进行重载)
        :param obj:
        :return:
        """
        return True

    def __len__(self):
        return len(self._sequencedObj_list)

    def __getitem__(self, index):
        return self._sequencedObj_list[index]

    def getAll(self):
        """
        取得所有的sequencedObj
        :return:
        """
        return self._sequencedObj_list

    def getAllContainedObj(self):
        """
        取得所有的containedObj
        :return:
        """
        _containedObj_list = []
        for seq_obj in self._sequencedObj_list:
            _containedObj_list.append(seq_obj.containedObj)
        return _containedObj_list

    def getById(self, id):
        """
        根据Id取得obj
        :param Id:
        :return:
        """
        return self._id_sequencedObj_dict.get(id)

    def getObjIds(self, obj):
        """
        根据obj取得Ids
        :param obj:
        :return:
        """
        return self._containedObj_ids_dict.get(obj)

    def getByTime(self, utctime):
        """
        根据输入时间取得序列中的对象
        :param utctime:
        :return:
        """
        return self._time_sequncedObjs_dict.get(utctime)

    def getByDuration(self, start_time, end_time):
        """
        根据输入时间段取得序列中的对象
        :param start_time:
        :param end_time:
        :return:
        """
        seq_objs = []
        for obj in self._sequencedObj_list:
            if end_time >= obj.utc_time >= start_time:
                seq_objs.append(obj)
        return seq_objs

    def getByPos(self, pos):
        """
        根据位置取得序列中的对象
        :param pos:位置
        :return:
        """
        try:
            return self._sequencedObj_list[pos]
        except:
            return None

    def getByPoses(self, poses: [int]):
        """
        根据位置取得序列中的对象
        :param poses:位置
        :return:
        """
        posed_objs = {}
        for pos in poses:
            try:
                temp_objs = self._sequencedObj_list[pos]
                posed_objs[pos] = temp_objs
            except:
                posed_objs[pos] = None

        return posed_objs

    def getAddTimes(self, obj):
        """
        根据序列中的对象取得输入时间（可能有多个）
        :param obj:
        :return:
        """
        return self._containedObj_times_dict.get(obj)

    def getObjPoses(self, obj):
        """
        根据序列中的对象取得输入位置（可能有多个）
        :param obj:
        :return:
        """
        return self._containedObj_poses_dict.get(obj)

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
        :return:todo 需要测试
        """

        if start_time:
            if end_time:
                time_to_eliminate = []
                for temp_time in self._time_sequncedObjs_dict.keys():
                    if start_time <= temp_time <= end_time:
                        time_to_eliminate.append(temp_time)
                self._eliminate_by_time(time_to_eliminate)
            else:
                time_to_eliminate = []
                for temp_time in self._time_sequncedObjs_dict.keys():
                    if start_time <= temp_time:
                        time_to_eliminate.append(temp_time)
                self._eliminate_by_time(time_to_eliminate)
        elif end_time:
            time_to_eliminate = []
            for temp_time in self._time_sequncedObjs_dict.keys():
                if temp_time <= end_time:
                    time_to_eliminate.append(temp_time)
            self._eliminate_by_time(time_to_eliminate)
        else:  # 没有时间段，全部清除
            self._sequencedObj_list = []  # 按顺序的元输入及时间，格式为：[SequencedObj1,...]}

            self._containedObj_sequencedObjs_dict = {}  # 将SequencedObj作为装载车厢时，对象与SequencedObj.id的映射关系

            self._id_sequencedObj_dict = {}
            self._containedObj_ids_dict = {}
            self._containedObj_times_dict = {}  # 元输入及时间，格式为：{元输入:[时间1,时间2,...]}
            self._time_sequncedObjs_dict = {}  # 按时间的元输入及时间，格式为：{时间:元输入,...]}
            self._containedObj_poses_dict = {}  # 元输入及位置，格式为：{元输入:[位置1,位置2,...]}

    def _eliminate_by_time(self, time_to_eliminate):
        """
        将指定时间的输入删除
        :param time_to_eliminate:
        :return:
        """
        if not time_to_eliminate:
            return

        sequence_objs_pos_to_eliminate = []

        for temp_time in time_to_eliminate:

            # temp_sequncedObjs = self._time_sequncedObjs_dict.get(temp_time)
            # 处理self._time_sequncedObjs_dict
            self._time_sequncedObjs_dict.pop(temp_time)
            # 处理self._containedObj_times_dict
            _containedObj_to_pop_list = []
            for _containedObj, times in self._containedObj_times_dict.items():
                if temp_time in times:
                    times.remove(temp_time)
                if len(times) == 0:
                    _containedObj_to_pop_list.append(_containedObj)
            if _containedObj_to_pop_list:
                for _containedObj_to_pop in _containedObj_to_pop_list:
                    self._containedObj_times_dict.pop(_containedObj_to_pop)

            pos = 0
            for sequenced_obj in self._sequencedObj_list:
                if sequenced_obj.utc_time == temp_time:
                    sequence_objs_pos_to_eliminate.append((sequenced_obj, pos))
                pos += 1

        for sequence_obj_to_eliminate, pos in sequence_objs_pos_to_eliminate:
            # 处理self._sequencedObj_list

            self._sequencedObj_list.remove(sequence_obj_to_eliminate)
            poses = self._containedObj_poses_dict.get(sequence_obj_to_eliminate.containedObj)
            if poses and pos in poses:
                poses.remove(pos)
            if len(poses) == 0:
                self._containedObj_poses_dict.pop(sequence_obj_to_eliminate.containedObj)

            self._id_sequencedObj_dict.pop(sequence_obj_to_eliminate.id)

            _sequencedObjs = self._containedObj_sequencedObjs_dict.get(sequence_obj_to_eliminate.containedObj)
            if _sequencedObjs:
                _sequencedObjs.remove(sequence_obj_to_eliminate)
            if len(_sequencedObjs) == 0:
                self._containedObj_sequencedObjs_dict.pop(sequence_obj_to_eliminate.containedObj)

            ids = self._containedObj_ids_dict.get(sequence_obj_to_eliminate.containedObj)
            if ids:
                ids.remove(sequence_obj_to_eliminate.id)
            if len(ids) == 0:
                self._containedObj_ids_dict.pop(sequence_obj_to_eliminate.containedObj)
