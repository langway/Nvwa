# /usr/bin/python
# coding: utf-8
__author__ = 'Leon'

import copy
import uuid
from loongtian.nvwa.models.enum import ObjType
from loongtian.nvwa.runtime.workflow import Workflow, Step, Status
from loongtian.util.common.generics import GenericsList

"""
意义的种类：
1、迁移出来的意义（真正意义）
2、自己解释自己。例如：牛有腿意义牛有腿，只是起强调作用，对注意力引擎有作用
2、建立意义。根据意义标记，建立了左右两侧对象的意义关联
"""
from loongtian.nvwa.runtime.instinct import Instincts

class BaseMeaning(object):
    """
    [运行时对象]意义的基础类（必须继承）。
    """

    def __init__(self, action=None, left=None, right=None,memory=None):
        self.id = str(uuid.uuid1()).replace("-", "")
        self.action = action
        self.left = left
        self.right = right

        self.memory=memory

        self._knowledge = None  # 已经生成的知识链

        # ####################################
        #      下面为运行时数据
        # ####################################

    def createKnowledge(self, recordInDB=False):
        """
        根据理解片段生成意义知识链。
        :return:
        """
        if self._knowledge:
            return self._knowledge
        if self.action and self.left and self.right:
            from loongtian.nvwa.models.knowledge import Knowledge
            self._knowledge = Knowledge.createKnowledgeByObjChain([self.left, self.action, self.right],
                                                                  recordInDB=recordInDB,
                                                                  memory=self.memory)
            return self._knowledge


