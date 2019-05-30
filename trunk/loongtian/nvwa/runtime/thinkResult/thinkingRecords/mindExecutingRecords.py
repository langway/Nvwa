#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

import uuid
import datetime
from loongtian.nvwa.runtime.systemInfo import ThinkingInfo
from loongtian.util.common.generics import GenericsList


class MindExecutingRecord():
    """
    Mind的一条思考记录
    """

    def __init__(self,mindExecuteInfo = ThinkingInfo.MindExecuteInfo.UNKNOWN):

        self.mindExecuteInfo = mindExecuteInfo

        self.id = str(uuid.uuid1()).replace("-","")
        self.time = datetime.datetime.utcnow() # 记录的时间

class MindExecutingRecords(GenericsList):
    """
    Mind的思考记录(多个)
    """

    def __init__(self):
        super(MindExecutingRecords, self).__init__(MindExecutingRecord)

    def createNewMindThinkingRecord(self,mindExecuteInfo):
        """
        创建Mind的一条思考记录
        :param mindExecuteInfo:
        :return:
        """
        mindThinkingRecord =MindExecutingRecord(mindExecuteInfo)
        self.append(mindThinkingRecord)
        return mindThinkingRecord

    def getMindExecutingPath(self):
        """
        取得Mind的思考路径
        :return:
        """
        path =""
        for mindThinkingRecord in self:
            cur_path =ThinkingInfo.MindExecuteInfo.getName(mindThinkingRecord.mindExecuteInfo)
            if cur_path:
                path += cur_path + "-"

        path = path.lstrip("-")
        return path

    def __repr__(self):
        return "{MindExecutingRecords:%s}" % self.getMindExecutingPath()




#
# class ThinkingObjs(GenericsList):
#     """
#     正在被思维记录的对象（可能有多个）(标签:值)
#     """
#     def __init__(self,):
#         super(ThinkingObjs,self).__init__(ThinkingObj)
#         self.tag_obj_dict = {}
#
#
#     def add(self,tag, value):
#         """
#         重写append
#         :param obj:
#         :return:
#         """
#         _thinkingObj = ThinkingObj(tag,value)
#         self.tag_obj_dict[tag]=_thinkingObj
#         self.append(_thinkingObj)
#
#
#     def getByTag(self,tag):
#         """
#         根据tag取思考对象（(标签,值)）
#         :param tag:
#         :return:
#         """
#         return self.tag_obj_dict.get(tag)
#
#     def getValueByTag(self,tag):
#         """
#         根据tag取思考对象（(标签,值)）
#         :param tag:
#         :return:
#         """
#         tag_obj = self.tag_obj_dict.get(tag)
#         if tag_obj:
#             return tag_obj.value
#         return None
#
# class ThinkingObj():
#     """
#     正在被思维记录的对象(标签:值)
#     """
#     def __init__(self,tag,value):
#         self.tag =tag
#         self.value =value

