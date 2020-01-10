#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

import uuid
from psycopg2 import IntegrityError

from loongtian.nvwa.tools.db import DbPools
from loongtian.util.helper import jsonplus
from loongtian.util.log import logger

from loongtian.nvwa import settings
from loongtian.nvwa.models.enum import ObjType, DirectionType, WhereRelation

from loongtian.nvwa.organs.character import Character

# debugCounter = {}  # 调试用计数器


class BaseEntity(object):
    """
    基础实体，主要作用是标识女娲实体类。
    其它女娲实体类要继承这个基础实体类。
    :parameter
    :attribute
    __tablename__ 模型对应的表名
    primaryKey 模型对应的主键
    cloumns 模型对应的非主键的列:
    status:状态; 0-不可用(逻辑删除);200-正常;800-不可遗忘
    createtime:创建时间。（使用trigger）
    updatetime:更新时间。（使用trigger）
    lasttime:最后使用时间。（使用trigger）
    """
    __databasename__ = None  # 所在数据库。
    __tablename__ = None  # 所在表。与Flask统一
    primaryKey = []
    columns = [
        "createrid",
        "createtime",
        "updatetime",
        "lasttime",
        "status",
    ]  # # 全部字段。"createtime","updatetime","lasttime"用来进行与时间有关操作的列（属性），例如遗忘等（使用trigger）。
    jsonColumns = []  # 需要用json解析的字段，一般都为text字段，创建(create)、更新(update)，需要解析为json，读取(retrive)时需要从json解析为对象
    retrieveColumns = []  # 查询时需要使用的字段

    isChainedObject = False  # 是否是链式对象的标记（metaNet、Knowledge等），
    # 用以在删除（逻辑、物理）时进行循环操作，
    # 例如：[[中国,人民],解放军]，根据中国 删除[中国,人民]时，还要删除[[中国,人民],解放军]

    directionInLayer = DirectionType.UNKNOWN
    upperLimitation = None  # 在上一层其他对象的分层中，包含的对象类型、数量限制，
    # 例如，MetaNet只能有一个下层对象MetaData，一个下层对象Knowledge，没有上层对象
    # MetaData 的上一层对象为MetaNet[多个，下一层对象为RealObject[多个]
    # 其格式为：{对象类型:数量限定}，其中数量限定为<=0 (一般为-1）时，相当于不限

    lowerLimitation = None  # 在下一层其他对象的分层中，包含的对象类型、数量限制，
    # 例如，MetaNet只能有一个下层对象MetaData，一个下层对象Knowledge，没有上层对象
    # MetaData 的上一层对象为MetaNet[多个，下一层对象为RealObject[多个]
    # 其格式为：{对象类型:数量限定}，其中数量限定为<=0 (一般为-1）时，相当于不限
    weightAttribName = "weight"

    def __init__(self, id=None,
                 createrid='',
                 createtime=None, updatetime=None, lasttime=None,
                 status=200,  # 状态; 0-不可用(逻辑删除);200-正常;800-不可遗忘
                 memory=None):
        """
        初始化函数
        :param id: 供内部使用的id，需要在子类中与具体的id挂钩，例如：元数据中，self.id==self.id
        :param createtime: 创建时间
        :param updatetime: 更新时间
        :param lasttime: 最近访问时间
        :param status:状态; 0-不可用(逻辑删除);200-正常;800-不可遗忘
        """
        # 检查参数
        if self.__tablename__ is None:
            raise Exception("\"__tablename__\" attribute is required, and isn't None.")
        if self.primaryKey is None and self.columns is None:
            raise Exception("\"primaryKey\" or \"columns\" has at least one not None.")
        # id属性
        if id is None:
            self.id = str(BaseEntity.createNewUuid())
        else:
            self.id = str(id)

        self.type = ObjType.UNKNOWN # 总是返回UNKNOWN类型

        self.createrid = createrid
        self.createtime = createtime
        self.updatetime = updatetime
        self.lasttime = lasttime
        self.status = status  # 状态; 0-不可用(逻辑删除);200-正常;800-不可遗忘

        self.MemoryCentral = memory  # 记录当前对象的记忆区，便于直接从记忆区取对象而不用每次从数据库中取
        self.Layers = Layers(self)  # 关联所有对于分层对象操作的封装类

        self.Observers = Observers(self)
        # ####################################
        #      下面为运行时数据
        # ####################################

        self._UpperEntities = None  # 上一层对象。格式为：UpperObjs
        self._LowerEntities = None  # 下一层对象。格式为：LowerObjs

        self._isInDB = False  # 是否从数据库中取出的标记
        self._isInWorkingMemory = False  # 是否保存在工作（临时）记忆区
        self._isInPersistentMemory = False  # 是否保存在持久记忆区
        self._isNewCreated = False  # 是否是新建对象的标记
        self._isGetByConflictDBColumns = False  # 是否根据“重复键违反唯一约束”取得数据库中的对象

        # self._isMemoryUseDoubleKeyDict = False # 内存之中存储是否使用双键字典。
        #                                        # 女娲系统的metanet、knowledge、layer的内存存储、查找都使用双键字典

    @staticmethod
    def createNewUuid():
        """
        创建一个新的uuid
        :return:
        """
        return str(uuid.uuid1()).replace("-", "")

    @staticmethod
    def _getId(entity):
        """
        取得对象的Id。
        根据entityItem._id，或 如果有多个primaryKey，拼接之
        :param entity:BaseEntity及其继承类，或 Id字符串
        :return:
        """
        if not entity:
            return u""

        if isinstance(entity, str):
            return entity

        if hasattr(entity, "id"):
            if entity.id:  # 如果已经有了，直接返回结果
                return entity.id

        if not isinstance(entity, BaseEntity):
            return None

        _id = None
        if len(entity.primaryKey) == 1:
            if hasattr(entity, entity.primaryKey[0]):
                _id = str(getattr(entity, entity.primaryKey[0]))
        else:
            _id = u""
            for key in entity.primaryKey:
                if hasattr(entity, key) and getattr(entity, key):
                    _id += str(getattr(entity, key))

        if not _id:
            raise Exception("无法取得Id，item类型：%s" % (type(entity)))

        entity._id = _id
        return _id

    @staticmethod
    def getIdAndType(entity):
        """
        取得对象的id及type
        :param entity:
        :return:_id,_type
        """
        error_msg = "无法取得对象的id及type，对象应为MetaData、MetaNet、RealObject、Knowledge、Layer或[sid,utype]\\(sid,utype)，当前类型错误："
        if isinstance(entity, list) or isinstance(entity, tuple):
            _id = entity[0]
            _type = entity[1]
        elif isinstance(entity, BaseEntity):
            try:
                _id = entity.id
                _type = entity.getType()
            except Exception as e:
                raise Exception(error_msg + str(type(entity)))
        else:
            raise Exception(error_msg + str(type(entity)))

        return _id, _type

    @staticmethod
    def getParamer(param, pythonToSQL=True):
        """
        Python类型转换成SQL语句
        :rawParam param: 参数
        :rawParam pythonToSQL: True:从python对象转化成sql字符串;False:
        :return: SQL字符串或Python字符串
        """
        if pythonToSQL:  # 从python对象转化成sql字符串
            if param is None:
                return "null"
            elif not isinstance(param, str):
                param = str(param)

            param = param.replace("'", "\\'")
            param = "'%s'" % param
            if param.find("\\"):
                param = "E" + param

        else:  # 从sql字符串转化成python对象
            if param == "'null'" or param == "\"null\"":
                return None
            elif isinstance(param, str) :
                param = "'%s'" % param.replace("'", "\\'")

            param = jsonplus.dumps(param)

        return param

    def _checkPrimaryKey(self, vars):
        for pk in self.primaryKey:
            if not pk in vars:
                raise Exception("Insert \"%s(pk)\" is Empty!" % pk)

    @classmethod
    def _resultToObject(cls, result):
        """
        将数据库中取出的数据转化为nvwa对象
        :rawParam result:
        :return:
        """
        entities = []
        for dct in result:
            entity = cls()
            for attribute in cls.primaryKey:
                if attribute.lower() in dct:
                    value = dct[attribute.lower()]

                    if isinstance(value, str):
                        value = value.strip()

                    setattr(entity, attribute, value)
                    # entity.__dict__[attribute] = cls.getParamer(dct[attribute.endid()], pythonToSQL = False)
                    # exec ("entity.%s = %s" % (attribute, cls.getParamer(dct[attribute.endid()], pythonToSQL=False)))

            for attribute in cls.columns:
                if attribute.lower() in dct:
                    value = dct[attribute.lower()]
                    if not value is None:

                        if cls.jsonColumns.__contains__(attribute):  # 从json解析为对象
                            value = jsonplus.loads(value)
                    setattr(entity, attribute, value)
                    # exec("entity.%s = %s" % (attribute, cls.getParamer(dct[attribute.endid()], pythonToSQL = False)))

            # ##################################
            # 同步_id 与primaryKey（否则会出现不一致的情况）
            # ##################################
            if len(cls.primaryKey) == 1:
                entity.id = str(getattr(entity, cls.primaryKey[0]))
            elif len(cls.primaryKey) > 1:
                temp_id = u""
                for _primaryKey in cls.primaryKey:
                    temp_id += str(getattr(entity, _primaryKey)) + u"_"
                temp_id = temp_id.rstrip(u"_")
                entity.id = temp_id

            # 标记是从数据库中取出来的
            entity._isInDB = True
            # 标记不是新建对象
            entity._isNewCreated = False
            entities.append(entity)

        return entities

    def create(self, checkExist=True, recordInDB=True):
        """
        CRUD - Create
        :param checkExist:检查是否存在
        :param recordInDB:是否在数据库中创建（False返回自身，例如：自然语言的知识链（NL_Knowledge，奇数位为“下一个为”）就不需要在数据库中创建）
        :return: 返回建立的Entity。
        """
        self.notifySysOperation(self.create)
        result = None
        if checkExist:  # 保证同一性（避免重复及不相同）
            # 从内存或数据库中取得已存在的对象
            result = self.getExist(getAllByColumnsInDB=False)

        # 从内存或数据库中取不到，真正创建到数据库，并添加到内存
        # 从内存或数据库中取不到，真正创建到数据库，并添加到内存
        if result is None:
            if recordInDB and not self._isInDB:
                result = self._createInDB()
                if result and not result._isGetByConflictDBColumns:  # 根据重复键违反唯一约束取得已知对象
                    result._isNewCreated = True
            else:
                result = self


            # 添加到工作内存以便后续操作
            if result and result.id and self.MemoryCentral:
                self.MemoryCentral.WorkingMemory.addInMemory(result)
                result._isInWorkingMemory = True
        elif recordInDB and not result._isInDB:  # 可能内存中有，但数据库没有，需要创建到数据库
            # result=result._createInDB() # 不要赋值！！！这里仅仅是创建到数据库，否则会将数据库中重新取得的对象赋值result，出现内存对象不一致
            result._createInDB()

        if result:  # 记录MemoryCentral
            result.MemoryCentral = self.MemoryCentral

        return result

    def getExist(self, fromMemory=True, fromDB=True, getAllByColumnsInDB=False):
        """
        从内存或数据库中取得已存在的对象
        :return:
        """
        if fromMemory:  # 0、首先从内存中取
            result = self.getByIdInMemory()
            if result:
                return result
            # 根据系统定义查询时需要使用的字段取得对象
            result = self.getByRetrieveColumns(fromMemory=True, fromDB=False)
            if result:
                return result

        if not fromDB:  # 上面内存没取到，如果不从数据库中取，直接返回None
            return None

        # 1、内存之中取不到，从数据库中取
        # 根据Id字段取得对象
        result = self.getByIdInDB()
        if result:
            return result

        # 根据系统定义查询时需要使用的字段取得对象
        result = self.getByRetrieveColumns(fromMemory=False, fromDB=True)
        if result:
            return result

        if getAllByColumnsInDB:
            result = self.getByColumnsInDB(useRetrieveColumns=False, recordInMemory=True)

        return result

    def _createInDB(self):
        """
        真正创建对象到数据库
        :return:
        """
        # self.__increaseDebugerCounter()
        cols_claus = []
        values_claus = []
        var = vars(self)
        self._checkPrimaryKey(var)

        result = None
        for col in list(self.primaryKey) + list(self.columns):
            if col in var:
                cols_claus.append("%s, " % col)
                value = var.get(col)
                if self.jsonColumns.__contains__(col):  # 是否需要使用使用json解析
                    value = jsonplus.dumps(value)

                values_claus.append("%s, " % self.getParamer(value))
        try:
            sql = "insert into %s(%s) values (%s)" % (
                BaseEntity._quote(self.__tablename__), "".join(cols_claus)[:-2], "".join(values_claus)[:-2])
            DbPools[self.__databasename__].executeSQL(sql)
            result = self

        except IntegrityError as e:
            # 有可能数据库已经存在，会抛出该错误，形式：
            # IntegrityError:
            # 1、错误:  重复键违反唯一约束"realobject_pkey"
            # DETAIL:  键值"(rid)=(R0000000000000000000000000000001)" 已经存在
            # 2、错误:  重复键违反唯一约束"metadata_mvalue_key"
            # DETAIL:  键值"(mvalue)=(组件)" 已经存在
            # 取得冲突的键-值
            conflictDBColumns = self._getConflictDBColumns(str(e))
            if conflictDBColumns:
                result = self.getAllByConditionsInDB(**conflictDBColumns)  # 不记录到内存中
                if result:
                    if not isinstance(result, BaseEntity):
                        raise Exception("根据唯一约束条件取得的对象不唯一！")

                    result._isGetByConflictDBColumns = True  # 标记根据重复键违反唯一约束取得对象
                    # 再从内存中取，保证同一性
                    if self.MemoryCentral:
                        self.__processDbResult(result,self.MemoryCentral)

                    if __debug__:
                        logger.debug("已存在该对象：%s,系统已取得数据库中对象" % str(e))
        except Exception as e:
            logger.error("创建对象到数据库错误！原因：%s" % e)
            result = None

        if result:
            result._isInDB = True
            # 记录MemoryCentral
            result.MemoryCentral = self.MemoryCentral
            # 添加到持久内存以便后续操作
            if result and result.id and self.MemoryCentral:
                self.MemoryCentral.PersistentMemory.addInMemory(result)

        return result

    @staticmethod
    def recordInDB(obj, memory=None):
        """
        将对象（单个/多个）记录到数据库
        :param obj:
        :return:
        """
        if obj is None:
            return
        if isinstance(obj, list) or isinstance(obj, tuple):
            for obj in obj:
                BaseEntity.recordInDB(obj, memory=memory)
        elif isinstance(obj, BaseEntity):
            if not obj._isInDB:
                obj.MemoryCentral=memory
                obj.create(checkExist=True, recordInDB=True)


    def _getConflictDBColumns(self, error_str):
        """
        取得冲突的键-值。处理IntegrityError:错误:  重复键违反唯一约束"realobject_pkey" DETAIL:  键值"(rid)=(R0000000000000000000000000000001)" 已经存在。
        :param error_str:
        :return:
        """
        import re
        p1 = re.compile(r'[(](.*?)[)=(](.*?)[)]', re.S)  # 最小匹配
        finds = re.findall(p1, error_str)
        if finds:
            results = {}
            for find in finds:
                column_name, column_value = find
                column_value = column_value[2:]  # 去掉左侧(
                # 这里还有一种情况：双键或多键，
                # 可能出现column_name='pkid, pkuuid'
                # column_value='0f6e0c903e3511e987ce40b89afe1ea2, 0f6e0c913e3511e9a40440b89afe1ea2'的情况，
                # 进一步分解
                if column_name.find(",") >= 0:
                    column_name = column_name.split(",")
                    column_value = column_value.split(",")
                    if len(column_name) != len(column_value):  # 两者必须相等
                        raise Exception("冲突的键-值是双键或多键，但键-值数量不等！")
                    for i in range(len(column_name)):
                        _column_name = self._get_column_name_in_columns_def(column_name[i].strip())
                        results[_column_name] = column_value[i].strip()
                else:
                    _column_name = self._get_column_name_in_columns_def(column_name.strip())
                    results[_column_name] = column_value.strip()
            return results
        return None

    def _get_column_name_in_columns_def(self, column_name):
        """
        有可能columns定义的是大写，但column_name可能是小写，这是要进行统一
        :param column_name:
        :return:
        """
        for _primarykey in self.primaryKey:
            if _primarykey.lower() == column_name.lower():
                return _primarykey
        for _column in self.columns:
            if _column.lower() == column_name.lower():
                return _column

        return None

    # def __increaseDebugerCounter(self):
    #     """
    #     [测试用] 增加调试用计数器。生产环境下注释掉
    #     :return:
    #     """
    #     if not __debug__:  # 测试用
    #         return
    #     cur_num = 0
    #     type_name = str(type(self)).split(".")[4].split("'")[0]
    #
    #     if type_name in debugCounter:
    #         cur_num = debugCounter.get(type_name) + 1
    #         debugCounter[type_name] = cur_num
    #     else:
    #         debugCounter[type_name] = cur_num
    #
    #     self._setId(type_name + str(cur_num))

    # def __decreaseDebugerCounter(self):
    #     """
    #     [测试用] 减少调试用计数器。生产环境下注释掉
    #     :return:
    #     """
    #     if not __debug__:  # 测试用，生产环境下注释掉
    #         return
    #     cur_num = 0
    #     type_name = str(type(self)).split(".")[4].split("'")[0]
    #
    #     if type_name in debugCounter:
    #         debugCounter[type_name] -= 1
    #
    #     self._setId(type_name + str(cur_num))

    def getByColumnsInDB(self, useRetrieveColumns=True, recordInMemory=True):
        """
        CRUD - Retrieve
        查找库中是否存在此Entity，不比较PrimaryKey。添加到内存
        :param useRetrieveColumns 是否使用规定的查询时需要使用的字段
        :param recordInMemory 是否记录到内存
        :return: 找到返回Entity，未找到返回None
        """
        wheres = {}
        curVars = vars(self)

        if useRetrieveColumns and not self.retrieveColumns is None and len(
                self.retrieveColumns) > 0:  # 如果规定了查询时需要使用的字段，使用之
            columns = self.retrieveColumns
        else:  # 如果没规定，使用全部字段作为查询条件
            columns = self.columns

        for column_name in columns:
            if self.jsonColumns.__contains__(column_name):  # 如果需要使用使用json解析，则不需要成为查询条件
                continue
            if column_name in curVars:
                column_value = curVars.get(column_name)
                if column_value and not isinstance(column_value, BaseEntity.Command):
                    wheres[column_name] = column_value
                # wheres.append("%s=%s and " % (column_name, self.getParamer(curVars.get(column_name))))

        if recordInMemory:
            return self.getAllByConditionsInDB(memory=self.MemoryCentral, **wheres)
        else:
            return self.getAllByConditionsInDB(**wheres)

    def getById(self):
        """
        CRUD - Retrieve从内存、数据库中取对象
        根据PrimaryKey查找内存、数据库中是否存在此Entity。
        :return: 找到返回Entity，未找到返回None
        """
        result = None
        # 首先从内存中取
        if self.id and self.MemoryCentral:
            result = self.getByIdInMemory()  # 首先从内存中取
        if not result:  # 如果内存中没取到，从数据库中取
            result = self.getByIdInDB()
        return result

    def getByIdInMemory(self):
        """
        CRUD - Retrieve从内存中取
        根据PrimaryKey查找内存中是否存在此Entity。
        :return: 找到返回Entity，未找到返回None
        """
        if self.id and self.MemoryCentral:
            return self.MemoryCentral.getByIdInMemory(self.id, type(self))
        return None

    def getByIdInDB(self):
        """
        CRUD - Retrieve
        根据PrimaryKey查找库中是否存在此Entity。
        :return: 找到返回Entity，未找到返回None
        """
        pks = {}
        for pk in self.primaryKey:
            pks[pk] = self.__getattribute__(pk)
        return self.getOneInDB(memory=self.MemoryCentral, **pks)

    def getByRetrieveColumns(self, fromMemory=True, fromDB=True):
        """
        根据系统定义查询时需要使用的字段取得对象
        :return:
        """
        if not self.retrieveColumns:
            return None
        # 先从内存中取
        if fromMemory and self.MemoryCentral:
            # 如果满足双键查询条件，使用双键查询内存
            # 女娲系统的metanet、knowledge、layer的内存存储、查找都使用双键字典
            if len(self.retrieveColumns) == 2:
                key1 = getattr(self, self.retrieveColumns[0])
                key2 = getattr(self, self.retrieveColumns[1])
                result = self.MemoryCentral.getByDoubleKeysInMemory(key1, key2, type(self))
                if result:
                    return result
            elif len(self.retrieveColumns) == 1:
                key = getattr(self, self.retrieveColumns[0])
                result = self.MemoryCentral.getBySingleKeyInMemory(key, type(self))
                if result:
                    return result
        if fromDB:  # 内存中取不到，从数据库中取
            result = self.getByColumnsInDB(useRetrieveColumns=True, recordInMemory=True)
            return result

        return None

    @classmethod
    def getOne(cls, memory=None, **pks):
        """
        静态方法，使用主键来查找唯一的对象。
        :rawParam pks: 查询参数（建议使用主键查询）。
        :return: BaseEntity的子对象。
        """
        result = cls.getOneInMemory(memory=memory, **pks)  # 首先从内存中取
        if not result:  # 如果内存中没取到，从数据库中取
            result = cls.getOneInDB(memory=memory, **pks)
        return result

    @classmethod
    def getOneInDB(cls, memory=None, **pks):
        """
        静态方法，使用主键来查找唯一的对象。
        :rawParam pks: 查询参数（建议使用主键查询）。
        :return: BaseEntity的子对象。
        """
        find = cls.getAllByConditionsInDB(limit=1, memory=memory, **pks)
        return find

    @classmethod
    def getOneInMemory(cls, memory=None, **pks):
        """
        静态方法，使用主键来查找唯一的对象。
        :rawParam pks: 查询参数（建议使用主键查询）。
        :return: BaseEntity的子对象。
        """
        return cls.getByIdsInMemory(memory, pks)

    @classmethod
    def getAllByRetriveColumnsInMemory(cls, memory=None, **retrieveColumnValues):
        """
        根据女娲模型类定义的retrieveColumns（查询时需要使用的字段）取得内存中的对象
        :return:
        """
        if not memory:
            return None
        if not cls.retrieveColumns:
            return
        if len(retrieveColumnValues) > 2:
            raise Exception("目前只能使用双键或单键查询！")
        # 如果满足双键查询条件，使用双键查询内存
        # 女娲系统的metanet、knowledge、layer的内存存储、查找都使用双键字典
        if len(cls.retrieveColumns) == 2:
            key1 = retrieveColumnValues.get(cls.retrieveColumns[0])
            key2 = retrieveColumnValues.get(cls.retrieveColumns[1])
            result = memory.getByDoubleKeysInMemory(key1, key2, cls)
            if result:
                if isinstance(result, dict):
                    return list(result.values())
                else:
                    return result
        elif len(cls.retrieveColumns) == 1:
            key = retrieveColumnValues.get(cls.retrieveColumns[0])
            result = memory.getBySingleKeyInMemory(key, cls)
            if result:
                return result

    @classmethod
    def getAllInDB(cls, memory=None):
        """
        取得数据库中所有实体类定义。
        :return:
        """
        return cls.getAllByConditionsInDB(memory=memory)

    # 标明对象类型的字段，用于查找子类型对象。在ObjType中进行枚举定义
    type_attributes = ["type", "stype", "etype", "start_type", "end_type"]

    @classmethod
    def getAllByConditionsInDB(cls, limit=None, offset=None,
                               memory=None, where_relation=WhereRelation.AND, **wheres):
        """
        [核心查询]静态方法，使用参数作为条件来查找多个对象（完全相等）。
        :param limit: 查寻几条记录。使用limit时需要同时使用offset。
        :param offset: 从第几条记录开始查询。使用offset时需要同时使用limit。
        :param memory 使用内存进行存储
        :param where_relation 查询参数之间的关系（and/or）
        :param wheres: 查询参数{属性名:属性值}。
        :return: [BaseEntity的子对象]。
        """
        wheres_claus = []
        limits_claus = ""
        if limit != None:
            if offset is None:
                offset = 0
            limits_claus = "limit %d offset %d" % (limit, offset)
        wheres.pop("limit", None)
        wheres.pop("offset", None)
        wheres.pop("memory", None)
        wheres.pop("where_relation", None)
        sub_results = []

        allColumns = list(cls.primaryKey) + list(cls.columns)
        if where_relation == WhereRelation.AND:
            where_relation = "and"
        elif where_relation == WhereRelation.OR:
            where_relation = "or"

        for attribute, value in wheres.items():

            if allColumns.count(attribute) != 0:
                if value is None:
                    wheres_claus.append("%s is null %s " % (attribute, where_relation))
                else:
                    wheres_claus.append("%s=%s %s " % (attribute, cls.getParamer(value), where_relation))

                    # 查找子类型。由于可能需要查找类似：所有的实际对象，要包括实对象、虚对象、动作等，所以需要查找其子类型
                    if attribute in cls.type_attributes:
                        sub_types = ObjType.getSubTypes(value)
                        if sub_types:
                            for sub_type in sub_types:
                                sub_wheres = dict(wheres)
                                sub_wheres[attribute] = sub_type
                                sub_result = cls.getAllByConditionsInDB(limit, offset, memory=memory, **sub_wheres)
                                if sub_result:
                                    if isinstance(sub_result, list):
                                        sub_results.extend(sub_result)
                                    else:
                                        sub_results.append(sub_result)
        results = None
        if len(wheres_claus) > 0:
            wheres_claus = "".join(wheres_claus)[:-5]  # 去掉后面的“ and ”
            results = cls._resultToObject(
                DbPools[cls.__databasename__].executeSQL(
                    "select * from %s where %s %s" % (
                        BaseEntity._quote(cls.__tablename__), wheres_claus, limits_claus)))
        else:
            results = cls._resultToObject(
                DbPools[cls.__databasename__].executeSQL(
                    "select * from %s %s" % (BaseEntity._quote(cls.__tablename__), limits_claus)))

        # 合并所有该类型的对象
        # 由于可能需要查找类似：所有的实际对象，要包括实对象、虚对象、动作等，所以需要查找其子类型
        results.extend(sub_results)

        if not results:
            return None

        # 最后处理结果
        return cls.__processDbResults(results, limit=limit, memory=memory)

    @classmethod
    def __processDbResults(cls, results, limit=None, memory=None):
        """
        最后处理结果，并添加到内存以便后续操作。
        :param results:
        :return:
        """
        if results is None or len(results) == 0:
            return None
        if limit is None or limit==-1:
            limit=len(results)

        if len(results) == 1:
            if limit<1:
                raise Exception("当前取得的数据库对象数量为1，超出数量限制%d" % limit)
            if memory:
                result=BaseEntity.__processDbResult(results[0],memory)
            else:
                result =results[0]
            return result
        else:
            if memory:  # 添加到内存以便后续操作
                final_results=[]
                for i in range(len(results)):
                    if i>limit:
                        break
                    result=BaseEntity.__processDbResult(results[i],memory)
                    final_results.append(result)
                results=final_results
            return results

    @classmethod
    def __processDbResult(cls, result, memory=None):

        if not isinstance(result,BaseEntity):
            return None
        if memory:  # 添加到内存以便后续操作
            # 记录MemoryCentral
            result.MemoryCentral = memory
            # 保证同一性
            result_in_memory = result.getExist(fromMemory=True, fromDB=False, getAllByColumnsInDB=False)
            if result_in_memory:
                result=result_in_memory
            else:
                memory.PersistentMemory.addInMemory(result)  # type(result))
                result._isInPersistentMemory = True

        result._isInDB = True
        result._isNewCreated = False
        return result

    @classmethod
    def getAllLikeByStartMiddleEndInDB(cls, attributeName, start=None, end=None, middles=None,
                                       limit=None, offset=None,
                                       seperator="%",
                                       memory=None):
        """
        取得指定属性（字段）中，所有以头部字符串开始，以尾部字符串结尾的实体类
        :param attributeName: 属性名称
        :param start: 头部字符串
        :param end: 尾部字符
        :param middles:中间字符（列表）
        :param limit: 查寻几条记录。使用limit时需要同时使用offset。
        :param offset: 从第几条记录开始查询。使用offset时需要同时使用limit。
        :param recordInMemory 使用内存进行存储
        :return:
        """
        if start is None and end is None and middles is None:
            raise Exception("至少提供头部、中部、尾部之中一个参数！")
        if start:
            pattern = cls.getLikePattern(start,seperator)
        else:
            pattern = "%"

        if middles:
            pattern += "%"
            for middle in middles:
                if not middle:
                    continue
                pattern += cls.getLikePattern(middle,seperator)
                if seperator:
                    pattern += seperator
            pattern += "%"
        # else: # 不应该加%，否则会查询出其他结果
        #     pattern += "%"

        if end:
            pattern += cls.getLikePattern(end,seperator)
        else:
            pattern += "%"

        while pattern.find("%%") > 0:
            pattern = pattern.replace("%%", "%")

        pattern = pattern.replace("[,", "[")
        pattern = pattern.replace(",]", "]")
        # SELECT * FROM tbl_knowledge WHERE s_chain LIKE '[R1,%,R3]'
        # raise Exception("正则表达式错误！")
        return cls.getAllLikeByInDB(limit, offset, memory=memory, **{attributeName: pattern})

    @classmethod
    def getLikePattern(cls, obj,seperator="%"):
        """
        取得对象的like查询的pattern
        :param obj:
        :return:
        """
        pattern = ""
        if isinstance(obj, BaseEntity):
            pattern = "\"%s\"" % cls._getId(obj)
        elif isinstance(obj, list):
            for _obj in obj:  # todo 这里不对
                child_pattern = cls.getLikePattern(_obj)
                if child_pattern:
                    pattern += child_pattern
                    if seperator:
                        pattern+=seperator
        elif isinstance(obj, str):
            pattern += obj

        if seperator:
            pattern=pattern.rstrip(seperator)
        return pattern

    @classmethod
    def getAllLikeByInDB(cls, limit=None, offset=None, memory=None, **attributeValues):
        """
        静态方法，使用参数来查找多个对象（相似查询）。
        :param limit: 查寻几条记录。使用limit时需要同时使用offset。
        :param offset: 从第几条记录开始查询。使用offset时需要同时使用limit。
        :param memory 使用内存进行存储
        :param attributeValues: 查询参数{属性名:属性值}，属性值为正则表达式。
        :return: [BaseEntity的子对象]。
        """
        wheres_claus = []
        limits_claus = ""
        if limit != None:
            if offset is None:
                offset = 0
            limits_claus = "limit %d offset %d" % (limit, offset)
        attributeValues.pop("limit", None)
        attributeValues.pop("offset", None)
        attributeValues.pop("memory", None)

        allColumns = list(cls.primaryKey) + list(cls.columns)
        for attribute, value in attributeValues.items():
            if allColumns.count(attribute) != 0:
                if value is None:
                    wheres_claus.append("%s is null and " % attribute)
                else:
                    wheres_claus.append("%s like %s and " % (attribute, cls.getParamer(value)))
        results = None
        if len(wheres_claus) > 0:
            wheres_claus = "".join(wheres_claus)[:-5]  # 去掉后面的“ and ”
            results = cls._resultToObject(DbPools[cls.__databasename__].executeSQL(
                "select * from %s where %s %s" % (BaseEntity._quote(cls.__tablename__), wheres_claus, limits_claus)))
        else:
            results = cls._resultToObject(DbPools[cls.__databasename__].executeSQL(
                "select * from %s %s" % (BaseEntity._quote(cls.__tablename__), limits_claus)))

        # 最后处理结果
        return cls.__processDbResults(results, limit=limit, memory=memory)

    @classmethod
    def getByIds(cls, ids, memory=None):
        """
        静态方法，传入一组[主键]，查询内存及数据库，返回这组主键对应的对象（列表）。
        :rawParam ids: [BaseEntity的子对象的主键]
            eg: [id1, id2, id3, ...] or [{pk1:id11, pk2:id12}, {pk1:id21, pk2:id22}, {pk1:id31, pk2:id32}, ...]
        :param memory 是否保存在内存
        :return: [BaseEntity的子对象]
        """
        results = cls.getByIdsInMemory(memory, ids)  # 首先从内存中取
        if not results or len(results):  # 如果内存中没取到，从数据库中取
            results = cls.getByIdsInDB(ids, memory)
        return results

    @classmethod
    def getByIdsInDB(cls, ids, memory=None):
        """
        静态方法，传入一组[主键]，返回这组主键对应的对象。
        :rawParam ids: [BaseEntity的子对象的主键]
            eg: [id1, id2, id3, ...] or [{pk1:id11, pk2:id12}, {pk1:id21, pk2:id22}, {pk1:id31, pk2:id32}, ...]
            eg: [rid:xxxx,rid:yyyy]
        :param memory 是否保存在内存
        :return: [BaseEntity的子对象]
        """
        if len(ids) == 0:
            return []
        if not isinstance(ids, list) and not isinstance(ids, tuple):
            ids = [ids]

        # 统一格式。[id1, id2, id3, ...] to [{pk:id1}, {pk:id2}, {pk:id3}, ...]
        if not isinstance(ids[0], dict):
            temp = []
            for pk in ids:
                temp.append({cls.primaryKey[0]: pk})
            ids = temp
        whereIn_claus = []
        for pk in ids:
            temp = []
            for atrrib, value in pk.items():
                temp.append("%s=%s and " % (atrrib, cls.getParamer(value)))
            whereIn_claus.append("(%s) or " % "".join(temp)[:-5])

        results = cls._resultToObject(DbPools[cls.__databasename__].executeSQL(
            "select * from %s where %s" % (BaseEntity._quote(cls.__tablename__), "".join(whereIn_claus)[:-4])))

        # 最后处理结果
        return cls.__processDbResults(results, limit=len(ids), memory=memory)

    @classmethod
    def getByIdsInMemory(cls, memory, ids):
        """
        静态方法，传入一组[主键]，返回这组主键对应的对象。
        :rawParam ids: [BaseEntity的子对象的主键]
            eg: [id1, id2, id3, ...] or [{pk1:id11, pk2:id12}, {pk1:id21, pk2:id22}, {pk1:id31, pk2:id32}, ...]
        :param memory 是否保存在内存
        :return: [BaseEntity的子对象]
        """
        if not memory:
            return None
        if len(ids) == 0:
            return []
        if not isinstance(ids, list) and not isinstance(ids, tuple):
            ids = [ids]

        # 统一格式。[id1, id2, id3, ...] to [{pk:id1}, {pk:id2}, {pk:id3}, ...]
        if not isinstance(ids[0], dict):
            temp = []
            for pk in ids:
                temp.append({cls.primaryKey[0]: pk})
            ids = temp
        __ids = []
        for pk in ids:
            __id = u""
            for atrrib, value in pk.items():
                __id += value
            __ids.append(__id)
        return memory.getByIdsInMemory(__ids, cls)

    def update(self):
        """
        CRUD - Update（全部属性）
        :return: 更改后的Entity
        """
        sets = {}
        wheres = {}
        var = vars(self)
        self._checkPrimaryKey(var)
        for where in self.primaryKey:
            wheres[where] = var.get(where)
        for col in self.columns:
            if col.startswith("_") or col.startswith("__"):  # 过滤掉私有变量
                continue
            if col in var:
                sets[col] = var.get(col)

        self.updateAllInDB(targetRowsAffected=1, wheres=wheres, **sets)

        return self

    def updateAttributeValues(self, **attributeValues):
        """
        CRUD - Update（指定属性）
        :return: 更改后的Entity
        """
        if not self._isInDB:
            return self
        wheres = {}
        var = vars(self)
        self._checkPrimaryKey(var)

        for where in self.primaryKey:
            wheres[where] = var.get(where)

        self.updateAllInDB(targetRowsAffected=1, wheres=wheres, **attributeValues)
        return self

    @classmethod
    def updateAllInDB(cls, targetRowsAffected=-1, wheres=None, **sets):
        """
        CRUD - Update
        :param targetRowsAffected: 更改后受影响的目标条数（默认为-1，小于等于0的情况下将不进行判断），如果不相等，将抛出错误
        :param wheres: 判断条件{属性:属性值}，例如：{startid:XXXXXXXXXXXXXXXXXXXX}。
                                    如果不提供，将更改全表的所有行。
        :param sets: 将要设置的属性{属性:属性值}
        :return:更改后受影响的条数
        """

        if sets is None or len(sets) < 0:
            raise Exception("必须提供将要更改的列及值！")

        # 拼接where_claus
        where_claus = []
        if not wheres is None and isinstance(wheres, dict) and len(wheres) > 0:
            for where, value in wheres.items():
                where_claus.append("%s=%s and " % (where, cls.getParamer(value)))

        # 拼接set_claus
        set_claus = []
        allColumns = cls.primaryKey + cls.columns
        for attribute, value in sets.items():
            if (attribute in allColumns) or (lambda: attribute.lower() == x.lower() for x in allColumns):  # 有可能大小写不一致
                if cls.jsonColumns.__contains__(attribute):
                    value = jsonplus.dumps(value)
                set_claus.append("%s=%s, " % (attribute, cls.getParamer(value)))

        if len(where_claus) > 0:
            DbPools[cls.__databasename__].executeSQL("update %s set %s where %s" % (
                BaseEntity._quote(cls.__tablename__), "".join(set_claus)[:-2], "".join(where_claus)[:-5]))
        else:
            DbPools[cls.__databasename__].executeSQL(
                "update %s set %s" % (BaseEntity._quote(cls.__tablename__), "".join(set_claus)[:-2]))

        # 如果规定了要检查的影响条数，检查是否正确
        affectedRowsNum = DbPools[cls.__databasename__].getRowCount()
        if targetRowsAffected > 0 and affectedRowsNum != targetRowsAffected:
            raise Exception("更改后受影响的条数(%d)错误！" % affectedRowsNum)
        else:
            logger.info("更改后受影响的条数(%d)。" % affectedRowsNum)

        return affectedRowsNum

    def updateWeight(self):
        """
        更新当前对象的权值（如果有的话）。
        由于经常需要更新权值，所以单独提出来
        :return:
        """
        if hasattr(self, self.weightAttribName):
            _weight = getattr(self, self.weightAttribName, None)
            return self.updateAttributeValues(weight=_weight)
        return False

    def delete(self, deleteRelatedLayers=True, deleteChainedObjs=True):
        """
        CRUD - Delete
        逻辑删除，非物理删除。
        :param deleteRelatedLayers: 是否删除所有相关联的Layer
        :param deleteChainedObjs: 是否删除链式对象（metaNet、Knowledge等）中的关联对象
        :return: 已删除的Entity
        """
        if self.status == 800:  # 不可遗忘
            return
        try:
            self.status = 0
            # 取得所有相关联的分层对象，并进行逻辑删除
            if deleteRelatedLayers:
                self.Layers.deleteRelatedLayers()

            # 如果是链式对象（metaNet、Knowledge等），还需对其关联对象进行处理
            # 在删除（逻辑、物理）时进行循环操作，
            # 例如：[[中国,人民],解放军]，根据中国 删除[中国,人民]时，还要删除[[中国,人民],解放军]
            if deleteChainedObjs and self.isChainedObject and self.id:
                # 根据查询字段=self.id进行删除，例如当前对象id=1，就要删除startid=1，endid=1的对象
                for column in self.retrieveColumns:
                    # 循环操作，直到删除干净
                    objs_in_chain = self.getAllByConditionsInDB(memory=self.MemoryCentral, **{column: self.id})
                    if objs_in_chain:
                        if isinstance(objs_in_chain, list):
                            for obj in objs_in_chain:
                                obj.delete()
                        elif isinstance(objs_in_chain, BaseEntity):
                            objs_in_chain.delete()

            self.updateAttributeValues(status=0)
        except Exception as e:
            raise Exception("逻辑删除对象失败，原因：%s" % str(e))
        return self

    @classmethod
    def deleteBy(cls, memory=None, **wheres):
        """
        根据条件进行逻辑删除
        :param wheres:
        :return:
        """
        try:
            entities = cls.getAllByConditionsInDB(memory=memory, **wheres)
            if entities:
                if isinstance(entities, list):
                    for entity in entities:
                        entity.delete()
                elif isinstance(entities, BaseEntity):
                    entities.delete()

        except Exception as e:
            raise Exception("逻辑删除对象失败，原因：%s" % str(e))

    @classmethod
    def deleteAll(cls, memory=None):
        """
        逻辑删除所有的对象（慎用！！！）
        :param wheres:
        :return:
        """
        try:
            entities = cls.getAllInDB(memory=memory)
            if entities:
                if isinstance(entities, list):
                    for entity in entities:  # 因为要循环删除每一条，所以不用删除其链条中其他对象
                        entity.delete(deleteChainedObjs=False)
                elif isinstance(entities, BaseEntity):
                    entities.delete()

        except Exception as e:
            raise Exception("逻辑删除对象失败，原因：%s" % str(e))

    def restore(self):
        """
        逻辑恢复（不删除），非物理创建。
        :return: 已恢复（不删除）的Entity
        """
        if self.status > 0:  # 正常/不可遗忘
            return
        try:
            self.status = 200
            self.updateAttributeValues(status=200)
        except Exception as e:
            raise Exception("恢复逻辑删除对象失败，原因：%s" % str(e))
        return self

    @classmethod
    def restoreBy(cls, **wheres):
        """
        根据条件进行逻辑恢复（不删除）
        :param wheres:
        :return:
        """
        try:
            cls.updateAllInDB(wheres=wheres, isdel=False)
        except Exception as e:
            raise Exception("逻辑恢复删除对象失败，原因：%s" % str(e))

    def setUnforgetable(self):
        """
        设置为不可遗忘
        :return:
        """
        self.status = 800
        self.updateAttributeValues(status=800)

    def _physicalDelete(self, recordInMemory=True, deleteRelatedLayers=True, deleteChainedObjs=True):
        """
        物理删除(根据PrimaryKey)，原则上由调度中枢调用。
        :param recordInMemory:是否从内存中删除
        :param deleteRelatedLayers: 是否删除所有相关联的Layer
        :param deleteChainedObjs: 是否删除链式对象（metaNet、Knowledge等）中的关联对象
        :return: 受影响的行数
        """
        if self.status == 800:  # 不可遗忘
            return
        try:
            self.status = 0

            # 取得所有相关联的Layer，并进行物理删除
            if deleteRelatedLayers:
                self.Layers._physicalDeleteRelatedLayers()

            # 如果是链式对象（metaNet、Knowledge等），需对其关联对象进行处理，删除所有引用本条对象的row
            # 在删除（物理、物理）时进行循环操作，
            # 例如：[[中国,人民],解放军]，根据中国 删除[中国,人民]时，还要删除[[中国,人民],解放军]
            if deleteChainedObjs and self.isChainedObject and self.id:
                # 根据查询字段=self.id进行删除，例如当前对象id=1，就要删除startid=1，endid=1的对象
                for column in self.retrieveColumns:
                    # 循环操作，直到删除干净
                    objs_in_chain = self.getAllByConditionsInDB(memory=self.MemoryCentral, **{column: self.id})
                    if objs_in_chain:
                        for obj in objs_in_chain:
                            obj._physicalDelete()

            wheres = {}
            var = vars(self)
            self._checkPrimaryKey(var)
            for where in list(self.primaryKey):
                value = var.get(where)
                if where in var and not isinstance(value, BaseEntity.Command):
                    if not value is None:
                        wheres[where] = value
                    else:
                        wheres[where] = None
            if recordInMemory:
                affectedRowsNum = self._physicalDeleteBy(targetRowsAffected=1, memory=self.MemoryCentral, **wheres)
            else:
                affectedRowsNum = self._physicalDeleteBy(targetRowsAffected=1, **wheres)
            return affectedRowsNum

        except Exception as e:
            raise Exception("物理删除对象失败，原因：%s" % str(e))

    @classmethod
    def _physicalDeleteAll(cls):
        """
        物理删除所有的对象（慎用！！！）
        :param wheres:
        :return:
        """
        if cls.__tablename__ in settings.db.tables.tablesShouldNotPhysicalDeleteAll:
            return

        try:
            entities = cls.getAllInDB()
            if entities:
                if isinstance(entities, list):
                    for entity in entities:  # 因为要循环删除每一条，所以不用删除其链条中其他对象
                        entity._physicalDelete(deleteChainedObjs=False)
                elif isinstance(entities, BaseEntity):
                    entities._physicalDelete(deleteChainedObjs=False)

        except Exception as e:
            raise Exception("物理删除对象失败，原因：%s" % str(e))

    @classmethod
    def _physicalDeleteBy(cls, targetRowsAffected=-1, memory=None, **wheres):
        """
        根据条件进行物理删除。原则上由调度中枢调用。
        :param targetRowsAffected: 规定的要检查的影响条数，检查是否正确
        :param memory:是否从内存中删除
        :param wheres: 查询条件，一般为{属性：属性值}
        :return:受影响的行数
        """
        wheres.pop("targetRowsAffected", None)
        wheres.pop("memory", None)
        wheres_clause = []

        # 先取得要删除的对象，以便后续处理
        waiting_deltions = cls.getAllByConditionsInDB(memory=memory, **wheres)

        if not waiting_deltions:  # 已经删除了，不再处理
            return -1
        # 拼接删除条件
        for where, value in wheres.items():  # + list(self.columns):
            if value is None:
                wheres_clause.append("%s is null and " % where)
            else:
                wheres_clause.append("%s=%s and " % (where, cls.getParamer(value)))

        # 从数据库删除
        if len(wheres_clause) > 0:
            DbPools[cls.__databasename__].executeSQL(
                "delete from %s where %s" % (BaseEntity._quote(cls.__tablename__), "".join(wheres_clause)[:-5]))
        else:
            DbPools[cls.__databasename__].executeSQL(["delete from %s " % BaseEntity._quote(cls.__tablename__), ])

        affectedRowsNum = DbPools[cls.__databasename__].getRowCount()
        # 如果规定了要检查的影响条数，检查是否正确
        if targetRowsAffected > 0 and affectedRowsNum != targetRowsAffected:
            raise Exception("删除后受影响的条数(%d)错误！应该为：%s" % (affectedRowsNum, targetRowsAffected))
        else:
            logger.info("删除后受影响的条数(%d)。" % affectedRowsNum)

        # 从内存中删除
        if waiting_deltions and memory:
            if isinstance(waiting_deltions, list):
                if len(waiting_deltions) == 1:
                    result = waiting_deltions[0]
                    if result.id:
                        memory.deleteByIdInMemory(result.id, type(result))
                else:
                    for result in waiting_deltions:
                        if result.id:
                            memory.deleteByIdInMemory(result.id, type(result))
            else:
                if isinstance(waiting_deltions, cls):
                    if waiting_deltions.id:
                        memory.deleteByIdInMemory(waiting_deltions.id, type(waiting_deltions))

        return affectedRowsNum

    @staticmethod
    def sortBy(li, attribName, reverse=True):
        """
        对集合中的元素根据attribName进行排序
        :param li:
        :param attribName:
        :param reverse:是否正序
        :return:
        """
        if li is None or not isinstance(li, list) or len(li) < 1:
            raise Exception("必须提供要排序的列表！参数错误！")
        if attribName is None or attribName == u"" or attribName == "":
            raise Exception("必须提供属性名称！参数错误！")
        if hasattr(li[0], attribName):
            raise Exception("当前列表元素没有%s属性！参数错误！" % attribName)

        try:
            import operator
        except ImportError:
            cmpfun = lambda x: x.__getattribute__(attribName)  # use a lambda if no operator module
        else:
            cmpfun = operator.attrgetter(attribName)  # use operator since it's faster than lambda

        li.sort(key=cmpfun, reverse=reverse)

    @staticmethod
    def sortByWeight(li, reverse=True):
        """
        对集合中的元素根据weight进行排序
        :param li:
        :param reverse:是否正序
        :return:
        """
        return BaseEntity.sortBy(li, BaseEntity.weightAttribName, reverse)

    def getType(self):
        """
        取得当前对象的类型。
        :return: 当前对象的类型。
        """
        return self.type

    def notifySysOperation(self,operation):
        """
        通知当前系统操作
        :return:
        """
        if self.MemoryCentral:
            pass
        logger.info(operation)

    def isKnownInDB(self):
        """
        是否在数据库中存在
        :return:
        """
        return self._isInDB

    def isKnownInMemory(self):
        """
        是否在内存中存在
        :return:
        """
        if self._isInDB:
            return True
        return self._isNewCreated

    @staticmethod
    def _quote(str):
        """
        postgre数据库需要在表名加双引号。
        :param str:
        :return:
        """

        return "\"" + str + "\""

    class Command(str):
        """
        SQL中的命令字符串
        eg:select now()
        """


