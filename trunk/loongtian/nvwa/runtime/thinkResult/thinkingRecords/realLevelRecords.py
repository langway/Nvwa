#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

import uuid
import datetime
from loongtian.nvwa.runtime.systemInfo import ThinkingInfo
from loongtian.util.common.generics import GenericsList

class RealLevelEexecuteRecord():
    """
    nvwa对象的一条执行记录
    """

    def __init__(self, realLevelExecuteInfo = ThinkingInfo.RealLevelInfo.ExecuteInfo.UNKNOWN, thinkingObj = None):

        self.realLevelExecuteInfo = realLevelExecuteInfo

        self.thinkingObj = thinkingObj
        self.id = str(uuid.uuid1()).replace("-","")
        self.time = datetime.datetime.utcnow()  # 记录的时间

class RealLevelEexecuteRecords(GenericsList):
    """
    nvwa对象的执行记录(多个)
    """

    def __init__(self):
        super(RealLevelEexecuteRecords, self).__init__(RealLevelEexecuteRecord)


    def createNewRealLevelEexecuteRecord(self, realLevelExecuteInfo, thinkingObj):
        """
        创建nvwa对象的一条执行记录
        :param realLevelExecuteInfo:
        :param thinkingObj:
        :return:
        """
        _realLevelEexecuteRecord =RealLevelEexecuteRecord(realLevelExecuteInfo, thinkingObj)
        self.append(_realLevelEexecuteRecord)
        return _realLevelEexecuteRecord

    def getRealLevelExecutePath(self):
        """
        取得nvwa对象的执行路径
        :return:
        """
        path = ""
        for realLevelExecuteRecord in self:
            cur_path = ThinkingInfo.RealLevelInfo.ExecuteInfo.getName(realLevelExecuteRecord.realLevelExecuteInfo)
            if cur_path:
                path += cur_path + "-"

        path = path.lstrip("-")
        return path

    def __repr__(self):
        return "{RealLevelEexecuteRecords:%s}" % self.getRealLevelExecutePath()

class RealLevelMatchRecord():
    """
    nvwa数据对象的一条匹配记录（从元数据开始、元数据网、实际对象、知识链、知识链意义）
    """

    def __init__(self, realLevelMatchInfo = ThinkingInfo.RealLevelInfo.MatchInfo.UNKNOWN, thinkingObj = None):

        self.realLevelMatchInfo = realLevelMatchInfo
        self.thinkingObj = thinkingObj
        self.id = str(uuid.uuid1()).replace("-","")
        self.time = datetime.datetime.utcnow()  # 记录的时间

class RealLevelMatchRecords(GenericsList):
    """
    nvwa数据对象的匹配记录（从元数据开始、元数据网、实际对象、知识链、知识链意义）(多个)
    """

    def __init__(self):
        super(RealLevelMatchRecords, self).__init__(RealLevelMatchRecord)


    def createNewRealLevelMatchRecord(self, realLevelMatchInfo, thinkingObj):
        """
        创建nvwa数据对象的一条匹配记录（从元数据开始、元数据网、实际对象、知识链、知识链意义）
        :param realLevelMatchInfo:
        :param thinkingObj:
        :return:
        """
        _realLevelMatchRecord =RealLevelMatchRecord(realLevelMatchInfo, thinkingObj)
        self.append(_realLevelMatchRecord)
        return _realLevelMatchRecord


    def getRealLevelMatchPath(self):
        """
        取得nvwa数据对象的匹配路径
        :return:
        """
        path = ""
        for realLevelMatchRecord in self:
            cur_path = ThinkingInfo.RealLevelInfo.MatchInfo.getName(realLevelMatchRecord.realLevelMatchInfo)
            if cur_path:
                path += cur_path + "-"

        path = path.lstrip("-")
        return path

    def __repr__(self):
        return "{RealLevelMatchRecords:%s}" % self.getRealLevelMatchPath()

class RealLevelUnderstoodRecord():
    """
    实际对象链的一条理解记录
    """

    def __init__(self, realLevelUnderstoodInfo = ThinkingInfo.RealLevelInfo.UnderstoodInfo.UNKNOWN, thinkingObj = None):

        self.realLevelUnderstoodInfo = realLevelUnderstoodInfo
        self.thinkingObj = thinkingObj
        self.id = str(uuid.uuid1()).replace("-","")
        self.time = datetime.datetime.utcnow()  # 记录的时间

