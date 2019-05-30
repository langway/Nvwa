#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

import copy
from loongtian.util.log import logger
from loongtian.util.helper import jsonplus

from loongtian.nvwa import settings
from loongtian.nvwa.models.baseEntity import BaseEntity, LayerLimitation
from loongtian.nvwa.models.enum import ObjType
from loongtian.nvwa.models.realObject import RealObject
from loongtian.nvwa.runtime.collection import Collection

from loongtian.nvwa.runtime.relatedObjects import RelatedObj
from loongtian.nvwa.runtime.instinct import Instincts
from loongtian.nvwa.runtime.thinkResult.fragments import UnknownResult, UnknownObj
from loongtian.nvwa.runtime.meanings import Meaning,Meanings

from loongtian.nvwa.organs.character import Character

class Knowledge(BaseEntity):
    """
    线性输入的实际对象组成的链（知识链，T型单向链）。
    #  2018-12-06:再论RealObject与Knowledge关系：
    # 有两种：1、由Knowledge的所有元素通过迁移引擎生成的RealObject，知识链的所有元素之间是修限关系或是动作执行关系
    #               例如：r:中国-r:人民-r:解放军——>r:中国人民解放军。r:小明-a:打-r:小丽——>r:小明-r:手疼，r:小丽-r:哭
    #               中国人民银行不是由r:中国-r:人民-r:银行三个组件组成的，
    #                而是一个父对象-银行，名称中国人民银行，从属于中国......的实体
    #         2、从集合的角度考虑，当前知识链本身转化成的实际对象（id相同） ，是由Knowledge的所有元素构成（组件关系）的RealObject。
    #               例如：k:{r:中国-r:人民-r:解放军}——》r:x，r:x-r:父对象-r:集合,r:x-r:组件-r:中国......
    #               其中：k的id 应与 r:x的id相同
    #         这里需要注意：knowledge本身是没有构成的，必须转化生成上面第一种对象才有构成，否则只有集合的元素

    1、t_graph是一个T字型结构的由realObject、Knowledge的Id组成的数组(嵌套代表一条Knowledge)。格式为：[mid,(kid,[t_graph])]
    2、t_chain 是一个T字型结构的由realObject的Id组成的数组(嵌套代表一条Knowledge)。
    3、s_chain  是一个未经T字型结构处理的由realObject的Id组成序列数组
    4、m_chain 是一个由外域（可能是个知识链，也可能是实际对象）、知识链的kid组成的序列数组。

    eg:
    1、t_graph = [情人节,(k8,[(k7,[(k6,[小明, 给]), 小丽]), (k5,[(k1,[一, 朵]), (k4,[(k3,[红色, 的]), (k2,[玫瑰, 花]]))])])]
    2、t_chain = [情人节,[[[小明, 给], 小丽], [[一, 朵], [[红色, 的], [玫瑰, 花]]]]
    3、s_chain = [情人节,小明, 给, 小丽,一, 朵,红色, 的, 玫瑰, 花]
    4、m_chain =[情人节,mn8,mn5,mn4,mn2]

    5、下面例子中所有的汉字，均代表其实际的实际对象id
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
        2、[r1,[r2,r3],r4...rn] 以单个元素开头，以单个元素结尾，中间有单个元素、转折元素（Knowledge元素）
        3、[r1,[r2,r3],r4...[rn-1,rn]] 以单个元素开头，以转折元素（Knowledge元素）结尾，中间有单个元素、转折元素（Knowledge元素）
        4、[[r1,r2],r3,[r4,r5]...,rn]] 以转折元素（Knowledge元素）开头，以单个元素结尾，中间有单个元素、转折元素（Knowledge元素）
        5、[[r1,r2],r3,[r4,r5]...[rn-1,rn]] 以转折元素（Knowledge元素）开头，以转折元素（Knowledge元素）结尾，中间有单个元素、转折元素（Knowledge元素）
        6、[[r1,r2],[r3,r4]...[rn-1,rn]] 转折元素（Knowledge元素）顺序型。以转折元素（Knowledge元素）开头，以转折元素（Knowledge元素）结尾，中间全部都是转折元素（Knowledge元素）

    2018-12-14 知识链的组成元素的结构，应该有以下几种形式：
    0、单独r      例如：[r]
    1、r 前 r',k  例如：(1)[a,b,c]中的b，(2)[[a,b],c]中的c
    2、r 后 r',k  例如：(3)[a,b,c]中的a、b，(4)[a,[b,c]]中的a
    3、k 前 r,k'  例如：(5)[a,[b,c]]中的[b,c]，(6)[[a,b],[c,d]]中的[c,d]
    4、k 后 r,k'  例如：(7)[[a,b],c]中的[a,b]，(8)[[a,b],[c,d]]中的[a,b]
    其中：(1)=(3)，(2)=(7)，(4)=(5)，(6)=(8)，
    (0)的知识链结构：
    id   start   end
    k0     r      None
    另外，(1)和(2)在知识链中的结构是等价的，所以必须加以区分
    (1)的知识链结构：
    id   start   end
    k0     a      b
    k1     k0     c

    (2)的知识链结构：
    id   start   end
    k0     a      b
    k1     k0     List（内部定义集合的标记）
    k2     k1     c
    注：在知识链中，start不能为None，end为None的时候，表示将start只有一个元素，例如：[[a]]的集合表示为k1：
    id   start   end
    k0     a      None
    k1     k0     List（内部定义集合的标记）
    """
    __databasename__ = settings.db.db_nvwa  # 所在数据库。
    __tablename__ = settings.db.tables.tbl_knowledge # 所在表。与Flask统一
    primaryKey = copy.copy(BaseEntity.primaryKey)  # 模型对应的主键
    primaryKey.extend(["kid"])
    columns = copy.copy(BaseEntity.columns)  # 模型对应的非主键的全部字段
    columns.extend(["startid", "stype", "endid", "etype", "weight", "uratio", "type",
                    "t_graph", "t_chain", "s_chain"])
    jsonColumns = copy.copy(
        BaseEntity.jsonColumns)  # 需要用json解析的字段，一般都为text字段，创建(create)、更新(update)，需要解析为json，读取(retrive)时需要从json解析为对象
    jsonColumns.extend(["t_graph", "t_chain", "s_chain"])
    retrieveColumns = copy.copy(BaseEntity.retrieveColumns)  # 查询时需要使用的字段
    retrieveColumns.extend(["startid", "endid"])

    upperLimitation = LayerLimitation()
    upperLimitation.update({ObjType.META_NET: 1,  # m:中国-m:人民-m:解放军——>r:中国-r:人民-r:解放军
                            ObjType.REAL_OBJECT: 1,  # realobject——>pattern(knowledge) ——>meaning(knowledge)
                            # ObjType.KNOWLEDGE: 1,
                            })  # 在上一层其他对象的分层中，包含的对象类型、数量限制，
    # Knowledge 的上一层对象，为RealObject[多个]，代表当前Knowledge，Knowledge[一个]
    lowerLimitation = LayerLimitation()
    lowerLimitation.update({ObjType.REAL_OBJECT: 1,  # r:中国-r:人民-r:解放军——>r:中国人民解放军
                            ObjType.KNOWLEDGE: 1,  # pattern(knowledge) ——>meaning(knowledge)
                            ObjType.EXE_INFO: -1,  # 一个模式对应多个意义
                            })  # 在下一层其他对象的分层中，包含的对象类型、数量限制，
    # Knowledge只能有一个下层对象RealObject，多个下层对象Knowledge（一个是meaning的头，一个是pattern）
    # RealObject和Knowledge的下一层对象可以解析为：意义为、意思为、指的是、含义为、meaning等

    isChainedObject = True  # 是否是链式对象的标记（realNet、Knowledge等）

    def __init__(self, start=None, end=None, kid=None, stype=None, etype=None,
                 weight=Character.Original_Link_Weight,
                 understood_ratio=0.0,
                 type=ObjType.KNOWLEDGE,
                 t_graph=None, t_chain=None, s_chain=None,  # m_chain=None,
                 createrid='',
                 createtime=None, updatetime=None, lasttime=None,
                 status=200,# 状态; 0-不可用(逻辑删除);200-正常;800-不可遗忘
                 memory=None):
        """
        实际对象组成的网（知识链，T型单向链）。
        :param kid:元数据网ID，UUID。
        :param start:起点实际对象、知识链或RID、kid。
        :param end:终点实际对象、知识链或RID、kid。
        :param stype:起点的类型，使用ObjType枚举。
        :param etype:终点的类型，使用ObjType枚举。
        :param weight: 起点和终点链接的权重
        :param understood_ratio:understood ratio，理解的程度（0=<ratio=<1，当为1时，就是全部理解，为0时，就是完全不理解）。
        :param type: 知识链的类型，使用ObjType枚举。
        :param t_graph:是一个T字型结构的由realObject、Knowledge的Id组成的数组(嵌套代表一条Knowledge)。格式为：[mid,(kid,[t_graph])]
        :param t_chain:是一个T字型结构的由realObject的Id组成的数组(嵌套代表一条Knowledge)。
        :param s_chain:是一个未经T字型结构处理的由realObject的Id组成序列数组
        # :param m_chain 是一个由外域（可能是个知识链，也可能是实际对象）、知识链的kid组成的序列数组。
        :param createrid: 添加人; 格式：(user_id)中文名
        :param createrip: 添加人IP
        :param createtime: 添加时间;
        :param updatetime: 更新时间
        :param lasttime: 最近访问时间
        :param status: 状态; 0-不可用(逻辑删除);200-正常;800-不可遗忘
        # :param related_real: （已由layer取代）元数据网相关连的元数据Id，例如：中国 - 人民 - 解放军，关联的元数据就是“中国人民解放军”
        # :param related_knowledge: （已由layer取代）元数据网相关的知识网Id。
        # [我, 知道, 中国, 人民, 解放军, 是, 最棒, 的]
        # 相关的知识网：
        # [我, 知道, [[中国, 人民, 解放军], 是, [最棒, 的]]]
        """
        super(Knowledge, self).__init__(kid,
                                        createrid,
                                        createtime, updatetime, lasttime,
                                        status,memory=memory)

        if kid is None:
            self.kid = self.id
        else:
            self.kid = kid
            self._id = kid

        # 单一链的前、后链对象（运行时数据）
        self._start_item = None
        self._end_item = None

        if start:
            if isinstance(start, str) or isinstance(start, unicode):
                self.startid = start
            elif isinstance(start, BaseEntity):
                self.startid = start.id
                self.stype = start.getType()
                self._start_item = start
        if stype:
            if isinstance(stype, int) or isinstance(stype, str) or isinstance(stype, unicode):
                self.stype = stype
            if isinstance(start, BaseEntity):
                self.stype = start.getType()

        if end:
            if isinstance(end, str) or isinstance(end, unicode):
                self.endid = end
            elif isinstance(end, BaseEntity):
                self.endid = end.id
                self.etype = end.getType()
                self._end_item = end
        if etype:
            if isinstance(etype, int) or isinstance(etype, str) or isinstance(etype, unicode):
                self.etype = etype
            if isinstance(end, BaseEntity):
                self.etype = end.getType()

        self.weight = weight
        self.uratio = understood_ratio  # 理解率
        self.type = type

        self._isMemoryUseDoubleKeyDict = True  # 内存之中存储是否使用双键字典。
                                              # 女娲系统的metanet、knowledge、layer的内存存储、查找都使用双键字典

        # ####################################
        #      下面为运行时数据
        # ####################################

        # 关联所有集合操作的封装类。
        self.Collection = Collection(self)

        # 知识链意义操作的封装类
        self.Meanings = _Meanings(self)

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

        self._chain_items = {}  # 当前Knowledge的链包含的所有Knowledge、RealObject，格式为：{kid/mid:Knowledge/RealObject}

        # 实际取得的实际对象（RealObject）。当前知识的实际对象链
        self._t_chain_items = []
        self._s_chain_items = []

        # 实际取得的实际对象（RealObject）的remark。当前知识的字符串（remark）列表（嵌套代表一条记录）
        self._t_chain_words = []
        self._s_chain_words = []  # 当前知识链的构成元素（有顺序）

        self._native_chain = []  # 纯正知识链的组成元素id的链，请参看NativeKnowledge定义，例如：[r1:我,r2:知道,k1:[牛有腿]]，native_chain就是[r1,r2,k1]，目的是为取出知识链的集合
        self._native_chain_items = []  # 纯正知识链的组成元素实体的链，请参看NativeKnowledge定义，例如：[r1:我,r2:知道,k1:[牛有腿]]，native_chain就是[r1,r2,k1]，目的是为取出知识链的集合

        self._head = None  # 知识链的头对象
        self._tail = None  # 知识链的尾对象

        # 2018-12-06:所有上下层对象一律在Layers中处理
        # # 从数据库中取得的下一层的实际对象（只能有一个）
        # self._lower_realObject = None  # r:中国-r:人民-r:解放军——>r:中国人民解放军
        #
        # # 从数据库中取得的上一层的元数据网（只能有一个）
        # self._upper_metaNet = None  # m:中国-m:人民-m:解放军——>r:中国-r:人民-r:解放军

        # 当前知识链本身转化成的实际对象（id相同） r:中国-r:人民-r:解放军——>r:x,，r:x-r:父对象-r:集合,r:x-r:组件-r:中国......
        self._self_realObject = None

        self._is_NL_Knowledge = None  # 当前知识链是否为自然语言（奇数位是"下一个为"）的知识链
        self._NL_Knowledge = None  # 当前知识链转换成自然语言（带"下一个为"）的知识链。默认情况下，自然语言知识链只在'思考'时使用。

        Instincts.loadAllInstincts(memory=self.MemoryCentral)
        # if __debug__:
        #     from loongtian.util.db.sequence import Sequence
        #     self.kid = "R%030d" % Sequence.nextKnowledge()
        #     self.isdel = True

    def getStartItem(self):
        """
        根据startid取得开始的对象（可能是realObject，也可能是Knowledge）
        :return:
        """
        if self.startid is None:
            return None
        if self._start_item:
            return self._start_item
        # 根据前链的类型取得对应的对象（包括：RealObject、Knowledge）
        if ObjType.isRealObject(self.stype):
            self._start_item = RealObject.getOne(memory=self.MemoryCentral, rid=self.startid)
        elif ObjType.isKnowledge(self.stype):
            self._start_item = Knowledge.getOne(memory=self.MemoryCentral, kid=self.startid)
        else:
            raise Exception("知识链开始对象类型错误：{%d:%s}。" % (self.stype, ObjType.getTypeNames(self.stype)))

        if not self._start_item:
            raise Exception(
                "未能取得知识链开始对象：{%s:%s,%d:%s}。" % ("Id", self.startid, self.stype, ObjType.getTypeNames(self.stype)))
        return self._start_item

    def getEndItem(self):
        """
        根据endid取得结束的对象（可能是realObject，也可能是Knowledge）
        :return:
        """
        if self.endid is None:
            return None
        if self._end_item:
            return self._end_item
        # 根据后链的类型取得对应的对象（包括：RealObject、Knowledge）
        if ObjType.isRealObject(self.etype):
            self._end_item = RealObject.getOne(memory=self.MemoryCentral, rid=self.endid)
        elif ObjType.isKnowledge(self.etype):
            self._end_item = Knowledge.getOne(memory=self.MemoryCentral, kid=self.endid)
        else:
            raise Exception("知识链结束对象类型错误：{%d:%s}。" % (self.etype, ObjType.getTypeNames(self.etype)))

        if not self._end_item:
            raise Exception(
                "未能取得知识链结束对象：{%s:%s,%d:%s}。" % ("Id", self.endid, self.etype, ObjType.getTypeNames(self.etype)))
        return self._end_item

    @staticmethod
    def createKnowledgeByStartEnd(start, end, type=ObjType.KNOWLEDGE,
                                  understood_ratio=Character.Original_Link_Weight,
                                  recordInDB=True,
                                  memory=None):
        """
        创建KnowledgeItem（允许end为None）
        :param start:可以是RealObject、KnowledgeItem或[sid,stype]\(sid,stype)
        :param end:可以是RealObject、KnowledgeItem或[eid,etype]\(eid,etype)
        :return:
        """
        # 确保第一个不是list标识符
        Instincts.loadAllInstincts(memory=memory)
        if start.id == Instincts.instinct_original_list.id:
            raise Exception("知识链的第一个start对象不应是内部集合标记（k1 k0 #List#，将k0包裹在集合中）！")
        elif isinstance(start, RealObject):
            sid = start.rid
            stype = ObjType.REAL_OBJECT
        elif isinstance(start, Knowledge):
            sid = start.kid
            stype = ObjType.KNOWLEDGE
        elif isinstance(start, list) or isinstance(start, tuple):
            sid = start[0]
            stype = start[1]
        else:
            raise Exception("start对象应为RealObject或KnowledgeItem或[sid,stype]\(sid,stype)，当前类型错误：%s" % type(start))

        if isinstance(end, RealObject):
            eid = end.rid
            etype = ObjType.REAL_OBJECT
        elif isinstance(end, Knowledge):
            eid = end.kid
            etype = ObjType.KNOWLEDGE
        elif isinstance(end, list) or isinstance(end, tuple):
            eid = end[0]
            etype = end[1]
        elif end is None:
            end = Instincts.instinct_none
            eid = end.rid
            etype = ObjType.REAL_OBJECT
        else:
            raise Exception("end对象应为RealObject或KnowledgeItem或[sid,stype]\(sid,stype)，当前类型错误：" + type(start))

        klg = Knowledge(start=sid, stype=stype, end=eid, etype=etype,
                        understood_ratio=understood_ratio, type=type,
                        memory=memory)
        exists_klg = klg.getExist()
        if exists_klg:
            klg=exists_klg
        if isinstance(start, BaseEntity):
            klg._start_item = start
        else:
            klg._start_item = klg.getStartItem()
        if isinstance(end, BaseEntity):
            klg._end_item = end
        else:
            klg._end_item = klg.getEndItem()
        klg.getChainItems()

        # 真正创建（内存、数据库）
        if not klg._isInDB: # and recordInDB:
            klg=klg.create(checkExist=False,recordInDB=recordInDB)

        if klg:
            klg.getChainItems()
        return klg

    @staticmethod
    def createKnowledgeByObjChain(obj_chain,
                                  type=ObjType.KNOWLEDGE,
                                  obj_nets=None,
                                  understood_ratio=0.0,
                                  recordInDB=True,
                                  recordRelationInFirstReal=False,
                                  memory=None):
        """
        根据实际对象或知识链序列创建Knowledge（完全匹配，顺序相同）
        :param obj_chain:[RealObject/Knowledge,[RealObject/Knowledge]]
        :param obj_nets: 最后形成knowledge的子knowledge，例如：k0:[k1:[a,b],k2:[c,d],e],k0的obj_nets就是[k1,k2,e]
        :param type:
        :param understood_ratio:
        :param recordInDB: 是否记录到数据库
        :param recordRelationInFirstReal: 是否将知识链作为关系记录到第一个实际对象，例如：牛-组件-腿，就将组件-腿的关系记录到牛这个对象中
        :return:
        """
        Instincts.loadAllInstincts(memory=memory)
        # 集合对象不能为None
        if obj_chain is None or (not isinstance(obj_chain, list) and not isinstance(obj_chain, tuple)):
            return None
        if len(obj_chain) == 0:
            return None

        # 只有一个对象的知识链，例如：[r/k]或[[r1/k1...rn/kn]]
        if len(obj_chain) == 1:  # 这里考虑只有一个对象的集合，例如[牛]，将其转换成knowledge(End为None)
            if isinstance(obj_chain[0], list) or isinstance(obj_chain[0], tuple):
                child_knowledge = Knowledge.createKnowledgeByObjChain(obj_chain[0], type, obj_nets, understood_ratio,
                                                                      recordInDB,
                                                                      recordRelationInFirstReal,
                                                                      memory=memory)
                return Knowledge.createKnowledgeByObjChain([child_knowledge,
                                                            Instincts.instinct_original_list], type,
                                                            obj_nets, understood_ratio,
                                                            recordInDB,
                                                            recordRelationInFirstReal,
                                                           memory=memory)

            else:
                if obj_chain[0].id == Instincts.instinct_original_list:  # 开始对象不能为List
                    return None
                # 这里考虑只有一个对象的集合，例如[牛]，将其转换成knowledge(End为List)
                return Knowledge.createKnowledgeByObjChain([obj_chain[0],
                                                            Instincts.instinct_original_list],
                                                           type,obj_nets, understood_ratio,
                                                           recordInDB,recordRelationInFirstReal,
                                                           memory=memory)

        cur_klg = None
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
                    if isinstance(unknown_objs[0].unknown_obj, Knowledge):
                        knowledges.append(unknown_objs[0].unknown_obj)

                cur_obj = Knowledge.createKnowledgeByObjChain(knowledges,
                                                              type, obj_nets,
                                                              understood_ratio,
                                                              recordInDB,
                                                              recordRelationInFirstReal,
                                                              memory=memory)
            if isinstance(cur_obj, UnknownObj):
                cur_obj = cur_obj.unknown_obj
            if isinstance(cur_obj, list):  # 如果当前real是list，创建其子KnowledgeItem
                if len(cur_obj) > 0:
                    cur_obj = Knowledge.createKnowledgeByObjChain(cur_obj,
                                                                  type, obj_nets,
                                                                  understood_ratio,
                                                                  recordInDB,
                                                                  recordRelationInFirstReal,
                                                                  memory=memory)
                else:  # 略掉空集合
                    i += 1
                    continue

            # 1、如果前面有了链，往后拼接
            if cur_klg:
                # 这里需要对[[a,b],c]这样的知识链进行特殊处理：后面加List
                if isinstance(last_obj, list):
                    # 这里面需要对[[a,b],c]这样的知识链进行特殊处理：后面加List
                    cur_obj = Knowledge.createKnowledgeByStartEnd(cur_obj,
                                                                  Instincts.instinct_original_list,
                                                                  memory=memory)

                cur_klg = Knowledge.createKnowledgeByStartEnd(cur_klg, cur_obj, type,
                                                              understood_ratio=understood_ratio,
                                                              recordInDB=recordInDB,
                                                              memory=memory)
                obj_nets.append(cur_klg)
                last_obj = cur_obj
                i += 1
                continue

            # 2、这里应该是第一组了，取下一个，然后创建知识链
            next_obj = None
            if i < len(obj_chain) - 1:  # # 确保后面至少有第二个
                next_obj = obj_chain[i + 1]
                if next_obj is None:  # 替换None为instinct_none
                    next_obj = Instincts.instinct_none

                if isinstance(original_cur_obj, list):
                    # 这里面需要对[[a,b],c]这样的知识链进行特殊处理：后面加List
                    cur_obj = Knowledge.createKnowledgeByStartEnd(cur_obj,
                                                                  Instincts.instinct_original_list,
                                                                  memory=memory)

                if isinstance(next_obj, RelatedObj):
                    next_obj = next_obj.obj
                if isinstance(next_obj, list):  # 如果下一real是list，创建其子KnowledgeItem
                    if len(next_obj) > 0:
                        next_obj = Knowledge.createKnowledgeByObjChain(next_obj,
                                                                       type, obj_nets,
                                                                       understood_ratio,
                                                                       recordInDB=recordInDB,
                                                                       recordRelationInFirstReal=recordRelationInFirstReal,
                                                                       memory=memory)
                        # # 这里面需要对[a,[b,c]]这样的知识链进行特殊处理：后面加List
                        # next_obj = Knowledge.createKnowledgeByStartEnd(next_obj, _Instincts.instinct_original_list)

                    else:
                        i += 1
                        continue

            if next_obj:
                cur_klg = Knowledge.createKnowledgeByStartEnd(cur_obj, next_obj, type,
                                                              understood_ratio=understood_ratio,
                                                              recordInDB=recordInDB,
                                                              memory=memory)
                obj_nets.append(cur_klg)
                i += 2
            else:  # 如果是最后一个
                return cur_obj

        if cur_klg:
            cur_klg.getChainItems()
            if recordRelationInFirstReal and len(obj_chain)==3:
                first_real = obj_chain[0]
                relation = obj_chain[1]
                related_obj = obj_chain[2]
                if first_real and isinstance(first_real,RealObject):
                    first_real.Constitutions.addRelatedObject(relation,related_obj)


        return cur_klg

    @staticmethod
    def recordInDB(know,memory=None):
        """
        将一个知识链记录到数据库中
        :param know:
        :return:
        """
        # if know._isInDB:  # 如果已经在数据库中了，略过
        #     return
        components = know.getSequenceComponents()
        Knowledge.createKnowledgeByObjChain(components, recordInDB=True, memory=memory)

    def createUpperRealObject(self, remark=None, realType=ObjType.REAL_OBJECT):
        """
        创建代表当前Knowledge的实际对象
        :return:
        """
        self.getChainItems()
        if remark is None:
            remark = self._s_chain_words
        new_real = RealObject(remark=remark, realType=realType,
                              memory=self.MemoryCentral).create()
        self.Layers.addUpper(new_real)
        new_real.Layers.addLower(self, recordInDB=False)  # 已经添加过了
        return new_real

    @staticmethod
    def getKnowledgeByObjectChain(obj_chain, obj_nets=None, unproceed=None,memory=None):
        """
        根据实际对象或知识链序列取得Knowledge（注意：这里可能是不完全匹配，顺序相同）
        :param obj_chain:[real,[real,real]]
        :param obj_nets:
        :param unproceed: 外部传入的list，记录未处理的对象
        :return:
        """
        if len(obj_chain) < 2:
            return None
        cur_klg = None
        if obj_nets is None:
            obj_nets = []

        if unproceed is None:
            unproceed = []

        i = 0
        while i < len(obj_chain):  # 确保后面至少有一条
            cur_obj = obj_chain[i]  # 第一个
            if isinstance(cur_obj, list):
                if len(cur_obj) > 0:  # 如果当前real是list，查询其子KnowledgeItem
                    cur_obj = Knowledge.getKnowledgeByObjectChain(cur_obj, obj_nets, unproceed,
                                                                  memory=memory)
                    if not cur_obj:  # 破解查询结构不一致
                        cur_obj = obj_chain[i][0]
            # 如果能够与前链“构成”，继续下一个
            if cur_klg:
                cur_temp_klg = Knowledge.getKnowledgeByStartAndEnd(cur_klg, cur_obj,
                                                                   memory=memory)
                if cur_temp_klg:
                    cur_klg = cur_temp_klg
                    obj_nets.append(cur_klg)
                    i += 1
                    continue
            # 不能与前链“构成”，查看与后一个元素是否能够“构成”
            next_real = None
            if i < len(obj_chain) - 1:  # # 确保后面至少有第二个
                next_real = obj_chain[i + 1]
                if isinstance(next_real, list):  # 如果下一real是list，查询其子KnowledgeItem
                    next_real = Knowledge.getKnowledgeByObjectChain(next_real, obj_nets, unproceed,memory=memory)
            if next_real:
                cur_temp_klg = Knowledge.getKnowledgeByStartAndEnd(cur_obj, next_real,
                                                                   memory=memory)
                if cur_temp_klg:
                    test_klg = None
                    if len(obj_chain) == 2:  # 如果没有前一个元素、后一个元素，说明是唯一的两个
                        test_klg = cur_temp_klg
                    if not test_klg and cur_klg:
                        # 这里需要考虑与cur_klg、前元素、后元素是否能够构成一条链，如果不构成，也要抛弃
                        test_klg = Knowledge.getKnowledgeByStartAndEnd(cur_klg,
                                                                       cur_temp_klg,
                                                                       memory=memory)
                    if not test_klg and i - 1 >= 0:
                        last_real = obj_chain[i - 1]  # 前一个元素
                        if last_real:
                            if isinstance(last_real, list):
                                test_klg = Knowledge.getKnowledgeByObjectChain([last_real, cur_temp_klg],
                                                                               obj_nets,
                                                                               unproceed,
                                                                               memory=memory)
                            else:
                                test_klg = Knowledge.getKnowledgeByStartAndEnd(last_real,
                                                                               cur_temp_klg,
                                                                               memory=memory)
                    if not test_klg and i < len(obj_chain) - 2:
                        next_next_real = obj_chain[i + 2]  # 后一个元素
                        if next_next_real:
                            if isinstance(next_next_real, list):
                                test_klg = Knowledge.getKnowledgeByObjectChain([cur_temp_klg, next_next_real],
                                                                               obj_nets,
                                                                               unproceed,
                                                                               memory=memory)
                            else:
                                test_klg = Knowledge.getKnowledgeByStartAndEnd(cur_temp_klg,
                                                                               next_next_real,
                                                                               memory=memory)

                    if not test_klg:  # 仍未找到，当前cur_temp_klg没有与前后产生构成，暂时放到待处理列表
                        unproceed.insert(0, cur_temp_klg)
                        i += 2
                        continue

                    # 如果不是最后一个，把cur_temp_klg赋值给cur_klg
                    # 反之，如果是最后一个，把cur_temp_klg与cur_klg粘连
                    if cur_klg:
                        cur_last_klg = Knowledge.getKnowledgeByStartAndEnd(cur_klg,
                                                                           cur_temp_klg,
                                                                           memory=memory)
                        if cur_last_klg:
                            cur_klg = cur_last_klg
                        else:
                            cur_klg = cur_temp_klg
                    else:
                        cur_klg = cur_temp_klg

                    # 如果前面有未连成链的，往前附着，连成链
                    cur_unproceed_klg = None
                    if len(unproceed) > 0:  # 如果前面有未连成链的，往前附着，连成链
                        cur_unproceed_klg = cur_klg
                        proceed = []
                        for j in range(len(unproceed)):  # 因为是线性输入，所以进行倒序处理
                            try:
                                cur_unproceed_klg = Knowledge.getKnowledgeByStartAndEnd(unproceed[j],
                                                                                        cur_unproceed_klg,
                                                                                        memory=memory)
                                if cur_unproceed_klg:
                                    # 继续往前粘连
                                    last_unproceed_klg = cur_unproceed_klg
                                    last_unproceed_klgs = []
                                    for real_net in obj_nets:
                                        last_unproceed_klg = Knowledge.getKnowledgeByStartAndEnd(real_net,
                                                                                                 last_unproceed_klg,
                                                                                                 memory=memory)
                                        if last_unproceed_klg:
                                            last_unproceed_klgs.append(last_unproceed_klg)

                                    obj_nets.append(cur_unproceed_klg)
                                    if len(last_unproceed_klgs) > 0:
                                        obj_nets.extend(last_unproceed_klgs)
                                        cur_unproceed_klg = last_unproceed_klgs[-1]

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

                    obj_nets.append(cur_klg)
                    i += 2
                    if cur_unproceed_klg:
                        cur_klg = cur_unproceed_klg
                        i += 2
                        # real_nets.append(cur_klg)
                else:  # 仍未找到，当前cur_real没有与前后产生构成，暂时放到待处理列表
                    unproceed.insert(0, cur_obj)
                    i += 1
            else:
                i += 1

        return cur_klg

    @staticmethod
    def getKnowledgeLikeObjChain(objChain,memory=None):
        """
        根据realChain取得Knowledge（不完全匹配，使用s_chain进行近似匹配，根据匹配数量、匹配对象的weight进行排序）
        :param objChain:[realData,[realData,realData]]
        :return:
        """
        # todo 目前还是使用全文匹配，未来应该使用近似匹配
        idChain, is_sequence = Knowledge.getIdChainByObjChain(objChain)
        like = jsonplus.dumps(idChain)
        if is_sequence:
            klg = Knowledge.getAllLikeByInDB(s_chain=like,memory=memory)
        else:
            klg = Knowledge.getAllLikeByInDB(t_chain=like,memory=memory)

        if klg:
            klg.getChainItems()
        return klg

    def getAllLikeByHeadAndTailInDB(self, attribute):
        """
        取得所有以头部对象开始，以尾部对象结尾的知识链，例如：给定苹果、红，查找出知识链苹果-颜色-红。
        :param attribute:
        :return:
        """
        self.getChainItems()
        if self._head is None:
            raise Exception("必须提供头部对象以便查找！")
        if self._tail is None:
            raise Exception("必须提供尾部对象以便查找！")

        return self.getAllLikeByStartMiddleEndInDB(attribute, "[" + self._head.id, self._tail.id + "]")

    @staticmethod
    def getKnowledgeByObjs(objs,memory=None):
        """
        根据散列化的实际对象或知识链取得Knowledge（顺序不一定相同）
        :param realChain:[realData,[realData,realData]]
        :return:
        """
        if len(objs) < 2:
            return None
        # 取得第一条记录，并根据上下条记录关系，并取得最终排序的结果
        cur_klg = None  # 第一条记录

        found_first = False
        for i in range(len(objs)):
            cur_related_klg = objs[i]
            cur_klg = Knowledge.getKnowledgesByStartInDB(cur_related_klg,memory=memory)
            if cur_klg:  # 找到了，停止
                if isinstance(cur_klg, list):  # 如果有很多个，找到related_ks中的一个知识链为结尾的
                    for _next_klg in cur_klg:
                        _next_klg.getChainItems()
                        if _next_klg._end_item in objs:
                            found_first = True
                            cur_klg = _next_klg
                            break
                elif isinstance(cur_klg, Knowledge):
                    cur_klg.getChainItems()
                    if cur_klg._end_item in objs:
                        found_first = True
                        break
            if found_first:
                break

        if not found_first:  # 没有找到第一个节点，应该是一个没有顺序的集合，直接返回现有列表
            return None

        while True:  # 递归查找下一个节点
            found_next = False
            next_klg = Knowledge.getKnowledgesByStartInDB(cur_klg,memory=memory)
            if not next_klg:  # 如果没找到，说明后面没有节点了
                break

            if isinstance(next_klg, list):
                for _next_klg in next_klg:
                    _next_klg.getChainItems()
                    if _next_klg._end_item in objs:
                        cur_klg = _next_klg
                        found_next = True
                        break
            elif isinstance(next_klg, Knowledge):
                next_klg.getChainItems()
                if next_klg._end_item in objs:
                    cur_klg = next_klg
                    found_next = True

            if not found_next:
                break

        # 检查两者是否相等（长度）
        cur_klg.getChainItems()
        if len(cur_klg._s_chain_items) != len(objs):
            cur_klg = None

        return cur_klg

    @staticmethod
    def getIdChainByObjChain(objChain):
        """
        取得realobject、meta_net_matched_knowledges Chain的id列表
        :param objChain:
        :return:
        """
        id_chain = []
        is_sequence = True
        for obj in objChain:
            if isinstance(obj, list):
                id_chain.append(Knowledge.getIdChainByObjChain(obj))
                is_sequence = False
            elif isinstance(obj, RealObject):
                id_chain.append(obj.rid)
            elif isinstance(obj, Knowledge):
                id_chain.append(obj.kid)

        return id_chain, is_sequence

    def getChainItems(self, keepEndKnowledge=False):
        """
        不断递归取得当前链的所有StartItem、EndItem对象（Knowledge、RealObject）
        :param keepEndKnowledge: 如果 end以Knowledge结尾，是否将endItem的Knowledge保留，如果不保留，意味着嵌套集合列表，例如：牛-有-腿-Knowledge(我-知道)，还原为：[[牛,有,腿],[我-知道]],否则将添加Knowledge
        :return:
        """
        # 递归取得元素
        # 例如：
        #         s     e
        # k0      1     2
        # k1      3     k0
        # k2      k1    4
        # 最终要取得：[3,[1,2],4]

        # if self._chainItemsProceed == True:
        #     return

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

        self._native_chain = []  # 纯正知识链的组成元素id的链，请参看NativeKnowledge定义，例如：[r1:我,r2:知道,k1:[牛有腿]]，native_chain就是[r1,r2,k1]
        self._native_chain_items = []  # 纯正知识链的组成元素实体的链，，请参看NativeKnowledge定义，例如：[r1:我,r2:知道,k1:[牛有腿]]，native_chain就是[r1,r2,k1]

        self._t_chain_words = []
        self._s_chain_words = []

        self._sequence_components = []
        self._sequence_component_ids = []
        self._sequence_components_words = []

        # 处理头部
        if isinstance(self._start_item, Knowledge):
            self._chain_items[self._start_item.kid] = self._start_item
            self._start_item.getChainItems()  # ,original=original)
            if self._start_item._head:  # 取得链的头（是一个KnowledgeItem）
                self._head = self._start_item._head

            start_components = self._start_item._sequence_components
            start_component_ids = self._start_item._sequence_component_ids
            # 处理尾部
            if isinstance(self._end_item, Knowledge):  # Knowledge-Knowledge
                self._chain_items[self._end_item.kid] = self._end_item

                self._end_item.getChainItems()
                if self._end_item._tail:  # 取得链的尾（是一个KnowledgeItem）
                    self._tail = self._end_item._tail

                # 处理t_graph、s_chain、t_chain、_word_chain等
                # 在前逐元素插入
                self.s_chain = self._start_item.s_chain + self.s_chain + self._end_item.s_chain
                self.t_graph.insert(0, (self.kid, [self._start_item.t_graph, self._end_item.t_graph]))
                self.t_chain.insert(0, [self._start_item.t_chain, self._end_item.t_chain])

                # 实际取得的实际对象（RealObject）
                self._t_chain_items.insert(0, [self._start_item._t_chain_items, self._end_item._t_chain_items])
                self._s_chain_items = self._start_item._s_chain_items + self._s_chain_items + self._end_item._s_chain_items

                # 实际取得的实际对象（RealObject）的remark
                self._t_chain_words.insert(0, [self._start_item._t_chain_words, self._end_item._t_chain_words])
                self._s_chain_words = self._start_item._s_chain_words + self._s_chain_words + self._end_item._s_chain_words

                if self._start_item.isNativeKnowledge():
                    self._native_chain.insert(0, self._start_item.id)
                    if self._end_item.isNativeKnowledge():
                        self._native_chain.insert(1, self._end_item.id)
                    else:
                        self._native_chain.insert(1, self._end_item.id)

                if keepEndKnowledge:
                    self._sequence_components.extend(start_components)
                    self._sequence_components.append(self._end_item)

                    self._sequence_component_ids.extend(start_component_ids)
                    self._sequence_component_ids.append(self._end_item.id)
                else:
                    end_components = self._end_item.getSequenceComponents(keepEndKnowledge)
                    self._sequence_components.extend(start_components)
                    self._sequence_components.append(end_components)

                    end_component_ids = self._end_item._sequence_component_ids
                    self._sequence_component_ids.extend(start_component_ids)
                    self._sequence_component_ids.append(end_component_ids)

            elif isinstance(self._end_item, RealObject):  # Knowledge-RealObject
                self._chain_items[self._end_item.rid] = self._end_item
                _end_is_real = True

                # 处理t_graph、s_chain、t_chain、_word_chain等
                # 在前逐元素插入
                self.s_chain.extend(self._start_item.s_chain)
                self.s_chain.append(self._end_item.rid)
                self.t_graph.insert(0, (self.kid, [self._start_item.t_graph, self._end_item.rid]))
                self.t_chain.insert(0, [self._start_item.t_chain, self._end_item.rid])

                # 实际取得的实际对象（RealObject）
                self._t_chain_items.insert(0, [self._start_item._t_chain_items, self._end_item])
                self._s_chain_items.extend(self._start_item._s_chain_items)
                self._s_chain_items.append(self._end_item)

                # 实际取得的实际对象（RealObject）的remark
                self._t_chain_words.insert(0, [self._start_item._t_chain_words, self._end_item.Remark])
                self._s_chain_words.extend(self._start_item._s_chain_words)
                self._s_chain_words.append(self._end_item.Remark)

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
                raise Exception("知识链的结尾应为实际对象或知识链！")
        elif isinstance(self._start_item, RealObject):
            self._chain_items[self._start_item.rid] = self._start_item
            _start_is_real = True

            # 处理尾部
            if isinstance(self._end_item, Knowledge):  # RealObject-Knowledge
                self._chain_items[self._end_item.kid] = self._end_item

                self._end_item.getChainItems()  # ,original=original)
                if self._end_item._tail:  # 取得链的尾（是一个KnowledgeItem）
                    self._tail = self._end_item._tail

                # 处理t_graph、s_chain、t_chain、_word_chain等
                # 在前逐元素插入
                self.s_chain.append(self._start_item.rid)
                self.s_chain += self._end_item.s_chain
                self.t_graph.insert(0, (self.kid, [self._start_item.rid, self._end_item.t_graph]))
                self.t_chain.insert(0, [self._start_item.rid, self._end_item.t_chain])

                # 实际取得的实际对象（RealObject）
                self._s_chain_items.append(self._start_item)
                self._s_chain_items += self._end_item._s_chain_items
                self._t_chain_items.insert(0, [self._start_item, self._end_item._t_chain_items])

                # 实际取得的实际对象（RealObject）的remark
                self._s_chain_words.append(self._start_item.Remark)
                self._s_chain_words += self._end_item._s_chain_words
                self._t_chain_words.insert(0, [self._start_item.Remark, self._end_item._t_chain_words])

                self._sequence_components.append(self._start_item)
                self._sequence_component_ids.append(self._start_item.id)
                if keepEndKnowledge:
                    self._sequence_components.append(self._end_item)
                    self._sequence_component_ids.append(self._end_item.id)
                else:
                    end_components = self._end_item.getSequenceComponents(keepEndKnowledge)
                    self._sequence_components.append(end_components)

                    end_component_ids = self._end_item._sequence_component_ids
                    self._sequence_component_ids.append(end_component_ids)

            elif isinstance(self._end_item, RealObject):  # RealObject-RealObject
                self._chain_items[self._end_item.rid] = self._end_item
                _end_is_real = True

                # 处理t_graph、s_chain、t_chain、_word_chain等
                # 在前逐元素插入
                self.s_chain.extend([self._start_item.rid, self._end_item.rid])
                self.t_graph.extend([(self.kid, [self._start_item.rid, self._end_item.rid])])
                self.t_chain.extend([self._start_item.rid, self._end_item.rid])
                # self.m_chain.extend([self.kid])

                # 实际取得的实际对象（RealObject）
                self._s_chain_items.extend([self._start_item, self._end_item])
                self._t_chain_items.extend([self._start_item, self._end_item])

                # 实际取得的实际对象（RealObject）的remark
                self._s_chain_words.extend([self._start_item.Remark, self._end_item.Remark])
                self._t_chain_words.extend([self._start_item.Remark, self._end_item.Remark])

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
            raise Exception("知识链的开始应为实际对象或知识链！")

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

        # 标记已经取得了chain
        self._chainItemsProceed = True

    def getSequenceComponents(self, keepEndKnowledge=False):
        """
        取得一个知识链的构成元素（有顺序）
        :param keepEndKnowledge: 如果 end以Knowledge结尾，是否将endItem的Knowledge保留，如果不保留，意味着嵌套集合列表，例如：牛-有-腿-Knowledge(我-知道)，还原为：[[牛,有,腿],[我-知道]],否则将添加Knowledge
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
        self.getChainItems()
        return self._sequence_components

    def isNativeKnowledge(self):
        """
        是否都是由realobject构成的知识链。例如：r:牛-r:有-r:腿
        :return:
        """
        components = self.getSequenceComponents()
        for component in components:
            if not isinstance(component, RealObject):
                return False

        return True


    def getAllForwardsInMemory(self, depth=Character.Search.Knowledge_Forwards_Depth, lazy_get=True):
        """
        取得以当前KnowledgeItem的kid为startid的所有后链（后链，即被域对象，以当前知识链为开始）。
        :param lazy_get 是否等需要的时候再取得对应的对象（以getChainItems填充）
        :param depth: 查找知识链的层深，-1表示不限层深。数值越大，查找到的知识链越多，但需要处理的也越多，系统耗时越长
        :return: 后链列表[Knowledge]
        """
        if len(self._forwards) > 0:
            return self._forwards
        forwards_klgs = []
        Knowledge._getAllForwardsInMemory(self, forwards_klgs, depth, lazy_get, memory=self.MemoryCentral)
        if forwards_klgs:
            if isinstance(forwards_klgs, list):
                for klg in forwards_klgs:
                    self._forwards[klg.kid] = klg
            elif isinstance(forwards_klgs, Knowledge):
                self._forwards[forwards_klgs.kid] = forwards_klgs

        return self._forwards

    @staticmethod
    def _getAllForwardsInMemory(klg, forwards_klgs,
                                depth=Character.Search.Knowledge_Forwards_Depth,
                                lazy_get=True,
                                memory=None):
        """
        [递归]取得以当前KnowledgeItem的kid为startid的所有后链（后链，即被域对象，以当前知识链为开始）。
        :param lazy_get 是否等需要的时候再取得对应的对象（以getChainItems填充）
        :param depth: 查找知识链的层深，-1表示不限层深。数值越大，查找到的知识链越多，但需要处理的也越多，系统耗时越长
        :return: 后链列表[Knowledge]
        """
        klgs = Knowledge.getKnowledgesByStartInMemory(klg, lazy_get,memory=memory)
        if klgs:
            if isinstance(klgs, list):
                forwards_klgs.extend(klgs)
                if depth > 0 or depth < 0:  # 只要是0，就停机
                    for klg in klgs:
                        # 继续取得以klg为开头的知识链
                        Knowledge._getAllForwardsInMemory(klg, forwards_klgs, depth - 1, lazy_get,
                                                          memory=memory)
            elif isinstance(klgs, Knowledge):
                forwards_klgs.append(klgs)
                if depth > 0 or depth < 0:  # 只要是0，就停机
                    # 继续取得以klg为开头的知识链
                    Knowledge._getAllForwardsInMemory(klgs, forwards_klgs, depth - 1, lazy_get,
                                                      memory=memory)


    def getAllForwardsInDB(self,
                           depth=Character.Search.Knowledge_Forwards_Depth,
                           lazy_get=True):
        """
        取得以当前KnowledgeItem的kid为startid的所有后链（后链，即被域对象，以当前知识链为开始）。
        :param lazy_get 是否等需要的时候再取得对应的对象（以getChainItems填充）
        :param depth: 查找知识链的层深，-1表示不限层深。数值越大，查找到的知识链越多，但需要处理的也越多，系统耗时越长
        :return: 后链列表[Knowledge]
        """
        if len(self._forwards) > 0:
            return self._forwards
        forwards_klgs = []
        Knowledge._getAllForwardsInDB(self,
                                      forwards_klgs, depth, lazy_get,
                                      memory=self.MemoryCentral)
        if forwards_klgs:
            if isinstance(forwards_klgs, list):
                for klg in forwards_klgs:
                    self._forwards[klg.kid] = klg
            elif isinstance(forwards_klgs, Knowledge):
                self._forwards[forwards_klgs.kid] = forwards_klgs

        return self._forwards

    @staticmethod
    def _getAllForwardsInDB(klg, forwards_klgs,
                            depth=Character.Search.Knowledge_Forwards_Depth,
                            lazy_get=True,
                            memory=None):
        """
        [递归]取得以当前KnowledgeItem的kid为startid的所有后链（后链，即被域对象，以当前知识链为开始）。
        :param lazy_get 是否等需要的时候再取得对应的对象（以getChainItems填充）
        :param depth: 查找知识链的层深，-1表示不限层深。数值越大，查找到的知识链越多，但需要处理的也越多，系统耗时越长
        :return: 后链列表[Knowledge]
        """
        klgs = Knowledge.getKnowledgesByStartInDB(klg, lazy_get,memory=memory)
        if klgs:
            if isinstance(klgs, list):
                forwards_klgs.extend(klgs)
                if depth > 0 or depth < 0:  # 只要是0，就停机
                    for klg in klgs:
                        # 继续取得以klg为开头的知识链
                        Knowledge._getAllForwardsInDB(klg, forwards_klgs, depth - 1, lazy_get,
                                                      memory=memory)
            elif isinstance(klgs, Knowledge):
                forwards_klgs.append(klgs)
                if depth > 0 or depth < 0:  # 只要是0，就停机
                    # 继续取得以klg为开头的知识链
                    Knowledge._getAllForwardsInDB(klgs, forwards_klgs, depth - 1, lazy_get,
                                                  memory=memory)

    def getAllBackwardsInDB(self, depth=Character.Search.Knowledge_Backwards_Depth, lazy_get=True):
        """
        取得以当前KnowledgeItem的kid为endid的所有前链（前链，即域对象、域或标签，以当前知识链为结束）。
        eg:
            self = [猪能说话]
            return [[西游记], [中国[上古[史诗神话]]], [猪八戒], [小猪佩奇]...]
        :param lazy_get 是否等需要的时候再取得对应的对象（以getChainItems填充）
        :param depth: 查找知识链的层深，-1表示不限层深。数值越大，查找到的知识链越多，但需要处理的也越多，系统耗时越长
        :return: 前链列表[Knowledge]
        """
        if len(self._backwards) > 0:
            return self._backwards
        backwards_klgs = []
        Knowledge._getAllBackwardsInDB(self, backwards_klgs, depth, lazy_get, memory=self.MemoryCentral)
        if backwards_klgs:
            if isinstance(backwards_klgs, list):
                for klg in backwards_klgs:
                    self._backwards[klg.kid] = klg
            elif isinstance(backwards_klgs, Knowledge):
                self._backwards[backwards_klgs.kid] = backwards_klgs

        return self._backwards

    @staticmethod
    def _getAllBackwardsInDB(klg, backwards_klgs,
                             depth=Character.Search.Knowledge_Backwards_Depth,
                             lazy_get=True,
                             memory=None):
        """
        [递归]取得以当前KnowledgeItem的kid为endid的所有前链（前链，即域对象、域或标签，以当前知识链为结束）。
        eg:
            self = [猪能说话]
            return [[西游记], [中国[上古[史诗神话]]], [猪八戒], [小猪佩奇]...]
        :param lazy_get: 是否等需要的时候再取得对应的对象（以getChainItems填充）
        :param depth: 查找知识链的层深，-1表示不限层深。数值越大，查找到的知识链越多，但需要处理的也越多，系统耗时越长
        :return: 前链列表[Knowledge]
        """
        klgs = Knowledge.getKnowledgesByStartInDB(klg, lazy_get,memory=memory)
        if klgs:
            if isinstance(klgs, list):
                backwards_klgs.extend(klgs)
                if depth > 0 or depth < 0:  # 只要是0，就停机
                    for klg in klgs:
                        # 继续取得以klg为开头的知识链
                        Knowledge._getAllBackwardsInDB(klg, backwards_klgs, depth - 1, lazy_get,
                                                       memory=memory)
            elif isinstance(klgs, Knowledge):
                backwards_klgs.append(klgs)
                if depth > 0 or depth < 0:  # 只要是0，就停机
                    # 继续取得以klg为开头的知识链
                    Knowledge._getAllBackwardsInDB(klgs, backwards_klgs, depth - 1, lazy_get,
                                                   memory=memory)

    #
    # def getAllBackwardsInDB(self, lazy_get=True):
    #     """
    #     取得以当前KnowledgeItem的kid为endid的所有前链（前链，即域对象、域或标签，以当前知识链为结束）。
    #     eg:
    #         self = [猪能说话]
    #         return [[西游记], [中国[上古[史诗神话]]], [猪八戒], [小猪佩奇]...]
    #     :param lazy_get 是否等需要的时候再取得对应的对象（以getChainItems填充）
    #     :return: 前链列表[Knowledge]
    #     """
    #     if len(self._backwards) > 0:
    #         return self._backwards
    #
    #     klgs = Knowledge.getKnowledgesByEndInDB(self.kid, lazy_get)
    #     if klgs:
    #         if isinstance(klgs, list):
    #             for klg in klgs:
    #                 self._backwards[klg.kid] = klg
    #         elif isinstance(klgs, Knowledge):
    #             self._backwards[klgs.kid] = klgs
    #     return self._backwards

    @staticmethod
    def getKnowledgesByStartInMemory(start, lazy_get=True,memory=None):
        """
        查找以start开头的所有知识链
        :param start: RealObject、Knowledge、kid或是rid(BaseEntity及其继承类，或 Id字符串)
        :param lazy_get 是否等需要的时候再取得对应的对象（以getChainItems填充）
        :return: [Knowledge]
        """
        if not memory:
            return None
        if not start:
            raise Exception("start(%s)不能为空！" % start)

        startid = Knowledge._getId(start)
        klgs = Knowledge.getAllByRetriveColumnsInMemory(memory=memory,startid=startid)

        if not lazy_get and klgs:
            if isinstance(klgs, list):
                for klg in klgs:
                    klg.getChainItems()
            else:
                klgs.getChainItems()

        return klgs

    @staticmethod
    def getKnowledgesByStartInDB(start, lazy_get=True,memory=None):
        """
        查找以start开头的所有知识链
        :param start: RealObject、Knowledge、kid或是rid(BaseEntity及其继承类，或 Id字符串)
        :param lazy_get 是否等需要的时候再取得对应的对象（以getChainItems填充）
        :return: [Knowledge]
        """
        if not start:
            raise Exception("start(%s)不能为空！" % start)

        startid = Knowledge._getId(start)
        klgs = Knowledge.getAllByConditionsInDB(memory=memory,startid=startid)

        if not lazy_get and klgs:
            if isinstance(klgs, list):
                for klg in klgs:
                    klg.getChainItems()
            else:
                klgs.getChainItems()

        return klgs

    @staticmethod
    def getKnowledgesByEndInDB(end, lazy_get=True,memory=None):
        """
        查找以end结尾的所有知识链
        :rawParam end: RealObject、Knowledge、kid或是rid(BaseEntity及其继承类，或 Id字符串)
        :param lazy_get 是否等需要的时候再取得对应的对象（以getChainItems填充）
        :return: [Knowledge]
        """
        if not end:
            raise Exception("end(%s)不能为空！" % end)

        endid = Knowledge._getId(end)

        klgs = Knowledge.getAllByConditionsInDB(memory=memory,endid=endid)

        if not lazy_get and klgs:
            if isinstance(klgs, list):
                for klg in klgs:
                    klg.getChainItems()
            else:
                klgs.getChainItems()

        return klgs


    @staticmethod
    def getKnowledgesByEndInMemory(end, lazy_get=True, memory=None):
        """
        查找以start开头的所有知识链
        :param end: RealObject、Knowledge、kid或是rid(BaseEntity及其继承类，或 Id字符串)
        :param lazy_get 是否等需要的时候再取得对应的对象（以getChainItems填充）
        :return: [Knowledge]
        """
        if not memory:
            return None
        if not end:
            raise Exception("end(%s)不能为空！" % end)

        endid = Knowledge._getId(end)
        klgs = Knowledge.getAllByRetriveColumnsInMemory(memory=memory,endid=endid)

        if not lazy_get and klgs:
            if isinstance(klgs, list):
                for klg in klgs:
                    klg.getChainItems()
            else:
                klgs.getChainItems()

        return klgs

    @staticmethod
    def getKnowledgeByStartAndEnd(start, end, lazy_get=False,memory=None):
        """
        在内存或数据库中查找以start开头并且以end结尾的元数据链(只能有一条)
        :param start: RealObject、Knowledge、kid或是rid(BaseEntity及其继承类，或 Id字符串)
        :param end: RealObject、Knowledge、kid或是rid(BaseEntity及其继承类，或 Id字符串)
        :param lazy_get 是否等需要的时候再取得对应的对象（以getChainItems填充）
        :return: Knowledge
        """
        # 首先在内存中查找
        klg = Knowledge.getKnowledgeByStartAndEndInMemory(start, end,memory=memory)
        if klg:
            return klg
        # 内存没找到，在数据库中查找
        klg = Knowledge.getKnowledgeByStartAndEndInDB(start, end, lazy_get,memory=memory)
        return klg

    @staticmethod
    def getKnowledgeByStartAndEndInMemory(start, end,memory=None):
        """
        [内存操作]查找以start开头并且以end结尾的元数据链(只能有一条)
        :param start: RealObject、Knowledge、kid或是rid(BaseEntity及其继承类，或 Id字符串)
        :param end: RealObject、Knowledge、kid或是rid(BaseEntity及其继承类，或 Id字符串)
        :return: Knowledge
        """
        if memory:
            if not start:
                raise Exception("start(%s)不能为空！" % start)
            if not end:
                raise Exception("end(%s)不能为空！" % end)

            startid = Knowledge._getId(start)
            endid = Knowledge._getId(end)
            return memory.getByDoubleKeysInMemory(startid,endid,Knowledge)


    @staticmethod
    def getKnowledgeByStartAndEndInDB(start, end, lazy_get=True,memory=None):
        """
        [数据库操作]查找以start开头并且以end结尾的元数据链(只能有一条)
        :param start: RealObject、Knowledge、kid或是rid(BaseEntity及其继承类，或 Id字符串)
        :param end: RealObject、Knowledge、kid或是rid(BaseEntity及其继承类，或 Id字符串)
        :param lazy_get 是否等需要的时候再取得对应的对象（以getChainItems填充）
        :return: Knowledge
        """
        if not start:
            raise Exception("start(%s)不能为空！" % start)
        if not end:
            raise Exception("end(%s)不能为空！" % end)

        startid = Knowledge._getId(start)
        endid = Knowledge._getId(end)
        klgs = Knowledge.getAllByConditionsInDB(memory=memory,startid=startid, endid=endid)
        if klgs is None:
            return None
        if isinstance(klgs, list):
            if klgs is None or len(klgs) == 0:
                return None
            if len(klgs) > 1:
                raise Exception("以start开头并且以end结尾的知识链只能有一条,start:%s,start type:%s,end:%s,end type:%s" % (
                    startid, str(type(start)), endid, str(type(end))))

            klg = klgs[0]
        else:
            klg = klgs

        klg._start_item = start
        klg._end_item = end

        if not lazy_get:
            klg.getChainItems()

        # 添加到内存以便后续操作
        if memory:
            memory.PersistentMemory.addInMemory(klg)

        return klg

    def delete(self):
        """
        [数据库操作]重写逻辑删除，逻辑删除Knowledge之前先把相关的关系逻辑删除。
        :return:
        """
        # 逻辑删除所有以本KnowledgeItem开始和结束的KnowledgeItem
        Knowledge.deleteByStart(self)
        Knowledge.deleteByEnd(self)

        return super(Knowledge, self).delete()

    @staticmethod
    def deleteByStart(start):
        """
        根据开始对象，逻辑删除所有KnowledgeItem
        :param start:BaseEntity及其继承类，或 Id字符串
        :return:
        """
        if start is None:
            raise Exception("无法逻辑删除所有KnowledgeItem，start is None！")
        # startid=Knowledge._getId(start)
        klgs = Knowledge.getKnowledgesByStartInDB(start)
        if isinstance(klgs, list):
            for klg in klgs:
                klg.delete()
        elif isinstance(klgs, Knowledge):
            klgs.delete()

            # Knowledge.updateAll(wheres = {"startid":startid},isdel=True)

    @staticmethod
    def deleteByEnd(end):
        """
        根据结尾对象，逻辑删除所有KnowledgeItem
        :param end:BaseEntity及其继承类，或 Id字符串
        :return:
        """
        if end is None:
            raise Exception("无法逻辑删除所有KnowledgeItem，end is None！")
        # endid=Knowledge._getId(end)
        klgs = Knowledge.getKnowledgesByEndInDB(end)
        if isinstance(klgs, list):
            for klg in klgs:
                klg.delete()
        elif isinstance(klgs, Knowledge):
            klgs.delete()

            # Knowledge.updateAll(wheres = {"endid":endid},isdel=True)

    def deleteAllBackwardsInDB(self):
        """
        删除以当前KnowledgeItem的kid为endid的所有前链（前链，即域对象、域或标签，以当前知识链为结束）。
        :return:
        """
        backwards = self.getAllBackwardsInDB()
        if backwards:
            for _id, backward in backwards:
                backward.delete()

    def deleteAllForwardsInDB(self):
        """
        删除以当前KnowledgeItem的kid为startid的所有后链。
        :return:
        """
        forwards = self.getAllForwardsInDB()
        if forwards:
            for _id, forward in forwards:
                forward.delete()

    @staticmethod
    def deleteByStartAndEnd(start, end):
        """
        根据start,end取得Knowledge，进行逻辑删除。
        :param start: RealObject、Knowledge、kid或是rid(BaseEntity及其继承类，或 Id字符串)
        :param end:  RealObject、Knowledge、kid或是rid(BaseEntity及其继承类，或 Id字符串)
        :return:
        """
        klg = Knowledge.getKnowledgeByStartAndEnd(start, end)
        if klg:
            klg.delete()

    @staticmethod
    def deleteByMetaChain(realChain, deleteAllChain=False):
        """
        根据realChain删除Knowledge
        :param realChain:[realData,[realData,realData]]
        :param deleteAllChain 是否删除全链
        :return:
        """
        if len(realChain) < 2:
            return
        real_nets = []
        klg = Knowledge.getKnowledgeByObjectChain(realChain, real_nets)
        if deleteAllChain:
            for real_net in real_nets:
                real_net.delete()
        elif klg:
            klg.delete()
        return klg
        # start = realChain[0]
        # for i in range(1, len(realChain)):
        #     if isinstance(start,list):
        #         start=Knowledge.deleteByMetaChain(start)
        #     if start is None:
        #         return None
        #
        #     end = realChain[i]
        #     if isinstance(end,list):
        #         end=Knowledge.deleteByMetaChain(end)
        #
        #     start = Knowledge.deleteByStartAndEnd(start,end)
        #     if start is None:
        #         return None
        #
        # return start

    def _physicalDelete(self, recordInMemory=True, deleteRelatedLayers=True, deleteChainedObjs=True):
        """
        [数据库操作]重写物理删除，物理删除Knowledge之前先把相关的关系物理删除。
        :return:
        """
        # 物理删除所有以本KnowledgeItem开始和结束的KnowledgeItem
        _memory=None
        if recordInMemory:
            _memory=self.MemoryCentral
        Knowledge._physicalDeleteByStart(self,memory=_memory)
        Knowledge._physicalDeleteByEnd(self,memory=_memory)

        return super(Knowledge, self)._physicalDelete(recordInMemory, deleteRelatedLayers, deleteChainedObjs)

    @staticmethod
    def _physicalDeleteByStart(start,memory=None):
        """
        根据开始对象，物理删除所有KnowledgeItem
        :param start:BaseEntity及其继承类，或 Id字符串
        :return:
        """
        if start is None:
            raise Exception("无法物理删除所有KnowledgeItem，start is None！")
        # startid=Knowledge._getId(start)
        klgs = Knowledge.getKnowledgesByStartInDB(start,memory=memory)
        if isinstance(klgs, list):
            for klg in klgs:
                klg._physicalDelete()
        elif isinstance(klgs, Knowledge):
            klgs._physicalDelete()

            # Knowledge.updateAll(wheres = {"startid":startid},isdel=True)

    @staticmethod
    def _physicalDeleteByEnd(end,memory=None):
        """
        根据结尾对象，物理删除所有KnowledgeItem
        :param end:BaseEntity及其继承类，或 Id字符串
        :return:
        """
        if end is None:
            raise Exception("无法物理删除所有KnowledgeItem，end is None！")
        # endid=Knowledge._getId(end)
        klgs = Knowledge.getKnowledgesByEndInDB(end,memory=memory)
        if isinstance(klgs, list):
            for klg in klgs:
                klg._physicalDelete()
        elif isinstance(klgs, Knowledge):
            klgs._physicalDelete()

    def _physicalDeleteAllBackwardsInDB(self):
        """
        物理删除以当前KnowledgeItem的kid为endid的所有前链（前链，即域对象、域或标签，以当前知识链为结束）。
        :return:
        """
        backwards = self.getAllBackwardsInDB()
        if backwards:
            for _id, backward in backwards:
                backward._physicalDelete()

    def _physicalDeleteAllForwardsInDB(self):
        """
        物理删除以当前KnowledgeItem的kid为startid的所有后链。
        :return:
        """
        forwards = self.getAllForwardsInDB()
        if forwards:
            for _id, forward in forwards:
                forward._physicalDelete()

    @staticmethod
    def _physicalDeleteByStartAndEnd(start, end,memory=None):
        """
        根据start,end取得Knowledge，进行物理删除。
        :param start: RealObject、Knowledge、kid或是rid(BaseEntity及其继承类，或 Id字符串)
        :param end:  RealObject、Knowledge、kid或是rid(BaseEntity及其继承类，或 Id字符串)
        :return:
        """
        klg = Knowledge.getKnowledgeByStartAndEnd(start, end,memory=memory)
        if klg:
            klg._physicalDelete()

    @staticmethod
    def _physicalDeleteByMetaChain(realChain, deleteAllChain=False,memory=None):
        """
        根据realChain物理删除Knowledge
        :param realChain:[realData,[realData,realData]]
        :param deleteAllChain 是否删除全链
        :return:
        """
        if len(realChain) < 2:
            return
        real_nets = []
        klg = Knowledge.getKnowledgeByObjectChain(realChain, real_nets,memory=memory)
        if deleteAllChain:
            for real_net in real_nets:
                real_net._physicalDelete()
        elif klg:
            klg._physicalDelete()

    def isUnderstood(self):
        """
        查看当前知识链是否被“理解”（是否具有顶级关系或匹配其他模式）
        :return:
        """
        return Knowledge.isUnderstoodKnowledge(self)

    @staticmethod
    def isUnderstoodKnowledge(knowledge):
        """
        查看知识链是否被“理解”（是否具有顶级关系或匹配其他模式）
        :param knowledge: 知识链
        :return:
        """
        # todo 目前未实现匹配其他模式
        if knowledge.uratio >= 1.0:
            return True
        meaning_klgs = knowledge.Meanings.getAllMeanings()
        if meaning_klgs:
            return True
        return False

    def getUnderstoodRatio(self):
        """
        取得知识链已被识别的比率。
        :return:
        """
        # todo 应该是知识链中实际对象以及下一层知识链识别比率的总和？
        pass

    def isExecutionInfo(self):
        """
        当前知识链是否作为可执行信息（模式和意义）（里面有placeholder）。
        :return:
        """
        if self.getType() == ObjType.EXE_INFO:
            return True
        components = self.getSequenceComponents()
        for component in components:
            if component.isPlaceHolder():  # 只要有一个是PlaceHolder
                return True
        return False

    @staticmethod
    def hasTopRelation(knowledge):
        """
        查看知识链是否具有顶级关系。
        :param knowledge:
        :return:
        """
        if not knowledge or not isinstance(knowledge, Knowledge):
            raise Exception("必须具有知识链，knowledge is null!")

        # 不断递归取得当前链的所有StartItem、EndItem对象（Knowledge、RealObject）
        components = knowledge.getSequenceComponents()

        for component in components:
            if component in Instincts.TopRelations:
                return True

        return False

    @staticmethod
    def isTriStructure(knowledge):
        """
        查看知识链是否符合顶级关系的三元组结构。
        :param knowledge:
        :return:
        """
        if not knowledge or not isinstance(knowledge, Knowledge):
            raise Exception("必须具有知识链，knowledge is null!")

        # 不断递归取得当前链的所有StartItem、EndItem对象（Knowledge、RealObject）
        components = knowledge.getSequenceComponents()

        return len(components)==3

    def isSelfRealObject(self):
        """
        判断一个知识链是否是实际对象（例如：知识链[中国-人民-解放军]，或是：[中国-[人民-解放军]]的实际对象，就是 中国人民解放军）。
        :return: 是否实际对象,实际对象（只能有一个）。
        """
        realObj = self.Layers.getLowerEntitiesByType(type=ObjType.REAL_OBJECT)
        if realObj is None:
            return False, None
        from loongtian.nvwa.models.realObject import RealObject
        if isinstance(realObj, RealObject):
            return True, realObj
        if isinstance(realObj, list):
            if len(realObj) == 1 and isinstance(realObj[0], RealObject):
                return True, realObj[0]
            else:
                raise Exception("当前知识链指向的实际对象有多个，系统规定只能有一个！")
        return False, None

    def toCollectionRealObject(self,recordInDB=False):
        """
        从集合的角度考虑，当前知识链本身转化成的代表集合的实际对象（id相同） ，是由Knowledge的所有元素构成（组件关系）的RealObject。
        :return:k:{r:中国-r:人民-r:解放军}——》r:x，r:x-r:父对象-r:集合,r:x-r:组件-r:中国......其中：k的id 应与 r:x的id相同
        """
        # 检查是否存在
        if not self._self_realObject:
            self._self_realObject = RealObject.getOneInDB(
                                                        rid=self.id,
                                                        memory=self.MemoryCentral)  # self.Layers.getLowerEntitiesByType(type=ObjType.REALOBJECT)

        # 如果存在
        if not self._self_realObject is None:
            self._self_realObject.Constitutions.getSequenceComponents()
            return self._self_realObject, \
                   self._self_realObject._sequence_components_klgs, \
                   self._self_realObject._sequence_components_klgs_sequence_klg

        # 如果不存在，创建之
        self._self_realObject = RealObject(rid=self.id,
                                           realType=ObjType.VIRTUAL,
                                           memory=self.MemoryCentral).create(checkExist=False,
                                                                             recordInDB=recordInDB)
        # 定义为集合
        self._self_realObject.Constitutions.addParent(Instincts.instinct_original_collection,
                                                      weight=Character.Inner_Instinct_Link_Weight,
                                                      recordInDB=recordInDB)

        # 将当前知识链的所有元素添加到实际对象的组件中（有顺序）
        # 取得当前知识链的构成元素（有顺序）
        self._self_realObject._sequence_components = self.getSequenceComponents()
        # 逐一添加元素
        self._self_realObject._sequence_components_klgs = []
        for component in self._self_realObject._sequence_components:
            cur_klg = self._self_realObject.Constitutions.addComponent(component,
                                                         recordInDB=recordInDB)  # 当前集合（实际对象）-组件为-实际组件记录
            self._self_realObject._sequence_components_klgs.append(cur_klg)

        # 添加上下条记录的关系
        # 应该形成的T-Graph：
        # k'0   k1    k2
        # k'1   k'0   k3
        # k'2   k'1   k4
        self._self_realObject._sequence_components_klgs_sequence_klg = \
            Knowledge.createKnowledgeByObjChain(
                self._self_realObject._sequence_components_klgs,
                understood_ratio=Character.Inner_Instinct_Link_Weight,
                recordInDB=recordInDB,
                memory=self.MemoryCentral)

        self._self_realObject.remark="CollectionReal:%s" % (self.getSequenceComponents())
        return self._self_realObject, \
               self._self_realObject._sequence_components_klgs, \
               self._self_realObject._sequence_components_klgs_sequence_klg

    def toEntityRealObject(self):
        """
        将一个知识链迁移为实际对象实体（下一层实际对象，id不同）。
        由Knowledge的所有元素通过迁移引擎生成的RealObject，知识链的所有元素之间是修限关系或是动作执行关系
        例如：r:中国-r:人民-r:银行——>r:中国人民银行。
        中国人民银行不是由r:中国-r:人民-r:银行三个组件组成的，
        而是一个父对象-银行，名称中国人民银行，从属于中国......的实体
        :return:
        """
        entity_reals = self.Layers.getLowerEntitiesByType(ObjType.REAL_OBJECT)
        if entity_reals:
            return entity_reals.getCurObj()

        entity_real =RealObject(memory=self.MemoryCentral)
        self.Layers.addLower(entity_real)
        entity_real.remark="EntityReal:%s" % (self.getSequenceComponents())
        return entity_real


    def isNLKnowledge(self):
        """
        判断当前知识链是否为自然语言（奇数位是"下一个为"）的知识链
        :return:bool
        """
        # 如果已经判断过了，直接返回结果
        if not self._is_NL_Knowledge is None and isinstance(self._is_NL_Knowledge, bool):
            return self._is_NL_Knowledge

        components = self.getSequenceComponents()

        _all_odd_is_next = True  # 判断奇数位是"下一个为"
        for i in range(1, len(components), 2):  # 取奇数位
            if components[i].id != Instincts.instinct_original_next.id:
                _all_odd_is_next = False
                break
        if _all_odd_is_next:
            self._is_NL_Knowledge = True
        else:
            self._is_NL_Knowledge = False

        return self._is_NL_Knowledge

    def toNLKnowledge(self):
        """
        将当前知识链转换成自然语言（带"下一个为"）的知识链。默认情况下，自然语言知识链只在'思考'时使用。
        :return:自然语言（带"下一个为"）知识链
        """
        # 如果已经取得了，直接返回结果
        if not self._NL_Knowledge is None and isinstance(self._NL_Knowledge, Knowledge):
            return self._NL_Knowledge

        components = self.getSequenceComponents()
        # 首先判断当前知识链是否为自然语言（奇数位是"下一个为"）的知识链
        _all_odd_is_next = True  # 判断奇数位是"下一个为"
        for i in range(1, len(components), 2):  # 取奇数位
            if components[i].id != Instincts.instinct_original_next.id:
                _all_odd_is_next = False
                break
        if _all_odd_is_next:
            self._is_NL_Knowledge = True
        else:
            self._is_NL_Knowledge = False
        # 如果是自然语言（奇数位是"下一个为"）的知识链，直接返回当前知识链
        if self._is_NL_Knowledge:
            return self

        nl_components = []
        for component in components:
            nl_components.extend([component, Instincts.instinct_original_next])

        # 删除掉最后一个"下一个为"
        nl_components.pop()
        klg = Knowledge.createKnowledgeByObjChain(nl_components, memory=self.MemoryCentral)
        return klg

    def toPlainKnowledge(self):
        """
        将自然语言（带"下一个为"）的知识链转换成内部存储的知识链。默认情况下，自然语言知识链只在'思考'时使用。
        :return:
        """
        if not self.isNLKnowledge():
            return self

        components = self.getSequenceComponents()
        final_components = []
        for component in components:
            if not component.id == Instincts.instinct_original_next.id:
                final_components.append(component)

        return Knowledge.createKnowledgeByObjChain(final_components, memory=self.MemoryCentral)

    def isSame(self, realChain):
        """
        匹配现有知识链与实际对象列表是否相同。
        :param realChain: 实际对象列表
        :return:
        """
        klg = Knowledge.createKnowledgeByObjChain(realChain, recordInDB=False, memory=self.MemoryCentral)
        if klg.id == self.id:
            return True
        return False

    def getDomains(self, lazy_get=True):
        """
        取得当前知识链所有的域。例如：猪-会-说话的域可以为：西游记，小猪佩奇etc.
        :return:
        """
        return Knowledge.getKnowledgesByEndInDB(self, memory=self.MemoryCentral)

    def getDomained(self, lazy_get=True):
        """
        取得当前知识链所有的被域。例如：猪-会-说话的域可以为：西游记，小猪佩奇etc.
        :return:
        """
        return Knowledge.getKnowledgesByStartInDB(self, lazy_get=lazy_get, memory=self.MemoryCentral)

    def addDomain(self, domain, understood_ratio):
        """
        给当前知识链添加域（域应为知识链或实际对象）。例如：猪-会-说话的域可以为：西游记，小猪佩奇etc.
        :param domain:
        :return:
        """
        if domain is None or not isinstance(domain, Knowledge) or not isinstance(domain, RealObject):
            raise Exception("参数错误，一个知识链的域应为知识链或实际对象！")
        # 查看是否存在
        klg = Knowledge.getKnowledgeByStartAndEnd(domain, self,
                                                  memory=self.MemoryCentral)
        if klg:
            return klg
        # 不存在，创建之
        return Knowledge.createKnowledgeByStartEnd(domain, self,
                                                   understood_ratio=understood_ratio,
                                                   memory=self.MemoryCentral)

    def removeDomain(self, domain):
        """
        给当前知识链删除域（域应为知识链或实际对象）。例如：猪-会-说话的域可以为：西游记，小猪佩奇etc.
        :param domain:
        :return:
        """
        if domain is None or not isinstance(domain, Knowledge) or not isinstance(domain, RealObject):
            raise Exception("参数错误，一个知识链的域应为知识链或实际对象！")
        return Knowledge.deleteByStartAndEnd(domain, self)


    def isMeaningKnowledge(self):
        """
        当前知识链是否符合意义（runtime.meanings.Meanings）的定义（三层list嵌套，steps-statuses-objChain）
        :return:True/False,_meaning/None
        """
        components = self.getSequenceComponents()
        if not components:
            return
        try:
            from loongtian.nvwa.runtime.meanings import Meaning
            _meaning = Meaning.createByStepsObjChain(components)
            if _meaning:
                return True,_meaning
        except: # 可能格式不匹配，不抛出错误
            return False,None

        return False, None

    def getInnerOperations(self):
        """
        判断当前知识链是否是内部操作。
        :return:
        """
        is_meaning,meaning =self.isMeaningKnowledge()
        if not is_meaning:
            return False,None
        from loongtian.nvwa.runtime.innerOperation import InnerOperations
        InnerOperations.loadAllInnerOperations()
        inner_operations=[]
        for step in meaning.steps:
            for status in step.statuses:
                if isinstance(status.objChain[0],RealObject) and status.objChain[0].id == InnerOperations.operation_mark.id:
                    cur_inner_operation=InnerOperations.InnerOperationMap.get(status.objChain[1])
                    if cur_inner_operation:
                        inner_operations.append(cur_inner_operation)

        return inner_operations


    def getType(self):
        """
        获得类型
        :return: 总是返回IdTypeEnum.Knowledge类型。
        """
        return self.type
        # return ObjType.KNOWLEDGE



    def __repr__(self):
        if len(self._t_chain_words) > 0:
            return "{Knowledge:{kid:%s,components:%s}}" % (self.kid, str(self.getSequenceComponents()))
        else:
            return "{Knowledge:{kid:%s}}" % (self.kid)


