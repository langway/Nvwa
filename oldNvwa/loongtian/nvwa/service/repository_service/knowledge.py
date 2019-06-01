#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Project:  nvwa
Title:    knowledge 
Author:   liuyl 
DateTime: 2014/9/5 10.59 
UpdateLog:
1、liuyl 2014/9/5 Create this File.


knowledge服务层
>>> print("No Test")
No Test
"""
from loongtian.nvwa.common.storage.db.entity_repository import knowledge_rep
from loongtian.nvwa.service.repository_service.base_knowledge_service import BaseKnowledgeService

__author__ = 'Liuyl'


class KnowledgeService(BaseKnowledgeService):
    def __init__(self):
        super(KnowledgeService, self).__init__(knowledge_rep)


if __name__ == '__main__':
    # import doctest
    #
    # doctest.testmod()

    # 内存存储测试
    from loongtian.nvwa.service import original_init_srv
    original_init_srv.init()

    # 数据库存储测试
    # import loongtian.nvwa.entities.inited_knowledge as db_dict

    # _dict = db_dict.dict

    # 以下不变
    # _parent_id = common_srv.get_knowledge_id_by_display(u'父对象')
    # _animal_id = common_srv.get_knowledge_id_by_display(u'动物类')
    # result = base_deduce_forward(_parent_id, _animal_id)
    # for res in result:
    # print([item[0] for item in common_srv.display_dict.items() if item[1] == res][0])
    # print(base_verify_forward(common_srv.get_knowledge_id_by_display(u'牛类'), _parent_id, _animal_id))
    # print(base_verify_forward(common_srv.get_knowledge_id_by_display(u'马类'), _parent_id, _animal_id))
    # print(base_verify_forward(common_srv.get_knowledge_id_by_display(u'羊类'), _parent_id, _animal_id))

    # knowledge_srv.select_bridge(original_base_srv.get(u'牛类'), original_base_srv.get(u'腿'))