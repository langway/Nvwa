#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

from loongtian.util.common.enum import Enum


class ThinkingInfo():
    """
    [运行时对象]关于思考状态的枚举信息（这些状态在思维处理中不断被改变，是单向、互斥的）。
    """

    class MindExecuteInfo(Enum):
        """
        [运行时对象]当前思考的执行信息。
        """
        UNKNOWN = 0  # 完全未知

        Start_Mind = 1  # 启动思考
        Pause_Mind = 2  # 暂停思考
        Restore_Mind = 3  # 恢复（重启）思考
        Stop_Mind = 4  # 停止思考

        Waiting_Aboves = 5  # 等待上文
        Waiting_Nexts = 6  # 等待下文
        Waiting_Contexts = 7  # 等待上、下文

        Processing_MetaArea = 10  # 开始处理元数据
        Processing_RealArea = 11  # 开始处理实际对象链

        Associating = 12  # 对实际对象进行联想
        Evaluating_Undertood = 13  # 对理解结果进行评估
        Calculating_Emotion = 14
        Creating_Plan = 15
        Executing_Behaviour = 16
        # todo 添加其他思考执行信息

    class MetaLevelInfo():
        """
        [运行时对象]元数据级别的处理信息。
        """

        class ExecuteInfo(Enum):
            """
            [运行时对象]元数据级别的处理的执行信息。
            """
            UNKNOWN = 100  # 完全未知

            # Processing_RawInput = 101

            Processing_MataData = 110
            Processing_RelatedRealObjects = 111

            Processing_MetaNet = 120

            Processing_MataDatas = 130  # 根据元数据链查找元数据网

            Processing_MetaNet_Matched_Knowledges = 150
            Processing_MetaNet_Matched_Knowledges_Meaning = 151

        class MatchInfo(Enum):
            """
            [运行时对象]对元数据、元数据网、实际对象、知识链的匹配结果
            """

            UNKNOWN = 1000
            # 单个元数据层面
            SINGLE_META_MATCHED = 1101  # 元数据匹配（属于metadata库）。相当于什么都不知道（所有层面上）
            SINGLE_META_UNMATCHED = 1102  # 【思考终结点】元数据未匹配（不属于metadata库）。相当于什么都不知道（所有层面上）

            # 多个元数据层面
            META_CHAIN_MATCHED = 1200
            META_CHAIN_UNMATCHED = 1201
            META_CHAIN_PARTIAL_MATCHED = 1203  # 元数据链部分匹配，说明有未知的（等待进一步实际对象级别处理）

            # 元数据网层面
            METANET_UNMATCHED = 1500  # 元数据网未匹配（不属于metanet库，等待进一步实际对象级别处理）
            METANET_MATCHED = 1501  # 元数据网、知识链已匹配（属于metanet库） 中间状态，马上会转为KNOWLEDGE_MATCHED_MEANING_MATCHED或KNOWLEDGE_MATCHED_MEANING_UNMATCHED
            # METANET_MATCHED_KNOWLEDGE_UNMATCHED = 1052  # 元数据网已匹配，知识链未匹配（没有对应的knowledge）

            # 单个元数据-实际对象层面
            SINGLE_META_RELATED_REALS_UNMATCHED = 2000  # 有单个meta，但实际对象未匹配（不属于realobject库）
            SINGLE_META_RELATED_REALS_MATCHED = 2001  # 有单个meta，实际对象已匹配（属于realobject库，可能有多个）

            # 知识链匹配层面
            METANET_KNOWLEDGE_UNMATCHED = 2500  # 知识链未匹配（不属于knowledge库，肯定找不到下一层知识链，相当于未理解）
            METANET_KNOWLEDGE_MATCHED = 2501  # 知识链已匹配（属于knowledge库），并能够理解（能找到下一层知识链）。系统已匹配（所有层面上，在metadata、realobject、knowledge库中都有）

            METANET_KNOWLEDGE_MEANING_MATCHED = 2502  # 【思考终结点】知识链已匹配（属于knowledge库），能够理解（找到了下一层知识链）
            METANET_KNOWLEDGE_MEANING_UNMATCHED = 2503  # 知识链已匹配（属于knowledge库），但不能够理解（找不到下一层知识链）

            RAWINPUT_KNOWLEDGE_MEANING_MATCHED = 2504  # 【思考终结点】知识链已匹配（属于knowledge库），能够理解（找到了下一层知识链）

    class RealLevelInfo():
        """
        [运行时对象]实际对象级别的处理信息。
        """

        class ExecuteInfo(Enum):
            """
            [运行时对象]实际对象级别的执行信息。
            """
            UNKNOWN = 100  # 完全未知

            Processing_RealObject = 111

            Processing_MataDatas_To_Reals = 120# 根据元数据链查找实际对象链

            Processing_RealObjects = 130  # 对实际对象链进行处理，例如：对其进行分组，然后理解等

            Processing_Matching_Knowledge = 140  # 根据实际对象链查找知识链
            Processing_Matched_Knowledge_Meaning = 141  # 根据实际对象链查找到的知识链，查找意义（下一层知识链）

            Processing_Knowledge = 150
            Processing_Knowledge_Meaning = 151

            Understanding = 160 # 试图理解（两种情况：1、查找到知识链，但在数据库中没有意义；2、查找不到知识链）

            Understanding_Fragment =161 # 试图理解部分片段
            Processing_UnderstoodFragment = 162  # 处理实际对象链中已经被理解的部分片段
            Processing_UnsatisfiedFragments = 163  # 处理实际对象链中动作的pattern只能部分匹配的部分片段

            Processing_RealLevelResult = 164  # 对实际对象级别的结果进行进一步处理

            WAITING_CONTEXT = 200  # 等待上下文

        class MatchInfo(Enum):
            """
            [运行时对象]实际对象级别的 对实际对象、知识链的匹配结果
            """

            UNKNOWN = 1000

            # 实际对象链层面（进入理解层面）
            REAL_CHAIN_MATCHED = 3000  # 所有实际对象已匹配
            REAL_CHAIN_UNMATCHED = 3001  # 所有实际对象均未能匹配
            PARTIAL_REAL_CHAIN_MATCHED = 3002  # 部分实际对象匹配

            # 知识链匹配层面
            REAL_CHAIN_KNOWLEDGE_UNMATCHED = 2500  # 知识链未匹配（不属于knowledge库，肯定找不到下一层知识链，相当于未理解）
            REAL_CHAIN_KNOWLEDGE_MATCHED = 2501  # 知识链已匹配（属于knowledge库），并能够理解（能找到下一层知识链）。系统已匹配（所有层面上，在metadata、realobject、knowledge库中都有）

            REAL_CHAIN_KNOWLEDGE_MEANING_MATCHED = 2502  # 知识链已匹配（属于knowledge库），但不能够理解（找不到下一层意义知识链）
            REAL_CHAIN_KNOWLEDGE_MEANING_UNMATCHED = 2503  # 知识链已匹配（属于knowledge库），但不能够理解（找不到下一层意义知识链）

            FRAGMENT_KNOWLEDGE_UNMATCHED = 2600  # 知识链未匹配（不属于knowledge库，肯定找不到下一层知识链，相当于未理解）
            FRAGMENT_KNOWLEDGE_MATCHED = 2601  # 知识链已匹配（属于knowledge库），并能够理解（能找到下一层知识链）。系统已匹配（所有层面上，在metadata、realobject、knowledge库中都有）
            FRAGMENT_KNOWLEDGE_MEANING_MATCHED = 2602  # 知识链已匹配（属于knowledge库），但不能够理解（找不到下一层意义知识链）
            FRAGMENT_KNOWLEDGE_MEANING_UNMATCHED = 2603  # 知识链已匹配（属于knowledge库），但不能够理解（找不到下一层意义知识链）

            FRAGMENT_UNSATISFIED_NEED_ABOVES = 2604  # 需要上文（实际对象链中动作的pattern只能部分匹配的部分片段）
            FRAGMENT_UNSATISFIED_NEED_NEXTS = 2605  # 需要下文（实际对象链中动作的pattern只能部分匹配的部分片段）
            FRAGMENT_UNSATISFIED_NEED_CONTEXTS = 2606  # 需要上、下文（实际对象链中动作的pattern只能部分匹配的部分片段）

        class UnderstoodInfo(Enum):
            """
            [运行时对象]实际对象级别的理解层面的枚举信息
            """
            UNKNOWN = 5000

            SINGLE_UNDERSTOOD = 5001  # 单个实际对象
            SINGLE_MISUNDERSTOOD = 5002
            SINGLE_UNDERSTOOD_NEED_CONTEXTS = 5003

            MEANING_MATCHED_UNDERSTOOD = 5004 # 实际对象链-知识链-意义知识链完全匹配之后的理解

            FRAGMENT_UNDERSTOOD = 5100  # 片段能够理解（可能会记录多个）
            FRAGMENT_MISUNDERSTOOD = 5101  # 片段能够理解（可能会记录多个）
            FRAGMENT_MEANING_MATCHED_UNDERSTOOD = 5102  # 片段实际对象链-知识链-意义知识链完全匹配之后的理解

            ALL_REALS_UNDERSTOOD = 5500  # 全都能够理解（所有实际对象已知，并且实际对象链能够迁移出结果）
            ALL_REALS_UNDERSTOOD_ANYTHING_MATCHED = 5600 # 全都能够理解，并且其中的未知对象已经过匹配处理。例如：已知：牛有腿，牛有角，输入：牛有什么，输出：牛有腿，牛有角

            ALL_REALS_UNKNOWN = 5501  # 所有实际对象均已知
            PARTIAL_UNDERSTOOD = 5502  # 所有实际对象已知，但只有部分实际对象链能够迁移出结果

            REALS_NEED_CONTEXT =5503 # 未满足pattern的片段长度大于实际对象链的长度

            REGENERRATED_REALS_UNDERSTOOD = 5504

            FRAGMENTS_CONFLICTED_MISUNDERSTOOD = 5505 # 由于理解片段有冲突所以导致的未能理解。
                                                      # 例如：牛组件腿属性黄，可以分解出的理解片段包括：牛组件腿，腿属性黄，
                                                      # 这两部分存在冲突，按顺序只能满足前者，那么后者 属性黄 的上文就包括：腿、牛组件腿、牛，这需要进一步处理

            SELF_EXPLAIN_SELF = 5506 # 自解释（自己解释自己，例如：牛组件腿意义为牛组件腿，牛有腿就是牛有腿）
                                         # 这种情况，只允许在“意义为”及其衍生对象中出现

            EXECUTIONINFO_CREATED = 5507 # 根据意义标记，建立了左右两侧对象的意义关联

            EXECUTIONINFO_EXIST = 5508 # 根据意义标记，匹配到了左右两侧对象的意义关联






