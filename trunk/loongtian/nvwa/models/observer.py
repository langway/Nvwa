#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

import copy
from loongtian.nvwa import settings
from loongtian.nvwa.models.enum import ObjType
from loongtian.nvwa.models.layer import Layer
from loongtian.nvwa.organs.character import Character


class Observer(Layer):
    """
    数据对象与观察者之间的关联关系（实现管理员数据对象与用户数据对象分离，相当于Layer的分表）
    """
    __databasename__ = settings.db.db_nvwa  # 所在数据库。
    __tablename__ = settings.db.tables.tbl_observer # 所在表。与Flask统一
    columns = copy.copy(Layer.columns)  # 模型对应的非主键的全部字段
    columns.remove("utype") # upper的类型无需考虑


    def __init__(self, observer=None, objid=None, objtype=None,
                 weight=Character.Original_Link_Weight,
                 createrid='',
                 createtime=None, updatetime=None, lasttime=None,
                 status=200,  # 状态; 0-不可用(逻辑删除);200-正常;800-不可遗忘
                 memory=None):
        """
        数据对象与观察者之间的关联关系（实现管理员数据对象与用户数据对象分离，相当于Layer的分表）
        :param observer:upper
        :param objid:lower
        :param objtype:ltype
        :param weight:
        :param createrid: 添加人; 格式：(user_id)中文名
        :param createrip: 添加人IP
        :param createtime: 添加时间;
        :param updatetime: 更新时间
        :param lasttime: 最近访问时间
        :param status: 状态; 0-不可用(逻辑删除);200-正常;800-不可遗忘
        :remarks:
        相当于observer1认识一个objid1李明，observer2认识一个objid2李明，observer3也认识objid1李明
        但，observer1对objid1李明的认识是，objid1李明这个人比较好，observer3对objid1李明的认识是，objid1李明这个人比较不好，
        观察者与最终数据的关联，成为认知隔离的最重要方式
        """
        super(Observer, self).__init__(observer, objid,ObjType.USER, objtype, weight,
                                       createrid,
                                       createtime, updatetime, lasttime,
                                       status,memory=memory)
