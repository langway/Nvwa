#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

import copy
from loongtian.nvwa import settings
from loongtian.nvwa.models.enum import ObjType
from loongtian.nvwa.models.diGraphEntity import DiGraphEntity
from loongtian.nvwa.organs.character import Character


class Observer(DiGraphEntity):
    """
    数据对象与观察者之间的关联关系（实现管理员数据对象与用户数据对象分离，相当于Layer的分表）
    """
    __tablename__ = settings.db.tables.tbl_observer # 所在表。与Flask统一
    columns = copy.copy(DiGraphEntity.columns)  # 模型对应的非主键的全部字段
    columns.remove("stype") # upper的类型无需考虑

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

        super(Observer, self).__init__(start=start, end=end, stype=stype, etype=etype,
                                    weight=weight,
                                    createrid=createrid,
                                    createtime=createtime, updatetime=updatetime, lasttime=lasttime,
                                    status=status,  # 状态; 0-不可用(逻辑删除);200-正常;800-不可遗忘
                                    memory=memory)

        self.type=ObjType.OBSERVER # 总是返回OBSERVER类型



    def __repr__(self):
        return "{Observer:{oid:%s}}" % (self.id)
