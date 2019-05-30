#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Project:  loongtian/fuxi
Title:    urls.py 
Author:   js 
Description: 此文件记录所有url及对应的实现view方法
"""

urlpatterns = patterns('loongtian.fuxi',
    url(r'^/captcha$', 'utils.captcha.get_code'),  # 验证码
    url(r'^/upload/image$', 'utils.file.uploadImageFile'),  # 接收js上传的图片
    url(r'^/upload/repics', 'utils.file.uploadImageFilesCut'),  # 对js上传的图片进行剪切
    url(r'^/login$', 'utils.gateway.login_valid'),  # 用户登录验证ajax，登录弹出窗口
    url(r'^/login/out$', 'utils.gateway.logout'),  # 注销登录ajax
    url(r'^/get/locations', 'utils.gateway.getLocations'),  # ajax获取省份城市

    url(r'^/register$', 'vie.register.views.register'),  # 注册页面
    url(r'^/register/verify/mail$', 'vie.register.views.registerVerifyMail'),  # 注册验证邮箱
    url(r'^/register/verify/phone', 'vie.register.views.registerVerifyPhone'),  # 注册验证手机
    url(r'^/register/finish$', 'vie.register.views.registerFinish'),  # 完成注册

    url(r'^/user/info$', 'vie.users.views.userInfo'),  # 个人信息设置页面
    url(r'^/user/search$', 'vie.users.views.userSearch'),  # 个人搜索记录页面
    url(r'^/user/photo$', 'vie.users.views.userPhoto'),  # 个人头像设置页面
    url(r'^/user/message$', 'vie.users.views.userMessage'),  # 个人消息列表页面
    url(r'^/user/message/detail$', 'vie.users.views.userMessageDetail'),  # 个人消息详细页面
    url(r'^/user/safety$', 'vie.users.views.userSafety'),  # 个人密码设置页面

    url(r'^/get/search/data$', 'vie.searchGateway.getSearchKeyword'),  # 获取搜索结果并处理

    url(r'^/$', 'vie.views.index'),  # 首页
    url(r'^/index$', 'vie.views.index'),  # 首页
    url(r'^/indexchat$', 'vie.views.indexChat'),  # 首页展示结果（聊天页面）
    url(r'^/pwd/find$', 'vie.views.pwdFind'),  # 忘记密码-找回页面
    url(r'^/pwd/sendmail$', 'vie.views.pwdSendMail'),  # 忘记密码-发送邮件
    url(r'^/pwd/set$', 'vie.views.pwdSet'),  # 忘记密码-设置密码


    url(r'^/u_test', 'utils.gateway.umeditorTest'),  # ？？？测试ueditor用？？？
)