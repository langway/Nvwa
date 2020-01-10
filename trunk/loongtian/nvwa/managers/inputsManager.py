#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Leon'

import datetime

from loongtian.nvwa.runtime.sequencedObjs import SequencedObjs

class InputsManager(SequencedObjs):
    """
    元输入信息管理器（上下文）
    """

    def __init__(self):
        """
        元输入信息管理器（上下文），用以记录系统的输入信息
        """
        # 限定被管理对象的类型
        super(InputsManager, self).__init__(objTypes=[str])

