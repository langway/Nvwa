#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Project:  loongtian/fuxi
Title:    conf\__init__.py 
Author:   script
DateTime: 2015/11/23
"""

import os
from loongtian.fuxi.conf import config

def load_config():
    """
    加载配置类
    Author: js
    DateTime: 2016/11/23
    :return: conf.py 配置文件
    """
    # mode = os.environ.get('MODE')

    return config