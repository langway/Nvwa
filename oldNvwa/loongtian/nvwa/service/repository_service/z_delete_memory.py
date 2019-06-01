#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    memory 
Author:   Liuyl 
DateTime: 2014/10/29 13:51 
UpdateLog:
1、Liuyl 2014/10/29 Create this File.

memory
>>> print("No Test")
No Test
"""
__author__ = 'Liuyl'
from loongtian.nvwa.service.repository_service.knowledge import BaseKnowledgeService
from loongtian.nvwa.common.storage.db.entity_repository import memory_rep


class MemoryService(BaseKnowledgeService):
    def __init__(self):
        super(MemoryService, self).__init__(memory_rep)



if __name__ == '__main__':
    import doctest

    doctest.testmod()