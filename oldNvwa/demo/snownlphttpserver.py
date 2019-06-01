#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    snownlphttpserver 
Author:   fengyh 
DateTime: 2014/9/30 14:40 
UpdateLog:
1、fengyh 2014/9/30 Create this File.


"""

import tornado.ioloop
import tornado.web
from snownlp import SnowNLP
import json

class MainHandler(tornado.web.RequestHandler):
