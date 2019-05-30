#!/usr/bin/env python
# coding: utf-8

import random
from unittest import TestCase

from loongtian.nvwa.tools.db import DbPools


class TestDbConnection(TestCase):
    def setUp(self):
        print("----setUp----")
        DbPools["nvwa"].executeSQL("""
        CREATE TABLE test(
            a int,
            b varchar(255)
        );""")

    def testSize(self):
        print("----testSize----")
        self.assertEqual(10, DbPools["nvwa"].size(), None)
        print("MaxConnectiosSize = ", DbPools["nvwa"].size())
    
    def testGetRowCount(self):
        print("----testGetRowCount----")
        sql = []
        for i in range(0, random.randint(10, 100)):
            rdm = random.randint(1, 100)
            sql.append("insert into test (a, b) values (%s, '%s')" % (rdm, "我就是一个测试"))
        DbPools["nvwa"].executeSQL(sql)
        print("insert受影响的行数：", DbPools["nvwa"].getRowCount())
        result = DbPools["nvwa"].executeSQL("select * from test", fetchone = True)
        for row in result:
            for column in row.items():
               print("{", column[0], ":", column[1], "}")
        print("select受影响的行数：", DbPools["nvwa"].getRowCount())
        DbPools["nvwa"].executeSQL("delete from test")
        print("delete受影响的行数：", DbPools["nvwa"].getRowCount())
    
    def testExecuteSQL(self):
        print("----testExecuteSQL----")
        sql = []
        for i in range(0, random.randint(10, 100)):
            rdm = random.randint(1, 100)
            sql.append("insert into test (a, b) values (%s, '%s')" % (rdm, "No.:" + str(rdm)))
        DbPools["nvwa"].executeSQL(sql)
        result = DbPools["nvwa"].executeSQL("select * from test", fetchone = False)
        for row in result:
            print(str(row))
        print("select受影响的行数：", DbPools["nvwa"].getRowCount())
        
    def tearDown(self):
        print("----tearDown----")
        DbPools["nvwa"].executeSQL("drop table test;")