class Layers(object):
    """
    所有对于分层对象操作的封装类。
    """

    def __init__(self, entity):
        """
        所有对于分层对象操作的封装类
        :param entity:
        """
        self.entity = entity

    def addUpper(self, upper,
                 weight=Character.Original_Link_Weight,
                 recordInDB=True, utype=None, ltype=None):
        """
        将上一层对象与当前对象的分层关系添加到内存及数据库
        :param upper:
        :param weight:
        :return:
        """
        if upper is None or not isinstance(upper, BaseEntity):
            return
        if weight is None:
            weight = Character.Original_Link_Weight

        if self.entity.upperLimitation is None:
            raise Exception(
                "无法添加上一层对象,当前对象规定不应该有上一层对象！")

        limitation = self.entity.upperLimitation.get(upper.getType())
        if limitation is None:
            raise Exception(
                "无法添加上一层对象，上一层对象可能的类型为:%s，当前对象对象类型为%s" % (self.entity.upperLimitation.keys(), upper.getType()))

        # 添加到内存
        result = self.addUpperInMemory(upper, weight, limitation)
        # 添加到数据库
        if recordInDB:
            return self.addUpperInDB(upper, weight, utype, ltype)

        return result

    def addUpperInMemory(self, upper, weight=Character.Original_Link_Weight, limitation=None):
        """
        将上一层对象与当前对象的分层关系添加到内存
        :param upper:
        :param weight:
        :param limitation: 数量限定
        :return:
        """
        if self.entity._UpperEntities is None:
            from loongtian.nvwa.runtime.relatedObjects import UpperObjs
            self.entity._UpperEntities = UpperObjs()
        if limitation <= 0:  # 这里未作数量限定，直接添加
            return self.entity._UpperEntities.add(upper, weight, self.entity)
        else:
            if len(self.entity._UpperEntities) < limitation:  # 数量小于限定，直接添加
                return self.entity._UpperEntities.add(upper, weight)
            else:
                raise Exception("当前对象的上一层对象限定为%d，无法继续添加！" % limitation)

    def addUpperInDB(self, upper, weight=Character.Original_Link_Weight, utype=None, ltype=None):
        """
        将上一层对象与当前对象的分层关系添加到数据库
        :param upper:
        :param weight:
        :return:
        """
        from loongtian.nvwa.models.layer import Layer
        return Layer.createByStartAndEndInDB(upper, self.entity,
                                             weight, utype, ltype,
                                             memory=self.entity.MemoryCentral)

    def addLower(self, lower, weight=Character.Original_Link_Weight, recordInDB=True, utype=None, ltype=None):
        """
        将下一层对象与当前对象的分层关系添加到内存及数据库
        :param lower:
        :param weight:
        :return:
        """
        if lower is None or not isinstance(lower, BaseEntity):
            return
        if weight is None:
            weight = Character.Original_Link_Weight

        if self.entity.lowerLimitation is None:
            raise Exception(
                "无法添加下一层对象,当前对象规定不应该有下一层对象！")

        limitation = self.entity.lowerLimitation.get(lower.getType())  # (self._processSubType(lower.getType()))
        if limitation is None:
            raise Exception(
                "无法添加下一层对象，下一层对象可能的类型为:%s，当前对象的对象类型为%s" % (self.entity.upperLimitation.keys(), lower.getType()))

        # 添加到内存
        result = self.addLowerInMemory(lower, weight, limitation)
        # 添加到数据库
        if recordInDB:
            return self.addLowerInDB(lower, weight, utype, ltype)
        return result

    def addLowerInMemory(self, lower, weight=Character.Original_Link_Weight, limitation=None):
        """
        将下一层对象与当前对象的分层关系添加到内存
        :param lower:
        :param weight:
        :return:
        """
        if self.entity._LowerEntities is None:
            from loongtian.nvwa.runtime.relatedObjects import LowerObjs
            self.entity._LowerEntities = LowerObjs()

        if limitation <= 0:  # 这里未作数量限定，直接添加
            return self.entity._LowerEntities.add(lower, weight, self.entity)
        else:
            if len(self.entity._LowerEntities) < limitation:  # 数量小于限定，直接添加
                return self.entity._LowerEntities.add(lower, weight, self.entity)
            else:
                raise Exception("当前对象的下一层对象数量限定为%d，无法继续添加！" % limitation)

    def addLowerInDB(self, lower,
                     weight=Character.Original_Link_Weight, utype=None, ltype=None):
        """
        将下一层对象与当前对象的分层关系添加到数据库
        :param lower:
        :param weight:
        :return:
        """
        from loongtian.nvwa.models.layer import Layer
        return Layer.createByStartAndEndInDB(self.entity, lower,
                                             weight, utype, ltype,
                                             memory=self.entity.MemoryCentral)

    def getLowerLayers(self):
        """
        取得当前对象的下一层所有layers
        :return:
        """
        from loongtian.nvwa.models.layer import Layer
        layers = Layer.getAllByConditionsInDB(startid=self.entity.id,
                                              memory=self.entity.MemoryCentral)
        return layers

    def getUpperLayers(self):
        """
        取得当前对象的上一层所有layers
        :return:
        """
        from loongtian.nvwa.models.layer import Layer
        layers = Layer.getAllByConditionsInDB(endid=self.entity.id,
                                              memory=self.entity.MemoryCentral)
        return layers

    def getUpperEntities(self):
        """
        取得当前对象的所有上一层对象
        :return:
        """
        if not self.entity._UpperEntities is None and len(self.entity._UpperEntities) > 0:
            self.checkLimitation(self.entity._UpperEntities, self.entity.upperLimitation, DirectionType.UPPER)
            return self.entity._UpperEntities
        from loongtian.nvwa.models.layer import Layer

        self.entity._UpperEntities = Layer.getStartsByEndInDB(self.entity, lazy_get=False,
                                                              memory=self.entity.MemoryCentral)
        self.checkLimitation(self.entity._UpperEntities, self.entity.upperLimitation, DirectionType.UPPER)
        return self.entity._UpperEntities

    def checkLimitation(self, ralatedObjects, limitation, direction=DirectionType.UNKNOWN):
        """
        检查当前对象的其他层对象是否符合类型限定、数量限定
        :param ralatedObjects:
        :param limitation:
        :param direction:
        :return:
        """
        if limitation is None:
            if direction == DirectionType.LOWER:
                raise Exception("当前对象不应该有下一层对象！")
            elif direction == DirectionType.UPPER:
                raise Exception("当前对象不应该有上一层对象")

        if ralatedObjects is None or len(ralatedObjects) <= 0:
            return
        for _type, limite in limitation.items():
            if limite <= 0:
                continue
            typed_objs = ralatedObjects.getObjsByType(_type)
            if typed_objs is None:
                continue
            if len(typed_objs) > limite:
                if direction == DirectionType.LOWER:
                    raise Exception("当前对象的下一层对象限定为%d，当前数量为%d！" % limitation, len(typed_objs))
                elif direction == DirectionType.UPPER:
                    raise Exception("当前对象的上一层对象限定为%d，当前数量为%d！" % limitation, len(typed_objs))

    def getUpperEntitiesByType(self, type=ObjType.UNKNOWN, lazy_get=False):
        """
        根据指定对象的类型，取得当前对象的所有上一层对象
        :param type:
        :return:
        """
        if type == ObjType.UNKNOWN:
            raise Exception("无法根据指定类型取得对应的上一层对象，type=ObjType.UNKNOWN！")
        uppers = None
        if not self.entity._UpperEntities is None and len(self.entity._UpperEntities) > 0:
            self.checkLimitation(self.entity._UpperEntities, self.entity.upperLimitation, DirectionType.UPPER)
            uppers = self.entity._UpperEntities.getObjsByType(type=type)
            if uppers:
                if isinstance(uppers, dict):
                    from loongtian.nvwa.runtime.relatedObjects import UpperObjs
                    temp_upper = UpperObjs()
                    for key, upper in uppers.items():
                        temp_upper.add(upper, weight=upper.weight, source=self.entity)
                    uppers = temp_upper

        if not uppers:
            from loongtian.nvwa.models.layer import Layer
            uppers = Layer.getTypedStartsByEndInDB(self.entity, start_type=type,
                                                   lazy_get=lazy_get,
                                                   memory=self.entity.MemoryCentral)
            if uppers:
                if self.entity._UpperEntities:
                    self.entity._UpperEntities.merge(uppers)
                else:
                    self.entity._UpperEntities = uppers

        self.checkLimitation(self.entity._UpperEntities, self.entity.upperLimitation, DirectionType.UPPER)
        return uppers

    def getLowerEntities(self):
        """
        取得当前对象的所有下一层对象
        :return:
        """
        if not self.entity._LowerEntities is None and len(self.entity._LowerEntities) > 0:
            self.checkLimitation(self.entity._LowerEntities, self.entity.lowerLimitation, DirectionType.LOWER)
            return self.entity._LowerEntities
        from loongtian.nvwa.models.layer import Layer

        self.entity._LowerEntities = Layer.getEndsByStartInDB(self.entity, lazy_get=False,
                                                              memory=self.entity.MemoryCentral)
        self.checkLimitation(self.entity._LowerEntities, self.entity.lowerLimitation, DirectionType.LOWER)
        return self.entity._LowerEntities

    def getLowerEntitiesByType(self, type=ObjType.UNKNOWN, lazy_get=False):
        """
        根据指定对象的类型，取得当前对象的所有下一层对象
        :param type:
        :return:
        """
        if type == ObjType.UNKNOWN:
            raise Exception("无法根据指定类型取得对应的下一层对象，type=ObjType.UNKNOWN！")

        lowers = None
        if not self.entity._LowerEntities is None and len(self.entity._LowerEntities) > 0:
            self.checkLimitation(self.entity._LowerEntities, self.entity.lowerLimitation, DirectionType.LOWER)
            lowers = self.entity._LowerEntities.getObjsByType(type=type)
            if lowers:
                if isinstance(lowers, dict):
                    from loongtian.nvwa.runtime.relatedObjects import LowerObjs
                    temp_lowers = LowerObjs()
                    for key, lower in lowers.items():
                        temp_lowers.add(lower, weight=lower.weight, source=self.entity)
                    lowers = temp_lowers

        if not lowers:
            from loongtian.nvwa.models.layer import Layer
            lowers = Layer.getTypedEndsByStartInDB(self.entity, end_type=type,
                                                   lazy_get=lazy_get,
                                                   memory=self.entity.MemoryCentral)
            if lowers:
                if self.entity._LowerEntities:
                    self.entity._LowerEntities.merge(lowers)
                else:
                    self.entity._LowerEntities = lowers
                self.checkLimitation(self.entity._LowerEntities, self.entity.lowerLimitation, DirectionType.LOWER)

        return lowers

    def hasUpper(self, upper):
        """
        查看当前对象是否有指定的上一层对象
        :param upper:
        :return:
        """
        return self.hasRelation(upper, self.entity)

    def hasLower(self, lower):
        """
        查看当前对象是否有指定的下一层对象
        :param lower:
        :return:
        """
        return self.hasRelation(self.entity, lower, memory=self.entity.MemoryCentral)

    @staticmethod
    def hasRelation(upper, lower, memory=None):
        """
        查看两个对象是否有分层关系
        :param upper:
        :param lower:
        :return:
        """
        from loongtian.nvwa.models.layer import Layer
        if Layer.getByStartAndEnd(upper, lower, lazy_get=True, memory=memory):
            return True
        return False

    def removeUpper(self, upper, recordInDB=True):
        """
        将上一层对象与当前对象的分层关系从内存及数据库移除（逻辑删除）
        :param upper:
        :param weight:
        :return:
        """
        self.removeUpperInMemory(upper)
        if recordInDB:
            return self.removeUpperInDB(upper)

    def removeUpperInMemory(self, upper):
        """
        将上一层对象与当前对象的分层关系从内存移除（逻辑删除）
        :param upper:
        :param weight:
        :return:
        """
        if self.entity._UpperEntities is None:
            return True

        return self.entity._UpperEntities.remove(upper)

    def removeUpperInDB(self, upper):
        """
        将上一层对象与当前对象的分层关系从数据库移除（逻辑删除）
        :param upper:
        :param weight:
        :return:
        """
        from loongtian.nvwa.models.layer import Layer
        return Layer.deleteByStartAndEnd(upper, self.entity)

    def removeLower(self, lower, recordInDB=True):
        """
        将下一层对象与当前对象的分层关系从内存及数据库移除（逻辑删除）
        :param lower:
        :param weight:
        :return:
        """
        self.removeLowerInMemory(lower)
        if recordInDB:
            return self.removeLowerInDB(lower)

    def removeLowerInMemory(self, lower):
        """
        将上一层对象与当前对象的分层关系从内存移除（逻辑删除）
        :param lower:
        :param weight:
        :return:
        """
        if self.entity._LowerEntities is None:
            return True

        return self.entity._LowerEntities.remove(lower)

    def removeLowerInDB(self, lower):
        """
        将上一层对象与当前对象的分层关系从数据库移除（逻辑删除）
        :param lower:
        :return:
        """
        from loongtian.nvwa.models.layer import Layer
        return Layer.deleteByStartAndEnd(self.entity, lower)

    def deleteRelatedLayers(self):
        """
        取得所有相关联的分层对象，并进行逻辑删除
        :return:
        """

        # 取得所有相关联的分层对象，并进行逻辑删除
        if self.entity.upperLimitation and len(self.entity.upperLimitation) > 0:
            uppers = self.getUpperLayers()
            if uppers:
                for upper in uppers:
                    upper.delete()
        if self.entity.lowerLimitation and len(self.entity.lowerLimitation) > 0:
            lowers = self.getLowerLayers()
            if lowers:
                for lower in lowers:
                    lower.delete()

    def _physicalDeleteRelatedLayers(self):
        """
        取得所有相关联的Layer，并进行物理删除
        :return:
        """

        if not self.entity.upperLimitation is None and len(self.entity.upperLimitation) > 0:
            uppers = self.getUpperLayers()
            if uppers:
                if isinstance(uppers, list):
                    for upper in uppers:
                        upper._physicalDelete()
                elif isinstance(uppers, BaseEntity):
                    uppers._physicalDelete()
        if not self.entity.lowerLimitation is None and len(self.entity.lowerLimitation) > 0:
            lowers = self.getLowerLayers()
            if lowers:
                if isinstance(lowers, list):
                    for lower in lowers:
                        lower._physicalDelete()
                elif isinstance(lowers, BaseEntity):
                    lowers._physicalDelete()

    def _physicalDeleteWithUpper(self, upper, recordInDB=True):
        """
        将上一层对象与当前对象的分层关系从内存及数据库移除（物理删除）
        :param upper:
        :param weight:
        :return:
        """
        self.removeUpperInMemory(upper)
        if recordInDB:
            return self._physicalDeleteWithUpperInDB(upper)

    def _physicalDeleteWithUpperInDB(self, upper):
        """
        将上一层对象添加到数据库
        :param upper:
        :return:
        """
        from loongtian.nvwa.models.layer import Layer
        return Layer._physicalDeleteByStartAndEnd(upper, self.entity)

    def _physicalDeleteWithLower(self, lower, recordInDB=True):
        """
        将上一层对象添加到内存及数据库
        :param lower:
        :param weight:
        :return:
        """
        self.removeLowerInMemory(lower)
        if recordInDB:
            return self._physicalDeleteWithLowerInDB(lower)

    def _physicalDeleteWithLowerInDB(self, lower):
        """
        将上一层对象添加到数据库
        :param lower:
        :param weight:
        :return:
        """
        from loongtian.nvwa.models.layer import Layer
        return Layer._physicalDeleteByStartAndEnd(self.entity, lower)