class RealLevelUnderstoodRecords(GenericsList):
    """
    实际对象链的理解记录(多个)
    """

    def __init__(self):
        super(RealLevelUnderstoodRecords, self).__init__(RealLevelUnderstoodRecord)


    def createNewRealLevelUnderstoodRecord(self, realLevelUnderstoodInfo, thinkingObj):
        """
        创建实际对象链的一条理解记录
        :param realLevelUnderstoodInfo:
        :param thinkingObj:
        :return:
        """
        _realLevelUnderstoodRecord =RealLevelUnderstoodRecord(realLevelUnderstoodInfo, thinkingObj)
        self.append(_realLevelUnderstoodRecord)
        return _realLevelUnderstoodRecord

    def getRealLevelUnderstoodPath(self):
        """
        取得实际对象链的理解路径
        :return:
        """
        path = ""
        for realLevelUnderstoodRecord in self:
            cur_path = ThinkingInfo.RealLevelInfo.UnderstoodInfo.getName(realLevelUnderstoodRecord.realLevelUnderstoodInfo)
            if cur_path:
                path += cur_path + "-"

        path = path.lstrip("-")
        return path

    def __repr__(self):
        return "{RealLevelUnderstoodRecords:%s}" % self.getRealLevelUnderstoodPath()

class RealLevelThinkingRecords():
    """
    关于元数据思考状态的信息记录（这些状态在思维处理中不断被改变，是单向、互斥的）。
    """

    def __init__(self, thinkResult):

        self.thinkResult = thinkResult

        self._RealLevelExecuteRecords = RealLevelEexecuteRecords()  # 按顺序设置的元数据链的执行记录(多个)
        self._RealLevelExecuteRecords.createNewRealLevelEexecuteRecord(ThinkingInfo.RealLevelInfo.ExecuteInfo.UNKNOWN, None) # 默认为未知

        self._RealLevelMatchRecords = RealLevelMatchRecords()  # 按顺序设置的nvwa数据对象的匹配记录（从元数据开始、元数据网、实际对象、知识链、知识链意义）(多个)
        self._RealLevelMatchRecords.createNewRealLevelMatchRecord(ThinkingInfo.RealLevelInfo.MatchInfo.UNKNOWN, None) # 默认为未知

        self._RealLevelUnderstoodRecords = RealLevelUnderstoodRecords()  # 按顺序设置的实际对象链的理解记录
        self._RealLevelUnderstoodRecords.createNewRealLevelUnderstoodRecord(ThinkingInfo.RealLevelInfo.UnderstoodInfo.UNKNOWN, None) # 默认为未知

    # ####################################
    # 执行状态信息
    # ####################################
    def isAllUnexecuted(self):
        """
        判断思考是否全都未执行。
        :return:
        """
        if self.curRealLevelExecuteInfo == ThinkingInfo.RealLevelInfo.ExecuteInfo.UNKNOWN:
            return True

        return False

    def setRealLevelExecuteRecord(self, realLevelExecuteInfo, thinkingObj, throw_exception=False):
        """
        设置执行状态信息。
        :param realLevelExecuteInfo:
        :return:
        """
        if self._canRealLevelExecuteInfoTransfer(realLevelExecuteInfo):
            return self._RealLevelExecuteRecords.createNewRealLevelEexecuteRecord(realLevelExecuteInfo, thinkingObj)
        else:
            if throw_exception:
                raise Exception("不能从一种执行状态（%s）转到当前执行状态（%s）" % (self.curRealLevelExecuteInfo, realLevelExecuteInfo))

    def _canRealLevelExecuteInfoTransfer(sel, realLevelExecuteInfo):
        """
        判断能从上一种执行状态转到当前执行状态。
        :param realLevelExecuteInfo:
        :return:
        """
        # todo 需要进行执行状态信息的判断（参考stateController）
        return True

    @property
    def curRealLevelExecuteRecord(self):
        """
        取得最新的执行状态记录。
        :return:
        """
        try:
            return self._RealLevelExecuteRecords[-1]
        except:  # 有可能取不到 ，忽略错误
            pass

    @property
    def curRealLevelExecuteInfo(self):
        """
        取得最新的执行状态信息
        :return:
        """
        try:
            _curRealLevelExecuteRecord= self.curRealLevelExecuteRecord
            if _curRealLevelExecuteRecord:
                return _curRealLevelExecuteRecord.metasExecuteInfo
        except:  # 有可能取不到 ，忽略错误
            pass

    def getRealLevelExecutePath(self):
        """
        取得nvwa对象的执行路径
        :return:
        """
        return self._RealLevelExecuteRecords.getRealLevelExecutePath()
    # ####################################
    # 匹配状态信息
    # ####################################

    def isRealObjectUnmatched(self):
        """
        判断实际对象是否未知（元数据已知）。
        :return:
        """
        return self.curRealLevelMatchInfo == ThinkingInfo.RealLevelInfo.MatchInfo.RELATED_REALS_UNMATCHED

    def isAllUnmatched(self):
        """
        判断元数据链是否全都未知（未能匹配）。
        :return:
        """
        if self.curRealLevelMatchInfo == ThinkingInfo.RealLevelInfo.MatchInfo.UNKNOWN:
            return True
        elif self.curRealLevelMatchInfo == ThinkingInfo.RealLevelInfo.MatchInfo.META_UNMATCHED:
            return True
        return self.thinkResult.realLevelResult.isAllUnknown()

    def setRealLevelMatchRecord(self, realLevelMatchInfo, thinkingObj, throw_exception=False):
        """
        设置匹配状态。
        :param realLevelMatchInfo:
        :return:
        """
        if self._canRealLevelMatchInfoTransfer(realLevelMatchInfo):
            self._RealLevelMatchRecords.createNewRealLevelMatchRecord(realLevelMatchInfo, thinkingObj)
        else:
            if throw_exception:
                raise Exception("不能从一种匹配状态（%s）转到当前匹配状态（%s）" % (self.curRealLevelMatchInfo, realLevelMatchInfo))

    def _canRealLevelMatchInfoTransfer(sel, realLevelMatchInfo):
        """
        判断能从上一种匹配状态转到当前匹配状态
        :param realLevelMatchInfo:
        :return:
        """
        # todo 需要进行匹配状态的判断（参考stateController）
        return True

    @property
    def curRealLevelMatchRecord(self):
        """
        取得最新的匹配信息
        :return:
        """
        try:
            return self._RealLevelMatchRecords[-1]
        except:  # 有可能取不到 ，忽略错误
            pass

    @property
    def curRealLevelMatchInfo(self):
        """
        取得最新的匹配信息
        :return:
        """
        try:
            _curRealLevelMatchRecord=self.curRealLevelMatchRecord
            if _curRealLevelMatchRecord:
                return _curRealLevelMatchRecord.realLevelMatchInfo
        except:  # 有可能取不到 ，忽略错误
            pass

    def getRealLevelMatchPath(self):
        """
        取得nvwa数据对象的匹配路径
        :return:
        """
        return self._RealLevelMatchRecords.getRealLevelMatchPath()

    # ####################################
    # 理解状态信息
    # ####################################
    def isAllUnunderstood(self):
        """
        判断思考是否全都未理解。
        :return:
        """
        if self.curRealLevelUnderstoodInfo == ThinkingInfo.RealLevelInfo.UnderstoodInfo.UNKNOWN:
            return True

        return False

    def setRealLevelUnderstoodRecord(self, realLevelUnderstoodInfo, thinkingObj, throw_exception=False):
        """
        设置理解状态信息。
        :param realLevelUnderstoodInfo:
        :return:
        """
        if self._canRealLevelUnderstoodInfoTransfer(realLevelUnderstoodInfo):
            self._RealLevelUnderstoodRecords.createNewRealLevelUnderstoodRecord(realLevelUnderstoodInfo, thinkingObj)
        else:
            if throw_exception:
                raise Exception("不能从一种理解状态（%s）转到当前理解状态（%s）" % (self.curRealLevelUnderstoodInfo, realLevelUnderstoodInfo))

    def _canRealLevelUnderstoodInfoTransfer(sel, realLevelUnderstoodInfo):
        """
        判断能从上一种理解状态转到当前理解状态。
        :param realLevelUnderstoodInfo:
        :return:
        """
        # todo 需要进行理解状态信息的判断（参考stateController）
        return True

    @property
    def curRealLevelUnderstoodRecord(self):
        """
        取得最新的理解状态信息
        :return:
        """
        try:
            return self._RealLevelUnderstoodRecords[-1]
        except:  # 有可能取不到 ，忽略错误
            pass

    @property
    def curRealLevelUnderstoodInfo(self):
        """
        取得最新的理解状态信息
        :return:
        """
        try:
            _curRealLevelUnderstoodRecord =self.curRealLevelUnderstoodRecord
            if _curRealLevelUnderstoodRecord:
                return _curRealLevelUnderstoodRecord.realLevelUnderstoodInfo
        except:  # 有可能取不到 ，忽略错误
            pass

    def getRealLevelUnderstoodPath(self):
        """
        取得实际对象链的理解路径
        :return:
        """
        return self._RealLevelUnderstoodRecords.getRealLevelUnderstoodPath()

    def __repr__(self):
        return "{RealLevelThinkingRecords:{%s,%s,%s}}" % (self._RealLevelExecuteRecords,
                                                           self._RealLevelMatchRecords,
                                                           self._RealLevelUnderstoodRecords)
