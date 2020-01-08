#!/usr/bin/env python
# coding: utf-8

__author__ = 'CoolSnow'

import types

import psycopg2
from psycopg2 import OperationalError,IntegrityError
from DBUtils.PooledDB import PooledDB

class _DbPool(object):
    """
    数据库连接池
    :parameter
    host 数据库IP地址，默认为LocalHost。
    port 数据库端口号，默认为5432。
    database 数据库名称。
    user 数据库登录用户名，默认为postgres。
    password 数据库登录密码，默认为123456。
    maxConnection 池中数据库连接数量，默认是10。
    mincached 最小连接数，默认是1。
    maxcached 最大连接数，默认是10。
    blocking 连接数超出后是否为阻塞，默认是False（直接报错）。
    maxusage 单个连接的最大复用次数，默认是无限制复用。
    setsession 额外的SQL命令（eg：["set datestyle to ...", "set time zone ..."]），默认为None。
    ping 检查连接（位运算），1：取出时检查；2：创建游标时检查；4：查询时检查；默认为1。
    :attribute
    count 受影响的行数
    """

    def __init__(
            self, host="localhost", port=5432,
            database="Test", user="postgres", password="123456",
            mincached=1, maxcached=10,
            blocking=False, maxusage=None, setsession=None, ping=7
    ):
        self.count = 0
        try:
            self.__pool = PooledDB(
                psycopg2, host=host, port=port,
                database=database, user=user, password=password,
                mincached=mincached, maxcached=maxcached, maxconnections=maxcached,
                blocking=blocking, maxusage=maxusage, setsession=setsession, ping=ping
            )

        except Exception as e:
            # print (str(e).decode("GBK"))
            raise e

    def size(self):
        """
        获得数据库连接池的最大连接数
        :return 返回当前数据库连接池的最大连接数
        """
        return self.__pool._maxconnections

    def executeSQL(self, sql, fetchone=False):
        """
        执行SQL语句
        :parameter
        sql 要执行的SQL语句，
            SQL可以是一组待执行的SQL语句数组，但如果包含查询，则只返回最后的查询结果。
            用例场景为：将一组事务放在[SQL]中执行，以保证其原子操作性。
        fetchone 取一行还是多行，True：取一行；False：取全部。默认False。
        :return 返回执行SQL语句的结果集
        """
        self.count = 0
        if not isinstance(sql,list):
            sql = [sql]

        connection = None
        cursor = None
        oneSql = None

        try:
            connection = self.__pool.connection()
            cursor = connection.cursor()
            for oneSql in sql:
                cursor.execute(oneSql)
                self.count += cursor.rowcount
                if __debug__:
                    print (cursor.rowcount, ":", oneSql)
            results = []
            try:
                desc = cursor.description
                if fetchone:
                    result = [cursor.fetchone()]
                else:
                    result = cursor.fetchall()
                for row in result:
                    dct = {}
                    for i in range(0, desc.__len__()):
                        dct[desc[i].name] = row[i]
                    results.append(dct)
            except Exception as e:
                pass
            connection.commit()
            return results
        # except IntegrityError as e:
        #     pass
        except Exception as  e:
            if connection:
                connection.rollback()
            if __debug__ and oneSql:
                print ("ErrorSQL:", oneSql)
            raise e
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def getRowCount(self):
        """
        返回受影响的行数
        :return: 受影响的行数
        """
        return self.count


# def createDbPool():
#     return _DbPool(host = Host, port = Port, database = Database, user = User, password = Password)
#
# DbPool = createDbPool()

class _DbPools():


    __DbPools = None

    @staticmethod
    def getDbPools(DB_Postgres_Settings, force_to_reload=False):
        if _DbPools.__DbPools and not force_to_reload:
            return _DbPools.__DbPools
        _DbPools.__DbPools = {}
        for key, setting in DB_Postgres_Settings.items():
            cur_DbPool = _DbPool(host=setting.Host, port=setting.Port,
                                 database=setting.Database, user=setting.User,
                                 password=setting.Password)
            if cur_DbPool:
                _DbPools.__DbPools[key] = cur_DbPool
        return _DbPools.__DbPools


# 仅做测试样例用，尽量不要在这里使用，应该在自己的程序中设置自己的DB_Postgres_Settings，然后创建自己的DbPools
if __name__ == "__main__":
    from loongtian.util.db.postgres.db_postgres_settings import *

    DbPools = _DbPools.getDbPools(DB_Postgres_Settings)
