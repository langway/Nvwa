#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Project:  loongtian/fuxi
Author:   js
DateTime: 2015/6/10
"""
import json
try:
    from flask.ext.paginate import Pagination
except:
    from flask_paginate import Pagination

import loongtian.util.helper.stringHelper as stringHelper
from loongtian.fuxi.mod.models import User, db, UsersSms, SearchRecord
from loongtian.fuxi.utils.email import send_email


__author__ = 'js'

from flask import render_template, request, redirect, session, Response
from loongtian.fuxi import app


@app.route('/user/info', methods=['GET', 'POST'])
def userInfo():
    try:
        mine = session['user']
        user = User.query.get(mine['id'])
    except:
        return redirect('/')
    if request.method == 'POST' and 'username' in request.form:
        username = request.form.get('username', '')
        if username.__len__() > 0:
            user.username = username
            db.session.commit()
            errorDict = {'url': '/'}
            return Response(json.dumps([errorDict]))
        else:
            errorDict = {'error': '昵称不能为空！'}
            return Response(json.dumps([errorDict]))

    if request.method == 'POST' and 'email' in request.form:
        email = request.form.get('email', '')
        mail_v = stringHelper.mailValid(email)
        if mail_v:
            usersMail = User.query.filter_by(email = email).first()
            if usersMail:
                errorDict = {'error': '邮箱已存在！'}
                return Response(json.dumps([errorDict]))
            else:
                active_m = stringHelper.Genjhm(6)   # 获取验证码发送到邮箱
                session['active_m'] = active_m
                session['email_new'] = email
                # 注册成功发送激活码邮件
                send_email(email, '账户激活码', 'email_verify', valid_key=active_m)
                errorDict = {'mess': '激活码已发送至邮箱！'}
                return Response(json.dumps([errorDict]))

        else:
            errorDict = {'error': '邮箱格式不正确！'}
            return Response(json.dumps([errorDict]))

    if request.method == 'POST' and 'active_m' in request.form:
        mail_n = request.form.get('mail_n', '')
        active_m = request.form.get('active_m', '')
        if mail_n == session['email_new'] and active_m == session['active_m']:
            user.email = mail_n
            db.session.commit()
            del session['email_new']
            del session['active_m']
            errorDict = {'url': '/'}
            return Response(json.dumps([errorDict]))
        else:
            errorDict = {'error': '激活码不正确！'}
            return Response(json.dumps([errorDict]))

    if request.method == 'POST' and 'phone' in request.form:
        phone = request.form.get('phone', '')
        phone_v = stringHelper.phoneValid(phone)
        if phone_v:
            usersPhone = User.query.filter_by(phone=phone).first()
            if usersPhone:
                errorDict = {'error': '手机已存在！'}
                return Response(json.dumps([errorDict]))
            else:
                active_p = stringHelper.Genjhm(6)   # 获取验证码发送到手机
                session['active_p'] = active_p
                session['phone_new'] = phone
                # 注册成功发送激活码邮件
                errorDict = {'mess': '激活码已发送至手机！测试用：%s'%active_p}
                return Response(json.dumps([errorDict]))

        else:
            errorDict = {'error': '手机格式不正确！'}
            return Response(json.dumps([errorDict]))

    if request.method == 'POST' and 'active_p' in request.form:
        phone_n = request.form.get('phone_n', '')
        active_p = request.form.get('active_p', '')
        if phone_n == session['phone_new'] and active_p == session['active_p']:
            user.phone = phone_n
            db.session.commit()
            del session['phone_new']
            del session['active_p']
            errorDict = {'url': '/'}
            return Response(json.dumps([errorDict]))
        else:
            errorDict = {'error': '激活码不正确！'}
            return Response(json.dumps([errorDict]))


    return render_template('user_info.html', mine=mine, user=user)

@app.route('/user/search', methods=['GET', 'POST'])
def userSearch():
    try:
        mine = session['user']
    except:
        return redirect('/')

    q = request.args.get('q', None)
    search = False
    if q:
        search = True
    try:
        page = int(request.args.get('page', 1))
    except ValueError:
        page = 1
    start_num = (page-1)*3
    end_num = start_num+3

    history_record = SearchRecord.query.filter_by(user=mine['id'], status=200)\
        .with_entities(SearchRecord.id, SearchRecord.search, SearchRecord.addtime).all()
    pagination = Pagination(page=page, total=history_record.__len__(),
                            search=search, record_name='searchRecord',
                            per_page=3)
    historyRecordItems = history_record[start_num:end_num]


    return render_template('user_search.html', mine=mine,
                           historyRecord=historyRecordItems, pagination=pagination)

@app.route('/user/photo', methods=['GET', 'POST'])
def userPhoto():
    try:
        mine = session['user']
        user = User.query.get(mine['id'])
    except:
        return redirect('/')
    if request.method == 'POST':
        imgUrl = request.form.get('imgUrl', '')
        try:
            user.photo = imgUrl.split('/')[-1]
            db.session.commit()
            session['user']['photo'] = user.photo
            errorDict = {'url': '/'}
            return Response(json.dumps([errorDict]))
        except:
            errorDict = {'error': '服务器忙，请稍后再试！'}
            return Response(json.dumps([errorDict]))

    return render_template('user_photo.html', mine=mine)

@app.route('/user/message', methods=['GET', 'POST'])
def userMessage():
    try:
        mine = session['user']
    except:
        return redirect('/')

    q = request.args.get('q', None)
    search = False
    if q:
        search = True
    try:
        page = int(request.args.get('page', 1))
    except ValueError:
        page = 1
    start_num = (page-1)*3
    end_num = start_num+3

    usersSms = UsersSms.query.filter_by(receive=mine['id'], status=200).\
                with_entities(UsersSms.id, UsersSms.title,
                              UsersSms.content, UsersSms.addtime).all()
    pagination = Pagination(page=page, total=usersSms.__len__(),
                            search=search, record_name='usersSms',
                            per_page=3)
    usersSmsItems = usersSms[start_num:end_num]

    return render_template('user_message.html', mine=mine,
                           usersSms=usersSmsItems, pagination=pagination)

@app.route('/user/message/detail', methods=['GET', 'POST'])
def userMessageDetail():
    try:
        mine = session['user']
    except:
        return redirect('/')

    m_id = request.args.get('m_id', None)

    usersSmsDetail = UsersSms.query.get(m_id)

    return render_template('user_message_detail.html', mine=mine,
                           usersSmsDetail=usersSmsDetail)

@app.route('/user/safety', methods=['GET', 'POST'])
def userSafety():
    try:
        mine = session['user']
        user = User.query.get(mine['id'])
    except:
        return redirect('/')

    if request.method == 'POST':
        pwd_old = request.form.get('pwd_old', '')
        pwd_new = request.form.get('pwd_new', '')
        pwd_repeat = request.form.get('pwd_repeat', '')
        pwd_old = stringHelper.encodeStringMD5(pwd_old)
        if pwd_old == user.password:
            if pwd_new.__len__() < 6 or pwd_new.__len__() > 16:
                errorDict = {'error': '密码长度在6-16个字符！'}
                return Response(json.dumps([errorDict]))
            elif pwd_new != pwd_repeat:
                errorDict = {'error': '重复密码不正确！'}
                return Response(json.dumps([errorDict]))
            user.password = stringHelper.encodeStringMD5(pwd_new)
            db.session.commit()
            errorDict = {'url': '/'}
            return Response(json.dumps([errorDict]))
        else:
            errorDict = {'error': '原密码不正确！'}
            return Response(json.dumps([errorDict]))

    return render_template('user_safety.html', mine=mine)
