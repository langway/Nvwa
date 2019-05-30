# /usr/bin/python
# coding: utf-8
__author__ = 'Leon'

from loongtian.nvwa.runtime.focus import Focus
from loongtian.nvwa.runtime.sequencedObjs import SequencedObjs
class AttentionManager(SequencedObjs):
    """
    注意力（关注对象列表）管理器。
    """

    def __init__(self):
        """
        注意力（关注对象列表）管理器。
        """
        super(AttentionManager, self).__init__(Focus)

        self.focuses =[]

        self.lastAttentionManager = None  # 上一个注意力（关注对象）管理器。
        self.nextAttentionManager = None  # 上一个注意力（关注对象）管理器。