class Meaning(Workflow, BaseMeaning):
    """
    [运行时对象]迁移引擎迁移出来的意义（真正意义）。
    """

    """
    类似于：
    meaning_objs=[ # meaning对应的knowledge知识链
            [ # steps：knowledge知识链的每一步的转换模式（可以有多个状态转换）
                status：[self.real_niu,self.brain.MemoryCentral.Instincts.instinct_component,self.real_tui], # knowledge知识链每一步中包含的每一个状态knowledge
            ],
        ]
    """

    def __init__(self, id=None, action=None, left=None, right=None,memory=None):
        """
        [运行时对象]迁移引擎迁移出来的意义（真正意义）。
        :param action:
        :param left:
        :param right:
        """
        BaseMeaning.__init__(self, action, left, right,memory=memory)
        Workflow.__init__(self, id,memory=memory)

    @staticmethod
    def createByFullKnowledge(meaning_knowledge, placeholder_obj_dict=None,memory=None):
        """
        [重载函数]根据意义的完整知识链创建意义包装类。
        :param meaning_knowledge:意义知识链（三层嵌套）
        :param placeholder_obj_dict:使用placeholder_dict对status中的obj_chain中的对象进行替换（如果有的话）
        :return:
        """
        if meaning_knowledge.getType() != ObjType.LINEAR_EXE_INFO:
            raise Exception("意义必须标记为可执行性信息！")
        # 意义包装类
        _meaning = Meaning(memory=memory)

        _meaning_knowledge_components = meaning_knowledge.getSequenceComponents()
        if not _meaning_knowledge_components:
            raise Exception("未能正确取得意义知识链的步骤元素！")
        # 步骤
        from loongtian.nvwa.models.knowledge import Knowledge
        for step in _meaning_knowledge_components:  # 步骤知识链（可能有多个，代表不同的步骤）
            step_obj_chain = step
            if isinstance(step, Knowledge):
                if step.getType() != ObjType.LINEAR_EXE_INFO:
                    raise Exception("意义的步骤必须标记为可执行性信息！")
                # 取得实际元素
                step_obj_chain = step.getSequenceComponents()

            if not isinstance(step_obj_chain, list):
                raise Exception("未能正确取得意义知识链的步骤!")

            # 状态
            _step = Step(memory=memory)
            from loongtian.nvwa.models.knowledge import Knowledge
            for status in step_obj_chain:
                status_obj_chain = status
                if isinstance(status, Knowledge):
                    # if step.getType() != ObjType.LINEAR_EXE_INFO: # 2019-02-14 状态不再检查类型，因为完全可能被其他对象复用，例如：小明打小丽中的“小明抬手、小明手落下”
                    #     raise Exception("意义的每一个步骤的每一个状态必须标记为可执行性信息！")
                    status_obj_chain = status.getSequenceComponents()

                if not isinstance(status_obj_chain, list):
                    raise Exception("未能正确取得意义知识链的状态!")

                # 使用placeholder_dict对obj_chain中的对象进行替换
                status_obj_chain = Meaning._replace_obj_with_placeholder_dict(status_obj_chain, placeholder_obj_dict)
                if not status_obj_chain:
                    raise Exception("未能正确迁移一个状态！")
                _status = Status(status_obj_chain,memory=memory)
                _step.addStatus(_status)

            _meaning.addStep(_step)

        # 记录到已经生成的知识链
        if not placeholder_obj_dict:
            _meaning._knowledge = meaning_knowledge
        else:
            _meaning.createKnowledge(recordInDB=False,memory=memory)

        return _meaning

    @staticmethod
    def createByStepKnowledge(step_knowledge, placeholder_obj_dict=None,memory=None):
        """
        [重载函数]根据单一的步骤知识链生成meaning
        :param step_knowledge: 两层嵌套知识链
        :param placeholder_obj_dict:使用placeholder_dict对status中的obj_chain中的对象进行替换（如果有的话）
        :return:
        """
        # 检查类型标记
        if step_knowledge.getType() != ObjType.LINEAR_EXE_INFO:
            raise Exception("意义的步骤必须标记为可执行性信息！")

        # 意义包装类
        _meaning = Meaning(memory=memory)
        # 取得实际元素
        step_obj_chain = step_knowledge.getSequenceComponents()

        if not isinstance(step_obj_chain, list):
            raise Exception("未能正确取得意义知识链的步骤!")

        # 步骤
        _step = Step(memory=memory)
        from loongtian.nvwa.models.knowledge import Knowledge
        # 状态
        for status in step_obj_chain:
            status_obj_chain = status
            if isinstance(status, Knowledge):
                # if step.getType() != ObjType.LINEAR_EXE_INFO: # 2019-02-14 状态不再检查类型，因为完全可能被其他对象复用，例如：小明打小丽中的“小明抬手、小明手落下”
                #     raise Exception("意义的每一个步骤的每一个状态必须标记为可执行性信息！")
                status_obj_chain = status.getSequenceComponents()

            if not isinstance(status_obj_chain, list):
                raise Exception("未能正确取得意义知识链的状态!")

            # 使用placeholder_dict对obj_chain中的对象进行替换
            status_obj_chain = Meaning._replace_obj_with_placeholder_dict(status_obj_chain, placeholder_obj_dict)
            if not status_obj_chain:
                raise Exception("未能正确迁移一个状态！")
            _status = Status(status_obj_chain,memory=memory)
            _step.addStatus(_status)

        _meaning.addStep(_step)

        # 记录到已经生成的知识链
        _meaning.createKnowledge(recordInDB=False,memory=memory)

        return _meaning

    @staticmethod
    def createByStatusKnowledge(status_knowledge, placeholder_obj_dict=None,memory=None):
        """
        [重载函数]根据单一的步骤知识链生成meaning
        :param status_knowledge: 两层嵌套知识链
        :param placeholder_obj_dict:使用placeholder_dict对status中的obj_chain中的对象进行替换（如果有的话）
        :return:
        """
        if not status_knowledge:
            return None
        if not memory:
            memory=status_knowledge.MemoryCentral
        # 意义包装类
        _meaning = Meaning(memory=memory)
        # 步骤
        _step = Step(memory=memory)
        from loongtian.nvwa.models.knowledge import Knowledge
        # 状态
        # if status_knowledge.getType() != ObjType.LINEAR_EXE_INFO: # 2019-02-14 状态不再检查类型，因为完全可能被其他对象复用，例如：小明打小丽中的“小明抬手、小明手落下”
        #     raise Exception("意义的每一个步骤的每一个状态必须标记为可执行性信息！")
        status_obj_chain = status_knowledge.getSequenceComponents()

        if not isinstance(status_obj_chain, list):
            raise Exception("未能正确取得意义知识链的状态!")

        # 使用placeholder_dict对obj_chain中的对象进行替换（如果有的话）
        status_obj_chain = Meaning._replace_obj_with_placeholder_dict(status_obj_chain, placeholder_obj_dict)

        _status = Status(status_obj_chain,memory=memory)
        _step.addStatus(_status)

        _meaning.addStep(_step)

        # 记录到已经生成的知识链
        _meaning.createKnowledge(recordInDB=False)

        return _meaning

    @staticmethod
    def _replace_obj_with_placeholder_dict(obj_chain, placeholder_dict):
        """
        使用placeholder_dict对obj_chain中的对象进行替换
        :param obj_chain:
        :return:
        """
        if not placeholder_dict:  # 如果没有，直接返回原obj_chain
            return obj_chain
        if isinstance(obj_chain, list) or isinstance(obj_chain, tuple):
            obj_chain = copy.copy(list(obj_chain))  # 浅表复制一个
        else:
            raise Exception("当前状态并非Knowledge或实际对象列表，迁移无法进行！")

        if obj_chain:
            from loongtian.nvwa.models.knowledge import Knowledge
            from loongtian.nvwa.models.realObject import RealObject
            for i in range(len(obj_chain)):
                cur_obj = obj_chain[i]
                if isinstance(cur_obj, RealObject):
                    if cur_obj in placeholder_dict:
                        obj_chain[i] = placeholder_dict[cur_obj]
                elif isinstance(cur_obj, Knowledge):
                    child_realChain = Meaning._replace_obj_with_placeholder_dict(cur_obj, placeholder_dict)
                    obj_chain[i] = child_realChain
                elif isinstance(cur_obj, list):
                    child_realChain = Meaning._replace_obj_with_placeholder_dict(cur_obj, placeholder_dict)
                    obj_chain[i] = child_realChain
                else:
                    raise Exception("当前状态并非Knowledge或实际对象列表，迁移无法进行！")

        return obj_chain

    def __repr__(self):
        return "{Meaning:{id:%s,steps:%s}}" % (self.id, self.steps)


