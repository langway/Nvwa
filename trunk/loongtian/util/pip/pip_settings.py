#!/usr/bin/env python
# coding: utf-8
"""
pip的参数类。
"""


# 是否使用douban等的国内镜像（默认为True）
useImageAddress=False


# pipy国内镜像
imageHosts= [
    ["pypi.douban.com ","http://pypi.douban.com/simple"],# 豆瓣
    ["pypi.mirrors.ustc.edu.cn","http://pypi.mirrors.ustc.edu.cn/simple"],# 中国科学技术大学
    ["mirrors.aliyun.com","http://mirrors.aliyun.com/pypi/simple/"], #  aliyun 的源
    ["e.pypi.python.org ","http://e.pypi.python.org"], # 另一个官网的源
]

# 特殊处理pywin32，numpy，安装Numpy+MKL，scipy，Twisted，lxml等组件
SpecialComponents=["pywin32",
                   "numpy",
                   "scipy",
                   "Twisted",
                   "lxml",
                   "SQLAlchemy",
                   "mysqlclient",
                   "seaborn",
                   "gensim",
                   # "PyQt5",
                   "tesseract-ocr",
                   # "TA-Lib",
    ]