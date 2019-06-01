#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    id_generator 
Author:   fengyh 
DateTime: 2014/9/4 10:40 
UpdateLog:
1、fengyh 2014/9/4 Create this File.
                    增加方法generate_unique_id。实现生成唯一Id。
2、fengyh 2014/9/5 将输出类型转换为字符串类型。

"""
import uuid


def generate_unique_id():
    """
    通用生成id的方法。
    提取这里方便未来变化生成Id的方式。
    fengyh 2014-9-4
    :return:
    """
    return str(uuid.uuid1())