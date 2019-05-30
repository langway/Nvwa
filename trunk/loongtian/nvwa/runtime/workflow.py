# /usr/bin/python
# coding: utf-8
__author__ = 'Leon'

import uuid
from loongtian.nvwa.models.enum import ObjType


class Status(object):
    """
    [运行时对象]workflow知识链每一步中包含的状态（knowledge）
    """

    def __init__(self, objChain,id=None,memory=None):
        """
        [运行时对象]workflow知识链每一步中包含的状态（knowledge）
        :param objChain:
        :param id:
        """
        if not objChain and not isinstance(objChain, list) and not isinstance(objChain, tuple):
            raise Exception("必须提供状态的实际对象链才能创建状态！")
        if id:
            self.id = id
        else:
            self.id = str(uuid.uuid1()).replace("-", "")
        self.objChain = objChain
        self._knowledge = None # 已经生成的知识链
        self.Memory =memory

    def toObjChain(self, forceToNvwaObject=False):
        """
        转换成对象list列表
        :param forceToNvwaObject:是否将其他对象实强制转换成际对象或知识链等nvwa系统对象。进入Knowledge的，必须是实际对象或知识链等nvwa系统对象，所以forceToNvwaObject=True
        :return:
        """
        if not forceToNvwaObject:
            return self.objChain
        else:
            real_chain = self._changeToNvwaObject(self.objChain)
            return real_chain

    def _changeToNvwaObject(self,objChain):
        """
        将其他对象实强制转换成际对象或知识链等nvwa系统对象。进入Knowledge的，必须是实际对象或知识链等nvwa系统对象，所以forceToNvwaObject=True
        :param objChain:
        :return:
        """
        from loongtian.nvwa.models.baseEntity import BaseEntity
        from loongtian.nvwa.models.realObject import RealObject

        real_chain = []
        for obj in objChain:
            if isinstance(obj, BaseEntity):
                real_chain.append(obj)
            else:
                if isinstance(obj,list):
                    child_real_chain=self._changeToNvwaObject(obj)
                    real_chain.append(child_real_chain)
                elif isinstance(obj,dict):
                    child_real_chain = self._changeToNvwaObject(obj.values())
                    real_chain.append(child_real_chain)
                else:
                    real = RealObject(remark=obj,memory=self.Memory)
                    real_chain.append(real)

        return real_chain

    def createKnowledge(self, type=ObjType.KNOWLEDGE, recordInDB=True):
        """
        根据状态创建知识链
        :return:
        """
        if not self._knowledge:
            return self._knowledge
        from loongtian.nvwa.runtime.instinct import Instincts
        Instincts.loadAllInstincts(memory=self.Memory)  # 避免直觉系统未加载造成错误
        from loongtian.nvwa.models.knowledge import Knowledge
        # 进入Knowledge的，必须是实际对象或知识链等nvwa系统对象，所以forceToNvwaObject=True
        self._knowledge = Knowledge.createKnowledgeByObjChain(self.toObjChain(forceToNvwaObject=True),
                                                              type=type,
                                                              recordInDB=recordInDB,
                                                              memory=self.Memory)
        return self._knowledge

    def __repr__(self):
        return "{Status:{id:%s,objChain:%s}}" % (self.id,self.objChain)


