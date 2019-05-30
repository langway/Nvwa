#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'


from loongtian.nvwa.organs.memory import GeneralMemoryBase,PersistentMemory

class CentralMemory(GeneralMemoryBase):
    """
    中央大脑的记忆中枢（用来管理永久记忆）
    """

    def __init__(self, centralBrain):
        """
        中央大脑的记忆中枢（用来管理永久记忆）
        :param centralBrain:
        """
        super(CentralMemory,self).__init__()
        # todo 待将用户记忆中枢的数据移植过来，然后每个用户的记忆中枢创建时，将浅拷贝其中的数据，实现数据隔离
        self.CentralBrain = centralBrain

        # 持久记忆区（长久记忆，重启后不会被被擦除，类似于电脑硬盘数据或数据库，其遗忘速度较慢）
        self.PersistentMemory = PersistentMemory(self) # 基类没有进行实例化

