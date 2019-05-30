#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Leon'

from loongtian.nvwa.runtime.sequencedObjs import SequencedObjs

class MessagesManager(SequencedObjs):
    """
    消息队列管理器。
    """


    def __init__(self):
        """
        元输入信息管理器（上下文）
        """
        # 限定被管理对象的类型
        super(MessagesManager, self).__init__(objType=str)