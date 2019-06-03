#!/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = 'Leon'

"""
女娲系统内部操作使用的对象的封装类，包括直觉对象、操作对象。
"""

from loongtian.nvwa.models.metaData import MetaData
from loongtian.nvwa.models.enum import ObjType
from loongtian.nvwa.language import InstinctsText, InstinctsErrors
from loongtian.nvwa.organs.character import Character


class _Instincts(object):
    """
    [运行时对象]直觉对象的封装类。
    """

    def __init__(self):
        """
        [运行时对象]直觉对象的封装类。
        """
        self.InstinctsIdDict = {}  # 所有直觉（包括属性、组件等顶级关系，意思是等分层“标签”）
        self.InstinctsMValueDict = {}  # 所有直觉（包括属性、组件等顶级关系，意思是等分层“标签”）

        self._AllInstincts = []  # 所有直觉对象的列表
        self._AllInstinctIds = []  # 所有直觉对象id的列表
        self.TopRelations = []  # 所有顶级关系对象的列表
        self.TopRelationIds =[] # 所有顶级关系对象id的列表
        self.Originals = []  # 所有"元"对象的列表
        self.OriginalIds = []  # 所有"元"对象id的列表
        ######################################
        #    直觉对象（系统内置）
        ######################################
        # 元对象（基础对象）
        self.instinct_none = None  # 无
        self.instinct_original_object = None  # 元对象
        self.instinct_original_knowledge = None  # 元知识链

        # 任意对象（需求解）
        self.instinct_original_anything = None # 需要对其进行数据库查询匹配、求解操作的任何对象（只在内存中存在，不记录数据库）。

        # 集合
        self.instinct_original_collection = None  # 元集合
        self.instinct_original_next = None  # 下一个为
        self.instinct_original_ellipsis = None  # 集合中的省略元素
        # 内部集合标记（k1     k0     List，将k0包裹在集合中）
        self.instinct_original_list = None  # 内部集合标记

        # 元占位符2018-09-02 取消，否则无法计算有多少个占位符，直接用realobject的type表示
        # self.instinct_original_placeholder = None
        # 构成
        self.instinct_ingredient = None  # 成分为
        self.instinct_attribute = None  # 属性为
        self.instinct_component = None  # 组件为
        self.instinct_action = None  # 动作为
        self.instinct_parent = None  # 父对象为。顶级关系中，只有父对象无值，因为父对象本身就是对象的类，就是值！
        self.instinct_belongs = None  # 所属物为
        self.instinct_relevancy = None  # 相关物为（牛的相关物对象，可能是牧童，也可能是青草。相关物对象是等待进一步建立关系的对象，这种关系是人类社会对对象的各种定义）

        self.instinct_meaning = None  # 意义为 # meaning不是top relation，是一种曲折线性对象的动作

        # 保证同一性的操作（两个对象变一个对象，同步Id）
        self.instinct_realSynchronizer = None

        # 观察者
        self.instinct_observer = None  # 观察者为
        # 女娲本身
        self.instinct_nvwa_ai = None  # 女娲智能的母体对象，所有的用户智能助理均继承自instinct_nvwa_ai。可以进行前期设定，例如：instinct_nvwa_ai 有 建模引擎

        # 代码，关联女娲世界与代码世界
        self.instinct_original_code = None
        self.instinct_original_code_language = None

        # 构成距离
        # 构成距离>=0.0,<0.1 为元对象（零点对象）及其派生类，无值
        self.distance_instinct_original_object = 0.0  # 元对象
        self.distance_instinct_original_knowledge = 0.01  # 元知识链
        self.distance_instinct_original_collection = 0.02  # 元集合
        # 构成距离>=0.1,<=1.0 为对象内部构成类，有值
        self.distance_instinct_ingredient = 0.1  # 成分为
        self.distance_instinct_attribute = 0.2  # 属性为
        self.distance_instinct_component = 0.3  # 组件为
        # 构成距离>1.0,<2.0 为对象外部构成类，有值（只有父对象无值，因为父对象本身就是对象的类）
        self.distance_instinct_action = 1.1  # 动作为
        self.distance_instinct_parent = 1.2  # 父对象为
        self.distance_instinct_belongs = 1.3  # 所属物为
        self.distance_instinct_relevancy = 1.5  # 相关物为

        self.distance_instinct_anything = 1.5  # 相关物为
        # 观察者是对对象构成的提供者
        self.distance_instinct_observer = 2.0  # 观察者为

    def _createMetas(self, memory=None):
        """
        加载元数据
        :return:
        """
        ######################################
        #    元数据对象（系统内置）
        ######################################

        # 元对象（基础对象）
        self.meta_none = MetaData(mvalue=InstinctsText.none,
                                  weight=Character.System_Obj_Weight * 9,
                                  status=800,
                                  memory=memory).create()
        self.meta_original_object = MetaData(mvalue=InstinctsText.original_object,
                                             weight=Character.System_Obj_Weight * 9,
                                             status=800,
                                             memory=memory).create()
        self.meta_original_knowledge = MetaData(mvalue=InstinctsText.original_knowledge,
                                                weight=Character.System_Obj_Weight * 9,
                                                status=800,
                                                memory=memory).create()

        # 任意对象（需求解）
        self.meta_original_anything = MetaData(mvalue=InstinctsText.original_anything,
                                                weight=Character.System_Obj_Weight * 9,
                                                status=800,
                                                memory=memory).create()

        # 集合
        self.meta_original_collection = MetaData(mvalue=InstinctsText.original_collection,
                                                 weight=Character.System_Obj_Weight * 9,
                                                 status=800,
                                                 memory=memory).create()
        self.meta_original_next = MetaData(mvalue=InstinctsText.original_next,
                                           weight=Character.System_Obj_Weight * 9,
                                           status=800,
                                           memory=memory).create()
        # 集合中的省略元素
        self.meta_original_ellipsis = MetaData(mvalue=InstinctsText.original_ellipsis,
                                               weight=Character.System_Obj_Weight * 9,
                                               status=800,
                                               memory=memory).create()
        # 内部集合标记（k1     k0     List，将k0包裹在集合中）2019-01-31：经慎重思考，女娲系统内部操作可向外部显现（leon）
        self.meta_original_list = MetaData(mvalue=InstinctsText.original_list,
                                           weight=Character.System_Obj_Weight * 9,
                                           status=800,
                                           memory=memory).create()

        # 元占位符,2018-09-02 取消，否则无法计算有多少个占位符，直接用realobject的type表示
        # self.meta_original_placeholder=MetaData(mvalue = "元占位符",weight=instinct_weight*9).create()

        # 构成
        self.meta_ingredient = MetaData(mvalue=InstinctsText.ingredient,
                                        weight=Character.System_Obj_Weight * 8,
                                        status=800, memory=memory).create()
        self.meta_attribute = MetaData(mvalue=InstinctsText.attribute,
                                       weight=Character.System_Obj_Weight * 7,
                                       status=800,
                                       memory=memory).create()
        self.meta_component = MetaData(mvalue=InstinctsText.component,
                                       weight=Character.System_Obj_Weight * 6,
                                       status=800,
                                       memory=memory).create()
        self.meta_parent = MetaData(mvalue=InstinctsText.parent,
                                    weight=Character.System_Obj_Weight * 5, status=800,
                                    memory=memory).create()
        # self.meta_contrary=MetaData(mvalue = "相反为",weight=instinct_weight).create()
        # self.meta_equivalent=MetaData(mvalue = "相同为",weight=instinct_weight).create()
        self.meta_belongs = MetaData(mvalue=InstinctsText.belongs,
                                     weight=Character.System_Obj_Weight * 4,
                                     status=800,
                                     memory=memory).create()
        self.meta_relevancy = MetaData(mvalue=InstinctsText.relevancy,
                                       weight=Character.System_Obj_Weight * 3,
                                       status=800,
                                       memory=memory).create()
        self.meta_action = MetaData(mvalue=InstinctsText.action,
                                    weight=Character.System_Obj_Weight * 3,
                                    status=800,
                                    memory=memory).create()

        # 模式创建使用，2018-07-04 不再使用意思、指、指的是等含义太多的对象
        # meaning不是top relation，是一种曲折线性对象的动作
        self.meta_meaning1 = MetaData(mvalue=InstinctsText.meaning1,
                                      weight=Character.System_Obj_Weight * 10,
                                      status=800,
                                      memory=memory).create()
        self.meta_meaning2 = MetaData(mvalue=InstinctsText.meaning2,
                                      weight=Character.System_Obj_Weight * 10,
                                      status=800,
                                      memory=memory).create()
        self.meta_meaning3 = MetaData(mvalue=InstinctsText.meaning3,
                                      weight=Character.System_Obj_Weight * 10,
                                      status=800,
                                      memory=memory).create()
        self.meta_meaning4 = MetaData(mvalue=InstinctsText.meaning4,
                                      weight=Character.System_Obj_Weight * 10,
                                      status=800,
                                      memory=memory).create()
        self.meta_meaning5 = MetaData(mvalue=InstinctsText.meaning5,
                                      weight=Character.System_Obj_Weight * 10,
                                      status=800,
                                      memory=memory).create()
        self.meta_meaning6 = MetaData(mvalue=InstinctsText.meaning6,
                                      weight=Character.System_Obj_Weight * 10,
                                      status=800,
                                      memory=memory).create()

        # 保证同一性的操作（两个对象变一个对象，同步Id）
        self.meta_realSynchronizer = MetaData(mvalue=InstinctsText.realSynchronizer,
                                      weight=Character.System_Obj_Weight * 10,
                                      status=800,
                                      memory=memory).create()

        # 观察者
        self.meta_observer = MetaData(mvalue=InstinctsText.observer,
                                      weight=Character.System_Obj_Weight * 10,
                                      status=800,
                                      memory=memory).create()
        # 女娲本身
        self.meta_nvwa_ai = MetaData(mvalue=InstinctsText.nvwa_ai,
                                     weight=Character.System_Obj_Weight * 10,
                                     status=800,
                                     memory=memory).create()
        # meta_self = MetaData(mvalue=InstinctsText.self, weight=instinct_weight * 10).create()

        # 代码，关联女娲世界与代码世界
        self.meta_original_code = MetaData(mvalue=InstinctsText.original_code,
                                           weight=Character.System_Obj_Weight * 10,
                                           status=800,
                                           memory=memory).create()
        self.meta_original_code_language = MetaData(mvalue=InstinctsText.original_code_language,
                                                    weight=Character.System_Obj_Weight * 10,
                                                    status=800,
                                                    memory=memory).create()

        self.mvalue_metas_dict = {
            # 元对象（基础对象）
            self.meta_none.mvalue: self.meta_none,
            self.meta_original_object.mvalue: self.meta_original_object,
            self.meta_original_knowledge.mvalue: self.meta_original_knowledge,

            # self.meta_original_anything.mvalue:self.meta_original_anything,

            # 集合
            self.meta_original_collection.mvalue: self.meta_original_collection,
            self.meta_original_next.mvalue: self.meta_original_next,
            self.meta_original_ellipsis.mvalue: self.meta_original_ellipsis,
            # 内部集合标记（k1     k0     List，将k0包裹在集合中）
            self.meta_original_list.mvalue: self.meta_original_list,

            # self.meta_original_placeholder.mvalue:self.meta_original_placeholder,

            # 构成
            self.meta_ingredient.mvalue: self.meta_ingredient,
            self.meta_attribute.mvalue: self.meta_attribute,
            self.meta_component.mvalue: self.meta_component,
            self.meta_parent.mvalue: self.meta_parent,
            self.meta_belongs.mvalue: self.meta_belongs,
            self.meta_relevancy.mvalue: self.meta_relevancy,
            self.meta_action.mvalue: self.meta_action,

            # meaning不是top relation，是一种曲折线性对象的动作
            self.meta_meaning1.mvalue: self.meta_meaning1,

            # 观察者
            self.meta_observer.mvalue: self.meta_observer,
            # 女娲本身
            self.meta_nvwa_ai.mvalue: self.meta_nvwa_ai,

            # 代码，关联女娲世界与代码世界
            self.meta_original_code.mvalue: self.meta_original_code,
            self.meta_original_code_language.mvalue: self.meta_original_code_language,

        }

        self.meta_meanings = [
            self.meta_meaning2,
            self.meta_meaning3,
            self.meta_meaning4,
            self.meta_meaning5,
            self.meta_meaning6,
        ]

    def _createInstinctByMeta(self, meta,realType=ObjType.INSTINCT):
        """
        根据元数据创建直觉实际对象
        :param meta:
        :return:
        """

        from loongtian.nvwa.models.realObject import RealObject
        real = RealObject.createRealByMeta(meta, weight=meta.weight, checkExist=True,
                                           realType=realType, status=800,
                                           recordInDB=True)
        self.InstinctsIdDict[real.id] = real
        self.InstinctsMValueDict[meta.mvalue] = real
        if meta is self.meta_meaning1:
            for meta_meaning in self.meta_meanings:
                meta_meaning.create()
                meta_meaning.Layers.addLower(real, weight=meta_meaning.weight)
                real.Layers.addUpper(meta_meaning, weight=meta_meaning.weight, recordInDB=False)  # 已经添加过数据库了
                self.InstinctsIdDict[real.id] = real
        return real

    def _createAllInstincts(self):
        """
        创建所有直觉（包括属性、组件等顶级关系，意思是等分层“标签”）
        :return:
        """
        try:
            # 元对象（基础对象）
            self.instinct_none = self._createInstinctByMeta(self.meta_none)
            self.instinct_original_object = self._createInstinctByMeta(self.meta_original_object)
            self.instinct_original_knowledge = self._createInstinctByMeta(self.meta_original_knowledge)

            # 这里有个特殊的存在：任意对象（需求解）
            # 需要对其进行数据库查询匹配、求解操作的任何对象。(类型不能设为ObjType.INSTINCT，否则会跟其他动作粘连，例如：牛有什么)
            self.instinct_original_anything = self._createInstinctByMeta(self.meta_original_anything)
            self.instinct_original_anything.type=ObjType.VIRTUAL
            # 集合
            self.instinct_original_collection = self._createInstinctByMeta(self.meta_original_collection)
            self.instinct_original_next = self._createInstinctByMeta(self.meta_original_next)
            self.instinct_original_ellipsis = self._createInstinctByMeta(self.meta_original_ellipsis)

            # 内部集合标记（k1     k0     List，将k0包裹在集合中）
            self.instinct_original_list = self._createInstinctByMeta(self.meta_original_list)

            # 弃用，直接使用realobject.type定义
            # self.instinct_original_placeholder=self.createInstinctByMeta(self.meta_original_placeholder)

            # 构成
            self.instinct_ingredient = self._createInstinctByMeta(self.meta_ingredient)
            self.instinct_attribute = self._createInstinctByMeta(self.meta_attribute)
            self.instinct_component = self._createInstinctByMeta(self.meta_component)
            self.instinct_parent = self._createInstinctByMeta(self.meta_parent)
            self.instinct_belongs = self._createInstinctByMeta(self.meta_belongs)
            self.instinct_relevancy = self._createInstinctByMeta(self.meta_relevancy)
            self.instinct_action = self._createInstinctByMeta(self.meta_action)

            # meaning不是top relation，是一种曲折线性对象的动作
            self.instinct_meaning = self._createInstinctByMeta(self.meta_meaning1)

            # 保证同一性的操作（两个对象变一个对象，同步Id）
            self.instinct_realSynchronizer=self._createInstinctByMeta(self.meta_realSynchronizer)

            # 观察者
            self.instinct_observer = self._createInstinctByMeta(self.meta_observer)
            # 女娲对象本身
            self.instinct_nvwa_ai = self._createInstinctByMeta(self.meta_nvwa_ai)

            # 代码，关联女娲世界与代码世界
            self.instinct_original_code = self._createInstinctByMeta(self.meta_original_code)
            self.instinct_original_code_language = self._createInstinctByMeta(self.meta_original_code_language)

            # 弃用，直接使用realobject.type定义
            # _self.instinct_original_placeholder,])
            # 加载直觉对象到列表
            self._loadInstinctsToList()

            return self._AllInstincts
        except Exception as e:
            raise Exception(InstinctsErrors.Can_Not_Create_Instinct % str(e))

    def _loadInstinctsToList(self):
        """
        加载直觉对象到列表
        :return:
        """

        # 添加到直觉对象列表
        self._AllInstincts.extend([
            # 元对象（基础对象）
            self.instinct_none,
            self.instinct_original_object,
            self.instinct_original_knowledge,

            # 任意对象（需求解）
            self.instinct_original_anything,

            #  集合
            self.instinct_original_collection,
            self.instinct_original_next,
            self.instinct_original_ellipsis,
            self.instinct_original_list,
            # 弃用，直接使用realobject.type定义
            # _self.instinct_original_placeholder,

            # 构成
            self.instinct_ingredient,
            self.instinct_attribute,
            self.instinct_component,
            self.instinct_parent,
            self.instinct_belongs,
            self.instinct_relevancy,
            self.instinct_action,
            self.instinct_observer,

            # meaning不是top relation，是一种曲折线性对象的动作
            self.instinct_meaning,

            # 保证同一性的操作（两个对象变一个对象，同步Id）
            self.instinct_realSynchronizer,

            # 女娲自身定义
            self.instinct_nvwa_ai,

            # 代码，关联女娲世界与代码世界
            self.instinct_original_code,
            self.instinct_original_code_language,

        ])
        self.TopRelations.extend([
            self.instinct_ingredient,
            self.instinct_attribute,
            self.instinct_component,
            self.instinct_action,
            self.instinct_parent,
            self.instinct_belongs,
            self.instinct_relevancy,
            # _self.instinct_meaning, # meaning不是top relation，是一种曲折线性对象的动作
        ])

        self.TopRelationIds.extend([
            self.instinct_ingredient.id,
            self.instinct_attribute.id,
            self.instinct_component.id,
            self.instinct_action.id,
            self.instinct_parent.id,
            self.instinct_belongs.id,
            self.instinct_relevancy.id,
            # _self.instinct_meaning, # meaning不是top relation，是一种曲折线性对象的动作
        ])

        self.Originals.extend([
            # 元对象（基础对象）
            self.instinct_original_object,
            self.instinct_original_knowledge,
            self.instinct_original_collection,

            # 代码，关联女娲世界与代码世界
            self.instinct_original_code,
            self.instinct_original_code_language,
        ])

        self.OriginalIds.extend([
            # 元对象（基础对象）
            self.instinct_original_object.id,
            self.instinct_original_knowledge.id,
            self.instinct_original_collection.id,

            # 代码，关联女娲世界与代码世界
            self.instinct_original_code.id,
            self.instinct_original_code_language.id,
        ])

    def _checkInstincts(self):
        """
        检查加载的直觉是否符合nvwa内部定义
        :return:
        """
        li1 = list(self.InstinctsMValueDict.keys())
        li1.sort()
        li2 = list(self.mvalue_metas_dict.keys())
        li2.sort()
        return li1 == li2

    def loadAllInstincts(self, forceToReload=False, memory=None):
        """
        加载所有直觉（包括属性、组件等顶级关系，意思是等分层“标签”）
        :param forceToReload:
        :return:
        """
        # 如果已加载，直接返回内存结果
        if not forceToReload and len(self.InstinctsIdDict) > 0:
            return list(self.InstinctsIdDict.values())

        # 加载元数据
        self._createMetas(memory=memory)

        # 从数据库加载
        try:
            from loongtian.nvwa.models.realObject import RealObject
            instincts = RealObject.getAllByConditionsInDB(memory=memory, type=ObjType.INSTINCT)

            # 首先加载父对象

            # 记录到内存中
            if instincts:
                if isinstance(instincts, list):
                    # 首先加载父对象
                    for instinct in instincts:
                        if instinct.remark == self.meta_parent.mvalue:
                            # 将数据库加载的直觉对象与当前类中的定义对象关联在一起
                            self._setInstinct(instinct)
                            break
                    for instinct in instincts:
                        if instinct.remark == self.meta_parent.mvalue:
                            continue
                        # 将数据库加载的直觉对象与当前类中的定义对象关联在一起
                        self._setInstinct(instinct)
                    # 加载直觉对象到列表
                    self._loadInstinctsToList()
                else:
                    self._setInstinct(instincts)

                if not self._checkInstincts():
                    instincts = self._createAllInstincts()
            else:
                instincts = self._createAllInstincts()


            return instincts
        except Exception as e:
            raise Exception(InstinctsErrors.Load_Instincts_Failure + str(e))

    def _setInstinct(self, instinct):
        """
        将数据库加载的直觉对象与当前类中的定义对象关联在一起
        :param instinct:
        :return:
        """
        self.InstinctsIdDict[instinct.id] = instinct
        if instinct.remark:
            self.InstinctsMValueDict[instinct.remark] = instinct

        # 将instinct赋予_Instincts中的对象
        # 元对象（基础对象）
        if instinct.remark == self.meta_none.mvalue:
            self.instinct_none = instinct
            self.meta_none.Layers.addLower(instinct, recordInDB=False)  # 关联meta和real
        elif instinct.remark == self.meta_original_object.mvalue:
            self.instinct_original_object = instinct
            self.meta_original_object.Layers.addLower(instinct, recordInDB=False)  # 关联meta和real
        elif instinct.remark == self.meta_original_knowledge.mvalue:
            self.instinct_original_knowledge = instinct
            self.meta_original_knowledge.Layers.addLower(instinct, recordInDB=False)  # 关联meta和real

        # 任意对象（需求解）
        elif instinct.remark == self.meta_original_anything.mvalue:
            self.instinct_original_anything = instinct
            self.instinct_original_anything.type = ObjType.VIRTUAL
            self.meta_original_anything.Layers.addLower(instinct, recordInDB=False)  # 关联meta和real

        # 集合
        elif instinct.remark == self.meta_original_collection.mvalue:
            self.instinct_original_collection = instinct
            self.meta_original_collection.Layers.addLower(instinct, recordInDB=False)  # 关联meta和real
        elif instinct.remark == self.meta_original_next.mvalue:
            self.instinct_original_next = instinct
            self.meta_original_next.Layers.addLower(instinct, recordInDB=False)  # 关联meta和real
        elif instinct.remark == self.meta_original_ellipsis.mvalue:
            self.instinct_original_ellipsis = instinct
            self.meta_original_ellipsis.Layers.addLower(instinct, recordInDB=False)  # 关联meta和real
        elif instinct.remark == self.meta_original_list.mvalue:  # 内部集合标记（k1     k0     List，将k0包裹在集合中）
            self.instinct_original_list = instinct
            self.meta_original_list.Layers.addLower(instinct, recordInDB=False)  # 关联meta和real

        # 弃用，直接使用realobject.type定义
        # elif instinct.remark==_self.meta_original_placeholder.mvalue:
        #     _self.meta_original_placeholder=instinct

        # 构成
        elif instinct.remark == self.meta_ingredient.mvalue:
            self.instinct_ingredient = instinct
            self.meta_ingredient.Layers.addLower(instinct, recordInDB=False)  # 关联meta和real
        elif instinct.remark == self.meta_attribute.mvalue:
            self.instinct_attribute = instinct
            self.meta_attribute.Layers.addLower(instinct, recordInDB=False)  # 关联meta和real
        elif instinct.remark == self.meta_component.mvalue:
            self.instinct_component = instinct
            self.meta_component.Layers.addLower(instinct, recordInDB=False)  # 关联meta和real
        elif instinct.remark == self.meta_parent.mvalue:
            self.instinct_parent = instinct
            self.meta_parent.Layers.addLower(instinct, recordInDB=False)  # 关联meta和real
        elif instinct.remark == self.meta_belongs.mvalue:
            self.instinct_belongs = instinct
            self.meta_belongs.Layers.addLower(instinct, recordInDB=False)  # 关联meta和real
        elif instinct.remark == self.meta_relevancy.mvalue:
            self.instinct_relevancy = instinct
            self.meta_relevancy.Layers.addLower(instinct, recordInDB=False)  # 关联meta和real
        elif instinct.remark == self.meta_meaning1.mvalue:
            self.instinct_meaning = instinct
            self.meta_meaning1.Layers.addLower(instinct, recordInDB=False)  # 关联meta和real
            self.meta_meaning2.Layers.addLower(instinct, recordInDB=False)  # 关联meta和real
            self.meta_meaning3.Layers.addLower(instinct, recordInDB=False)  # 关联meta和real
            self.meta_meaning4.Layers.addLower(instinct, recordInDB=False)  # 关联meta和real
            self.meta_meaning5.Layers.addLower(instinct, recordInDB=False)  # 关联meta和real
            self.meta_meaning6.Layers.addLower(instinct, recordInDB=False)  # 关联meta和real
        elif instinct.remark == self.meta_action.mvalue:
            self.instinct_action = instinct
            self.meta_action.Layers.addLower(instinct, recordInDB=False)  # 关联meta和real
        elif instinct.remark == self.meta_observer.mvalue:
            self.instinct_observer = instinct
            self.meta_observer.Layers.addLower(instinct, recordInDB=False)  # 关联meta和real
        # 保证同一性的操作（两个对象变一个对象，同步Id）
        elif instinct.remark == self.meta_realSynchronizer.mvalue:
            self.instinct_realSynchronizer = instinct
            self.meta_realSynchronizer.Layers.addLower(instinct, recordInDB=False)  # 关联meta和real
        elif instinct.remark == self.meta_nvwa_ai.mvalue:
            self.instinct_nvwa_ai = instinct
            self.meta_nvwa_ai.Layers.addLower(instinct, recordInDB=False)  # 关联meta和real

        # 代码，关联女娲世界与代码世界
        elif instinct.remark == self.meta_original_code.mvalue:
            self.instinct_original_code = instinct
            self.meta_original_code.Layers.addLower(instinct, recordInDB=False)  # 关联meta和real
        elif instinct.remark == self.meta_original_code_language.mvalue:
            self.instinct_original_code_language = instinct
            self.meta_original_code_language.Layers.addLower(instinct, recordInDB=False)  # 关联meta和real
        else:
            raise Exception("未知的直觉对象")

    def getConstituentDistance(self, instinct):
        """
        取得构成距离
        :param instinct:
        :return:
        """
        if not hasattr(instinct, "id"):
            return -1

        elif instinct.id == self.instinct_original_object.id:  # 元对象
            return self.distance_instinct_original_object
        elif instinct.id == self.instinct_original_knowledge.id:  # 元知识链
            return self.distance_instinct_original_knowledge
        # 集合
        elif instinct.id == self.instinct_original_collection.id:  # 元集合
            return self.distance_instinct_original_collection

        # elif instinct.id == self.instinct_original_anything.id:  # 元集合
        #     return self.distance_instinct_original_anything

        # 构成
        elif instinct.id == self.instinct_ingredient.id:  # 成分为
            return self.distance_instinct_ingredient
        elif instinct.id == self.instinct_attribute.id:  # 属性为
            return self.distance_instinct_attribute
        elif instinct.id == self.instinct_component.id:  # 组件为
            return self.distance_instinct_component
        elif instinct.id == self.instinct_action.id:  # 动作为
            return self.distance_instinct_action
        elif instinct.id == self.instinct_parent.id:  # 父对象为
            return self.distance_instinct_parent
        elif instinct.id == self.instinct_belongs.id:  # 所属物为
            return self.distance_instinct_belongs
        elif instinct.id == self.instinct_relevancy.id:  # 相关物为（牛的相关物对象，可能是牧童，也可能是青草。相关物对象是等待进一步建立关系的对象，这种关系是人类社会对对象的各种定义）
            return self.distance_instinct_relevancy
        elif instinct.id == self.instinct_observer.id:  # 相关物为（牛的相关物对象，可能是牧童，也可能是青草。相关物对象是等待进一步建立关系的对象，这种关系是人类社会对对象的各种定义）
            return self.distance_instinct_observer

        else:
            return -1

    def hasConstituentValue(self, instinct):
        """
        是否有构成的值（内部值），例如：牛-组件-腿，值就是一个（或多个）父对象为腿的实际对象
        :param instinct:
        :return:
        """

        distance = self.getConstituentDistance(instinct)
        if distance >= 0.0:
            if instinct.id == self.instinct_parent.id:  # 顶级关系中，只有父对象无值，因为父对象本身就是对象的类，就是值！
                return False
            return True

    @staticmethod
    def hasInstinctMeaning(reals):
        """
        当前实际对象链是否需要创建意义（包含直觉意义对象）
        :return:
        """
        from loongtian.nvwa.models.realObject import RealObject
        for real in reals:
            if isinstance(real,RealObject) and Instincts.instinct_meaning.id == real.id:
                return True

        return False


# 向外部显现直觉对象
Instincts = _Instincts()
