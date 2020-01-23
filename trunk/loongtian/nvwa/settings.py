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
        user_name = "nvwa"
        nick_name = "女娲"
        real_name ="女娲AI"
        user_password ="123"
        user_email ="langway@163.com"
        user_phone ="15640193617"
        user_gender =2  # 性别 1-男，2-女
        server_ip = "127.0.0.1"
        server_port = 8077
        manageIp = "127.0.0.1"
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


class LinearPattern():
    """
    目前发现的线性pattern包括：
        1、修限型
        （1）R1-...Rn，例如：中国人民银行
        （2）A1A2，例如：跑了
        （3）A1A2R1，例如：跑是动作，跑了一圈
        （4）R1A1A2，例如：动作包含跑
        2、集合型（一般为同一父对象）
        （1）R1-...Rn，例如：四五六七
        （2）A1A2...An，例如：跑跳蹲
    """