class Step():
    """
    [运行时对象]workflow知识链每一步（包含多个status，knowledge）
    """

    def __init__(self, condition=None,id=None,memory=None):
        """
        [运行时对象]workflow知识链每一步（包含多个status，knowledge）
        :param condition:
        :param id:
        """

        if id:
            self.id = id
        else:
            self.id = str(uuid.uuid1()).replace("-", "")
        self.statuses = []

        if condition and (isinstance(condition, list) or isinstance(condition, tuple)):
            condition = Condition.createByConditionChain(condition)

        self.condition = condition
        self._knowledge = None  # 已经生成的知识链
        self.Memory = memory

    @staticmethod
    def createByStatusesObjChain(statusesObjChain, condition_objs=None,memory=None):
        """
        根据StatusChain创建step
        :param statusesObjChain:必须为二层嵌套的集合
        :return:
        """
        if not statusesObjChain and not isinstance(statusesObjChain, list) and not isinstance(statusesObjChain, tuple):
            raise Exception("必须提供多个状态的实际对象链才能创建步骤！")

        _step = Step(memory=memory)
        for statusObjChain in statusesObjChain:
            _status = Status(statusObjChain,memory=memory)
            _step.addStatus(_status)

        return _step

    def addStatus(self, status):
        """
        添加状态
        :param status:
        :return:
        """
        if not isinstance(status, Status):
            return  # 不抛出错误
        status.Memory=self.Memory
        self.statuses.append(status)

    def toObjChain(self, forceToNvwaObject=False):
        """
        转换成对象list列表（嵌套，这里将前置condition）
        :param forceToNvwaObject:是否将其他对象实强制转换成际对象或知识链等nvwa系统对象。进入Knowledge的，必须是实际对象或知识链等nvwa系统对象，所以forceToNvwaObject=True
        :return:
        """
        statuses_objChain = []
        for _status in self.statuses:
            status_objChain = _status.toObjChain(forceToNvwaObject)
            statuses_objChain.append(status_objChain)

        if self.condition:
            condition_objChain = self.condition.toObjChain()
            statuses_objChain = [condition_objChain, statuses_objChain]

        return statuses_objChain

    def createKnowledge(self, type=ObjType.KNOWLEDGE, recordInDB=True):
        """
        根据步骤的状态（可能有多个）创建知识链（每个步骤创建时，应该将condition作为域）
        :return:
        """
        if not self._knowledge:
            return self._knowledge
        from loongtian.nvwa.runtime.instinct import Instincts
        Instincts.loadAllInstincts(memory=self.Memory)  # 避免直觉系统未加载造成错误
        from loongtian.nvwa.models.knowledge import Knowledge
        # 进入Knowledge的，必须是实际对象或知识链等nvwa系统对象，所以forceToNvwaObject=True
        self._knowledge = Knowledge.createKnowledgeByObjChain(self.toObjChain(forceToNvwaObject=True), type=type,
                                                              recordInDB=recordInDB,
                                                              memory=self.Memory)

        # condition_klg = self.condition.createKnowledge()
        # # 关联两个知识链
        # # todo 应该在处理“如果...那么...”之后才能关联处理
        #
        return self._knowledge

    def __repr__(self):
        return "{Step:{id:%s,statuses:%s}}" % (self.id,self.statuses)


class Condition(Step):
    """
    [运行时对象]workflow知识链每一步迁移的条件（是一个对对象构成的描述集合）
    """

    @staticmethod
    def createByConditionChain(conditionChain):
        """

        :param conditionChain:
        :return:
        """


