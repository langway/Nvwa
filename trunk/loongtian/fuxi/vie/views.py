#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Project:  loongtian/fuxi
Author:   js
DateTime: 2015/6/10
"""
import json

import loongtian.util.helper.stringHelper as stringHelper
from loongtian.fuxi.utils.emailHelper import send_email
from loongtian.fuxi.utils.gateway import verifyValid

__author__ = 'js'

from flask import render_template, request, session, redirect, Response
from loongtian.fuxi import app
from loongtian.fuxi.mod.models import User, db, SearchRecord


@app.route('/')
@app.route('/index', methods=['GET'])
def index():
    """
    网站首页
    :return:首页html页面
    """
    try:
        mine = session['user']
    except:
        mine = None


    return render_template('index.html', mine=mine)


@app.route('/indexchat', methods=['GET', 'POST'])
def indexChat():
    """
    聊天模式首页页面
    :return:pattern 判断不同参数显示不同规格的页面， 值['small', 'id', 'max']
    """
    try:
        mine = session['user']
    except:
        mine = None
    pattern = 'small'
    keyword = ''  # 搜索关键词

    if mine:
        history_record = SearchRecord.query.filter_by(user=mine['id'], status=200).order_by('createtime')\
            .with_entities(SearchRecord.id, SearchRecord.result,
                           SearchRecord.search, SearchRecord.addtime).all()
    else:
        history_record = []


    if request.method == 'GET' and 'pattern' in request.args:
        if request.args['pattern'] in ['small', 'id', 'max']:
            pattern = request.args['pattern']
    if request.method == 'GET' and 'keyword' in request.args:
        keyword = request.args.get('keyword', '')

    return render_template('index_chat.html', pattern=pattern, mine=mine,
                           keyword=keyword, history_record=history_record)

@app.route('/pwd/find', methods=['GET', 'POST'])
def pwdFind():
    """
    忘记密码找回页面
    :return:返回页面
    """
    try:
        mine = session['user']
    except:
        mine = None
    if request.method == 'POST':
        usermail = request.form.get('usermail', '')
        verify = request.form.get('verify', '')
        mail_isMatch = stringHelper.mailValid(usermail)
        error_dic = {}
        if mail_isMatch == False:
            error_dic['error'] = u'邮箱格式不正确'
            user_mail = None
        else:
            user_mail = User.query.filter_by(email=usermail).first()
        if not user_mail and not error_dic:
            error_dic['error'] = u'邮箱不存在'
        if verify.__len__() != 0 and not error_dic:
            verify_ok = verifyValid(verify=verify)
            if verify_ok == False:
                error_dic['error'] = u'验证码不对'
        if not error_dic:
            session['mail'] = usermail
            error_dic['url'] = '/pwd/sendmail'
            valid_key_md5 = stringHelper.encodeStringMD5(stringHelper.Genjhm(6))   # 获取验证码发送到邮箱
            # ？？？此处需加入时间及用户信息做验证？？？
            session['valid_key'] = valid_key_md5
            valid_key = '%spwd/set?mail=%s&code=%s' % \
                        (request.host_url, usermail, valid_key_md5)
            send_email(usermail, '找回密码', 'pwd_email_verify', valid_key=valid_key)
        return Response(json.dumps([error_dic]))

    return render_template('pwd_find.html', mine=mine)

@app.route('/pwd/sendmail', methods=['GET', 'POST'])
def pwdSendMail():
    """
    忘记密码找回邮件发送成功页面
    :return:返回页面
    """
    try:
        mine = session['user']
    except:
        mine = None
    usermail = session['mail']
    try:
        mail_url = 'http://mail.%s' % usermail.split('@')[1]
    except:
        mail_url = ''
    if request.method == 'POST':
        pass

    return render_template('pwd_sendmail.html', mine=mine, usermail=usermail,
                           mail_url=mail_url)

@app.route('/pwd/set', methods=['GET', 'POST'])
def pwdSet():
    """
    忘记密码重新设置密码页面
    :return:返回页面
    """
    try:
        mine = session['user']
    except:
        mine = None
    usermail = session['mail']
    try:
        del session['mail']
    except:
        pass

    if request.method == 'GET':
        valid_code = request.args.get('code', '')
        try:
            valid_key_md5 = session['valid_key']
            del session['valid_key']
            # ？？？此处需调整根据验证码code设置时间过期？？？
        except Exception as e:
            valid_key_md5 = None
        if not valid_key_md5 or valid_code != valid_key_md5:
            return Response('您的链接已失效，请重新找回！')

    if request.method == 'POST':
        pwd = request.form.get('pwd', '')
        repeat = request.form.get('repeat', '')
        error_dic = {}
        if pwd !=repeat:
            error_dic['error'] = '重复密码不一致！'
        else:
            user = User.query.filter_by(email=usermail).first()
            user.password = stringHelper.encodeStringMD5(pwd)
            db.session.commit()
            error_dic['url'] = '/'
            session['user'] = {'id': user.id, 'name': user.username, 'email': user.email}

        return Response(json.dumps([error_dic]))

    return render_template('pwd_set.html', mine=mine, usermail=usermail)
