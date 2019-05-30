#!/usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import call

__author__ = 'Administrator'

# python - 随笔分类 - 秋楓 - 博客园
# http://www.cnblogs.com/rwxwsblog/category/698452.html

# 核心API — Scrapy 0.24.6 文档
# https://scrapy-chs.readthedocs.org/zh_CN/0.24/topics/api.html


# line="scrapy crawl gushiwen.org"
#
# # line="scrapy crawl dmoz -o items.json -t json"
#
# # line="scrapy crawl mininova.org -o mininova.org.json -t json"
# #
# #
# call(line, shell=False)


from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from loongtian .util .webcrawler .spiders import spiders
import loongtian.util.webcrawler.spiderHelper as spiderHelper
from loongtian.util.webcrawler.settings import USER_AGENTS,USER_AGENTS_LIST_FILE,PROXIES,PROXY_LIST_FILE

#要进行抓取的爬虫列表
proxySpidersList=[
    spiders.xicidailiProxySpider, # xicidaili抓取器
    spiders.kuaidailiSpider, # kuaidaili抓取器
    spiders.xroxySpider, # xroxy抓取器

]
# 初始化
spiderHelper.getProxiesOnWeb(proxySpidersList) # 从网络取得高匿代理列表
spiderHelper.resolveUserAgents(USER_AGENTS,USER_AGENTS_LIST_FILE) # 处理用户代理
spiderHelper.resolveProxies(PROXIES,PROXY_LIST_FILE) # 处理http代理

#要进行抓取的爬虫列表
spidersList=[
    spiders.gushiwenSpider, # 古诗文网抓取器

]
configure_logging()
runner = CrawlerRunner()
@defer.inlineCallbacks
def crawl():
    for spider in spidersList:
        yield runner.crawl(spider)

    reactor.stop()


crawl()
reactor.run() # the script will block here until the last crawl call is finished