class Workflow(object):
    """
    [运行时对象]workflow工作流（ConditionedStep列表）
    """

    def __init__(self,id=None,memory=None):
        """
        [运行时对象]workflow工作流（Step列表(Step可能带条件Condition)）
        """
        if id:
            self.id = id
        else:
            self.id = str(uuid.uuid1()).replace("-", "")
        self.steps = []
        self._knowledge = None  # 已经生成的知识链
        self.Memory=memory

    @classmethod
    def createByObjChain(cls,objChain,memory=None):
        """
        根据对象链（实际对象、知识链）创建workflow工作流
        :param objChain: 可能为三层嵌套、二层嵌套以及单层的对象列表
        :return:
        """
        try:
            _workflow=cls.createByStepsObjChain(objChain,memory=memory)
        except:
            try:
                _workflow = cls.createByStatusesObjChain(objChain,memory=memory)
            except:
                try:
                    _workflow = cls.createByStatusObjChain(objChain,memory=memory)
                except:
                    return None
        return _workflow

    @classmethod
    def createByStepsObjChain(cls,stepsObjChain, conditionObjChain=None,memory=None):
        """
        根据对象链（实际对象、知识链）创建workflow工作流
        :param stepsObjChain: 必须为三层嵌套的集合
        :return:
        """

        if not stepsObjChain and not isinstance(stepsObjChain, list) and not isinstance(stepsObjChain, tuple):
            raise Exception("必须提供多个步骤的实际对象链才能创建workflow！")
        _workflow = cls()
        # i=0
        for step_objs in stepsObjChain:
            condition_objs = None
            # if conditionObjChain and (isinstance(conditionObjChain, list) or isinstance(conditionObjChain, tuple)):
            #     try:
            #         condition_objs = conditionObjChain[i]
            #     except Exception as ex: # todo 有可能取不到，目前不报错
            #         print (ex)
            #         pass

            _step = Step.createByStatusesObjChain(step_objs, condition_objs,memory=memory)
            _workflow.addStep(_step)
            # i+=1

        return _workflow

    @classmethod
    def createByStatusesObjChain(cls,statusesObjChain,memory=None):
        """
        根据对象链（实际对象、知识链）创建workflow工作流
        :param stepsObjChain: 必须为三层嵌套的集合
        :return:
        """

        if not statusesObjChain and not isinstance(statusesObjChain, list) and not isinstance(statusesObjChain, tuple):
            raise Exception("必须提供多个状态的实际对象链才能创建workflow！")
        _workflow = cls()

        _step = Step.createByStatusesObjChain(statusesObjChain, None,memory=memory)
        _workflow.addStep(_step)

        return _workflow

    @classmethod
    def createByStatusObjChain(cls, statusObjChain,memory=None):
        """
        根据对象链（实际对象、知识链）创建workflow工作流
        :param stepsObjChain: 必须为三层嵌套的集合
        :return:
        """

        if not statusObjChain and not isinstance(statusObjChain, list) and not isinstance(statusObjChain, tuple):
            raise Exception("必须提供状态的实际对象链才能创建workflow！")
        _workflow = cls(memory=memory)

        _step = Step(memory=memory)
        _status=Status(statusObjChain,memory=memory)
        _step.addStatus(_status)
        _workflow.addStep(_step)

        return _workflow


    @classmethod
    def createByKnowledge(cls, knowledge,memory=None):
        """
        根据对象链（实际对象、知识链）创建workflow工作流
        :param knowledge: 可能为三层嵌套、二层嵌套以及单层的知识链
        :return:
        """
        try:
            _workflow=cls.createByFullKnowledge(knowledge,memory=memory)
        except:
            try:
                _workflow = cls.createByStepKnowledge(knowledge,memory=memory)
            except:
                try:
                    _workflow = cls.createByStatusKnowledge(knowledge,memory=memory)
                except:
                    return None
        return _workflow


    @classmethod
    def createByFullKnowledge(cls,workflow_knowledge,memory=None):
        """
        根据多步骤、多状态知识链生成workflow
        :param step_knowledge: 三层嵌套知识链
        :return:
        """
        from loongtian.nvwa.models.knowledge import Knowledge
        _workflow = cls(memory=memory)

        _workflow_knowledge_components = workflow_knowledge.getSequenceComponents()
        if not _workflow_knowledge_components:
            raise Exception("未能正确取得workflow的步骤元素！")
        # 步骤
        for step in _workflow_knowledge_components:  # 步骤知识链（可能有多个，代表不同的步骤）
            step_obj_chain=step
            if isinstance(step, Knowledge):
                # 取得实际元素
                step_obj_chain = step.getSequenceComponents()

            if not isinstance(step_obj_chain,list):
                raise Exception("未能正确取得workflow的步骤!")

            # 状态
            _step = Step(memory=memory)
            for status in step_obj_chain:
                status_obj_chain = status
                if isinstance(status, Knowledge):
                    status_obj_chain = status.getSequenceComponents()

                if not isinstance(status_obj_chain, list):
                    raise Exception("未能正确取得workflow的状态!")
                _status = Status(status_obj_chain,memory=memory)
                _step.addStatus(_status)

            _workflow.addStep(_step)

        # 记录到已经生成的知识链
        _workflow._knowledge=workflow_knowledge

        return _workflow


    @classmethod
    def createByStepKnowledge(cls,step_knowledge,memory=None):
        """
        根据单一的步骤知识链生成workflow
        :param step_knowledge: 两层嵌套知识链
        :return:
        """

        from loongtian.nvwa.models.knowledge import Knowledge
        _workflow = cls(memory=memory)

        _step_knowledge_components = step_knowledge.getSequenceComponents()
        if not _step_knowledge_components:
            raise Exception("未能正确取得workflow的步骤！")
        # 步骤

            # 状态
        _step = Step(memory=memory)
        for status in _step_knowledge_components:
            status_obj_chain = status
            if isinstance(status, Knowledge):
                status_obj_chain = status.getSequenceComponents()

            if not isinstance(status_obj_chain, list):
                raise Exception("未能正确取得workflow的状态!")
            _status = Status(status_obj_chain,memory=memory)
            _step.addStatus(_status)

            _workflow.addStep(_step)

        # 记录到已经生成的知识链
        _workflow.createKnowledge(recordInDB=False,memory=memory)

        return _workflow

    @classmethod
    def createByStatusKnowledge(cls,status_knowledge,memory=None):
        """
        根据单一的状态知识链生成workflow
        :param status_knowledge: 单层知识链
        :return:
        """

        _workflow = cls(memory=memory)

        _status_knowledge_components = status_knowledge.getSequenceComponents()
        if not _status_knowledge_components:
            raise Exception("未能正确取得workflow的状态元素！")
        # 步骤
        _step = Step(memory=memory)
        # 状态
        _status = Status(_status_knowledge_components,memory=memory)
        _step.addStatus(_status)

        _workflow.addStep(_step)

        # 记录到已经生成的知识链
        _workflow.createKnowledge(recordInDB=False,memory=memory)

        return _workflow

    # def addStepByObjChain(self, step_objs,condition_objs=None):
    #     _step = Step.createByStatusesObjChain(step_objs, condition_objs)
    #     self.addStep(_step)

    def addStep(self, step):
        """
        添加步骤
        :param step:
        :return:
        """
        if not isinstance(step, Step):
            return  # 不抛出错误
        step.Memory=self.Memory
        self.steps.append(step)

    def toObjChain(self, forceToNvwaObject=False,simplified=False):
        """
        将当前workflow转化为实际对象链（嵌套）
        :param forceToNvwaObject:是否将其他对象实强制转换成际对象或知识链等nvwa系统对象。进入Knowledge的，必须是实际对象或知识链等nvwa系统对象，所以forceToNvwaObject=True
        :param simplified:是否将实际对象链不断扒皮：[[[a,b,c]]]——> [a,b,c]
        :return:
        """
        steps_objChain = []
        for _step in self.steps:
            step_objChain = _step.toObjChain(forceToNvwaObject)
            steps_objChain.append(step_objChain)

        if simplified:
            steps_objChain=self._simplified_objChain(steps_objChain)

        return steps_objChain

    def _simplified_objChain(self,objChain):
        """
        将实际对象链不断扒皮：[[[a,b,c]]]——> [a,b,c]
        :param objChain:
        :return:
        """
        if not self._is_simplified_objChain(objChain):
            objChain=objChain[0]
            return self._simplified_objChain(objChain)
        return objChain

    def _is_simplified_objChain(self,objChain):
        if  len(objChain) > 1:
            return False
        for obj in objChain:
            if not isinstance(obj,list) and not isinstance(obj,tuple):
                return True

        return False


    def createKnowledge(self,
                        type=ObjType.KNOWLEDGE,
                        recordInDB=True,
                        useSimplifiedObjChain=False,
                        understood_ratio=1.0,
                        memory=None):
        """
        根据workflow的步骤（可能有多个）创建知识链（每个步骤创建时，应该将condition作为域）
        :return:
        """
        if self._knowledge: # 如果已经取得了，直接返回
            return self._knowledge
        from loongtian.nvwa.runtime.instinct import Instincts
        Instincts.loadAllInstincts(memory=self.Memory)  # 避免直觉系统未加载造成错误
        from loongtian.nvwa.models.knowledge import Knowledge
        # 进入Knowledge的，必须是实际对象或知识链等nvwa系统对象，所以forceToNvwaObject=True
        self._knowledge = Knowledge.createKnowledgeByObjChain(self.toObjChain(forceToNvwaObject=True,simplified=useSimplifiedObjChain), type=type,
                                                              recordInDB=recordInDB,
                                                              understood_ratio=understood_ratio,
                                                              memory=memory)
        return self._knowledge

    def __repr__(self):
        return "{Workflow:{id:%s,steps:%s}}" % (self.id,self.steps)
