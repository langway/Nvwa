#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

import copy
from loongtian.nvwa import settings
from loongtian.nvwa.language import EntityName
from loongtian.nvwa.models.baseEntity import LayerLimitation
from loongtian.nvwa.models.tGraphEntity import TGraphEntity, Instincts
from loongtian.nvwa.models.enum import ObjType
from loongtian.nvwa.models.realObject import RealObject
from loongtian.nvwa.models.executionInfo import ContextExecutionInfo

from loongtian.nvwa.runtime.collection import Collection
from loongtian.nvwa.runtime.meanings import Meaning, Meanings

from loongtian.nvwa.organs.character import Character


class Knowledge(TGraphEntity):
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

    1、t_graph是一个T字型结构的由realObject、Knowledge的Id组成的数组(嵌套代表一条Knowledge)。格式为：[id,(kid,[t_graph])]
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
    __tablename__ = settings.db.tables.tbl_knowledge  # 所在表。与Flask统一
    primaryKey = copy.copy(TGraphEntity.primaryKey)  # 模型对应的主键
    primaryKey.extend(["id"])
    columns = copy.copy(TGraphEntity.columns)  # 模型对应的非主键的全部字段
    columns.extend(["uratio", "type"])
    # columns.remove("mnvalue")

    upperLimitation = LayerLimitation()
    upperLimitation.update({ObjType.META_NET: 1,  # m:中国-m:人民-m:解放军——>r:中国-r:人民-r:解放军
                            ObjType.REAL_OBJECT: 1,  # realobject——>pattern(knowledge) ——>meaning(knowledge)
                            # ObjType.KNOWLEDGE: 1,
                            })  # 在上一层其他对象的分层中，包含的对象类型、数量限制，
    # Knowledge 的上一层对象，为RealObject[多个]，代表当前Knowledge，Knowledge[一个]
    lowerLimitation = LayerLimitation()
    lowerLimitation.update({ObjType.REAL_OBJECT: 1,  # r:中国-r:人民-r:解放军——>r:中国人民解放军
                            ObjType.KNOWLEDGE: 1,  # pattern(knowledge) ——>meaning(knowledge)
                            ObjType.LINEAR_EXE_INFO: -1,  # 一个模式对应多个意义
                            })  # 在下一层其他对象的分层中，包含的对象类型、数量限制，
    # Knowledge只能有一个下层对象RealObject，多个下层对象Knowledge（一个是meaning的头，一个是pattern）
    # RealObject和Knowledge的下一层对象可以解析为：意义为、意思为、指的是、含义为、meaning等

    curEntityName = EntityName.KnowledgeEntityName  # 当前T字形结构实体类的名称：元数据网、知识链，在两个类中赋值
    curEntityObjType = ObjType.KNOWLEDGE  # 对象定义类型
    curItemObjType = ObjType.REAL_OBJECT
    curItemType = RealObject  # MetaData/RealObject
    curItemWordColumn = "remark"

    def __init__(self, start=None, end=None, kid=None, stype=None, etype=None,
                 weight=Character.Original_Link_Weight,
                 understood_ratio=0.0,
                 type=ObjType.KNOWLEDGE,
                 t_graph=None, t_chain=None, s_chain=None,  # m_chain=None,
                 createrid=None,
                 createtime=None, updatetime=None, lasttime=None,
                 status=200,  # 状态; 0-不可用(逻辑删除);200-正常;800-不可遗忘
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
        :param t_graph:是一个T字型结构的由realObject、Knowledge的Id组成的数组(嵌套代表一条Knowledge)。格式为：[id,(kid,[t_graph])]
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
        super(Knowledge, self).__init__(start, end, kid, stype, etype,
                                        weight,
                                        t_graph, t_chain, s_chain,
                                        createrid,
                                        createtime, updatetime, lasttime,
                                        status, memory)
        self.type = type  # 类型根据外部设置

        self.uratio = understood_ratio  # 理解率

        # ####################################
        #      下面为运行时数据
        # ####################################

        # 关联所有集合操作的封装类。
        self.Collection = Collection(self)

        # 知识链意义操作的封装类
        self.Meanings = _Meanings(self)

        self.ContextExecutionInfo = None # ContextExecutionInfo(self)

        # 当前知识链本身转化成的实际对象（id相同） r:中国-r:人民-r:解放军——>r:x,，r:x-r:父对象-r:集合,r:x-r:组件-r:中国......
        self._self_realObject = None

        self._is_NL_Knowledge = None  # 当前知识链是否为自然语言（奇数位是"下一个为"）的知识链
        self._NL_Knowledge = None  # 当前知识链转换成自然语言（带"下一个为"）的知识链。默认情况下，自然语言知识链只在'思考'时使用。

    def create(self, checkExist=True, recordInDB=True, **kwargs):
        """
        [重载函数]CRUD - Create（因为要对所有的components进行处理，所以不能简单的对当前的知识链（仅仅是start、end）进行处理）
        :param checkExist:检查是否存在
        :param recordInDB:是否在数据库中创建（False返回自身，例如：自然语言的知识链（NL_Knowledge，奇数位为“下一个为”）就不需要在数据库中创建）
        :return: 返回建立的knowledge。
        """
        if not kwargs:
            kwargs = {"understood_ratio": self.uratio}
        else:
            kwargs.update({"understood_ratio": self.uratio})
        return super(Knowledge, self).create(checkExist=checkExist,
                                             recordInDB=recordInDB,
                                             **kwargs)

    @classmethod
    def createKnowledgeByStartEnd(cls, start, end, type=ObjType.KNOWLEDGE,
                                  understood_ratio=Character.Original_Link_Weight,
                                  recordInDB=True,
                                  checkExist=True,
                                  memory=None):
        """
        创建Knowledge（允许end为None）
        :param start:可以是RealObject、Knowledge或[sid,stype]\\(sid,stype)
        :param end:可以是RealObject、Knowledge或[eid,etype]\\(eid,etype)
        :return:
        """
        kwargs = {"understood_ratio": understood_ratio,
                  "type": type}
        return cls.createByStartEnd(start, end, recordInDB, checkExist, memory, **kwargs)

    @classmethod
    def createKnowledgeByObjChain(cls,
                                  obj_chain,
                                  type=ObjType.KNOWLEDGE,
                                  obj_nets=None,
                                  understood_ratio=0.0,
                                  recordInDB=True,
                                  checkExist=True,
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
        kwargs = {"type": type,
                  "understood_ratio": understood_ratio,
                  "recordRelationInFirstReal": recordRelationInFirstReal}
        return cls._createByObjChain(obj_chain, obj_nets,
                                     recordInDB, checkExist, memory,
                                     **kwargs)

    def createUpperRealObject(self, remark=None, realType=ObjType.REAL_OBJECT):
        """
        创建代表当前Knowledge的实际对象
        :return:
        """
        self.getChainItems()
        if remark is None:
            remark = self._s_chain_words
        new_real = RealObject(remark=remark, type=realType,
                              memory=self.MemoryCentral).create()
        self.Layers.addUpper(new_real)
        new_real.Layers.addLower(self, recordInDB=False)  # 已经添加过了
        return new_real

    def isUnderstood(self):
        """
        查看当前知识链是否被“理解”（当前知识链，或下层知识链是否具有顶级关系或匹配其他模式）
        :return:
        """
        return Knowledge.isUnderstoodKnowledge(self)

    @staticmethod
    def isUnderstoodKnowledge(knowledge):
        """
        查看当前知识链是否被“理解”（当前知识链，或下层知识链是否具有顶级关系或匹配其他模式）
        :param knowledge: 知识链
        :return:
        """
        # todo 目前未实现匹配其他模式
        if knowledge.uratio >= 1.0:
            return True, knowledge
        if Knowledge.hasTopRelation(knowledge):
            return True, knowledge
        if knowledge.isMeaningKnowledge():
            return True, knowledge
        # 下层知识链
        meaning_klgs = knowledge.Meanings.getAllMeanings()  # 可能有多个
        if meaning_klgs:
            return True, meaning_klgs
        return False, None

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
        if self.getType() == ObjType.LINEAR_EXE_INFO:
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
            if component.id in Instincts.InstinctsIdDict:
                return True

        return False

    @staticmethod
    def isTriStructure(tgraph):
        """
        查看知识链是否符合顶级关系的三元组结构。
        :param tgraph:
        :return:
        """
        if not tgraph or not isinstance(tgraph, Knowledge):
            raise Exception("必须具有知识链，tgraph is null!")

        # 不断递归取得当前链的所有StartItem、EndItem对象（Knowledge、RealObject）
        components = tgraph.getSequenceComponents()

        return len(components) == 3

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

    def toCollectionRealObject(self, recordInDB=False):
        """
        从集合的角度考虑，当前知识链本身转化成的代表集合的实际对象（id相同） ，是由Knowledge的所有元素构成（组件关系）的RealObject。
        :return:k:{r:中国-r:人民-r:解放军}——》r:x，r:x-r:父对象-r:集合,r:x-r:组件-r:中国......其中：k的id 应与 r:x的id相同
        """
        # 检查是否存在
        if not self._self_realObject:
            self._self_realObject = RealObject.getOneInDB(
                id=self.id,
                memory=self.MemoryCentral)  # self.Layers.getLowerEntitiesByType(type=ObjType.REALOBJECT)

        # 如果存在
        if not self._self_realObject is None:
            self._self_realObject.Constitutions.getSequenceComponents()
            return self._self_realObject, \
                   self._self_realObject._sequence_components_klgs, \
                   self._self_realObject._sequence_components_klgs_sequence_klg

        import loongtian.nvwa.models.entityHelper as  entityHelper
        # 如果不存在，创建之
        self._self_realObject = RealObject(id=self.id,
                                           type=ObjType.VIRTUAL,
                                           remark="CollectionReal:%s" % entityHelper.getNatureLanguage(
                                               self.getSequenceComponents()),
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
            Knowledge.createKnowledgeByObjChain(self._self_realObject._sequence_components_klgs,
                                                understood_ratio=Character.Inner_Instinct_Link_Weight,
                                                recordInDB=recordInDB,
                                                memory=self.MemoryCentral)

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
        # 创建到内存
        entity_real = RealObject(memory=self.MemoryCentral).create(checkExist=False, recordInDB=False)
        self.Layers.addLower(entity_real)
        components = self.getSequenceComponents()
        import loongtian.nvwa.models.entityHelper as entityHelper
        entity_real.remark = entityHelper.getNatureLanguage(components, seperator="")
        entity_real.type=ObjType.ENTITY_REAL_OBJECT # 根据动作分组产生的新实体对象，需在存储时进行处理（暂时转换成VIRTUAL对象【待考虑】）
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
                return True, _meaning
        except:  # 可能格式不匹配，不抛出错误
            return False, None

        return False, None

    def getInnerOperations(self):
        """
        判断当前知识链是否是内部操作。
        :return:
        """
        is_meaning, meaning = self.isMeaningKnowledge()
        if not is_meaning:
            return False, None
        from loongtian.nvwa.runtime.innerOperation import InnerOperations
        InnerOperations.loadAllInnerOperations()
        inner_operations = []
        for step in meaning.steps:
            for status in step.statuses:
                if isinstance(status.objChain[0], RealObject) and \
                        status.objChain[0].id == InnerOperations.operation_mark.id:
                    cur_inner_operation = InnerOperations.InnerOperationMap.get(status.objChain[1])
                    if cur_inner_operation:
                        inner_operations.append(cur_inner_operation)

        return inner_operations

    def __repr__(self):
        if len(self._t_chain_words) > 0:
            return "{Knowledge:{kid:%s,components:%s}}" % (self.id, str(self.getSequenceComponents()))
        else:
            return "{Knowledge:{kid:%s}}" % (self.id)


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
        if Knowledge.hasTopRelation(self.know) and Knowledge.isTriStructure(
                self.know):  # 如果知识链已经包含顶级关系了，并且符合三元组原则，创建Meaning
            return Meaning.createByStatusKnowledge(self.know, memory=self.know.MemoryCentral)

        all_meaning_klgs = []

        dominance_meanings = self.getDominanceMeanings()
        if dominance_meanings:
            all_meaning_klgs.extend(dominance_meanings)
        recessivity_meanings = self.getRecessivityMeanings()
        if recessivity_meanings:
            all_meaning_klgs.extend(recessivity_meanings)

        if all_meaning_klgs:
            # 可能有重复的（显性意义与隐性意义同时存在），去重
            all_meaning_klgs = set(all_meaning_klgs)
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
        list_self = self.know.getByStartAndEnd(self.know,
                                               Instincts.instinct_original_list,
                                               memory=self.know.MemoryCentral)
        if list_self:
            start_klg = self.know.getByStartAndEnd(list_self,
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
