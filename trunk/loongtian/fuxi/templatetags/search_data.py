#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from loongtian.fuxi import app
import random


def show_result(data, type='title'):
    """
    处理模板显示后台返回搜索数据
    :rawParam data:搜索数据json格式
    :return:返回处理后的结果
    """
    try:
        data = eval(data)
        data_new = data[0][type]
        try:
            return unicode(data_new, 'utf-8')
        except:
            return data_new
    except Exception as e:
        pass
    return data

env = app.jinja_env
env.filters['show_result'] = show_result

def show_unicode(data):
    """
    模板str类型报错，转换成unicode
    :rawParam data:str字符串
    :return:返回处理后的结果
    """
    try:
        return unicode(data, 'utf-8')
    except Exception as e:
        pass
    return ''

env = app.jinja_env
env.filters['show_unicode'] = show_unicode
