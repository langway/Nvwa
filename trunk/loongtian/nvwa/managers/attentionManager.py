# /usr/bin/python
# coding: utf-8
__author__ = 'Leon'

from loongtian.nvwa.models.baseEntity import BaseEntity
from loongtian.nvwa.runtime.focus import Focus
from loongtian.nvwa.runtime.sequencedObjs import SequencedObjs
from loongtian.nvwa.organs.character import Character

class AttentionManager(SequencedObjs):
    """
    注意力（关注对象列表）管理器。
    """

    def __init__(self):
        """
        注意力（关注对象列表）管理器。
        """
        super(AttentionManager, self).__init__(Focus)

        self.focuses ={}

        self.UpperAttentionManager=None

        self.lastAttentionManager = None  # 上一个注意力（关注对象）管理器。
        self.nextAttentionManager = None  # 上一个注意力（关注对象）管理器。

    def addFocus(self,obj):
        """
        添加一个关注点
        :param obj:
        :return:
        """
        if not isinstance(obj,BaseEntity):
            raise Exception("必须提供BaseEntity或其子类！")
        if obj.id in self.focuses.has_key:
            _focus=self.focuses.get(obj.id)
            _focus.increase(1)
            _focus.positions.append(len(self.focuses))

        else:
            _focus=Focus(obj)
            _focus.increase(1)
            _focus.positions.append(len(self.focuses))
            self.focuses[obj.id]=_focus

        _focus.calculateWeight() # 计算关注点的权重
        # 判断是否超过了注意力的值，如超过，对其进行处理
        if _focus.weight>=Character.Focus.Ratio:
            if self.UpperAttentionManager:
                pass

            return True

        return False






