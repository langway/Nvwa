#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase
import uuid
import loongtian.util.helper.timeHelper as timeHelper
from loongtian.nvwa.tools.db import DbPools

from loongtian.nvwa.models.baseEntity import BaseEntity

class MyEntity(BaseEntity):
    __databasename__ = "nvwa"  # 所在数据库。
    __tablename__ = "test"  # 所在表。与Flask统一

    primaryKey = ("pkId", "pkUuid")
    columns = ("colNone", "colInt", "colString", "colBool", "colNull","colList","status")
    jsonColumns=["colList"] # 需要用json解析的字段，一般都为text字段，创建(create)、更新(update)，需要解析为json，读取(retrive)时需要从json解析为对象
    retrieveColumns=("pkId", "pkUuid")
    def __init__(self,memory=None):
        super(MyEntity, self).__init__(memory=memory)
        self.pkId = str(uuid.uuid1()).replace("-", "")
        self.pkUuid = str(uuid.uuid1()).replace("-", "")

class TestBaseEntity(TestCase):
    def setUp(self):
        print ("----setUp----")
        try:
            DbPools["nvwa"].executeSQL("drop table test")
        except:
            pass

        DbPools["nvwa"].executeSQL("""
        CREATE TABLE test(
            pkId char(32),
            pkUuid char(32),
            colNone varchar(255),
            colInt int,
            colString varchar(255),
            colBool boolean,
            colNull text,
            colList text,
            updatetime timestamp,
            status int,
            PRIMARY KEY (pkId, pkUuid)
        );""")


        from loongtian.nvwa.organs.brain import Brain
        brain = Brain()

        self.MemoryCentral=brain.MemoryCentral

        self.entity = MyEntity(self.MemoryCentral)

    def test_id(self):
        print("----test_id----")
        print(self.entity.id)

    def test__getId(self):
        print("----test__getId----")
        print(MyEntity._getId(self.entity))

    def test_getIdAndType(self):
        print("----test_getIdAndType----")
        print(MyEntity.getIdAndType(self.entity))

    def test_createNewUuid(self):
        print("----test_createNewUuid----")
        print(MyEntity.createNewUuid())

    def test_create(self):
        print("----test_create----")
        self.entity.colNone = None
        self.entity.colInt = 123
        self.entity.colString = timeHelper.getNow() #BaseEntity.Command("now()")
        self.entity.colBool = True
        self.entity.colList=[1.2,"testString","test_unicode",set([2.3,("a","e",6)])]
        created_entity = self.entity.create(checkExist=True,recordInDB=True) # 第一次写到记忆中枢及数据库
        self.assertIsNotNone(self.entity)
        self.assertIsNotNone(self.entity.pkId)
        self.assertIsNotNone(self.entity.pkUuid)
        self.assertEqual(id(self.entity), id(created_entity))
        # print(Json.obj2json(self.entity, False))

        self.entity = self.entity.create(checkExist=True,recordInDB=False)  # 再次创建，应该是记忆中枢中的
        self.entity = self.entity.create(checkExist=True,recordInDB=True)  # 再次创建，强制写到数据库，这里会通过记忆中枢取出根据上面字段（pkId，_id）查找出的对象，所以后面会出现self.entity与create相同的情况
        self.assertIsNotNone(self.entity)
        self.assertIsNotNone(self.entity.pkId)
        self.assertIsNotNone(self.entity.pkUuid)
        self.assertEqual(id(self.entity), id(created_entity))

        create = MyEntity(self.MemoryCentral)
        create.pkId=self.entity.pkId
        create.pkUuid=self.entity.pkUuid
        create.colNone = self.entity.colNone
        create.colInt = self.entity.colInt
        create.colString = self.entity.colString
        create.colBool = self.entity.colBool
        create = create.create(checkExist=False,recordInDB=True)
        self.assertEqual(self.entity.pkId, create.pkId)
        self.assertEqual(self.entity.pkUuid, create.pkUuid)
        self.assertEqual(id(self.entity), id(create))

        create = create.create(recordInDB=True)
        self.assertEqual(self.entity.pkId, create.pkId)
        self.assertEqual(self.entity.pkUuid, create.pkUuid)
        self.assertEqual(id(self.entity), id(create))

        create = MyEntity(self.MemoryCentral)
        create.colNone = self.entity.colNone
        create.colInt = self.entity.colInt
        create.colString = self.entity.colString
        create.colBool = self.entity.colBool
        create = create.create(checkExist=False)  # 这里会在数据库中创建新的对象，所以后面会出现self.entity与create不相同的情况
        self.assertNotEqual(self.entity.pkId, create.pkId)
        self.assertNotEqual(self.entity.pkUuid, create.pkUuid)
        self.assertNotEqual(id(self.entity), id(create))


    def test_getByColumnsInDB(self):
        print ("----test_getByColumnsInDB----")
        self.entity.colNone = None
        self.entity.colInt = 987
        self.entity.colString = "null"
        self.entity.colBool = False
        self.entity = self.entity.create()
        retrieve = MyEntity(self.MemoryCentral)
        retrieve.colNone = self.entity.colNone
        retrieve.colInt = self.entity.colInt
        retrieve.colString = self.entity.colString
        # getByColumnsInDB.colBool = self.entity.colBool
        retrieve = retrieve.getByColumnsInDB(useRetrieveColumns=False) # 根据其他值来查找
        self.assertIsNotNone(retrieve)
        self.assertIsNotNone(retrieve.pkId)
        self.assertIsNotNone(retrieve.pkUuid)
        self.assertIsNotNone(retrieve.colInt)
        self.assertIsNotNone(retrieve.colString)
        self.assertIsNotNone(retrieve.colBool)
        # print (Json.obj2json(retrieve, False))
        retrieve.colBool = True
        retrieve = retrieve.getByColumnsInDB(useRetrieveColumns=False) # 根据其他值来查找，增加了colBool，但与数据库中不相等，所以查不到
        self.assertIsNone(retrieve)

        retrieve = MyEntity(self.MemoryCentral)
        retrieve.colNone = self.entity.colNone
        retrieve.colInt = self.entity.colInt
        retrieve.colString = self.entity.colString
        retrieve.colBool=self.entity.colBool
        retrieve = retrieve.getByColumnsInDB() # 根据retrieveColumns来查找，所以查不到
        self.assertIsNone(retrieve)


    def test_getById(self):

        temp=None
        for i in range(0, 100):
            temp = MyEntity(self.MemoryCentral)
            temp.colInt = i
            temp.colString = "Hello, I'm Python."
            temp.create()

        retrived=temp.getByIdInMemory()
        self.assertIsNotNone(retrived)
        retrived=temp.getByIdInDB()
        self.assertEqual(99,retrived.colInt)


    def test_getOne(self):
        print ("----test_getOne----")
        self.entity.colNone = None
        self.entity.colInt = 987
        self.entity.colString = "null"
        self.entity.colBool = False
        self.entity.create()
        # 从内存取
        findOne = MyEntity.getOne(pkId = self.entity.pkId, pkUuid = self.entity.pkUuid)
        self.assertEqual(findOne.colInt,self.entity.colInt)
        self.assertEqual(findOne.colString,self.entity.colString)
        self.assertEqual(findOne.colBool,self.entity.colBool)

        # 从数据库取
        findOne = MyEntity.getOneInDB(pkId=self.entity.pkId, pkUuid=self.entity.pkUuid)
        self.assertEqual(findOne.colInt, self.entity.colInt)
        self.assertEqual(findOne.colString, self.entity.colString)
        self.assertEqual(findOne.colBool, self.entity.colBool)

    def test_getAllByInDB(self):
        print ("----test_getAllByInDB----")
        for i in range(0, 10):
            temp = MyEntity(self.MemoryCentral)
            temp.colInt = i
            temp.colString = "Hello, I'm Python."
            temp.create()

        # colNo用于验证鲁棒性
        findAll = MyEntity.getAllByConditionsInDB(memory=self.MemoryCentral,colString ="Hello, I'm Python.", colNo = 123, colNone = None)
        self.assertEqual(10, len(findAll))
        self.assertEqual(0, findAll[0].colInt)
        find = MyEntity.getAllByConditionsInDB(memory=self.MemoryCentral,limit = 5, offset = 2, colString ="Hello, I'm Python.", colNo = 123, colNone = None)
        self.assertEqual(5, len(find))
        self.assertEqual(4, find[2].colInt)

    def test_getAllLikeByInDB(self):
        print ("----test_getAllLikeByInDB----")
        for i in range(0, 10):
            temp = MyEntity(self.MemoryCentral)
            temp.colInt = i
            temp.colString = "Hello, I'm Python No.%d." % i
            temp.create()

        findAll = MyEntity.getAllLikeByStartMiddleEndInDB(attributeName="colString", start="Hello, I'm ")
        self.assertEqual(10, len(findAll))
        self.assertEqual(0, findAll[0].colInt)

        findAll = MyEntity.getAllLikeByStartMiddleEndInDB(attributeName="colString", end=".")
        self.assertEqual(10, len(findAll))
        self.assertEqual(0, findAll[0].colInt)

        findAll = MyEntity.getAllLikeByStartMiddleEndInDB(attributeName="colString", middles=["Python No."])
        self.assertEqual(10, len(findAll))
        self.assertEqual(0, findAll[0].colInt)

        findAll = MyEntity.getAllLikeByStartMiddleEndInDB(attributeName="colString", end="3.")
        self.assertIs(type(findAll),MyEntity)
        self.assertEqual(3, findAll.colInt)

    def test_getByIds(self):
        print ("----test_getByIds----")
        pk_ids = []
        ids = []
        double_ids = []
        for i in range(0, 100):
            temp = MyEntity(self.MemoryCentral)
            temp.colInt = i
            temp.colString = "Hello, I'm Python."
            temp.create()
            pk_ids.append(temp.pkId) # 双pk，尽量不要出现在这种情况
            ids.append(temp.id)# 双pk，尽量不要出现在这种情况
            double_ids.append({"pkId" : temp.pkId, "pkUuid" : temp.pkUuid})
        findIn = MyEntity.getByIds(pk_ids)
        self.assertEqual(100, len(findIn))

        findIn = MyEntity.getByIds(ids)
        self.assertIsNone(findIn)

        findIn = MyEntity.getByIds(double_ids)
        self.assertEqual(100, len(findIn))


    def testUpdate(self):
        print ("----testUpdate----")
        self.entity.colNone = None
        self.entity.colInt = 987
        self.entity.colString = "null"
        self.entity.colBool = False
        self.entity = self.entity.create()
        self.entity.colInt = 258
        self.entity.colString = None
        self.entity.colNone = "I'm Tester."
        self.entity = self.entity.update()
        self.assertIsNotNone(self.entity)
        findOne = MyEntity.getOneInDB(pkId = self.entity.pkId, pkUuid = self.entity.pkUuid)
        self.assertEqual(258, findOne.colInt)
        self.assertEqual(None, findOne.colString)
        self.assertEqual("I'm Tester.", findOne.colNone)
        # print (Json.obj2json(findOne, False))

    def testUpdateAttributeValue(self):
        print ("----testUpdateAttributeValue----")
        self.entity.colNone = None
        self.entity.colInt = 987
        self.entity.colString = "null"
        self.entity.colBool = False
        self.entity = self.entity.create()
        self.entity.colInt = 258
        self.entity.colString = None
        self.entity.colNone = "I'm Tester."
        self.entity = self.entity.updateAttributeValues(colInt=258,colString=None,colList=set([2.3,("a","e",6)]),colNone=self.entity.colNone)
        self.assertIsNotNone(self.entity)
        findOne = MyEntity.getOneInDB(pkId = self.entity.pkId, pkUuid = self.entity.pkUuid)
        self.assertEqual(258, findOne.colInt)
        self.assertEqual(None, findOne.colString)
        self.assertEqual("I'm Tester.", findOne.colNone)
        self.assertEqual(set([2.3,("a","e",6)]), findOne.colList)
        # print (Json.obj2json(findOne, False))

    def testDelete(self):
        print ("----testDelete----")
        self.entity.colNone = None
        self.entity.colInt = 987
        self.entity.colString = "null"
        self.entity.colBool = False
        self.entity = self.entity.create()
        self.entity = self.entity.delete()
        self.assertIsNotNone(self.entity)
        findAll = MyEntity.getAllByConditionsInDB(memory=self.MemoryCentral,pkId = self.entity.pkId, pkUuid = self.entity.pkUuid)
        self.assertEqual(findAll.status,0)
        self.entity._physicalDelete()
        findAll = MyEntity.getAllByConditionsInDB(memory=self.MemoryCentral,pkId = self.entity.pkId, pkUuid = self.entity.pkUuid)
        self.assertIsNone(findAll)


    #
    # def testRetrieveByBasicColumns(self):
    #     print ("----testRetrieveByBasicColumns----")
    #     temp=None
    #     for i in range(0, 10):
    #         temp = MyEntity()
    #         temp.colInt = i
    #         temp.colString = "Hello, I'm Python."
    #         temp.create()
    #     findAll = temp.retrieveByBasicColumns()
    #     print(findAll)


    def tearDown(self):
        print ("----tearDown----")
        DbPools["nvwa"].executeSQL("drop table test")


