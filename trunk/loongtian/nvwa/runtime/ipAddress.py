#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

from loongtian.util.common.generics import GenericsList

class IPAddress(object):
    """
    IP地址的包装类
    """

    def __init__(self,ip=None,port=None):
        """
        IP地址的包装类
        :param ip:
        :param port:
        """
        self.ip=ip
        self.port=port

    @property
    def id(self):
        return self.getAddress()

    def getAddress(self):
        """
        取得真正的ip地址。
        :return:
        """
        if self.ip:
            if self.port:
                return "%s:%s" % (self.ip, self.port)
            else:
                return self.ip

        return ""



class IPAddressList(GenericsList):
    """
    IP地址的包装类的泛型列表
    """
    def __init__(self):
        """
        IP地址的包装类的泛型列表
        """
        super(IPAddressList,self).__init__(item_type=IPAddress)
        self.ip_address_dict={}

    def add(self,host,port):
        """
        添加IP地址
        :param host:
        :param port:
        :return:
        """
        _IPAddress=IPAddress(host,port)
        if _IPAddress.getAddress() in self.ip_address_dict:
            return
        self.ip_address_dict[_IPAddress.getAddress()]=_IPAddress
        self.append(_IPAddress)

    def get(self,host,port):
        """
        取得IP地址的包装类
        :param host:
        :param port:
        :return:
        """
        _IPAddress = IPAddress(host, port)
        if _IPAddress.getAddress() in self.ip_address_dict:
            return self.ip_address_dict[_IPAddress.getAddress()]
        return None
