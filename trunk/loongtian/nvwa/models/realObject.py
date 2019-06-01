#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

import copy
from loongtian.nvwa import settings
from loongtian.nvwa.models.baseEntity import BaseEntity, LayerLimitation
from loongtian.nvwa.models.enum import ObjType
from loongtian.nvwa.models.executionInfo import LinearExecutionInfo,ConjugatedExecutionInfo

from loongtian.nvwa.runtime.collection import Collection
from loongtian.nvwa.runtime.relatedObjects import RelatedObj
from loongtian.nvwa.organs.character import Character


class RealObject(BaseEntity):
    """
    实际对象实体。
    #  2018-12-06:再论RealObject与Knowledge关系：
    # 有两种：1、由Knowledge的所有元素通过迁移引擎生成的RealObject，知识链的所有元素之间是修限关系或是动作执行关系
    #               例如：r:中国-r:人民-r:解放军——>r:中国人民解放军。r:小明-a:打-r:小丽——>r:小明-r:手疼，r:小丽-r:哭
    #         2、从集合的角度考虑，当前知识链本身转化成的实际对象（id相同） ，是由Knowledge的所有元素构成（组件关系）的RealObject。
    #               例如：k:{r:中国-r:人民-r:解放军}——》r:x，r:x-r:父对象-r:集合,r:x-r:组件-r:中国......
    #               其中：k的id 应与 r:x的id相同
    :parameter
    :attribute
    rid RealObjectID，UUID。
    # pattern RealObject的模式（Id）,当RealObject为动词或修限词时。
    # meaning 含义（指的是）（Id），当RealObject为动词或修限词时时。
    remark 备注，一般用于显示。
    WordFrequncyDict 实际对象对应的元数据的集合。格式为：{id:(MetaData,threshhold)}，一个RealObjectEntity对应多个MetaDataEntity。
        eg：RealObject:牛 ==> Meta:[牛, cow, 声音牛, 图像牛]
    chains 该标签的被域知识链
    type 实际对象的类型，
        MOTIFIER 修限类
        ACTION 动作类
        EXISTENCE 实对象（可以通过感知器感知的实际存在的对象，例如“爱因斯坦”，“这头牛”，“小明”,可以理解为类的实例）
        VIRTUAL 虚对象（不可以通过感知器感知的不实际存在的对象，例如“牛”，“人类”,是大脑经过抽象提炼出的对象，可以理解为类）
                在人类的语言中，大部分为虚对象
        ### TOP_RELATION 顶级关系（与INSTINCT合并）
        INSTINCT 内置对象（本能，包括顶级关系）
    """
    __databasename__ = settings.db.db_nvwa  # 所在数据库。
    __tablename__ = settings.db.tables.tbl_realObject  # 所在表。与Flask统一
    primaryKey = copy.copy(BaseEntity.primaryKey)
    primaryKey.append("id")
    columns = copy.copy(BaseEntity.columns)
    columns.extend(["type", "remark", "uratio"])
    upperLimitation = LayerLimitation()
    upperLimitation.update({ObjType.META_DATA: -1,  # 有多个
                            ObjType.KNOWLEDGE: -1,  # 有多个
                            # ObjType.COLLECTION: 1,
                            })  # RealObject 的上一层对象，为MetaData[可能有多个]，例如：R牛的MetaData包括：文字牛、图片牛、声音牛等
    # Knowledge[可能有多个],Collection[一个]

    lowerLimitation = LayerLimitation()
    lowerLimitation.update({
        # ObjType.REALOBJECT: 1,
        ObjType.LINEAR_EXE_INFO: -1,  # 有多个模式
        # ObjType.MEANING: 1,
    })  # 在下一层其他对象的分层中，包含的对象类型、数量限制，

    # RealObject只能有一个下层对象RealObject，两个下层对象Knowledge（一个是meaning的头，一个是pattern）
    # RealObject和Knowledge的下一层对象可以解析为：意义为、意思为、指的是、含义为、meaning等

    def __init__(self, id=None, remark=None, type=ObjType.REAL_OBJECT,
                 createrid='',
                 createtime=None, updatetime=None, lasttime=None,
                 status=200,  # 状态; 0-不可用(逻辑删除);200-正常;800-不可遗忘
                 memory=None):
        """
        实际对象实体。
        :param id:
        :param remark:
        :param type:
        :param createrid: 添加人; 格式：(user_id)中文名
        :param createrip: 添加人IP
        :param createtime: 添加时间;
        :param updatetime: 更新时间
        :param lasttime: 最近访问时间
        :param status: 状态; 0-不可用(逻辑删除);200-正常;800-不可遗忘
        """
        super(RealObject, self).__init__(id,
                                         createrid,
                                         createtime, updatetime, lasttime,
                                         status, memory=memory)

        self.type = type # 类型根据外部设置

        self.remark = remark
        self._got_realType = False  # 是否已经取得了realType的标记。如果是UNKNOWN，试图查询数据库取得实际对象类型

        self.uratio = 0.0  # 实际对象已被识别的比率。
        # 如果已经有父对象（除original_object之外）+10.0，n个乘n
        # 有构成（顶级关系） +5.0 ，n个乘n
        # 无构成，但有关联 +1.0，n个乘n

        # ####################################
        #      下面为运行时数据
        # ####################################
        # 对象的所有构成
        self.Constitutions = Constitutions(self)
        # 关联所有集合操作的封装类。
        self.Collection = Collection(self)

        # 实际对象的关系的前、后约束，例如：手机不能进水。牛 - 有 - 腿，腿的前约束，就是组件，便于系统查找和处理关系，避免出现马云 - 有 - 钱，将其处理成马云 - 组件 - 钱的情况。
        self.Connstrains = Connstrains(self)

        self.ExecutionInfo = ExecutionInfo(self)

        # 2018-12-06:所有上下层对象一律在Layers中处理
        # # 从数据库中取得的关联的元数据（可能有多个可能有多个，例如：r:苹果<——m:字符串苹果，m:字符串Apple，m:声音的苹果）
        # self._upper_metas = UpperObjs()
        # # 从数据库中取得的关联的知识链（可能有多个r:中国人民解放军 的知识链，可能就是[r:中国-r:人民-r:解放军]，或是：[r:中国-[r:人民-r:解放军]]）
        # self._upper_knowledges = UpperObjs()

        # 实际对象本身转化成的知识链（id相同） r:中国-r:人民-r:解放军——>r:x,，r:x-r:父对象-r:集合,r:x-r:组件-r:中国......
        self._self_knowledge = None

        self._isSingularity = None  # 一个实际对象是否是奇点对象（孤儿对象。没有任何构成、知识链、动作定义或是在知识链中引用。只在realobject表中，不是知识链、没有以其为start的知识链、不是动作）

    def create(self, checkExist=True, recordInDB=True):
        """
        CRUD - Create
        :return: 返回建立的Entity。
        """
        RealObject.getRealType(self)
        return super(RealObject,self).create(checkExist,recordInDB)


    @staticmethod
    def getRealType(real):
        """
        取得realObject对象的类型。包括：实对象、虚对象、动作、修限符、直觉等。
        如果是UNKNOWN，试图查询数据库取得实际对象类型
        :param real:
        :return:
        """
        # 如果已经判断了实际对象的类型，直接返回该类型
        if real._got_realType == True:
            return real.type

        # 试着通过pattern和meaning定义判断对象类型
        real.ExecutionInfo.getSelfLinearExecutionInfo()

        real._got_realType = True
        return real.type

    # def getType(self):
    #     """
    #     [重载函数]取得当前实际对象的类型。
    #     :return: 当前实际对象的类型。
    #     """
    #     return RealObject.getRealType(self)


    @property
    def Remark(self):
        """
        取得realObject的remark，没有的时候返回id
        :return:
        """
        if self.remark:
            return self.remark
        else:
            return self.id

    @staticmethod
    def createRealByMeta(meta, weight=Character.Original_Link_Weight,
                         checkExist=True, realType=ObjType.REAL_OBJECT,
                         status=200, recordInDB=True):
        """
        根据metaData创建realObject，并添加二者的关系（无需memory，直接取得meta的memory）
        :param meta: 
        :param weight: 
        :param checkExist: 
        :param realType: 
        :param status: 状态; 0-不可用(逻辑删除);200-正常;800-不可遗忘
        :param recordInDB: 是否保存在数据库之中（False只保存在内存）
        :return: 
        """
        if checkExist:
            # 检查是否存在
            reals = meta.Layers.getLowerEntitiesByType(ObjType.REAL_OBJECT)
            if reals:
                for id, real in reals.items():
                    if real.obj.remark == meta.mvalue:
                        return real.obj
                # 如果没有找到对应对象，返回第一个最可能的对象
                reals.sort()
                return reals.sorted_typed_objects[ObjType.REAL_OBJECT][0].obj

        real = RealObject(remark=meta.mvalue,
                          type=realType, status=status,
                          memory=meta.MemoryCentral).create(recordInDB=recordInDB)
        RealObject.addMetaRealRelation(meta, real, weight, recordInDB=recordInDB)
        return real

    def addRelatedMetaData(self, meta, weight=Character.Original_Link_Weight, recordInDB=True):
        """
        将当前实际对象关联到元数据。
        :param meta:
        :param weight:
        :param recordInDB:
        :return:
        """
        self.addMetaRealRelation(meta, self, weight, recordInDB)

    @staticmethod
    def addMetaRealRelation(meta, real, weight=Character.Original_Link_Weight, recordInDB=True):
        """
        添加元数据与实际对象之间的关系
        :param meta:
        :param real:
        :param weight:
        :return:
        """
        meta.Layers.addLower(real, weight, recordInDB=recordInDB)
        real.Layers.addUpper(meta, weight, recordInDB=False)  # 已经添加过数据库了

    @staticmethod
    def createMetaRealByValue(mvalue, metaType=ObjType.WORD,
                              weight=Character.Original_Link_Weight,
                              realType=ObjType.REAL_OBJECT,
                              checkExist=True,
                              recordInDB=False,
                              memory=None):
        """
        根据元数据的值直接创建元数据、实际对象及其关联
        :param metaType:
        :return:
        """
        from loongtian.nvwa.models.metaData import MetaData
        meta = MetaData(type=metaType, mvalue=mvalue, memory=memory).create(checkExist=checkExist,
                                                                            recordInDB=recordInDB)
        real = RealObject.createRealByMeta(meta, weight,
                                           realType=realType,
                                           checkExist=checkExist,
                                           recordInDB=recordInDB)

        return meta, real



    def isExecutable(self):
        """
        当前实际对象是否是可执行性的实际对象（包括Instinct\Action）。
        :return:
        """
        if ObjType.isExecutable(self.getType()):
            return True
        # 取得模式
        executionInfo = self.ExecutionInfo.getSelfLinearExecutionInfo()
        if executionInfo and executionInfo.isExecutable():
            return True
        return False

    def isSelfKnowledge(self):
        """
        判断一个实际对象本身是否是知识链（两者的id相同）。
        :return: 是否知识链,知识链（只能有一个）。
        """
        from loongtian.nvwa.models.knowledge import Knowledge

        self_klg = Knowledge.getOneInDB(memory=self.MemoryCentral,
                                        id=self.id)  # self.Layers.getUpperEntitiesByType(type=ObjType.KNOWLEDGE)
        return not self_klg is None, self_klg

    def getSequenceComponents(self):
        """
        取得排序的组件
        :return:
        """
        return self.Constitutions.getSequenceComponents()

    # # 2018-12-06:所有上下层对象一律在Layers中处理
    # def getUpperMetas(self):
    #     """
    #     取得当前实际对象的上一层元数据（有多个。例如：r:中国人民解放军的元数据，可能就是m:中国人民解放军，m-声音:中国人民解放军）。与当前实际对象转换的元数据不同。
    #     :return:
    #     """
    #     if self._upper_metas is None or len(self._upper_metas)==0:
    #         self._upper_metas = self.Layers.getUpperEntitiesByType(type=ObjType.METADATA)
    #     return self._upper_metas
    #
    # def hasUpperMetas(self):
    #     """
    #     判断一个实际对象是否有上一层元数据（例如：r:中国人民解放军的元数据，可能就是m:中国人民解放军，m-声音:中国人民解放军）。
    #     :return: 是否有上一层元数据（可能一个或多个）。
    #     上层元数据与元数据转实际对象是不同的，[m:中国-m:人民-m:0解放军]=>中国人民解放军，这是上层元数据=>实际对象
    #     [1-2-3-4] ——> 集合（两者的id相同）
    #     """
    #     metas = self.getUpperMetas()
    #     if metas:
    #         return True, metas
    #     return False, None
    #
    # def getUpperKnowledges(self):
    #     """
    #     取得当前实际对象的上一层知识链（例如：r:中国人民解放军 的知识链，可能就是[r:中国-r:人民-r:解放军]，或是：[r:中国-[r:人民-r:解放军]]）。与当前实际对象转换的知识链不同。
    #     :return:
    #     """
    #     if self._upper_knowledges is None or len(self._upper_knowledges)==0:
    #         self._upper_knowledges = self.Layers.getUpperEntitiesByType(type=ObjType.KNOWLEDGE)
    #     return self._upper_knowledges
    #
    # def hasUpperKnowledges(self):
    #     """
    #     判断一个实际对象是否有上一层知识链（例如：中国人民解放军的知识链，可能就是[中国-人民-解放军]，或是：[中国-[人民-解放军]]）。
    #     :return: 是否有上一层知识链（可能一个或多个）。
    #     上层知识链与知识链转实际对象是不同的，[中国-人民-解放军]=>中国人民解放军，这是上层知识链=>实际对象
    #     [1-2-3-4] ——> 集合（两者的id相同）
    #     """
    #     meta_net_matched_knowledges = self.getUpperKnowledges()
    #     if meta_net_matched_knowledges:
    #         return True, meta_net_matched_knowledges
    #     return False, None

    def isTopRelation(self):
        """
        判断一个实际对象是否是顶级关系
        :return:
        """
        from loongtian.nvwa.runtime.instinct import Instincts
        if self.id in Instincts.TopRelationIds:
            return True
        return False

    def isInstinctMeaning(self):
        """
        判断一个实际对象是否是顶级关系-意义为
        :return:
        """
        from loongtian.nvwa.runtime.instinct import Instincts
        return self.id == Instincts.instinct_meaning.id

    def isSame(self, other):
        """
        判断一个实际对象是否是另外一个实际对象（id相同）
        :param other:
        :return:
        """
        if not isinstance(other, BaseEntity):
            return False
        return self.id == other.id

    def isOriginals(self):
        """
        判断一个实际对象是否是“元”对象（元对象、元知识链、元集合）。
        :return:
        """
        from loongtian.nvwa.runtime.instinct import Instincts
        return self in Instincts.Originals

    def isInstincts(self):
        """
        判断一个实际对象是否是“元”对象（元对象、元知识链、元集合）
        :return:
        """
        from loongtian.nvwa.runtime.instinct import Instincts
        return self in Instincts.Instincts

    def isAnything(self):
        """
        判断实际对象是否是Anything及其子对象，例如：什么，谁，哪里，啥，啥时候等
        :param real:
        :return:
        """
        from loongtian.nvwa.runtime.instinct import Instincts
        if self.id == Instincts.instinct_original_anything.id:
            return True
        elif self.Constitutions.isChild(Instincts.instinct_original_anything):
            return True

        return False

    def isPlaceHolder(self):
        """
        判断一个实际对象是否是占位符
        :return:
        """
        return ObjType.isPlaceHolder(self.type)

    def isNone(self):
        """
        判断一个实际对象是否是None
        :return:
        """
        from loongtian.nvwa.runtime.instinct import Instincts
        return self.id == Instincts.instinct_none.id

    def isSingularity(self):
        """
        判断一个实际对象是否是奇点对象（孤儿对象。没有任何构成、知识链、动作定义或是在知识链中引用。只在realobject表中，不是知识链、没有以其为start的知识链、不是动作）
        :return:
        """
        # 如果已经判断过了，直接返回结果
        if not self._isSingularity is None and isinstance(self._isSingularity, bool):
            return self._isSingularity
        # 如果有等价知识链
        if self.isSelfKnowledge()[0]:
            return False
        from loongtian.nvwa.models.knowledge import Knowledge
        if Knowledge.getAllByConditionsInDB(limit=1, memory=self.MemoryCentral, startid=self.id):
            return False
        elif Knowledge.getAllByConditionsInDB(limit=1, memory=self.MemoryCentral, endid=self.id):
            return False
        # 如果是可执行的（执行信息在Layer中关联）
        elif self.isExecutable():
            return False
        return True

    def isRecognized(self):
        """
        实际对象已被识别的比率（识别度，数值越高，说明其被识别的程度越高）。
        :return:
        :remarks:
        如果已经有父对象（除original_object之外）+10.0，n个乘n
        有构成（顶级关系） +5.0 ，n个乘n
        无构成，但有关联 +1.0，n个乘n
        """
        if self.uratio >= 1.0:
            return True
        return False

    def getUnderstoodRatio(self):
        """
        实际对象已被识别的比率。
        :return:
        :remarks:
        如果已经有父对象（除original_object之外）+10.0，n个乘n
        有构成（顶级关系） +5.0 ，n个乘n
        无构成，但有关联 与其他对象关联+1.0，n个乘n；被其他对象关联+0.5，n个乘n
        """
        parents = self.Constitutions.getSelfParentObjects()
        if parents:
            self.uratio += len(parents) * Character.RecognizedRatio.Has_Parent_Ratio
        top_relations = self.Constitutions.getSelfAllTopRelationObjects(getParent=False)
        if top_relations:
            self.uratio += len(top_relations) * Character.RecognizedRatio.toprelation_ratio
        from loongtian.nvwa.models.knowledge import Knowledge
        link_others = Knowledge.getByStartInDB(self, memory=self.MemoryCentral)
        if link_others:
            self.uratio += len(link_others) * Character.RecognizedRatio.link_others_ratio

        other_links = Knowledge.getByEndInDB(self, memory=self.MemoryCentral)
        if other_links:
            self.uratio += len(other_links) * Character.RecognizedRatio.other_links_ratio

        return self.uratio

    def toCollectionKnowledge(self):
        """
        从集合的角度考虑，将当前实际对象的组件转换成代表集合的知识链（id相同）（需考察上下条记录的关系）。
        :return:self._self_knowledge/Non（没有排序组件）
        """
        if self._self_knowledge:
            return self._self_knowledge
        from loongtian.nvwa.models.knowledge import Knowledge
        # 检查是否存在
        self._self_knowledge = Knowledge.getOne(memory=self.MemoryCentral, kid=self.id)
        if self._self_knowledge:
            return self._self_knowledge

        # 如果不存在，取得排序的组件，创建新的
        sequence_components = self.Constitutions.getSequenceComponents()
        # 生成最后的结果
        if sequence_components and isinstance(sequence_components, list):
            temp_klg = Knowledge.createKnowledgeByObjChain(sequence_components, memory=self.MemoryCentral)
            # 同步id
            temp_klg.id = self.id
            temp_klg.updateAttributeValues(id=self.id)
            self._self_knowledge = temp_klg

        return self._self_knowledge

    def toEntityKnowledge(self):
        """
        取得实际对象的迁移来源：知识链实体（上一层知识链）。
        由Knowledge的所有元素通过迁移引擎生成的RealObject，知识链的所有元素之间是修限关系或是动作执行关系
        例如：r:中国-r:人民-r:银行——>r:中国人民银行。
        中国人民银行不是由r:中国-r:人民-r:银行三个组件组成的，
        而是一个父对象-银行，名称中国人民银行，从属于中国......的实体
        :return:
        """
        entity_klgs = self.Layers.getUpperEntitiesByType(ObjType.KNOWLEDGE)
        if entity_klgs:
            return entity_klgs[0].obj

    def isCode(self):
        """
        判断一个实际对象是否是可执行的代码
        :return:
        """
        from loongtian.nvwa.runtime.instinct import Instincts
        return self.Constitutions.isChild(Instincts.instinct_original_code)

    def setType(self, type):
        """
        将当前实际对象设置为指定对象类型
        :return:
        """
        if not self.type == type:
            self.type = type
            self.updateAttributeValues(type=self.type)

    def __repr__(self):
        return "{RealObject:{rid:%s,remark:%s}}" % (self.id, self.remark)

    def addExecutionInfo(self, pattern_klg, meaning_klg, value_placeholder):
        """
        添加可执行性信息
        :param pattern_klg: 模式知识链
        :param meaning_klg: 意义知识链
        :return:
        """
        if not self.LinearExecutionInfo:
            self.LinearExecutionInfo = LinearExecutionInfo(self)
        return self.LinearExecutionInfo.add(pattern_klg, meaning_klg, value_placeholder)


    @staticmethod
    def hasAnything(objs):
        """
        判断实际对象链中是否有Instincts.instinct_original_anything
        :param objs:
        :return:
        """
        for real in objs:
            if isinstance(real, list):
                child_has_anything = RealObject.hasAnything(real)
                if child_has_anything:
                    return True
            elif isinstance(real, RealObject):
                if real.isAnything():
                    return True
        return False


