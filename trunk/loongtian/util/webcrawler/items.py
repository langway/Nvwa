#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy



class GushiwenContentItem(scrapy.Item):
    """
    古诗文网-内容
    """
    # define the fields for your item here like:
    title = scrapy.Field() # 名称
    dynasty = scrapy.Field() # 朝代
    author = scrapy.Field() # 作者
    content = scrapy.Field() # 原文
    translation = scrapy .Field () # 翻译（列表）
    appreciation=scrapy.Field() # 赏析（列表）

    pass

class CnproxyItem(scrapy.Item):
    # define the fields for your item here like:
    tp = scrapy.Field()
    ip = scrapy.Field()
    port = scrapy.Field()


class KuaidailiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    tp = scrapy.Field()
    ip = scrapy.Field()
    port = scrapy.Field()


class XroxyItem(scrapy.Item):
    # define the fields for your item here like:
    ip = scrapy.Field()
    port = scrapy.Field()
    tp = scrapy.Field()

# class DmozItem(scrapy.Item):
#     # define the fields for your item here like:
#     title = scrapy.Field()
#     link = scrapy.Field()
#     desc = scrapy.Field()
#     pass
#
#
# class TorrentItem(scrapy.Item):
#     url = scrapy.Field()
#     name = scrapy.Field()
#     description = scrapy.Field()
#     size = scrapy.Field()
