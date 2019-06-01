# /usr/bin/python
# coding: utf-8
__author__ = 'Leon'

"""
nvwa的注意力模型的封装类（实际对象、知识链）
"""

from datetime import datetime
from loongtian.nvwa.runtime.sequencedObjs import SequencedObj

"""
[运行时对象]nvwa的注意力模型的封装类（实际对象、知识链）
关注度的计算：
1、根据输入的先后，越靠前，关注度越高
2、根据一次输入的对象的激活度（meta.weight,real.weight），可计算出关注度；例如：牛有腿，腿有毛，有、腿先后出现了两次
3、根据情感刺激度（计算方法参见emotion）

综上，关注度的计算公式 为：
  Focus.degree = meta.weight×real.weight×注意顺序的权重×情感刺激度
"""
class Focus(SequencedObj):
    """
    [运行时对象]nvwa的注意力模型的封装类（实际对象、知识链）
    """

    def __init__(self,obj):
        """
        [运行时对象]nvwa的注意力模型的封装类（实际对象、知识链）
        """
        super(Focus, self).__init__()
        self.obj = obj  # 被关注的实际对象、知识链
        self.positions=[] # 注意的位置，例如：牛有腿牛是动物，这里的牛，positions=[0,3]
        self.weight = 0.0
        self.targetEmotion = None  # 目标情感

        self.starttime = datetime.utcnow()
        self.endtime = datetime.utcnow()

    def increase(self,times):
        """
        增加指定次数的关注
        :param times: 指定次数
        :return:
        """

    def decrease(self,times):
        """
        减少指定次数的关注
        :param times: 指定次数
        :return:
        """


    def calculateWeight(self):
        """
        计算关注点的权重
        :return:
        """

