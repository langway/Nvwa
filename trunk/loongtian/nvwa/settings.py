#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

from loongtian.util.db.postgres.db_postgres_settings import PostgresSetting

fontFamily = "微软雅黑"
fontSize = 12
language = "chinese"

class auth():
    """
    权限管理的配置信息
    """
    class message():
        logon_msg = '#logon#' # 登录命令
        logon_succeed_msg = '#logon succeed#'
        logout_msg = '#logout#' # 登出命令

    class adminUser():
        """
        默认超级管理员参数设置
        """
        user_name = u"nvwa"
        nick_name = u"女娲"
        real_name =u"女娲AI"
        user_password =u"123"
        user_email =u"langway@163.com"
        user_phone =u"15640193617"
        user_gender =2  # 性别 1-男，2-女
        server_ip = u"127.0.0.1"
        server_port = 8077
        manageIp = u"127.0.0.1"
        managePort = 8078



class db():
    """
    数据库参数设置
    """
    db_type = "postgres" # 数据库类型
    db_nvwa = "nvwa"
    db_auth ="auth"
    db_yiya = "yiya"
    postgres={
        db_auth:PostgresSetting(Host="localhost", Port=5432, Database="auth", User="postgres", Password="123456qaz"),
        db_nvwa:PostgresSetting(Host="localhost", Port=5432, Database="nvwa", User="postgres", Password="123456qaz"),
        db_yiya: PostgresSetting(Host="localhost", Port=5432, Database="yiya", User="postgres", Password="123456qaz"),
    }

    class tables():
        # table names
        # #############################
        # nvwa数据库表
        # #############################
        tbl_metaData = "tbl_metaData"
        tbl_metaNet = "tbl_metaNet"
        tbl_layer = "tbl_layer"
        tbl_realObject = "tbl_realObject"
        tbl_knowledge = "tbl_knowledge"

        tbl_observer = "tbl_observer"  # 数据对象与观察者之间的关联关系（实现管理员数据对象与用户数据对象分离，相当于Layer的分表）

        # #############################
        # auth数据库表
        # #############################
        tbl_users ="users"
        tbl_locations ="locations"
        tbl_roles = "roles"
        # #############################
        # yiya数据库表
        # #############################
        tbl_users_sms="users_sms"
        tbl_search_record="search_record"


        # 不能删除全部数据的表
        tablesShouldNotPhysicalDeleteAll = [
            tbl_metaData,
        ]

    class mongo():
        mongo_host = "localhost"
        mongo_port = 27017
        mongo_logging = True

class log():
    """
    log参数设置
    """
    logActive = True
    logLevel = "debug"
    logConsole = True
    logFile = True

class InnerOperations():
    """

    """

