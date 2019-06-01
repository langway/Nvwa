#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

import copy
from loongtian.util.log import logger

from loongtian.nvwa import settings
from loongtian.nvwa.language import EntityName

from loongtian.nvwa.models.tGraphEntity import TGraphEntity
from loongtian.nvwa.models.baseEntity import LayerLimitation
from loongtian.nvwa.models.enum import ObjType
from loongtian.nvwa.models.metaData import MetaData

from loongtian.nvwa.organs.character import Character


class MetaNet(TGraphEntity):
    """
    元数据组成的网（T型单向链）,之间的关系体现了词、音节、视线扫描的关系。
    :rawParam
    :attribute
    mnid 元数据网ID，UUID。
    startid 起点ID，RID或mnid。
    stype 起点ID的类型，使用MetaNetEntity.IdTypeEnum枚举。
    endid 终点ID，RID或mnid。
    etype 终点ID的类型，使用MetaNetEntity.IdTypeEnum枚举。
    weight 阀值，用于遗忘或凝固。
    related_meta 元数据网相关连的元数据Id，例如：中国-人民-解放军，关联的元数据就是“中国人民解放军”
    related_knowledge 元数据网相关的知识网Id。
                        [我,知道,中国,人民,解放军,是,最棒,的]相关的知识网：
                        [我,知道,[[中国,人民,解放军],是,[最棒,的]]]
    status:状态; 0-不可用(逻辑删除);200-正常;800-不可遗忘
    1、 是一个T字型结构的由metaData、MetaNetItem的Id组成的数组(嵌套代表一条MetaNet)。格式为：[id,(kid,[t_graph])]
    2、 t_chain 是一个T字型结构的由metaData的Id组成的数组(嵌套代表一条metaNet)。
    3、s_chain  是一个未经T字型结构处理的由metaData的Id组成序列数组
    4、m_chain 是一个由外域（可能是个知识链，也可能是实际对象）、知识链的mnid组成的序列数组。

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
        2、[r1,[r2,r3],r4...rn] 以单个元素开头，以单个元素结尾，中间有单个元素、转折元素（MetaNet元素）
        3、[r1,[r2,r3],r4...[rn-1,rn]] 以单个元素开头，以转折元素（MetaNet元素）结尾，中间有单个元素、转折元素（MetaNet元素）
        4、[[r1,r2],r3,[r4,r5]...,rn]] 以转折元素（MetaNet元素）开头，以单个元素结尾，中间有单个元素、转折元素（MetaNet元素）
        5、[[r1,r2],r3,[r4,r5]...[rn-1,rn]] 以转折元素（MetaNet元素）开头，以转折元素（MetaNet元素）结尾，中间有单个元素、转折元素（MetaNet元素）
        6、[[r1,r2],[r3,r4]...[rn-1,rn]] 转折元素（MetaNet元素）顺序型。以转折元素（MetaNet元素）开头，以转折元素（MetaNet元素）结尾，中间全部都是转折元素（MetaNet元素）
    """

    __tablename__ = settings.db.tables.tbl_metaNet  # 所在表。与Flask统一
    primaryKey = copy.copy(TGraphEntity.primaryKey)  # 模型对应的主键
    primaryKey.extend(["id"])


    isChainedObject = True  # 是否是链式对象的标记（metaNet、Knowledge等）
    upperLimitation = None  # MetaNet 没有上一层对象

    lowerLimitation = LayerLimitation()
    lowerLimitation.update({ObjType.META_DATA: 1,
                            ObjType.KNOWLEDGE: -1})  # MetaNet只能有一个下层对象MetaData，一个同样结构的下层对象Knowledge，

    curEntityName = EntityName.MetaNetEntityName  # 当前T字形结构实体类的名称：元数据网、知识链，在两个类中赋值
    curEntityObjType = ObjType.META_NET  # 对象定义类型
    curItemObjType = ObjType.META_DATA
    curItemType = MetaData  # MetaData/RealObject
    curItemWordColumn = "mvalue"

    def __init__(self, start=None, end=None, id=None, stype=None, etype=None, weight=Character.Original_Link_Weight,
                 t_graph=None, t_chain=None, s_chain=None,  # m_chain=None,
                 createrid=None,
                 createtime=None, updatetime=None, lasttime=None,
                 status=200,  # 状态; 0-不可用(逻辑删除);200-正常;800-不可遗忘
                 memory=None):
        """

        :param start:
        :param end:
        :param mnid:
        :param stype:
        :param etype:
        :param weight:
        :param t_graph:
        :param t_chain:
        :param s_chain:
        :param createrid: 添加人; 格式：(user_id)中文名
        :param createrip: 添加人IP
        :param createtime: 添加时间;
        :param updatetime: 更新时间
        :param lasttime: 最近访问时间
        :param status: 状态; 0-不可用(逻辑删除);200-正常;800-不可遗忘
        :param memory:
        """
        super(MetaNet, self).__init__(start, end, id, stype, etype,
                                      weight,
                                      t_graph, t_chain, s_chain,
                                      createrid,
                                      createtime, updatetime, lasttime,
                                      status, memory)

        self.type = ObjType.META_NET  # 总是返回META_NET类型




    @classmethod
    def createMetaNetByMetaChain(cls,
                                 meta_chain,
                                 obj_nets=None,
                                 recordInDB=True,
                                 checkExist=True,
                                 memory=None):
        """
        根据MetaChain创建MetaNetItem
        :param meta_chain:[MetaData,[MetaData]]
        :return:
        """
        return cls._createByObjChain(meta_chain, obj_nets,
                                     recordInDB, checkExist, memory
                                     )

    @staticmethod
    def createMetaNetBySequnceWords(s_chain):
        """
        根据字符串列表创建元数据网络
        :param s_chain: 字符串列表
        :return:
        """
        meta_chain = MetaNet.createMetaChainByWordChain(s_chain)
        return MetaNet.createMetaNetByMetaChain(meta_chain)

    @staticmethod
    def createMetaChainByWordChain(s_chain, memory=None):
        """
        根据字符串列表创建元数据链
        :param s_chain: 字符串列表
        :return:
        """
        if s_chain is None or len(s_chain) < 2:
            return

        meta_chain = []

        for item in s_chain:
            if isinstance(item, str):
                word = item
                meta = MetaData(mvalue=word, memory=memory).create()
                meta_chain.append(meta)
            elif isinstance(item, list):
                child_meta_chain = MetaNet.createMetaChainByWordChain(item, memory=memory)
                meta_chain.append(child_meta_chain)

        return meta_chain

    def getMetaNetByStartAndEndWords(self, start_word, end_word):
        """
        根据两个字符串取得相应的MetaNet
        :param start_word:
        :param end_word:
        :return:
        """
        if start_word is None:
            raise Exception("必须提供start_word！")
        if end_word is None:
            raise Exception("必须提供end_word！")

        start = MetaData(mvalue=start_word, memory=self.MemoryCentral).create()
        end = MetaData(mvalue=end_word, memory=self.MemoryCentral).create()
        return MetaNet.getByStartAndEnd(start, end, memory=self.MemoryCentral)

    @staticmethod
    def getMetaNetsByStringValue(str_value, memory=None):
        """
        根据输入字符串取得元数据网（可能有多个：南京市长江大桥，南京市-长江大桥，南京-市长-江大桥，可能都对）。
        :param str_value:
        :param recordInMemory:
        :return:
        """
        if memory:
            meta_net=memory.getMetaNetByMNValueInMemory(mnvalue=str_value)
            if meta_net:
                return meta_net
        return MetaNet.getAllByConditionsInDB(memory=memory, mnvalue=str_value)


    def __repr__(self):
        if len(self._t_chain_words) > 0:
            return "{MetaNet:{mnid:%s,t_chain_words:%s}}" % (self.id, self._t_chain_words)
        if len(self.t_graph) > 0:
            return "{MetaNet:{mnid:%s,t_graph:%s}}" % (self.id, self.t_graph)
        else:
            return "{MetaNet:{mnid:%s}}" % (self.id)
