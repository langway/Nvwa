#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

"""
存储配置
"""

import os

basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = 'you-will-never-guess'
SQLALCHEMY_TRACK_MODIFICATIONS = True

# 数据库地址需要配置在SQLALCHEMY_DATABASE_URI中, SQLALchemy支持多种数据库, 配置格式如下
"""
Postgres:
　　  postgresql://username:password@hostname:port/mydatabase
　　MySQL:
　　  mysql://username:password@hostname:port/mydatabase
　　Oracle:
　　  oracle://username:password@hostname:port/sidname
　　SQLite:
  sqlite:///c:/absolute/path/to/mydatabase(win)
　　  sqlite:////absolute/path/to/mydatabase(unix) foo.db
"""
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:123456qaz@localhost:5432/auth'  # 'mysql://root:root@localhost:3306/loongsou'
SQLALCHEMY_DEV_DATABASE_URI = 'postgresql://postgres:123456qaz@localhost:5432/auth'
SQLALCHEMY_TEST_DATABASE_URI = 'postgresql://postgres:123456qaz@localhost:5432/auth'

# SQLALCHEMY_BINDS = { # 绑定多个数据库
#     'users': 'mysqldb://localhost/users',
#     'appmeta': 'sqlite:////path/to/appmeta.db'
# }
SQLALCHEMY_BINDS = { # 绑定多个数据库
    'users_sms': 'postgresql://postgres:123456qaz@localhost:5432/yiya',
    'search_record': 'postgresql://postgres:123456qaz@localhost:5432/yiya'
}
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
DEBUG = True

MAIL_SERVER = 'smtp.163.com'
MAIL_PORT = 25

MAIL_USERNAME = 'dnet12@163.com'
MAIL_PASSWORD = 'vlgvbixywqitbysc'  # 后期设定环境变量
FLASKY_MAIL_SUBJECT_PREFIX = '[龙搜]'
FLASKY_MAIL_SENDER = '龙搜 <dnet12@163.com>'
FLASKY_ADMIN = ''

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'img')  # 获取当前文件夹内的Test_Data文件
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
SYSTEM_ROOT = os.getcwd()  # 系统环境根目录
SITE_PATH = os.path.join(SYSTEM_ROOT, 'static', 'photo')  # 上传图片路径

# 设置SESSION参数有效期
PERMANENT_SESSION_LIFETIME = 60 * 60 * 7
# 设置SESSION参数有效期，用于用户自动登录
PERMANENT_SESSION_LIFETIME_USER = 60 * 60 * 24 * 2

class BaseConfig:
    SECRET_KEY = 'you-will-never-guess'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # 数据库地址需要配置在SQLALCHEMY_DATABASE_URI中, SQLALchemy支持多种数据库, 配置格式如下
    """
    Postgres:
　　  postgresql://username:password@hostname:port/mydatabase
　　MySQL:
　　  mysql://username:password@hostname:port/mydatabase
　　Oracle:
　　  oracle://username:password@hostname:port/sidname
　　SQLite:
      sqlite:///c:/absolute/path/to/mydatabase(win)
　　  sqlite:////absolute/path/to/mydatabase(unix) foo.db
    """
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:123456qaz@localhost:5432/auth'  # 'mysql://root:root@localhost:3306/loongsou'
    SQLALCHEMY_DEV_DATABASE_URI = 'postgresql://postgres:123456qaz@localhost:5432/auth'
    SQLALCHEMY_TEST_DATABASE_URI = 'postgresql://postgres:123456qaz@localhost:5432/auth'

    # SQLALCHEMY_BINDS = { # 绑定多个数据库
    #     'users': 'mysqldb://localhost/users',
    #     'appmeta': 'sqlite:////path/to/appmeta.db'
    # }
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    DEBUG = True

    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 25

    MAIL_USERNAME = 'dnet12@163.com'
    MAIL_PASSWORD = 'vlgvbixywqitbysc'  # 后期设定环境变量
    FLASKY_MAIL_SUBJECT_PREFIX = '[龙搜]'
    FLASKY_MAIL_SENDER = '龙搜 <dnet12@163.com>'
    FLASKY_ADMIN = ''

    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'img')  # 获取当前文件夹内的Test_Data文件
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
    SYSTEM_ROOT = os.getcwd()  # 系统环境根目录
    SITE_PATH = os.path.join(SYSTEM_ROOT, 'static', 'photo')  # 上传图片路径

    # 设置SESSION参数有效期
    PERMANENT_SESSION_LIFETIME = 60 * 60 * 7
    # 设置SESSION参数有效期，用于用户自动登录
    PERMANENT_SESSION_LIFETIME_USER = 60 * 60 * 24 * 2

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = BaseConfig.SQLALCHEMY_DEV_DATABASE_URI


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = BaseConfig.SQLALCHEMY_TEST_DATABASE_URI


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = BaseConfig.SQLALCHEMY_DATABASE_URI


config_dict = {
    'running_state': {  # 运行状态
        'development': DevelopmentConfig,
        'testing': TestingConfig,
        'production': ProductionConfig,
        'default': DevelopmentConfig, },
    'cur_running_state': 'development',  # 当前的运行状态
    'database': "postgre"
}
