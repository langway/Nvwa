#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

import copy
from loongtian.nvwa import settings
from loongtian.nvwa.models.diGraphEntity import DiGraphEntity
from loongtian.nvwa.models.enum import ObjType
from loongtian.nvwa.organs.character import Character


class Layer(DiGraphEntity):
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
    startid 上一级对象ID，RID或mnid。
    utype 上一级对象ID的类型，使用IdTypeEnum枚举。
    endid 下一级对象ID，RID或mnid。
    ltype 下一级对象ID的类型，使用IdTypeEnum枚举。
    weight 阀值，用于遗忘或凝固。
    isdel 逻辑删除标记
    """
    __tablename__ = settings.db.tables.tbl_layer  # 所在表。与Flask统一

    isChainedObject = False  # 是否是链式对象的标记（metaNet、Knowledge等）

    # Layer没有分层对象
    upperLimitation = None
    lowerLimitation = None

    def __init__(self, start=None, end=None, stype=None, etype=None,
                 weight=Character.Original_Link_Weight,
                 createrid=None,
                 createtime=None, updatetime=None, lasttime=None,
                 status=200,  # 状态; 0-不可用(逻辑删除);200-正常;800-不可遗忘
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

        super(Layer, self).__init__(start=start, end=end, stype=stype, etype=etype,
                                    weight=weight,
                                    createrid=createrid,
                                    createtime=createtime, updatetime=updatetime, lasttime=lasttime,
                                    status=status,  # 状态; 0-不可用(逻辑删除);200-正常;800-不可遗忘
                                    memory=memory)

        self.type = ObjType.LAYER # 总是返回LAYER类型


    def __repr__(self):
        return "{Layer:{lid:%s}}" % (self.id)