class Constitutions():
    """
    对象的所有构成的封装类。
    """

    def __init__(self, real):
        """
        对象的所有构成的封装类。
        :param real:
        """
        self.real = real

        self._constitute_reals = {}  # 当前实际对象关联的直觉类对象（例如组件对象）。{relation:[obj1,obj2...]}
        self._constitute_knowledges = {}  # 当前实际对象关联的直觉类知识链（例如组件对象）{relation:{cur_k.id:cur_k}}。

        self._inherit_relation = {}  # 这是与当前实际对象最紧密的父对象继承关系
        self._all_parents_relation = {}  # 这是当前实际对象所有父对象的列表及其继承关系
        self._got_inherit_relation = False  # 是否已经取得当前实际对象最紧密的父对象继承关系的标记

        self._all_constitute_objs = {}  # 当前实际对象及父对象关联的所有构成类对象（例如组件对象）。
        self._all_constitute_knowledges = {}  # 当前实际对象及父对象关联的所有构成类知识链（例如组件对象）。

        self._sequence_components = None  # 实际对象的所有序列化组件
        self._sequence_components_klgs = None  # 实际对象的所有序列化组件知识链
        self._sequence_components_sequence_klg = None  # 实际对象的所有序列化组件知识链的序列

    @staticmethod
    def getRealObjsByConstitutions(memory=None, **constitutions):
        """
        根据构成（关联关系-关联对象）取得实际对象。例如：根据颜色-红，形状-圆，可能取得的实际对象包括：苹果，气球等。
        :param relatedObj:
        :return:
        """
        if not constitutions:
            return None
        # 取得以当前实际对象开头，以relatedObj结尾的所有Knowledge
        from loongtian.nvwa.models.knowledge import Knowledge

        relations = constitutions.keys()
        error_msg = "查询条件必须是实际对象、知识链或字符串！"
        # 首先取得符合第一个条件的所有结果（可能有多个）
        first_relations = Constitutions.__getConditionObject(relations[0], error_msg)
        if not first_relations:
            return None
        first_relatedObjs = Constitutions.__getConditionObject(constitutions[first_relations], error_msg)
        if not first_relatedObjs:
            return None

        # 笛卡尔积
        import itertools
        reals = []
        for first_relation, first_relatedObj in itertools.product(*[first_relations, first_relatedObjs]):  # 这里是产生式
            first_related_ks = Knowledge.getAllLikeByStartMiddleEndInDB(attributeName="s_chain", end=first_relatedObj,
                                                                        middles=[first_relation])
            cur_reals = []
            for related_klg in first_related_ks:
                related_klg.getChainItems()
                cur_reals.append(related_klg._head)

            for relation in relations[1:]:  # 从第二个，根据后续的继续查询，去除不符合条件的
                relation = Constitutions.__getConditionObject(relation, error_msg)
                if not relation:
                    return None
                relatedObj = Constitutions.__getConditionObject(constitutions[relation], error_msg)
                if not relatedObj:
                    return None

                related_ks = Knowledge.getAllLikeByStartMiddleEndInDB(attributeName="s_chain", end=relatedObj,
                                                                      middles=[relation])

                if not related_ks:  # 没有满足条件的，清空结果，直接跳出
                    cur_reals = []
                    break
                next_reals = []
                for related_klg in first_related_ks:
                    related_klg.getChainItems()
                    next_reals.append(related_klg._head)

                # 求交集
                cur_reals = list((set(cur_reals).union(set(next_reals))) ^ (set(cur_reals) ^ set(next_reals)))
            if cur_reals:
                reals.extend(cur_reals)
        return reals

    @staticmethod
    def __getConditionObject(obj, error_msg, memory=None):
        """
        取得条件查询中对应的的元数据、实际对象
        :return:
        """
        from loongtian.nvwa.models.knowledge import Knowledge
        if isinstance(obj, RealObject) or isinstance(obj, Knowledge):
            return obj
        if isinstance(obj, str):
            # 取得字符串对应的的元数据、实际对象
            meta, obj = RealObject.createMetaRealByValue(mvalue=obj, memory=memory)
            return obj

        raise Exception(error_msg)

    def getRelatedKnowledges(self, relation, relatedObj):
        """
        取得当前实际对象-关系-关联对象的knowledge
        :param relation:关系
        :param relatedObj:关联对象
        :return:
        """
        # 检查参数，如果不是女娲系统对象，转换之
        if not isinstance(relation, BaseEntity):
            relationmeta, relation = RealObject.createMetaRealByValue(str(relation),
                                                                      recordInDB=True,
                                                                      memory=self.real.MemoryCentral)
        if not isinstance(relatedObj, BaseEntity):
            relatedmeta, relatedObj = RealObject.createMetaRealByValue(str(relatedObj),
                                                                       recordInDB=True,
                                                                       memory=self.real.MemoryCentral)

        from loongtian.nvwa.models.knowledge import Knowledge
        return Knowledge.getByObjectChain([self.real, relation, relatedObj],
                                          memory=self.real.MemoryCentral)

    def getRelations(self, relatedObj):
        """
        取得与关联对象的关系。例如：苹果-红，可能取得的关系包括：苹果-颜色-红，苹果-属性-红，苹果-属性-颜色-红，苹果-是-红-的，其中：...-是-...-的，也是一种关系。
        :param relatedObj:
        :return:
        """
        # 检查参数，如果不是女娲系统对象，转换之
        if not isinstance(relatedObj, BaseEntity):
            relatedmeta, relatedObj = RealObject.createMetaRealByValue(str(relatedObj),
                                                                       recordInDB=True,
                                                                       memory=self.real.MemoryCentral)

        # 取得以当前实际对象开头，以relatedObj结尾的所有Knowledge
        from loongtian.nvwa.models.knowledge import Knowledge
        related_ks = Knowledge.getAllLikeByStartMiddleEndInDB(attributeName="s_chain",
                                                              start=self,
                                                              end=relatedObj,
                                                              memory=self.real.MemoryCentral)
        return related_ks

    def getAllRelatedKnowledges(self, relation):
        """
        取得当前实际对象关联的知识（可能有多个，例如：牛-父对象-动物、牛-父对象-反刍动物）。
        :return:
        """
        if relation in self._constitute_knowledges:
            return self._constitute_knowledges.get(relation)

        from loongtian.nvwa.models.knowledge import Knowledge

        # 取得以当前对象开头，以instinct(例如，父对象）为结尾的一条Knowledge
        cur_k = Knowledge.getByStartAndEnd(self.real,
                                           relation,
                                           memory=self.real.MemoryCentral)
        if not cur_k:
            self._constitute_knowledges[relation] = None
            return None

        related_ks = cur_k.getAllForwardsInMemory()  # 首先从内存查
        if not related_ks:  # 内存中查不到，从数据库查
            related_ks = cur_k.getAllForwardsInDB(lazy_get=False)
        self._constitute_knowledges[relation] = related_ks
        return related_ks

    def getRelatedObjects(self, relation):
        """
        取得当前实际对象关联的对象（例如有、父对象、属性等）。
        :return:related_objs, related_ks
        """
        # 检查参数，如果不是女娲系统对象，转换之
        if not isinstance(relation, BaseEntity):
            relationmeta, relation = RealObject.createMetaRealByValue(str(relation),
                                                                      recordInDB=True,
                                                                      memory=self.real.MemoryCentral)

        if relation in self._constitute_reals:
            return self._constitute_reals.get(relation), self._constitute_knowledges.get(relation)

        # 取得当前实际对象关联的知识（例如：牛 - 父对象 - 动物,牛 - 父对象 - 哺乳动物）。
        related_ks = self.getAllRelatedKnowledges(relation)
        if related_ks:
            related_objs = []
            # 分别提取关联的对象
            for kid, klg in related_ks.items():
                klg.getChainItems()
                componets = klg.getSequenceComponents()
                last_item = componets[-1]
                if not isinstance(last_item, BaseEntity):  # 抛弃那些不是女娲对象的item，例如：list等
                    continue
                from loongtian.nvwa.runtime.instinct import Instincts
                if relation.id == Instincts.instinct_parent.id and \
                        isinstance(last_item, RealObject) and \
                        last_item.isPlaceHolder():  # 实际对象父对象不能是placeholder，这种情况发生在创建意义时，例如：牛是动物意义牛父对象动物
                    return None, None
                related_objs.append(last_item)
            self._constitute_reals[relation] = related_objs
            self._constitute_knowledges[relation] = related_ks
            return related_objs, related_ks

        else:
            self._constitute_reals[relation] = None
            self._constitute_knowledges[relation] = None
            return None, None

    def getSelfParentObjects(self):
        """
        取得当前实际对象的父对象（可能有多个。例如：牛的父对象，可能是动物，也可能是家畜、牲口）。
        :return:父对象,父对象知识链
        """
        from loongtian.nvwa.runtime.instinct import Instincts
        return self.getRelatedObjects(Instincts.instinct_parent)

    def getSelfChildren(self):
        """
        取得当前实际对象的所有子对象
        :return:
        """
        # todo 未完成

    def getSelfIngredientObjects(self):
        """
        取得当前实际对象的成分对象（可能有多个。例如：牛肉的成分，包括蛋白质、碳水化合物等）。
        :return:成分对象,成分对象知识链
        """
        from loongtian.nvwa.runtime.instinct import Instincts
        return self.getRelatedObjects(Instincts.instinct_ingredient)

    def getSelfComponentObjects(self):
        """
        取得当前实际对象的组件对象（可能有多个。例如：牛的组件，包括腿、头、尾等）。
        :return:组件对象,组件对象知识链
        """
        from loongtian.nvwa.runtime.instinct import Instincts
        return self.getRelatedObjects(Instincts.instinct_component)

    def getSelfAttributeObjects(self):
        """
        取得当前实际对象的属性对象（可能有多个。例如：牛的属性，可能是品种、畜龄、牝牡、肥瘦等）。
        :return:
        """
        from loongtian.nvwa.runtime.instinct import Instincts
        return self.getRelatedObjects(Instincts.instinct_attribute)

    def getSelfActionObjects(self):
        """
        取得当前实际对象的动作对象（可能有多个。例如：牛的属性，可能是品种、畜龄、牝牡、肥瘦等）。
        :return:
        """
        from loongtian.nvwa.runtime.instinct import Instincts
        return self.getRelatedObjects(Instincts.instinct_action)

    def getSelfBelongsObjects(self):
        """
        取得当前实际对象的所属物对象（可能有多个。例如：牛的所属物对象，可能是铃铛，也可能是鞍子）。
        :return:
        """
        from loongtian.nvwa.runtime.instinct import Instincts
        return self.getRelatedObjects(Instincts.instinct_belongs)

    def getSelfRelevancyObjects(self):
        """
        取得当前实际对象的相关物对象（可能有多个。例如：牛的相关物对象，可能是牧童，也可能是青草。相关物对象是等待进一步建立关系的对象，这种关系是人类社会对对象的各种定义）。
        :return:
        """
        from loongtian.nvwa.runtime.instinct import Instincts
        return self.getRelatedObjects(Instincts.instinct_relevancy)

    def getSelfAllTopRelationObjects(self, getParent=True):
        """
        取得当前实际对象的所有构成对象（可能有多个）。
        :param:getParent:是否取父对象
        :return:
        """
        # 如果已经取得过了，直接返回结果
        if self._all_constitute_objs:
            return self._all_constitute_objs

        from loongtian.nvwa.runtime.instinct import Instincts
        constituentKnowledges = {}
        for toprelation in Instincts.TopRelations:
            if not getParent and toprelation.id == Instincts.instinct_parent.id:
                continue
            related_objs, related_ks = self.getRelatedObjects(toprelation)
            self._all_constitute_objs[toprelation] = related_objs
            constituentKnowledges[toprelation] = related_ks

        return self._all_constitute_objs

    def getInheritRelation(self, forceToReload=False):
        """
        取得当前实际对象所有父对象的继承关系
        :param forceToReload: 是否强制重新加载
        :return:
        """
        from loongtian.nvwa.runtime.instinct import Instincts

        # 如果已经取得当前实际对象所有父对象的继承关系，直接返回
        if self._got_inherit_relation and not forceToReload:
            return self._inherit_relation, self._all_parents_relation

        parents, parent_ks = self.getSelfParentObjects()
        if parents:
            for parent in parents:
                if parent.isOriginals():
                    self._inherit_relation[parent] = None
                    self._all_parents_relation.update(self._inherit_relation)
                else:
                    parent_inherit_relation, parent_parents_relation = parent.Constitutions.getInheritRelation()
                    if len(parent_inherit_relation) > 0:
                        self._inherit_relation[parent] = parent_inherit_relation  # 这是与对象最紧密的继承关系
                        self._all_parents_relation.update(parent_inherit_relation)  # 这是所有父对象的列表
                        # self._all_parents_relation.update(self._inherit_relation)
        else:
            self._inherit_relation[Instincts.instinct_original_object] = None  # 所有对象都有一个最终的父对象：元对象
            self._all_parents_relation.update(self._inherit_relation)

        # 标记已经取得了
        self._got_inherit_relation = True

        return self._inherit_relation, self._all_parents_relation

    def isChild(self, parent):
        """
        判断一个对象是否继承自，例如：已知牛——>哺乳动物，哺乳动物——>动物，现判断是否牛——>动物
        :param parent:
        :return:
        """
        if parent is None or not isinstance(parent, RealObject):
            raise Exception("父对象必须存在，并为实际对象！")

        # 判断parent是否是元对象，如果是，直接返回True（因为所有实际对象均继承自元对象）
        from loongtian.nvwa.runtime.instinct import Instincts
        if parent is Instincts.instinct_original_object or parent.id == Instincts.instinct_original_object.id:
            return True

        # 取得所有父对象的继承关系
        inherit_relation, all_parents_relation = self.getInheritRelation()
        if parent in inherit_relation:
            return True
        return parent in all_parents_relation

    def getParentsIngredientObjects(self):
        """
        取得所有父对象的成分对象
        :return:
        """
        parent_ingredient_dict = {}
        # 取得所有父对象的继承关系
        inherit_relation, all_parents_relation = self.getInheritRelation()
        for parent in all_parents_relation.keys():
            ingredients = parent.Constitutions.getSelfIngredientObjects()
            parent_ingredient_dict[parent] = ingredients

        return parent_ingredient_dict

    def getParentsAttributeObjects(self):
        """
        取得所有父对象的属性对象
        :return:
        """
        parent_attribute_dict = {}
        # 取得所有父对象的继承关系
        inherit_relation, all_parents_relation = self.getInheritRelation()
        for parent in all_parents_relation.keys():
            attributes = parent.Constitutions.getSelfAttributeObjects()
            parent_attribute_dict[parent] = attributes

        return parent_attribute_dict

    def getParentsActionObjects(self):
        """
        取得所有父对象的动作对象
        :return:
        """
        parent_action_dict = {}
        # 取得所有父对象的继承关系
        inherit_relation, all_parents_relation = self.getInheritRelation()
        for parent in all_parents_relation.keys():
            attributes = parent.Constitutions.getSelfActionObjects()
            parent_action_dict[parent] = attributes

        return parent_action_dict

    def getParentsComponentObjects(self):
        """
        取得所有父对象的组件对象
        :return:
        """
        parent_component_dict = {}
        # 取得所有父对象的继承关系
        inherit_relation, all_parents_relation = self.getInheritRelation()
        for parent in all_parents_relation.keys():
            components = parent.Constitutions.getSelfComponentObjects()
            parent_component_dict[parent] = components

        return parent_component_dict

    def getParentsBelongsObjects(self):
        """
        取得所有父对象的所属物对象
        :return:
        """
        parent_belongs_dict = {}
        # 取得所有父对象的继承关系
        inherit_relation, all_parents_relation = self.getInheritRelation()
        for parent in all_parents_relation.keys():
            belongss = parent.Constitutions.getSelfBelongsObjects()
            parent_belongs_dict[parent] = belongss

        return parent_belongs_dict

    def getParentsRelevancyObjects(self):
        """
        取得所有父对象的相关物对象
        :return:
        """
        parent_relevancy_dict = {}
        # 取得所有父对象的继承关系
        inherit_relation, all_parents_relation = self.getInheritRelation()
        for parent in all_parents_relation.keys():
            relevancys = parent.Constitutions.getSelfRelevancyObjects()
            parent_relevancy_dict[parent] = relevancys

        return parent_relevancy_dict

    def getAllIngredientObjects(self):
        """
        取得所有当前实际对象及父对象的成分对象（解决冲突）
        :return:
        """
        self_ingredients, self_ingredients_ks = self.getSelfIngredientObjects()
        parent_ingredients, parent_ingredients_ks = self.getParentsIngredientObjects()
        all_ingredients = list(self_ingredients)
        all_ingredients.extend(parent_ingredients)
        all_ingredients = set(self_ingredients)
        return all_ingredients

    def getAllAttributeObjects(self):
        """
        取得所有当前实际对象及父对象的属性对象（解决冲突）
        :return:
        """
        # 如果已经取得过了，直接返回结果
        from loongtian.nvwa.runtime.instinct import Instincts
        if Instincts.instinct_attribute in self._all_constitute_objs:
            return self._all_constitute_objs[Instincts.instinct_attribute]

        self_attributes, self_attributes_ks = self.getSelfAttributeObjects()
        parent_attributes, parent_attributes_ks = self.getParentsAttributeObjects()
        all_attributes = list(self_attributes)
        all_attributes.extend(parent_attributes)
        all_attributes = set(self_attributes)

        # 添加到内存
        self._all_constitute_objs[Instincts.instinct_attribute] = all_attributes
        return all_attributes

    def getAllActionObjects(self):
        """
        取得所有当前实际对象及父对象的动作对象（解决冲突）
        :return:
        """
        # 如果已经取得过了，直接返回结果
        from loongtian.nvwa.runtime.instinct import Instincts
        if Instincts.instinct_action in self._all_constitute_objs:
            return self._all_constitute_objs[Instincts.instinct_action]

        self_actions, self_actions_ks = self.getSelfActionObjects()
        parent_actions, parent_actions_ks = self.getParentsActionObjects()
        import copy
        all_actions = copy.copy(self_actions)
        all_actions.extend(self_actions)
        all_actions = set(self_actions)

        # 添加到内存
        self._all_constitute_objs[Instincts.instinct_action] = self_actions
        return self_actions

    def getAllComponentObjects(self):
        """
        取得所有当前实际对象及父对象的组件对象（解决冲突）
        :return:
        """
        # 如果已经取得过了，直接返回结果
        from loongtian.nvwa.runtime.instinct import Instincts
        if Instincts.instinct_component in self._all_constitute_objs:
            return self._all_constitute_objs[Instincts.instinct_component]

        self_components, self_components_ks = self.getSelfComponentObjects()
        parent_components, parent_components_ks = self.getParentsComponentObjects()
        all_components = list(self_components)
        all_components.extend(parent_components)
        all_components = set(self_components)

        # 添加到内存
        self._all_constitute_objs[Instincts.instinct_component] = all_components
        return all_components

    def getAllBelongsObjects(self):
        """
        取得所有当前实际对象及父对象的成分对象（解决冲突）
        :return:
        """
        # 如果已经取得过了，直接返回结果
        from loongtian.nvwa.runtime.instinct import Instincts
        if Instincts.instinct_belongs in self._all_constitute_objs:
            return self._all_constitute_objs[Instincts.instinct_belongs]

        self_belongss, self_belongss_ks = self.getSelfBelongsObjects()
        parent_belongss, parent_belongss_ks = self.getParentsBelongsObjects()
        all_belongses = list(self_belongss)
        all_belongses.extend(parent_belongss)
        all_belongses = set(self_belongss)

        # 添加到内存
        self._all_constitute_objs[Instincts.instinct_belongs] = all_belongses
        return all_belongses

    def getAllRelevancyObjects(self):
        """
        取得所有当前实际对象及父对象的相关物对象（解决冲突）
        :return:
        """
        self_relevancys, self_relevancys_ks = self.getSelfRelevancyObjects()
        parent_relevancys, parent_relevancys_ks = self.getParentsRelevancyObjects()
        all_relevancys = list(self_relevancys)
        all_relevancys.extend(parent_relevancys)
        all_relevancys = set(self_relevancys)
        return all_relevancys

    def addRelatedObject(self, relation, relatedObj,
                         weight=Character.Inner_Thinking_Link_Weight,
                         recordInDB=False
                         ):
        """
        添加与其他对象的关系。例如：为‘牛’添加‘组件’-‘腿’。
        :param relation:
        :param relatedObj:实际对象或实际对象的集合列表
        :return:
        """
        # 检查参数，如果不是女娲系统对象，转换之
        if not isinstance(relation, BaseEntity):
            relationmeta, relation = RealObject.createMetaRealByValue(str(relation),
                                                                      recordInDB=recordInDB,
                                                                      memory=self.real.MemoryCentral)
        if not isinstance(relatedObj, BaseEntity):
            relatedmeta, relatedObj = RealObject.createMetaRealByValue(str(relatedObj),
                                                                       recordInDB=recordInDB,
                                                                       memory=self.real.MemoryCentral)

        if RealObject.hasAnything([self.real, relation, relatedObj]):  # 构成关系中不能有anything
            return None
        from loongtian.nvwa.runtime.instinct import Instincts
        if relation.id == Instincts.instinct_parent.id and relatedObj.isPlaceHolder():  # 父对象不能是placeholder，这种情况发生在创建意义时，例如：牛是动物意义牛父对象动物
            return None
        # 首先查看内存、数据库是否存在
        cur_k = self.getRelatedKnowledges(relation, relatedObj)
        if cur_k:
            # 将在[self, relation, relatedObj]关系记录在realobject内部
            self.recordRelatedObject(relation, relatedObj, cur_k)
            return cur_k
        # 如果不存在，直接创建
        from loongtian.nvwa.models.knowledge import Knowledge
        cur_k = Knowledge.createKnowledgeByObjChain([self.real, relation, relatedObj],
                                                    understood_ratio=weight,
                                                    recordInDB=recordInDB,
                                                    memory=self.real.MemoryCentral)
        if cur_k:
            # 将在[self, relation, relatedObj]关系记录在realobject内部
            self.recordRelatedObject(relation, relatedObj, cur_k)

        return cur_k

    def recordRelatedObject(self, relation, relatedObj, knowledge):
        """
        将在[self, relation, relatedObj]关系记录在realobject内部
        :param relation:
        :param relatedObj:
        :param knowledge: [self, relation, relatedObj] 形成的知识链
        :return:
        """
        if not relatedObj:
            raise Exception("关系的值不应该为None！")
        # 检查参数，如果不是女娲系统对象，转换之
        if not isinstance(relation, BaseEntity):
            relationmeta, relation = RealObject.createMetaRealByValue(str(relation),
                                                                      recordInDB=True,
                                                                      memory=self.real.MemoryCentral)
        if not isinstance(relatedObj, BaseEntity):
            relatedmeta, relatedObj = RealObject.createMetaRealByValue(str(relatedObj),
                                                                       recordInDB=True,
                                                                       memory=self.real.MemoryCentral)

        if not relation in self._constitute_reals:
            self._constitute_reals[relation] = [relatedObj]
        else:
            relatedObjs = self._constitute_reals.get(relation)
            if relatedObjs:
                if not isinstance(relatedObjs, list):
                    raise Exception("_constitute_reals的key应该是构成关系，值应该是list!")
                relatedObjs.append(relatedObj)
            else:
                self._constitute_reals[relation] = [relatedObj]

        if not relation in self._constitute_knowledges:
            self._constitute_knowledges[relation] = {knowledge.id: knowledge}
        else:
            related_klgs = self._constitute_knowledges.get(relation)
            if related_klgs:
                if not isinstance(related_klgs, dict):
                    raise Exception("_constitute_knowledges的key应该是构成关系，值应该是dict!")
                related_klgs[knowledge.id] = knowledge
            else:
                self._constitute_knowledges[relation] = {knowledge.id: knowledge}

    def addParent(self, obj, recordInDB=False, weight=Character.Inner_Thinking_Link_Weight):
        """
        添加当前实际对象的父对象。
        :return:父对象,父对象知识链
        """
        if not isinstance(obj, RealObject):
            raise Exception("当前实际对象的父对象应为实际对象！")

        if obj.isPlaceHolder():  # 父对象不能是placeholder，这种情况发生在创建意义时，例如：牛是动物意义牛父对象动物
            return None
        from loongtian.nvwa.runtime.instinct import Instincts
        return self.addRelatedObject(Instincts.instinct_parent, obj, recordInDB=recordInDB, weight=weight)

    def addIngredient(self, obj, recordInDB=False, weight=Character.Inner_Thinking_Link_Weight):
        """
        添加当前实际对象的成分对象。
        :return:成分对象,成分对象知识链
        """
        if not isinstance(obj, RealObject):
            raise Exception("当前实际对象的成分对象应为实际对象！")

        from loongtian.nvwa.runtime.instinct import Instincts
        return self.addRelatedObject(Instincts.instinct_ingredient, obj, recordInDB=recordInDB, weight=weight)

    def addComponent(self, obj, recordInDB=False, weight=Character.Inner_Thinking_Link_Weight):
        """
        添加当前实际对象的组件对象（不添加顺序）。
        :return:组件对象知识链
        """
        if not isinstance(obj, RealObject):
            raise Exception("当前实际对象的组件对象应为实际对象！")

        from loongtian.nvwa.runtime.instinct import Instincts
        return self.addRelatedObject(Instincts.instinct_component, obj, recordInDB=recordInDB, weight=weight)

    def addSequnceComponents(self, components, recordInDB=False, weight=Character.Inner_Thinking_Link_Weight):
        """
        添加有顺序的系列组件
        :param components:
        :param recordInDB:
        :param weight:
        :return:
        """
        _components_klgs = []

        for component in components:
            _component_klg = self.real.Constitutions.addComponent(component, recordInDB=recordInDB, weight=weight)
            _components_klgs.append(_component_klg)

        # 添加上下条记录的关系
        from loongtian.nvwa.models.knowledge import Knowledge
        _components_klgs_sequence_klg = Knowledge.createKnowledgeByObjChain(
            _components_klgs,
            understood_ratio=weight,
            recordInDB=recordInDB,
            memory=self.real.MemoryCentral)

        return _components_klgs, _components_klgs_sequence_klg

    def addAttribute(self, obj, recordInDB=False, weight=Character.Inner_Thinking_Link_Weight):
        """
        添加当前实际对象的属性对象。
        :return:
        """
        if not isinstance(obj, RealObject):
            raise Exception("当前实际对象的属性对象应为实际对象！")

        from loongtian.nvwa.runtime.instinct import Instincts
        return self.addRelatedObject(Instincts.instinct_attribute, obj, recordInDB=recordInDB, weight=weight)

    def addAction(self, obj, recordInDB=False, weight=Character.Inner_Thinking_Link_Weight):
        """
        添加当前实际对象的动作对象（鸟-能-飞）。
        :return:
        """
        if not isinstance(obj, RealObject):
            raise Exception("当前实际对象的动作对象应为实际对象！")

        from loongtian.nvwa.runtime.instinct import Instincts
        return self.addRelatedObject(Instincts.instinct_action, obj, recordInDB=recordInDB, weight=weight)

    def addBelongs(self, obj, recordInDB=False, weight=Character.Inner_Thinking_Link_Weight):
        """
        添加当前实际对象的所属物对象。
        :return:
        """
        if not isinstance(obj, RealObject):
            raise Exception("当前实际对象的所属对象应为实际对象！")

        from loongtian.nvwa.runtime.instinct import Instincts
        return self.addRelatedObject(Instincts.instinct_belongs, obj, recordInDB=recordInDB, weight=weight)

    def addRelevancy(self, obj, recordInDB=False, weight=Character.Inner_Thinking_Link_Weight):
        """
        添加当前实际对象的相关物对象。
        :return:
        """
        if not isinstance(obj, RealObject):
            raise Exception("当前实际对象的相关物对象应为实际对象！")

        from loongtian.nvwa.runtime.instinct import Instincts
        return self.addRelatedObject(Instincts.instinct_relevancy, obj, recordInDB=recordInDB, weight=weight)

    def deleteRelatedObject(self, relation, relatedObj):
        """
        逻辑删除与其他对象的直觉关系。例如：为‘牛’添加‘组件’-‘腿’。
        :param relation:
        :param relatedObj:实际对象或实际对象的集合列表
        :return:
        """
        # 检查参数，如果不是女娲系统对象，转换之
        if not isinstance(relation, BaseEntity):
            relationmeta, relation = RealObject.createMetaRealByValue(str(relation),
                                                                      recordInDB=True,
                                                                      memory=self.real.MemoryCentral)
        if not isinstance(relatedObj, BaseEntity):
            relatedmeta, relatedObj = RealObject.createMetaRealByValue(str(relatedObj),
                                                                       recordInDB=True,
                                                                       memory=self.real.MemoryCentral)

        cur_k = self.getRelatedKnowledges(relation, relatedObj)
        if cur_k:
            return cur_k.delete()

    def deleteParent(self, obj):
        """
        逻辑删除当前实际对象的父对象。
        :return:父对象,父对象知识链
        """
        if not isinstance(obj, RealObject):
            raise Exception("要逻辑删除的当前实际对象的父对象应为实际对象！")

        from loongtian.nvwa.runtime.instinct import Instincts
        return self.deleteRelatedObject(Instincts.instinct_parent, obj)

    def deleteIngredient(self, obj):
        """
        逻辑删除当前实际对象的成分对象。
        :return:成分对象,成分对象知识链
        """
        if not isinstance(obj, RealObject):
            raise Exception("要逻辑删除的当前实际对象的成分对象应为实际对象！")

        from loongtian.nvwa.runtime.instinct import Instincts
        return self.deleteRelatedObject(Instincts.instinct_ingredient, obj)

    def deleteComponent(self, obj):
        """
        逻辑删除当前实际对象的组件对象。
        :return:组件对象,组件对象知识链
        """
        if not isinstance(obj, RealObject):
            raise Exception("要逻辑删除的当前实际对象的组件对象应为实际对象！")

        from loongtian.nvwa.runtime.instinct import Instincts
        return self.deleteRelatedObject(Instincts.instinct_component, obj)

    def deleteAttribute(self, obj):
        """
        逻辑删除当前实际对象的属性对象。
        :return:
        """
        if not isinstance(obj, RealObject):
            raise Exception("要逻辑删除的当前实际对象的属性对象应为实际对象！")

        from loongtian.nvwa.runtime.instinct import Instincts
        return self.deleteRelatedObject(Instincts.instinct_attribute, obj)

    def deleteAction(self, obj):
        """
        逻辑删除当前实际对象的属性对象。
        :return:
        """
        if not isinstance(obj, RealObject):
            raise Exception("要逻辑删除的当前实际对象的动作对象应为实际对象！")

        from loongtian.nvwa.runtime.instinct import Instincts
        return self.deleteRelatedObject(Instincts.instinct_action, obj)

    def deleteBelongs(self, obj):
        """
        逻辑删除当前实际对象的所属物对象。
        :return:
        """
        if not isinstance(obj, RealObject):
            raise Exception("要逻辑删除的当前实际对象的所属对象应为实际对象！")

        from loongtian.nvwa.runtime.instinct import Instincts
        return self.deleteRelatedObject(Instincts.instinct_belongs, obj)

    def deleteRelevancy(self, obj):
        """
        逻辑删除当前实际对象的相关物对象。
        :return:
        """
        if not isinstance(obj, RealObject):
            raise Exception("要逻辑删除的当前实际对象的相关物对象应为实际对象！")

        from loongtian.nvwa.runtime.instinct import Instincts
        return self.deleteRelatedObject(Instincts.instinct_relevancy, obj)

    def _physicalDeleteRelatedObject(self, relation, relatedObj):
        """
        物理删除与其他对象的关系。例如：为‘牛’添加‘组件’-‘腿’。
        :param relation:
        :param relatedObj:实际对象或实际对象的集合列表
        :return:
        """
        cur_k = self.getRelatedKnowledges(relation, relatedObj)
        if cur_k:
            return cur_k._physicalDelete()

    def _physicalDeleteParent(self, obj):
        """
        物理删除当前实际对象的父对象。
        :return:父对象,父对象知识链
        """
        if not isinstance(obj, RealObject):
            raise Exception("要物理删除的当前实际对象的父对象应为实际对象！")

        from loongtian.nvwa.runtime.instinct import Instincts
        return self._physicalDeleteRelatedObject(Instincts.instinct_parent, obj)

    def _physicalDeleteIngredient(self, obj):
        """
        物理删除当前实际对象的成分对象。
        :return:成分对象,成分对象知识链
        """
        if not isinstance(obj, RealObject):
            raise Exception("要物理删除的当前实际对象的成分对象应为实际对象！")

        from loongtian.nvwa.runtime.instinct import Instincts
        return self._physicalDeleteRelatedObject(Instincts.instinct_ingredient, obj)

    def _physicalDeleteComponent(self, obj):
        """
        物理删除当前实际对象的组件对象。
        :return:组件对象,组件对象知识链
        """
        if not isinstance(obj, RealObject):
            raise Exception("要物理删除的当前实际对象的组件对象应为实际对象！")

        from loongtian.nvwa.runtime.instinct import Instincts
        return self._physicalDeleteRelatedObject(Instincts.instinct_component, obj)

    def _physicalDeleteAttribute(self, obj):
        """
        物理删除当前实际对象的属性对象。
        :return:
        """
        if not isinstance(obj, RealObject):
            raise Exception("要物理删除的当前实际对象的属性对象应为实际对象！")

        from loongtian.nvwa.runtime.instinct import Instincts
        return self._physicalDeleteRelatedObject(Instincts.instinct_attribute, obj)

    def _physicalDeleteAction(self, obj):
        """
        物理删除当前实际对象的属性对象。
        :return:
        """
        if not isinstance(obj, RealObject):
            raise Exception("要物理删除的当前实际对象的动作对象应为实际对象！")

        from loongtian.nvwa.runtime.instinct import Instincts
        return self._physicalDeleteRelatedObject(Instincts.instinct_action, obj)

    def _physicalDeleteBelongs(self, obj):
        """
        物理删除当前实际对象的所属物对象。
        :return:
        """
        if not isinstance(obj, RealObject):
            raise Exception("要物理删除的当前实际对象的所属对象应为实际对象！")

        from loongtian.nvwa.runtime.instinct import Instincts
        return self._physicalDeleteRelatedObject(Instincts.instinct_belongs, obj)

    def _physicalDeleteRelevancy(self, obj):
        """
        物理删除当前实际对象的相关物对象。
        :return:
        """
        if not isinstance(obj, RealObject):
            raise Exception("要物理删除的当前实际对象的相关物对象应为实际对象！")

        from loongtian.nvwa.runtime.instinct import Instincts
        return self._physicalDeleteRelatedObject(Instincts.instinct_relevancy, obj)

    def getSequenceComponents(self):
        """
        取得排序的组件（可能取不到，因为可能未排序）
        :return:
        """
        # 如果已经取得了，直接返回
        if self._sequence_components:
            return self._sequence_components

        related_objs, related_ks = self.getSelfComponentObjects()

        if related_ks is None or len(related_ks) == 0:
            # 没有找到任何组件
            self._sequence_components = None
            return None

        from loongtian.nvwa.models.knowledge import Knowledge
        # 根据散列化的实际对象或知识链取得Knowledge（顺序不一定相同）
        self._sequence_components_sequence_klg = Knowledge.getByObjs(related_ks,
                                                                     memory=self.real.MemoryCentral)
        if not self._sequence_components_sequence_klg:
            # 没有找到，应该是一个没有顺序的集合，直接返回None
            self._sequence_components = None
            return None

        # 拆解"牛-组件-腿"、"牛-组件-尾巴"这样的知识链组成的知识链，得到[腿,尾巴...]
        self._sequence_components_klgs = self._sequence_components_sequence_klg.getSequenceComponents()  # 仍然是知识链
        self._sequence_components = []
        for sequence_component_klg in self._sequence_components_klgs:
            sequence_component_klg.getChainItems()
            self._sequence_components.append(sequence_component_klg._end_item)

        return self._sequence_components

