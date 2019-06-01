#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

from loongtian.nvwa.models.metaData import MetaData
from loongtian.nvwa.models.enum import ObjType
from loongtian.nvwa.runtime.collection import Collection
from loongtian.nvwa.runtime.systemInfo import SystemInfo
from loongtian.nvwa.runtime.instinct import Instincts
from loongtian.nvwa.language import InstinctsText, InnerOperationsErrors
from loongtian.nvwa.organs.character import Character

"""
系统内部做处理时的操作映射
所有的inner operation的参数，均由placeholder按顺序传入
"""


class _InnerOperations():
    """
    [运行时对象]女娲系统内部操作对象的封装类。
    """

    def __init__(self):
        self.InnerOperationsIdDict = {}
        self.InnerOperations = []
        self.InnerOperationsMValueDict = {}
        self._InnerOperationMap = None  # 女娲系统的内部操作对象与操作函数的映射

        ######################################
        #    操作对象的实际对象（系统内置）
        ######################################
        # 女娲系统内部操作的标记符
        self.operation_mark = None

        # 创建实际对象的可执行信息
        self.operation_CreateExcutionInfo = None

        # 保证同一性的操作（两个对象变一个对象，同步Id）
        self.operation_realSynchronization = None

    def createMeta(self, memory=None):
        """
        加载元数据
        :return:
        """

        ######################################
        #    操作对象的元数据对象（系统内置）
        ######################################
        # 女娲系统内部操作的标记符 2019-01-31：经慎重思考，女娲系统内部操作可向外部显现（leon）
        self.meta_operation_mark = MetaData(mvalue=InstinctsText.inner_operation,
                                            weight=Character.System_Obj_Weight * 100,
                                            memory=memory).create()

        # 创建实际对象的可执行信息
        self.meta_operation_createExcutionInfo = MetaData(mvalue=InstinctsText.inner_operation_createExcutionInfo,
                                                          weight=Character.System_Obj_Weight * 10,
                                                          memory=memory).create()

        # 保证同一性的操作（两个对象变一个对象，同步Id）
        self.meta_operation_realSynchronization = MetaData(mvalue=InstinctsText.inner_operation_Synchronization,
                                                           weight=Character.System_Obj_Weight * 10,
                                                           memory=memory).create()

        self.mvalue_metas_dict = {
            # 女娲系统内部操作的标记符
            self.meta_operation_mark.mvalue: self.meta_operation_mark,
            # 创建实际对象的可执行信息
            self.meta_operation_createExcutionInfo.mvalue: self.meta_operation_createExcutionInfo,

            # 保证同一性的操作（两个对象变一个对象，同步Id）
            self.meta_operation_realSynchronization.mvalue: self.meta_operation_realSynchronization,

        }

    def createInnerOperationByMeta(self, meta):
        """
        根据元数据创女娲系统内部操作对象的实际对象
        :param meta:
        :return:
        """
        # meta = meta.create()
        from loongtian.nvwa.models.realObject import RealObject
        real = RealObject.createRealByMeta(meta,
                                           weight=meta.weight,
                                           checkExist=True,
                                           realType=ObjType.INNER_OPERATION,
                                           status=800,
                                           recordInDB=True)
        self.InnerOperationsIdDict[real.id] = real
        self.InnerOperationsMValueDict[meta.mvalue] = real
        return real

    def _createAllInnerOperations(self):
        """
        创建所有直觉（包括属性、组件等顶级关系，意思是等分层“标签”）
        :return:
        """
        try:
            # 女娲系统内部操作的标记符
            self.operation_mark = self.createInnerOperationByMeta(self.meta_operation_mark)

            # 创建实际对象的可执行信息
            self.operation_CreateExcutionInfo = self.createInnerOperationByMeta(
                self.meta_operation_createExcutionInfo)

            # 保证同一性的操作（两个对象变一个对象，同步Id）
            self.operation_realSynchronization = self.createInnerOperationByMeta(
                self.meta_operation_realSynchronization)

            # 添加到直觉对象列表
            self.InnerOperations.extend([
                # 女娲系统内部操作的标记符
                self.operation_mark,
                # 元对象（基础对象）
                self.operation_CreateExcutionInfo,
                # 保证同一性的操作（两个对象变一个对象，同步Id）
                self.operation_realSynchronization,

            ])

            return self.InnerOperations
        except Exception as e:
            raise Exception(InnerOperationsErrors.Can_Not_Create_InnerOperation % str(e))

    def checkInnerOperations(self):
        """
        检查加载的女娲系统内部操作对象的实际对象是否符合nvwa内部定义
        :return:
        """
        li1 = self.InnerOperationsMValueDict.keys()
        li1.sort()
        li2 = self.mvalue_metas_dict.keys()
        li2.sort()
        return li1 == li2

    def loadAllInnerOperations(self, forceToReload=False, memory=None):
        """
        加载所有女娲系统内部操作对象的实际对象
        :param forceToReload:
        :return:
        """
        # 从内存加载
        if not forceToReload and len(self.InnerOperationsIdDict) > 0:
            return list(self.InnerOperationsIdDict.values())

        # 加载元数据
        self.createMeta(memory=memory)
        # 从数据库加载
        try:
            from loongtian.nvwa.models.realObject import RealObject
            Operations = RealObject.getAllByConditionsInDB(memory=memory, type=ObjType.INNER_OPERATION)

            # 记录到内存中
            if Operations:
                if isinstance(Operations, list):
                    for Operation in Operations:
                        self.setInnerOperation(Operation)
                else:
                    self.setInnerOperation(Operations)

                if not self.checkInnerOperations():
                    Operations = self._createAllInnerOperations()
            else:
                Operations = self._createAllInnerOperations()

            # 将女娲系统的内部操作对象映射到操作函数
            self._InnerOperationMap = {

                SystemInfo.InnerOperationInfo.Union: Collection.union,
                SystemInfo.InnerOperationInfo.Difference: Collection.difference,
                SystemInfo.InnerOperationInfo.Intersection: Collection.intersection,

                self.operation_CreateExcutionInfo: InnerOperation_CreateExcutionInfo,
                self.operation_realSynchronization: InnerOperation_RealSynchronization,
            }

            return Operations
        except Exception as e:
            raise Exception(InnerOperationsErrors.Load_InnerOperations_Failure + str(e))

    def setInnerOperation(self, Operation):
        """
        将数据库加载的女娲系统内部操作对象的实际对象与当前类中的定义对象关联在一起
        :param Operation:
        :return:
        """
        self.InnerOperationsIdDict[Operation.id] = Operation
        if Operation.remark:
            self.InnerOperationsMValueDict[Operation.remark] = Operation

        # 将Operation赋予_InnerOperations中的对象
        # 女娲系统内部操作的标记符
        if Operation.remark == self.meta_operation_mark.mvalue:
            self.operation_mark = Operation
            self.meta_operation_mark.Layers.addLower(Operation, recordInDB=False)  # 关联meta和real
        # 创建实际对象的可执行信息
        elif Operation.remark == self.meta_operation_createExcutionInfo.mvalue:
            self.operation_CreateExcutionInfo = Operation
            self.meta_operation_createExcutionInfo.Layers.addLower(Operation, recordInDB=False)  # 关联meta和real

        # 保证同一性的操作（两个对象变一个对象，同步Id）
        elif Operation.remark == self.meta_operation_realSynchronization.mvalue:
            self.operation_realSynchronization = Operation
            self.meta_operation_realSynchronization.Layers.addLower(Operation, recordInDB=False)  # 关联meta和real

    @property
    def InnerOperationMap(self):
        """
        取得女娲系统的内部操作对象与操作函数的映射
        :return:
        """
        # 如果不存在，强制加载
        if not InnerOperations._InnerOperationMap:
            InnerOperations.loadAllInnerOperations(forceToReload=True)
        # 如果仍不存在，抛出错误
        if not InnerOperations._InnerOperationMap:
            raise Exception("无法取得女娲系统的内部操作对象与操作函数的映射，请检查系统!")

        return InnerOperations._InnerOperationMap

    @staticmethod
    def createMeaningExecutionInfo(memory=None):
        """
        创建“意义为”的执行信息（pattern、meaning，其中的meaning对应到内部操作）
        :return:
        """
        from loongtian.nvwa.models.realObject import RealObject
        Instincts.loadAllInstincts(memory=memory)
        meaning_real = Instincts.instinct_meaning
        if not meaning_real or not isinstance(meaning_real, RealObject):
            return None

        # 如果已经存在，直接返回
        meaning_real_exeinfo = meaning_real.ExecutionInfo.getSelfLinearExecutionInfo()
        if meaning_real_exeinfo and meaning_real_exeinfo.isExecutable():
            return meaning_real_exeinfo

        # 左占位符
        left_placeholder = RealObject(remark="placeholder", type=ObjType.PLACEHOLDER, memory=memory).create(
            recordInDB=True)
        # 对占位符的父对象进行限定-知识链（实际对象列表）
        left_placeholder.Constitutions.addParent(Instincts.instinct_original_knowledge, recordInDB=True,
                                                 weight=Character.Inner_Instinct_Link_Weight)
        # 右占位符
        right_placeholder = RealObject(remark="placeholder", type=ObjType.PLACEHOLDER, memory=memory).create(
            recordInDB=True)
        # 对占位符的父对象进行限定-知识链（实际对象列表）
        right_placeholder.Constitutions.addParent(Instincts.instinct_original_knowledge, recordInDB=True,
                                                  weight=Character.Inner_Instinct_Link_Weight)

        from loongtian.nvwa.models.knowledge import Knowledge
        pattern_klg = Knowledge.createKnowledgeByObjChain([left_placeholder, meaning_real, right_placeholder],
                                                          type=ObjType.LINEAR_EXE_INFO,
                                                          understood_ratio=Character.Inner_Instinct_Link_Weight,
                                                          recordInDB=True,
                                                          memory=memory)
        # 关联可执行对象及其pattern
        meaning_real.Layers.addLower(pattern_klg, recordInDB=True,
                                     weight=Character.Inner_Instinct_Link_Weight)

        # 对应到内部操作（为保证一致性(有强制检查)，使用Workflow）：
        from loongtian.nvwa.runtime.meanings import Meaning
        meaning = Meaning.createByStepsObjChain(
            [[[InnerOperations.operation_mark, InnerOperations.operation_CreateExcutionInfo]]])
        meaning_klg = meaning.createKnowledge(type=ObjType.LINEAR_EXE_INFO, recordInDB=True,
                                              understood_ratio=Character.Inner_Instinct_Link_Weight,
                                              memory=memory)
        pattern_klg.Layers.addLower(meaning_klg, recordInDB=True, weight=Character.Inner_Instinct_Link_Weight)

        meaning_real.ExecutionInfo.LinearExecutionInfo.add(pattern_klg, meaning_klg, value_placeholder=None)

    @staticmethod
    def createTopRelationExecutionInfo(memory=None):
        """
        创建所有顶级关系的执行信息（pattern、meaning，meaning、pattern相等。除了顶级关系，对象不能被用来解释自身！）
        :return:
        """
        from loongtian.nvwa.models.realObject import RealObject
        Instincts.loadAllInstincts(memory=memory)
        for top_real in Instincts.TopRelations:
            if not top_real or not isinstance(top_real, RealObject):
                continue

            # if top_real is Instincts.instinct_parent:
            #     a=1
            # 如果已经存在，直接返回
            top_real_exeinfo = top_real.ExecutionInfo.getSelfLinearExecutionInfo()
            if top_real_exeinfo and top_real_exeinfo.isExecutable():
                continue

            # 左占位符
            left_placeholder = RealObject(remark="placeholder",
                                          type=ObjType.PLACEHOLDER,
                                          memory=memory).create(recordInDB=True)
            # 对占位符的父对象进行限定-实际对象/知识链（实际对象列表），这个地方应该很灵活
            left_placeholder.Constitutions.addParent(Instincts.instinct_original_object, recordInDB=True,
                                                     weight=Character.Inner_Instinct_Link_Weight)

            # 右占位符
            right_placeholder = RealObject(remark="placeholder",
                                           type=ObjType.PLACEHOLDER,
                                           memory=memory).create(recordInDB=True)
            # 对占位符的父对象进行限定-实际对象/知识链（实际对象列表），这个地方应该很灵活
            right_placeholder.Constitutions.addParent(Instincts.instinct_original_object, recordInDB=True,
                                                      weight=Character.Inner_Instinct_Link_Weight)
            # right_placeholder.Constitutions.addParent(Instincts.instinct_original_knowledge)

            from loongtian.nvwa.models.knowledge import Knowledge
            pattern_components = [left_placeholder, top_real, right_placeholder]
            pattern_klg = Knowledge.createKnowledgeByObjChain(pattern_components, ObjType.LINEAR_EXE_INFO,
                                                              understood_ratio=Character.Inner_Instinct_Link_Weight,
                                                              recordInDB=True,
                                                              memory=memory)  # ,recordRelationInFirstReal=True)
            # 关联可执行对象及其pattern
            top_real.Layers.addLower(pattern_klg, weight=Character.Inner_Instinct_Link_Weight, recordInDB=True)

            # 顶级关系的meaning、pattern相等。类似于：牛-组件-腿 意义为 牛-组件-腿。除了顶级关系，对象不能被用来解释自身！
            # （为保证一致性(有强制检查)，使用Meaning）
            from loongtian.nvwa.runtime.meanings import Meaning
            meaning = Meaning.createByStepsObjChain([[pattern_components]])
            meaning_klg = meaning.createKnowledge(type=ObjType.LINEAR_EXE_INFO, recordInDB=True,
                                                  understood_ratio=Character.Inner_Instinct_Link_Weight,
                                                  memory=memory)
            pattern_klg.Layers.addLower(meaning_klg, recordInDB=True, weight=Character.Inner_Instinct_Link_Weight)

            # 建立值
            value_placeholder = None
            if Instincts.hasConstituentValue(top_real):
                value_placeholder = RealObject(remark="placeholder",
                                               type=ObjType.PLACEHOLDER,
                                               memory=memory).create(recordInDB=True)
                # 关联值到意义，对占位符的父对象进行限定-实际对象/知识链（实际对象列表），这个地方应该很灵活
                # value_placeholder.Constitutions.addParent(right_placeholder,recordInDB=True, weight=Character.Inner_Instinct_Link_Weight)
                meaning_klg.Layers.addLower(value_placeholder, ltype=ObjType.LINEAR_EXE_MEANING_VALUE,
                                            weight=Character.Inner_Instinct_Link_Weight, recordInDB=True)

            top_real.ExecutionInfo.LinearExecutionInfo.add(pattern_klg, meaning_klg, value_placeholder)

    @staticmethod
    def createRealsSynchronizer(memory=None):
        """
        保证对象同一性的操作（两个对象变一个对象，同步Id）执行信息
        :return:
        """
        from loongtian.nvwa.models.realObject import RealObject
        Instincts.loadAllInstincts(memory=memory)
        _real = Instincts.instinct_realSynchronizer
        if not _real or not isinstance(_real, RealObject):
            return None

        # 如果已经存在，直接返回
        meaning_real_exeinfo = _real.ExecutionInfo.getSelfLinearExecutionInfo()
        if meaning_real_exeinfo and meaning_real_exeinfo.isExecutable():
            return meaning_real_exeinfo

        # 左占位符
        left_placeholder = RealObject(remark="placeholder", type=ObjType.PLACEHOLDER, memory=memory).create(
            recordInDB=True)
        # 对占位符的父对象进行限定-实际对象
        left_placeholder.Constitutions.addParent(Instincts.instinct_original_object, recordInDB=True,
                                                 weight=Character.Inner_Instinct_Link_Weight)
        # 右占位符
        right_placeholder = RealObject(remark="placeholder", type=ObjType.PLACEHOLDER, memory=memory).create(
            recordInDB=True)
        # 对占位符的父对象进行限定-实际对象
        right_placeholder.Constitutions.addParent(Instincts.instinct_original_object, recordInDB=True,
                                                  weight=Character.Inner_Instinct_Link_Weight)

        from loongtian.nvwa.models.knowledge import Knowledge
        pattern_klg = Knowledge.createKnowledgeByObjChain([left_placeholder, _real, right_placeholder],
                                                          type=ObjType.LINEAR_EXE_INFO,
                                                          understood_ratio=Character.Inner_Instinct_Link_Weight,
                                                          recordInDB=True,
                                                          memory=memory)
        # 关联可执行对象及其pattern
        _real.Layers.addLower(pattern_klg, recordInDB=True,
                              weight=Character.Inner_Instinct_Link_Weight)

        # 对应到内部操作（为保证一致性(有强制检查)，使用Meaning/Workflow）：
        from loongtian.nvwa.runtime.meanings import Meaning
        meaning = Meaning.createByStepsObjChain(
            [[[InnerOperations.operation_mark, InnerOperations.operation_realSynchronization]]])
        meaning_klg = meaning.createKnowledge(type=ObjType.LINEAR_EXE_INFO, recordInDB=True,
                                              understood_ratio=Character.Inner_Instinct_Link_Weight,
                                              memory=memory)
        pattern_klg.Layers.addLower(meaning_klg, recordInDB=True, weight=Character.Inner_Instinct_Link_Weight)

        _real.ExecutionInfo.LinearExecutionInfo.add(pattern_klg, meaning_klg, value_placeholder=None)


