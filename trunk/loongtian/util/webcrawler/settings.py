#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Administrator'

# 要防止scrapy被ban，主要有以下几个策略。
#
# 动态设置user agent
# 禁用cookies
# 设置延迟下载
# 使用Google cache
# 使用IP地址池（Tor project、VPN和代理IP）
# 使用Crawlera

# ****************************
# **     参考文献：         **
# ****************************
# 通用爬虫(Broad Crawls) — Scrapy 0.24.1 文档
# http://scrapy-chs.readthedocs.org/zh_CN/latest/topics/broad-crawls.html

# Scrapy settings for webcrawler project
#
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'webcrawler'

SPIDER_MODULES = ['spiders']
NEWSPIDER_MODULE = 'spiders'

# 用户代理
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'webcrawler (+http://www.yourdomain.com)'
USER_AGENTS = [
# "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
# "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
# "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
# "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
# "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
# "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
# "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
# "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
# "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
# "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
# "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
# "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
# "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
# "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
# "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
# "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
# "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.8.1000 Chrome/30.0.1599.101 Safari/537.36",
# "Mozilla/5.0 (windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
# "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
# "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
# "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
# "Mozilla/5.0 (windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
# "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
# "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
# "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
# "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
# "Mozilla/5.0 (X11; linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
# "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
# "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
# "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
# "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
# "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
# "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
# "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
# "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
# "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
# "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
# "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
# "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
# "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
# "Mozilla/5.0 (X11; linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
# "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
# "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
# "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
# "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
# "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
# "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
# "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
# "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
# "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
# "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
# "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
# "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
# "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
# "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
# "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
# "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
# "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
# "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
# "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
# "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
# "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
# "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
# "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
# "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
# "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
# "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
# "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
# "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
# "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
# "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",

]

USER_AGENTS_LIST_FILE = './resources/useragentlist.txt'


# Configure maximum concurrent requests performed by Scrapy (default: 16)
# 增加全局并发数:
# Scrapy默认的全局并发限制对同时爬取大量网站的情况并不适用，因此您需要增加这个值。
# 增加多少取决于您的爬虫能占用多少CPU。 一般开始可以设置为 100 。
# 不过最好的方式是做一些测试，获得Scrapy进程占取CPU与并发数的关系。
# 为了优化性能，您应该选择一个能使CPU占用率在80%-90%的并发数。
CONCURRENT_REQUESTS=100

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# 设置下载延迟
DOWNLOAD_DELAY=3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN=16
#CONCURRENT_REQUESTS_PER_IP=16

# 禁用cookies
# Disable cookies (enabled by default)
# 除非您 真的 需要，否则请禁止cookies。
# 在进行通用爬取时cookies并不需要， (搜索引擎则忽略cookies)。
# 禁止cookies能减少CPU使用率及Scrapy爬虫在内存中记录的踪迹，提高性能。
COOKIES_ENABLED=False

# 给定重试的次数（如果指定代理，有可能是由于代理打开失败导致的页面下载问题，需要给定重试次数）
# Retry many times since proxies often fail
RETRY_TIMES = 10

# Retry on most error codes since proxies fail for different reasons
RETRY_HTTP_CODES = [ 500 , 503 , 504 , 400 , 403 , 404 , 408 ]

# # 禁止重试
# # 对失败的HTTP请求进行重试会减慢爬取的效率，尤其是当站点响应很慢(甚至失败)时，
# # 访问这样的站点会造成超时并重试多次。这是不必要的，同时也占用了爬虫爬取其他站点的能力。
# RETRY_ENABLED = False

# 减小下载超时:
# 如果您对一个非常慢的连接进行爬取(一般对通用爬虫来说并不重要)，
# 减小下载超时能让卡住的连接能被快速的放弃并解放处理其他站点的能力。
DOWNLOAD_TIMEOUT = 15


# 关闭重定向:
# 除非您对跟进重定向感兴趣，否则请考虑关闭重定向。
# 当进行通用爬取时，一般的做法是保存重定向的地址，并在之后的爬取进行解析。
# 这保证了每批爬取的request数目在一定的数量， 否则重定向循环可能会导致爬虫在某个站点耗费过多资源。
REDIRECT_ENABLED = False

# 添加http代理IP设置PROXIES(词典,这样做是为了去重非常方便)
# 格式为：ip_port:user_pass
# Proxy list containing entries like:
# http://host1:port
# http://username:password@host2:port
# http://host3:port
PROXIES = {
    # 'http://111.11.228.75:80': '',
    # 'http://120.198.243.22:80': '',
    # 'http://111.8.60.9:8123': '',
    # 'http://101.71.27.120:80': '',
    # 'http://122.96.59.104:80': '',
    # 'http://122.224.249.122:8088': '',
}
PROXY_LIST_FILE = './resources/proxylist.txt'

# 设置Log级别
# 当进行通用爬取时，一般您所注意的仅仅是爬取的速率以及遇到的错误。
# Scrapy使用 INFO log级别来报告这些信息。
# 为了减少CPU使用率(及记录log存储的要求), 在生产环境中进行通用爬取时您不应该使用 DEBUG log级别。
# 不过在开发的时候使用 DEBUG 应该还能接受。
LOG_LEVEL = 'INFO'

# # 有些站点(基于2013年的经验数据，之多有1%)声明其为 ajax crawlable 。
# # 这意味着该网站提供了原本只有ajax获取到的数据的纯HTML版本。
# # 网站通过两种方法声明:
# # 1、在url中使用 #! - 这是默认的方式;
# # 2、使用特殊的meta标签 - 这在”main”, “index” 页面中使用。
# # Scrapy自动解决(1)；解决(2)您需要启用 AjaxCrawlMiddleware 参考:http://scrapy-chs.readthedocs.org/zh_CN/latest/topics/downloader-middleware.html#ajaxcrawl-middleware
# # 通用爬取经常抓取大量的 “index” 页面； AjaxCrawlMiddleware能帮助您正确地爬取。
# # 由于有些性能问题，且对于特定爬虫没有什么意义，该中间件默认关闭。
# AJAXCRAWL_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED=False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'webcrawler.middlewares.MyCustomSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html

# from scrapy.contrib.downloadermiddleware.httpproxy import  HttpProxyMiddleware
# from loongtian.util.webcrawler .middlewares import  ProxyMiddleware

DOWNLOADER_MIDDLEWARES = {
        'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware' : 90 ,
        'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 100,
        'loongtian.util.webcrawler.middlewares.ProxyMiddleware': 110,
        'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware' : None,#取消默认的useragent,使用新的useragent
        'loongtian.util.webcrawler.middlewares.RandomUserAgentMiddleware' :400
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
# The integer values you assign to classes in this setting determine the order in which they start:
# items go through from lower valued to higher valued classes.
# It’s customary to define these numbers in the 0-1000 range.
ITEM_PIPELINES = {
   'loongtian.util.webcrawler.pipelines.CnproxyPipeline': 100,
   'loongtian.util.webcrawler.pipelines.XroxyPipeline':200,
   'loongtian.util.webcrawler.pipelines.KuaidailiPipeline':300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# NOTE: AutoThrottle will honour the standard settings for concurrency and delay
#AUTOTHROTTLE_ENABLED=True
# The initial download delay
#AUTOTHROTTLE_START_DELAY=5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY=60
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG=False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED=True
#HTTPCACHE_EXPIRATION_SECS=0
#HTTPCACHE_DIR='httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES=[]
#HTTPCACHE_STORAGE='scrapy.extensions.httpcache.FilesystemCacheStorage'
