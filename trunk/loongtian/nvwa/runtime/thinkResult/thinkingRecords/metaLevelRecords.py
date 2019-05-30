#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

import uuid
import datetime
from loongtian.nvwa.runtime.systemInfo import ThinkingInfo
from loongtian.util.common.generics import GenericsList

class MetaLevelEexecuteRecord():
    """
    nvwa对象的一条执行记录
    """

    def __init__(self, metaLevelExecuteInfo = ThinkingInfo.MetaLevelInfo.ExecuteInfo.UNKNOWN, thinkingObj = None):

        self.metaLevelExecuteInfo = metaLevelExecuteInfo

        self.thinkingObj = thinkingObj
        self.id = str(uuid.uuid1()).replace("-","")
        self.time = datetime.datetime.utcnow()  # 记录的时间

class MetaLevelEexecuteRecords(GenericsList):
    """
    nvwa对象的执行记录(多个)
    """

    def __init__(self):
        super(MetaLevelEexecuteRecords, self).__init__(MetaLevelEexecuteRecord)


    def createNewMetaLevelEexecuteRecord(self, metaLevelExecuteInfo, thinkingObj):
        """
        创建nvwa对象的一条执行记录
        :param metaLevelExecuteInfo:
        :param thinkingObj:
        :return:
        """
        _metaLevelEexecuteRecord =MetaLevelEexecuteRecord(metaLevelExecuteInfo, thinkingObj)
        self.append(_metaLevelEexecuteRecord)
        return _metaLevelEexecuteRecord

    def getMetaLevelExecutePath(self):
        """
        取得nvwa对象的执行路径
        :return:
        """
        path = ""
        for metaLevelExecuteRecord in self:
            cur_path = ThinkingInfo.MetaLevelInfo.ExecuteInfo.getName(metaLevelExecuteRecord.metaLevelExecuteInfo)
            if cur_path:
                path += cur_path + "-"

        path = path.lstrip("-")
        return path

    def __repr__(self):
        return "{MetaLevelEexecuteRecords:%s}" % self.getMetaLevelExecutePath()

class MetaLevelMatchRecord():
    """
    nvwa数据对象的一条匹配记录（从元数据开始、元数据网、实际对象、知识链、知识链意义）
    """

    def __init__(self, metaLevelMatchInfo = ThinkingInfo.MetaLevelInfo.MatchInfo.UNKNOWN, thinkingObj = None):

        self.metaLevelMatchInfo = metaLevelMatchInfo
        self.thinkingObj = thinkingObj
        self.id = str(uuid.uuid1()).replace("-","")
        self.time = datetime.datetime.utcnow()  # 记录的时间

class MetaLevelMatchRecords(GenericsList):
    """
    nvwa数据对象的匹配记录（从元数据开始、元数据网、实际对象、知识链、知识链意义）(多个)
    """

    def __init__(self):
        super(MetaLevelMatchRecords, self).__init__(MetaLevelMatchRecord)


    def createNewMetaLevelMatchRecord(self, metaLevelMatchInfo, thinkingObj):
        """
        创建nvwa数据对象的一条匹配记录（从元数据开始、元数据网、实际对象、知识链、知识链意义）
        :param metaLevelMatchInfo:
        :param thinkingObj:
        :return:
        """
        _metaLevelMatchRecord =MetaLevelMatchRecord(metaLevelMatchInfo, thinkingObj)
        self.append(_metaLevelMatchRecord)
        return _metaLevelMatchRecord


    def getMetaLevelMatchPath(self):
        """
        取得nvwa数据对象的匹配路径
        :return:
        """
        path = ""
        for metaLevelMatchRecord in self:
            cur_path = ThinkingInfo.MetaLevelInfo.MatchInfo.getName(metaLevelMatchRecord.metaLevelMatchInfo)
            if cur_path:
                path += cur_path + "-"

        path = path.lstrip("-")
        return path

    def __repr__(self):
        return "{MetaLevelMatchRecords:%s}" % self.getMetaLevelMatchPath()

