#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

import random
import base64
from settings import PROXIES
from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware
from loongtian .util.log.logger import  logger

class RandomUserAgentMiddleware(UserAgentMiddleware):
    """
    随机选取用户
    Randomly rotate user agents based on a list of predefined ones
    """

    def __init__(self, agents):
        super(RandomUserAgentMiddleware, self).__init__()
        self.agents = agents

    @classmethod
    def from_crawler(cls, crawler):
        """
        这里给爬虫提供了一个静态方法以便获取用户代理列表，以便创建RandomUserAgent的实例
        :rawParam crawler:
        :return:
        """
        user_agents=list(set(crawler.settings.getlist('USER_AGENTS')))

        return cls(user_agents)

    def process_request(self, request, spider):
        """
        重载的用户方法，取得随机用户代理
        :rawParam request:
        :rawParam spider:
        :return:
        """
        ua = None
        while ua is None:# 这里保证一定能取到用户代理
            ua=random.choice(self.agents)

        if ua:
            #显示当前使用的useragent
            print "********Current UserAgent:%s************" %ua

            #记录
            logger.info('Current UserAgent: '+ua)
            request.headers.setdefault('User-Agent', ua)



class ProxyMiddleware(object):
    """
    scrapy 网络采集使用代理
    在项目配置文件里(./project_name/settings.py)添加如下字段：
    DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
    'project_name.middlewares.ProxyMiddleware': 100,}
    """
    def process_request(self, request, spider):
        """
        对request进行处理，
        :rawParam request:
        :rawParam spider:
        :return:
        """
        # Don't overwrite with a random one (server-side state for IP)
        # 如果request已经有了代理，不进行覆盖，直接返回
        if 'proxy' in request.meta:
            return

        proxy = self.randomChoiceProxy(PROXIES)
        ip_port= self.safetyJoinAddress(proxy[0])
        if ip_port is None:
            raise Exception("ip_port IS None,please check PROXIES in setting!")

        request.meta['proxy'] = ip_port

        user_pass= proxy[1]
        if user_pass is not None:
          encoded_user_pass = base64.encodestring(user_pass)
          request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
          print ("**************ProxyMiddleware with pass************" + ip_port)
        else:
          print ("**************ProxyMiddleware without pass************" + ip_port)


    def safetyJoinAddress(self,ipAddress):
        """
        安全拼接浏览地址。
        :rawParam ipAddress:
        :return:
        """

        if ipAddress ==None or ipAddress =="":
            return None
        if ipAddress .startswith("http://") or ipAddress .startswith("https://") :
            return ipAddress
        if ipAddress .startswith("//"):
            return "http:"+ipAddress

        return "http://%s" % ipAddress

    def process_exception (self, request, exception, spider) :
        """
        当抓取进程出现错误，删除导致错误的代理
        :rawParam request:
        :rawParam exception:
        :rawParam spider:
        :return:
        """
        proxy = request.meta['proxy']
        proxy=proxy.lstrip("http://").lstrip("https://") # 去掉前面的http头

        logger.debug( 'Removing failed proxy <%s>, %d proxies left' % (proxy, len(PROXIES)))

        try :
            del PROXIES[proxy]
        except ValueError:
            pass

    def randomChoiceProxy(self,PROXIES):
        """
        在当前代理列表（字典）中随机选择一个proxy
        :rawParam PROXIES:
        :return:
        """
        #生成一个长度范围内的随机位置
        index=int(random.random() * len(PROXIES))

        counter=0
        for proxy in PROXIES.items():
            if index ==counter:
                return proxy
            counter+=1

        return None


if __name__ == "__main__":
    proxyTest=ProxyMiddleware()

    proxy=proxyTest .randomChoiceProxy(PROXIES )
    print(proxy)

    ipAddress="http://111.222.234.567:80"

    print (proxyTest.safetyJoinAddress(ipAddress) )

    ipAddress="111.222.234.567:80"

    print (proxyTest.safetyJoinAddress(ipAddress) )

    ipAddress =""

    print (proxyTest.safetyJoinAddress(ipAddress) )







