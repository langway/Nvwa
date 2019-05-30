#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试题关键词获取相关内容接口
Project:  loongtian/fuxi
Author:   js
DateTime: 2015/12/2
"""
import json
import datetime
from loongtian.fuxi import app
from flask import request, Response, session, render_template
from loongtian.fuxi.mod.models import SearchRecord, db
from loongtian.fuxi.vie.nvwaGateway import getSearchData

__author__ = 'js'


@app.route('/get/search/data', methods=['GET', 'POST'])
def getSearchKeyword():
    """
    关键词获取相关搜索
    在此方法中调用webservers 获取数据处理后返回到页面
    :return:webServers 返回json格式数据
    """
    try:
        mine = session['user']
    except:
        mine = None

    keyword = request.args.get('keyword', '')
    k_id = request.args.get('k_id', '')

    # 此处调用接口方法获取返回数据， 之后需调整返回不用样式的html模板
    searchData = getSearchData(keyword)
    search_type = searchData[0]['type']
    if search_type == u'text':
        tmp_html = 'chat_tags/sys_text.html'
    elif search_type == u'images':
        tmp_html = 'chat_tags/sys_images.html'
    elif search_type == u'info':
        tmp_html = 'chat_tags/sys_info.html'
    elif search_type == u'music':
        tmp_html = 'chat_tags/sys_music.html'
    elif search_type == u'video':
        tmp_html = 'chat_tags/sys_video.html'

    # 此处调用webservers获取返回数据， 之后需调整返回不用样式的html模板
    if mine and keyword:
        search_his = SearchRecord.query.filter_by(user=mine['id'], search=keyword).first()
        if search_his:
            search_his.result = json.dumps(searchData, ensure_ascii=False)
            search_his.addtime = datetime.datetime.now()
        else:
            search_record = SearchRecord(user=mine['id'], search=keyword,
                                         result=json.dumps(searchData, ensure_ascii=False), status=200)
            db.session.add(search_record)
        db.session.commit()

    return render_template(tmp_html, searchData=searchData)
    # return Response(json.dumps(searchData))

