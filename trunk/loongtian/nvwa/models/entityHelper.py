#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

from loongtian.nvwa.models.enum import ObjType
from loongtian.nvwa.models.metaData import MetaData
from loongtian.nvwa.models.metaNet import MetaNet
from loongtian.nvwa.models.realObject import RealObject
from loongtian.nvwa.models.knowledge import Knowledge
from loongtian.nvwa.models.observer import Observer
from loongtian.nvwa.models.layer import Layer

def getEntityByTypeAndId(entityType=ObjType.UNKNOWN,id=None,memory=None):
    """
    根据对象的类型及Id取得对应的对象（包括：MetaData、MetaNet、RealObject、Knowledge）
    :param entityType:
    :param id:
    :param memory:
    :return:
    """
    entity=None

    if ObjType.isMetaData(entityType):
        entity = MetaData.getOne(memory=memory, id=id)
    elif ObjType.isMetaNet(entityType):
        entity = MetaNet.getOne(memory=memory, id=id)
    elif ObjType.isRealObject(entityType):
        entity = RealObject.getOne(memory=memory, id=id)
    elif ObjType.isKnowledge(entityType):
        entity = Knowledge.getOne(memory=memory, id=id)
    elif ObjType.isLayer(entityType):
        entity = Layer.getOne(memory=memory, id=id)
    elif ObjType.isObserver(entityType):
        entity = Observer.getOne(memory=memory, id=id)
    # elif ObjType.isCollection(entityType):
    #     entity = Collection.getOne(cid = id)
    else:
        raise Exception("对象类型错误：{%d:%s}。" % (entityType, ObjType.getTypeNames(entityType)))

    return entity


def getNatureLanguage(obj,seperator=None):
    """
    取得对象的自然语言
    :param obj:
    :return:
    """
    if seperator is None:
        seperator=","
    if isinstance(obj, RealObject):
        return obj.remark
    elif isinstance(obj, MetaData):
        return obj.mvalue
    elif isinstance(obj, MetaNet):
        obj.getSequenceComponents()
        return obj._t_chain_words
    elif isinstance(obj, Knowledge):
        components = obj.getSequenceComponents()
        return getNatureLanguage(components)
    elif isinstance(obj, list) or isinstance(obj, tuple):
        nl = "["
        for _obj in obj:
            nl += getNatureLanguage(_obj) + seperator
        nl = nl.rstrip(seperator)
        nl += "]"
        return nl
    elif isinstance(obj, dict):
        nl = "{"
        for id, _obj in obj.items():
            nl += getNatureLanguage(_obj) + seperator
        nl = nl.rstrip(seperator)
        nl += "}"
        return nl

    from loongtian.nvwa.runtime.relatedObjects import RelatedObj
    from loongtian.nvwa.runtime.thinkResult.fragments import (UnknownMeta,UnknownObj)
    from loongtian.nvwa.runtime.meanings import Meaning
    if isinstance(obj, RelatedObj):
        return getNatureLanguage(obj.obj)
    elif isinstance(obj, UnknownMeta):
        return getNatureLanguage(obj.unknown_meta)
    elif isinstance(obj, UnknownObj):
        return getNatureLanguage(obj.unknown_obj)
    elif isinstance(obj, Meaning):
        return getNatureLanguage(obj.toObjChain())
    return ""
