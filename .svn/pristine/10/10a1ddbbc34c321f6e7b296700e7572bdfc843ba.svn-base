#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Leon'

from loongtian.nvwa.engines.engineBase import ThinkEngineBase

from loongtian.nvwa.models.enum import ObjType
from loongtian.nvwa.models.baseEntity import BaseEntity
from loongtian.nvwa.models.realObject import RealObject
from loongtian.nvwa.models.knowledge import Knowledge

from loongtian.nvwa.runtime.instinct import Instincts

from loongtian.util.text.edit_distance import SequenceMatcher

"""
建模引擎。
1、构成角度：泛化抽象出类 ，牛是动物，能吃草，马是动物，能吃草，抽象出食草动物。
2、知识链角度：
  （1）抽取关键字（集合模式）
  （2）结构的角度。
      a.修限关系，如RRR（中国人民银行），可提取为R。
      b.当一个句子中出现多个C时，提取模式。5253545556……
      c.因为K1所以K2。先对K1和K2进行分组，最后做C的模式。
  （3）知识链的语义角度：
      a.强关联，天下雨——天冷，超过一定阀值，就可自动推导。
      b.阈值。西游记里，猪能说话。其他地方是不对的，不一定强关联，但仍可以推导。
3.语义:意义为。根据输入创建意义的模式。模式分层，意义递进。
"""


