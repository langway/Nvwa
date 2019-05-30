#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

import copy
from loongtian.util.log import logger

from loongtian.nvwa import settings
from loongtian.nvwa.models.baseEntity import BaseEntity, LayerLimitation
from loongtian.nvwa.models.enum import ObjType
from loongtian.nvwa.models.metaData import MetaData
from loongtian.util.helper import jsonplus
from loongtian.nvwa.organs.character import Character


class MetaNet(BaseEntity):
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
    isdel 逻辑删除标记
    1、 是一个T字型结构的由metaData、MetaNetItem的Id组成的数组(嵌套代表一条MetaNet)。格式为：[mid,(kid,[t_graph])]
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
    __databasename__ = settings.db.db_nvwa  # 所在数据库。
    __tablename__ = settings.db.tables.tbl_metaNet # 所在表。与Flask统一
    primaryKey = copy.copy(BaseEntity.primaryKey)  # 模型对应的主键
    primaryKey.extend(["mnid"])
    columns = copy.copy(BaseEntity.columns)  # 模型对应的非主键的全部字段
    columns.extend(["startid", "stype", "endid", "etype", "weight",
                    "t_graph", "t_chain", "s_chain", "mnvalue"])
    jsonColumns = copy.copy(
        BaseEntity.jsonColumns)  # 需要用json解析的字段，一般都为text字段，创建(create)、更新(update)，需要解析为json，读取(retrive)时需要从json解析为对象
    jsonColumns.extend(["t_graph", "t_chain", "s_chain"])
    retrieveColumns = copy.copy(BaseEntity.retrieveColumns)  # 查询时需要使用的字段
    retrieveColumns.extend(["startid", "endid"])

    isChainedObject = True  # 是否是链式对象的标记（metaNet、Knowledge等）
    upperLimitation = None  # MetaNet 没有上一层对象

    lowerLimitation = LayerLimitation()
    lowerLimitation.update({ObjType.META_DATA: 1,
                            ObjType.KNOWLEDGE: 1})  # MetaNet只能有一个下层对象MetaData，一个同样结构的下层对象Knowledge，

    def __init__(self, start=None, end=None, mnid=None, stype=None, etype=None, weight=Character.Original_Link_Weight,
                 t_graph=None, t_chain=None, s_chain=None,  # m_chain=None,
                 createrid='',
                 createtime=None, updatetime=None, lasttime=None,
                 status=200, # 状态; 0-不可用(逻辑删除);200-正常;800-不可遗忘
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

        super(MetaNet, self).__init__(mnid,
                                      createrid,
                                      createtime, updatetime, lasttime,
                                      status,memory=memory)
        if mnid is None:
            self.mnid = self.id
        else:
            self.mnid = mnid
            self._id = mnid


        if start:
            if isinstance(start, str) or isinstance(start, unicode):
                self.startid = start
            elif isinstance(start, BaseEntity):
                self.startid = start.id
                self.stype = start.getType()
        if stype:
            if isinstance(stype, int) or isinstance(stype, str) or isinstance(stype, unicode):
                self.stype = stype
            elif isinstance(start, BaseEntity):
                self.stype = start.getType()

        if end:
            if isinstance(end, str) or isinstance(end, unicode):
                self.endid = end
            elif isinstance(end, BaseEntity):
                self.endid = end.id
                self.etype = end.getType()
        if etype:
            if isinstance(etype, int) or isinstance(etype, str) or isinstance(etype, unicode):
                self.etype = etype
            elif isinstance(end, BaseEntity):
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
            t_chain = []
        self.t_chain = t_chain
        if not s_chain:
            s_chain = []
        self.s_chain = s_chain
        # if not m_chain:
        #     m_chain=[]
        # self.m_chain=m_chain

        # # 实际取得的metaData对象，当前元数据网的元数据链
        self._t_chain_items = []
        self._s_chain_items = []

        # # 实际取得的metaData对象的mvalue。当前元数据网的字符串列表（嵌套代表一条记录）
        self._t_chain_words = []
        self._s_chain_words = []

        # 是否已经取得了chain的标记
        self._chainItemsProceed = False

        self.mnvalue = None  # 媒体值，是元数据mvalue拼合的结果（用来供字符串快速查询）
        # 当type为文字时，保存的是文字字符串
        # 当type为声音或图像时，保存的是声音或图像的URI或对象地址

        # 所有的后链列表
        self._forwards = {}
        # 所有的前链列表
        self._backwards = {}

        self._ChainItems = {}  # 当前MetaNetItem的链包含的所有MetaNetItem、MetaData，格式为：{mnid/mid:MetaNet/MetaData}

        # 单一链的前、后链对象
        self._StartItem = None
        self._EndItem = None

        self._head = None
        self._tail = None

        # 2018-12-06:所有上下层对象一律在Layers中处理
        # # 元数据网相关连的下一层元数据（只能有一个）。
        # # 例如：m:中国-m:人民-m:解放军，关联的元数据就是“m:中国人民解放军”
        # self._lower_meta = None
        # # 元数据网相关的下一层知识链（只能有一个）。
        # # [m:我,m:知道,[[m:中国,m:人民,m:解放军],m:是,[m:最棒,m:的]]]相关的知识网：
        # # [r:我,r:知道,[[r:中国,r:人民,r:解放军],r:是,[r:最棒,r:的]]]
        # self._lower_knowledge = None

        # if __debug__:
        #     from loongtian.util.db.sequence import Sequence
        #     self.mnid = "MN%030d" % Sequence.nextMetaNet()
        #     self.isdel = True

    def getStartItem(self):
        """
        根据startid取得开始的对象（可能是metaData，也可能是metaNetItem）
        :return:
        """
        if self.startid is None:
            return None
        if self._StartItem:
            return self._StartItem
        # 根据前链的类型取得对应的对象（包括：MetaData、MetaNet）
        if ObjType.isMetaData(self.stype):
            self._StartItem = MetaData.getOne(mid=self.startid)
        elif ObjType.isMetaNet(self.stype):
            self._StartItem = MetaNet.getOne(mnid=self.startid)
        else:
            raise Exception("前链类型错误：{%d:%s}。" % (self.stype, ObjType.getTypeNames(self.stype)))

        if not self._StartItem:
            raise Exception(
                "未能取得前链对象：{%s:%s,%d:%s}。" % ("Id", self.startid, self.stype, ObjType.getTypeNames(self.stype)))
        return self._StartItem

    def getEndItem(self):
        """
        根据endid取得开始的对象（可能是metaData，也可能是metaNetItem）
        :return:
        """
        if self.endid is None:
            return None
        if self._EndItem:
            return self._EndItem
        # 根据后链的类型取得对应的对象（包括：MetaData、MetaNet）
        if ObjType.isMetaData(self.etype):
            self._EndItem = MetaData.getOne(mid=self.endid)
        elif ObjType.isMetaNet(self.etype):
            self._EndItem = MetaNet.getOne(mnid=self.endid)
        else:
            raise Exception("后链类型错误：{%d:%s}。" % (self.etype, ObjType.getTypeNames(self.etype)))

        if not self._EndItem:
            raise Exception(
                "未能取得后链对象：{%s:%s,%d:%s}。" % ("Id", self.endid, self.etype, ObjType.getTypeNames(self.etype)))
        return self._EndItem

    def getRelatedMeta(self):
        """
        取得元数据网相关连的元数据，例如：中国-人民-解放军，关联的元数据就是“中国人民解放军”
        :return:
        """
        return self.Layers.getLowerEntitiesByType(ObjType.META_DATA)

    def getRelatedKnowledge(self):
        """
        取得元数据网相关连的元数据，例如：中国-人民-解放军，关联的元数据就是“中国人民解放军”
        :return:
        """
        return self.Layers.getLowerEntitiesByType(ObjType.KNOWLEDGE)

    @staticmethod
    def createMetaNetByStartEnd(start, end, mnid=None):
        """
        创建MetaNetItem
        :param start:可以是MetaData、MetaNetItem或[sid,stype]\(sid,stype)
        :param end:可以是MetaData、MetaNetItem或[eid,etype]\(eid,etype)
        :return:
        """
        if isinstance(start, MetaData):
            sid = start.mid
            stype = ObjType.META_DATA
        elif isinstance(start, MetaNet):
            sid = start.mnid
            stype = ObjType.META_NET
        elif isinstance(start, list) or isinstance(start, tuple):
            sid = start[0]
            stype = start[1]
        else:
            raise Exception("start对象应为MetaData或MetaNetItem或[sid,stype]\(sid,stype)，当前类型错误：" + type(start))

        if isinstance(end, MetaData):
            eid = end.mid
            etype = ObjType.META_DATA
        elif isinstance(end, MetaNet):
            eid = end.mnid
            etype = ObjType.META_NET
        elif isinstance(end, list) or isinstance(end, tuple):
            eid = end[0]
            etype = end[1]
        else:
            raise Exception("end对象应为MetaData或MetaNetItem或[sid,stype]\(sid,stype)，当前类型错误：" + type(start))

        mni = MetaNet(start=sid, stype=stype, end=eid, etype=etype, mnid=mnid)

        retrived = mni.getByColumnsInDB()
        if not retrived:
            mni._StartItem = start
            mni._EndItem = end
            mni.status = 200  # 确保未逻辑删除
            mni.getChainItems()
            mni.create(checkExist=False)
        else:
            mni = retrived
            if mni.isdel:  # 如果逻辑删除，恢复之
                mni.restore()

            mni._StartItem = start
            mni._EndItem = end
            mni.getChainItems()

        return mni

    @staticmethod
    def createMetaNetByMetaChain(meta_chain, meta_nets=None):
        """
        根据MetaChain创建MetaNetItem
        :param meta_chain:[MetaData,[MetaData]]
        :return:
        """
        if meta_chain is None or len(meta_chain) < 2:
            return None
        cur_mni = None
        if meta_nets is None:
            meta_nets = []
        i = 0
        while i < len(meta_chain):  # 确保后面至少有一条
            cur_meta = meta_chain[i]  # 第一个
            if isinstance(cur_meta, list):  # 如果当前meta是list，创建其子MetaNetItem
                if len(cur_meta) > 0:
                    cur_meta = MetaNet.createMetaNetByMetaChain(cur_meta, meta_nets)
                else:
                    i += 1
                    continue

            if cur_mni:
                cur_mni = MetaNet.createMetaNetByStartEnd(cur_mni, cur_meta)
                meta_nets.append(cur_mni)
                i += 1
                continue

            next_meta = None
            if i < len(meta_chain) - 1:  # # 确保后面至少有第二个
                next_meta = meta_chain[i + 1]
                if isinstance(next_meta, list):  # 如果下一meta是list，创建其子MetaNetItem
                    if len(next_meta) > 0:
                        next_meta = MetaNet.createMetaNetByMetaChain(next_meta, meta_nets)
                    else:
                        i += 1
                        continue

            if next_meta:
                cur_mni = MetaNet.createMetaNetByStartEnd(cur_meta, next_meta)
                meta_nets.append(cur_mni)
                i += 2

        return cur_mni

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
    def createMetaChainByWordChain(s_chain,memory=None):
        """
        根据字符串列表创建元数据链
        :param s_chain: 字符串列表
        :return:
        """
        if s_chain is None or len(s_chain) < 2:
            return

        meta_chain = []

        for item in s_chain:
            if isinstance(item, str) or isinstance(item, unicode):
                word = item
                meta = MetaData(mvalue=word,memory=memory).create()
                meta_chain.append(meta)
            elif isinstance(item, list):
                child_meta_chain = MetaNet.createMetaChainByWordChain(item,memory=memory)
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
        return MetaNet.getMetaNetByStartAndEnd(start, end, memory=self.MemoryCentral)

    @staticmethod
    def getMetaNetByMetaChain(meta_chain, meta_nets=None, unproceed=None):
        """
        根据metaChain取得MetaNet（完全匹配）
        :param metaChain:[metaData,[metaData,metaData]]
        :return:
        """
        cur_mni = None
        if meta_nets is None:
            meta_nets = []

        if unproceed is None:
            unproceed = []

        i = 0
        while i < len(meta_chain):  # 确保后面至少有一条
            cur_meta = meta_chain[i]  # 第一个
            if isinstance(cur_meta, list):
                if len(cur_meta) > 0:  # 如果当前meta是list，查询其子MetaNetItem
                    cur_meta = MetaNet.getMetaNetByMetaChain(cur_meta, meta_nets, unproceed)
                    if not cur_meta:  # 破解查询结构不一致
                        cur_meta = meta_chain[i][0]
            # 如果能够与前链“构成”，继续下一个
            if cur_mni:
                cur_temp_mni = MetaNet.getMetaNetByStartAndEnd(cur_mni, cur_meta)
                if cur_temp_mni:
                    cur_mni = cur_temp_mni
                    meta_nets.append(cur_mni)
                    i += 1
                    continue
            # 不能与前链“构成”，查看与后一个元素是否能够“构成”
            next_meta = None
            if i < len(meta_chain) - 1:  # # 确保后面至少有第二个
                next_meta = meta_chain[i + 1]
                if isinstance(next_meta, list):  # 如果下一meta是list，查询其子MetaNetItem
                    next_meta = MetaNet.getMetaNetByMetaChain(next_meta, meta_nets, unproceed)
            if next_meta:
                cur_temp_mni = MetaNet.getMetaNetByStartAndEnd(cur_meta, next_meta)
                if cur_temp_mni:
                    test_mni = None
                    if len(meta_chain) == 2:  # 如果没有前一个元素、后一个元素，说明是唯一的两个
                        test_mni = cur_temp_mni
                    if not test_mni and cur_mni:
                        # 这里需要考虑与cur_mni、前元素、后元素是否能够构成一条链，如果不构成，也要抛弃
                        test_mni = MetaNet.getMetaNetByStartAndEnd(cur_mni, cur_temp_mni)
                    if not test_mni and i - 1 >= 0:
                        last_meta = meta_chain[i - 1]  # 前一个元素
                        if last_meta:
                            if isinstance(last_meta, list):
                                test_mni = MetaNet.getMetaNetByMetaChain([last_meta, cur_temp_mni], meta_nets,
                                                                         unproceed)
                            else:
                                test_mni = MetaNet.getMetaNetByStartAndEnd(last_meta, cur_temp_mni)
                    if not test_mni and i < len(meta_chain) - 2:
                        next_next_meta = meta_chain[i + 2]  # 后一个元素
                        if next_next_meta:
                            if isinstance(next_next_meta, list):
                                test_mni = MetaNet.getMetaNetByMetaChain([cur_temp_mni, next_next_meta], meta_nets,
                                                                         unproceed)
                            else:
                                test_mni = MetaNet.getMetaNetByStartAndEnd(cur_temp_mni, next_next_meta)

                    if not test_mni:  # 仍未找到，当前cur_temp_mni没有与前后产生构成，暂时放到待处理列表
                        unproceed.insert(0, cur_temp_mni)
                        i += 2
                        continue

                    # 如果不是最后一个，把cur_temp_mni赋值给cur_mni
                    # 反之，如果是最后一个，把cur_temp_mni与cur_mni粘连
                    if cur_mni:
                        cur_last_mni = MetaNet.getMetaNetByStartAndEnd(cur_mni, cur_temp_mni)
                        if cur_last_mni:
                            cur_mni = cur_last_mni
                        else:
                            cur_mni = cur_temp_mni
                    else:
                        cur_mni = cur_temp_mni

                    # 如果前面有未连成链的，往前附着，连成链
                    cur_unproceed_mni = None
                    if len(unproceed) > 0:  # 如果前面有未连成链的，往前附着，连成链
                        cur_unproceed_mni = cur_mni
                        proceed = []
                        for j in range(len(unproceed)):  # 因为是线性输入，所以进行倒序处理
                            try:
                                cur_unproceed_mni = MetaNet.getMetaNetByStartAndEnd(unproceed[j], cur_unproceed_mni)
                                if cur_unproceed_mni:
                                    # 继续往前粘连
                                    last_unproceed_mni = cur_unproceed_mni
                                    last_unproceed_mnis = []
                                    for meta_net in meta_nets:
                                        last_unproceed_mni = MetaNet.getMetaNetByStartAndEnd(meta_net,
                                                                                             last_unproceed_mni)
                                        if last_unproceed_mni:
                                            last_unproceed_mnis.append(last_unproceed_mni)

                                    meta_nets.append(cur_unproceed_mni)
                                    if len(last_unproceed_mnis) > 0:
                                        meta_nets.extend(last_unproceed_mnis)
                                        cur_unproceed_mni = last_unproceed_mnis[-1]

                                    proceed.append(j)

                            except Exception as e:  # do nothing
                                logger.info(e)
                                pass
                        # 去掉已经处理过的
                        if len(proceed) > 0:
                            temp_unproceed = []
                            for i in range(len(unproceed)):
                                if not proceed.__contains__(i):
                                    temp_unproceed.append(unproceed[i])
                            unproceed = temp_unproceed

                    meta_nets.append(cur_mni)
                    i += 2
                    if cur_unproceed_mni:
                        cur_mni = cur_unproceed_mni
                        i += 2
                        # meta_nets.append(cur_mni)
                else:  # 仍未找到，当前cur_meta没有与前后产生构成，暂时放到待处理列表
                    unproceed.insert(0, cur_meta)
                    i += 1
            else:
                i += 1

        return cur_mni

    @staticmethod
    def getMetaNetLikeMetaChain(metaChain):
        """
        根据metaChain取得MetaNet（不完全匹配，使用s_chain进行近似匹配，根据匹配数量、匹配对象的weight进行排序）
        :param metaChain:[metaData,[metaData,metaData]]
        :return:
        """
        # todo 目前还是使用全文匹配，未来应该使用近似匹配
        valueChian, is_sequence = MetaNet.getValueChainByMetaChain(metaChain)
        like = jsonplus.dumps(valueChian)
        if is_sequence:
            mni = MetaNet.getAllLikeByInDB(s_chain=like)
        else:
            mni = MetaNet.getAllLikeByInDB(t_chain=like)

        if mni:
            mni.getChainItems()
        return mni

    @staticmethod
    def getValueChainByMetaChain(metaChain):
        """
        取得MetaChain的value列表
        :param metaChain:
        :return:
        """
        valueChian = []
        is_sequence = True
        for meta in metaChain:
            if isinstance(meta, list):
                valueChian.append(MetaNet.getValueChainByMetaChain(meta))
                is_sequence = False
            elif isinstance(meta, MetaData):
                valueChian.append(meta.mid)
            elif isinstance(meta, MetaNet):
                valueChian.append(meta.mnid)

        return valueChian, is_sequence

    def getChainItems(self):
        """
        不断递归取得当前链的所有StartItem、EndItem对象（MetaNet、MetaData）
        :return:
        """
        if self._chainItemsProceed == True:
            return

        self.getStartItem()
        self.getEndItem()
        _start_proceed = False
        _end_proceed = False

        _start_is_meta = False
        _end_is_meta = False

        # 查找
        while True:
            if isinstance(self._StartItem, MetaNet):
                self._ChainItems[self._StartItem.mnid] = self._StartItem
                self._StartItem.getChainItems()  # ,original=original)
                if self._StartItem._head:  # 取得链的头（是一个MetaNetItem）
                    self._head = self._StartItem._head
                _start_proceed = True
            elif isinstance(self._StartItem, MetaData):
                self._ChainItems[self._StartItem.mid] = self._StartItem
                _start_proceed = True
                _start_is_meta = True

            if isinstance(self._EndItem, MetaNet):
                self._ChainItems[self._EndItem.mnid] = self._EndItem

                self._EndItem.getChainItems()  # ,original=original)
                if self._EndItem._tail:  # 取得链的尾（是一个MetaNetItem）
                    self._tail = self._EndItem._tail
                _end_proceed = True
            elif isinstance(self._EndItem, MetaData):
                self._ChainItems[self._EndItem.mid] = self._EndItem
                _end_proceed = True
                _end_is_meta = True

            if _start_is_meta and _end_is_meta:
                self._head = self
                self._tail = self

            # 处理t_graph、s_chain、t_chain、_word_chain等
            self.getGraph()

            if _start_proceed and _end_proceed:  # 如果start和end都处理过了，停机
                break
        # 标记已经取得了chain
        self._chainItemsProceed = True

    def getSequenceComponents(self, keepEndKnowledge=False):
        """
        取得一个知识链的构成元素（有顺序）
        :param keepEndKnowledge: 如果 end以Knowledge结尾，是否将endItem的Knowledge保留，如果不保留，意味着嵌套集合列表，例如：牛-有-腿-Knowledge(我-知道)，还原为：[[牛,有,腿],[我-知道]],否则将添加Knowledge
        :return:
        """
        raise NotImplementedError

    def getGraph(self):
        """
        处理t_graph、s_chain、t_chain、_word_chain等
        :return:
        """
        self.t_graph = []
        self.t_chain = []
        self.s_chain = []
        # self.m_chain=[]

        self._t_chain_items = []
        self._s_chain_items = []

        self._t_chain_words = []
        self._s_chain_words = []

        if isinstance(self._StartItem, MetaNet):
            if isinstance(self._EndItem, MetaNet):
                # 在前逐元素插入
                self.s_chain = self._StartItem.s_chain + self.s_chain + self._EndItem.s_chain
                self.t_graph.insert(0, (self.mnid, [self._StartItem.t_graph, self._EndItem.t_graph]))
                self.t_chain.insert(0, [self._StartItem.t_chain, self._EndItem.t_chain])

                # 实际取得的metaData对象
                self._t_chain_items.insert(0, [self._StartItem._t_chain_items, self._EndItem._t_chain_items])
                self._s_chain_items = self._StartItem._s_chain_items + self._s_chain_items + self._EndItem._s_chain_items

                # 实际取得的metaData对象的mvalue
                self._t_chain_words.insert(0, [self._StartItem._t_chain_words, self._EndItem._t_chain_words])
                self._s_chain_words = self._StartItem._s_chain_words + self._s_chain_words + self._EndItem._s_chain_words

            elif isinstance(self._EndItem, MetaData):
                # 在前逐元素插入
                self.s_chain.extend(self._StartItem.s_chain)
                self.s_chain.append(self._EndItem.mid)
                self.t_graph.insert(0, (self.mnid, [self._StartItem.t_graph, self._EndItem.mid]))
                self.t_chain.insert(0, [self._StartItem.t_chain, self._EndItem.mid])

                # 实际取得的metaData对象
                self._t_chain_items.insert(0, [self._StartItem._t_chain_items, self._EndItem])
                self._s_chain_items.extend(self._StartItem._s_chain_items)
                self._s_chain_items.append(self._EndItem)

                # 实际取得的metaData对象的mvalue
                self._t_chain_words.insert(0, [self._StartItem._t_chain_words, self._EndItem.mvalue])
                self._s_chain_words.extend(self._StartItem._s_chain_words)
                self._s_chain_words.append(self._EndItem.mvalue)

        elif isinstance(self._StartItem, MetaData):
            if isinstance(self._EndItem, MetaNet):
                # 在前逐元素插入
                self.s_chain.append(self._StartItem.mid)
                self.s_chain += self._EndItem.s_chain
                self.t_graph.insert(0, (self.mnid, [self._StartItem.mid, self._EndItem.t_graph]))
                self.t_chain.insert(0, [self._StartItem.mid, self._EndItem.t_chain])

                # 实际取得的metaData对象
                self._s_chain_items.append(self._StartItem)
                self._s_chain_items += self._EndItem._s_chain_items
                self._t_chain_items.insert(0, [self._StartItem, self._EndItem._t_chain_items])

                # 实际取得的metaData对象的mvalue
                self._t_chain_words.insert(0, [self._StartItem.mvalue, self._EndItem._t_chain_words])
                self._s_chain_words.append(self._StartItem.mvalue)
                self._s_chain_words += self._EndItem._s_chain_words

            else:  # 都是metaData
                self.s_chain.extend([self._StartItem.mid, self._EndItem.mid])
                self.t_graph.extend([(self.mnid, [self._StartItem.mid, self._EndItem.mid])])
                self.t_chain.extend([self._StartItem.mid, self._EndItem.mid])
                # self.m_chain.extend([self.mnid])

                # 实际取得的metaData对象
                self._s_chain_items.extend([self._StartItem, self._EndItem])
                self._t_chain_items.extend([self._StartItem, self._EndItem])

                # 实际取得的metaData对象的mvalue
                self._t_chain_words.extend([self._StartItem.mvalue, self._EndItem.mvalue])
                self._s_chain_words.extend([self._StartItem.mvalue, self._EndItem.mvalue])

        if len(self.t_chain) == 1:
            self.t_chain = self.t_chain[0]
        if len(self._t_chain_items) == 1:
            self._t_chain_items = self._t_chain_items[0]
        if len(self._t_chain_words) == 1:
            self._t_chain_words = self._t_chain_words[0]

    def getAllForwardsInDB(self, lazy_get=True):
        """
        取得以当前MetaNetItem的mnid为startid的所有后链（后链，即被域对象，以当前知识链为开始）。
        :param lazy_get 是否等需要的时候再取得对应的对象（以getChainItems填充）
        :return: 后链列表[MetaNet]
        """
        if len(self._forwards) > 0:
            return self._forwards
        mnis = MetaNet.getMetaNetsByStartInDB(self.mnid, lazy_get)
        if mnis:
            for mni in mnis:
                self._forwards[mni.mnid] = mni
        return self._forwards

    def getAllBackwardsInDB(self, lazy_get=True):
        """
        取得以当前MetaNetItem的mnid为endid的所有前链（前链，即域对象、域或标签，以当前知识链为结束）。
        eg:
            self = [猪能说话]
            return [[西游记], [中国[上古[史诗神话]]], [猪八戒], [小猪佩奇]...]
        :param lazy_get 是否等需要的时候再取得对应的对象（以getChainItems填充）
        :return: 前链列表[MetaNet]
        """
        if len(self._backwards) > 0:
            return self._backwards

        mnis = MetaNet.getMetaNetsByEndInDB(self.mnid, lazy_get)
        if mnis:
            for mni in mnis:
                self._backwards[mni.mnid] = mni
        return self._backwards

    @staticmethod
    def getMetaNetsByStartInDB(start, lazy_get=True,memory=None):
        """
        查找以start开头的所有知识链
        :param start: MetaData、MetaNet、mnid或是mid(BaseEntity及其继承类，或 Id字符串)
        :param lazy_get 是否等需要的时候再取得对应的对象（以getChainItems填充）
        :return: [MetaNet]
        """
        if not start:
            raise Exception("start(%s)不能为空！" % start)

        startid = MetaNet._getId(start)
        mnis = MetaNet.getAllByConditionsInDB(memory=memory,startid=startid)

        if not lazy_get and mnis:
            if isinstance(mnis, list):
                for mni in mnis:
                    mni.getChainItems()
            else:
                mnis.getChainItems()

        return mnis

    @staticmethod
    def getMetaNetsByEndInDB(end, lazy_get=True,memory=None):
        """
        查找以end结尾的所有知识链
        :rawParam end: MetaData、MetaNet、mnid或是mid(BaseEntity及其继承类，或 Id字符串)
        :param lazy_get 是否等需要的时候再取得对应的对象（以getChainItems填充）
        :return: [MetaNet]
        """
        if not end:
            raise Exception("end(%s)不能为空！" % end)

        endid = MetaNet._getId(end)

        mnis = MetaNet.getAllByConditionsInDB(memory=memory,endid=endid)

        if not lazy_get and mnis:
            if isinstance(mnis, list):
                for mni in mnis:
                    mni.getChainItems()
            else:
                mnis.getChainItems()

        return mnis

    @staticmethod
    def getMetaNetByStartAndEnd(start, end, lazy_get=False,memory=None):
        """
        在内存或数据库中查找以start开头并且以end结尾的元数据链(只能有一条)
        :param start: MetaData、MetaNet、mnid或是mid(BaseEntity及其继承类，或 Id字符串)
        :param end: MetaData、MetaNet、mnid或是mid(BaseEntity及其继承类，或 Id字符串)
        :param lazy_get 是否等需要的时候再取得对应的对象（以getChainItems填充）
        :return: MetaNet
        """
        # 首先在内存中查找
        mni = MetaNet.getMetaNetByStartAndEndInMemory(start, end,memory=memory)
        if mni:
            return mni
        # 内存没找到，在数据库中查找
        mni = MetaNet.getMetaNetByStartAndEndInDB(start, end, lazy_get,memory=memory)
        return mni

    @staticmethod
    def getMetaNetByStartAndEndInMemory(start, end,memory=None):
        """
        [内存操作]查找以start开头并且以end结尾的元数据链(只能有一条)
        :param start: MetaData、MetaNet、mnid或是mid(BaseEntity及其继承类，或 Id字符串)
        :param end: MetaData、MetaNet、mnid或是mid(BaseEntity及其继承类，或 Id字符串)
        :return: MetaNet
        """
        if memory and memory.MetaNetDict:
            if not start:
                raise Exception("start(%s)不能为空！" % start)
            if not end:
                raise Exception("end(%s)不能为空！" % end)

            startid = MetaNet._getId(start)
            endid = MetaNet._getId(end)
            return memory.MetaNetDict.getByKeys(startid, endid)

    @staticmethod
    def getMetaNetByStartAndEndInDB(start, end, lazy_get=True,memory=None):
        """
        [数据库操作]查找以start开头并且以end结尾的元数据链(只能有一条)
        :param start: MetaData、MetaNet、mnid或是mid(BaseEntity及其继承类，或 Id字符串)
        :param end: MetaData、MetaNet、mnid或是mid(BaseEntity及其继承类，或 Id字符串)
        :param lazy_get 是否等需要的时候再取得对应的对象（以getChainItems填充）
        :return: MetaNet
        """
        if not start:
            raise Exception("start(%s)不能为空！" % start)
        if not end:
            raise Exception("end(%s)不能为空！" % end)

        startid = MetaNet._getId(start)
        endid = MetaNet._getId(end)
        mnis = MetaNet.getAllByConditionsInDB(memory=memory,startid=startid, endid=endid)
        if mnis is None:
            return None
        if isinstance(mnis, list):
            if mnis is None or len(mnis) == 0:
                return None
            if len(mnis) > 1:
                raise Exception("以start开头并且以end结尾的知识链只能有一条,start:%s,start type:%s,end:%s,end type:%s" % (
                    startid, str(type(start)), endid, str(type(end))))

            mni = mnis[0]
        else:
            mni = mnis

        mni._StartItem = start
        mni._EndItem = end

        if not lazy_get:
            mni.getChainItems()

        # # 添加到内存以便后续操作(已经在memory中进行了操作)
        # if self.MemoryCentral and self.MemoryCentral.MetaNetStartAndEndDict:
        #     self.MemoryCentral.MetaNetStartAndEndDict[startid][endid]=mni

        return mni

    @staticmethod
    def getMetaNetsByStringValue(str_value, memory=None):
        """
        根据输入字符串取得元数据网（可能有多个：南京市长江大桥，南京市-长江大桥，南京-市长-江大桥，可能都对）。
        :param str_value:
        :param recordInMemory:
        :return:
        """
        return MetaNet.getAllByConditionsInDB(memory=memory, mnvalue=str_value)

    @staticmethod
    def deleteByStart(start):
        """
        根据开始对象，逻辑删除所有MetaNetItem
        :param start:BaseEntity及其继承类，或 Id字符串
        :return:
        """
        if start is None:
            raise Exception("无法逻辑删除所有MetaNetItem，start is None！")
        # startid=MetaNet._getId(start)
        mnis = MetaNet.getMetaNetsByStartInDB(start)
        if isinstance(mnis, list):
            for mni in mnis:
                mni.delete()
        elif isinstance(mnis, MetaNet):
            mnis.delete()

        # MetaNet.updateAll(wheres = {"startid":startid},isdel=True)

    @staticmethod
    def deleteByEnd(end):
        """
        根据结尾对象，逻辑删除所有MetaNetItem
        :param end:BaseEntity及其继承类，或 Id字符串
        :return:
        """
        if end is None:
            raise Exception("无法逻辑删除所有MetaNetItem，end is None！")
        # endid=MetaNet._getId(end)
        mnis = MetaNet.getMetaNetsByEndInDB(end)
        if isinstance(mnis, list):
            for mni in mnis:
                mni.delete()
        elif isinstance(mnis, MetaNet):
            mnis.delete()

        # MetaNet.updateAll(wheres = {"endid":endid},isdel=True)

    def deleteAllBackwardsInDB(self):
        """
        删除以当前MetaNetItem的mnid为endid的所有前链（前链，即域对象、域或标签，以当前知识链为结束）。
        :return:
        """
        backwards = self.getAllBackwardsInDB()
        if backwards:
            for _id, backward in backwards:
                backward.delete()

    def deleteAllForwardsInDB(self):
        """
        删除以当前MetaNetItem的mnid为startid的所有后链。
        :return:
        """
        forwards = self.getAllForwardsInDB()
        if forwards:
            for _id, forward in forwards:
                forward.delete()

    @staticmethod
    def deleteByStartAndEnd(start, end):
        """
        根据start,end取得MetaNet，进行逻辑删除。
        :param start: MetaData、MetaNet、mnid或是mid(BaseEntity及其继承类，或 Id字符串)
        :param end:  MetaData、MetaNet、mnid或是mid(BaseEntity及其继承类，或 Id字符串)
        :return:
        """
        mni = MetaNet.getMetaNetByStartAndEnd(start, end)
        if mni:
            mni.delete()

    @staticmethod
    def deleteByMetaChain(metaChain, deleteAllChain=False):
        """
        根据metaChain删除MetaNet
        :param metaChain:[metaData,[metaData,metaData]]
        :param deleteAllChain 是否删除全链
        :return:
        """
        if len(metaChain) < 2:
            return
        meta_nets = []
        mni = MetaNet.getMetaNetByMetaChain(metaChain, meta_nets)
        if deleteAllChain:
            for meta_net in meta_nets:
                meta_net.delete()
        elif mni:
            mni.delete()
        return mni
        # start = metaChain[0]
        # for i in range(1, len(metaChain)):
        #     if isinstance(start,list):
        #         start=MetaNet.deleteByMetaChain(start)
        #     if start is None:
        #         return None
        #
        #     end = metaChain[i]
        #     if isinstance(end,list):
        #         end=MetaNet.deleteByMetaChain(end)
        #
        #     start = MetaNet.deleteByStartAndEnd(start,end)
        #     if start is None:
        #         return None
        #
        # return start

    @staticmethod
    def _physicalDeleteByStart(start):
        """
        根据开始对象，物理删除所有MetaNetItem
        :param start:BaseEntity及其继承类，或 Id字符串
        :return:
        """
        if start is None:
            raise Exception("无法物理删除所有MetaNetItem，start is None！")
        # startid=MetaNet._getId(start)
        mnis = MetaNet.getMetaNetsByStartInDB(start)
        if isinstance(mnis, list):
            for mni in mnis:
                mni._physicalDelete()
        elif isinstance(mnis, MetaNet):
            mnis._physicalDelete()

        # MetaNet.updateAll(wheres = {"startid":startid},isdel=True)

    @staticmethod
    def _physicalDeleteByEnd(end):
        """
        根据结尾对象，物理删除所有MetaNetItem
        :param end:BaseEntity及其继承类，或 Id字符串
        :return:
        """
        if end is None:
            raise Exception("无法物理删除所有MetaNetItem，end is None！")
        # endid=MetaNet._getId(end)
        mnis = MetaNet.getMetaNetsByEndInDB(end)
        if isinstance(mnis, list):
            for mni in mnis:
                mni._physicalDelete()
        elif isinstance(mnis, MetaNet):
            mnis._physicalDelete()

    def _physicalDeleteAllBackwardsInDB(self):
        """
        物理删除以当前MetaNetItem的mnid为endid的所有前链（前链，即域对象、域或标签，以当前知识链为结束）。
        :return:
        """
        backwards = self.getAllBackwardsInDB()
        if backwards:
            for _id, backward in backwards:
                backward._physicalDelete()

    def _physicalDeleteAllForwardsInDB(self):
        """
        物理删除以当前MetaNetItem的mnid为startid的所有后链。
        :return:
        """
        forwards = self.getAllForwardsInDB()
        if forwards:
            for _id, forward in forwards:
                forward._physicalDelete()

    @staticmethod
    def _physicalDeleteByStartAndEnd(start, end):
        """
        根据start,end取得MetaNet，进行物理删除。
        :param start: MetaData、MetaNet、mnid或是mid(BaseEntity及其继承类，或 Id字符串)
        :param end:  MetaData、MetaNet、mnid或是mid(BaseEntity及其继承类，或 Id字符串)
        :return:
        """
        mni = MetaNet.getMetaNetByStartAndEnd(start, end)
        if mni:
            mni._physicalDelete()

    @staticmethod
    def _physicalDeleteByMetaChain(metaChain, deleteAllChain=False):
        """
        根据metaChain物理删除MetaNet
        :param metaChain:[metaData,[metaData,metaData]]
        :param deleteAllChain 是否删除全链
        :return:
        """
        if len(metaChain) < 2:
            return
        meta_nets = []
        mni = MetaNet.getMetaNetByMetaChain(metaChain, meta_nets)
        if deleteAllChain:
            for meta_net in meta_nets:
                meta_net._physicalDelete()
        elif mni:
            mni._physicalDelete()

    def zig_to(self, to_meta_chain):
        if not self.t_chain:
            self.getChainItems()

        return self.zig(self.t_chain, to_meta_chain)

    @staticmethod
    def zig(from_meta_chain, to_meta_chain):
        """
        根据第二个对第一个进行折叠。
        例如：将[我,知道,中国,人民,解放军] 折叠为：[[我,知道],[中国,[人民,解放军]]]
        :param from_meta_chain:
        :param to_meta_chain:
        :return:
        """
        raise NotImplementedError

    def getType(self):
        """
        获得类型
        :return: 总是返回IdTypeEnum.MetaNet类型。
        """
        return ObjType.META_NET

    def __repr__(self):
        if len(self._t_chain_words) > 0:
            return "{MetaNet:{mnid:%s,t_chain_words:%s}}" % (self.mnid, self._t_chain_words)
        if len(self.t_graph) > 0:
            return "{MetaNet:{mnid:%s,t_graph:%s}}" % (self.mnid, self.t_graph)
        else:
            return "{MetaNet:{mnid:%s}}" % (self.mnid)
