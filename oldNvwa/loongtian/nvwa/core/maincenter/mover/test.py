#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    test 
Author:   Liuyl 
DateTime: 2014/9/9 16:20 
UpdateLog:
1、Liuyl 2014/9/9 Create this File.

test
>>> print("No Test")
No Test
"""
__author__ = 'Liuyl'
import mover

if __name__ == '__main__':
    # 内存存储测试
    from loongtian.nvwa.service import common_srv

    common_srv.InitHelper.init()

    _words = [u'牛', u'有', u'腿']
    from loongtian.nvwa.core.maincenter.modeler.grouper import Grouper

    _grouper = Grouper()
    _group_result = _grouper.do_group(_words)
    for _group in _group_result:
        if hasattr(_group[1], 'Sequence') and len(_group[1].Sequence) != 0:
            if mover.match(_group[1].Sequence[0], _group):
                print(_group)