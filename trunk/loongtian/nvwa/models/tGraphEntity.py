#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

import copy
from loongtian.util.log import logger
from loongtian.util.helper import jsonplus

from loongtian.nvwa import settings
from loongtian.nvwa.models.baseEntity import BaseEntity
from loongtian.nvwa.models.enum import ObjType
from loongtian.nvwa.runtime.collection import Collection

from loongtian.nvwa.runtime.relatedObjects import RelatedObj
from loongtian.nvwa.runtime.instinct import Instincts
from loongtian.nvwa.runtime.thinkResult.fragments import UnknownResult, UnknownObj

from loongtian.nvwa.organs.character import Character


class TGraphEntity(BaseEntity):
    """
    T字形结构图。线性输入的元数据/实际对象组成的链（元数据网/T字形结构实体类，T型单向链）。
    1、t_graph是一个T字型结构的由metaData/realObject、TGraphEntity的Id组成的数组(嵌套代表一条TGraphEntity)。格式为：[id,(id,[t_graph])]
    2、t_chain 是一个T字型结构的由metaData/realObject的Id组成的数组(嵌套代表一条TGraphEntity)。
    3、s_chain  是一个未经T字型结构处理的由metaData/realObject的Id组成序列数组
    4、m_chain 是一个由外域（可能是个T字形结构实体类，也可能是元数据/实际对象）、T字形结构实体类的id组成的序列数组。

    eg:
    1、t_graph = [情人节,(k8,[(k7,[(k6,[小明, 给]), 小丽]), (k5,[(k1,[一, 朵]), (k4,[(k3,[红色, 的]), (k2,[玫瑰, 花]]))])])]
    2、t_chain = [情人节,[[[小明, 给], 小丽], [[一, 朵], [[红色, 的], [玫瑰, 花]]]]
    3、s_chain = [情人节,小明, 给, 小丽,一, 朵,红色, 的, 玫瑰, 花]
    4、m_chain =[情人节,mn8,mn5,mn4,mn2]

    5、下面例子中所有的汉字，均代表其实际的元数据/实际对象id
    id      start       end       t_graph                                                                                                              t_chain                                                                 s_chain
    k1      一          朵        [(k1,[一, 朵])]                                                                                                     [一, 朵]                                                                 [一, 朵]
    k2      玫瑰        花        [(k2,[玫瑰, 花])]                                                                                                   [玫瑰, 花]                                                               [玫瑰, 花]
    k3      红色        的        [(k3,[红色, 的])]                                                                                                   [红色, 的]                                                               [红色, 的]
    k4      k3          k2        [(k3,[红色, 的]), (k2,[玫瑰, 花])]                                                                                  [[红色, 的], [玫瑰, 花]]                                                 [红色, 的, 玫瑰, 花]
    k5      k1          k4        [(k1,[一, 朵]), (k4,[(k3,[红色, 的]), (k2,[玫瑰, 花]]))]                                                            [[一, 朵],[[红色, 的], [玫瑰, 花]]]                                      [一, 朵, 红色, 的, 玫瑰, 花]
    k6      小明        给        [(k6,[小明, 给] )]                                                                                                  [小明, 给]                                                               [小明, 给]
    k7      k6          小丽      [(k6,[小明, 给]), 小丽]                                                                                             [[小明, 给], 小丽]                                                       [小明, 给, 小丽]
    k8      k7          k5        [(k7,[(k6,[小明, 给]), 小丽]), (k5,[(k1,[一, 朵]), (k4,[(k3,[红色, 的]), (k2,[玫瑰, 花]]))])]                       [[[小明, 给], 小丽], [[一, 朵], [[红色, 的], [玫瑰, 花]]]                [小明, 给, 小丽,一, 朵,红色, 的, 玫瑰, 花]
    k9      情人节      k8        [情人节,(k8,[(k7,[(k6,[小明, 给]), 小丽]), (k5,[(k1,[一, 朵]), (k4,[(k3,[红色, 的]), (k2,[玫瑰, 花]]))])])]         [情人节,[[[小明, 给], 小丽], [[一, 朵], [[红色, 的], [玫瑰, 花]]]]       [情人节,小明, 给, 小丽,一, 朵,红色, 的, 玫瑰, 花]
    ka      一          块        [(ka,[一, 块])]                                                                                                     [一, 块]                                                                 [一, 块]
    kb      ka          巧克力    [(ka,[一, 块]), 巧克力]                                                                                             [[一, 块], 巧克力]                                                       [一, 块, 巧克力]
    kc      k6          小绿      [(k6,[小明, 给]), 小绿]                                                                                             [[小明, 给], 小绿]                                                       [小明, 给, 小绿]
    kd      kc          kb        [(kc,[(k6,[小明, 给]), 小绿]), (kb,[(ka,[一, 块]), 巧克力])]                                                        [[[小明, 给], 小绿], [[一, 块], 巧克力]]                                 [小明, 给, 小绿，一, 块, 巧克力]
    ke      情人节      kd        [情人节,(kd,[(kc,[(k6,[小明, 给]), 小绿]), (kb,[(ka,[一, 块]), 巧克力])])]                                          [情人节,[[[小明, 给], 小绿], [[一, 块], 巧克力]]]                        [情人节,小明, 给, 小绿，一, 块, 巧克力]
    Note:
        丁字型结构的六种类型（按元素种类划分）：
        1、[r1,r2,r3,r4...rn]   单个元数顺序型
        2、[r1,[r2,r3],r4...rn] 以单个元素开头，以单个元素结尾，中间有单个元素、转折元素（TGraphEntity元素）
        3、[r1,[r2,r3],r4...[rn-1,rn]] 以单个元素开头，以转折元素（TGraphEntity元素）结尾，中间有单个元素、转折元素（TGraphEntity元素）
        4、[[r1,r2],r3,[r4,r5]...,rn]] 以转折元素（TGraphEntity元素）开头，以单个元素结尾，中间有单个元素、转折元素（TGraphEntity元素）
        5、[[r1,r2],r3,[r4,r5]...[rn-1,rn]] 以转折元素（TGraphEntity元素）开头，以转折元素（TGraphEntity元素）结尾，中间有单个元素、转折元素（TGraphEntity元素）
        6、[[r1,r2],[r3,r4]...[rn-1,rn]] 转折元素（TGraphEntity元素）顺序型。以转折元素（TGraphEntity元素）开头，以转折元素（TGraphEntity元素）结尾，中间全部都是转折元素（TGraphEntity元素）

    2018-12-14 T字形结构实体类的组成元素的结构，应该有以下几种形式：
    0、单独r      例如：[r]
    1、r 前 r',k  例如：(1)[a,b,c]中的b，(2)[[a,b],c]中的c
    2、r 后 r',k  例如：(3)[a,b,c]中的a、b，(4)[a,[b,c]]中的a
    3、k 前 r,k'  例如：(5)[a,[b,c]]中的[b,c]，(6)[[a,b],[c,d]]中的[c,d]
    4、k 后 r,k'  例如：(7)[[a,b],c]中的[a,b]，(8)[[a,b],[c,d]]中的[a,b]
    其中：(1)=(3)，(2)=(7)，(4)=(5)，(6)=(8)，
    (0)的T字形结构实体类结构：
    id   start   end
    k0     r      None
    另外，(1)和(2)在T字形结构实体类中的结构是等价的，所以必须加以区分
    (1)的T字形结构实体类结构：
    id   start   end
    k0     a      b
    k1     k0     c

    (2)的T字形结构实体类结构：
    id   start   end
    k0     a      b
    k1     k0     List（内部定义集合的标记）
    k2     k1     c
    注：在T字形结构实体类中，start不能为None，end为None的时候，表示将start只有一个元素，例如：[[a]]的集合表示为k1：
    id   start   end
    k0     a      None
    k1     k0     List（内部定义集合的标记）
    """
    __databasename__ = settings.db.db_nvwa  # 所在数据库。
    __tablename__ = None  # 所在表。与Flask统一
    columns = copy.copy(BaseEntity.columns)  # 模型对应的非主键的全部字段
    columns.extend(["startid", "stype", "endid", "etype", "weight",
                    "t_graph", "t_chain", "s_chain", "mnvalue"])

    jsonColumns = copy.copy(
        BaseEntity.jsonColumns)  # 需要用json解析的字段，一般都为text字段，创建(create)、更新(update)，需要解析为json，读取(retrive)时需要从json解析为对象
    jsonColumns.extend(["t_graph", "t_chain", "s_chain"])
    retrieveColumns = copy.copy(BaseEntity.retrieveColumns)  # 查询时需要使用的字段
    retrieveColumns.extend(["startid", "endid"])

    isChainedObject = True  # 是否是链式对象的标记（metaNet、TGraphEntity等）
    curEntityName = "T字形结构实体类"  # 当前T字形结构实体类的名称：元数据网、T字形结构实体类（元数据网、知识链），在两个类中赋值
    curEntityObjType = ObjType.UNKNOWN  # 对象定义类型
    curItemObjType = ObjType.UNKNOWN  # T字形结构实体类元素对象的系统定义类型
    curItemType = None  # T字形结构实体类元素模型类型：MetaData/RealObject
    curItemWordColumn = None  # metaData.mvalue,/MetaData/RealObject.remark

    def __init__(self, start=None, end=None, id=None, stype=None, etype=None,
                 weight=Character.Original_Link_Weight,
                 t_graph=None, t_chain=None, s_chain=None,  # m_chain=None,
                 createrid=None,
                 createtime=None, updatetime=None, lasttime=None,
                 status=200,  # 状态; 0-不可用(逻辑删除);200-正常;800-不可遗忘
                 memory=None):
        """
        元数据/实际对象组成的网（T字形结构实体类，T型单向链）。
        :param id:元数据网ID，UUID。
        :param start:起点元数据/实际对象、T字形结构实体类或RID、id。
        :param end:终点元数据/实际对象、T字形结构实体类或RID、id。
        :param stype:起点的类型，使用ObjType枚举。
        :param etype:终点的类型，使用ObjType枚举。
        :param weight: 起点和终点链接的权重
        :param understood_ratio:understood ratio，理解的程度（0=<ratio=<1，当为1时，就是全部理解，为0时，就是完全不理解）。
        :param type: T字形结构实体类的类型，使用ObjType枚举。
        :param t_graph:是一个T字型结构的由metaData/realObject、TGraphEntity的Id组成的数组(嵌套代表一条TGraphEntity)。格式为：[id,(id,[t_graph])]
        :param t_chain:是一个T字型结构的由metaData/realObject的Id组成的数组(嵌套代表一条TGraphEntity)。
        :param s_chain:是一个未经T字型结构处理的由metaData/realObject的Id组成序列数组
        # :param m_chain 是一个由外域（可能是个T字形结构实体类，也可能是元数据/实际对象）、T字形结构实体类的id组成的序列数组。
        :param createrid: 添加人; 格式：(user_id)中文名
        :param createrip: 添加人IP
        :param createtime: 添加时间;
        :param updatetime: 更新时间
        :param lasttime: 最近访问时间
        :param status: 状态; 0-不可用(逻辑删除);200-正常;800-不可遗忘
        """
        super(TGraphEntity, self).__init__(id,
                                           createrid,
                                           createtime, updatetime, lasttime,
                                           status, memory=memory)

        # 单一链的前、后链对象（运行时数据）
        self._start_item = None
        self._end_item = None

        if start:
            if isinstance(start, str):
                self.startid = start
            elif isinstance(start, BaseEntity):
                self.startid = start.id
                self.stype = start.getType()
                self._start_item = start
        if stype:
            if isinstance(stype, int) or isinstance(stype, str):
                self.stype = stype
            if isinstance(start, BaseEntity):
                self.stype = start.getType()

        if end:
            if isinstance(end, str):
                self.endid = end
            elif isinstance(end, BaseEntity):
                self.endid = end.id
                self.etype = end.getType()
                self._end_item = end
        if etype:
            if isinstance(etype, int) or isinstance(etype, str):
                self.etype = etype
            if isinstance(end, BaseEntity):
                self.etype = end.getType()

        self.weight = weight

        self._isMemoryUseDoubleKeyDict = True  # 内存之中存储是否使用双键字典。
        # 女娲系统的metanet、knowledge、layer的内存存储、查找都使用双键字典

        # ####################################
        #      下面为运行时数据
        # ####################################

        if not t_graph:
            t_graph = []
        self.t_graph = t_graph
        if not t_chain:
            t_chain = []  # [情人节,[[[小明, 给], 小丽], [[一, 朵], [[红色, 的], [玫瑰, 花]]]]
        self.t_chain = t_chain
        if not s_chain:
            s_chain = []  # [情人节,小明, 给, 小丽,一, 朵,红色, 的, 玫瑰, 花]
        self.s_chain = s_chain

        # 是否已经取得了chain的标记
        self._chainItemsProceed = False

        # 所有的后链列表
        self._forwards = {}
        # 所有的前链列表
        self._backwards = {}

        self._chain_items = {}  # 当前TGraphEntity的链包含的所有TGraphEntity、MetaData/RealObject，格式为：{id/id:TGraphEntity/MetaData/RealObject}

        # 实际取得的元数据/实际对象（MetaData/RealObject）。当前知识的元数据/实际对象链
        self._t_chain_items = []
        self._s_chain_items = []

        # 实际取得的元数据/实际对象（MetaData/RealObject）的remark。当前知识的字符串（remark）列表（嵌套代表一条记录）
        self._t_chain_words = []
        self._s_chain_words = []  # 当前T字形结构实体类的构成元素（有顺序）

        self._native_chain = []  # 纯正T字形结构实体类的组成元素id的链，请参看NativeTGraphEntity定义，例如：[r1:我,r2:知道,k1:[牛有腿]]，native_chain就是[r1,r2,k1]，目的是为取出T字形结构实体类的集合
        self._native_chain_items = []  # 纯正T字形结构实体类的组成元素实体的链，请参看NativeTGraphEntity定义，例如：[r1:我,r2:知道,k1:[牛有腿]]，native_chain就是[r1,r2,k1]，目的是为取出T字形结构实体类的集合

        self._sequence_components = []
        self._sequence_component_ids = []
        self._sequence_components_words = []

        self._head = None  # T字形结构实体类的头对象
        self._tail = None  # T字形结构实体类的尾对象

        self.mnvalue = None  # 媒体值，是元数据mvalue拼合的结果（用来供字符串快速查询）
        # 当type为文字时，保存的是文字字符串
        # 当type为声音或图像时，保存的是声音或图像的URI或对象地址

        # 2018-12-06:所有上下层对象一律在Layers中处理
        # # 从数据库中取得的下一层的元数据/实际对象（只能有一个）
        # self._lower_realObject = None  # r:中国-r:人民-r:解放军——>r:中国人民解放军
        #
        # # 从数据库中取得的上一层的元数据网（只能有一个）
        # self._upper_metaNet = None  # m:中国-m:人民-m:解放军——>r:中国-r:人民-r:解放军

    def create(self, checkExist=True, recordInDB=True, **kwargs):
        """
        [重载函数]CRUD - Create（因为要对所有的components进行处理，所以不能简单的对当前的T字形结构实体类（仅仅是start、end）进行处理）
        :param checkExist:检查是否存在
        :param recordInDB:是否在数据库中创建（False返回自身，例如：自然语言的T字形结构实体类（NL_TGraphEntity，奇数位为“下一个为”）就不需要在数据库中创建）
        :return: 返回建立的knowledge。
        """
        components = self.getSequenceComponents()
        return self._createByObjChain(components,
                                      recordInDB=recordInDB,
                                      memory=self.MemoryCentral, **kwargs)

    def getStartItem(self):
        """
        根据startid取得开始的对象（可能是metaData/realObject，也可能是TGraphEntity）
        :return:
        """
        if self.startid is None:
            return None
        if self._start_item:
            return self._start_item
        # 根据前链的类型取得对应的对象（包括：MetaData/RealObject、TGraphEntity）
        if ObjType.isInstance(self.stype, self.curItemObjType) or ObjType.isInstance(self.curItemObjType, self.stype):
            condition = {self.curItemType.primaryKey[0]: self.startid}
            self._start_item = self.curItemType.getOne(memory=self.MemoryCentral, **condition)
        elif ObjType.isInstance(self.stype, self.type) or ObjType.isInstance(self.type, self.stype):
            condition = {self.primaryKey[0]: self.startid}
            self._start_item = self.getOne(memory=self.MemoryCentral, **condition)
        else:
            raise Exception("%s开始对象类型错误：{%d:%s}。" % (self.curEntityName, self.stype, ObjType.getTypeNames(self.stype)))

        if not self._start_item:
            raise Exception(
                "未能取得%s开始对象：{%s:%s,%d:%s}。" % (
                    self.curEntityName, "Id", self.startid, self.stype, ObjType.getTypeNames(self.stype)))
        return self._start_item

    def getEndItem(self):
        """
        根据endid取得结束的对象（可能是metaData/realObject，也可能是TGraphEntity）
        :return:
        """
        if self.endid is None:
            return None
        if self._end_item:
            return self._end_item
        # 根据后链的类型取得对应的对象（包括：MetaData/RealObject、TGraphEntity）
        if self.etype == self.curItemObjType:
            condition = {self.curItemType.primaryKey[0]: self.endid}
            self._end_item = self.curItemType.getOne(memory=self.MemoryCentral, **condition)
        elif self.etype == self.type:
            condition = {self.primaryKey[0]: self.startid}
            self._end_item = self.getOne(memory=self.MemoryCentral, **condition)
        else:
            raise Exception("%s结束对象类型错误：{%s:%s,%d:%s,%s:%s}。" % ("Id", self.endid,self.curEntityName, self.etype, ObjType.getTypeNames(self.etype),"mnvalue",self.mnvalue))

        if not self._end_item:
            raise Exception(
                "未能取得%s结束对象：{%s:%s,%d:%s,%s:%s}。" % (
                    self.curEntityName, "Id", self.endid, self.etype, ObjType.getTypeNames(self.etype),"mnvalue",self.mnvalue))
        return self._end_item

    @classmethod
    def createByStartEnd(cls, start, end,
                         recordInDB=True,
                         checkExist=True,
                         memory=None,
                         **kwargs):
        """
        创建TGraphEntity（允许end为None）
        :param start:可以是MetaData\\MetaData\\RealObject、TGraphEntity或[sid,stype]\\(sid,stype)
        :param end:可以是MetaData\\MetaData\\RealObject、TGraphEntity或[eid,etype]\\(eid,etype)
        :return:
        """
        Instincts.loadAllInstincts(memory=memory)

        # 确保第一个不是list标识符
        if start.id == Instincts.instinct_original_list.id:
            raise Exception("%s的第一个start对象不应是内部集合标记（k1 k0 #List#，将k0包裹在集合中）！" % cls.curEntityName)
        elif isinstance(start, TGraphEntity):
            sid = start.id
            stype = cls.curEntityObjType
        elif isinstance(start, cls.curItemType):
            sid = start.id
            stype = cls.curItemObjType

        elif isinstance(start, list) or isinstance(start, tuple):
            sid = start[0]
            stype = start[1]
        else:
            raise Exception(
                "start对象应为MetaData/MetaData/RealObject或TGraphEntity或[sid,stype]/(sid,stype)，当前类型错误：%s" % type(start))

        if isinstance(end, cls.curItemType):
            eid = end.id
            etype = cls.curItemObjType
        elif isinstance(end, TGraphEntity):
            eid = end.id
            etype = cls.curEntityObjType
        elif isinstance(end, list) or isinstance(end, tuple):
            eid = end[0]
            etype = end[1]
        elif end is None:
            end = Instincts.instinct_none
            eid = end.id
            etype = cls.curItemObjType
        else:
            raise Exception(
                "end对象应为MetaData/MetaData/RealObject或TGraphEntity或[sid,stype]/(sid,stype)，当前类型错误：" + type(start))

        obj = cls(start=sid, stype=stype, end=eid, etype=etype,
                  memory=memory,
                  **kwargs)  # .create(checkExist=checkExist,recordInDB=recordInDB)

        if checkExist:
            exists_obj = obj.getExist()
            if exists_obj:
                obj = exists_obj
            elif memory:
                # 添加到工作内存以便后续操作
                memory.WorkingMemory.addInMemory(obj)
                obj._isInWorkingMemory = True
        elif memory:
            # 添加到工作内存以便后续操作
            memory.WorkingMemory.addInMemory(obj)
            obj._isInWorkingMemory = True

        if isinstance(start, BaseEntity):
            obj._start_item = start
        else:
            obj._start_item = obj.getStartItem()
        if isinstance(end, BaseEntity):
            obj._end_item = end
        else:
            obj._end_item = obj.getEndItem()

        # 填充需要记录到数据库的字段
        obj.getChainItems()

        # 真正创建（内存、数据库）
        if recordInDB and not obj._isInDB:
            obj = obj._createInDB()
            if obj and not obj._isGetByConflictDBColumns:  # 根据重复键违反唯一约束取得已知对象
                obj._isNewCreated = True

            # 添加到工作内存以便后续操作
            if obj and obj.id and obj.MemoryCentral:
                obj.MemoryCentral.WorkingMemory.addInMemory(obj)
                obj._isInWorkingMemory = True

        if obj:
            obj.getChainItems()
        return obj

    @classmethod
    def _createByObjChain(cls,
                          obj_chain,
                          obj_nets=None,
                          recordInDB=True,
                          checkExist=True,
                          memory=None,
                          **kwargs):
        """
        根据元数据/实际对象或T字形结构实体类（元数据网、知识链）序列创建TGraphEntity（完全匹配，顺序相同）
        :param obj_chain:[MetaData/RealObject/TGraphEntity,[MetaData/RealObject/TGraphEntity]]
        :param obj_nets: 最后形成knowledge的子knowledge，例如：k0:[k1:[a,b],k2:[c,d],e],k0的obj_nets就是[k1,k2,e]
        :param type:
        :param understood_ratio:
        :param recordInDB: 是否记录到数据库
        :param recordRelationInFirstReal: 是否将T字形结构实体类（元数据网、知识链）作为关系记录到第一个元数据/实际对象，例如：牛-组件-腿，就将组件-腿的关系记录到牛这个对象中
        :return:
        """
        # 集合对象不能为None
        if obj_chain is None or (not isinstance(obj_chain, list) and not isinstance(obj_chain, tuple)):
            return None
        if len(obj_chain) == 0:
            return None

        Instincts.loadAllInstincts(memory=memory)
        recordRelationInFirstReal = kwargs.get("recordRelationInFirstReal", False)
        kwargs.pop("recordRelationInFirstReal", False)

        # 只有一个对象的T字形结构实体类（元数据网、知识链），例如：[r/k]或[[r1/k1...rn/kn]]
        if len(obj_chain) == 1:  # 这里考虑只有一个对象的集合，例如[牛]，将其转换成knowledge(End为None)
            if isinstance(obj_chain[0], list) or isinstance(obj_chain[0], tuple):
                child_knowledge = cls._createByObjChain(obj_chain[0], obj_nets,
                                                        recordInDB,
                                                        memory=memory,
                                                        **kwargs)
                return cls._createByObjChain([child_knowledge,
                                              Instincts.instinct_original_list],
                                             obj_nets,
                                             recordInDB,
                                             checkExist,
                                             memory=memory,
                                             **kwargs)

            else:
                if obj_chain[0].id == Instincts.instinct_original_list:  # 开始对象不能为List
                    return None
                # 这里考虑只有一个对象的集合，例如[牛]，将其转换成knowledge(End为List)
                return cls._createByObjChain([obj_chain[0],
                                              Instincts.instinct_original_list],
                                             obj_nets,
                                             recordInDB,
                                             checkExist,
                                             memory=memory,
                                             **kwargs)

        cur_tgraph = None
        if obj_nets is None:
            obj_nets = []
        i = 0
        last_obj = None
        while i < len(obj_chain):  # 确保后面至少有一条
            original_cur_obj = obj_chain[i]  # 原始的第一个
            cur_obj = original_cur_obj  # 第一个

            # 处理当前对象
            if cur_obj is None:  # 替换None为instinct_none
                cur_obj = Instincts.instinct_none
            elif isinstance(cur_obj, RelatedObj):
                cur_obj = cur_obj.obj
            elif isinstance(cur_obj, UnknownResult):
                knowledges = []
                for unknown_objs in cur_obj:
                    if isinstance(unknown_objs[0].unknown_obj, TGraphEntity):
                        knowledges.append(unknown_objs[0].unknown_obj)

                cur_obj = cls._createByObjChain(knowledges,
                                                obj_nets,
                                                recordInDB,
                                                checkExist,
                                                memory=memory,
                                                **kwargs)
            if isinstance(cur_obj, UnknownObj):
                cur_obj = cur_obj.unknown_obj
            if isinstance(cur_obj, list):  # 如果当前real是list，创建其子TGraphEntity
                if len(cur_obj) > 0:
                    cur_obj = cls._createByObjChain(cur_obj,
                                                    obj_nets,
                                                    recordInDB,
                                                    checkExist,
                                                    memory=memory,
                                                    **kwargs)
                else:  # 略掉空集合
                    i += 1
                    continue

            # 1、如果前面有了链，往后拼接
            if cur_tgraph:
                # 这里需要对[[a,b],c]这样的T字形结构实体类（元数据网、知识链）进行特殊处理：后面加List
                if isinstance(last_obj, list):
                    # 这里面需要对[[a,b],c]这样的T字形结构实体类（元数据网、知识链）进行特殊处理：后面加List
                    cur_obj = cls.createByStartEnd(cur_obj,
                                                   Instincts.instinct_original_list,
                                                   recordInDB=recordInDB,
                                                   checkExist=checkExist,
                                                   memory=memory,
                                                   **kwargs)

                cur_tgraph = cls.createByStartEnd(cur_tgraph, cur_obj,
                                                  recordInDB=recordInDB,
                                                  checkExist=checkExist,
                                                  memory=memory,
                                                  **kwargs)
                obj_nets.append(cur_tgraph)
                last_obj = cur_obj
                i += 1
                continue

            # 2、这里应该是第一组了，取下一个，然后创建T字形结构实体类（元数据网、知识链）
            next_obj = None
            if i < len(obj_chain) - 1:  # # 确保后面至少有第二个
                next_obj = obj_chain[i + 1]
                if next_obj is None:  # 替换None为instinct_none
                    next_obj = Instincts.instinct_none

                if isinstance(original_cur_obj, list):
                    # 这里面需要对[[a,b],c]这样的T字形结构实体类（元数据网、知识链）进行特殊处理：后面加List
                    cur_obj = cls.createByStartEnd(cur_obj,
                                                   Instincts.instinct_original_list,
                                                   recordInDB=recordInDB,
                                                   checkExist=checkExist,
                                                   memory=memory,
                                                   **kwargs)

                if isinstance(next_obj, RelatedObj):
                    next_obj = next_obj.obj
                if isinstance(next_obj, list):  # 如果下一real是list，创建其子TGraphEntity
                    if len(next_obj) > 0:
                        next_obj = cls._createByObjChain(next_obj,
                                                         obj_nets,
                                                         recordInDB=recordInDB,
                                                         checkExist=checkExist,
                                                         memory=memory,
                                                         **kwargs)
                        # # 这里面需要对[a,[b,c]]这样的T字形结构实体类（元数据网、知识链）进行特殊处理：后面加List
                        # next_obj = cls.createTGraphEntityByStartEnd(next_obj, _Instincts.instinct_original_list)

                    else:
                        i += 1
                        continue

            if next_obj:
                cur_tgraph = cls.createByStartEnd(cur_obj, next_obj,
                                                  recordInDB=recordInDB,
                                                  checkExist=checkExist,
                                                  memory=memory,
                                                  **kwargs)
                obj_nets.append(cur_tgraph)
                i += 2
            else:  # 如果是最后一个
                return cur_obj

        if cur_tgraph:
            cur_tgraph.getChainItems()
            if recordRelationInFirstReal and len(obj_chain) == 3:
                first_real = obj_chain[0]
                relation = obj_chain[1]
                related_obj = obj_chain[2]
                if first_real and isinstance(first_real, cls.curItemType):
                    first_real.Constitutions.addRelatedObject(relation, related_obj)

        return cur_tgraph

    @classmethod
    def getByObjectChain(cls, obj_chain, obj_nets=None, unproceed=None, memory=None):
        """
        根据元数据/实际对象或T字形结构实体类（元数据网、知识链）序列取得TGraphEntity（注意：这里可能是不完全匹配，顺序相同）
        :param obj_chain:[real,[real,real]]
        :param obj_nets:
        :param unproceed: 外部传入的list，记录未处理的对象
        :return:
        """
        if len(obj_chain) < 2:
            return None
        cur_tgraph = None
        if obj_nets is None:
            obj_nets = []

        if unproceed is None:
            unproceed = []

        i = 0
        while i < len(obj_chain):  # 确保后面至少有一条
            cur_obj = obj_chain[i]  # 第一个
            if isinstance(cur_obj, list):
                if len(cur_obj) > 0:  # 如果当前real是list，查询其子TGraphEntity
                    cur_obj = cls.getByObjectChain(cur_obj, obj_nets, unproceed,
                                                   memory=memory)
                    if not cur_obj:  # 破解查询结构不一致
                        cur_obj = obj_chain[i][0]
            # 如果能够与前链“构成”，继续下一个
            if cur_tgraph:
                cur_temp_tgraph = cls.getByStartAndEnd(cur_tgraph, cur_obj,
                                                       memory=memory)
                if cur_temp_tgraph:
                    cur_tgraph = cur_temp_tgraph
                    obj_nets.append(cur_tgraph)
                    i += 1
                    continue
            # 不能与前链“构成”，查看与后一个元素是否能够“构成”
            next_real = None
            if i < len(obj_chain) - 1:  # # 确保后面至少有第二个
                next_real = obj_chain[i + 1]
                if isinstance(next_real, list):  # 如果下一real是list，查询其子TGraphEntity
                    next_real = cls.getByObjectChain(next_real, obj_nets, unproceed, memory=memory)
            if next_real:
                cur_temp_tgraph = cls.getByStartAndEnd(cur_obj, next_real,
                                                       memory=memory)
                if cur_temp_tgraph:
                    test_tgraph = None
                    if len(obj_chain) == 2:  # 如果没有前一个元素、后一个元素，说明是唯一的两个
                        test_tgraph = cur_temp_tgraph
                    if not test_tgraph and cur_tgraph:
                        # 这里需要考虑与cur_tgraph、前元素、后元素是否能够构成一条链，如果不构成，也要抛弃
                        test_tgraph = cls.getByStartAndEnd(cur_tgraph,
                                                           cur_temp_tgraph,
                                                           memory=memory)
                    if not test_tgraph and i - 1 >= 0:
                        last_real = obj_chain[i - 1]  # 前一个元素
                        if last_real:
                            if isinstance(last_real, list):
                                test_tgraph = cls.getByObjectChain([last_real, cur_temp_tgraph],
                                                                   obj_nets,
                                                                   unproceed,
                                                                   memory=memory)
                            else:
                                test_tgraph = cls.getByStartAndEnd(last_real,
                                                                   cur_temp_tgraph,
                                                                   memory=memory)
                    if not test_tgraph and i < len(obj_chain) - 2:
                        next_next_real = obj_chain[i + 2]  # 后一个元素
                        if next_next_real:
                            if isinstance(next_next_real, list):
                                test_tgraph = cls.getByObjectChain([cur_temp_tgraph, next_next_real],
                                                                   obj_nets,
                                                                   unproceed,
                                                                   memory=memory)
                            else:
                                test_tgraph = cls.getByStartAndEnd(cur_temp_tgraph,
                                                                   next_next_real,
                                                                   memory=memory)

                    if not test_tgraph:  # 仍未找到，当前cur_temp_tgraph没有与前后产生构成，暂时放到待处理列表
                        unproceed.insert(0, cur_temp_tgraph)
                        i += 2
                        continue

                    # 如果不是最后一个，把cur_temp_tgraph赋值给cur_tgraph
                    # 反之，如果是最后一个，把cur_temp_tgraph与cur_tgraph粘连
                    if cur_tgraph:
                        cur_last_tgraph = cls.getByStartAndEnd(cur_tgraph,
                                                               cur_temp_tgraph,
                                                               memory=memory)
                        if cur_last_tgraph:
                            cur_tgraph = cur_last_tgraph
                        else:
                            cur_tgraph = cur_temp_tgraph
                    else:
                        cur_tgraph = cur_temp_tgraph

                    # 如果前面有未连成链的，往前附着，连成链
                    cur_unproceed_tgraph = None
                    if len(unproceed) > 0:  # 如果前面有未连成链的，往前附着，连成链
                        cur_unproceed_tgraph = cur_tgraph
                        proceed = []
                        for j in range(len(unproceed)):  # 因为是线性输入，所以进行倒序处理
                            try:
                                cur_unproceed_tgraph = cls.getByStartAndEnd(unproceed[j],
                                                                            cur_unproceed_tgraph,
                                                                            memory=memory)
                                if cur_unproceed_tgraph:
                                    # 继续往前粘连
                                    last_unproceed_tgraph = cur_unproceed_tgraph
                                    last_unproceed_tgraphs = []
                                    for real_net in obj_nets:
                                        last_unproceed_tgraph = cls.getByStartAndEnd(real_net,
                                                                                     last_unproceed_tgraph,
                                                                                     memory=memory)
                                        if last_unproceed_tgraph:
                                            last_unproceed_tgraphs.append(last_unproceed_tgraph)

                                    obj_nets.append(cur_unproceed_tgraph)
                                    if len(last_unproceed_tgraphs) > 0:
                                        obj_nets.extend(last_unproceed_tgraphs)
                                        cur_unproceed_tgraph = last_unproceed_tgraphs[-1]

                                    proceed.append(j)

                            except Exception as e:  # do nothing
                                logger.debug(e)
                                pass
                        # 去掉已经处理过的
                        if len(proceed) > 0:
                            temp_unproceed = []
                            for i in range(len(unproceed)):
                                if not proceed.__contains__(i):
                                    temp_unproceed.append(unproceed[i])
                            unproceed = temp_unproceed

                    obj_nets.append(cur_tgraph)
                    i += 2
                    if cur_unproceed_tgraph:
                        cur_tgraph = cur_unproceed_tgraph
                        i += 2
                        # real_nets.append(cur_tgraph)
                else:  # 仍未找到，当前cur_real没有与前后产生构成，暂时放到待处理列表
                    unproceed.insert(0, cur_obj)
                    i += 1
            else:
                i += 1

        # 如果已经全部匹配了，直接返回结果
        if cur_tgraph and cur_tgraph.getSequenceComponents() == obj_chain:
            return cur_tgraph
        # 由于可能有多个匹配，所以要最后进行过滤，
        # 例如：输入：牛有腿马有头，目前的匹配应该包括：牛有，牛有腿，马有，马有头
        matched_tgraphs = []
        i = 0

        while i < len(obj_nets):
            cur_tgraph = obj_nets[i]
            cur_tgraph_index = 0
            has_contained = False

            cur_tgraph_components = cur_tgraph.getSequenceComponents()
            j = i + 1
            while j < len(obj_nets):
                next_tgraph = obj_nets[j]
                next_tgraph_components = next_tgraph.getSequenceComponents()
                if Collection.contains(next_tgraph_components, cur_tgraph_components):
                    cur_tgraph_components = next_tgraph_components
                    cur_tgraph_index = j
                    has_contained = True
                j += 1

            if has_contained:
                matched_tgraphs.append(obj_nets[cur_tgraph_index])
            i += 1

        matched_tgraphs=list(set(matched_tgraphs)) # 去重
        if len(matched_tgraphs) == 1:  # 扒皮
            return matched_tgraphs[0]

        return matched_tgraphs

    @classmethod
    def getLikeObjChain(cls, objChain, memory=None):
        """
        根据realChain取得TGraphEntity（不完全匹配，使用s_chain进行近似匹配，根据匹配数量、匹配对象的weight进行排序）
        :param objChain:[realData,[realData,realData]]
        :return:
        """
        # todo 目前还是使用全文匹配，未来应该使用近似匹配
        idChain, is_sequence = cls.getIdChainByObjChain(objChain)
        like = jsonplus.dumps(idChain)
        if is_sequence:
            tgraph = cls.getAllLikeByInDB(s_chain=like, memory=memory)
        else:
            tgraph = cls.getAllLikeByInDB(t_chain=like, memory=memory)

        if tgraph:
            tgraph.getChainItems()
        return tgraph

    def getAllLikeByHeadAndTailInDB(self, attribute):
        """
        取得所有以头部对象开始，以尾部对象结尾的T字形结构实体类（元数据网、知识链），例如：给定苹果、红，查找出T字形结构实体类（元数据网、知识链）苹果-颜色-红。
        :param attribute:
        :return:
        """
        self.getChainItems()
        if self._head is None:
            raise Exception("必须提供头部对象以便查找！")
        if self._tail is None:
            raise Exception("必须提供尾部对象以便查找！")

        return self.getAllLikeByStartMiddleEndInDB(attribute, "[" + self._head.id, self._tail.id + "]")

    @classmethod
    def getByObjs(cls, objs, memory=None):
        """
        根据散列化的元数据/实际对象或T字形结构实体类（元数据网、知识链）取得TGraphEntity（顺序不一定相同）
        :param realChain:[realData,[realData,realData]]
        :return:
        """
        if len(objs) < 2:
            return None
        # 取得第一条记录，并根据上下条记录关系，并取得最终排序的结果
        cur_tgraph = None  # 第一条记录

        found_first = False
        for i in range(len(objs)):
            cur_related_tgraph = objs[i]
            cur_tgraph = cls.getByStartInDB(cur_related_tgraph, memory=memory)
            if cur_tgraph:  # 找到了，停止
                if isinstance(cur_tgraph, list):  # 如果有很多个，找到related_ks中的一个T字形结构实体类（元数据网、知识链）为结尾的
                    for _next_tgraph in cur_tgraph:
                        _next_tgraph.getChainItems()
                        if _next_tgraph._end_item in objs:
                            found_first = True
                            cur_tgraph = _next_tgraph
                            break
                elif isinstance(cur_tgraph, TGraphEntity):
                    cur_tgraph.getChainItems()
                    if cur_tgraph._end_item in objs:
                        found_first = True
                        break
            if found_first:
                break

        if not found_first:  # 没有找到第一个节点，应该是一个没有顺序的集合，直接返回现有列表
            return None

        while True:  # 递归查找下一个节点
            found_next = False
            next_tgraph = cls.getByStartInDB(cur_tgraph, memory=memory)
            if not next_tgraph:  # 如果没找到，说明后面没有节点了
                break

            if isinstance(next_tgraph, list):
                for _next_tgraph in next_tgraph:
                    _next_tgraph.getChainItems()
                    if _next_tgraph._end_item in objs:
                        cur_tgraph = _next_tgraph
                        found_next = True
                        break
            elif isinstance(next_tgraph, TGraphEntity):
                next_tgraph.getChainItems()
                if next_tgraph._end_item in objs:
                    cur_tgraph = next_tgraph
                    found_next = True

            if not found_next:
                break

        # 检查两者是否相等（长度）
        cur_tgraph.getChainItems()
        if len(cur_tgraph._s_chain_items) != len(objs):
            cur_tgraph = None

        return cur_tgraph

    @classmethod
    def getIdChainByObjChain(cls, objChain):
        """
        取得realobject、meta_net_matched_knowledges Chain的id列表
        :param objChain:
        :return:
        """
        id_chain = []
        is_sequence = True
        for obj in objChain:
            if isinstance(obj, list):
                id_chain.append(cls.getIdChainByObjChain(obj))
                is_sequence = False
            elif isinstance(obj, cls.curItemType):
                id_chain.append(obj.id)
            elif isinstance(obj, TGraphEntity):
                id_chain.append(obj.id)

        return id_chain, is_sequence

    def getChainItems(self, keepEnd=False):
        """
        不断递归取得当前链的所有StartItem、EndItem对象（TGraphEntity、MetaData/RealObject）
        :param keepEnd: 如果 end以TGraphEntity结尾，是否将endItem的TGraphEntity保留，如果不保留，意味着嵌套集合列表，例如：牛-有-腿-TGraphEntity(我-知道)，还原为：[[牛,有,腿],[我-知道]],否则将添加TGraphEntity
        :return:
        """
        # 递归取得元素
        # 例如：
        #         s     e
        # k0      1     2
        # k1      3     k0
        # k2      k1    4
        # 最终要取得：[3,[1,2],4]

        if self._chainItemsProceed:
            return
        Instincts.loadAllInstincts(memory=self.MemoryCentral)

        self.getStartItem()
        self.getEndItem()

        _start_is_real = False
        _end_is_real = False

        # 处理t_graph、s_chain、t_chain、_word_chain等
        self.t_graph = []
        self.t_chain = []
        self.s_chain = []
        # self.m_chain=[]
        self._t_chain_items = []
        self._s_chain_items = []

        self._native_chain = []  # 纯正T字形结构实体类的组成元素id的链，请参看NativeTGraphEntity定义，例如：[r1:我,r2:知道,k1:[牛有腿]]，native_chain就是[r1,r2,k1]
        self._native_chain_items = []  # 纯正T字形结构实体类的组成元素实体的链，，请参看NativeTGraphEntity定义，例如：[r1:我,r2:知道,k1:[牛有腿]]，native_chain就是[r1,r2,k1]

        self._t_chain_words = []
        self._s_chain_words = []

        self._sequence_components = []
        self._sequence_component_ids = []
        self._sequence_components_words = []

        # 处理头部
        if isinstance(self._start_item, TGraphEntity):
            self._chain_items[self._start_item.id] = self._start_item
            self._start_item.getChainItems()  # ,original=original)
            if self._start_item._head:  # 取得链的头（是一个TGraphEntity）
                self._head = self._start_item._head

            start_components = self._start_item._sequence_components
            start_component_ids = self._start_item._sequence_component_ids
            # 处理尾部
            if isinstance(self._end_item, TGraphEntity):  # TGraphEntity-TGraphEntity
                self._chain_items[self._end_item.id] = self._end_item

                self._end_item.getChainItems()
                if self._end_item._tail:  # 取得链的尾（是一个TGraphEntity）
                    self._tail = self._end_item._tail

                # 处理t_graph、s_chain、t_chain、_word_chain等
                # 在前逐元素插入
                self.s_chain = self._start_item.s_chain + self.s_chain + self._end_item.s_chain
                self.t_graph.insert(0, (self.id, [self._start_item.t_graph, self._end_item.t_graph]))
                self.t_chain.insert(0, [self._start_item.t_chain, self._end_item.t_chain])

                # 实际取得的元数据/实际对象（MetaData/RealObject）
                self._t_chain_items.insert(0, [self._start_item._t_chain_items, self._end_item._t_chain_items])
                self._s_chain_items = self._start_item._s_chain_items + self._s_chain_items + self._end_item._s_chain_items

                # 实际取得的元数据/实际对象（MetaData/RealObject）的remark
                self._t_chain_words.insert(0, [self._start_item._t_chain_words, self._end_item._t_chain_words])
                self._s_chain_words = self._start_item._s_chain_words + self._s_chain_words + self._end_item._s_chain_words

                if self._start_item.isNative():
                    self._native_chain.insert(0, self._start_item.id)
                    if self._end_item.isNative():
                        self._native_chain.insert(1, self._end_item.id)
                    else:
                        self._native_chain.insert(1, self._end_item.id)

                if keepEnd:
                    self._sequence_components.extend(start_components)
                    self._sequence_components.append(self._end_item)

                    self._sequence_component_ids.extend(start_component_ids)
                    self._sequence_component_ids.append(self._end_item.id)
                else:
                    end_components = self._end_item.getSequenceComponents(keepEnd)
                    self._sequence_components.extend(start_components)
                    self._sequence_components.append(end_components)

                    end_component_ids = self._end_item._sequence_component_ids
                    self._sequence_component_ids.extend(start_component_ids)
                    self._sequence_component_ids.append(end_component_ids)

            elif isinstance(self._end_item, self.curItemType):  # TGraphEntity-MetaData/RealObject
                self._chain_items[self._end_item.id] = self._end_item
                _end_is_real = True

                # 处理t_graph、s_chain、t_chain、_word_chain等
                # 在前逐元素插入
                self.s_chain.extend(self._start_item.s_chain)
                self.s_chain.append(self._end_item.id)
                self.t_graph.insert(0, (self.id, [self._start_item.t_graph, self._end_item.id]))
                self.t_chain.insert(0, [self._start_item.t_chain, self._end_item.id])

                # 实际取得的元数据/实际对象（MetaData/RealObject）
                self._t_chain_items.insert(0, [self._start_item._t_chain_items, self._end_item])
                self._s_chain_items.extend(self._start_item._s_chain_items)
                self._s_chain_items.append(self._end_item)

                # 实际取得的元数据/实际对象（MetaData/RealObject）的remark
                self._t_chain_words.insert(0, [self._start_item._t_chain_words, self._getItemWord(self._end_item)])
                self._s_chain_words.extend(self._start_item._s_chain_words)
                self._s_chain_words.append(self._getItemWord(self._end_item))

                # 如果 end以List结尾，意味着嵌套集合列表，例如：牛-有-腿-Lsit，还原为：[[牛,有,腿]],视情况添加None
                if self._end_item.id == Instincts.instinct_original_list.id:
                    self._sequence_components.append(start_components)
                    self._sequence_component_ids.append(start_component_ids)
                else:
                    self._sequence_components.extend(start_components)
                    self._sequence_components.append(self._end_item)

                    self._sequence_component_ids.extend(start_component_ids)
                    self._sequence_component_ids.append(self._end_item.id)

            else:
                raise Exception("T字形结构实体类的结尾应为元数据/实际对象或T字形结构实体类！")
        elif isinstance(self._start_item, self.curItemType):
            self._chain_items[self._start_item.id] = self._start_item
            _start_is_real = True

            # 处理尾部
            if isinstance(self._end_item, TGraphEntity):  # MetaData/RealObject-TGraphEntity
                self._chain_items[self._end_item.id] = self._end_item

                self._end_item.getChainItems()  # ,original=original)
                if self._end_item._tail:  # 取得链的尾（是一个TGraphEntity）
                    self._tail = self._end_item._tail

                # 处理t_graph、s_chain、t_chain、_word_chain等
                # 在前逐元素插入
                self.s_chain.append(self._start_item.id)
                self.s_chain += self._end_item.s_chain
                self.t_graph.insert(0, (self.id, [self._start_item.id, self._end_item.t_graph]))
                self.t_chain.insert(0, [self._start_item.id, self._end_item.t_chain])

                # 实际取得的元数据/实际对象（MetaData/RealObject）
                self._s_chain_items.append(self._start_item)
                self._s_chain_items += self._end_item._s_chain_items
                self._t_chain_items.insert(0, [self._start_item, self._end_item._t_chain_items])

                # 实际取得的元数据/实际对象（MetaData/RealObject）的remark
                self._s_chain_words.append(self._getItemWord(self._start_item))
                self._s_chain_words += self._end_item._s_chain_words
                self._t_chain_words.insert(0, [self._getItemWord(self._start_item), self._end_item._t_chain_words])

                self._sequence_components.append(self._start_item)
                self._sequence_component_ids.append(self._start_item.id)
                if keepEnd:
                    self._sequence_components.append(self._end_item)
                    self._sequence_component_ids.append(self._end_item.id)
                else:
                    end_components = self._end_item.getSequenceComponents(keepEnd)
                    self._sequence_components.append(end_components)

                    end_component_ids = self._end_item._sequence_component_ids
                    self._sequence_component_ids.append(end_component_ids)

            elif isinstance(self._end_item, self.curItemType):  # MetaData/RealObject-MetaData/RealObject
                self._chain_items[self._end_item.id] = self._end_item
                _end_is_real = True

                # 处理t_graph、s_chain、t_chain、_word_chain等
                # 在前逐元素插入
                self.s_chain.extend([self._start_item.id, self._end_item.id])
                self.t_graph.extend([(self.id, [self._start_item.id, self._end_item.id])])
                self.t_chain.extend([self._start_item.id, self._end_item.id])
                # self.m_chain.extend([self.id])

                # 实际取得的元数据/实际对象（MetaData/RealObject）
                self._s_chain_items.extend([self._start_item, self._end_item])
                self._t_chain_items.extend([self._start_item, self._end_item])

                # 实际取得的元数据/实际对象（MetaData/RealObject）的remark
                words = [self._getItemWord(self._start_item), self._getItemWord(self._end_item)]
                self._s_chain_words.extend(words)
                self._t_chain_words.extend(words)

                # 如果 end以List结尾，意味着嵌套集合列表，例如：牛-有-腿-Lsit，还原为：[[牛,有,腿]],视情况添加None
                if self._end_item.id == Instincts.instinct_original_list.id:
                    self._sequence_components.append(self._start_item)
                    self._sequence_component_ids.append(self._start_item.id)
                else:
                    self._sequence_components.append(self._start_item)
                    self._sequence_components.append(self._end_item)

                    self._sequence_component_ids.append(self._start_item.id)
                    self._sequence_component_ids.append(self._end_item.id)
        else:
            raise Exception("T字形结构实体类的开始应为元数据/实际对象或T字形结构实体类！")

        if _start_is_real and _end_is_real:
            self._head = self._start_item
            self._tail = self._end_item

        # 处理t_graph、s_chain、t_chain、_word_chain等
        if len(self.t_chain) == 1:
            self.t_chain = self.t_chain[0]
        if len(self._t_chain_items) == 1:
            self._t_chain_items = self._t_chain_items[0]
        if len(self._t_chain_words) == 1:
            self._t_chain_words = self._t_chain_words[0]

        self.mnvalue = "".join(self._s_chain_words)

        # 标记已经取得了chain
        self._chainItemsProceed = True

    def _getItemWord(self, item):
        """
        取得metaData的mvalue/realObject的remark，没有的时候返回id
        :param item:
        :return:
        """
        word = getattr(item, self.curItemWordColumn)
        if word:
            return word
        else:
            return item.id

    def getSequenceComponents(self, keepEnd=False):
        """
        取得一个T字形结构实体类（元数据网、知识链）的构成元素（有顺序）
        :param keepEnd: 如果 end以TGraphEntity结尾，是否将endItem的TGraphEntity保留，如果不保留，意味着嵌套集合列表，例如：牛-有-腿-TGraphEntity(我-知道)，还原为：[[牛,有,腿],[我-知道]],否则将添加TGraphEntity
        :return:
        """
        # 递归取得元素，规则为end直接保留，start如果是knowledge继续往上扒
        # 例如：
        #         s     e
        # k0      1     2
        # k1      k0    3
        # k2      k1    4
        # 最终要取得：[1,2,3,4]

        # 如果已经取得了，直接返回
        # if self._sequence_components:
        #     return self._sequence_components
        self.getChainItems(keepEnd)
        return self._sequence_components

    def isNative(self):
        """
        是否都是由metadata/realobject构成的T字形结构实体类（元数据网、知识链）。例如：r:牛-r:有-r:腿
        :return:
        """
        components = self.getSequenceComponents()
        for component in components:
            if not isinstance(component, self.curItemType):
                return False

        return True

    def getAllForwardsInMemory(self, depth=Character.Search.TGraphEntity_Forwards_Depth, lazy_get=True):
        """
        取得以当前TGraphEntity的kid为startid的所有后链（后链，即被域对象，以当前T字形结构实体类（元数据网、知识链）为开始）。
        :param lazy_get 是否等需要的时候再取得对应的对象（以getChainItems填充）
        :param depth: 查找T字形结构实体类（元数据网、知识链）的层深，-1表示不限层深。数值越大，查找到的T字形结构实体类（元数据网、知识链）越多，但需要处理的也越多，系统耗时越长
        :return: 后链列表[TGraphEntity]
        """
        if len(self._forwards) > 0:
            return self._forwards
        forwards_tgraphs = []
        self._getAllForwardsInMemory(self, forwards_tgraphs, depth, lazy_get, memory=self.MemoryCentral)
        if forwards_tgraphs:
            if isinstance(forwards_tgraphs, list):
                for tgraph in forwards_tgraphs:
                    self._forwards[tgraph.id] = tgraph
            elif isinstance(forwards_tgraphs, TGraphEntity):
                self._forwards[forwards_tgraphs.id] = forwards_tgraphs

        return self._forwards

    @classmethod
    def _getAllForwardsInMemory(cls,
                                tgraph, forwards_tgraphs,
                                depth=Character.Search.TGraphEntity_Forwards_Depth,
                                lazy_get=True,
                                memory=None):
        """
        [递归]取得以当前TGraphEntity的id为startid的所有后链（后链，即被域对象，以当前T字形结构实体类（元数据网、知识链）为开始）。
        :param lazy_get 是否等需要的时候再取得对应的对象（以getChainItems填充）
        :param depth: 查找T字形结构实体类（元数据网、知识链）的层深，-1表示不限层深。数值越大，查找到的T字形结构实体类（元数据网、知识链）越多，但需要处理的也越多，系统耗时越长
        :return: 后链列表[TGraphEntity]
        """
        tgraphs = cls.getByStartInMemory(tgraph, lazy_get, memory=memory)
        if tgraphs:
            if isinstance(tgraphs, list):
                forwards_tgraphs.extend(tgraphs)
                if depth > 0 or depth < 0:  # 只要是0，就停机
                    for tgraph in tgraphs:
                        # 继续取得以tgraph为开头的T字形结构实体类（元数据网、知识链）
                        cls._getAllForwardsInMemory(tgraph, forwards_tgraphs, depth - 1, lazy_get,
                                                    memory=memory)
            elif isinstance(tgraphs, TGraphEntity):
                forwards_tgraphs.append(tgraphs)
                if depth > 0 or depth < 0:  # 只要是0，就停机
                    # 继续取得以tgraph为开头的T字形结构实体类（元数据网、知识链）
                    cls._getAllForwardsInMemory(tgraphs, forwards_tgraphs, depth - 1, lazy_get,
                                                memory=memory)

    def getAllForwardsInDB(self,
                           depth=Character.Search.TGraphEntity_Forwards_Depth,
                           lazy_get=True):
        """
        取得以当前TGraphEntity的id为startid的所有后链（后链，即被域对象，以当前T字形结构实体类（元数据网、知识链）为开始）。
        :param lazy_get 是否等需要的时候再取得对应的对象（以getChainItems填充）
        :param depth: 查找T字形结构实体类（元数据网、知识链）的层深，-1表示不限层深。数值越大，查找到的T字形结构实体类（元数据网、知识链）越多，但需要处理的也越多，系统耗时越长
        :return: 后链列表[TGraphEntity]
        """
        if len(self._forwards) > 0:
            return self._forwards
        forwards_tgraphs = []
        self._getAllForwardsInDB(self,
                                 forwards_tgraphs, depth, lazy_get,
                                 memory=self.MemoryCentral)
        if forwards_tgraphs:
            if isinstance(forwards_tgraphs, list):
                for tgraph in forwards_tgraphs:
                    self._forwards[tgraph.id] = tgraph
            elif isinstance(forwards_tgraphs, TGraphEntity):
                self._forwards[forwards_tgraphs.id] = forwards_tgraphs

        return self._forwards

    @classmethod
    def _getAllForwardsInDB(cls, tgraph, forwards_tgraphs,
                            depth=Character.Search.TGraphEntity_Forwards_Depth,
                            lazy_get=True,
                            memory=None):
        """
        [递归]取得以当前TGraphEntity的id为startid的所有后链（后链，即被域对象，以当前T字形结构实体类（元数据网、知识链）为开始）。
        :param lazy_get 是否等需要的时候再取得对应的对象（以getChainItems填充）
        :param depth: 查找T字形结构实体类（元数据网、知识链）的层深，-1表示不限层深。数值越大，查找到的T字形结构实体类（元数据网、知识链）越多，但需要处理的也越多，系统耗时越长
        :return: 后链列表[TGraphEntity]
        """
        tgraphs = cls.getByStartInDB(tgraph, lazy_get, memory=memory)
        if tgraphs:
            if isinstance(tgraphs, list):
                forwards_tgraphs.extend(tgraphs)
                if depth > 0 or depth < 0:  # 只要是0，就停机
                    for tgraph in tgraphs:
                        # 继续取得以tgraph为开头的T字形结构实体类（元数据网、知识链）
                        cls._getAllForwardsInDB(tgraph, forwards_tgraphs, depth - 1, lazy_get,
                                                memory=memory)
            elif isinstance(tgraphs, TGraphEntity):
                forwards_tgraphs.append(tgraphs)
                if depth > 0 or depth < 0:  # 只要是0，就停机
                    # 继续取得以tgraph为开头的T字形结构实体类（元数据网、知识链）
                    cls._getAllForwardsInDB(tgraphs, forwards_tgraphs, depth - 1, lazy_get,
                                            memory=memory)

    def getAllBackwardsInDB(self, depth=Character.Search.TGraphEntity_Backwards_Depth, lazy_get=True):
        """
        取得以当前TGraphEntity的id为endid的所有前链（前链，即域对象、域或标签，以当前T字形结构实体类（元数据网、知识链）为结束）。
        eg:
            self = [猪能说话]
            return [[西游记], [中国[上古[史诗神话]]], [猪八戒], [小猪佩奇]...]
        :param lazy_get 是否等需要的时候再取得对应的对象（以getChainItems填充）
        :param depth: 查找T字形结构实体类（元数据网、知识链）的层深，-1表示不限层深。数值越大，查找到的T字形结构实体类（元数据网、知识链）越多，但需要处理的也越多，系统耗时越长
        :return: 前链列表[TGraphEntity]
        """
        if len(self._backwards) > 0:
            return self._backwards
        backwards_tgraphs = []
        self._getAllBackwardsInDB(self, backwards_tgraphs, depth, lazy_get, memory=self.MemoryCentral)
        if backwards_tgraphs:
            if isinstance(backwards_tgraphs, list):
                for tgraph in backwards_tgraphs:
                    self._backwards[tgraph.id] = tgraph
            elif isinstance(backwards_tgraphs, TGraphEntity):
                self._backwards[backwards_tgraphs.id] = backwards_tgraphs

        return self._backwards

    @classmethod
    def _getAllBackwardsInDB(cls, tgraph, backwards_tgraphs,
                             depth=Character.Search.TGraphEntity_Backwards_Depth,
                             lazy_get=True,
                             memory=None):
        """
        [递归]取得以当前TGraphEntity的id为endid的所有前链（前链，即域对象、域或标签，以当前T字形结构实体类（元数据网、知识链）为结束）。
        eg:
            self = [猪能说话]
            return [[西游记], [中国[上古[史诗神话]]], [猪八戒], [小猪佩奇]...]
        :param lazy_get: 是否等需要的时候再取得对应的对象（以getChainItems填充）
        :param depth: 查找T字形结构实体类（元数据网、知识链）的层深，-1表示不限层深。数值越大，查找到的T字形结构实体类（元数据网、知识链）越多，但需要处理的也越多，系统耗时越长
        :return: 前链列表[TGraphEntity]
        """
        tgraphs = cls.getByStartInDB(tgraph, lazy_get, memory=memory)
        if tgraphs:
            if isinstance(tgraphs, list):
                backwards_tgraphs.extend(tgraphs)
                if depth > 0 or depth < 0:  # 只要是0，就停机
                    for tgraph in tgraphs:
                        # 继续取得以tgraph为开头的T字形结构实体类（元数据网、知识链）
                        cls._getAllBackwardsInDB(tgraph, backwards_tgraphs, depth - 1, lazy_get,
                                                 memory=memory)
            elif isinstance(tgraphs, TGraphEntity):
                backwards_tgraphs.append(tgraphs)
                if depth > 0 or depth < 0:  # 只要是0，就停机
                    # 继续取得以tgraph为开头的T字形结构实体类（元数据网、知识链）
                    cls._getAllBackwardsInDB(tgraphs, backwards_tgraphs, depth - 1, lazy_get,
                                             memory=memory)

    @classmethod
    def getByStartInMemory(cls, start, lazy_get=True, memory=None):
        """
        查找以start开头的所有T字形结构实体类（元数据网、知识链）
        :param start: MetaData/RealObject、TGraphEntity、id或是rid(BaseEntity及其继承类，或 Id字符串)
        :param lazy_get 是否等需要的时候再取得对应的对象（以getChainItems填充）
        :return: [TGraphEntity]
        """
        if not memory:
            return None
        if not start:
            raise Exception("start(%s)不能为空！" % start)

        startid = BaseEntity._getId(start)
        tgraphs = cls.getAllByRetriveColumnsInMemory(memory=memory, startid=startid)

        if not lazy_get and tgraphs:
            if isinstance(tgraphs, list):
                for tgraph in tgraphs:
                    tgraph.getChainItems()
            else:
                tgraphs.getChainItems()

        return tgraphs

    @classmethod
    def getByStartInDB(cls, start, lazy_get=True, memory=None):
        """
        查找以start开头的所有T字形结构实体类（元数据网、知识链）
        :param start: MetaData/RealObject、TGraphEntity、id或是rid(BaseEntity及其继承类，或 Id字符串)
        :param lazy_get 是否等需要的时候再取得对应的对象（以getChainItems填充）
        :return: [TGraphEntity]
        """
        if not start:
            raise Exception("start(%s)不能为空！" % start)

        startid = BaseEntity._getId(start)
        tgraphs = cls.getAllByConditionsInDB(memory=memory, startid=startid)

        if not lazy_get and tgraphs:
            if isinstance(tgraphs, list):
                for tgraph in tgraphs:
                    tgraph.getChainItems()
            else:
                tgraphs.getChainItems()

        return tgraphs

    @classmethod
    def getByEndInDB(cls, end, lazy_get=True, memory=None):
        """
        查找以end结尾的所有T字形结构实体类（元数据网、知识链）
        :rawParam end: MetaData/RealObject、TGraphEntity、id或是rid(BaseEntity及其继承类，或 Id字符串)
        :param lazy_get 是否等需要的时候再取得对应的对象（以getChainItems填充）
        :return: [TGraphEntity]
        """
        if not end:
            raise Exception("end(%s)不能为空！" % end)

        endid = BaseEntity._getId(end)

        tgraphs = cls.getAllByConditionsInDB(memory=memory, endid=endid)

        if not lazy_get and tgraphs:
            if isinstance(tgraphs, list):
                for tgraph in tgraphs:
                    tgraph.getChainItems()
            else:
                tgraphs.getChainItems()

        return tgraphs

    @classmethod
    def getByEndInMemory(cls, end, lazy_get=True, memory=None):
        """
        查找以start开头的所有T字形结构实体类（元数据网、知识链）
        :param end: MetaData/RealObject、TGraphEntity、id或是rid(BaseEntity及其继承类，或 Id字符串)
        :param lazy_get 是否等需要的时候再取得对应的对象（以getChainItems填充）
        :return: [TGraphEntity]
        """
        if not memory:
            return None
        if not end:
            raise Exception("end(%s)不能为空！" % end)

        endid = BaseEntity._getId(end)
        tgraphs = cls.getAllByRetriveColumnsInMemory(memory=memory, endid=endid)

        if not lazy_get and tgraphs:
            if isinstance(tgraphs, list):
                for tgraph in tgraphs:
                    tgraph.getChainItems()
            else:
                tgraphs.getChainItems()

        return tgraphs

    @classmethod
    def getByStartAndEnd(cls, start, end, lazy_get=False, memory=None):
        """
        在内存或数据库中查找以start开头并且以end结尾的元数据链(只能有一条)
        :param start: MetaData/RealObject、TGraphEntity、id或是rid(BaseEntity及其继承类，或 Id字符串)
        :param end: MetaData/RealObject、TGraphEntity、id或是rid(BaseEntity及其继承类，或 Id字符串)
        :param lazy_get 是否等需要的时候再取得对应的对象（以getChainItems填充）
        :return: TGraphEntity
        """
        # 首先在内存中查找
        tgraph = cls.getByStartAndEndInMemory(start, end, memory=memory)
        if tgraph:
            return tgraph
        # 内存没找到，在数据库中查找
        tgraph = cls.getByStartAndEndInDB(start, end, lazy_get, memory=memory)
        return tgraph

    @classmethod
    def getByStartAndEndInMemory(cls, start, end, memory=None):
        """
        [内存操作]查找以start开头并且以end结尾的元数据链(只能有一条)
        :param start: MetaData/RealObject、TGraphEntity、id或是rid(BaseEntity及其继承类，或 Id字符串)
        :param end: MetaData/RealObject、TGraphEntity、id或是rid(BaseEntity及其继承类，或 Id字符串)
        :return: TGraphEntity
        """
        if memory:
            if not start:
                raise Exception("start(%s)不能为空！" % start)
            if not end:
                raise Exception("end(%s)不能为空！" % end)

            startid = BaseEntity._getId(start)
            endid = BaseEntity._getId(end)
            return memory.getByDoubleKeysInMemory(startid, endid, cls)

    @classmethod
    def getByStartAndEndInDB(cls, start, end, lazy_get=True, memory=None):
        """
        [数据库操作]查找以start开头并且以end结尾的元数据链(只能有一条)
        :param start: MetaData/RealObject、TGraphEntity、id或是rid(BaseEntity及其继承类，或 Id字符串)
        :param end: MetaData/RealObject、TGraphEntity、id或是rid(BaseEntity及其继承类，或 Id字符串)
        :param lazy_get 是否等需要的时候再取得对应的对象（以getChainItems填充）
        :return: TGraphEntity
        """
        if not start:
            raise Exception("start(%s)不能为空！" % start)
        if not end:
            raise Exception("end(%s)不能为空！" % end)

        startid = BaseEntity._getId(start)
        endid = BaseEntity._getId(end)
        tgraphs = cls.getAllByConditionsInDB(memory=memory, startid=startid, endid=endid)
        if tgraphs is None:
            return None
        if isinstance(tgraphs, list):
            if tgraphs is None or len(tgraphs) == 0:
                return None
            if len(tgraphs) > 1:
                raise Exception("以start开头并且以end结尾的T字形结构实体类（元数据网、知识链）只能有一条,start:%s,start type:%s,end:%s,end type:%s" % (
                    startid, str(type(start)), endid, str(type(end))))

            tgraph = tgraphs[0]
        else:
            tgraph = tgraphs

        tgraph._start_item = start
        tgraph._end_item = end

        if not lazy_get:
            tgraph.getChainItems()

        # 添加到内存以便后续操作
        if memory:
            memory.PersistentMemory.addInMemory(tgraph)

        return tgraph

    def delete(self, deleteRelatedLayers=True, deleteChainedObjs=True):
        """
        [数据库操作]重写逻辑删除，逻辑删除TGraphEntity之前先把相关的关系逻辑删除。
        :return:
        """
        # 逻辑删除所有以本TGraphEntity开始和结束的TGraphEntity
        self.deleteByStart(self)
        self.deleteByEnd(self)

        return super(TGraphEntity, self).delete(deleteRelatedLayers, deleteChainedObjs)

    @classmethod
    def deleteByStart(cls, start):
        """
        根据开始对象，逻辑删除所有TGraphEntity
        :param start:BaseEntity及其继承类，或 Id字符串
        :return:
        """
        if start is None:
            raise Exception("无法逻辑删除所有TGraphEntity，start is None！")
        tgraphs = cls.getByStartInDB(start)
        if isinstance(tgraphs, list):
            for tgraph in tgraphs:
                tgraph.delete()
        elif isinstance(tgraphs, TGraphEntity):
            tgraphs.delete()

    @classmethod
    def deleteByEnd(cls, end):
        """
        根据结尾对象，逻辑删除所有TGraphEntity
        :param end:BaseEntity及其继承类，或 Id字符串
        :return:
        """
        if end is None:
            raise Exception("无法逻辑删除所有TGraphEntity，end is None！")
        tgraphs = cls.getByEndInDB(end)
        if isinstance(tgraphs, list):
            for tgraph in tgraphs:
                tgraph.delete()
        elif isinstance(tgraphs, TGraphEntity):
            tgraphs.delete()

    def deleteAllBackwardsInDB(self):
        """
        删除以当前TGraphEntity的id为endid的所有前链（前链，即域对象、域或标签，以当前T字形结构实体类（元数据网、知识链）为结束）。
        :return:
        """
        backwards = self.getAllBackwardsInDB()
        if backwards:
            for _id, backward in backwards:
                backward.delete()

    def deleteAllForwardsInDB(self):
        """
        删除以当前TGraphEntity的id为startid的所有后链。
        :return:
        """
        forwards = self.getAllForwardsInDB()
        if forwards:
            for _id, forward in forwards:
                forward.delete()

    @classmethod
    def deleteByStartAndEnd(cls, start, end):
        """
        根据start,end取得TGraphEntity，进行逻辑删除。
        :param start: MetaData/RealObject、TGraphEntity、id或是rid(BaseEntity及其继承类，或 Id字符串)
        :param end:  MetaData/RealObject、TGraphEntity、id或是rid(BaseEntity及其继承类，或 Id字符串)
        :return:
        """
        tgraph = cls.getByStartAndEnd(start, end)
        if tgraph:
            tgraph.delete()

    @classmethod
    def deleteByObjChain(cls, objChain, deleteAllChain=False):
        """
        根据realChain删除TGraphEntity
        :param objChain:[realData,[realData,realData]]
        :param deleteAllChain 是否删除全链
        :return:
        """
        if len(objChain) < 2:
            return
        real_nets = []
        tgraph = cls.getByObjectChain(objChain, real_nets)
        if deleteAllChain:
            for real_net in real_nets:
                real_net.delete()
        elif tgraph:
            tgraph.delete()
        return tgraph
        # start = objChain[0]
        # for i in range(1, len(objChain)):
        #     if isinstance(start,list):
        #         start=cls.deleteByMetaChain(start)
        #     if start is None:
        #         return None
        #
        #     end = objChain[i]
        #     if isinstance(end,list):
        #         end=cls.deleteByMetaChain(end)
        #
        #     start = cls.deleteByStartAndEnd(start,end)
        #     if start is None:
        #         return None
        #
        # return start

    def _physicalDelete(self, recordInMemory=True, deleteRelatedLayers=True, deleteChainedObjs=True):
        """
        [数据库操作]重写物理删除，物理删除TGraphEntity之前先把相关的关系物理删除。
        :return:
        """
        # 物理删除所有以本TGraphEntity开始和结束的TGraphEntity
        _memory = None
        if recordInMemory:
            _memory = self.MemoryCentral
        self._physicalDeleteByStart(self, memory=_memory)
        self._physicalDeleteByEnd(self, memory=_memory)

        return super(TGraphEntity, self)._physicalDelete(recordInMemory, deleteRelatedLayers, deleteChainedObjs)

    @classmethod
    def _physicalDeleteByStart(cls, start, memory=None):
        """
        根据开始对象，物理删除所有TGraphEntity
        :param start:BaseEntity及其继承类，或 Id字符串
        :return:
        """
        if start is None:
            raise Exception("无法物理删除所有TGraphEntity，start is None！")
        tgraphs = cls.getByStartInDB(start, memory=memory)
        if isinstance(tgraphs, list):
            for tgraph in tgraphs:
                tgraph._physicalDelete()
        elif isinstance(tgraphs, TGraphEntity):
            tgraphs._physicalDelete()

    @classmethod
    def _physicalDeleteByEnd(cls, end, memory=None):
        """
        根据结尾对象，物理删除所有TGraphEntity
        :param end:BaseEntity及其继承类，或 Id字符串
        :return:
        """
        if end is None:
            raise Exception("无法物理删除所有TGraphEntity，end is None！")
        tgraphs = cls.getByEndInDB(end, memory=memory)
        if isinstance(tgraphs, list):
            for tgraph in tgraphs:
                tgraph._physicalDelete()
        elif isinstance(tgraphs, TGraphEntity):
            tgraphs._physicalDelete()

    def _physicalDeleteAllBackwardsInDB(self):
        """
        物理删除以当前TGraphEntity的id为endid的所有前链（前链，即域对象、域或标签，以当前T字形结构实体类（元数据网、知识链）为结束）。
        :return:
        """
        backwards = self.getAllBackwardsInDB()
        if backwards:
            for _id, backward in backwards:
                backward._physicalDelete()

    def _physicalDeleteAllForwardsInDB(self):
        """
        物理删除以当前TGraphEntity的id为startid的所有后链。
        :return:
        """
        forwards = self.getAllForwardsInDB()
        if forwards:
            for _id, forward in forwards:
                forward._physicalDelete()

    @classmethod
    def _physicalDeleteByStartAndEnd(cls, start, end, memory=None):
        """
        根据start,end取得TGraphEntity，进行物理删除。
        :param start: MetaData/RealObject、TGraphEntity、id或是rid(BaseEntity及其继承类，或 Id字符串)
        :param end:  MetaData/RealObject、TGraphEntity、id或是rid(BaseEntity及其继承类，或 Id字符串)
        :return:
        """
        tgraph = cls.getByStartAndEnd(start, end, memory=memory)
        if tgraph:
            tgraph._physicalDelete()

    @classmethod
    def _physicalDeleteByObjChain(cls, objChain, deleteAllChain=False, memory=None):
        """
        根据realChain物理删除TGraphEntity
        :param objChain:[realData,[realData,realData]]
        :param deleteAllChain 是否删除全链
        :return:
        """
        if len(objChain) < 2:
            return
        real_nets = []
        tgraph = cls.getByObjectChain(objChain, real_nets, memory=memory)
        if deleteAllChain:
            for real_net in real_nets:
                real_net._physicalDelete()
        elif tgraph:
            if isinstance(tgraph, cls):
                tgraph._physicalDelete()
            elif isinstance(tgraph, list):
                for _obj in tgraph:
                    _obj._physicalDelete()

    @staticmethod
    def isTriStructure(tgraph):
        """
        查看T字形结构实体类（元数据网、知识链）是否符合顶级关系的三元组结构。
        :param tgraph:
        :return:
        """
        if not tgraph or not isinstance(tgraph, TGraphEntity):
            raise Exception("必须具有T字形结构实体类（元数据网、知识链），tgraph is null!")

        # 不断递归取得当前链的所有StartItem、EndItem对象（TGraphEntity、MetaData/RealObject）
        components = tgraph.getSequenceComponents()

        return len(components) == 3

    def isSame(self, objChain):
        """
        匹配现有T字形结构实体类（元数据网、知识链）与元数据/实际对象列表是否相同。
        :param objChain: 元数据/实际对象列表
        :return:
        """
        tgraph = self._createByObjChain(objChain, recordInDB=False, memory=self.MemoryCentral)
        if tgraph.id == self.id:
            return True
        return False

    def getDomains(self, lazy_get=True):
        """
        取得当前T字形结构实体类（元数据网、知识链）所有的域。例如：猪-会-说话的域可以为：西游记，小猪佩奇etc.
        :return:
        """
        return self.getByEndInDB(self, memory=self.MemoryCentral)

    def getDomained(self, lazy_get=True):
        """
        取得当前T字形结构实体类（元数据网、知识链）所有的被域。例如：猪-会-说话的域可以为：西游记，小猪佩奇etc.
        :return:
        """
        return self.getByStartInDB(self, lazy_get=lazy_get, memory=self.MemoryCentral)

    def addDomain(self, domain, understood_ratio):
        """
        给当前T字形结构实体类（元数据网、知识链）添加域（域应为T字形结构实体类（元数据网、知识链）或元数据/实际对象）。例如：猪-会-说话的域可以为：西游记，小猪佩奇etc.
        :param domain:
        :return:
        """
        if domain is None or not isinstance(domain, TGraphEntity) or not isinstance(domain, self.curItemType):
            raise Exception("参数错误，一个T字形结构实体类（元数据网、知识链）的域应为T字形结构实体类（元数据网、知识链）或元数据/实际对象！")
        # 查看是否存在
        tgraph = self.getByStartAndEnd(domain, self,
                                       memory=self.MemoryCentral)
        if tgraph:
            return tgraph
        # 不存在，创建之
        return self.createByStartEnd(domain, self,
                                     understood_ratio=understood_ratio,
                                     memory=self.MemoryCentral)

    def removeDomain(self, domain):
        """
        给当前T字形结构实体类（元数据网、知识链）删除域（域应为T字形结构实体类（元数据网、知识链）或元数据/实际对象）。例如：猪-会-说话的域可以为：西游记，小猪佩奇etc.
        :param domain:
        :return:
        """
        if domain is None or not isinstance(domain, TGraphEntity) or not isinstance(domain, self.curItemType):
            raise Exception("参数错误，一个T字形结构实体类（元数据网、知识链）的域应为T字形结构实体类（元数据网、知识链）或元数据/实际对象！")
        return self.deleteByStartAndEnd(domain, self)

    def zig_to(self, to_obj_chain):
        if not self.t_chain:
            self.getChainItems()

        return self.zig(self.t_chain, to_obj_chain)

    @staticmethod
    def zig(from_obj_chain, to_obj_chain):
        """
        根据第二个对第一个进行折叠。
        例如：将[我,知道,中国,人民,解放军] 折叠为：[[我,知道],[中国,[人民,解放军]]]
        :param from_obj_chain:
        :param to_obj_chain:
        :return:
        """
        raise NotImplementedError

    def __repr__(self):
        if len(self._t_chain_words) > 0:
            return "{TGraphEntity:{id:%s,components:%s}}" % (self.id, str(self.getSequenceComponents()))
        else:
            return "{TGraphEntity:{id:%s}}" % (self.id)
