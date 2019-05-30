#encoding=utf-8
import os

from loongtian.fuxi import app
import random


def show_head(url_raw, size, type='users'):
    """
    处理模板图片不同尺寸显示
    :rawParam url_raw:图片原地址
    :rawParam size:显示图片尺寸
    :rawParam type:图片类型
    :return:返回拼接后的图片url
    """
    try:
        path = ''
        if type == 'users':
            path = '/static/photo/users/'
        url_raw_list = url_raw.split('.')
        url_new = '%s%s_%s.%s?%s' % (path, url_raw_list[0], size, url_raw_list[1], random.random())
        return url_new
    except Exception as e:
        pass
    return url_raw

env = app.jinja_env
env.filters['show_head'] = show_head