class LayerLimitation(object):
    """
    分层对象的限定关系
    """

    def __init__(self):
        """
        分层对象的限定关系
        """
        # super(Limitation,self).__init__()
        self.main = {}
        self.subs = {}

    def get(self, type):
        result = self.main.get(type)
        if result:
            return result
        return self.subs.get(type)

    def add(self, type, limit):
        if type >= 0 and type < 10:
            self.main[type] = limit
            subtypes = ObjType.getSubTypes(type)
            if subtypes:
                for subtype in subtypes:
                    self.add(subtype, limit)
        else:
            self.subs[type] = limit

    def pop(self, type):
        self.main.pop(type)
        self.subs.pop(type)

    def clean(self):
        self.main = {}
        self.subs = {}

    def update(self, limitation):
        if isinstance(limitation, LayerLimitation):
            self.main.update(limitation.main)
            self.subs.update(limitation.subs)
        elif isinstance(limitation, dict):
            for k, v in limitation.items():
                self.add(k, v)

    def keys(self):
        return list(self.main.keys()) + list(self.subs.keys())

    def items(self):
        return tuple(list(self.main.items()) + list(self.subs.items()))

    def __len__(self):
        return len(self.main) + len(self.subs)


class Observers(Layers):
    """
    所有对于数据对象与观察者之间的关联关系操作的封装类。todo 与_Layers相同
    """

    def __init__(self, entity):
        """
        所有对于数据对象与观察者之间的关联关系操作的封装类 todo 与_Layers相同
        :param entity:
        """
        super(Observers, self).__init__(entity)

        # todo 每个函数单独调用下面的Observer
        # from loongtian.nvwa.models.observer import Observer
