#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

import json

class MsgInfo(object):
    """
    客户端与服务器端通信信息的包装类。
    """

    def __init__(self):
        """
        客户端与服务器端通信信息的包装类。
        """
        self.msg = None
        self.client_address = None
        self.facility = None # 当前的用户设备，目前包括：console、网页、Android、ios等，用以调用不同的登录、登出界面
                            # 100-输入输出面板；200-webpage；300-Android；400-iOS
    def fromStr(self,_str):
        """
        从json字符串加载属性
        :param str:
        :return:
        """
        dict=json.loads(_str)
        if not dict:
            raise Exception("非json格式字符串！")

        for attribute,value in dict.items():
            if hasattr(self,attribute.lower()):
                setattr(self,attribute, value)

    def toStr(self):
        """
        将属性值转化成json字符串
        :return:
        """
        dict = {
            "msg": self.msg,
            "client_address": self.client_address,
            "facility": self.facility,
        }
        return json.dumps(dict)
