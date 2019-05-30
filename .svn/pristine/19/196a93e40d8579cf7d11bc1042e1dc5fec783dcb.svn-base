#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    util.py 
Created by zheng on 2014/11/20.
UpdateLog:

"""


def get_match_random(n):
    '''
    生成指定长度的随机符合key值的字符串
    :param n: 要生成的字符串长度
    :return:
    '''
    '''
    :param n:
    :return:
    '''
    import random, string

    allw = 'abcdef' + string.digits
    r = []
    for i in xrange(n):
        r.append(random.choice(allw))
    return ''.join(r)


def get_match_string():
    return '.{8}-.{4}-.{4}-88' + get_match_random(2) + '-.{12}'


def clear_database():
    from entity_repository import RealObjectRepository, MetadataRepository, KnowledgeRepository

    KnowledgeRepository().clear()
    RealObjectRepository().clear()
    MetadataRepository().clear()


if __name__ == "__main__":
    clear_database()
    # from loongtian.nvwa.service import  metadata_srv,real_object_srv
    # metadata_srv.create(u'有')
    #tmp = metadata_srv.get_by_string_value(u'有')
    #print real_object_srv.gets(tmp.RealObjectList)
    #print metadata_srv.get_default_action(metadata_srv.get_by_string_value(u'有'))