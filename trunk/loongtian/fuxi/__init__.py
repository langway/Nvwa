#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Project:  loongtian/fuxi
Title:    __init__.py 
Author:   xujz 
DateTime: 2015/6/10 11:13 
UpdateLog:
1、xujz 2015/6/10 Create this File.
__init__.py
2、script 2015/11/23 update this File.
"""
from flask import Flask
from flask_mail import Mail
from loongtian.fuxi.conf import load_config

app = Flask(__name__)
_config = load_config() # ['running_state']['development']
app.config.from_object(_config)
# _config.init_app(app)

from flask import Blueprint
# 实例化 Blueprint 类，两个参数分别为蓝本的名字和蓝本所在包或模块，第二个通常填 __name__ 即可
main = Blueprint('main', __name__)

# 取得与女娲大脑通讯的控制台
from loongtian.nvwa.organs.console import HttpConsole
from loongtian.nvwa.settings import auth

console = HttpConsole(auth.adminUser.server_ip,auth.adminUser.server_port)

mail = Mail(app)
from loongtian.fuxi.mod import models
from loongtian.fuxi.templatetags import show_img
from loongtian.fuxi.templatetags import search_data
from loongtian.fuxi.utils import gateway
from loongtian.fuxi.utils import file
from loongtian.fuxi.vie import views, searchGateway,errors
from loongtian.fuxi.vie.users import views
from loongtian.fuxi.vie.register import views
import loongtian.fuxi.utils.captcha

