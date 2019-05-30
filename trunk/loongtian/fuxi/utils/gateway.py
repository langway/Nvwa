#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Project:  loongtian/fuxi
Author:   js
DateTime: 2015/12/2
"""
import hashlib
import json
import random
import re
import datetime
from sqlalchemy import or_
import loongtian.util.helper.stringHelper as stringHelper
from loongtian.fuxi import app
from loongtian.fuxi.conf.config import PERMANENT_SESSION_LIFETIME_USER
from loongtian.fuxi.mod.models import User, Locations, db
from flask import request, session, render_template, redirect, Response

__author__ = 'js'

# def tmp_render(fn):
#     """
#     描述：用户登录信息装饰器
#     """
#     def tmp_render_init(*args):
#         try:
#             mine = session['user']
#             user = User.query.get(id=mine['id'])
#         except Exception as e:
#             mine = None
#             user = None
#         return fn(*args)
#     return tmp_render_init


def getIpAddress():
    """
    描述 : 获取当前用户的IP地址
    :return:ip字符串；
    """
    try:
        ip = request.META['HTTP_X_FORWARDED_FOR'].split(",")[0]
    except:
        try:
            ip = request.META['REMOTE_ADDR']
        except:
            ip = '0.0.0.0'
    return ip

def verifyValid(verify):
    """
    验证码比对
    """
    captcha = session['captcha']#系统验证码
    #不区分大小写
    if captcha.lower() == verify.lower():
        return True
    else:
        return False

def register_valid(username, password, repeat, verify):
    """
    注册信息验证
    :return:错误信息
    error = [{'username':'邮箱不能为空','pwd':'密码不能为空','verify':'验证码错误'}]
    """
    error_dic = {}
    regtype = '1'   # 判断手机或邮箱注册，1为邮箱，2为手机
    if regtype == '1':
        mail_isMatch = stringHelper.mailValid(username)
        if mail_isMatch == False:
            error_dic['error'] = u'邮箱格式不正确'
            return error_dic
        user_mail = User.query.filter_by(email=username).first()
        if user_mail:
            error_dic['error'] = u'邮箱已存在'
            if user_mail.status == 206:
                error_dic['error'] = u'邮箱已存在, 请激活！'
            return error_dic
    # elif regtype == '2':
    #     if len(mail) != 11:
    #         error_dic['mail'] = u'手机号长度错误'
    #     user_mail = User.objects.filter(mobile=mail, status=200)
    #     if user_mail.__len__() > 0:
    #         error_dic['mail'] = u'手机号已存在'

    if password.__len__() < 6 or password.__len__() > 16:
        error_dic['error'] = u'密码长度在6-16位'
        return error_dic
    if repeat != password:
        error_dic['error'] = u'密码不一致'
        return error_dic
    if verify.__len__() != 0:
        verify_ok = verifyValid(verify=verify)
        if verify_ok == False:
            error_dic['error'] = u'验证码不对'
            return error_dic

    if error_dic.__len__() != 0:
        return error_dic
    else:
        return True

# def test_ip(request):
#     """
#     时间：2015-04-10
#     描述：排除注册机ip号段
#     """
#     result = False
#     ip = getIpAddress(request).split('.')
#     if ip[0] != 115:
#         result = True
#     else:
#         if ip[1] != 239:
#             result = True
#         else:
#             if ip[2] != 212:
#                 result = True
#
#     return result

@app.route('/login', methods=['POST'])
def login_valid():
    """
    用户登录验证
    :return:
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        next_login = request.form['next_login']
        pwd_md5 = stringHelper.encodeStringMD5(password)
        user = User.query.filter(or_(User.username == username, User.email == username),
                                 User.password == pwd_md5, User.status == 200).first()
        if not user:
            dictBackData = {'error': '用户名或密码错误！'}
            return Response(json.dumps([dictBackData]))
        else:
            session['user'] = {'id': user.id, 'name': user.username,
                               'email': user.email, 'photo': user.photo}

            if next_login == 'true':
                # 下次自动登录, 修改session过期时间
                # 添加自动登录加密码到该用户remember_key字段记录， 下
                # 次访问页面查找该session存在则匹配数据库值是否等于session值
                session.permanent = True
                app.permanent_session_lifetime = PERMANENT_SESSION_LIFETIME_USER
                # user_remember_str = encodeStringMD5('%s|%s|%s'% (user.id, random.random(), datetime.datetime.now()))
                # session['remember_key'] = user_remember_str
                # user.remember_key = user_remember_str
            else:
                user.remember_key = ''
            db.session.commit()

            return Response('')


@app.route('/login/out', methods=['POST'])
def logout():
    """
    注销登录ajax
    author: js 2015-12-3
    :return:返回当前页面， 如当前页面需登录后查看，返回首页
    """
    if request.method == 'POST':
        exit = request.form['exit']
        if exit == 'exit':
            try:
                del session['user']
            except:
                pass
            # try:
            #     del session['remember_key']
            # except:
            #     pass
    return redirect('/')

@app.route('/get/locations', methods=['GET'])
def getLocations():
    """
    描述：获取省份城市
    :rawParam：GET方法传入,省份/城市id， level 级别;1-国家;2-省份(州);3-城市(地级市);5-区(县级市);7-街道
    """
    locations = ''
    if request.method == 'GET':
        id = request.args['id']
        level = request.args['level']
        if level == '2':
            locations = Locations.query.filter_by(level=2, status=200).\
                with_entities(Locations.id, Locations.depict).all()
        else:
            try:
                start_num = id[0:int(level)-1]
            except:
                start_num = 0
            locations = Locations.query.filter(Locations.id.startswith(start_num)).filter_by(level=level, status=200).\
                with_entities(Locations.id, Locations.depict).all()

        locations = json.dumps(list(locations))

    return Response(locations)

# @app.route('/login/auto', methods=['POST'])
# def loginAuto():
#     """
#     用户自动登录验证
#     # 下次自动登录, 修改session过期时间
#     # 添加自动登录加密码到该用户remember_key字段记录， 下
#     # 次访问页面查找该session存在则匹配数据库值是否等于session值
#     :return:
#     """
#     try:
#         mine = session['user']
#     except:
#         mine = None
#     if request.method == 'POST' and 'auto_login' in request.form:
#         if not mine:
#             try:
#                 remember_key = session['remember_key']
#             except:
#                 return Response('500')
#             user = User.query.filter_by(remember_key = remember_key).first()
#             if user:
#                 session['user'] = {'id': user.id, 'name': user.username,
#                                    'email': user.email, 'photo': user.photo}
#                 user.remember_key = ''
#                 del session['remember_key']
#                 db.session.commit()
#                 return Response('200')
#             return Response('500')
#         return Response('500')
#
#     return Response('404')

@app.route('/u_test', methods=['GET', 'POST'])
def umeditorTest():

    return render_template('umeditor_test.html')