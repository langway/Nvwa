#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
语言中枢
>>> print("No Test")
No Test
"""
from loongtian.nvwa.service.repository_service import memory as Selector

__author__ = 'Liuyl'
import baseCentre
import jieba
from loongtian.nvwa.service.repository_service.memory.globalMemory import GlobalMemory as GlobalMemory
from loongtian.nvwa.service.repository_service.memory.globalMemory import deep_remember


class LanguageCentre(baseCentre.BaseCentre):
    def __init__(self):
        super(LanguageCentre, self).__init__()
        self.memory = GlobalMemory().memory
        # 词库
        self._words = [
            [6001, u"牛"],
            [6003, u"的"],
            [6002, u"名字"],
            [6004, u"是"],
            [6005, u"有"]
        ]
        self.__init_words_link()

    def __init_words_link(self):
        # 提取object和对应的词的映射关系
        metadata_structure = [
            {"start": "X", "end": 22},
            {"start": "0", "end": 1002},
            {"start": "1", "end": 21},
            {"start": "2", "end": "Y"},
        ]
        metadata_X = [
            {"start": "X", "end": 0},
        ]
        metadata_Y = [
            {"start": "Y", "end": 12},
            {"start": "0", "end": 23},
            {"start": "1", "end": 1001},
        ]
        metadata_order, self._metadata = Selector.find_structure_variable2(
            self.memory, metadata_structure, X=metadata_X, Y=metadata_Y)
        if metadata_order[0] != 'X':
            self._metadata = [[link[1], link[0]] for link in self._metadata]
            # print(self.__metadata)

        # 提取词与词所对应的机器表示的映射关系
        machine_structure = [
            {"start": "X", "end": 24},
            {"start": "0", "end": "Y"},
        ]
        machine_X = [
            {"start": "X", "end": 12},
            {"start": "0", "end": 23},
            {"start": "1", "end": 1001},
        ]
        machine_Y = [
            {"start": "Y", "end": 13},
        ]
        machine_order, self._machine = Selector.find_structure_variable2(
            self.memory, machine_structure, X=machine_X, Y=machine_Y)
        if machine_order[0] != 'X':
            self._machine = [[link[1], link[0]] for link in self._machine]
        # print(self.__machine)
        self._words_link = [x + [y[-1]] for x in self._machine for y in self._words if x[1] == y[0]]
        # print(self._words_link)

    def decode(self, information):
        word_list = [word for word in list(jieba.cut(information)) if word.strip() != '']
        print(','.join(word_list))
        self.handle_unknown(word_list)

        objects = [y[0] for x in word_list for y in self._words_link if x == y[2]]
        # print(objects)
        knowledge = str(objects)
        return knowledge

    def encode(self, knowledge):
        output = knowledge
        return output

    def handle_unknown(self, word_list):
        unknown = [x for x in word_list if x not in [y[2] for y in self._words_link]]
        if len(unknown) == 0:
            return
        for word in unknown:
            # 关联词的编码和机器表示,并记忆此机器表示
            id_machine = deep_remember(-1, 13)
            self._words.append([id_machine, word])
            # 记忆一个中文词
            id_word = deep_remember(-1, 12, 23, 1001)
            # 关联中文词与机器表示
            deep_remember(id_word, 24, id_machine)
            # 定义object 并关联object与词
            deep_remember(-1, 0, 22, 1002, 21, id_word)
        self.__init_words_link()


_instance = LanguageCentre()


def GetCentre():
    return _instance


if __name__ == '__main__':
    # import doctest

    # doctest.testmod()
    LanguageCentre()
