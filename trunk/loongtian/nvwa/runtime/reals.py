#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

"""
[运行时对象]用户操作的封装类（对应于软件、数据库等旧系统）
"""
import copy, datetime

import loongtian.util.helper.stringHelper as stringHelper

from loongtian.nvwa import settings
from loongtian.nvwa.models.enum import ObjType
from loongtian.nvwa.models.baseEntity import BaseEntity
from loongtian.nvwa.models.realObject import RealObject, Constitutions
from loongtian.nvwa.language import UserTags, UserErrors
from loongtian.nvwa.runtime.ipAddress import IPAddress

class RealUser(BaseEntity):
    """
    [运行时对象]用户操作的封装类（对应于软件、数据库等旧系统）
    """
    __databasename__ = settings.db.db_auth  # 所在数据库。
    __tablename__ = settings.db.tables.tbl_users  # 所在表。与Flask统一
    primaryKey = copy.copy(BaseEntity.primaryKey)
    primaryKey.append("id")
    columns = copy.copy(BaseEntity.columns)
    columns.extend(["username", "realname","nickname", "email", "phone",
                    "password", "gender", "ismanager", "photo",
                    "assistantid", "location", "oauth"])
    retrieveColumns = copy.copy(BaseEntity.retrieveColumns)  # 查询时需要使用的字段
    retrieveColumns.extend(["username", "email", "phone", "password"])

    def __init__(self, userid=None, username=None, realname=None,nickname=None, email=None, phone=None,
                 password=None, gender=1, ismanager=False, photo=None,
                 assistantid=None, location=0, oauth=0,
                 createrid=None, createrip='0.0.0.1',
                 createtime=datetime.datetime.now(), updatetime=None, lasttime=None,
                 status=200,
                 memory=None):
        """
        [运行时对象]用户操作的封装类（对应于软件、数据库等旧系统）
        :param userid: 主键ID
        :param username: 用户名
        :param realname: 实际名
        :param nickname: 显示昵称
        :param email: 用户邮箱
        :param phone: 手机
        :param password: 密码
        :param gender: 性别 1-男，2-女
        :param ismanager: 是否管理员; False-会员;True-管理员
        :param photo: 用户头像， 存储原图路径，不同尺寸头像单独方法处理
        :param assistantid: 个人助理ID
        :param location: 地区代码， 记录地区唯一编码，单独方法处理
        :param oauth: 标记第三方授权登录， 0为非授权， 1为授权
        :param createrid: 添加人; 格式：(user_id)中文名
        :param createrip: 添加人IP
        :param createtime: 添加时间;
        :param updatetime: 更新时间
        :param lasttime: 最近访问时间
        :param status: 状态; 0-不可用(逻辑删除);200-正常;800-不可遗忘
        """
        super(RealUser, self).__init__(userid,
                                       createrid,
                                       createtime, updatetime, lasttime,
                                       status, memory=memory)

        self.username = username
        self.realname = realname
        self.nickname=nickname
        self.email = email
        self.phone = phone
        self.password = password
        self.gender = gender  # 性别 1-男，2-女
        self.ismanager = ismanager
        self.photo = photo
        self.assistantid = assistantid  # 个人助理ID
        self.location = location
        self.oauth = oauth

        self.createrip = createrip

        self.server_address = IPAddress  # 服务器端的ip地址
        self.client_address = set([])  # 客户端的ip地址(可能有多个,都是str，一个用户有多个连接设备)

    def __repr__(self):
        return '<RealUser %s>' % self.username

    def getShowName(self):
        """
        取得系统显示的名字
        :return:
        """
        show_name = self.nickname
        if show_name:
            return show_name
        show_name = self.username
        if  show_name:
            return show_name
        show_name = self.email
        if show_name:
            return show_name
        return self.phone

    @staticmethod
    def getRealByUserInfo(username, password):
        """
        根据用户名取得实际对象。
        :param username:
        :return:
        """
        if password:
            password = stringHelper.encodeStringMD5(password)

        _real_user = RealUser(username=username, password=password).create()
        user_real = None
        if _real_user:
            user_real = RealObject(rid=_real_user.id).create()
        if user_real:
            return user_real

        user_reals = Constitutions.getRealObjsByConstitutions(
            **{UserTags.username: username, UserTags.password: password})
        return RealUser.__processUser(user_reals)

    @staticmethod
    def getRealByPhoneInfo(phone, password):
        """
        根据用户电话取得实际对象。
        :param phone:
        :return:
        """
        if password:
            password = stringHelper.encodeStringMD5(password)
        if password:
            password = stringHelper.encodeStringMD5(password)

        _real_user = RealUser(phone=phone, password=password).create()
        user_real = None
        if _real_user:
            user_real = RealObject(rid=_real_user.id).create()
        if user_real:
            return user_real

        user_reals = Constitutions.getRealObjsByConstitutions(
            **{UserTags.phone: phone, UserTags.password: password})
        return RealUser.__processUser(user_reals)

    @staticmethod
    def getRealByEmailInfo(email, password):
        """
        根据用户邮件取得实际对象。
        :param email:
        :return:
        """
        if password:
            password = stringHelper.encodeStringMD5(password)

        _real_user = RealUser(email=email, password=password).create()
        user_real = None
        if _real_user:
            user_real = RealObject(rid=_real_user.id).create()
        if user_real:
            return user_real

        user_reals = Constitutions.getRealObjsByConstitutions(
            **{UserTags.email: email, UserTags.password: password})
        return RealUser.__processUser(user_reals)

    @staticmethod
    def __processUser(user_reals):
        """
        对实际对象查询的结果进一步处理
        :param user_reals:
        :return:
        """
        if len(user_reals) <= 0:
            return None
        elif len(user_reals) == 1:
            real_user = user_reals[0]
            if real_user.getType() == ObjType.USER:
                return real_user
            raise Exception(UserErrors.ObjType_Is_Not_USER)

        else:
            for real_user in user_reals:
                if real_user.realType == ObjType.USER:
                    return real_user

            raise Exception(UserErrors.Multi_Results_And_ObjType_Is_Not_USER)

    @staticmethod
    def getAssistant(real):
        """
        根据用户取得个人助理。
        :param real:
        :return:
        """
        real_assistants, related_ks = real.Constitutions.getRelatedObjects(UserTags.assistant)
        return RealUser.__processAssistant(real_assistants)

    @staticmethod
    def __processAssistant(real_assistants):
        """
        对个人助理实际对象查询的结果进一步处理
        :param real_assistants:
        :return:
        """
        if not real_assistants:
            return None
        elif len(real_assistants) == 1:
            real_assistant = real_assistants[0]
            if real_assistant.getType() == ObjType.ASSISTANT or \
                    real_assistant.getType() == ObjType.INSTINCT:  # 普通用户-个人助理类型，超级用户直接使用女娲AI
                return real_assistant
            raise Exception(UserErrors.ObjType_Is_Not_ASSISTANT)

        else:
            for real_assistant in real_assistants:
                if real_assistant.realType == ObjType.ASSISTANT or \
                        real_assistant.getType() == ObjType.INSTINCT:  # 普通用户-个人助理类型，超级用户直接使用女娲AI:
                    return real_assistant

            raise Exception(UserErrors.Multi_Results_And_ObjType_Is_Not_ASSISTANT)

    @classmethod
    def createUser(cls, username=None, realname=None, nickname=None,
                   password=None,
                   email=None, phone=None,
                   gender=1, ismanager=False, photo=None,
                   assistantid=None, status=200,
                   memory=None,
                   create_assistant=True,
                   recordInDB=True):
        """
        根据用户信息创建用户、个人助理
        :param username:
        :param password:
        :param email:
        :param phone:
        :return:
        """
        if not username and not email and not phone:
            raise Exception("username、email、phone至少要有一个！")
        if not password:
            raise Exception("必须提供密码！")
        password=stringHelper.encodeStringMD5(password)
        _real_user = cls(username=username, realname=realname,nickname=nickname, password=password,
                         email=email, phone=phone, gender=gender,
                         ismanager=ismanager, photo=photo,
                         assistantid=assistantid,
                         status=status, memory=memory).create(recordInDB=recordInDB)
        _user_real = RealObject(rid=_real_user.id,
                                remark=username,
                                realType=ObjType.USER,
                                status=status,
                                memory=memory).create(recordInDB=recordInDB)
        real_assistant = None
        if _user_real:
            if create_assistant:  # 如果数据库中已存在用户，检查其关联的个人助理
                real_assistant = RealUser.getAssistant(_user_real)
                if not real_assistant:
                    real_assistant = RealUser.createAssistant(_user_real,
                                                              ismanager=True,
                                                              recordInDB=recordInDB)
                    if real_assistant and not assistantid:
                        assistantid = real_assistant.id
                        _real_user.updateAttributeValues(**{"assistantid": assistantid})
        else:
            raise Exception(UserErrors.Can_Not_Create_User)

        RealUser.setUserRealConstituents(_user_real,
                                         username=username, realname=realname,nickname=nickname,
                                         password=password,
                                         email=email, phone=phone, gender=gender,
                                         ismanager=ismanager, photo=photo,
                                         recordInDB=recordInDB)

        return _real_user, _user_real, real_assistant

    @staticmethod
    def setUserRealConstituents(user_real, username=None, realname=None, nickname=None,
                                password=None,
                                email=None, phone=None, gender=1, ismanager=False, photo=None,
                                recordInDB=True):
        if username:
            user_real.Constitutions.addRelatedObject(UserTags.username, username, recordInDB=recordInDB)
        if realname:
            user_real.Constitutions.addRelatedObject(UserTags.realname, realname, recordInDB=recordInDB)
        if nickname:
            user_real.Constitutions.addRelatedObject(UserTags.nickname, nickname, recordInDB=recordInDB)

        if password:
            password = stringHelper.encodeStringMD5(password)
            user_real.Constitutions.addRelatedObject(UserTags.password, password, recordInDB=recordInDB)
        if email:
            user_real.Constitutions.addRelatedObject(UserTags.email, email, recordInDB=recordInDB)
        if phone:
            user_real.Constitutions.addRelatedObject(UserTags.phone, phone, recordInDB=recordInDB)
        if gender:  # 性别 1-男，2-女
            if gender == 1:
                gender = "男"
            else:
                gender = "女"
            user_real.Constitutions.addRelatedObject(UserTags.gender, gender, recordInDB=recordInDB)
        if ismanager:
            user_real.Constitutions.addRelatedObject(UserTags.manager, ismanager, recordInDB=recordInDB)
        if photo:
            user_real.Constitutions.addRelatedObject(UserTags.photo, photo, recordInDB=recordInDB)

    @staticmethod
    def createAssistant(user_real, ismanager=False, recordInDB=True,memory=None):
        """
        根据用户创建其个人助理。
        :param _user_real:
        :return:
        """
        assistant_real = None
        from loongtian.nvwa.runtime.instinct import Instincts
        Instincts.loadAllInstincts(memory=memory)
        if ismanager:
            assistant_real = Instincts.instinct_nvwa_ai
        else:
            # 创建一个新的
            assistant_real = RealObject(remark=user_real.remark + "的助理",
                                        realType=ObjType.ASSISTANT,
                                        createrid=user_real.id).create(recordInDB=recordInDB)

        user_real.Constitutions.addRelatedObject(UserTags.assistant, assistant_real, recordInDB=recordInDB)

        return assistant_real


