#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Leon'

import itertools
from loongtian.nvwa.models.enum import ObjType
from loongtian.nvwa.models.realObject import RealObject
from loongtian.nvwa.models.knowledge import Knowledge
from loongtian.nvwa.runtime.relatedObjects import RelatedObj
from loongtian.nvwa.runtime.thinkResult.fragments import Unknowns
from loongtian.nvwa.runtime.specialList import GroupedReals
from loongtian.nvwa.engines.engineBase import ThinkEngineBase

"""
分组引擎。
1、按照Action的优先级进行分组
2、按照上下文的关联模式分组
    （1）、RCR-C：第一次
    （2）、ACA/AA-C：看一看，看看
    （3）、CR-R：一车
    （4）、RC-R：第一
    （5）、CA-A：又看，再看
    （6）、AC-A：走了
    （7）、CCC-C：1234
    （8）、RRR-R：中国建设银行
    （9）、AAA-R/A：打跑了，开关，伟大
    （10）、RAR-R：小明打小丽

"""


class GroupEngine(ThinkEngineBase):
    """
    分组引擎。
    :rawParam
    :attribute
    """

    def __init__(self, thinkingCentral):
        """
        分组引擎。按照Action的优先级以及上下文的关联模式进行分组
        :param memoryCentral: 用来存放当前对象的内存空间（避免每次都从数据库中调用）
                       当前GroupEngine的memory是MemoryCentral
        """
        super(GroupEngine, self).__init__(thinkingCentral)


    def group1(self, reals):
        """
        按照Action的优先级进行分组（产生式，例如：我知道中国人民解放军是最棒的，小明用手拿起瓶子）
        :param reals:
        ：remark : 我知道中国人民解放军是最棒的 分组结果：[我,知道,[中国人民解放军,是,最棒的]，[[我,知道,中国人民解放军],是,最棒的]...
                  小明用手拿起瓶子 分组结果：[小明,[[用,手],[拿,起]],瓶子],[小明,[用,[手拿,起]],瓶子]...
                  牛有腿意义为牛组件为腿 分组结果：[[牛,有,腿],意义为,[牛,组件为,腿]],[牛,有,[腿,意义为,[牛组件为腿]]...
        :return:
        """
        typed_objs = {
            ObjType.UNKNOWN: {},
            ObjType.EXISTENCE: {},
            ObjType.VIRTUAL: {},
            # ObjType.MOTIFIER:{},
            ObjType.ACTION: {},
            ObjType.INSTINCT: {},
            ObjType.KNOWLEDGE: {}
        }

        actions = {}
        i = 0
        for real in reals:
            if isinstance(real, RelatedObj):
                real = real.obj
            if isinstance(real, RealObject):
                if real.isSingularity():  # 判断当前实际对象是否是奇点对象
                    typed_objs[ObjType.UNKNOWN][i] = real
                else:
                    real.ExecutionInfo.getSelfLinearExecutionInfo()
                    typed_objs[real.getType()][i] = real
            elif isinstance(real, Unknowns):
                typed_objs[ObjType.UNKNOWN][i] = real
            elif isinstance(real, Knowledge):
                typed_objs[ObjType.KNOWLEDGE][i] = real
            elif isinstance(real, list):
                child_group = self.groupRealChain(real)

            else:
                raise Exception("无法处理的类型！")
            i += 1

        execute_sequence = []  # 执行的先后顺序

        # # 1、首先处理未知的对象，如果全部未知，直接返回UnknownResult
        # unknown_reals = typed_objs.get(ObjType.UNKNOWN)
        # unknown_objs = None
        # if unknown_reals and len(unknown_reals) > 0:
        #     unknown_objs = UnknownObjs(reals)
        #     if len(unknown_reals) > 0:
        #         for pos, unknown_real in unknown_reals.items():
        #             unknown_obj = UnknownObj(unknown_real, pos)
        #             unknown_objs.append(unknown_obj)
        #             # self.Mind.unknowns_ratio=len(unknown_obj)/len(reals)
        #     if len(unknown_reals) == len(reals):  # 如果全部输入都为未知，直接生成knowledge（不保存在数据库）
        #
        #         if len(unknown_reals) == 1:
        #             return None, unknown_objs  # unknown_reals[0]
        #
        #         unknown_knowledge = Knowledge.createKnowledgeByRealChain(reals, understood_ratio=0.0, recordInDB=False)
        #         if unknown_knowledge:
        #             unknown_obj = UnknownObj(unknown_knowledge)
        #             unknown_objs.insert(0, unknown_obj)  # 把整个未知的knowledge放在第一个，便与后续追问
        #             return unknown_knowledge, unknown_objs
        #         else:
        #             return None, unknown_objs

        # 1、首先对instinct之间的对象进行处理
        knowledge = None
        instincts = typed_objs.get(ObjType.INSTINCT)

        instincts_splits = None
        if not instincts is None and len(instincts) > 0:
            instincts_splits = self.splitByPosExecutable(reals, instincts)
            realsChainList = self.getCandidatesRealChains(instincts_splits, list(instincts.values()))
        else:
            realsChainList = [reals]

        # 1、首先对action之间的对象进行处理
        actions = typed_objs.get(ObjType.ACTION)

        actions_splits = None
        if not actions is None and len(actions) > 0:
            if instincts_splits:
                actions_splits = []
                for instincts_split in instincts_splits:
                    temp_actions_splits = self.splitByPosExecutable(instincts_split, actions)
                    actions_splits.append(temp_actions_splits)
            else:
                actions_splits = self.splitByPosExecutable(reals, actions)

        # modifiers_splits = None
        # if not modifiers is None and len(modifiers) > 0:
        #     if actions_splits:
        #         modifiers_splits = []
        #         for actions_split in actions_splits:
        #             temp_modifiers_splits = self.splitByExecutable(actions_split, modifiers)
        #             modifiers_splits.append(temp_modifiers_splits)
        #     else:
        #         if instincts_splits:
        #             modifiers_splits = []
        #             for instincts_split in instincts_splits:
        #                 temp_modifiers_splits = self.splitByExecutable(instincts_split, modifiers)
        #                 modifiers_splits.append(temp_modifiers_splits)
        #
        #         else:
        #             modifiers_splits = self.splitByExecutable(reals, modifiers)

        grouped_reals_list = None
        # if modifiers_splits:
        #     grouped_reals_list = modifiers_splits
        # else:
        if actions_splits:
            grouped_reals_list = actions_splits
        else:
            if instincts_splits:
                grouped_reals_list = instincts_splits
            else:
                grouped_reals_list = [reals]

        return grouped_reals_list, execute_sequence

    def groupRealChain(self, reals):
        """
        按照Action的范式及优先级，对实际对象的序列进行分组（产生式，例如：我知道中国人民解放军是最棒的，小明用手拿起瓶子）
        :param reals:实际对象（realtedObj）的序列（可能嵌套）
        :remark: 我知道中国人民解放军是最棒的 分组结果：[我,知道,[中国人民解放军,是,最棒的]，[[我,知道,中国人民解放军],是,最棒的]...
                  小明用手拿起瓶子 分组结果：[小明,[[用,手],[拿,起]],瓶子],[小明,[用,[手拿,起]],瓶子]...
                  牛有腿意义为牛组件为腿 分组结果：[[牛,有,腿],意义为,[牛,组件为,腿]],[牛,有,[腿,意义为,[牛组件为腿]]...
        :return:
        """
        # 方法：
        # 1、查找到所有动作
        # 2、对动作按优先级排序
        # 3、查看是否符合动作的pattern
        # 4、按符合的进行分组

        return reals
        # grouped_reals = GroupedReals()
        # children_grouped_reals = []
        #
        # # 0、首先对子列表进行分组
        # for real in reals:
        #     if isinstance(real,RelatedObj):
        #         children_grouped_reals.append([real])
        #     elif isinstance(real,list) or isinstance(real,tuple):
        #         result = self.groupRealChain(real)
        #         children_grouped_reals.append(result)
        #
        # # 笛卡尔积
        # for child_grouped_reals in itertools.product(*children_grouped_reals):
        #
        #     # 1、取得所有的可执行性对象，并根据executables的权重重新计算执行的顺序
        #     # 只有pattern中父对象为knowledge或collection的才需要分组
        #     pos_executables = self.getExecutables(child_grouped_reals)
        #
        #     executables_splits = None
        #     if pos_executables:
        #         executables_splits = self.splitByPosExecutable(reals, pos_executables)
        #
        #     if executables_splits:
        #         grouped_reals_list = executables_splits
        #     else:
        #         grouped_reals_list = reals
        #
        #     grouped_reals_list, pos_executables
        #
        # return grouped_reals

    def getExecutables(self, reals):
        """
        递归取得实际对象链中所有的可执行性对象
        :param reals: 实际对象链
        :return: pos_executables:{pos:(real,weight)/{pos:(real,weight)}} {位置:(实际对象,权重)或pos_executables(代表着嵌套)}
        """
        # 首先取得所有的可执行性对象
        pos_executables = []
        # pos_sub_pos_executables
        pos = 1
        for real in reals:
            if isinstance(real, RelatedObj):
                if real.obj.isExecutable():  # 判断当前实际对象是否是可执行性对象
                    real.obj.ExecutionInfo.getSelfLinearExecutionInfo() # 取得执行信息
                    pos_executables.append((pos,real))
            pos += 1

        if pos_executables:
            # 根据(pos, real, weight)的weight/pos进行排序
            # todo 目前的公式为：weight/pos
            pos_executables.sort(key=lambda x: x[1].weight / float(pos),reverse=True)


        return pos_executables

    def splitByPosExecutable(self, reals, pos_exe_dict):

        pos_exe_list = list(pos_exe_dict.keys())
        pos_exe_list.sort()

        fragments_pos = []  # 匹配当前可执行对象模式的碎片（位置信息）
        fragments = []
        for cur_exe_pos in pos_exe_list:
            cur_exe = pos_exe_dict[cur_exe_pos]

            # 1、特殊处理意义为
            if cur_exe.isInstinctMeaning():
                pass
            elif cur_exe.isTopRelation():  # 2、特殊处理顶级关系
                pass
            else:
                # 取得模式、意义
                pattern_knowledge, meaning_knowledge = cur_exe.ExecutionInfo.getSelfLinearExecutionInfo()
                if pattern_knowledge:
                    # 取得线性列表
                    pattern_objs = pattern_knowledge.getSequenceComponents()
                    pattern_exe_pos = pattern_objs.index(cur_exe)  # 当前可执行实际对象在pattern中的位置
                    # 取得匹配当前可执行对象模式的碎片（根据位置信息）
                    distance = cur_exe_pos - pattern_exe_pos
                    if distance >= 0 and distance + len(pattern_objs) - 1 <= len(reals) - 1:  # 0到尾的才合法
                        fragment_pos = (distance, distance + len(pattern_objs) - 1)
                        fragments_pos.append(fragment_pos)
                        fragment = reals[distance:distance + len(pattern_objs) - 1]
                        fragments.append(fragment)

        results = []
        # 拼接所有线性序列

        return results

    def getCandidatesRealChains(self, splits, executabls):

        tri_candidates = []

        for i in range(len(splits)):
            cur = splits[i]
            last = None
            next = None
            if i > 0:
                last = splits[i - 1]
            if i < len(splits):
                next = splits[i + 1]
            if cur in executabls and last and next:
                cur_candidate = (last, cur, next)

        pass

    #
    # @staticmethod
    # def groupByMeta(metas):
    #     """
    #     分组操作
    #     [MetaData]的模式匹配：
    #         顺序  模式  结果及存储  匹配规则    是否迁移   eg
    #         1     RRR   R(知识链)   由后向前      否       中国人民建设银行
    #         2     AAA   A(新动词)   由前向后      否       打跑了  跑了  走了
    #         3     RAR   R(知识链)   优先级        是       小明打小丽  小明给小丽花
    #     动词模式有三种占位符：
    #         {数字}：表示左右的RealObject。
    #         {字母}：表示Anything，引用的第三方RealObject。
    #         {问号}：表示本身的RealObject。
    #         eg：
    #         "打" ==> {"pattern":"{0}打{1}", "meaning":"{0}手拿{A};{A}快速接触{1};{1}痛;"}
    #         "新" ==> {"pattern":"{?}:新{0}", "meaning":"{?}父对象{0};{?}=new{0};{?}.状态=新;"}
    #     :rawParam WordFrequncyDict: 输入的[MetaData]数据。
    #     :return: 可能的分组数据
    #     """
    #     if metas is None or len(metas) == 0:
    #         raise Exception("将要分组的数据(%s)不能为空！" % metas)
    #     result = copy.copy(metas)
    #     length = len(result)
    #     rrr = False
    #     i = 0
    #     while not rrr:
    #         index = i
    #         while index < length and not result[index].isAction():
    #             index += 1
    #         i += 1
    #         while index > i:
    #             result[index-2] = TansitionEngine.tansiteToRealObject(result[index - 2:index])
    #             result.pop(index-1)
    #             index -= 1
    #             length = len(result)
    #         if i >= length:
    #             rrr = True
    #     return result
    #         # AAA
    #         # AR
    #         # RAR
    #         # RA
