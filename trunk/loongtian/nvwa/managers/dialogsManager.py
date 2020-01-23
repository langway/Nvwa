#!/usr/bin/env python

__author__ = 'Leon'

from loongtian.util.common.generics import GenericsList

from loongtian.nvwa.models.realObject import RealObject
from loongtian.nvwa.runtime.sequencedObjs import SequencedObjs
from loongtian.nvwa.runtime.article import StrContent, DialogDirection


class Dialog(SequencedObjs):
    """
    对话类的字串符的包装类。
    """

    def __init__(self):
        """
        对话类的字串符的包装类。
        :param ask:
        :param anwser:
        """
        # 限定被管理对象的类型
        super(Dialog, self).__init__(objTypes=[StrContent])

        self.subjects = GenericsList(item_type=RealObject)  # 当前对话的主题对象（可能有多个）

    def addInput(self, rawInput: str):
        """
        添加输入字符串
        :param rawInput:
        :return:
        """
        article=A

    def addRawOutput(self, rawOuput: str):
        """
        添加输出字符串
        :param rawOuput:
        :return:
        """

    def getLastInput(self):
        """
        取得最近一次的输入信息
        :return:
        """

        for i in range(len(self) - 1, -1, -1):
            if self[i].dialogDirection == DialogDirection.Input:
                return self[i]
        return None


class DialogsManager(SequencedObjs):
    """
    元输入信息管理器（上下文）
    """

    def __init__(self):
        """
        元输入信息管理器（上下文），用以记录系统的输入信息
        """
        # 限定被管理对象的类型
        super(DialogsManager, self).__init__(objTypes=[Dialog])

        self.Inputs = SequencedObjs(objTypes=[StrContent])

    def addStrContent(self, input:StrContent):
        """
        添加输入或输出字符串
        :param input:
        :return:
        """
        self.Inputs.add(input)



    def getRelatedDialogsBySubjects(self, subjects: list):
        """
        根据主题（可能有多个）取得相关对话的包装类（可能有多个，根据相关度排序）
        :param subjects:
        :return:
        """
        subjects = set(subjects)
        dialogs = {}
        for cur_dialog in self:
            cur_subjects = set(cur_dialog.containedObj.subjects)
            intersection = subjects & cur_subjects
            if len(intersection) > 0:
                dialogs[cur_dialog.containedObj] = len(intersection) / len(subjects)  # todo 目前只考虑占比
        return dialogs