class ObjectTags():
    RawInput = "RawInput"
    SegmentResult = "SegmentResult"
    MetaData = "MetaData"
    RealObject = "RealObject"
    MetaNet = "MetaNet"
    RelatedKnowledges = "RelatedKnowledges"
    Knowledge = "Knowledge"
    Knowledge_Meanings = "Knowledge_Meanings"

    Pattern_klg = "Pattern_klg"
    Meaning_klg = "Meaning_klg"

    MetaDatas = "MetaDatas"
    RealObjects = "RealObjects"
    RealObjects_Meanings = "RealObjects_Meanings"

    _tags = [
        RawInput,
        MetaData,
        RealObject,
        MetaNet,
        Knowledge,
        Knowledge_Meanings,
        Pattern_klg,
        Meaning_klg,
        MetaDatas,
        RealObjects,
        RealObjects_Meanings,
    ]

    @staticmethod
    def isObjectTags(tag):
        """
        判断一个标签是否位于系统定义的标签中
        :param tag:
        :return:
        """
        return tag in ObjectTags._tags


class SystemInfo(Enum):
    """
    [运行时对象]女娲系统级别反馈的信息，例如：吗?---{系统已匹配:有,系统未知:没有}
    """

    class CollectionInfo(Enum):
        """
        关于集合的枚举信息。
        """
        ELEMENTTYPE = 200  # 集合元素的类型
        NUMBER = 201  # 集合元素数量

    class InnerOperationInfo(Enum):
        """
        系统内部做处理时的操作信息
        """
        # 参考：ARM指令集 --RISC精简指令集 - xiangxistu的博客 - CSDN博客
        # https://blog.csdn.net/xiangxistu/article/details/83018715

        # 数据库操作
        Create = 300  # 增加
        Retrieve = 301  # 读取查询
        Update = 302  # 更新
        Delete = 303  # 逻辑删除
        PhysicalDelete = 304  # 物理删除
        Forget = 305  # 遗忘
        Compare = 306  # 比较

        # 集合操作
        Intersection = 307  # 求同（交集）
        Difference = 308  # 求异（差集）
        Union = 309  # 求和（并集）
        Count = 310  # 计算
        RestoreIndex = 311  # 重置索引

        # 数学操作

        CreateExecutionInfo = 500  # 创建意义
