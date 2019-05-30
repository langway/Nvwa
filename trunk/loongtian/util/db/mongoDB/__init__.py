#! /usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'leon'

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from loongtian.util.db.mongoDB import db_mongo_settings
from loongtian.util.language import text



class mongo():
    """
    MongoDB数据库操作类。
    """

    def __init__(self):
        #
        self.dbClient = None  # MongoDB客户端对象


    def writeLogCallBack(self,content):
        """
        用来记录日志的函数，可在调用端重写。
        :param content:
        :return:
        """
        print (content)


    # ----------------------------------------------------------------------
    def dbConnect(self):
        """连接MongoDB数据库"""
        # 试着启动服务
        from loongtian.util.db.mongoDB import mongoHelper
        mongoHelper.startMongoDBService()

        if not self.dbClient:
            # 读取MongoDB的设置
            try:
                # 设置MongoDB操作的超时时间为0.5秒
                self.dbClient = MongoClient(db_mongo_settings.mongoHost, db_mongo_settings.mongoPort, connectTimeoutMS=db_mongo_settings.connectTimeoutMS)

                # 调用server_info查询服务器状态，防止服务器异常并未连接成功
                self.dbClient.server_info()

                self.writeLogCallBack(text.DATABASE_CONNECTING_COMPLETED)

            except ConnectionFailure as ex:
                self.writeLogCallBack(text.DATABASE_CONNECTING_FAILED)
            except Exception as ex:

                self.writeLogCallBack(text.DATABASE_CONNECTING_FAILED)

    # ----------------------------------------------------------------------
    def dbInsert(self, dbName, collectionName, d):
        """向MongoDB中插入数据，d是具体数据"""
        if self.dbClient:
            db = self.dbClient[dbName]
            collection = db[collectionName]
            collection.insert_one(d)
            collection.save(d)  # 添加数据
        else:
            self.writeLogCallBack(text.DATA_INSERT_FAILED)

    # ----------------------------------------------------------------------
    def dbQuery(self, dbName, collectionName, d):
        """
        从MongoDB中读取数据，d是查询要求，返回的是数据库查询的指针。查询所有记录。
        :param dbName:
        :param collectionName:
        :param d: 例如{"name":"xiaoliu"}
        :return:
        """
        if self.dbClient:
            db = self.dbClient[dbName]
            collection = db[collectionName]
            cursor = collection.find(d)
            if cursor:
                return list(cursor)
            else:
                return []
        else:
            self.writeLogCallBack(text.DATA_QUERY_FAILED)
            return []

    # ----------------------------------------------------------------------
    def dbQuery_One(self, dbName, collectionName, d):
        """
        从MongoDB中读取数据，d是查询要求，返回的是数据库查询的指针。查询单条记录。
        :param dbName:
        :param collectionName:
        :param d: 例如{"name":"xiaoliu"}
        :return:
        """
        if self.dbClient:
            db = self.dbClient[dbName]
            collection = db[collectionName]
            return collection.find_one(d)

        else:
            self.writeLogCallBack(text.DATA_QUERY_FAILED)
            return None
    # ----------------------------------------------------------------------
    def dbUpdate(self, dbName, collectionName, d, flt, upsert=False):
        """
        向MongoDB中更新数据，d是具体数据，flt是过滤条件，upsert代表若无是否要插入
        :param dbName:
        :param collectionName:
        :param d:
        :param flt: 例如{"name":"xiaoliu"}
        :param upsert:
        :return:
        """
        if self.dbClient:
            db = self.dbClient[dbName]
            collection = db[collectionName]
            collection.replace_one(flt, d, upsert)
        else:
            self.writeLogCallBack(text.DATA_UPDATE_FAILED)

            # ----------------------------------------------------------------------

    def dbRemove(self, dbName, collectionName, d):
        """
        从MongoDB中删除数据
        :param dbName:
        :param collectionName:
        :param d:
        :return:
        """
        if self.dbClient:
            db = self.dbClient[dbName]
            collection = db[collectionName]
            collection.remove(d)
        else:
            self.writeLogCallBack(text.DATA_REMOVE_FAILED)

