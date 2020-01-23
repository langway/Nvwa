#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

from abc import ABC
from loongtian.util.log import logger

class CentralBase(ABC):
    """
    各中枢的基础类。
    :rawParam
    构造函数参数说明
    :attribute
    对象属性说明
    """

    def __init__(self,brain):
        if not brain :
            try:
                from loongtian.nvwa.runtime.reals import AdminUser
                from loongtian.nvwa.organs.brain import Brain
                brain=Brain()
            except Exception as e:
                logger.critical(e)
                raise Exception("必须提供女娲大脑！Brain is None!")

        self.Brain=brain
        pass