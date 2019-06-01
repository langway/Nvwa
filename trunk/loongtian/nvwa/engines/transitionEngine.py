#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Leon'

from loongtian.nvwa.engines.engineBase import ThinkEngineBase
from loongtian.util.log import logger
from loongtian.nvwa.models.realObject import RealObject
from loongtian.nvwa.models.knowledge import Knowledge
from loongtian.nvwa.models.enum import ObjType
from loongtian.nvwa.runtime.placeholder import Placeholder
from loongtian.nvwa.runtime.meanings import Meaning, SelfExplainSelfMeaning,ExecutionInfoCreatedMeaning
from loongtian.nvwa.runtime.instinct import Instincts

class TransitionEngine(ThinkEngineBase):
    """
    迁移引擎
    :rawParam
    :attribute
    """

    def __init__(self, thinkingCentral):
        """
        迁移引擎。按照步骤-状态的顺序迁移成结果。
        :param memoryCentral: 用来存放当前对象的内存空间（避免每次都从数据库中调用）
                       当前TansitionEngine的memory是MemoryCentral
        """
        super(TransitionEngine, self).__init__(thinkingCentral)

    def transitByAction(self, reals, pattern_knowledge, meaning_knowledge,meaning_value,
                        strictly_match_parent=True):
        """
        使用动作定义的模式和意义对输入实际对象列表进行状态迁移。将输入对象列表根据模式转换，按意义步骤一步一步迁移为最终状态
        :param reals:输入实际对象列表，例如：牛-有-尾巴
        :param pattern_knowledge:作为模式的知识链，例如：?1-有-?2
        :param meaning_knowledge:作为意义的知识链列表（相当于步骤），例如：?1-组件为-?2
        :param strictly_match_parent:是否严格按照占位符所限定的父对象匹配输入的实际对象。
        :return:
        """
        # 检查参数
        if reals is None or (not isinstance(reals, list) and not isinstance(reals, tuple)) or len(reals) < 1:
            raise Exception("必须提供输入实际对象列表，例如：牛-有-尾巴！")
        for real in reals:
            if not isinstance(real, RealObject) and not isinstance(real, Knowledge):
                raise Exception("必须输入实际对象或知识链！当前对象：" + str(real))

        if pattern_knowledge is None or not isinstance(pattern_knowledge, Knowledge):
            raise Exception("必须提供作为模式的知识链，例如：?1-有-?2")
        if meaning_knowledge is None or not isinstance(meaning_knowledge, Knowledge):
            raise Exception("必须提供作为意义的知识链集合，例如：[[[?1-组件为-?2]]]")

        pattern_knowledge.getChainItems()
        meaning_knowledge.getChainItems()

        if not len(reals) == len(pattern_knowledge.s_chain):
            raise Exception("当前输入对象列表与作为模式的知识链不匹配，无法进行迁移操作！")

        # 如果是内部操作，取得内部操作函数
        inner_operations = meaning_knowledge.getInnerOperations()
        if inner_operations:  # 执行内部操作
            return self._processInnerOperations(reals, pattern_knowledge, inner_operations)
        else:
            return self._processWithPlaceholders(reals, pattern_knowledge, meaning_knowledge,meaning_value, strictly_match_parent)

    def _processInnerOperations(self, reals, pattern_knowledge, inner_operations):
        """
        如果是内部操作，取得内部操作函数，然后执行
        :param reals:
        :param pattern_knowledge:
        :param inner_operations:
        :return:
        """
        pattern_components = pattern_knowledge.getSequenceComponents()
        action = set(reals) & set(pattern_components)  # 求交集
        if not action:
            return None

        action=list(action)
        if len(action) == 1:
            action = action[0]
        elif len(action) > 1:  # todo 目前未考虑两个动作构成一个pattern
            pass

        if not isinstance(action,RealObject):
            raise Exception("动作必须是可执行的实际对象！")

        action_index = reals.index(action)
        left = reals[0:action_index]
        right = reals[action_index+1:]

        differ = set(left)-set(right)
        if not differ: # 动作的左右两侧相等
            # 判断该动作是否是内部定义的“意义为”或是其子类
            if action.isInstinctMeaning() or action.Constitutions.isChild(Instincts.instinct_meaning):
                # 自解释（自己解释自己，例如：牛组件腿意义为牛组件腿，牛有腿就是牛有腿）
                # 这种情况，只允许在“意义为”及其衍生对象中出现
                return SelfExplainSelfMeaning(action,left,right)

        if len(left)==1:
            left=left[0]
        if len(right)==1:
            right=right[0]
        inner_operation_results =[] # 执行结果
        for inner_operation in inner_operations:
            cur_result = inner_operation(left, right, self.MemoryCentral)
            if cur_result:
                inner_operation_results.append(cur_result)
        if len(inner_operation_results)==1: # 扒皮
            inner_operation_results=inner_operation_results[0]
        return inner_operation_results


    def _processWithPlaceholders(self, reals, pattern_knowledge, meaning_knowledge,meaning_value,strictly_match_parent=True):
        """
        根据占位符同位置替换的原则，对意义知识链进行替换，取得最终的意义。
        :param reals:
        :param pattern_knowledge:
        :param meaning_knowledge:
        :param strictly_match_parent:
        :return:
        """
        pattern_components = pattern_knowledge.getSequenceComponents()
        # 取得占位符对应的输入实际对象的词典，例如：牛 - 有 - 尾巴，？1 - 有 -？2，？1就对应牛，？2就对应尾巴
        placeholder_obj_dict, obj_placeholder_dict = Placeholder.get_placeholder_dict(reals, pattern_components)

        if not placeholder_obj_dict:
            raise Exception("无法取得占位符对应的输入实际对象的词典，输入实际对象列表与模式不匹配！")

        # 根据meaning_value创建值
        if meaning_value:
            meaning_value_obj = self._createdMeaningValueObj(meaning_value)
            placeholder_obj_dict[meaning_value]=meaning_value_obj

        if strictly_match_parent:  # 如果要求严格按照占位符所限定的父对象匹配输入的实际对象，对其进行检查，例如realObj限定为食草类哺乳动物，placeholder限定为哺乳动物，就可通过，反之，则不能通过
            succeed_num = 0
            parentsConfusions = []
            for _placeholder, realObj in placeholder_obj_dict.items():
                # 取得所有父对象的继承关系
                inherit_relation, all_parents_relation = _placeholder.Constitutions.getInheritRelation()
                succeed = False

                for parent in all_parents_relation.keys():
                    if realObj.Constitutions.isChild(parent):  # 只要有一个符合限定即可
                        succeed_num += 1
                        succeed = True
                        break

                if not succeed:
                    parentsConfusions.append((_placeholder, realObj, all_parents_relation))

            if succeed_num != len(placeholder_obj_dict):
                e = Exception("占位符的父对象不匹配实际对象的父对象，无法继续进行迁移操作！未匹配的对象包括：\r\n" + str(parentsConfusions))
                logger.info(e)
                # 将父对象困惑送入nvwa大脑进行进一步思维（当前思维线程暂停，等待结果）
                if self.MemoryCentral and self.MemoryCentral.Brain:
                    self.MemoryCentral.Brain.ThinkingCentral.thinkParentsConfusion(parentsConfusions)

        _meaning = Meaning.createByFullKnowledge(meaning_knowledge, placeholder_obj_dict,memory=self.MemoryCentral)
        return _meaning

    def _createdMeaningValueObj(self,meaning_value):
        """
        根据meaning_value（是一个placeholder），创建一个instinct_anything的子对象（只在内存中），以便系统进行进一步思考处理
        :param meaning_value:是一个placeholder
        :return:
        """
        meaning_value_obj = RealObject(memory=self.MemoryCentral)
        meaning_value_obj.remark="Object(%s)" % meaning_value_obj.id
        # meaning_value_obj.Constitutions.addParent(Instincts.instinct_original_object,recordInDB=False)

        return meaning_value_obj

    def transitByParadigm(self):
        """
        按照上下文的关联模式进行迁移。
        :return:
        :remarks:
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

    # @staticmethod
    # def tansiteToRealObject(entity):
    #     """
    #     迁移方法
    #     :return: 迁移后的结果，如果迁移失败返回None。
    #     """
    #     haveAction = False
    #     onlyAction = True
    #     remark = []
    #     for item in entity:
    #         haveAction = haveAction or item.isAction()
    #         onlyAction = onlyAction and item.isAction()
    #         if isinstance(item, MetaData):
    #             remark.append("%s," % item.mvalue)
    #         elif isinstance(item, RealObject):
    #             remark.append("<%s>:%s," % (item.id, item.remark))
    #         else:
    #             raise Exception("%s类型错误。" % item)
    #     remark = "[" + "".join(remark)[:-1] + "]"
    #     if onlyAction:
    #         return RealObject(remark = remark, pattern = "???", relatedMetas = "???")
    #     if not haveAction:
    #         return RealObject(remark = remark)
    #     return RealObject(remark = remark)
