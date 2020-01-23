#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

import os
import types
from loongtian.util.helper import  fileHelper
import loongtian.util.helper.jsonHelper as jsonHelper
from loongtian.util.log.logger  import logger

def removeDuplicateList(candidate_list):
    """
    列表去重
    :rawParam list:
    :return:
    """
    result=list(set(candidate_list))

    return result

def resolveUserAgents(USER_AGENTS,USER_AGENTS_LIST_FILE):
    """
    预处理用户代理
    :return:
    """
    user_agents=fileHelper.readLines(USER_AGENTS_LIST_FILE)
    if not len(user_agents)==len(USER_AGENTS):
        user_agents.extend(USER_AGENTS)
        del USER_AGENTS[:]# 清空列表
        USER_AGENTS.extend(removeDuplicateList(user_agents))
        fileHelper.writeLines(USER_AGENTS_LIST_FILE,user_agents)

def resolveProxies(PROXIES,PROXY_LIST_FILE):
    """
    预处理http代理
    :return:
    """
    proxieDicts=jsonHelper.loadObjectsFromJsonFile(PROXY_LIST_FILE)

    proxies={}
    for proxy in proxieDicts:
        import types
        if type(proxy) is types.DictionaryType:
            proxies.update(proxy)
        else:
            proxies[proxy]=""

    if not len(proxies)==len(PROXIES):
        proxies.update(PROXIES)
        PROXIES.clear()# 清空列表
        PROXIES.update(proxies)
        jsonHelper.saveObjectToFile(PROXIES,PROXY_LIST_FILE)



def trimList(list):
    """
    对抓取结果（一般是个列表）进行处理，包括：去除空白项，如果只有一个元素，直接返回该元素等
    :rawParam list:
    :return:
    """
    if not type(list)== types.ListType:# 目前只处理list类型
        return list

    if len(list)<=0:
        return None
    result=[]
    for item in list :
        if item==None :
            continue
        item =item.strip().strip("\r\n").strip("\r").strip("\n")
        if item =="":
            continue
        result.append(item)
    if len(result )==0: # 如果仍然没有，返回None
        return None
    if len(result )==1: # 如果只有一个，只返回第一个
        return result[0]

    return result

def checkResult(name,fetched,throwExcetion=True):
    """
    检查抓取结果，如果没有取到，需要记录，并报错
    :rawParam name:
    :rawParam fetched: 抓取结果
    :return:
    """
    if fetched is None:
        ex="当前{0}的抓取结果{0}为空，请检查抓取规则！".format(name )
        logger.logger.exception(ex)
        if throwExcetion:
            raise FetchContentNullException(ex)

class FetchContentNullException(Exception ):
    """
    抓取结果为空的错误
    """
    pass


from settings import USER_AGENTS,USER_AGENTS_LIST_FILE,PROXIES,PROXY_LIST_FILE


if __name__=="__main__":

    resolveUserAgents(USER_AGENTS,USER_AGENTS_LIST_FILE)

    resolveProxies(PROXIES,PROXY_LIST_FILE)

    print (USER_AGENTS,PROXIES)

