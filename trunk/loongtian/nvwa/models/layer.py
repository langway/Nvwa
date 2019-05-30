#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

import copy
from loongtian.nvwa import settings
from loongtian.nvwa.models.baseEntity import BaseEntity
from loongtian.nvwa.models.enum import ObjType
from loongtian.nvwa.models.metaData import MetaData
from loongtian.nvwa.models.metaNet import MetaNet
from loongtian.nvwa.models.realObject import RealObject
from loongtian.nvwa.models.knowledge import Knowledge
from loongtian.nvwa.organs.character import Character
from loongtian.nvwa.runtime.relatedObjects import UpperObjs, LowerObjs


class Layer(BaseEntity):
    """
    分层对象的关系表（元数据、元数据网、实际对象、知识网、集合等），包括：
        MetaData--RealObject
        MetaNet--MetaData
        MetaNet--Knowledge
        Knowledge--RealObject
        Knowledge-Knowledge（[苹果,红]--[苹果,颜色,红]--[苹果,属性,颜色,红]）
        Collection-RealObject 把集合当成一个对象
        [Knowledge]-Collection ??
        每个层的对象可能是多对多关系，
        例如：
            MetaData[牛] -- RealObject[动物牛, 形容词牛]
            RealObject[动物牛] -- MetaData[牛, cow, 图片牛]
    :rawParam
    :attribute    
    upperid 上一级对象ID，RID或mnid。
    utype 上一级对象ID的类型，使用IdTypeEnum枚举。
    lowerid 下一级对象ID，RID或mnid。
    ltype 下一级对象ID的类型，使用IdTypeEnum枚举。
    weight 阀值，用于遗忘或凝固。
    isdel 逻辑删除标记
    """
    __databasename__ = settings.db.db_nvwa  # 所在数据库。
    __tablename__ = settings.db.tables.tbl_layer # 所在表。与Flask统一
    primaryKey = copy.copy(BaseEntity.primaryKey)  # 模型对应的主键
    primaryKey.extend(["upperid", "lowerid"])
    columns = copy.copy(BaseEntity.columns)  # 模型对应的非主键的全部字段
    columns.extend(["utype", "ltype", "weight"])

    retrieveColumns = copy.copy(BaseEntity.retrieveColumns)  # 查询时需要使用的字段
    retrieveColumns.extend(["upperid", "lowerid"])

    isChainedObject = False  # 是否是链式对象的标记（metaNet、Knowledge等）

    # Layer没有分层对象
    upperLimitation = None
    lowerLimitation = None

    def __init__(self, upper=None, lower=None, utype=None, ltype=None,
                 weight=Character.Original_Link_Weight,
                 createrid='',
                 createtime=None, updatetime=None, lasttime=None,
                 status=200, # 状态; 0-不可用(逻辑删除);200-正常;800-不可遗忘
                 memory=None):
        """
        分层对象的关系表（元数据、元数据网、实际对象、知识网、集合等）
        :param upper:上一级对象
        :param lower:下一级对象
        :param utype:上一级对象的类型
        :param ltype:下一级对象的类型
        :param weight:两者相连的权重
        :param createrid: 添加人; 格式：(user_id)中文名
        :param createrip: 添加人IP
        :param createtime: 添加时间;
        :param updatetime: 更新时间
        :param lasttime: 最近访问时间
        :param status: 状态; 0-不可用(逻辑删除);200-正常;800-不可遗忘
        :param memory:
        """

        super(Layer, self).__init__(None,
                                    createrid,
                                    createtime, updatetime, lasttime,
                                    status,memory=memory)

        if upper:
            if isinstance(upper, str) or isinstance(upper, unicode):
                self.upperid = upper
                self._UpperItem = None
            elif isinstance(upper, BaseEntity):
                self.upperid = upper.id
                self.utype = upper.getType()
                self._UpperItem = upper
            else:
                self._UpperItem = None
        else:
            self._UpperItem = None
        if utype:
            if isinstance(utype, int) or isinstance(utype, str) or isinstance(utype, unicode):
                self.utype = utype
            elif isinstance(upper, BaseEntity):
                self.utype = upper.getType()

        if lower:
            if isinstance(lower, str) or isinstance(lower, unicode):
                self.lowerid = lower
                self._UpperItem = None
            elif isinstance(lower, BaseEntity):
                self.lowerid = lower.id
                self.ltype = lower.getType()
                self._LowerItem = lower
            else:
                self._UpperItem = None
        else:
            self._LowerItem = None

        if ltype:
            if isinstance(ltype, int) or isinstance(ltype, str) or isinstance(ltype, unicode):
                self.ltype = ltype
            elif isinstance(lower, BaseEntity):
                self.ltype = lower.getType()

        self.weight = weight


        self._isMemoryUseDoubleKeyDict = True  # 内存之中存储是否使用双键字典。
                                              # 女娲系统的metanet、knowledge、layer的内存存储、查找都使用双键字典


    @staticmethod
    def createLayerByUpperAndLower(upper, lower,
                                   weight=Character.Original_Link_Weight,
                                   recordInDB=True, utype=None, ltype=None,
                                   memory= None):

        if not recordInDB:
            return Layer.createLayerByUpperAndLowerInMemory(upper, lower,
                                                            weight, utype, ltype,
                                                            memory= memory)
        else:
            return Layer.createLayerByUpperAndLowerInDB(upper, lower,
                                                        weight, utype, ltype,
                                                        memory= memory)

    @staticmethod
    def createLayerByUpperAndLowerInMemory(upper, lower,
                                           weight=Character.Original_Link_Weight,
                                           utype=None, ltype=None,
                                           memory= None):
        """
        创建LayerItem（不记录到数据库）
        :param upper:可以是MetaData、MetaNetItem、RealObject、Knowledge、Collection或upperid(BaseEntity及其继承类，或 Id字符串)或[uid,utype]\(uid,utype)
        :param lower:可以是MetaData、MetaNetItem、RealObject、Knowledge、Collection或upperid(BaseEntity及其继承类，或 Id字符串)或[lid,ltype]\(lid,ltype)
        :return:
        """
        if utype:
            uid, _utype = Layer.getIdAndType(upper)
        else:
            uid, utype = Layer.getIdAndType(upper)

        if ltype:
            lid, _ltype = Layer.getIdAndType(lower)
        else:
            lid, ltype = Layer.getIdAndType(lower)

        _layer = Layer(upper=uid, utype=utype, lower=lid, ltype=ltype, weight=weight,memory=memory)
        if memory: # 添加到临时记忆区
            memory.WorkingMemory.addInMemory(_layer)
        return _layer

    @staticmethod
    def createLayerByUpperAndLowerInDB(upper, lower,
                                       weight=Character.Original_Link_Weight,
                                       utype=None, ltype=None,
                                       memory= None):
        """
        创建LayerItem
        :param upper:可以是MetaData、MetaNetItem、RealObject、Knowledge、Collection或upperid(BaseEntity及其继承类，或 Id字符串)或[uid,utype]\(uid,utype)
        :param lower:可以是MetaData、MetaNetItem、RealObject、Knowledge、Collection或upperid(BaseEntity及其继承类，或 Id字符串)或[lid,ltype]\(lid,ltype)
        :return:
        """
        layer = Layer.createLayerByUpperAndLowerInMemory(upper, lower, weight, utype, ltype,
                                                         memory=memory)

        # 首先检查是否存在
        retrived = layer.getByColumnsInDB()
        if not retrived:
            # 如果不存在，创建之
            layer._UpperItem = upper
            layer._LowerItem = lower
            layer.status = 200  # 确保未逻辑删除
            layer.create(checkExist=False)
            # # 已经添加到持久记忆区
            # memory.PersistentMemory.a
        else:
            layer = retrived
            if layer.status==0:  # 如果逻辑删除，恢复之
                layer.restore()

            layer._UpperItem = upper
            layer._LowerItem = lower

        return layer

    def getUpperItem(self):
        """
        根据upper取得上一级对象的对象（可能是MetaData、MetaNetItem、RealObject、Knowledge、Collection）
        :return:
        """
        if self.upperid is None:
            return None
        if self._UpperItem:
            return self._UpperItem

        # 根据上一级对象的类型取得对应的对象（包括：MetaData、MetaNet）
        if ObjType.isMetaData(self.utype):
            self._UpperItem = MetaData.getOne(memory=self.MemoryCentral, mid=self.upperid)
        elif ObjType.isMetaNet(self.utype):
            self._UpperItem = MetaNet.getOne(memory=self.MemoryCentral, mnid=self.upperid)
        elif ObjType.isUnclassifiedRealObject(self.utype):
            self._UpperItem = RealObject.getOne(memory=self.MemoryCentral, rid=self.upperid)
        elif ObjType.isKnowledge(self.utype):
            self._UpperItem = Knowledge.getOne(memory=self.MemoryCentral, kid=self.upperid)
        # elif ObjType.isCollection(self.utype):
        #     self._UpperItem = Collection.getOne(cid = self.upperid)
        else:
            raise Exception("上一级对象类型错误：{%d:%s}。" % (self.utype, ObjType.getTypeNames(self.utype)))

        if not self._UpperItem:
            raise Exception(
                "未能取得上一级对象对象：{%s:%s,%d:%s}。" % ("Id", self.upperid, self.utype, ObjType.getTypeNames(self.utype)))
        return self._UpperItem

    def getLowerItem(self):
        """
        根据lower取得实际的下一层对象（可能是MetaData、MetaNetItem、RealObject、Knowledge、Collection）
        :return:
        """
        if self.lowerid is None:
            return None
        if self._LowerItem:
            return self._LowerItem
        # 根据下一级对象的类型取得对应的对象（包括：MetaData、MetaNet）
        if ObjType.isMetaData(self.ltype):
            self._LowerItem = MetaData.getOne(memory=self.MemoryCentral, mid=self.lowerid)
        elif ObjType.isMetaNet(self.ltype):
            self._LowerItem = MetaNet.getOne(memory=self.MemoryCentral, mnid=self.lowerid)
        elif ObjType.isRealObject(self.ltype):
            self._LowerItem = RealObject.getOne(memory=self.MemoryCentral, rid=self.lowerid)
        elif ObjType.isKnowledge(self.ltype):
            self._LowerItem = Knowledge.getOne(memory=self.MemoryCentral, kid=self.lowerid)
        # elif ObjType.isCollection(self.ltype):
        #     self._LowerItem = Collection.getOne(cid = self.lowerid)
        else:
            raise Exception("下一级对象类型错误：{%d:%s}。" % (self.ltype, ObjType.getTypeNames(self.ltype)))

        if not self._LowerItem:
            raise Exception(
                "未能取得下一级对象对象：{%s:%s,%d:%s}。" % ("Id", self.lowerid, self.ltype, ObjType.getTypeNames(self.ltype)))
        return self._LowerItem

    @staticmethod
    def getLowersByUpperInDB(upper, lazy_get=True,memory=None):
        """
        查找以upper开头的所有下一级对象
        :param upper: MetaData、MetaNetItem、RealObject、Knowledge、Collection或upperid(BaseEntity及其继承类，或 Id字符串)
        :param lazy_get 是否等需要的时候再取得对应的对象（以getChainItems填充）
        :return: [nvwa对象]
        """
        if not upper:
            raise Exception("upper or upperid(%s)不能为空！" % upper)

        upperid = Layer._getId(upper)
        layers = Layer.getAllByConditionsInDB(memory=memory,upperid=upperid)

        if not lazy_get and layers:
            if isinstance(layers, list):
                lowers = LowerObjs()
                for layer in layers:
                    layer.getLowerItem()
                    lowers.add(layer._LowerItem, layer.weight,upper)
                return lowers
            else:  # 一个对象
                lowers = LowerObjs()
                layers.getLowerItem()
                lowers.add(layers._LowerItem, layers.weight,upper)
                return lowers

        return layers

    @staticmethod
    def getUppersByLowerInDB(lower, lazy_get=True,memory=None):
        """
        查找lower的所有上一级对象
        :param lower: MetaData、MetaNetItem、RealObject、Knowledge、Collection或upperid(BaseEntity及其继承类，或 Id字符串)
        :param lazy_get 是否等需要的时候再取得对应的对象（以getChainItems填充）
        :return: [nvwa对象]
        """
        if not lower:
            raise Exception("lower or lowerid(%s)不能为空！" % lower)

        lower = Layer._getId(lower)
        layers = Layer.getAllByConditionsInDB(memory=memory,lowerid=lower)

        if not lazy_get and layers:
            if isinstance(layers, list):
                uppers = UpperObjs()
                for layer in layers:
                    layer.getUpperItem()
                    uppers.add(layer._UpperItem, layer.weight,lower)
                return uppers
            else:  # 一个对象
                uppers = UpperObjs()
                layers.getUpperItem()
                uppers.add(layers._UpperItem, layers.weight,lower)
                return uppers

        return layers

    @staticmethod
    def getTypedLowersByUpperInDB(upper,
                                  lower_type=ObjType.UNKNOWN,
                                  lazy_get=True,
                                  memory=None):
        """
        根据指定类型，查找upper的所有下一级对象，例如：查找MetaData相关联的所有RealObject
        :param upper: MetaData、MetaNetItem、RealObject、Knowledge、Collection或upperid(BaseEntity及其继承类，或 Id字符串)
        :param lazy_get 是否等需要的时候再取得对应的对象（以getChainItems填充）
        :return: [nvwa对象]
        """
        if not upper:
            raise Exception("upper or upperid(%s)不能为空！" % upper)
        if lower_type is None or lower_type == ObjType.UNKNOWN:
            raise Exception("必须提供下一层对象的nvwa对象类型，当前类型为%s" % lower_type)

        upperid = Layer._getId(upper)
        layers = Layer.getAllByConditionsInDB(memory=memory,upperid=upperid, ltype=lower_type)

        if not lazy_get and layers:
            if isinstance(layers, list):
                lowers = LowerObjs()
                for layer in layers:
                    layer.getLowerItem()
                    lowers.add(layer._LowerItem, layer.weight,upper)
                return lowers
            else:  # 一个对象
                lowers = LowerObjs()
                layers.getLowerItem()
                lowers.add(layers._LowerItem, layers.weight,upper)
                return lowers

        return layers

    @staticmethod
    def getTypedUppersByLowerInDB(lower,
                                  upper_type=ObjType.UNKNOWN,
                                  lazy_get=True,
                                  memory=None):
        """
        根据指定类型，查找lower的所有上一级对象，例如：查找RealObject相关联的所有MetaData
        :param lower: MetaData、MetaNetItem、RealObject、Knowledge、Collection或upperid(BaseEntity及其继承类，或 Id字符串)
        :param lazy_get 是否等需要的时候再取得对应的对象（以getChainItems填充）
        :return: [nvwa对象]
        """
        if not lower:
            raise Exception("lower or lowerid(%s)不能为空！" % lower)
        if upper_type is None or upper_type == ObjType.UNKNOWN:
            raise Exception("必须提供上一层对象的nvwa对象类型，当前类型为%s" % upper_type)

        lower = Layer._getId(lower)
        layers = Layer.getAllByConditionsInDB(memory=memory,utype=upper_type, lowerid=lower)

        if not lazy_get and layers:
            if isinstance(layers, list):
                uppers = UpperObjs()
                for layer in layers:
                    layer.getUpperItem()
                    uppers.add(layer._UpperItem, layer.weight,lower)
                return uppers
            else:  # 一个对象
                uppers = UpperObjs()
                layers.getUpperItem()
                uppers.add(layers._UpperItem, layers.weight,lower)
                return uppers

        return layers

    @staticmethod
    def getLayerByUpperAndLower(upper, lower, lazy_get=False,memory=None):
        """
        在内存或数据库中查找以upper开头并且以lower结尾的元数据链(只能有一条)
        :param upper: MetaData、MetaNetItem、RealObject、Knowledge、Collection或upperid(BaseEntity及其继承类，或 Id字符串)
        :param lower: MetaData、MetaNetItem、RealObject、Knowledge、Collection或upperid(BaseEntity及其继承类，或 Id字符串)
        :param lazy_get 是否等需要的时候再取得对应的对象（以getChainItems填充）
        :return: Layer
        """
        # 首先在内存中查找
        layer = Layer.getLayerByUpperAndLowerInMemory(upper, lower,memory=memory)
        if layer:
            return layer
        # 内存没找到，在数据库中查找
        layer = Layer.getLayerByUpperAndLowerInDB(upper, lower, lazy_get)
        return layer

    @staticmethod
    def getLayerByUpperAndLowerInMemory(upper, lower,memory=None):
        """
        [内存操作]查找以upper开头并且以lower结尾的元数据链(只能有一条)
        :param upper: MetaData、MetaNetItem、RealObject、Knowledge、Collection或upperid(BaseEntity及其继承类，或 Id字符串)
        :param lower: MetaData、MetaNetItem、RealObject、Knowledge、Collection或upperid(BaseEntity及其继承类，或 Id字符串)
        :return: Layer
        """
        if memory and memory.LayerUpperAndLowerDict:
            if not upper:
                raise Exception("upperid(%s)不能为空！" % upper)
            if not lower:
                raise Exception("lowerid(%s)不能为空！" % lower)

            upperid = Layer._getId(upper)
            lowerid = Layer._getId(lower)
            layer = memory.WorkingMemory.getLayerByDoubleKeysInMemory(upperid,lowerid)
            if layer:
                return layer
            layer = memory.PersistentMemory.getLayerByDoubleKeysInMemory(upperid, lowerid)

            return layer

    @staticmethod
    def getLayerByUpperAndLowerInDB(upper, lower, lazy_get=True,memory=None):
        """
        [数据库操作]查找以upper开头并且以lower结尾的元数据链(只能有一条)
        :param upper: MetaData、MetaNetItem、RealObject、Knowledge、Collection或upperid(BaseEntity及其继承类，或 Id字符串)
        :param lower: MetaData、MetaNetItem、RealObject、Knowledge、Collection或upperid(BaseEntity及其继承类，或 Id字符串)
        :param lazy_get 是否等需要的时候再取得对应的对象（以getChainItems填充）
        :return: Layer
        """
        if not upper:
            raise Exception("upperid(%s)不能为空！" % upper)
        if not lower:
            raise Exception("lowerid(%s)不能为空！" % lower)

        upper = Layer._getId(upper)
        lower = Layer._getId(lower)
        layers = Layer.getAllByConditionsInDB(memory=memory,upperid=upper, lowerid=lower)
        if layers is None:
            return None
        if isinstance(layers, list):
            if layers is None or len(layers) == 0:
                return None
            if len(layers) > 1:
                raise Exception(
                    "以upper开头并且以lower结尾的Layer对象只能有一条,upperid:%s,upperid type:%s,lowerid:%s,lowerid type:%s" % (
                    upper, str(type(upper)), lower, str(type(lower))))

            layer = layers[0]
        else:
            layer = layers

        layer._UpperItem = upper
        layer._LowerItem = lower

        if not lazy_get:
            layer.getLowerItem()
            layer.getUpperItem()

        # # 添加到内存以便后续操作(已经在memory中进行了操作)
        # if self.MemoryCentral and self.MemoryCentral.MetaNetUpperAndLowerDict:
        #     self.MemoryCentral.MetaNetUpperAndLowerDict[upperid][lowerid]=layer

        return layer

    @staticmethod
    def deleteByUpper(upper):
        """
        根据上一级对象对象，逻辑删除所有LayerItem
        :param upper:BaseEntity及其继承类，或 Id字符串
        :return:affectedRowsNum
        """
        if upper is None:
            raise Exception("无法逻辑删除所有LayerItem，upperid is None！")

        upperid = Layer._getId(upper)
        return Layer.updateAllInDB(wheres={"upperid": upperid}, isdel=True)

    @staticmethod
    def deleteByLower(lower):
        """
        根据结尾对象，逻辑删除所有LayerItem
        :param lower:BaseEntity及其继承类，或 Id字符串
        :return:
        """
        if lower is None:
            raise Exception("无法逻辑删除所有LayerItem，lowerid is None！")

        lowerid = Layer._getId(lower)
        return Layer.updateAllInDB(wheres={"lowerid": lowerid}, isdel=True)

    @staticmethod
    def deleteByUpperAndLower(upper, lower):
        """
        逻辑删除Layer。
        :param upper: MetaData、MetaNetItem、RealObject、Knowledge、Collection或upperid(BaseEntity及其继承类，或 Id字符串)
        :param lower:  MetaData、MetaNetItem、RealObject、Knowledge、Collection或upperid(BaseEntity及其继承类，或 Id字符串)
        :return:
        """
        if upper is None:
            raise Exception("无法逻辑删除所有LayerItem，upperid is None！")

        upperid = Layer._getId(upper)
        if lower is None:
            raise Exception("无法逻辑删除所有LayerItem，lowerid is None！")

        lowerid = Layer._getId(lower)
        return Layer.updateAllInDB(wheres={"upperid": upperid, "lowerid": lowerid}, isdel=True)

    @staticmethod
    def _physicalDeleteByUpper(upper):
        """
        根据上一级对象对象，物理删除所有LayerItem
        :param upper:BaseEntity及其继承类，或 Id字符串
        :return:
        """
        if upper is None:
            raise Exception("无法物理删除所有LayerItem，upperid is None！")

        upperid = Layer._getId(upper)
        return Layer._physicalDeleteBy(recordInMemory=True, upperid=upperid)

    @staticmethod
    def _physicalDeleteByLower(lower):
        """
        根据结尾对象，物理删除所有LayerItem
        :param lower:BaseEntity及其继承类，或 Id字符串
        :return:
        """
        if lower is None:
            raise Exception("无法物理删除所有LayerItem，lowerid is None！")

        lowerid = Layer._getId(lower)
        return Layer._physicalDeleteBy(recordInMemory=True, lowerid=lowerid)

    @staticmethod
    def _physicalDeleteByUpperAndLower(upper, lower):
        """
        物理删除Layer。
        :param upper: MetaData、MetaNetItem、RealObject、Knowledge、Collection或upperid(BaseEntity及其继承类，或 Id字符串)
        :param lower:  MetaData、MetaNetItem、RealObject、Knowledge、Collection或upperid(BaseEntity及其继承类，或 Id字符串)
        :return:
        """
        if upper is None:
            raise Exception("无法物理删除所有LayerItem，upper is None！")

        upperid = Layer._getId(upper)
        if lower is None:
            raise Exception("无法物理删除所有LayerItem，lower is None！")

        lowerid = Layer._getId(lower)
        return Layer._physicalDeleteBy(targetRowsAffected=1, recordInMemory=True, upperid=upperid, lowerid=lowerid)

    def getType(self):
        """
        获得类型
        :return: 总是返回IdTypeEnum.LAYER类型。
        """
        return ObjType.LAYER

    def __repr__(self):
        return "{Layer:{lid:%s}}" % (self.id)
