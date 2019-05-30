#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Administrator'

"""
参考： 选择器(Selectors) — Scrapy 0.24.1 文档
http://scrapy-chs.readthedocs.org/zh_CN/latest/topics/selectors.html#topics-selectors
"""

import scrapy
from scrapy.selector import Selector
try:
    from scrapy.spiders import Spider,CrawlSpider
except:
    from scrapy.spiders import BaseSpider as Spider,CrawlSpider
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor# as sle
from scrapy.selector import HtmlXPathSelector

import loongtian.util.webcrawler.spiderHelper as spiderHelper

# http网页代理列表的爬虫
from loongtian.util.webcrawler.items import KuaidailiItem,XroxyItem #,CnproxyItem

# 内容爬虫
from loongtian.util.webcrawler.items import GushiwenContentItem




class gushiwenSpider(Spider):
    """
    古诗文网的网络爬虫
    """
    name = 'gushiwen.org'
    allowed_domains = ['gushiwen.org']
    start_urls = ['http://so.gushiwen.org/view_1.aspx']
    # 定义爬取URL的规则
    # rules = [Rule(LinkExtractor(allow=['/view_\d+']), follow=True, callback='parse_content')]
    #         # http://so.gushiwen.org/author_
    #         # http://so.gushiwen.org/guwen/book_
    #          # Rule(LinkExtractor(allow=['/abc/\d+']), 'parse_torrent')]
    def parse(self, response):
        x = Selector(response)
        gushiwen = GushiwenContentItem()

        title= x.xpath("/html/body/div[3]/div[1]/div[1]/h1/text()").extract()
        title=spiderHelper.trimList(title)
        spiderHelper.checkResult("title",title)
        gushiwen['title'] =title

        dynasty=x.xpath("/html/body/div[3]/div[1]/div[2]/p[1]/text()").extract()
        dynasty=spiderHelper.trimList(dynasty)
        spiderHelper.checkResult("dynasty",dynasty)
        gushiwen['dynasty'] = dynasty

        #这里有两种情况：有作者或无作者。有作者时，将会有a标签，如果无，则直接取p[2]的文本
        author = x.xpath("/html/body/div[3]/div[1]/div[2]/p[2]/a/text()").extract()
        author=spiderHelper.trimList(author)
        if author is None:
            author = x.xpath("/html/body/div[3]/div[1]/div[2]/p[2]/text()").extract()
            author=spiderHelper.trimList(author)
            spiderHelper.checkResult("author",author)
        gushiwen['author'] = author

        content = x.xpath("/html/body/div[3]/div[1]/div[2]/text()").extract()
        content=spiderHelper.trimList(content)
        if content is None:
            content = x.xpath("/html/body/div[3]/div[1]/div[2]/p[4]/text()").extract()
            content=spiderHelper.trimList(content)
            spiderHelper.checkResult("content",content)
        gushiwen['content'] = content

        print( "----title----:%s" % title)
        print( "----dynasty----:%s" % dynasty)
        print( "----author----:%s" % author)
        print( "----content----:%s" % content)
        # print( "----content----:%s\r\n%s" % (content[4],content[5]))

        return gushiwen


class xicidailiProxySpider(Spider):
    name = "xicidaili"
    allowed_domains = ["xicidaili.com"]
    start_urls = [
        'http://www.xicidaili.com/'
    ]



class kuaidailiSpider(Spider):
    name = "kuaidaili"
    allowed_domains = ["kuaidaili.com"]
    start_urls = list()
    for i in range(1,11):
        start_urls.append('http://www.kuaidaili.com/proxylist/%d/' % i)
    # start_urls = [
    # 	'http://www.kuaidaili.com/proxylist/1/',
    # ]

    def parse(self, response):

        reses = response.xpath(".//table/tbody/tr")

        for res in reses:
            item = KuaidailiItem()
            item['ip'] = res.xpath("td[1]/text()").extract()[0].strip()
            item['port'] = res.xpath("td[2]/text()").extract()[0].strip()
            tp = res.xpath("td[4]/text()").extract()[0].strip()
            if 'https' in tp.lower():
                item['tp'] = u'https'
            else:
                item['tp'] = u'http'
            yield item

        # num = response.xpath(".//div[@id='listnav']/ul/li/a[@class='active']/text()").extract()[0]
        # Npage = int(num)
        # num = response.xpath(".//div[@id='listnav']/ul/li/a[@class='active']/text()").extract()[0]
        # Apage = int(num)/10