class _Meanings(object):
    """
    知识链意义操作的封装类
    """

    def __init__(self, know):
        """
        知识链意义操作的封装类
        :param know:当前知识链
        """
        if not isinstance(know, Knowledge):
            raise Exception("必须提供知识链，才能进行意义操作！")
        self.know = know  # 当前知识链
        self._dominance_meanings = None  # 当前知识链的显性意义。（只有知识链才能有迁移意义。实际对象的意义由构成表示）
        self._recessivity_meanings = None  # 当前知识链的隐性意义。（只有知识链才能有迁移意义。实际对象的意义由构成表示）
        # self._meanings =Meanings()

    def getAllMeanings(self):
        """
        取得当前知识链的所有意义（包括显性意义、隐性意义）。
        :return:
        """
        if self.know.isExecutionInfo():
            return None
        if Knowledge.hasTopRelation(self.know) and Knowledge.isTriStructure(self.know): # 如果知识链已经包含顶级关系了，并且符合三元组原则，创建Meaning
            return Meaning.createByStatusKnowledge(self.know)

        all_meaning_klgs = []

        dominance_meanings = self.getDominanceMeanings()
        if dominance_meanings:
            all_meaning_klgs.extend(dominance_meanings)
        recessivity_meanings = self.getRecessivityMeanings()
        if recessivity_meanings:
            all_meaning_klgs.extend(recessivity_meanings)

        if all_meaning_klgs:
            # 可能有重复的（显性意义与隐性意义同时存在），去重
            all_meaning_klgs=set(all_meaning_klgs)
            # todo 此处可能会产生错误，需要进一步处理
            _meanings = Meanings(memory=self.know.MemoryCentral)
            for _meaning_klg in all_meaning_klgs:
                _meaning = Meaning.createByStatusKnowledge(_meaning_klg)
                _meanings.append(_meaning)
            return _meanings

        return None



    # @staticmethod
    # def getKnowledgeMeaning(knowledge):
    #     """
    #     取得知识链被“理解”的意义（是否具有顶级关系或匹配其他模式）
    #     :param knowledge: 知识链
    #     :return:
    #     """
    #     if knowledge.isExecutionInfo():
    #         return None
    #     if Knowledge.hasTopRelation(knowledge):
    #         return knowledge
    #
    #     meaning_klg = None
    #     next_layer_knowledge = knowledge
    #     # 循环操作，查找下一层的knowledge（如果有的话），直到找到被“理解”（具有顶级关系）的knowledge
    #     while True:
    #         next_layer_knowledge = next_layer_knowledge.Layers.getLowerEntitiesByType(ObjType.KNOWLEDGE)
    #         if next_layer_knowledge:
    #             next_layer_knowledge = next_layer_knowledge[0]
    #             if Knowledge.isUnderstoodKnowledge(next_layer_knowledge):
    #                 meaning_klg = next_layer_knowledge
    #                 break
    #         else:
    #             break
    #
    #     return meaning_klg

    def getDominanceMeanings(self):
        """
        取得当前知识链的显性意义。（使用知识链-意义为-知识链2表示。只有知识链才能有迁移意义。实际对象的意义由构成表示）
        :return:
        """
        # 如果已经取得过了，直接返回结果
        if self._dominance_meanings:
            return self._dominance_meanings

        # 取得知识链-意义为-知识链2
        list_self = self.know.getKnowledgeByStartAndEnd(self.know,
                                                        Instincts.instinct_original_list,
                                                        memory=self.know.MemoryCentral)
        if list_self:
            start_klg = self.know.getKnowledgeByStartAndEnd(list_self,
                                                            Instincts.instinct_meaning,
                                                            memory=self.know.MemoryCentral)
            if start_klg and isinstance(start_klg, Knowledge):
                self._dominance_meanings = start_klg.getAllForwardsInDB()
        return self._dominance_meanings

    def getRecessivityMeanings(self):
        """
        取得当前知识链的隐性意义。（使用知识链的下一层知识链表示。只有知识链才能有迁移意义。实际对象的意义由构成表示）
        :return:
        """
        # 如果已经取得过了，直接返回结果
        if self._recessivity_meanings:
            return self._recessivity_meanings
        # 取得当前知识链的下一层知识链
        self._recessivity_meanings = self.know.Layers.getLowerEntitiesByType(ObjType.KNOWLEDGE)

        return self._recessivity_meanings

    def convertDominanceMeaningsToRecessivity(self):
        """
        将知识链所有的显性意义转换为隐性意义（压缩知识库的规模，以减少查找等操作的管理）。
        :param know:
        :return:
        """
        return _Meanings.convertKnowledgeDominanceMeaningsToRecessivity(self.know)

    @staticmethod
    def convertKnowledgeDominanceMeaningsToRecessivity(know):
        """
        将知识链所有的显性意义转换为隐性意义（压缩知识库的规模，以减少查找等操作的管理）。
        :param know:
        :return:
        """
        if not know or not isinstance(know, Knowledge):
            raise ("必须提供Knowledge，当前将知识链所有的显性意义转换为隐性意义操作无法完成！")

        dominance_meanings = know.Meanings.getDominanceMeanings()
        if dominance_meanings:
            for dominance_meaning in dominance_meanings:
                _Meanings._convertDominanceMeaningToRecessivity(know, dominance_meaning)

    @staticmethod
    def _convertDominanceMeaningToRecessivity(know, dominance_meaning):
        """
        将知识链所有的显性意义转换为隐性意义（压缩知识库的规模，以减少查找等操作的管理）。
        :param know:
        :return:
        """
        # todo 这里可能产生大量错误！需修改
        dominance_meaning.getChainItems()
        know.Layers.addLower(dominance_meaning._end_item)
        dominance_meaning._physicalDelete()

