#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

from loongtian.nvwa.organs.character import Character
from loongtian.nvwa.runtime.relatedObjects import RelatedObj,LowerObjs

class LinearExecutionInfo(object):
    """
    线性动作对象的可执行信息，例如：牛-有-腿（多模式，多意义）
    """

    def __init__(self, real):
        """
        线性动作对象的可执行信息，例如：牛-有-腿（多模式，多意义）
        :param real:
        """
        self.real = real
        self.pattern_knowledges = None  # (LowerObjs)从数据库中取得的模式知识链（ObjType.EXEINFO类型的LowerObjs）
        self.meaning_knowledges = {}  # （{pattern.id:LowerObjs}）从数据库中取得的意义知识链

        self.meaning_value_dict = {}  # {meaning.id:realobject} # 值（实际对象，父对象构成没有值）
        # ####################################
        #      下面为运行时数据
        # ####################################
        self.cur_pattern = None

    def isExecutable(self):
        """
        动作对象是否可执行（必须至少有一个pattern及其对应的meaning）
        :return:
        """
        if self.meaning_knowledges:
            return True
        return False

    def getCur(self):
        """
        取得当前的模式及意义知识链、意义值（顺序下一个）。
        :return:cur_pattern, cur_meaning,cur_meaning_value
        """
        if not self.cur_pattern and self.pattern_knowledges:  # 模式
            self.cur_pattern = self.pattern_knowledges.getCurObj()

        if not self.cur_pattern:  # 没有pattern了，直接返回
            return None, None, None

        cur_meanings = self.meaning_knowledges.get(self.cur_pattern.id)
        if cur_meanings:  # 意义
            cur_meaning = cur_meanings.getCurObj()
            if cur_meaning:
                # 意义的值
                cur_meaning_value = self.meaning_value_dict.get(cur_meaning.id)
                return self.cur_pattern, cur_meaning, cur_meaning_value
            else:  # 如果没取到，已经是最后一个了，递归取下一个,直到没有pattern
                self.cur_pattern = None
                return self.getCur()
        else:
            # return self.cur_pattern,None
            raise Exception("可执行的实际对象有模式，但没有对应的意义！")

    def restoreCurObjIndex(self):
        """
        将当前可执行信息所处的位置重置为0（模式及模式的意义）
        :return:
        """
        self.pattern_knowledges.restoreCurObjIndex()
        for key,meaning_knowledge in self.meaning_knowledges.items():
            meaning_knowledge.restoreCurObjIndex()

    def add(self, pattern_klg, meaning_klg, value_placeholder=None, pattern_weight=Character.Original_Link_Weight,
            meaning_weight=Character.Original_Link_Weight):
        """
        添加可执行性信息
        :param pattern_klg: 模式知识链
        :param meaning_klg: 意义知识链
        :return:
        """
        # 检查参数
        from loongtian.nvwa.models.knowledge import Knowledge
        if not pattern_klg or not isinstance(pattern_klg, Knowledge):
            raise Exception("应提供模式知识链！")
        if not meaning_klg or not isinstance(meaning_klg, Knowledge):
            raise Exception("应提供意义知识链！")
        if self.pattern_knowledges is None:
            self.pattern_knowledges = LowerObjs()
        self.pattern_knowledges.add(pattern_klg, pattern_weight, source=self.real)

        if self.meaning_knowledges is None:
            self.meaning_knowledges = {}

        cur_meaning_knowledges = self.meaning_knowledges.get(pattern_klg.id)
        if cur_meaning_knowledges:
            cur_meaning_knowledges.add(meaning_klg)
        else:
            cur_meaning_knowledges = LowerObjs()
            cur_meaning_knowledges.add(meaning_klg, meaning_weight, pattern_klg)
            self.meaning_knowledges[pattern_klg.id] = cur_meaning_knowledges

        # 检查可执行信息的值
        if not value_placeholder is None:
            value_placeholder = self.get_meaning_value(value_placeholder)
        self.meaning_value_dict[meaning_klg.id] = value_placeholder

    def get_meaning_value(self, value_placeholder):
        """
        检查可执行信息的值
        :param value_placeholder:
        :return:
        """
        if isinstance(value_placeholder, LowerObjs):
            if not len(value_placeholder) == 1:
                raise Exception("女娲系统的意义的值只能有一个实际对象，或为一个表示集合的实际对象！")
            meaning_value = value_placeholder.getCurObj()
            if isinstance(meaning_value, RelatedObj):
                meaning_value = meaning_value.obj
            value_placeholder = meaning_value

        from loongtian.nvwa.models.realObject import RealObject
        if not isinstance(value_placeholder, RealObject):
            raise Exception("可执行信息的值必须是一个实际对象！")
        if not value_placeholder.isPlaceHolder():
            raise Exception("可执行信息的值必须是一个占位符！")

        return value_placeholder


class ConjugatedExecutionInfo(LinearExecutionInfo):
    """
    共轭执行信息，例如：因为...所以...
    """
    def __init__(self, real):
        """
        线性动作对象的可执行信息，例如：牛-有-腿（多模式，多意义）
        :param real:
        """
        super(ConjugatedExecutionInfo,self).__init__(real)

        self.conjugatedExecutabls=[] #  与其共轭的可执行对象[(位置,实际对象)]

class ContextExecutionInfo(object):
    """
    上下文的执行信息，例如：系统：牛-有-腿，上文：牛-有-腿-吗，下文：有，其中，吗这个动作，要对上下文进行处理
    """

