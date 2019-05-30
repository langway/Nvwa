#!/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = 'Leon'

"""
记忆中枢。
"""

from loongtian.nvwa.centrals.centralBase import CentralBase
from loongtian.nvwa.managers.inputsManager import InputsManager

from loongtian.nvwa.organs.memory import GeneralMemoryBase,PersistentMemory


class MemoryCentral(CentralBase, GeneralMemoryBase):
    """
    女娲大脑的记忆中枢
    """

    def __init__(self, brain):
        """
        女娲大脑的记忆中枢。
        :param brain:女娲大脑
        :remark
        """

        CentralBase.__init__(self, brain)
        GeneralMemoryBase.__init__(self)

        # # 供model模型调用
        # Memory.memory = self # 现改由用户memoryCentral维护
        # 元输入信息管理器（上下文），用以记录系统的输入信息
        self.InputsManager = InputsManager()

        # 持久记忆区（长久记忆，重启后不会被被擦除，类似于电脑硬盘数据或数据库，其遗忘速度较慢）
        if self.Brain :
            # 从DoubleFrequancyDict根据阀值和元输入的位置提取元数据（可能有多个）的频率阀值（超过该阀值才提取），包括：独立成字符块的阀值，连续连接成词的阀值。
            # MetaDataExtractThreshold_SingleBlock =0.09 # 从DoubleFrequancyDict根据阀值和元输入的位置提取元数据（可能有多个）的频率阀值（超过该阀值才提取），随着理解的元数据的增多，其阀值应该逐渐增加
            # 从metaNet根据阀值和元输入的位置提取元数据（可能有多个）的频率阀值（超过该阀值才提取）
            self.Threshold_ContinuousBlocks = self.Brain.Character.MetaDataExtractThreshold_ContinuousBlocks

            if self.Brain.CentralBrain:
                # 如果已经有了AdminBrain，直接赋值，并更改当前引擎的加载信息，避免重复调用
                self.PersistentMemory = self.Brain.CentralBrain.CentralMemory.PersistentMemory
                self.TextEngine._allMetaFromDBLoaded = True  # 标记已经加载数据库元数据，无需重新加载
                self.MetaNetEngine._allNgramDictFromDBLoaded = True  # 标记已从MetaNet数据库加载NgramDict，无需重新加载
            else:
                self.PersistentMemory = PersistentMemory(self)  # 基类没有进行实例化
        else:
            self.PersistentMemory = PersistentMemory(self) # 基类没有进行实例化