# class MetaLevelUnderstoodRecord():
#     """
#     实际对象链的一条理解记录
#     """
#
#     def __init__(self, metaLevelUnderstoodInfo = ThinkingInfo.MetaLevelInfo.UnderstoodInfo.UNKNOWN, thinkingObj = None):
#
#         self.metaLevelUnderstoodInfo = metaLevelUnderstoodInfo
#         self.thinkingObj = thinkingObj
#         self.id = str(uuid.uuid1()).replace("-","")
#         self.time = datetime.datetime.utcnow()  # 记录的时间
#
# class MetaLevelUnderstoodRecords(GenericsList):
#     """
#     实际对象链的理解记录(多个)
#     """
#
#     def __init__(self):
#         super(MetaLevelUnderstoodRecords, self).__init__(MetaLevelUnderstoodRecord)
#
#
#     def createNewMetaLevelUnderstoodRecord(self, metaLevelUnderstoodInfo, thinkingObj):
#         """
#         创建实际对象链的一条理解记录
#         :param metaLevelUnderstoodInfo:
#         :param thinkingObj:
#         :return:
#         """
#         _metaLevelUnderstoodRecord =MetaLevelUnderstoodRecord(metaLevelUnderstoodInfo, thinkingObj)
#         self.append(_metaLevelUnderstoodRecord)
#         return _metaLevelUnderstoodRecord
#
#     def getMetaLevelUnderstoodPath(self):
#         """
#         取得实际对象链的理解路径
#         :return:
#         """
#         path = ""
#         for metaLevelUnderstoodRecord in self:
#             cur_path = ThinkingInfo.MetaLevelInfo.UnderstoodInfo.getName(metaLevelUnderstoodRecord.metaLevelUnderstoodInfo)
#             if cur_path:
#                 path += cur_path + "-"
#
#         path = path.lstrip("-")
#         return path
#
#     def __repr__(self):
#         return "{MetaLevelUnderstoodRecords:%s}" % self.getMetaLevelUnderstoodPath()