class SelfExplainSelfMeaning(BaseMeaning):
    """
    [运行时对象]自己解释自己。例如：牛有腿意义牛有腿，只是起强调作用，对注意力引擎有作用。
    """

    def __init__(self, action=None, left=None, right=None,memory=None):
        """
        [运行时对象]自己解释自己。例如：牛有腿意义牛有腿，只是起强调作用，对注意力引擎有作用。
        :param action:
        :param left:
        :param right:
        """
        super(SelfExplainSelfMeaning, self).__init__(action, left, right,memory=memory)


class ExecutionInfoCreatedMeaning(BaseMeaning):
    """
    [运行时对象]建立意义。根据意义标记，建立了左右两侧对象的意义关联
    """

    def __init__(self, action=None, left=None, right=None,newCreated=False,memory=None):
        """
        [运行时对象]建立意义。根据意义标记，建立了左右两侧对象的意义关联。
        :param action:
        :param left:
        :param right:
        """
        super(ExecutionInfoCreatedMeaning, self).__init__(action,left, right,memory=memory)
        # self.executionInfoCreater = executionInfoCreater
        self.newCreated =newCreated

    def createKnowledge(self, recordInDB=False):
        """
        根据理解片段生成意义知识链。
        :return:
        """
        if self._knowledge:
            return self._knowledge
        if self.action and self.left and self.right:
            from loongtian.nvwa.models.knowledge import Knowledge
            self._knowledge = Knowledge.createKnowledgeByObjChain([self.left, Instincts.instinct_meaning, self.right],
                                                                  recordInDB=recordInDB,
                                                                  memory=self.memory)
            return self._knowledge

class ExecutionInfoCreatedMeanings(GenericsList):
    """
    [运行时对象]建立意义。根据意义标记，建立了左右两侧对象的意义关联的包装类的列表。
    """
    def __init__(self,memory=None):
        """
        [运行时对象]建立意义。根据意义标记，建立了左右两侧对象的意义关联的包装类的列表。
        """
        super(ExecutionInfoCreatedMeanings, self).__init__(ExecutionInfoCreatedMeaning)

class Meanings(GenericsList):
    """
    [运行时对象]是迁移引擎使用的表示意义的列表的包装类的列表。
    """

    def __init__(self,memory=None):
        """
        [运行时对象]是迁移引擎使用的表示意义的列表的包装类的列表。
        """
        super(Meanings, self).__init__(BaseMeaning)
        # ####################################
        #      下面为运行时数据
        # ####################################
        self.memory=memory
        self.meaningsKnowledges = None  # 由列表中所有的意义取得的知识链（多个）
        self.meaningsKnowledge = None  # 由列表中所有的意义创建的知识链（一个）

    def getMeaningsKnowledges(self):
        """
        （注意与getMeaningsKnowledge的区别）取得列表中所有的意义取得的知识链（多个）
        :return:
        """
        if self.meaningsKnowledges:
            return self.meaningsKnowledges
        self.meaningsKnowledges = []

        for cur_meaning in self:
            if not cur_meaning.memory:
                cur_meaning.memory=self.memory
            cur_klg = cur_meaning.createKnowledge()
            self.meaningsKnowledges.append(cur_klg)
        return self.meaningsKnowledges

    def getMeaningsKnowledge(self,recordInDB=False):
        """
        （注意与getMeaningsKnowledges的区别）取得列表中所有的意义创建的知识链（一个）
        :return:
        """
        if self.meaningsKnowledge:
            return self.meaningsKnowledge
        cur_klgs = []
        from loongtian.nvwa.models.knowledge import Knowledge
        cur_klgs = self.getMeaningsKnowledges()
        if cur_klgs:
            self.meaningsKnowledge = Knowledge.createKnowledgeByObjChain(cur_klgs,
                                                                         recordInDB=recordInDB,
                                                                         memory=self.memory)
        return self.meaningsKnowledge