class xroxySpider(Spider):
    name = "xroxy"
    allowed_domains = ["xroxy.com"]
    baseurl = "http://www.xroxy.com/proxylist.php?port=&type=All_http&ssl=&country=&latency=&reliability=7500&sort=reliability&desc=true&pnum=0"
    Npage = 0
    Apage = 5
    start_urls = [
        baseurl+str(Npage)
    ]

    def parse(self, response):

        reses = response.xpath(".//*[@id='content']/table[1]/tr[@class='row1' or @class='row0']")

        for res in reses:
            item = XroxyItem()
            item['ip'] = res.xpath("td[2]/a/text()").extract()[0].strip()
            item['port'] = res.xpath("td[3]/a/text()").extract()[0].strip()
            item['tp'] = 'http'
            yield item

        num = response.xpath(".//*[@id='content']/table[2]/tr/td[1]/table/tr[1]/td/small/a/b/text()").extract()[0]
        self.Npage = int(num.replace('Page ','').strip())
        num = response.xpath(".//*[@id='content']/table[2]/tr/td[1]/table/tr[2]/td/small/b/text()").extract()[0]
        self.Apage = int(num)/10
        print ("************%d/%d**************" % (self.Npage,self.Apage))
        if self.Npage < self.Apage-1:
            yield scrapy.Request(self.baseurl+str(self.Npage+1), callback=self.parse)
        else:
            print ("[+] Seems like to finish:)")
            exit()

# class cnproxySpider(Spider):
#     name = "cnproxy"
#     allowed_domains = ["cn-proxy.com"]
#     start_urls = [
#         'http://cn-proxy.com/',
#         'http://cn-proxy.com/archives/218'
#     ]
#
#     def parse(self, response):
#
#         reses = response.xpath(".//table/tbody/tr")
#
#         for res in reses:
#             item = CnproxyItem()
#             item['tp'] = u'http'
#             item['ip'] = res.xpath("td[1]/text()").extract()[0].strip()
#             item['port'] = res.xpath("td[2]/text()").extract()[0].strip()
#
#             yield item



# class DmozSpider(Spider):
#     name = "dmoz"
#     allowed_domains = ["dmoz.org"]
#     start_urls = [
#         "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
#         "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
#     ]
#     def parse(self, response):
#         # # ------第一部分测试------
#         # filename = response.url.split("/")[-2] +".html"
#         # with open(filename, 'wb') as f:
#         #     f.write(response.body)
#
#         # # ------第二部分测试------
#         # hxs = HtmlXPathSelector(response)
#         # sites = hxs.select('//ul/li')
#         # for site in sites:
#         #     title = site.select('a/text()').extract()
#         #     link = site.select('a/@href').extract()
#         #     desc = site.select('text()').extract()
#         #     print title, link, desc
#
#         # ------第三部分测试------
#         hxs = HtmlXPathSelector(response)
#         sites = hxs.select('//ul/li')
#         items = []
#         for site in sites:
#            item = DmozItem()
#            item['title'] = site.select('a/text()').extract()
#            item['link'] = site.select('a/@href').extract()
#            item['desc'] = site.select('text()').extract()
#            items.append(item)
#         # print(items )
#         return items
#
# class MininovaSpider(CrawlSpider):
#     name = 'mininova.org'
#     allowed_domains = ['mininova.org']
#     start_urls = ['http://www.mininova.org/today']
#     rules = [Rule(LinkExtractor(allow=['/tor/\d+'])),
#              Rule(LinkExtractor(allow=['/abc/\d+']), 'parse_torrent')]
#     def parse_torrent(self, response):
#         x = HtmlXPathSelector(response)
#         torrent = TorrentItem()
#         torrent['url'] = response.url
#         torrent['name'] = x.select("//h1/text()").extract()
#         torrent['description'] = x.select("//div[@id='description']").extract()
#         torrent['size'] = x.select("//div[@id='info-left']/p[2]/text()[2]").extract()
#         return torrent