# 向外部显现内部操作
InnerOperations = _InnerOperations()


def InnerOperation_CreateExcutionInfo(pattern, meaning, memory=None):
    """
    [运行时对象-内部操作]创建实际对象的执行信息
    :param pattern: 实际对象链或知识链
    :param meaning:实际对象链或知识链
    :return:
    """

    # 检查参数
    if not pattern or not meaning:
        raise Exception("必须提供参数left_know及right_know！")

    # “意义”的两边至少是个三元组，需要进一步判断
    from loongtian.nvwa.models.realObject import RealObject
    from loongtian.nvwa.models.knowledge import Knowledge
    pattern_components = None
    if isinstance(pattern, RealObject) or isinstance(pattern, Knowledge):
        pattern_components = pattern.getSequenceComponents()
    elif isinstance(pattern, list):
        pattern_components = pattern

    if not pattern_components:
        raise Exception("参数错误！“意义”的左边pattern没有定义！")

    meaning_components = None
    if isinstance(meaning, RealObject) or isinstance(meaning, Knowledge):
        meaning_components = meaning.getSequenceComponents()
    elif isinstance(meaning, list):
        meaning_components = meaning

    if not meaning_components:
        raise Exception("参数错误！“意义”的右边meaning没有定义！")
    if len(meaning_components) < 3:
        raise Exception("参数错误！“意义”的右边meaning至少是个三元组，例如：牛-组件-腿。目前是：%s" % meaning_components)

    hasTopRelation = False
    for meaning_component in meaning_components:
        if isinstance(meaning_component, RealObject) and meaning_component.isTopRelation():
            hasTopRelation = True
            break

    if hasTopRelation and len(pattern_components) < 3:
        raise Exception("参数错误！“意义”的的右边具有顶级关系，左边pattern至少是个三元组，例如：牛-组件-腿。目前是：%s" % pattern_components)

    from loongtian.nvwa.engines.modelingEngine import ModelingEngine

    # 两者相差，得出即将创建意义的动作对象，
    # 例如：牛-有-腿  牛-组件-腿，两者相差，得出“有”是动作，或是多动作【因为...所以...】
    action = ModelingEngine.getAction(pattern_components, meaning_components)
    if action:
        # todo 由于尚未建立时间概念，这里是临时替代方案
        # from loongtian.nvwa.runtime.meanings import Meaning
        meaning_components = [[meaning_components]]  # 三层嵌套(本身已经有一层了)
        meaning_value = None

    else:  # 没能找到action。这里有第二种情况，要创建的意义左边对象（将其作为一个整体）就是意义右边要输出的对象，
        # 例如：小明的手机意义real-（小明的手机）是手机小明有real-（小明的手机）

        meaning_components, meaning_value = ModelingEngine.regroupMeaningComponentsByPattern(meaning_components,
                                                                                             pattern_components,
                                                                                             memory=memory)
        if meaning_components is None:
            raise Exception("未能根据左边的模式重新构建（分组）意义！")

        # todo 这里应区分实体的“头”（例如：牛有头）和做成动作的“头”-例如：“四头牛”
        action = ModelingEngine.getAction(pattern_components, meaning_components)
        if not action:
            raise Exception("未能根据左边的模式及重新构建（分组）意义取得动作！")
        meaning_components = [[meaning_components]]  # 三层嵌套(本身已经有一层了)

    # 创建模式、意义、意义值的关联。
    if isinstance(action,list) and len(action)>1: # 多动作
        result = ModelingEngine.createExcutionInfo(action,
                                                   pattern_components,
                                                   meaning_components,
                                                   meaning_value=meaning_value,
                                                   pattern_type=ObjType.CONJUGATED_EXE_INFO,
                                                   meaning_type=ObjType.CONJUGATED_EXE_INFO,
                                                   meaning_value_type=ObjType.CONJUGATED_EXE_MEANING_VALUE,
                                                   recordInDB=True,
                                                   memory=memory)
    else: # 单动作
        result = ModelingEngine.createExcutionInfo(action,
                                                   pattern_components,
                                                   meaning_components,
                                                   meaning_value=meaning_value,
                                                   pattern_type=ObjType.LINEAR_EXE_INFO,
                                                   meaning_type=ObjType.LINEAR_EXE_INFO,
                                                   meaning_value_type=ObjType.LINEAR_EXE_MEANING_VALUE,
                                                   recordInDB=True,
                                                   memory=memory)
    if result:
        from loongtian.nvwa.runtime.meanings import ExecutionInfoCreatedMeaning,ExecutionInfoCreatedMeanings
        if len(result)==1:
            exe_info, new_created =result[action]
            return ExecutionInfoCreatedMeaning(action, pattern, meaning, new_created)
        else:
            _ExecutionInfoCreatedMeanings=ExecutionInfoCreatedMeanings()
            for _action in action:
                exe_info, new_created=result[_action]
                exe_info.restoreCurObjIndex()
                cur_pattern,cur_meaning,cur_meaning_value=exe_info.getCur()
                exe_info.restoreCurObjIndex()
                _result= ExecutionInfoCreatedMeaning(_action, cur_pattern, cur_meaning, new_created)
                _ExecutionInfoCreatedMeanings.append(_result)
            return _ExecutionInfoCreatedMeanings


def InnerOperation_RealSynchronization(obj1, obj2, memory=None):
    """
    保证同一性的操作（两个对象变一个对象，同步Id）
    :param obj1:
    :param obj2:
    :param memory:
    :return:
    """
    if obj1.id == obj2.id:
        return True
    # TODO 同步两个对象


"""
从一个organ到另一个organ的各种操作应该建立起来一个map(映射表)，代表了不同能力，比如记忆能力，就是从临时记忆区到短时记忆区再到长时记忆区的创建（create）的能力，以及不断重复后，增加其权重的值的大小
"""
OrganOperationMap = {

}