from loongtian.util.common.singleton import singleton


# @singleton
class AdminUser(RealUser):
    """
    超级管理员用户（只有一个）
    """
    # 超级管理员用户（只有一个）
    admin_real_user = None
    admin_user_real = None
    admin_user_assistant = None

    @classmethod
    def getAdminUser(cls, memory=None):
        """
        取得或创建超级管理员用户（只有一个）
        :return:
        """
        if cls.admin_real_user:
            return cls.admin_real_user
        from loongtian.nvwa.runtime.instinct import Instincts
        Instincts.loadAllInstincts(memory=memory)
        from loongtian.nvwa import settings
        result = AdminUser.createUser(username=settings.auth.adminUser.user_name,
                                      realname=settings.auth.adminUser.real_name,
                                      nickname=settings.auth.adminUser.nick_name,
                                      password=settings.auth.adminUser.user_password,
                                      email=settings.auth.adminUser.user_email,
                                      phone=settings.auth.adminUser.user_phone,
                                      gender=settings.auth.adminUser.user_gender,
                                      ismanager=True,  # 超级管理员
                                      assistantid=Instincts.instinct_nvwa_ai.id,
                                      status=800,  # 不可删除
                                      memory=memory,
                                      create_assistant=True, recordInDB=True)  # 创建个人助理
        if result:
            cls.admin_real_user, cls.admin_user_real, cls.admin_user_assistant = result
            cls.admin_real_user.server_address.ip = settings.auth.adminUser.server_ip
            cls.admin_real_user.server_address.port = settings.auth.adminUser.server_port

        return cls.admin_real_user

    def __repr__(self):
        return '<AdminUser %s>' % self.username


