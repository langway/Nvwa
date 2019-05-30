#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Project:  loongtian/fuxi
Author:   js
DateTime: 2015/6/10
"""

import json
import loongtian.util.helper.stringHelper as stringHelper

from loongtian.fuxi.mod.models import User, Locations
from loongtian.fuxi.utils.email import send_email
from loongtian.fuxi.utils.gateway import register_valid

__author__ = 'js'

from flask import render_template, request, session, Response, redirect
from loongtian.fuxi import app
from loongtian.fuxi.mod.models import db


@app.route('/register', methods=['GET', 'POST'])
def register():
    try:
        mine = session['user']
        return redirect('/')
    except:
        mine = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        repeat = request.form['repeat']
        verify = request.form['verify']
        isValid = register_valid(username, password, repeat, verify)
        if isValid == True:
            password = stringHelper.encodeStringMD5(password)
            user = User(username=username, email=username, password=password, status=206)
            db.session.add(user)
            db.session.commit()

            valid_key = stringHelper.Genjhm(6)   # 获取验证码发送到邮箱
            session['valid_key'] = valid_key
            session['user'] = {'id': user.id, 'name': user.username, 'email': user.email}

            # 注册成功发送激活码邮件
            send_email(user.email, '账户激活码', 'email_verify', valid_key=valid_key)

            isValid = {'url': '/register/verify/mail'}
        return Response(json.dumps([isValid]))

    return render_template('register.html', mine=mine)

@app.route('/register/verify/mail', methods=['GET', 'POST'])
def registerVerifyMail():
    try:
        mine = session['user']
    except:
        mine = None
    if request.method == 'POST':
        validKey = request.form['verify']
        sessionValidKey = session['valid_key']
        if sessionValidKey == validKey:
            User.query.filter_by(id=mine['id']).update({User.status: 200})
            db.session.commit()
            dictBackData = {'url': '/register/finish'}
            return Response(json.dumps([dictBackData]))
        else:
            dictBackData = {'error': '验证码不正确！'}
            return Response(json.dumps([dictBackData]))

    return render_template('register_verify_mail.html', mine=mine)

@app.route('/register/verify/phone')
def registerVerifyPhone():

    return render_template('register_verify_phone.html')

@app.route('/register/finish', methods=['GET', 'POST'])
def registerFinish():
    try:
        mine = session['user']
        user = User.query.get(mine['id'])
    except:
        mine = None
    if request.method == 'POST':
        username = request.form['username']
        gender = request.form['gender']
        location = request.form['location']
        if username.__len__() > 0:
            userExist = User.query.filter(User.id!=mine['id']).filter_by(username=username).first()
            if userExist:
                dictBackData = {'error': '用户名已存在！'}
                return Response(json.dumps([dictBackData]))
            user.username = username
        if location.__len__() > 0:
            user.location = location
        user.gender = gender

        db.session.commit()
        return Response('/')

    return render_template('register_finish.html', mine=mine)