#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
调用webServers获取关键词获取相关内容接口
Project:  loongtian/fuxi
Author:   js
DateTime: 2015/12/2
"""
import threading

from loongtian.nvwa.runtime.msgInfo import MsgInfo
from loongtian.fuxi import console


__author__ = 'js'

def getSearchData(input):
    """
    关键词获取相关搜索
    在此方法中调用webservers 获取数据处理后返回到页面
    :return:webServers 返回json格式数据
    """

    # 此处调用webservers获取返回数据， 之后需调整返回不用样式的html模板
    if input == u'':
        searchData = [{'title': u'您想知道什么？', 'type': u'text'}]
    elif input == u'哈哈':
        searchData = [{'title': u'呵呵呵呵呵呵呵呵呵呵！', 'type': u'text'}]
    elif input == u'忘情水' or input == u'我想听忘情水':
        searchData = [{'title': u'刘德华-忘情水', 'url': u'', 'type': u'music'}]
    elif input == u'速度与激情' or input == u'速度' or input == u'我想看速度与激情' :
        searchData = [{'title': u'速度与激情', 'url': u'', 'type': u'video'}]
    elif input == u'图片':
        searchData = [{'title': u'12岁男孩捡钥匙开走车', 'url': u'/static/photo/a.jpeg', 'type': u'images'}]
    elif input == u'刘德华':
        info = u"""
            刘德华（Andy Lau），1961年9月出生于中国香港，中国知名演员、歌手、词作人、制片人、电影人，
            影视歌多栖发展的代表艺人之一。1982年以全优成绩毕业于TVB艺训班签约出道，同年凭《猎鹰》走红，
            1983年主演《神雕侠侣》
            """
        searchData = [{'type': u'info', 'title': u'刘德华', 'url': u'/static/photo/a.jpeg', 'info': info
                    , 'tags': [{'title': u'演艺经历', 'url': u''}, {'title': u'主要作品', 'url': u''},
                                {'title': u'获奖记录', 'url': u''}]
        }]
    else:
        # 压入输入队列进行思考
        _lock = threading.Lock()
        _lock.acquire()
        console.input_queue.put(input)
        _lock.release()

        while True:
            _lock.acquire()
            # 等待输出队列返回结果
            if console.listener.output_queue.empty():
                _lock.release()
                continue

            _output =console.listener.output_queue.get()
            _lock.release()

            searchData = [{'title': _output, 'type': u'text'}]
            # 一旦有结果，终止循环
            break
    # 此处调用webservers获取返回数据， 之后需调整返回不用样式的html模板

    return searchData

