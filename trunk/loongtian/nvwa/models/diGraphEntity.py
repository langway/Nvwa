#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

import copy
from loongtian.nvwa import settings
from loongtian.nvwa.models.baseEntity import BaseEntity
from loongtian.nvwa.models.enum import ObjType


from loongtian.nvwa.organs.character import Character
from loongtian.nvwa.runtime.relatedObjects import UpperObjs, LowerObjs


class DiGraphEntity(BaseEntity):
    """
    有向图
    :rawParam
    :attribute    
    startid 始端对象ID，RID或mnid。
    stype 始端对象ID的类型，使用IdTypeEnum枚举。
    endid 尾端对象ID，RID或mnid。
    etype 尾端对象ID的类型，使用IdTypeEnum枚举。
    weight 阀值，用于遗忘或凝固。
    isdel 逻辑删除标记
    """
    __databasename__ = settings.db.db_nvwa  # 所在数据库。
    __tablename__ = None  # 所在表。与Flask统一
    primaryKey = copy.copy(BaseEntity.primaryKey)  # 模型对应的主键
    primaryKey.extend(["startid", "endid"])
    columns = copy.copy(BaseEntity.columns)  # 模型对应的非主键的全部字段
    columns.extend(["stype", "etype", "weight"])

    retrieveColumns = copy.copy(BaseEntity.retrieveColumns)  # 查询时需要使用的字段
    retrieveColumns.extend(["startid", "endid"])

    isChainedObject = False  # 是否是链式对象的标记（metaNet、Knowledge等）

    # Digraph没有有向图
    upperLimitation = None
    lowerLimitation = None

    def __init__(self, start=None, end=None, stype=None, etype=None,
                 weight=Character.Original_Link_Weight,
                 createrid=None,
                 createtime=None, updatetime=None, lasttime=None,
                 status=200,  # 状态; 0-不可用(逻辑删除);200-正常;800-不可遗忘
                 memory=None):
        """
        有向图的关系表（元数据、元数据网、实际对象、知识网、集合等）
        :param start:始端对象
        :param end:尾端对象
        :param stype:始端对象的类型
        :param etype:尾端对象的类型
        :param weight:两者相连的权重
        :param createrid: 添加人; 格式：(user_id)中文名
        :param createrip: 添加人IP
        :param createtime: 添加时间;
        :param updatetime: 更新时间
        :param lasttime: 最近访问时间
        :param status: 状态; 0-不可用(逻辑删除);200-正常;800-不可遗忘
        :param memory:
        """

        super(DiGraphEntity, self).__init__(None,
                                            createrid,
                                            createtime, updatetime, lasttime,
                                            status, memory=memory)

        if start:
            if isinstance(start, str):
                self.startid = start
                self._StartItem = None
            elif isinstance(start, BaseEntity):
                self.startid = start.id
                self.stype = start.getType()
                self._StartItem = start
            else:
                self._StartItem = None
        else:
            self._StartItem = None
        if stype:
            if isinstance(stype, int) or isinstance(stype, str):
                self.stype = stype
            elif isinstance(start, BaseEntity):
                self.stype = start.getType()

        if end:
            if isinstance(end, str):
                self.endid = end
                self._StartItem = None
            elif isinstance(end, BaseEntity):
                self.endid = end.id
                self.etype = end.getType()
                self._EndItem = end
            else:
                self._StartItem = None
        else:
            self._EndItem = None

        if etype:
            if isinstance(etype, int) or isinstance(etype, str):
                self.etype = etype
            elif isinstance(end, BaseEntity):
                self.etype = end.getType()

        self.weight = weight

        self._isMemoryUseDoubleKeyDict = True  # 内存之中存储是否使用双键字典。
        # 女娲系统的metanet、knowledge、layer的内存存储、查找都使用双键字典

    @classmethod
    def createByStartAndEnd(cls,start, end,
                            weight=Character.Original_Link_Weight,
                            recordInDB=True, stype=None, etype=None,
                            memory=None):

        if not recordInDB:
            return cls.createByStartAndEndInMemory(start, end,
                                                   weight, stype, etype,
                                                   memory=memory)
        else:
            return cls.createByStartAndEndInDB(start, end,
                                               weight, stype, etype,
                                               memory=memory)

    @classmethod
    def createByStartAndEndInMemory(cls, start, end,
                                    weight=Character.Original_Link_Weight,
                                    stype=None, etype=None,
                                    memory=None):
        """
        创建Digraph（不记录到数据库）
        :param start:可以是MetaData、MetaNetItem、RealObject、Knowledge、Collection或startid(BaseEntity及其继承类，或 Id字符串)或[uid,stype]\\(uid,stype)
        :param end:可以是MetaData、MetaNetItem、RealObject、Knowledge、Collection或startid(BaseEntity及其继承类，或 Id字符串)或[lid,etype]\\(lid,etype)
        :return:
        """
        if stype:
            sid, _stype = cls.getIdAndType(start)
        else:
            sid, stype = cls.getIdAndType(start)

        if etype:
            eid, _etype = cls.getIdAndType(end)
        else:
            eid, etype = cls.getIdAndType(end)

        _digraph = cls(start=sid, stype=stype, end=eid, etype=etype, weight=weight, memory=memory)
        if memory:  # 添加到临时记忆区
            memory.WorkingMemory.addInMemory(_digraph)
        return _digraph

    @classmethod
    def createByStartAndEndInDB(cls, start, end,
                                weight=Character.Original_Link_Weight,
                                stype=None, etype=None,
                                memory=None):
        """
        创建Digraph
        :param start:可以是MetaData、MetaNetItem、RealObject、Knowledge、Collection或startid(BaseEntity及其继承类，或 Id字符串)或[uid,stype]\\(uid,stype)
        :param end:可以是MetaData、MetaNetItem、RealObject、Knowledge、Collection或startid(BaseEntity及其继承类，或 Id字符串)或[lid,etype]\\(lid,etype)
        :return:
        """
        digraph = cls.createByStartAndEndInMemory(start, end, weight, stype, etype,
                                                  memory=memory)

        # 首先检查是否存在
        retrived = digraph.getByColumnsInDB()
        if not retrived:
            # 如果不存在，创建之
            digraph._StartItem = start
            digraph._EndItem = end
            digraph.status = 200  # 确保未逻辑删除
            digraph.create(checkExist=False)
            # # 已经添加到持久记忆区
            # memory.PersistentMemory.a
        else:
            digraph = retrived
            if digraph.status == 0:  # 如果逻辑删除，恢复之
                digraph.restore()

            digraph._StartItem = start
            digraph._EndItem = end

        return digraph

    def getStartItem(self):
        """
        根据start取得始端对象的对象（可能是MetaData、MetaNetItem、RealObject、Knowledge、Collection）
        :return:
        """
        if self.startid is None:
            return None
        if self._StartItem:
            return self._StartItem
        import loongtian.nvwa.models.entityHelper as  entityHelper
        # 根据对象的类型及Id取得对应的对象（包括：MetaData、MetaNet、RealObject、Knowledge）     
        self._StartItem = entityHelper.getEntityByTypeAndId(entityType=self.stype, id=self.startid,memory=self.MemoryCentral)
        
        if not self._StartItem:
            raise Exception(
                "未能取得始端对象对象：{%s:%s,%d:%s}。" % ("Id", self.startid, self.stype, ObjType.getName(self.stype)))
        return self._StartItem

    def getEndItem(self):
        """
        根据end取得实际的尾端对象（可能是MetaData、MetaNetItem、RealObject、Knowledge、Collection）
        :return:
        """
        if self.endid is None:
            return None
        if self._EndItem:
            return self._EndItem
        import loongtian.nvwa.models.entityHelper as  entityHelper
        # 根据对象的类型及Id取得对应的对象（包括：MetaData、MetaNet、RealObject、Knowledge）     
        self._EndItem = entityHelper.getEntityByTypeAndId(entityType=self.etype, id=self.endid,
                                                            memory=self.MemoryCentral)

        if not self._EndItem:
            raise Exception(
                "未能取得尾端对象对象：{%s:%s,%d:%s}。" % ("Id", self.endid, self.etype, ObjType.getName(self.etype)))
        return self._EndItem

    @classmethod
    def getEndsByStartInDB(cls, start, lazy_get=True, memory=None):
        """
        查找以start开头的所有尾端对象
        :param start: MetaData、MetaNetItem、RealObject、Knowledge、Collection或startid(BaseEntity及其继承类，或 Id字符串)
        :param lazy_get 是否等需要的时候再取得对应的对象（以getChainItems填充）
        :return: [nvwa对象]
        """
        if not start:
            raise Exception("start or startid(%s)不能为空！" % start)

        startid = BaseEntity._getId(start)
        ends = cls.getAllByConditionsInDB(memory=memory, startid=startid)

        if not lazy_get and ends:
            end_objs = LowerObjs()
            if isinstance(ends, list):
                for digraph in ends:
                    digraph.getEndItem()
                    end_objs.add(digraph._EndItem, digraph.weight, start)

            else:  # 一个对象
                ends.getEndItem()
                end_objs.add(ends._EndItem, ends.weight, start)
            return end_objs

        return ends

    @classmethod
    def getStartsByEndInDB(cls, end, lazy_get=True, memory=None):
        """
        查找end的所有始端对象
        :param end: MetaData、MetaNetItem、RealObject、Knowledge、Collection或startid(BaseEntity及其继承类，或 Id字符串)
        :param lazy_get 是否等需要的时候再取得对应的对象（以getChainItems填充）
        :return: [nvwa对象]
        """
        if not end:
            raise Exception("end or endid(%s)不能为空！" % end)

        end = BaseEntity._getId(end)
        starts = cls.getAllByConditionsInDB(memory=memory, endid=end)

        if not lazy_get and starts:
            start_objs=UpperObjs()
            if isinstance(starts, list):
                for start in starts:
                    start.getStartItem()
                    start_objs.add(start._StartItem, start.weight, end)

            else:  # 一个对象
                starts.getStartItem()
                start_objs.add(starts._StartItem, starts.weight, end)
            return start_objs

        return starts

    @classmethod
    def getTypedEndsByStartInDB(cls,
                                start,
                                end_type=ObjType.UNKNOWN,
                                lazy_get=True,
                                memory=None):
        """
        根据指定类型，查找start的所有尾端对象，例如：查找MetaData相关联的所有RealObject
        :param start: MetaData、MetaNetItem、RealObject、Knowledge、Collection或startid(BaseEntity及其继承类，或 Id字符串)
        :param lazy_get 是否等需要的时候再取得对应的对象（以getChainItems填充）
        :return: [nvwa对象]
        """
        if not start:
            raise Exception("start or startid(%s)不能为空！" % start)
        if end_type is None or end_type == ObjType.UNKNOWN:
            raise Exception("必须提供尾端对象的nvwa对象类型，当前类型为%s" % end_type)

        startid = BaseEntity._getId(start)
        ends = cls.getAllByConditionsInDB(memory=memory, startid=startid, etype=end_type)

        if not lazy_get and ends:
            end_objs=LowerObjs()
            if isinstance(ends, list):
                for digraph in ends:
                    digraph.getEndItem()
                    end_objs.add(digraph._EndItem, digraph.weight, start)

            else:  # 一个对象
                ends.getEndItem()
                end_objs.add(ends._EndItem, ends.weight, start)
            return end_objs

        return ends

    @classmethod
    def getTypedStartsByEndInDB(cls,
                                end,
                                start_type=ObjType.UNKNOWN,
                                lazy_get=True,
                                memory=None):
        """
        根据指定类型，查找end的所有始端对象，例如：查找RealObject相关联的所有MetaData
        :param end: MetaData、MetaNetItem、RealObject、Knowledge、Collection或startid(BaseEntity及其继承类，或 Id字符串)
        :param lazy_get 是否等需要的时候再取得对应的对象（以getChainItems填充）
        :return: [nvwa对象]
        """
        if not end:
            raise Exception("end or endid(%s)不能为空！" % end)
        if start_type is None or start_type == ObjType.UNKNOWN:
            raise Exception("必须提供始端对象的nvwa对象类型，当前类型为%s" % start_type)

        end = BaseEntity._getId(end)
        starts = cls.getAllByConditionsInDB(memory=memory, stype=start_type, endid=end)

        if not lazy_get and starts:
            start_objs = UpperObjs()
            if isinstance(starts, list):
                for start in starts:
                    start.getStartItem()
                    start_objs.add(start._StartItem, start.weight, end)
            else:  # 一个对象
                starts.getStartItem()
                start_objs.add(starts._StartItem, starts.weight, end)

            return start_objs

        return starts

    @classmethod
    def getByStartAndEnd(cls, start, end, lazy_get=False, memory=None):
        """
        在内存或数据库中查找以start开头并且以end结尾的元数据链(只能有一条)
        :param start: MetaData、MetaNetItem、RealObject、Knowledge、Collection或startid(BaseEntity及其继承类，或 Id字符串)
        :param end: MetaData、MetaNetItem、RealObject、Knowledge、Collection或startid(BaseEntity及其继承类，或 Id字符串)
        :param lazy_get 是否等需要的时候再取得对应的对象（以getChainItems填充）
        :return: Digraph
        """
        # 首先在内存中查找
        digraph = cls.getByStartAndEndInMemory(start, end, memory=memory)
        if digraph:
            return digraph
        # 内存没找到，在数据库中查找
        digraph = cls.getByStartAndEndInDB(start, end, lazy_get)
        return digraph

    @classmethod
    def getByStartAndEndInMemory(cls, start, end, memory=None):
        """
        [内存操作]查找以start开头并且以end结尾的元数据链(只能有一条)
        :param start: MetaData、MetaNetItem、RealObject、Knowledge、Collection或startid(BaseEntity及其继承类，或 Id字符串)
        :param end: MetaData、MetaNetItem、RealObject、Knowledge、Collection或startid(BaseEntity及其继承类，或 Id字符串)
        :return: Digraph
        """
        if not memory:
            return None

        if not start:
            raise Exception("startid(%s)不能为空！" % start)
        if not end:
            raise Exception("endid(%s)不能为空！" % end)

        startid = BaseEntity._getId(start)
        endid = BaseEntity._getId(end)
        return memory.getByDoubleKeysInMemory(startid, endid,cls)

    @classmethod
    def getByStartAndEndInDB(cls, start, end, lazy_get=True, memory=None):
        """
        [数据库操作]查找以start开头并且以end结尾的元数据链(只能有一条)
        :param start: MetaData、MetaNetItem、RealObject、Knowledge、Collection或startid(BaseEntity及其继承类，或 Id字符串)
        :param end: MetaData、MetaNetItem、RealObject、Knowledge、Collection或startid(BaseEntity及其继承类，或 Id字符串)
        :param lazy_get 是否等需要的时候再取得对应的对象（以getChainItems填充）
        :return: Digraph
        """
        if not start:
            raise Exception("startid(%s)不能为空！" % start)
        if not end:
            raise Exception("endid(%s)不能为空！" % end)

        start = BaseEntity._getId(start)
        end = BaseEntity._getId(end)
        digraphs = cls.getAllByConditionsInDB(memory=memory, startid=start, endid=end)
        if digraphs is None:
            return None
        if isinstance(digraphs, list):
            if digraphs is None or len(digraphs) == 0:
                return None
            if len(digraphs) > 1:
                raise Exception(
                    "以start开头并且以end结尾的Digraph对象只能有一条,startid:%s,startid type:%s,endid:%s,endid type:%s" % (
                        start, str(type(start)), end, str(type(end))))

            digraph = digraphs[0]
        else:
            digraph = digraphs

        digraph._StartItem = start
        digraph._EndItem = end

        if not lazy_get:
            digraph.getEndItem()
            digraph.getStartItem()

        # # 添加到内存以便后续操作(已经在memory中进行了操作)
        # if self.MemoryCentral and self.MemoryCentral.MetaNetStartAndEndDict:
        #     self.MemoryCentral.MetaNetStartAndEndDict[startid][endid]=digraph

        return digraph

    @classmethod
    def deleteByStart(cls, start):
        """
        根据始端对象对象，逻辑删除所有Digraph
        :param start:BaseEntity及其继承类，或 Id字符串
        :return:affectedRowsNum
        """
        if start is None:
            raise Exception("无法逻辑删除所有Digraph，startid is None！")

        startid = BaseEntity._getId(start)
        return cls.updateAllInDB(wheres={"startid": startid}, status=0)

    @classmethod
    def deleteByEnd(cls, end):
        """
        根据结尾对象，逻辑删除所有Digraph
        :param end:BaseEntity及其继承类，或 Id字符串
        :return:
        """
        if end is None:
            raise Exception("无法逻辑删除所有Digraph，endid is None！")

        endid = BaseEntity._getId(end)
        return cls.updateAllInDB(wheres={"endid": endid}, status=0)

    @classmethod
    def deleteByStartAndEnd(cls, start, end):
        """
        逻辑删除Digraph。
        :param start: MetaData、MetaNetItem、RealObject、Knowledge、Collection或startid(BaseEntity及其继承类，或 Id字符串)
        :param end:  MetaData、MetaNetItem、RealObject、Knowledge、Collection或startid(BaseEntity及其继承类，或 Id字符串)
        :return:
        """
        if start is None:
            raise Exception("无法逻辑删除所有Digraph，startid is None！")

        startid = BaseEntity._getId(start)
        if end is None:
            raise Exception("无法逻辑删除所有Digraph，endid is None！")

        endid = BaseEntity._getId(end)
        return cls.updateAllInDB(wheres={"startid": startid, "endid": endid}, status=0)

    @classmethod
    def _physicalDeleteByStart(cls, start,memory=None):
        """
        根据始端对象对象，物理删除所有Digraph
        :param start:BaseEntity及其继承类，或 Id字符串
        :return:
        """
        if start is None:
            raise Exception("无法物理删除所有Digraph，startid is None！")

        startid = BaseEntity._getId(start)
        return cls._physicalDeleteBy(memory=memory, startid=startid)

    @classmethod
    def _physicalDeleteByEnd(cls, end,memory=None):
        """
        根据结尾对象，物理删除所有Digraph
        :param end:BaseEntity及其继承类，或 Id字符串
        :return:
        """
        if end is None:
            raise Exception("无法物理删除所有Digraph，endid is None！")

        endid = BaseEntity._getId(end)
        return cls._physicalDeleteBy(memory=memory, endid=endid)

    @classmethod
    def _physicalDeleteByStartAndEnd(cls,start, end,memory=None):
        """
        物理删除Digraph。
        :param start: MetaData、MetaNetItem、RealObject、Knowledge、Collection或startid(BaseEntity及其继承类，或 Id字符串)
        :param end:  MetaData、MetaNetItem、RealObject、Knowledge、Collection或startid(BaseEntity及其继承类，或 Id字符串)
        :return:
        """
        if start is None:
            raise Exception("无法物理删除所有Digraph，start is None！")

        startid = BaseEntity._getId(start)
        if end is None:
            raise Exception("无法物理删除所有Digraph，end is None！")

        endid = BaseEntity._getId(end)
        return cls._physicalDeleteBy(targetRowsAffected=1, memory=memory, startid=startid, endid=endid)



    def __repr__(self):
        return "{Digraph:{lid:%s}}" % (self.id)
