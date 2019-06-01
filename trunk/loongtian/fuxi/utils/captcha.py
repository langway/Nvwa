#!/usr/bin/env python
# coding: utf-8
"""
Project:  loongtian/fuxi
Title:    captcha 
Author:   xujz 
DateTime: 2015/6/10 9:50 
UpdateLog:
1、xujz 2015/6/10 Create this File.
captcha
"""
__author__ = 'xujz'


from io import StringIO
from loongtian.util.helper import captcha
from flask import session
from loongtian.fuxi import app

@app.route('/captcha')
def get_code():
    #把strs发给前端,或者在后台使用session保存
    code_img, strs = captcha.create_validate_code()
    session['captcha'] = strs
    buf = StringIO.StringIO()
    code_img.save(buf,'JPEG', quality=70)
    buf_str = buf.getvalue()
    response = app.make_response(buf_str)
    response.headers['Content-Type'] = 'image/jpeg'

    return response


