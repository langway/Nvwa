#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

import copy
from loongtian.nvwa import settings
from loongtian.nvwa.models.baseEntity import BaseEntity, LayerLimitation
from loongtian.nvwa.models.enum import ObjType
from loongtian.nvwa.organs.character import Character
from loongtian.nvwa.runtime.specialList import RelatedRealObjs, RelatedRealChain


class MetaData(BaseEntity):
    """
    Meta元数据。
    :parameter
    :attribute
    id MetaID，UUID。
    type 资源类型，使用MetaDataEntity.TypeEnum枚举。
    mvalue 资源，文字直接存String，声音或图像存地址。
    frequency 优先级(int，使用次数)。
    createtime 创建时间。
    updatetime 更新时间。
    lasttime 上次访问时间。
    actType MetaData的词性，由其下的RealObject的类型决定。
    recognized 是否识别的标志。
                在系统运行中，经常会出现未能提取，但被截取出来的情况，
                例如：‘住房市级备案’，住房、备案可能都已识别，
                经过切割，市级也会被切割出来，但不属于已识别，需要等待后续的，例如反问等进行处理。
    relatedRealObjs 元数据对应实际对象的的集合。格式为：{rid:(RealObject,threshhold)}，一个MetaEntity对应多个RealObjectEntity。
        eg：Meta:牛 ==> RealObject:[动物牛, 形容词牛(厉害)]
    """
    __databasename__ = settings.db.db_nvwa  # 所在数据库。
    __tablename__ = settings.db.tables.tbl_metaData  # 所在表。与Flask统一
    primaryKey = copy.copy(BaseEntity.primaryKey)
    primaryKey.append("id")
    columns = copy.copy(BaseEntity.columns)
    columns.extend(["type", "mvalue", "weight", "recognized"])
    retrieveColumns = copy.copy(BaseEntity.retrieveColumns)  # 查询时需要使用的字段
    retrieveColumns.extend(["mvalue"])

    upperLimitation = LayerLimitation()
    upperLimitation.update({ObjType.META_NET: -1})  # MetaData 的上一层对象为MetaNet[可能有多个]
    # 例如：metanet:[[中国-人民]-解放军]\[中国-[人民-解放军]]----metadata:中国人民解放军-

    lowerLimitation = LayerLimitation()
    lowerLimitation.update({ObjType.REAL_OBJECT: -1,
                            ObjType.ACTION:-1})  # MetaData 的下一层对象为RealObject[可能有多个]

    # 例如：牛-realobject:R1:动物牛、R2:很牛的牛
    def __init__(self, id=None, type=ObjType.WORD, mvalue=None,
                 weight=Character.Original_Link_Weight, recognized=True,
                 createrid='',
                 createtime=None, updatetime=None, lasttime=None,
                 status=200,  # 状态; 0-不可用(逻辑删除);200-正常;800-不可遗忘
                 memory=None):
        """
        Meta元数据。
        :param id:
        :param type:
        :param mvalue:
        :param weight:
        :param recognized:
        :param createrid: 添加人; 格式：(user_id)中文名
        :param createrip: 添加人IP
        :param createtime: 添加时间;
        :param updatetime: 更新时间
        :param lasttime: 最近访问时间
        :param status: 状态; 0-不可用(逻辑删除);200-正常;800-不可遗忘
        """
        super(MetaData, self).__init__(id,
                                       createrid,
                                       createtime, updatetime, lasttime,
                                       status, memory=memory)

        self.type = type  # 类型根据外部设置

        if not isinstance(mvalue, str):
            mvalue = str(mvalue)
        self.mvalue = mvalue
        self.weight = weight
        self.recognized = recognized

        # ####################################
        #      下面为运行时数据
        # ####################################

        # 2018-12-06:所有上下层对象一律在Layers中处理
        # # 从数据库中取得的上一层的元数据网（可能有多个，例如：m:中国人民解放军<——m:中国-m:人民-m:解放军，m:中国-m:人民解放军）
        # self._upper_metanets = UpperObjs()
        # # 从数据库中取得的下一层的实际对象（可能有多个，例如：m:苹果——>r:可以吃的苹果，r:苹果公司，r:苹果手机）
        # self._lower_reals = LowerObjs()

        # self.gotRelatedRealObjsInDB = False  # 是否已经取得元数据对应实际对象的的集合的标记

    @staticmethod
    def retrieveByMvalue(mvalue, memory=None):
        """
        CRUD - Retrieve
        根据元字符串，查找库中是否存在此Entity，不比较PrimaryKey。
        :return: 找到返回Entity，未找到返回None
        """
        if mvalue is None or mvalue == "":
            return None

        # 首先从内存中取
        if memory:
            result = memory.getMetaByMvalueInMemory(mvalue)
            if result:
                return result

        # 未取到，查询数据库
        result = MetaData.getAllByConditionsInDB(memory=memory, limit=1, mvalue=mvalue)
        if result is None:
            return None
        elif isinstance(result, BaseEntity):
            return result
        elif isinstance(result, list):
            if len(result) == 0:
                return None
            elif len(result) == 1:
                # 已经记录到数据库，当前无需记载
                return result[0]
            else:
                raise Exception("查询结果%s不唯一！" % result)

    # #####################################################
    # 与实际对象相关的操作
    # #####################################################

    @staticmethod
    def getAllRelatedRealObjsInMetaChain(metaChain, createNewReal=True, recordInDB=True):
        """
        取得metaChain中metaData对应的realObjects，排序
        :param metaChain: [metaData]
        :param createNewReal: # 如果没找到，是否创建新的实际对象
        :param recordInDB: 是否记录到数据库中
        :return:
        """
        if not metaChain:
            return None, None

        realLowerObjs = []
        sorted_realsChain = RelatedRealChain()

        for meta in metaChain:
            if isinstance(meta, MetaData):
                reals = meta.Layers.getLowerEntitiesByType(ObjType.REAL_OBJECT)  # 取得相关的实际对象
                # 按相关性排序
                if not reals and createNewReal:  # 如果没找到，创建新的对象
                    from loongtian.nvwa.models.realObject import RealObject
                    real = RealObject.createRealByMeta(meta, checkExist=False,
                                                       recordInDB=recordInDB)  # checkExist=False，上面已经找过了
                    real._isFromDB = recordInDB
                    real._isNewCreated = True
                    # 下面对meta的realObjs进行排序（这里只有一个，是从内存中取得的，目的是产生sorted_typed_objects）
                    reals = meta.Layers.getLowerEntitiesByType(ObjType.REAL_OBJECT)

                if reals and len(reals) > 0:
                    # 下面对meta的realObjs进行排序
                    sorted_reals = reals.sort()
                    relatedRealObjs = RelatedRealObjs()
                    relatedRealObjs.extend(sorted_reals)
                    realLowerObjs.append(reals)
                    sorted_realsChain.append(relatedRealObjs)
            elif isinstance(meta, list):
                temp_realLowerObjs, temp_realChain = MetaData.getAllRelatedRealObjsInMetaChain(meta,
                                                                                               recordInDB=recordInDB)
                realLowerObjs.append(temp_realLowerObjs)
                sorted_realsChain.append(temp_realChain)
            else:
                raise Exception("在meta_chain中存在非metadata或[metadata]对象！")

        return realLowerObjs, sorted_realsChain



    def __repr__(self):
        return "{MetaData:{id:%s,mvalue:%s,type:%s,recognized:%s}}" % (
            self.id, self.mvalue, ObjType.getName(self.type), self.recognized)
