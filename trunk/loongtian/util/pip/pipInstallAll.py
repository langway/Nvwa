#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
安装列表中的所有组件
"""

__author__ = 'Leon'

import sys

import loongtian.util.pip.pipHelper as pipHelper

#python版本号及文件路径
pyVersion=sys.version
if pyVersion >= '3':
    PY3 = True
else:
    PY3 = False

# http://www.lfd.uci.edu/~gohlke/pythonlibs/ 这个地址非常重要！有大多数组件的下载！
# 如果pip安装出现错误，大部分可以到该网站下载对应的模块解决问题，如：scipy
COMPONENTS=[
    "pip",
    "pytz",

    "pywin32",

    # ——安装软件部分（一般省略）——
    "wheel",
    "setuptools",
    # ——开发环境部分——
    "ipython",
    "threadpool",
    "pytest",  # 测试

    # ——数据库部分——
    "psycopg2",  # （见support文件夹）
    "postgres",  # PostgreSQL数据库连接
    "dbutils",  # 数据库连接池
    "redis",  # redis数据库连接
    "SQLAlchemy",
    "mysqlclient",
    "pymongo", # MongoDB的数据库连接

    "lxml",
    "simplejson",
    "jsonplus",

    # ——科学计算计算部分——
    "numpy",  #
    "scipy", # （见support文件夹）主要是一些科学工具集，信号处理工具集（如线性代数使用LAPACK库，快速傅立叶变换使用FFTPACK库）及数值计算的一些工具（常微分方程求解使用ODEPACK库，非线性方程组求解以及最小值求解等）
    "matplotlib",  # 是一个画图工具，和Matlab中的画图工程类似，作数据可视化。
    "seaborn", # 用于美化matplotlib图表
    "networkx",
    "pandas", # 处理结构化的表格数据
    "nose",
    "atlas",
    # "Lapack",
    # "theano",
    "sklearn",
    # 机器学习模块。scikit-learn：里面有很多机器学习相关的算法（如聚类算法，SVM等）。sklearn（Google公司开始投资，是大数据战略的一个步骤）可以用于模式识别，用在一般知识发现，例如户外参与人口的类型，sklearn包自己带了两个数据集，其中一个是鸢尾花数据库（iris，鸢尾花）
    # 安装后可用nosetests -v sklearn来进行测试

    # ——自然语言处理组件部分——
    "jieba",  # 结巴分词
    # "word2vec",  # 不再使用，直接使用gensim
    "nltk",
    "gensim",# Word2Vec的Python实现。
    # 参考：中英文维基百科语料上的Word2Vec实验 | 我爱自然语言处理
    # http://www.52nlp.cn/%e4%b8%ad%e8%8b%b1%e6%96%87%e7%bb%b4%e5%9f%ba%e7%99%be%e7%a7%91%e8%af%ad%e6%96%99%e4%b8%8a%e7%9a%84word2vec%e5%ae%9e%e9%aa%8c

    # "dateutil",
    "requests",

    "beautifulsoup4",


    # ——深度学习部分——
    # "tensorflow", # tensorflow 注意版本更新，目前只能支持3.5以上版本
    # "Keras",# 易用的深度学习框架
    # "pybrain",
    # "pygame",Pygame需单独安装文件，下载地址：http://www.pygame.org/download.shtml.
    # 请参照:用Python和Pygame写游戏-从入门到精通（1） | 目光博客
    # http://eyehere.net/2011/python-pygame-novice-professional-1/

    # ——语音处理部分——
    "Speech",  # Python3.5环境安装及使用 Speech问题解决 - xhz1234的专栏 - 博客频道 - CSDN.NET
    # http://blog.csdn.net/xhz1234/article/details/49386399
    # 百度语音识别API的使用样例（python实现） - 六个九十度 - 博客频道 - CSDN.NET
    # http://blog.csdn.net/happen23/article/details/45821697

    # 百度语音API使用（python实现之二） - 六个九十度 - 博客频道 - CSDN.NET
    # http://blog.csdn.net/happen23/article/details/45866783
    # ——其他组件部分——
    "apscheduler",  # 计划调度
    # "PySide",  # 图像界面开发(目前不支持python3.5)
    # "Twisted",#scrapy需要组件
    "scrapy",  # 网络爬虫，要首先安装lxml（见support文件夹），参见：Index of Packages : Python Package Index
    # https://pypi.python.org/pypi/lxml
    # 需要安装pywin32（见support文件夹），参见Python for Windows Extensions - Browse /pywin32 at SourceForge.net
    # https://sourceforge.net/projects/pywin32/files/pywin32/

    # ——网络扩展部分——
    "flask",  #
    "flask_mail",  #
    "flask-script", # 可以自定义命令行命令，用来启动程序或其它任务
    "Flask-SQLAlchemy",  #flask-sqlalchemy  用来管理数据库的工具，支持多种数据库后台
    "flask-migrate", # 数据库迁移工具，该工具命令集成到 flask-script 中，方便在命令行中进行操作。
    "Flask-MySQLdb",  #
    "flask_paginate",
    "tweepy",# for Twitter support.
    # Flask 常用库详情
    # flask-script
    # 为Flask提供强大的命令行操作，与Django shell类似。
    #
    # flask-login
    # Flask user session 管理，提供诸如login_user, logout_user, login_required, current_user等功能，也是其他很多Flask库的基础。
    #
    # flask-admin
    # 为Flask应用提供操作简单且易于扩展的数据库管理界面，与Django自带的数据库管理app类似。
    #
    # Flask-WTF
    # Flask与WTForms的集成，提供强大的Form安全和校验机制，与Django内置的Form功能类似。
    #
    # flask-principal
    # Flask强大的权限管理机制，灵活性强，提供了一个权限管理的基础框架，是很多Flask权限相关扩展的基础。
    #
    # flask-restful
    # 一个强大的Flask RESTful框架，简单好用。
    #
    # flask-api
    # 相当于Django REST Framework的Flask版，是另一个强大的Flask RESTful框架。
    #
    # Flask-Mail
    # Flask-Mail 为Flask应用添加了SMTP 邮件发送功能
    #
    # Flask-User
    # Flask-User集成了用户管理相关功能，并允许对功能做定制性修改，其相关功能包括Register, Confirm email, Login, Change username, Change password, Forgot password等。
    #
    # Flask-User 基于Flask-SQLAlchemy，NoSQL数据库无法使用。
    #
    # flask-security
    # Flask-Security让开发者能够很快的为应用添加常用的安全机制，其整合了Flask-Login, Flask-Mail, Flask-Principal, Flask-Script等应用。其安全机制包括：
    #
    # Session based authentication
    # Role management
    # Password encryption
    # Basic HTTP authentication
    # Token based authentication
    # Token based account activation (optional)
    # Token based password recovery / resetting (optional)
    # User registration (optional)
    # Login tracking (optional)
    # JSON/Ajax Support
    # flask-babel
    # Flask国际化和本地化扩展，基于Babel
    #
    # flask-locale
    # 为Flask应用添加语言包，与flask-babel类似。

    "itchat", # itchat 是 A complete and graceful API for Wechat . 微信个人号接口、微信机器人及命令行微信，三十行即可自定义个人号机器人。了解更多使用方法，可以阅读使用
    "Pillow", # Python图像处理库:Pillow
    # "tesseract-ocr", # Tesseract OCR  下载地址：Home · UB-Mannheim/tesseract Wiki · GitHub https://github.com/UB-Mannheim/tesseract/wiki
    #                     # 1、下载Tesseract-OCR引擎，注意要3.0以上才支持中文哦，按照提示安装就行。
    #                     # 2、设置环境变量path：d:\Program Files (x86)\Tesseract-OCR
    #                     # 下载chi_sim.traindata字库。要有这个才能识别中文。下好后，放到Tesseract-OCR项目的tessdata文件夹里面。
    #                     # 3、下载jTessBoxEditor，这个是用来训练字库的。
    "psutil", # psutil是一个跨平台库（http://code.google.com/p/psutil/），能够轻松实现获取系统运行的进程和系统利用率（包括CPU、内存、磁盘、网络等）信息。它主要应用于系统监控，分析和限制系统资源及进程的管理。
    "websocket",


    # 界面部分
    "PyQt5",
    "qdarkstyle", # QDarkStyleSheet（非常漂亮的PyQt黑色主题）

    "msgpack-python", #MessagePack是一个基于二进制高效的对象序列化Library用于跨语言通信。
                        #它可以像JSON那样，在许多种语言之间交换结构对象；但是它比JSON更快速也更轻巧。


    "treelib",
    "SocketServer",

]



AUTO_TRADE_COMPONENTS=[ # 自动化交易所需要的特定资源
    "pytesseract",
    "pymongo",
    "tushare",
    "TA-Lib",
    # talib比较小众，但是做量化的应该都知道，本人在安装这个库时，遇到了一些问题，网上的方法散乱而且没能完全解决，这篇博客记录了我的安装过程，希望对有需要的同学提供帮助。
    #
    # 1.执行pip install TA-Lib
    # 如果以前没有安装过vc，或者编译工具没在path下面，应该会遇到这个错误 error: Microsoft Visual C++ 9.0 is required. Get it from http://aka.ms/vcpython27
    # 这个错误提示非常友好，我们按照链接下载安装编译工具就好了
    #
    # 2.安装Microsoft Visual C++ Compiler for Python 2.7，然后继续执行pip install TA-Lib
    # 很不幸，你应该还是会遇到错误talib/common.c(240) : fatal error C1083: Cannot open include file: 'ta_libc.h': No such file or directory
    # 这个错误是因为TA-Lib的python库需要先安装ta-lib，也就是TA-Lib实际是对ta-lib的一层python包装
    #
    # 3.下载ta-lib，解压到C:\ta-lib
    # 这时候，我们继续执行pip install TA-Lib，很可能你就安装成功了。但如果你是64位的系统，可能还是会遇到问题
    # common.obj : error LNK2019: unresolved external symbol TA_Initialize referenced in function __pyx_pf_5talib_6common_2_ta_initialize
    # 这个问题有点高级，看起来说是链接错误，很多人到这就不知道怎么办了，网上也没有很好的办法。这个问题的来由是，我们下载的ta-lib除了头文件外，还有编译好的库，但是这个库是32位系统编译好的，所以我们需要在64位系统下面重新编译它。还好，我们下载的ta-lib就包含了源码，而编译工具就是之前安装的Microsoft Visual C++ Compiler for Python 2.7。
    #
    # 4.打开【开始菜单】》【Microsoft Visual C++ Compiler Package for Python 2.7】》【Visual C++ 2008 64-bit Command Prompt】，然后在控制台里面进入到目录C:\ta-lib\c\make\cdr\win32\msvc。执行nmake，一段时间后，新的64位库就编译好了
    #
    # 5.此时，再次执行pip install TA-Lib。我们终于看到安装成功了。
    # "ws4py" # for Bitstamp support.
    # "tornado", # for Bitstamp support.
]

if __name__ == '__main__':
    # 安装所有components列表中定义的python组件。
    pipHelper.installAll(COMPONENTS)

    # pipHelper.installAll(AUTO_TRADE_COMPONENTS)

# python27、python35配置：
# 1、环境变量Path:C:\Python\Python35\Scripts\;C:\Python\Python35\;C:\Python27\Scripts\;C:\Python27\;
# 2、以某一版本为默认值，修改另一版本的python.exe为python[版本号].exe，例如：python2.exe

# 如果安装时报错，error: Microsoft Visual C++ 9.0 is required (Unable to find vcvarsall.bat)，下载地址：
# http://aka.ms/vcpython27
# 实际下载地址：
# http://www.microsoft.com/en-us/download/details.aspx?id=44266

# ---------------postgre安装错误或运行时报错的处理办法---------------------------
# 一、psycopg2 ImportError: DLL load failed
# from psycopg2._psycopg import BINARY, NUMBER, STRING, DATETIME
# ImportError: DLL load failed
# 这个错误
# 1. 使用了mingw32作为编译器
# 2. 然后这个_psycopg.pyd 老是加载不成功.
# 3. 有资料说是libpg.dll的版本和本机的postgresql不匹配, 或者说libpg.dll 不在windows的Path路径里
# 反正没解决, 最后在stackoverflow上找到答案, 安装一个别人编译好的windows版本, 地址在: http://www.stickpeople.com/projects/python/win-psycopg/
# 选择自己的python和postgresql对应的版本即可。

# ---------------scipy安装错误或运行时报错的处理办法---------------------------
# 到网站Python Extension Packages for Windows - Christoph Gohlke
# http://www.lfd.uci.edu/~gohlke/pythonlibs/ 下载对应的scipy版本（根据python版本及win版本），使用pip install [下载目录]即可安装。
# 注意：下载目录不能有空格!
#        http://www.lfd.uci.edu/~gohlke/pythonlibs/ 这个地址非常重要！有大多数组件的下载！
# 如果pip下载不了，请登陆上面网址，手动下载！！！