class RealLocation(BaseEntity):
    """
    [运行时对象]实际地址的封装类（对应于软件、数据库等旧系统）
    """
    __databasename__ = settings.db.db_auth  # 所在数据库。
    __tablename__ = settings.db.tables.tbl_locations  # 所在表。与Flask统一
    primaryKey = copy.copy(BaseEntity.primaryKey)
    primaryKey.append("id")
    columns = copy.copy(BaseEntity.columns)
    columns.extend(["depict", "level",
                    "lead", "arecode", "zipcode", "remark",
                    ])

    def __init__(self, id=None, depict=None, level=None,
                 lead=None, arecode=None, zipcode=None, remark=None,
                 createrid=None, createrip='0.0.0.1',
                 createtime=None, updatetime=None, lasttime=None,
                 status=200  # 状态; 0-不可用(逻辑删除);200-正常;800-不可遗忘
                 ):
        """
        [运行时对象]实际地址的封装类（对应于软件、数据库等旧系统）
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
        super(RealLocation, self).__init__(id,
                                           createrid, createrip,
                                           createtime, updatetime, lasttime,
                                           status)
        self.depict = depict
        self.level = level
        self.lead = lead
        self.arecode = arecode
        self.zipcode = zipcode
        self.remark = remark

    def __repr__(self):
        return '<RealLocation %r>' % self.lead


class RealUsersSms(BaseEntity):
    """
    [运行时对象]消息数据模型的封装类（对应于软件、数据库等旧系统）
    """
    __databasename__ = settings.db.db_yiya  # 所在数据库。
    __tablename__ = settings.db.tables.tbl_users_sms  # 所在表。与Flask统一
    primaryKey = copy.copy(BaseEntity.primaryKey)
    primaryKey.append("id")
    columns = copy.copy(BaseEntity.columns)
    columns.extend(["stype", "sender",
                    "receiver", "title", "content", "read",
                    ])

    def __init__(self, id=None, stype=None, sender=None,
                 receiver=None, title=None, content=None, read=None,
                 createrid=None, createrip=None,
                 createtime=None, updatetime=None, lasttime=None,
                 status=None
                 ):
        """
        [运行时对象]消息数据模型的封装类（对应于软件、数据库等旧系统）
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
        super(RealUsersSms, self).__init__(id,
                                           createrid, createrip,
                                           createtime, updatetime, lasttime,
                                           status)
        self.stype = stype  # 信息类型: 0-系统消息;1-站内信
        self.sender = sender  # 发件人; 用户id  ？？？是否需要做成外键关联？？？
        self.receiver = receiver  # 收件人; 用户id  ？？？是否需要做成外键关联？？？
        self.title = title  # 标题
        self.content = content  # 内容
        self.read = read  # 是否已读; 0-未读;1-已读

    def __repr__(self):
        return '<RealUsersSms %r>' % self.title


