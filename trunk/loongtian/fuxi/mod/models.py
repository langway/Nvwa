#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Project:  loongtian/fuxi
Title:    models 
Author:   js 
DateTime: 2015/11/23
"""
import datetime

__author__ = 'js'
try:
    from flask.ext.sqlalchemy import SQLAlchemy
except:
    from flask_sqlalchemy import SQLAlchemy
from loongtian.nvwa.runtime.reals import RealUser, RealLocation, RealUsersSms, RealSearchRecord
from loongtian.fuxi import app

db = SQLAlchemy(app)


class User(db.Model, RealUser):
    """
    用户基础数据模型
    Author:   js 
    DateTime: 2015/11/23
    """

    # __tablename__ = 'users' # 已在RealUser中定义

    userid = db.Column(db.String(32), primary_key=True)  # 主键ID
    username = db.Column(db.String(80), unique=True, index=True)  # 用户名
    nickname = db.Column(db.String(80), unique=True, index=True)  # 显示昵称
    realname = db.Column(db.String(80), index=True)  # 真实的用户名
    email = db.Column(db.String(120), unique=True)  # 用户邮箱
    phone = db.Column(db.String(80), unique=True)  # 手机
    password = db.Column(db.String(256), unique=False)  # 密码
    gender = db.Column(db.Integer(), default=1)  # 性别
    ismanager = db.Column(db.Boolean(), default=False)  # 是否管理员; False-会员;True-管理员
    photo = db.Column(db.String(248), unique=False)  # 用户头像， 存储原图路径，不同尺寸头像单独方法处理
    assistantid = db.Column(db.String(32), index=True)  # 个人助理ID
    location = db.Column(db.Integer(), default=0)  # 地区代码， 记录地区唯一编码，单独方法处理
    oauth = db.Column(db.Integer(), default=0)  # 标记第三方授权登录， 0为非授权， 1为授权
    # remember_key = db.Column(db.String(256), nullable=True)     # 用于记录用户自动登录加密值

    createrid = db.Column(db.String(32), unique=False)  # 添加人; 格式：(user_id)中文名
    createrip = db.Column(db.String(15), unique=False, default='0.0.0.0')  # 添加人IP
    createtime = db.Column(db.DateTime(), unique=False, default=datetime.datetime.now())  # 添加时间;
    updatetime = db.Column(db.DateTime(), unique=False, default=datetime.datetime.now())  # 更新时间;
    lasttime = db.Column(db.DateTime(), unique=False, default=datetime.datetime.now())  # 最近访问时间;
    status = db.Column(db.Integer(), nullable=False, default=200)  # 状态; 0-不可用(逻辑删除);200-正常;800-不可遗忘

    def __init__(self, userid=None, username='', email='', phone='', password='',
                 gender=1, ismanager=False, photo='',
                 location=0, oauth=0,
                 createrid='', createrip='0.0.0.1',
                 createtime=datetime.datetime.now(), updatetime=None, lasttime=None,
                 status=200,memory=None):
        RealUser.__init__(userid, username, email, phone, password, gender, ismanager, photo,
                          location, oauth,
                          createrid, createrip,
                          createtime, updatetime, lasttime,
                          status,memory=memory)

    def __repr__(self):
        return '<User %r>' % self.username


class Locations(db.Model, RealLocation):
    """
    描述：地区（行政区划）
    Author:   js 
    DateTime: 2015/11/24
    """
    # __tablename__ = 'locations' # 已在RealLocation中定义

    CHOICES_LEVEL = (
        (0, '层次标记'),  # 不显示也不被应用，仅体现层级关系
        (1, '国家'),
        (2, '省份(州)'),  # 包括省、直辖市
        (3, '城市'),  # 包括省会城市、地级市
        (5, '区/县'),  # 包括区、县级市
        (7, '街道'),
    )

    id = db.Column(db.Integer, primary_key=True)  # 地区编码  代码;
    depict = db.Column(db.String(20))  # 名称;
    level = db.Column(db.Integer, default=0)  # 级别;1-国家;2-省份(州);3-城市(地级市);5-区(县级市);7-街道
    lead = db.Column(db.String(64))  # 全名
    arecode = db.Column(db.String(20))  # 区号
    zipcode = db.Column(db.Integer, default=0, nullable=True)  # 邮编
    remark = db.Column(db.String(500), nullable=True)  # 注释

    createrid = db.Column(db.String(32), unique=False)  # 添加人; 格式：(user_id)中文名
    createrip = db.Column(db.String(15), unique=False, default='0.0.0.0')  # 添加人IP
    createtime = db.Column(db.DateTime(), unique=False, default=datetime.datetime.now())  # 添加时间;
    updatetime = db.Column(db.DateTime(), unique=False, default=datetime.datetime.now())  # 更新时间;
    lasttime = db.Column(db.DateTime(), unique=False, default=datetime.datetime.now())  # 最近访问时间;
    status = db.Column(db.Integer(), nullable=False, default=200)  # 状态; 0-不可用(逻辑删除);200-正常;800-不可遗忘

    def __init__(self, id=None, depict=None, level=None,
                 lead=None, arecode=None, zipcode=None, remark=None,
                 createrid='', createrip='0.0.0.1',
                 createtime=None, updatetime=None, lasttime=None,
                 status=200,  # 状态; 0-不可用(逻辑删除);200-正常;800-不可遗忘
                 ):
        """
        实际地址的封装类（对应于软件、数据库等旧系统）
        :param id: 地区编码  代码
        :param depict: 名称
        :param level: 级别;1-国家;2-省份(州);3-城市(地级市);5-区(县级市);7-街道
        :param lead: 全名
        :param arecode: 区号
        :param zipcode: 邮编
        :param remark:注释
        :param createrid: 添加人; 格式：(user_id)中文名
        :param createrip: 添加人IP
        :param createtime: 添加时间;
        :param updatetime: 更新时间
        :param lasttime: 最近访问时间
        :param status: 状态; 0-不可用(逻辑删除);200-正常;800-不可遗忘
        :param memory:
        """
        RealLocation.__init__(id, depict, level, lead, arecode, zipcode, remark,
                              createrid, createrip,
                              createtime, updatetime, lasttime,
                              status)

    def __repr__(self):
        return '<Locations %r>' % self.depict


class UsersSms(db.Model, RealUsersSms):
    """
    消息数据模型
    Author:   js 
    DateTime: 2015/11/24
    """

    # __tablename__ = 'users_sms' # 已在RealUsersSms中定义
    __bind_key__ = 'users_sms'  # 对应SQLALCHEMY_BINDS
    id = db.Column(db.Integer, primary_key=True)  # 主键ID
    stype = db.Column(db.Integer, default=0)  # 信息类型: 0-系统消息;1-站内信
    sender = db.Column(db.String(32))  # 发件人; 用户id  ？？？是否需要做成外键关联？？？
    receiver = db.Column(db.String(32))  # 收件人; 用户id  ？？？是否需要做成外键关联？？？
    title = db.Column(db.String(256))
    content = db.Column(db.String(512))
    read = db.Column(db.Integer, default=0)  # 是否已读; 0-未读;1-已读

    createrid = db.Column(db.String(32), unique=False)  # 添加人; 格式：(user_id)中文名
    createrip = db.Column(db.String(15), unique=False, default='0.0.0.0')  # 添加人IP
    createtime = db.Column(db.DateTime(), unique=False, default=datetime.datetime.now())  # 添加时间;
    updatetime = db.Column(db.DateTime(), unique=False, default=datetime.datetime.now())  # 更新时间;
    lasttime = db.Column(db.DateTime(), unique=False, default=datetime.datetime.now())  # 最近访问时间;
    status = db.Column(db.Integer(), nullable=False, default=200)  # 状态; 0-不可用(逻辑删除);200-正常;800-不可遗忘

    def __init__(self, id=None, stype=None, sender=None,
                 receiver=None, title=None, content=None, read=None,
                 createrid=None, createrip=None,
                 createtime=None, updatetime=None, lasttime=None,
                 status=None
                 ):
        """
        消息数据模型
        :param id:
        :param stype: # 信息类型: 0-系统消息;1-站内信
        :param sender: # 发件人; 用户id  ？？？是否需要做成外键关联？？？
        :param receiver: # 收件人; 用户id  ？？？是否需要做成外键关联？？？
        :param title: 标题
        :param content: 内容
        :param read: 是否已读的标记
        :param createrid: 添加人; 格式：(user_id)中文名
        :param createrip: 添加人IP
        :param createtime: 添加时间;
        :param updatetime: 更新时间
        :param lasttime: 最近访问时间
        :param status: 状态; 0-不可用(逻辑删除);200-正常;800-不可遗忘
        """
        RealUsersSms.__init__(id,
                              stype, sender,
                              receiver, title, content, read,
                              createrid, createrip,
                              createtime, updatetime, lasttime,
                              status)

    def __repr__(self):
        return '<UsersSms %r>' % self.title


class SearchRecord(db.Model, RealSearchRecord):
    """
    搜索记录数据模型
    Author:   js 
    DateTime: 2015/12/11
    """
    # __tablename__ = 'search_record' # 已在RealSearchRecord中定义
    __bind_key__ = 'search_record'  # 对应SQLALCHEMY_BINDS
    id = db.Column(db.Integer, primary_key=True)  # 主键ID
    user = db.Column(db.String(32), nullable=False)  # 记录用户id， ？？？是否改成外键？？？
    search = db.Column(db.String(512), nullable=False)  # 记录用户搜索问题
    result = db.Column(db.String(1024), nullable=False)  # 记录返回搜索结果 ？？？暂时记录后台返回内容？？？

    createrid = db.Column(db.String(32), unique=False)  # 添加人; 格式：(user_id)中文名
    createrip = db.Column(db.String(15), unique=False, default='0.0.0.0')  # 添加人IP
    createtime = db.Column(db.DateTime(), unique=False, default=datetime.datetime.now())  # 添加时间;
    updatetime = db.Column(db.DateTime(), unique=False, default=datetime.datetime.now())  # 更新时间;
    lasttime = db.Column(db.DateTime(), unique=False, default=datetime.datetime.now())  # 最近访问时间;
    status = db.Column(db.Integer(), nullable=False, default=200)  # 状态; 0-不可用(逻辑删除);200-正常;800-不可遗忘

    def __init__(self, id=None, user=None, search=None, result=None,
                 createrid=None, createrip=None,
                 createtime=None, updatetime=None, lasttime=None,
                 status=None
                 ):
        """
        搜索记录数据模型
        :param id:
        :param user: # 记录用户id， ？？？是否改成外键？？？
        :param search: # 记录用户搜索问题
        :param result: # 记录返回搜索结果 ？？？暂时记录后台返回内容？？？
        :param createrid: 添加人; 格式：(user_id)中文名
        :param createrip: 添加人IP
        :param createtime: 添加时间;
        :param updatetime: 更新时间
        :param lasttime: 最近访问时间
        :param status: 状态; 0-不可用(逻辑删除);200-正常;800-不可遗忘
        """
        RealSearchRecord.__init__(id,
                                  user, search, result,
                                  createrid, createrip,
                                  createtime, updatetime, lasttime,
                                  status)

    def __repr__(self):
        return '<searchRecord %r>' % self.search


db.create_all()

# db.create_all(bind=['users'])
# db.create_all(bind='appmeta')
# db.drop_all(bind=None)