class ExecutionInfo():
    """
    对象可执行信息的包装类
    """

    def __init__(self,real):

        self.real=real

        # 当前realobject的可执行的信息(executionInfo)，包括：模式（左右、左右定义）及意义（对左右对象的构成进行更改）
        # 模式、意义可能有多个（代表不同的执行步骤），与realobject的关系是1:n,n:n
        # 其中pattern和meaning均为特殊格式的knowledge
        self.LinearExecutionInfo = LinearExecutionInfo(
            self.real)  # 线性执行信息，例如：牛-有-腿格式为：{pattern_knowledge:[meaning_knowledges]}

        self.ConjugatedExecutionInfo = ConjugatedExecutionInfo(
            self.real)  # 共轭执行信息，例如：因为...所以...格式为：{pattern_knowledge:[meaning_knowledges]}

        # self._got_executionInfo = False  # 是否已经取得了executionInfos的标记。



    def getSelfLinearExecutionInfo(self):
        """
        取得当前realobject的线性可执行的信息，如：牛-有-腿。包括：模式（左右、左右定义）及意义（对左右对象的构成进行更改）[多模式，多意义]
        :return:self.LinearExecutionInfo
        """
        # 如果已经取得了，直接返回
        if self.LinearExecutionInfo and self.LinearExecutionInfo.isExecutable():
            return self.LinearExecutionInfo

        # 取得模式
        cur_patterns = self.real.Layers.getLowerEntitiesByType(ObjType.LINEAR_EXE_INFO)

        if not cur_patterns: # 没有模式，不是线性结构可执行性对象
            return self.LinearExecutionInfo

        if isinstance(cur_patterns, RelatedObj):  # 可能有多个
            cur_patterns = {cur_patterns.id:cur_patterns}
        if not self.LinearExecutionInfo:
            self.LinearExecutionInfo = LinearExecutionInfo(self)
        self.LinearExecutionInfo.pattern_knowledges = cur_patterns

        from loongtian.nvwa.models.knowledge import Knowledge
        for id, cur_pattern in cur_patterns.items():
            if isinstance(cur_patterns, RelatedObj):
                cur_pattern = cur_pattern.obj
            if not isinstance(cur_pattern,Knowledge):
                raise Exception("当前实际对象的模式不是知识链！")
            cur_pattern.getChainItems()

            # 取得意义
            # 在深度语义网中，意义可能会有不同程度的递进，这里只递进到第一层，以待后续处理
            cur_meanings = cur_pattern.Layers.getLowerEntitiesByType(ObjType.LINEAR_EXE_INFO)
            if not cur_meanings:
                raise Exception("当前实际对象“%s”有pattern，但没有意义！" % self.real.remark)
            self.LinearExecutionInfo.meaning_knowledges[cur_pattern.id] = cur_meanings

            # 取得值
            from loongtian.nvwa.runtime.instinct import Instincts
            if Instincts.hasConstituentValue(self):  # 目前只能有顶级关系才能有值（内部值）的概念
                from loongtian.nvwa.models.knowledge import Knowledge
                for id, cur_meaning in cur_meanings.items():
                    cur_meaning = cur_meaning.obj
                    if not isinstance(cur_meaning, Knowledge):
                        raise Exception("当前实际对象的意义不是Knowledge类型！")
                    meaning_value = cur_meaning.Layers.getLowerEntitiesByType(ObjType.LINEAR_EXE_MEANING_VALUE)
                    if meaning_value:
                        meaning_value = self.LinearExecutionInfo.get_meaning_value(meaning_value)
                        if meaning_value:
                            self.LinearExecutionInfo.meaning_value_dict[cur_meaning.id] = meaning_value
        # 除了顶级关系、意义之外，明确实际对象的子类型为：动作
        if len(self.LinearExecutionInfo.meaning_knowledges) > 0 \
                and not self.real.isTopRelation() and not self.real.isInstinctMeaning():
            self.real.setType(type=ObjType.ACTION)

        # else:
        #     self.LinearExecutionInfo = None
        #     # # 明确实际对象的子类型为：虚对象:2019-1-28 不能直接设置，类型不一定
        #     # self.setType(type=ObjType.VIRTUAL)

        return self.LinearExecutionInfo



    def getSelfConjugatedExecutionInfo(self):
        """
        取得当前realobject的共轭结构可执行的信息，例如：因为...所以...包括：模式（左右、左右定义）及意义（对左右对象的构成进行更改）[多模式，多意义]
        :return:self.ConjugatedExecutionInfo
        """
        # 如果已经取得了，直接返回
        if self.ConjugatedExecutionInfo and self.ConjugatedExecutionInfo.isExecutable():
            return self.ConjugatedExecutionInfo

        # 取得模式
        cur_patterns = self.real.Layers.getLowerEntitiesByType(ObjType.CONJUGATED_EXE_INFO)
        if not cur_patterns: # 没有模式，不是线性结构可执行性对象
            return self.ConjugatedExecutionInfo

        if isinstance(cur_patterns, RelatedObj):  # 可能有多个
            cur_patterns = {cur_patterns.id:cur_patterns}
        if not self.ConjugatedExecutionInfo:
            self.ConjugatedExecutionInfo = ConjugatedExecutionInfo(self)
        self.ConjugatedExecutionInfo.pattern_knowledges = cur_patterns

        from loongtian.nvwa.models.knowledge import Knowledge
        for id, cur_pattern in cur_patterns.items():
            if isinstance(cur_patterns, RelatedObj):
                cur_pattern = cur_pattern.obj
            if not isinstance(cur_pattern,Knowledge):
                raise Exception("当前实际对象的模式不是知识链！")
            cur_pattern.getChainItems()

            # 取得意义
            # 在深度语义网中，意义可能会有不同程度的递进，这里只递进到第一层，以待后续处理
            cur_meanings = cur_pattern.Layers.getLowerEntitiesByType(ObjType.CONJUGATED_EXE_INFO)
            if not cur_meanings:
                raise Exception("当前实际对象“%s”有pattern，但没有意义！" % self.real.remark)
            self.ConjugatedExecutionInfo.meaning_knowledges[cur_pattern.id] = cur_meanings

            # 取得值
            from loongtian.nvwa.runtime.instinct import Instincts
            if Instincts.hasConstituentValue(self):  # 目前只能有顶级关系才能有值（内部值）的概念
                from loongtian.nvwa.models.knowledge import Knowledge
                for id, cur_meaning in cur_meanings.items():
                    cur_meaning = cur_meaning.obj
                    if not isinstance(cur_meaning, Knowledge):
                        raise Exception("当前实际对象的意义不是Knowledge类型！")
                    meaning_value = cur_meaning.Layers.getLowerEntitiesByType(ObjType.CONJUGATED_EXE_MEANING_VALUE)
                    if meaning_value:
                        meaning_value = self.ConjugatedExecutionInfo.get_meaning_value(meaning_value)
                        if meaning_value:
                            self.ConjugatedExecutionInfo.meaning_value_dict[cur_meaning.id] = meaning_value
        # 除了顶级关系、意义之外，明确实际对象的子类型为：动作
        if len(self.ConjugatedExecutionInfo.meaning_knowledges) > 0 \
                and not self.real.isTopRelation() and not self.real.isInstinctMeaning():
            self.real.setType(type=ObjType.ACTION)

        # else:
        #     self.LinearExecutionInfo = None
        #     # # 明确实际对象的子类型为：虚对象:2019-1-28 不能直接设置，类型不一定
        #     # self.setType(type=ObjType.VIRTUAL)

        return self.ConjugatedExecutionInfo