class RealSearchRecord(BaseEntity):
    """
    [运行时对象]搜索记录数据模型的封装类（对应于软件、数据库等旧系统）
    Author:   leon 
    DateTime: 2019/3/5
    """
    __databasename__ = settings.db.db_yiya  # 所在数据库。
    __tablename__ = settings.db.tables.tbl_search_record  # 所在表。与Flask统一
    primaryKey = copy.copy(BaseEntity.primaryKey)
    primaryKey.append("id")
    columns = copy.copy(BaseEntity.columns)
    columns.extend(["user", "search", "result",
                    ])

    def __init__(self, id=None, user=None, search=None, result=None,
                 createrid=None, createrip=None,
                 createtime=None, updatetime=None, lasttime=None,
                 status=None
                 ):
        """
        [运行时对象]搜索记录数据模型的封装类（对应于软件、数据库等旧系统）
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
        super(RealSearchRecord, self).__init__(id,
                                               createrid, createrip,
                                               createtime, updatetime, lasttime,
                                               status)
        self.user = user  # 记录用户id， ？？？是否改成外键？？？
        self.search = search  # 记录用户搜索问题
        self.result = result  # 记录返回搜索结果 ？？？暂时记录后台返回内容？？？

    def __repr__(self):
        return '<RealSearchRecord %r>' % self.search
