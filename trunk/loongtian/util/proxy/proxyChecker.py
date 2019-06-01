#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import requests
# import urllib2
from loongtian.util.proxy import setting
from loongtian.util.helper.outputer import Outputer
import loongtian.util.helper.threadHelper as threadHelper

def checkProxy(proxy_urls,threadNum,checkedProxies):
    """
    检查多个http代理是否可用（多线程）。
    :rawParam proxy_urls:多个http代理
    :rawParam threadNum: 线程数
    :rawParam checkedProxies:可用的http代理
    :return:
    """
    if len(proxy_urls) > 0:
        Outputer.w('Checking the proxy is available..')

        def runer(q):
            while not q.empty():
                _proxyurl = q.get()
                if __checkProxy(_proxyurl):
                    Outputer.s('OK: %s' % _proxyurl)
                    checkedProxies.append(_proxyurl)
                else:
                    Outputer.e('NO: %s' % _proxyurl)

        #todo 这里需要重写
        threadHelper.startThread(proxy_urls, runer,threadNum)
    else:
        Outputer.i('Not proxy to checking..')
        
def __checkProxy(proxy_url):
    """
    （内部调用）检查http代理是否可用。
    :rawParam proxy_url:
    :return:
    """
    # 平均时间，平均成功次数
    time_avrage,succeed_avrage = __getTime(proxy_url)
    print (proxy_url +  '\ttimesec='+ str(time_avrage))
    if time_avrage < setting.timeout and succeed_avrage >setting.succeedavrage:
        return True
    return False


def __getTime(proxyurl):
    """
    （内部调用）经过多次查询，取得目标路径内容的平均时间
    @proxyurl： http代理
    :return:（平均时间，平均成功次数）
    """
    proxies = None
    if proxyurl.startswith('http://'):
        proxies = {'http': proxyurl}
    elif proxyurl.startswith('https://'):
        proxies = {'https': proxyurl}

    timetotal = 0
    succeed=0
    for x in range(setting.repeatTimes):
        timesec = 10
        start = time.time()
        try:
            rq = requests.get(setting.targetUrl, proxies = proxies, timeout = setting.timeout)
            # 如果取得的内容长度不等于目标长度，继续下一个
            if not len(rq.content )==setting.tagetSize:
                continue

            end = time.time()
            timesec = end - start
            succeed+=1
        except IOError as e:
            print ("IOError:" + str(e))

        timetotal += int(timesec * 1000)


    time_avrage = int(timetotal / setting.repeatTimes)
    succeed_avrage=succeed/setting.repeatTimes
    return time_avrage,succeed_avrage

# if __name__=="__main__":
#
#     print '-'*20,'workmanager.threadWorkerSize:', 555,'-'*20
#     print ('-'*20 + 'workmanager.threadWorkerSize:'+str(555) + '-'*20)