class MetaLevelThinkingRecords():
    """
    关于元数据思考状态的信息记录（这些状态在思维处理中不断被改变，是单向、互斥的）。
    """

    def __init__(self, thinkResult):

        self.thinkResult = thinkResult

        self._MetaLevelExecuteRecords = MetaLevelEexecuteRecords()  # 按顺序设置的元数据链的执行记录(多个)
        self._MetaLevelExecuteRecords.createNewMetaLevelEexecuteRecord(ThinkingInfo.MetaLevelInfo.ExecuteInfo.UNKNOWN, None) # 默认为未知

        self._MetaLevelMatchRecords = MetaLevelMatchRecords()  # 按顺序设置的nvwa数据对象的匹配记录（从元数据开始、元数据网、实际对象、知识链、知识链意义）(多个)
        self._MetaLevelMatchRecords.createNewMetaLevelMatchRecord(ThinkingInfo.MetaLevelInfo.MatchInfo.UNKNOWN, None) # 默认为未知

        # self._MetaLevelUnderstoodRecords = MetaLevelUnderstoodRecords()  # 按顺序设置的实际对象链的理解记录
        # self._MetaLevelUnderstoodRecords.createNewMetaLevelUnderstoodRecord(ThinkingInfo.MetaLevelInfo.UnderstoodInfo.UNKNOWN, None) # 默认为未知

    # ####################################
    # 执行状态信息
    # ####################################
    def isAllUnexecuted(self):
        """
        判断思考是否全都未执行。
        :return:
        """
        if self.curMetaLevelExecuteInfo == ThinkingInfo.MetaLevelInfo.ExecuteInfo.UNKNOWN:
            return True

        return False

    def setMetaLevelExecuteRecord(self, metaLevelExecuteInfo, thinkingObj, throw_exception=False):
        """
        设置执行状态信息。
        :param metaLevelExecuteInfo:
        :return:
        """
        if self._canMetaLevelExecuteInfoTransfer(metaLevelExecuteInfo):
            return self._MetaLevelExecuteRecords.createNewMetaLevelEexecuteRecord(metaLevelExecuteInfo, thinkingObj)
        else:
            if throw_exception:
                raise Exception("不能从一种执行状态（%s）转到当前执行状态（%s）" % (self.curMetaLevelExecuteInfo, metaLevelExecuteInfo))

    def _canMetaLevelExecuteInfoTransfer(sel, metaLevelExecuteInfo):
        """
        判断能从上一种执行状态转到当前执行状态。
        :param metaLevelExecuteInfo:
        :return:
        """
        # todo 需要进行执行状态信息的判断（参考stateController）
        return True

    @property
    def curMetaLevelExecuteRecord(self):
        """
        取得最新的执行状态记录。
        :return:
        """
        try:
            return self._MetaLevelExecuteRecords[-1]
        except:  # 有可能取不到 ，忽略错误
            pass

    @property
    def curMetaLevelExecuteInfo(self):
        """
        取得最新的执行状态信息
        :return:
        """
        try:
            _curMetaLevelExecuteRecord= self.curMetaLevelExecuteRecord
            if _curMetaLevelExecuteRecord:
                return _curMetaLevelExecuteRecord.metaLevelExecuteInfo
        except:  # 有可能取不到 ，忽略错误
            pass

    def getMetaLevelExecutePath(self):
        """
        取得nvwa对象的执行路径
        :return:
        """
        return self._MetaLevelExecuteRecords.getMetaLevelExecutePath()
    # ####################################
    # 匹配状态信息
    # ####################################

    def isRealObjectUnmatched(self):
        """
        判断实际对象是否未知（元数据已知）。
        :return:
        """
        return self.curMetaLevelMatchInfo == ThinkingInfo.MetaLevelInfo.MatchInfo.SINGLE_META_RELATED_REALS_UNMATCHED

    def isAllUnmatched(self):
        """
        判断元数据链是否全都未知（未能匹配）。
        :return:
        """
        if self.curMetaLevelMatchInfo == ThinkingInfo.MetaLevelInfo.MatchInfo.UNKNOWN:
            return True
        elif self.curMetaLevelMatchInfo == ThinkingInfo.MetaLevelInfo.MatchInfo.SINGLE_META_UNMATCHED:
            return True
        return self.thinkResult.metaLevelResult.isAllUnknown()

    def setMetaLevelMatchRecord(self, metaLevelMatchInfo, thinkingObj, throw_exception=False):
        """
        设置匹配状态。
        :param metaLevelMatchInfo:
        :return:
        """
        if self._canMetaLevelMatchInfoTransfer(metaLevelMatchInfo):
            self._MetaLevelMatchRecords.createNewMetaLevelMatchRecord(metaLevelMatchInfo, thinkingObj)
        else:
            if throw_exception:
                raise Exception("不能从一种匹配状态（%s）转到当前匹配状态（%s）" % (self.curMetaLevelMatchInfo, metaLevelMatchInfo))

    def _canMetaLevelMatchInfoTransfer(sel, metaLevelMatchInfo):
        """
        判断能从上一种匹配状态转到当前匹配状态
        :param metaLevelMatchInfo:
        :return:
        """
        # todo 需要进行匹配状态的判断（参考stateController）
        return True

    @property
    def curMetaLevelMatchRecord(self):
        """
        取得最新的匹配信息
        :return:
        """
        try:
            return self._MetaLevelMatchRecords[-1]
        except:  # 有可能取不到 ，忽略错误
            pass

    @property
    def curMetaLevelMatchInfo(self):
        """
        取得最新的匹配信息
        :return:
        """
        try:
            _curMetaLevelMatchRecord=self.curMetaLevelMatchRecord
            if _curMetaLevelMatchRecord:
                return _curMetaLevelMatchRecord.metaLevelMatchInfo
        except:  # 有可能取不到 ，忽略错误
            pass

    def getMetaLevelMatchPath(self):
        """
        取得nvwa数据对象的匹配路径
        :return:
        """
        return self._MetaLevelMatchRecords.getMetaLevelMatchPath()
    #
    # # ####################################
    # # 理解状态信息
    # # ####################################
    # def isAllUnderstood(self):
    #     """
    #     判断思考是否已经理解。
    #     :return:
    #     """
    #     if self.curMetaLevelUnderstoodInfo == ThinkingInfo.MetaLevelInfo.UnderstoodInfo.UNKNOWN:
    #         return True
    #
    #     return False
    #
    # def setMetaLevelUnderstoodRecord(self, metaLevelUnderstoodInfo, thinkingObj, throw_exception=False):
    #     """
    #     设置理解状态信息。
    #     :param metaLevelUnderstoodInfo:
    #     :return:
    #     """
    #     if self._canMetaLevelUnderstoodInfoTransfer(metaLevelUnderstoodInfo):
    #         self._MetaLevelUnderstoodRecords.createNewMetaLevelUnderstoodRecord(metaLevelUnderstoodInfo, thinkingObj)
    #     else:
    #         if throw_exception:
    #             raise Exception("不能从一种理解状态（%s）转到当前理解状态（%s）" % (self.curMetaLevelUnderstoodInfo, metaLevelUnderstoodInfo))
    #
    # def _canMetaLevelUnderstoodInfoTransfer(sel, metaLevelUnderstoodInfo):
    #     """
    #     判断能从上一种理解状态转到当前理解状态。
    #     :param metaLevelUnderstoodInfo:
    #     :return:
    #     """
    #     # todo 需要进行理解状态信息的判断（参考stateController）
    #     return True
    #
    # @property
    # def curMetaLevelUnderstoodRecord(self):
    #     """
    #     取得最新的理解状态信息
    #     :return:
    #     """
    #     try:
    #         return self._MetaLevelUnderstoodRecords[-1]
    #     except:  # 有可能取不到 ，忽略错误
    #         pass
    #
    # @property
    # def curMetaLevelUnderstoodInfo(self):
    #     """
    #     取得最新的理解状态信息
    #     :return:
    #     """
    #     try:
    #         _curMetaLevelUnderstoodRecord =self.curMetaLevelUnderstoodRecord
    #         if _curMetaLevelUnderstoodRecord:
    #             return _curMetaLevelUnderstoodRecord.metaLevelUnderstoodInfo
    #     except:  # 有可能取不到 ，忽略错误
    #         pass
    #
    # def getMetaLevelUnderstoodPath(self):
    #     """
    #     取得实际对象链的理解路径
    #     :return:
    #     """
    #     return self._MetaLevelUnderstoodRecords.getMetaLevelUnderstoodPath()

    def __repr__(self):
        return "{MetaLevelThinkingRecords:{%s,%s}}" % (self._MetaLevelExecuteRecords,
                                                           self._MetaLevelMatchRecords)
