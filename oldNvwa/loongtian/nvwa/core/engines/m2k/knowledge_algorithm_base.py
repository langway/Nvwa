#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    knowledge_algorithm_base 
Author:   fengyh 
DateTime: 2014-10-29 10:33 
UpdateLog:
1、fengyh 2014-10-29 Create this File.
2、fengyh 2014-11-04

"""
import itertools


class KnowledgeAlgorithmBase(object):
    """
    提取知识算法基类
    """

    def __init__(self, t_frag_list_before):
        self.FragList = t_frag_list_before
        self.KnowledgeResult = []
        pass

    def distill(self):
        return self.KnowledgeResult


class KnowledgeAlgorithmSimpleExistNTimes(KnowledgeAlgorithmBase):
    """
    出现N次即认为是知识，最简单的提取知识算法。
    """

    def __init__(self, t_frag_list_before, n):
        super(KnowledgeAlgorithmSimpleExistNTimes, self).__init__(t_frag_list_before)
        self.Threshold_N = n
        pass

    def distill(self):
        # 去重
        # 由于改变了Fragment的hash函数,导致这里的去重失效,临时修改去重逻辑,不完善 liuyl 2014.11.11
        from loongtian.nvwa.service import fragment_srv

        _dict = dict()
        for _t in self.FragList:
            # 去掉时间和感知器层
            _k = fragment_srv.get_deep_start(fragment_srv.get_deep_start(_t))
            if not _k:
                continue
            if _k.ref.Id in _dict:
                _dict[_k.ref.Id][1] += 1
            else:
                _dict[_k.ref.Id] = [_t, 1]
        for _item in _dict.values():
            if _item[1] >= self.Threshold_N:
                self.KnowledgeResult.append(_item[0])
        # t_model_set = set(self.FragList)
        # for t in t_model_set:
        # t_count = self.FragList.count(t)
        # if t_count >= self.Threshold_N:
        # self.KnowledgeResult.append(t)
        return self.KnowledgeResult
        pass


class KnowledgeAlgorithmSimpleExistNOneByOne(KnowledgeAlgorithmBase):
    """
    连续出现达到或超过N次即认为是知识，简单的提取知识算法。
    """

    def __init__(self, t_frag_list_before, n):
        super(KnowledgeAlgorithmSimpleExistNOneByOne, self).__init__(t_frag_list_before)
        self.Threshold_N = n
        pass

    def distill(self):
        # 用groupby方法对连续元素进行分组，得到连续并且长度超过指定值的列表。
        kr = [t1 for t1, t2 in itertools.groupby(self.FragList) if len(list(t2)) >= self.Threshold_N]
        # 去除不连续各段都符合要求的重复对象。
        self.KnowledgeResult.extend(set(kr))
        return self.KnowledgeResult


class KnowledgeAlgorithmManage(object):
    """
    实现支持多个算法叠加应用提取知识。
    """

    def __init__(self, *algorithms):
        self.AlgorithmsList = algorithms
        self.AlgorithmResult = []

    def distill_and(self):
        """
        将输入算法集求与关系，交集。
        :return:
        """
        for index, a in enumerate(self.AlgorithmsList):
            if index == 0:
                self.AlgorithmResult = a.distill()
            else:
                self.AlgorithmResult = set(self.AlgorithmResult).intersection(a.distill())
        return list(self.AlgorithmResult)


    def distill_or(self):
        """
        将输入算法集求并关系，并集。
        :return:
        """
        for index, a in enumerate(self.AlgorithmsList):
            if index == 0:
                self.AlgorithmResult = a.distill()
            else:
                self.AlgorithmResult = set(self.AlgorithmResult).union(a.distill())
        return list(self.AlgorithmResult)

    def distill_difference(self):
        """
        将输入算法集求差集。即符合某算法但不符合其它算法。
        暂时不实现。
        :return:
        """
        pass