class Connstrains():
    """
    实际对象的关系的前、后约束，相当于词向量的距离。例如：手机不能进水。牛-有-腿，腿的前约束，就是组件，便于系统查找和处理关系，避免出现马云-有-钱，将其处理成马云-组件-钱的情况。
    """

    def __init__(self, real):
        """
        实际对象的关系的前、后约束，相当于词向量的距离。例如：手机不能进水。牛-有-腿，腿的前约束，就是组件，便于系统查找和处理关系，避免出现马云-有-钱，将其处理成马云-组件-钱的情况。
        :param real:
        """
        self.real = real

    def getConnstrains(self):
        """
        定义实际对象的关系的前、后约束，例如：手机不能进水。牛-有-腿，腿的前约束，就是组件，便于系统查找和处理关系，避免出现马云-有-钱，将其处理成马云-组件-钱的情况。
        :return:
        """
        # todo 暂未实现
        raise NotImplemented

    def getPreConnstrains(self):
        """
        定义实际对象的关系的前约束，例如：牛-有-腿，腿的前约束，就是组件，便于系统查找和处理关系，避免出现马云-有-钱，将其处理成马云-组件-钱的情况。
        :return:
        """
        # todo 暂未实现
        raise NotImplemented

    def getPostConnstrains(self):
        """
        定义实际对象的关系的后约束，例如：牛-有-腿，腿的前约束，就是组件，便于系统查找和处理关系，避免出现马云-有-钱，将其处理成马云-组件-钱的情况。
        :return:
        """
        # todo 暂未实现
        raise NotImplemented

    def getTopRelationConnstrains(self):
        """
        定义实际对象的顶级关系的前约束，例如：牛-有-腿，腿的前约束，就是组件，便于系统查找和处理关系，避免出现马云-有-钱，将其处理成马云-组件-钱的情况。
        :return:
        """
        # todo 暂未实现
        raise NotImplemented
