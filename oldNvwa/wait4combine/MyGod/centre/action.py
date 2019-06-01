#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
新建python文件
>>> print("No Test")
No Test
"""
from loongtian.nvwa.service.repository_service import memory as Selector

__author__ = 'Liuyl'
from baseCentre import BaseCentre as BaseCentre
from loongtian.nvwa.service.repository_service.memory.globalMemory import GlobalMemory as GlobalMemory


class ActionCentre(BaseCentre):
    def __init__(self):
        super(ActionCentre, self).__init__()
        self.memory = GlobalMemory().memory
        # 初始化Action列表
        action_list = [[record["key"], record["value"]["end"]] for record in
                       Selector.select_whole_end_restrict(self.memory, [61, 62], inherit=True)]
        #[[action[0], for action in action_list]
        print(action_list)
        # a = [
        # {"start": "X", "end": 22},
        # {"start": "0", "end": 1002},
        # {"start": "1", "end": 21},
        #     {"start": "2", "end": "Y"},
        # ]
        # metadata_X = [
        #     {"start": "X", "end": 0},
        # ]
        # metadata_Y = [
        #     {"start": "Y", "end": 12},
        #     {"start": "0", "end": 23},
        #     {"start": "1", "end": 1001},
        # ]
        # metadata_order, self._metadata = Selector.find_structure_variable2(
        #     self._global_memory.memory, metadata_structure, X=metadata_X, Y=metadata_Y)
        # if metadata_order[0] != 'X':
        #     self._metadata = [[link[1], link[0]] for link in self._metadata]


_instance = ActionCentre()


def GetCentre():
    return _instance


if __name__ == '__main__':
    GetCentre()