class ModelingEngine(ThinkEngineBase):
    """
    建模引擎。
    :rawParam
    :attribute
    """

    def __init__(self, thinkingCentral):
        """
        建模引擎。
        :param memoryCentral:
        """
        super(ModelingEngine, self).__init__(thinkingCentral)

    @staticmethod
    def createExcutionInfo(executable,
                           patten, meaning, meaning_value=None,
                           memory=None, recordInDB=False):
        """
        创建可执行性信息。根据输入的实际对象链提取/创建模式pattern、提取/创建意义meaning。左右形式及左右对象类别
        :param executable 可执行性的实际对象（包括Instinct\Action\Modifier\Knowledge[因为...所以...]）
        :param patten_objs:用来创建模式的对象列表（realObject、knowledge、collection），是一个线性结构列表，一个可执行的实际对象可以有多个模式，例如：我知道中国人民解放军，r1-知道-r2;我知道中国人民解放军是最棒的，r1-知道-k1
        :param meaning_objs:用来创建意义的列表（realObject、knowledge、collection），其标准格式为：
        [ # steps：意义对应的每一步知识链:step1-step2...
            [ # statuses:每一步知识链的的转换模式（一个状态集合，可以有多个状态转换）：status1,status2...
                [self.real_niu,self.brain.MemoryCentral.Instincts.instinct_component,self.real_tui], # knowledge知识链第一步中包含的第一个knowledge，是一个线性结构
            ],
        ]
        :return:
        """
        # 牛有腿，马有腿，羊有腿，提取出 动物有腿，桌子有腿，凳子有腿，机器人有腿，提取出 元对象有腿。同理，元对象有元对象(组件关系)，这里将是两个元对象的实例
        # 例如：id1是id1，
        # 牛是动物，
        # 苹果是红色
        # 1是[1,2,3]的元素，
        # 桌子1是桌子，
        # 太阳东升西落是对的
        # 牛组件腿，腿是牛的组件

        # 检查参数
        if executable is None:
            raise Exception("必须提供可执行的实际对象（Instinct\Action\Modifier\Knowledge[因为...所以...]）才能创建pattern！")
        if not patten or not meaning:
            raise Exception("必须提供参数patten及meaning！")

        if isinstance(patten, list):
            patten_objs = patten
        elif isinstance(patten, Knowledge):
            patten_objs = patten.getSequenceComponents()
        else:
            raise Exception("patten必须为知识链或list！")

        if isinstance(meaning, list):
            meaning_objs = meaning
        elif isinstance(meaning, Knowledge):
            meaning_objs = meaning.getSequenceComponents()
        else:
            raise Exception("meaning必须为知识链或list！")

        # 检查executable、patten_objs、meaning_objs及其关系
        ModelingEngine.checkPattenAndMeaningObjs(executable, patten_objs, meaning_objs)

        # 真正创建可执行信息
        if isinstance(executable, RealObject):
            # 为实际对象提取/创建模式pattern、提取/meaning
            return ModelingEngine._createRealObjectExecutionInfo(executable,
                                                                 patten_objs,
                                                                 meaning_objs,
                                                                 meaning_value,
                                                                 memory=memory,
                                                                 recordInDB=recordInDB)
        # 为多实际对象，例如：[因为...所以...]提取/创建模式pattern、提取/meaning
        elif isinstance(executable, list):  # 例如：因为placeholder-k1所以placeholder-k2,这是一种模式，应该创建一个对象代表之
            return ModelingEngine._createRealChainExecutionInfo(executable,
                                                                patten_objs,
                                                                meaning_objs,
                                                                meaning_value,
                                                                memory=memory)
        elif isinstance(executable, Knowledge):  # 例如：因为placeholder-k1所以placeholder-k2,这是一种模式，应该创建一个对象代表之
            executable.getChainItems()
            if executable.s_chain != patten_objs:
                raise Exception("当前Knowledge与提供的实际对象链不相同，无法创建pattern！")

            return ModelingEngine._createKnowledgeExecutionInfo(executable,
                                                                patten_objs,
                                                                meaning_objs,
                                                                meaning_value,
                                                                memory=memory)

    @staticmethod
    def checkPattenAndMeaningObjs(executable, patten_objs, meaning_objs):
        """
        检查executable、patten_objs、meaning_objs及其关系
        :param patten_objs:
        :param meaning_objs:
        :return:
        """
        if patten_objs is None:
            raise Exception("必须提供实际对象链才能创建pattern！")

        if meaning_objs is None:
            raise Exception("必须提供实际对象链才能创建meaning！")

        # 2018-09-26 不再检查type，因为Action本是一种具有pattern和meaning的realobject，区别是形式上的，后面赋义后会更改其type
        # if isinstance(executable, RealObject):
        #     if not ObjType.isExecutable(executable.type):
        #         raise Exception("当前实际对象为不可执行的实际对象（Instinct\Action\Modifier，无法创建pattern！")

        # 0、检查patten_objs
        if isinstance(patten_objs, list) or isinstance(patten_objs, tuple):
            if len(patten_objs) < 1:
                raise Exception("实际对象链的数量必须大于等于1，才能创建pattern！")

        if isinstance(executable, list):
            for _executable in executable:
                if not _executable in patten_objs:
                    raise Exception("当前实际对象不在提供的模式对象链中，无法创建pattern！")

        else:
            if not executable in patten_objs:
                raise Exception("当前实际对象不在提供的模式对象链中，无法创建pattern！")

        # 1、检查meaning_objs
        if meaning_objs is None or (not isinstance(meaning_objs, list) and not isinstance(meaning_objs, tuple)):
            raise Exception("必须提供实际对象链才能创建meaning！")
        for step_objs in meaning_objs:
            if (not isinstance(step_objs, list) and not isinstance(step_objs, tuple)):
                raise Exception("必须提供实际对象链才能创建meaning的步骤！")
            for status_objs in step_objs:
                if (not isinstance(status_objs, list) and not isinstance(status_objs, tuple)):
                    raise Exception("必须提供实际对象链才能创建meaning的步骤中的状态！")

        if len(meaning_objs) < 1 or len(meaning_objs[0]) < 1 or len(meaning_objs[0][0]) < 1:
            raise Exception("实际对象链的数量必须大于等于1，才能创建meaning！")

        from loongtian.nvwa.runtime.instinct import Instincts

        # 2、继续判断executable 与patten_objs、meaning_objs的关系
        # todo 暂未考虑[因为...所以...]
        if isinstance(executable, list):
            for _executable in executable:
                if _executable in meaning_objs and not _executable in Instincts.TopRelations:
                    raise Exception("当前实际对象位于意义对象链中，除了顶级关系，对象不能被用来解释自身！无法创建pattern！")
                    # 牛-组件-腿 意义为 牛-组件-腿 成立
        else:
            if executable in meaning_objs and not executable in Instincts.TopRelations:
                raise Exception("当前实际对象位于意义对象链中，除了顶级关系，对象不能被用来解释自身！无法创建pattern！")
                # 牛-组件-腿 意义为 牛-组件-腿 成立

        hasTopRelation = False
        for meaning_obj in meaning_objs:
            if meaning_obj in Instincts.TopRelations:
                hasTopRelation = True
                break
        sm = SequenceMatcher(patten_objs, meaning_objs)
        if sm.distance() == 0 and hasTopRelation:  # 如果两个实际对象链完全相等，则抛出错误
            raise Exception("用来创建模式的对象列表（realObject、knowledge）与用来创建意义的对象列表完全相等,"
                            "对象的意义无法用自己来解释自身！")

    @staticmethod
    def _createRealObjectExecutionInfo(executable,
                                       patten_objs, meaning_objs, meaning_value=None,
                                       memory=None,
                                       recordInDB=False):
        """
        为实际对象提取/创建模式pattern、提取/meaning
        :param executable:
        :param patten_objs:用来创建模式的对象列表（realObject、knowledge、collection），是一个线性结构
        :param meaning_objs:用来创建意义的列表（realObject、knowledge、collection），其标准格式为：
        [ # 意义对应的每一步知识链:step1-step2...
            [ # 每一步知识链的的转换模式（一个状态集合，可以有多个状态转换）：status1,status2...
                [self.real_niu,self.brain.MemoryCentral.Instincts.instinct_component,self.real_tui], # knowledge知识链第一步中包含的第一个knowledge，是一个线性结构
            ],
        ]
        :return:
        """
        # 取得现有的执行相关信息
        executionInfo = executable.getSelfExecutionInfo()
        new_created=True
        # 如果已有pattern/meaning，对现有pattern/meaning进行检查
        if executionInfo and executionInfo.isExecutable():

            if not ObjType.isAction(executable.type):
                executable.setType(ObjType.ACTION)

            if ModelingEngine._matchPatternAndMeaning(executionInfo, patten_objs, meaning_objs, meaning_value):
                new_created=False
                return executionInfo, new_created  # newcreted=False
            # 如果没有匹配出来的模式和意义，创建新的pattern、meaning（先不考虑模式是否相同，后期应该有一个专有模式处理引擎对其进行合并）
            return ModelingEngine._createNewPatternAndMeaning(executable, patten_objs, meaning_objs,
                                                              meaning_value=meaning_value,
                                                              recordInDB=recordInDB,
                                                              memory=memory),new_created

        else:  # 如果没有，创建新的pattern、meaning
            return ModelingEngine._createNewPatternAndMeaning(executable, patten_objs, meaning_objs,
                                                              meaning_value=meaning_value,
                                                              recordInDB=recordInDB,
                                                              memory=memory),new_created

    @staticmethod
    def _matchPatternAndMeaning(executionInfo, patten_objs, meaning_objs,
                                meaning_value=None):
        """
        匹配
        :param executionInfo:
        :param patten_objs:
        :param meaning_objs:
        :return:
        """
        from loongtian.nvwa.runtime.placeholder import Placeholder
        executionInfo.restoreCurObjIndex()  # 将当前可执行信息所处的位置重置为0（模式及模式的意义）
        while True:
            cur_pattern, cur_meaning ,cur_meaning_value= executionInfo.getCur()
            if not cur_pattern:  # 如果是最后一个了，停止循环
                break

            # 判断输入的模式、意义对象是否能够匹配现有模式、意义定义。
            # 如果能够匹配现有的，直接返回现有模式、意义定义。反之，创建新的
            placeholder_obj_dict, obj_placeholder_dict = Placeholder.get_placeholder_dict(patten_objs,
                                                                                          cur_pattern.getSequenceComponents())
            if obj_placeholder_dict:
                replaced_meaning_objs = Placeholder.replaceWithPlaceholderDict(meaning_objs,
                                                                               obj_placeholder_dict)
                if cur_meaning.isSame(replaced_meaning_objs):
                    # 如果匹配出了模式和意义，直接返回
                    return True  # not new created

        executionInfo.restoreCurObjIndex()  # 将当前可执行信息所处的位置重置为0（模式及模式的意义）

        return False

    @staticmethod
    def _createNewPatternAndMeaning(executable, patten_objs, meaning_objs,
                                    meaning_value=None,
                                    recordInDB=False,
                                    memory=None):
        """
        如果没有匹配出来的模式和意义，创建新的pattern、meaning
        :param executable:
        :param patten_objs:
        :param meaning_objs:
        :return:executable.ExecutionInfo,True/False # newcreted=True/False
        """
        from loongtian.nvwa.runtime.placeholder import Placeholder
        from loongtian.nvwa.models.knowledge import Knowledge

        # 0、处理模式
        pattern_placeholders, pattern_dict, pattern_splits = \
            Placeholder._createPlaceHolders(patten_objs, executable,
                                            recordInDB=recordInDB,
                                            memory=memory)
        if not pattern_placeholders or not pattern_dict:
            raise Exception("无法取得pattern的占位符链，无法创建pattern！")

        # 0.1 关联占位符及对应的实际对象之间的父对象
        ModelingEngine._createPlaceholdersParent(pattern_dict)

        pattern_klg = Knowledge.createKnowledgeByObjChain(pattern_placeholders,
                                                          type=ObjType.EXE_INFO,
                                                          understood_ratio=1.0,
                                                          recordInDB=recordInDB,
                                                          memory=memory)
        if not pattern_klg:
            raise Exception("未能创建pattern！")
        pattern_klg.getChainItems()
        # 关联可执行对象及其pattern
        executable.Layers.addLower(pattern_klg, recordInDB=recordInDB)

        # 1、处理意义
        meaning_placeholders = Placeholder.replaceWithPlaceholderDict(meaning_objs, pattern_dict)
        if not meaning_placeholders:
            raise Exception("无法取得meaning的占位符链，无法创建meaning！")

        # 创建意义
        meaning_klg = Knowledge.createKnowledgeByObjChain(meaning_placeholders, type=ObjType.EXE_INFO,
                                                          understood_ratio=1.0, recordInDB=recordInDB,
                                                          memory=memory)
        if not meaning_klg:
            raise Exception("未能创建meaning！")

        # 关联pattern对象及其meaning
        pattern_klg.Layers.addLower(meaning_klg, recordInDB=recordInDB)

        # 关联meaning对象及其meaning_value
        meaning_klg.Layers.addLower(meaning_value,ltype=ObjType.EXE_MEANING_VALUE, recordInDB=recordInDB)

        # pattern_placeholders、meaning_placeholders里面可能有一些并未记录到数据库，
        # 这时要记录之，否则未来读取时会出现找不到对象的情况
        if recordInDB:
            ModelingEngine._createInDB(pattern_placeholders)
            ModelingEngine._createInDB(meaning_placeholders)

        # 2、设置到实际对象的可执行信息
        executable.addExecutionInfo(pattern_klg, meaning_klg, meaning_value)

        executable._gotExecutionInfo = True
        executable.setType(ObjType.ACTION)
        Instincts.loadAllInstincts(memory=memory)
        executable.Constitutions.addParent(Instincts.instinct_action)

        return executable.ExecutionInfo  # newcreted=True

    @staticmethod
    def _createInDB(objs):
        """
        将对象记录到数据库
        :param objs:
        :return:
        """
        if objs is None:
            return
        if isinstance(objs, list) or isinstance(objs, list):
            for obj in objs:
                ModelingEngine._createInDB(obj)
        elif isinstance(objs, BaseEntity):
            if not objs._isInDB:
                objs.create(checkExist=False, recordInDB=True)

    @staticmethod
    def _createPlaceholdersParent(obj_placeholder_dict):
        """
        关联占位符及对应的实际对象之间的父对象
        :return:
        """
        for real, placeholder in obj_placeholder_dict.iteritems():
            real_parents, real_parents_klg = real.Constitutions.getSelfParentObjects()
            if not real_parents:
                # 2019-03-12：默认都是元对象，不需要添加
                # placeholder.Constitutions.addParent(Instincts.instinct_original_object)
                continue
            for real_parent in real_parents:
                # todo 这个地方不一定对，例如：通过“牛是动物意义牛父对象动物”，生成
                #  “是”的模式：{p1}是{p2}，就会限定了{p1}的父对象是动物，那么，如果输入“苹果是水果”，
                #  已知“苹果父对象水果”，在思考时，就可能出现前期模式不匹配，或是迁移不成功的情况
                placeholder.Constitutions.addParent(real_parent)

    @staticmethod
    def _createRealChainExecutionInfo(real_chain,
                                      patten_objs, meaning_objs, meaning_value=None,
                                      memory=None):
        """
        为多实际对象，例如：[因为...所以...]提取/创建模式pattern、提取/meaning
        :param real_chain:
        :param patten_objs:
        :param meaning_objs:
        :param meaning_value:
        :return:
        """
        for real in real_chain:
            ModelingEngine._createRealObjectExecutionInfo(real,
                                                          patten_objs, meaning_objs,
                                                          meaning_value,
                                                          memory=memory)

    def _createKnowledgeExecutionInfo(self, knowledge,
                                      patten_objs, meaning_objs,
                                      memory=None):
        """
        创建知识链的可执行信息（pattern，meaning）
        :param knowledge:
        :param patten_objs:
        :param meaning_objs:
        :return:
        """
        executable = knowledge.Layers.getUpperEntitiesByType(type=ObjType.REAL_OBJECT)

        # 创建其上一层实际对象
        upper_obj = knowledge.createUpperRealObject(realType=ObjType.ACTION)
        # 关联其模式、意义
        pattern_knowledge = Knowledge.createKnowledgeByObjChain(patten_objs, type=ObjType.EXE_INFO,
                                                                understood_ratio=1.0,
                                                                memory=self.MemoryCentral)
        meaning_knowledge = Knowledge.createKnowledgeByObjChain(meaning_objs, type=ObjType.EXE_INFO,
                                                                understood_ratio=1.0,
                                                                memory=self.MemoryCentral)
        # 关联可执行对象及其pattern
        upper_obj.Layers.addLower(pattern_knowledge)
        # 关联pattern对象及其meaning
        pattern_knowledge.Layers.addLower(meaning_knowledge)

        upper_obj.executionInfos[pattern_knowledge] = meaning_knowledge

        return pattern_knowledge, meaning_knowledge

    def _compareKnowledgesAndCreateExecutionInfo(self, knowledge1, knowledge2):
        """
        比较两个知识链，求同存异，然后生成第一个知识链的模式、意义
        :param knowledge1:
        :param knowledge2:
        :return:
        """
        knowledge1.getChainItems()
        knowledge2.getChainItems()

        # 进一步比较两个知识链，求同存异，然后生成第一个知识链的模式、意义
        kcr = self.thinkingCentral.CompareEngine.knowledgeComparer(knowledge1, knowledge2)
        sames1, differs1, sames2, differs2 = kcr.getSamesAndDiffers()
        # 如果第一个知识链被求出了相同的和差异，例如：牛-有-腿，牛-组件为-腿，进一步生成其模式、意义，否则，只是简单关联其分层关系
        # 这里需要特别说明一下：如果只有差异，没有相同，说明是两个完全不相关的内容，无法对其进行意义上的处理。
        if len(sames1) > 0 and len(differs1) > 0:
            if len(differs1) == 1:  # 如果只有一个，例如：牛 有 腿——牛 组件为 腿，将差出"有"，直接生成"有"的模式
                sub_exe = knowledge1._s_chain_items[differs1.keys()[0]]
                # 因为要生成模式，所以需要对其类型进行更改
                if isinstance(sub_exe, RealObject) and not ObjType.isExecutable(sub_exe):
                    sub_exe.type = ObjType.ACTION

                self.createExcutionInfo(sub_exe, knowledge1._s_chain_items, knowledge2._s_chain_items)
            elif len(differs1) > 1:  # 有两个及以上的差异，例如：因为...所以，分成一组，生成其模式、意义
                # 根据differs1对其进行分组，例如：因为太阳升起来了所以天亮了，如果差是"因为""所以"，则分组出：如果-太阳升起来了-所以-天亮了
                grouped_splits = self._splitByDiffers(knowledge1.s_chain, differs1)

                # 把如果-太阳升起来了-所以-天亮了 分别加入到最后需要创建模式的
                final_grouped_pattern = []
                for grouped_split in grouped_splits:
                    if isinstance(grouped_split, tuple):  # 这是被分解出来的
                        if len(grouped_split) == 1:
                            final_grouped_pattern.append(grouped_split[0])
                        else:
                            grouped_split_knowledge = Knowledge.createKnowledgeByObjChain(grouped_split,
                                                                                          type=ObjType.EXE_INFO,
                                                                                          memory=self.MemoryCentral)
                            final_grouped_pattern.append(grouped_split_knowledge)
                    else:
                        final_grouped_pattern.append(grouped_split)

                cur_knowledge = Knowledge.createKnowledgeByObjChain(final_grouped_pattern,
                                                                    type=ObjType.EXE_INFO,
                                                                    memory=self.MemoryCentral)
                # 创建模式及意义
                self.createExcutionInfo(cur_knowledge, final_grouped_pattern, knowledge2.s_chain)

    def _splitByDiffers(self, objs, differs):
        """
        根据对象的差异对
        :param differs:
        :return:
        """
        splits = []
        cur_split = []
        for obj in objs:
            if isinstance(obj, list):
                child_pattern_objs, child_pattern_dict, child_splits = self._splitByDiffers(obj, differs)
                splits.append(tuple(child_splits))
                continue
            if differs:  # 把differs剔除
                if isinstance(differs, list):
                    objExecutable = False
                    for exe in differs:
                        if obj.id == exe.id:  # 一个对象不能解释自身
                            objExecutable = True
                            break
                    if objExecutable:
                        if len(cur_split) > 0:
                            splits.append(tuple(cur_split))
                            splits.append(obj)
                            cur_split = []
                        else:
                            splits.append(obj)
                    continue
                elif isinstance(differs, RealObject):
                    if obj.id == differs.id:  # 一个对象不能解释自身
                        if len(cur_split) > 0:
                            splits.append(tuple(cur_split))
                            splits.append(differs)
                            cur_split = []
                        else:
                            splits.append(obj)
                        continue

            if isinstance(obj, RealObject):  # 略去所有的可执行性对象
                if obj.isExecutable():
                    if len(cur_split) > 0:
                        splits.append(tuple(cur_split))
                        splits.append(obj)
                        cur_split = []
                    else:
                        splits.append(obj)
                    continue

            elif isinstance(obj, Knowledge):
                obj.getChainItems()

            # 剩下的应该是不可执行的RealObject、knowledge，
            cur_split.append(obj)

        return splits

    def _mergePlaceHolders(self):
        """
        对占位符进行清理合并
        :return:
        """
        raise NotImplementedError

    def createParent(self, *children):
        """
        根据子对象创建父对象（解决冲突，相当于逻辑里的泛化）
        :param children:
        :return:
        """

    @staticmethod
    def regroupMeaningComponentsByPattern(meaning_components, pattern_components,memory=None):
        """
        根据左边的模式重新构建（分组）意义
        :param meaning_components:
        :param pattern_components:
        :return:
        """
        # 将左边的模式创建为实体实际对象
        klg = Knowledge.createKnowledgeByObjChain(pattern_components, memory=memory)
        meaning_value = klg.toEntityRealObject()
        meaning_value.setType(ObjType.PLACEHOLDER)
        # if pattern_components in meaning_components:
        #     return meaning_components, meaning_value

        meaning_components = ModelingEngine._group_meaning_components_by_pattern(meaning_components, pattern_components,meaning_value)
        if not meaning_components:
            return None, None
        return meaning_components, meaning_value


    @staticmethod
    def _group_meaning_components_by_pattern(meaning_components, pattern_components,meaning_value):
        """
        根据pattern对meaning进行重新分组
        :param meaning_components:
        :param pattern_components:
        :return:
        """
        meaning_components = ModelingEngine._plain_meaning_components(meaning_components) # 扁平化
        temp_pattern_components = ModelingEngine._plain_meaning_components(pattern_components)
        if len(temp_pattern_components) > len(meaning_components):
            return None

        first_pattern_component = temp_pattern_components[0]
        need_group_index=[]
        i = 0
        while i < len(meaning_components):
            cur_meaning_component=meaning_components[i]
            if cur_meaning_component.id==first_pattern_component.id: # 看开头
                cur_meaning_components=meaning_components[i:i+len(temp_pattern_components)] # 截取等长
                if cur_meaning_components==temp_pattern_components: # 如果截取部分与pattern扁平化部分相同，说明可以替换
                    need_group_index.append(i)
                    i+=len(temp_pattern_components)
                    continue

            i += 1
        if not need_group_index:
            return None
        grouped_meaning_components=[]

        i=0
        while i < len(meaning_components): # 替换
            if i in need_group_index:
                grouped_meaning_components.append(meaning_value)
                i += len(temp_pattern_components)
                continue
            cur_meaning_component = meaning_components[i]
            grouped_meaning_components.append(cur_meaning_component)
            i+=1

        return grouped_meaning_components




    @staticmethod
    def _plain_meaning_components(meaning_components):
        """
        将meaning_components打散
        :param meaning_components:
        :return:
        """
        result = []
        for meaning_component in meaning_components:
            if isinstance(meaning_component, list) or isinstance(meaning_component, tuple):
                child_result = ModelingEngine._plain_meaning_components(meaning_component)
                result.extend(child_result)
            else:
                result.append(meaning_component)

        return result

    @staticmethod
    def getAction(pattern_components, meaning_components):
        """
        根据pattern及meaning取得动作。
        :param pattern_components:
        :param meaning_components:
        :return:
        """
        from loongtian.nvwa.runtime.collection import Collection
        action = Collection.difference(pattern_components, meaning_components)
        if action:
            action = list(action)
            if len(action) == 1:
                action = action[0]
            else:  # 应该有多个action，应该排序，因为集合的差值用的是set，无序
                # 多动作【因为...所以...】
                sorted_actions = []
                for pattern_component in pattern_components:
                    if pattern_component in action:
                        sorted_actions.append(pattern_component)
                action = sorted_actions

        return action