#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    memory_to_knowledge 
Author:   fengyh 
DateTime: 2014-10-27 13:47 
UpdateLog:
1、fengyh 2014-10-27 Create this File.
2、fengyh 2014-10-29 创建初始化功能。
3、fengyh 2014-10-30 创建生成知识新的方法
4、fengyh 2014-10-30 创建生成新知识书籍的递归方法

"""
from loongtian.nvwa.core.engines.m2k.knowledge_algorithm_base import *
from loongtian.nvwa.entities.entity import RealObject
from loongtian.nvwa.service import *
from loongtian.nvwa.core.gdef import OID
from loongtian.nvwa.service.fragment_service.memory import MemoryFragmentEnum
# todo 算法参数暂时放这里，后面要提取到专门的常量设置区域。或者保存到数据库中可以根据情感性格动态变化。
Knowledge_Algorithm_Parameter_SimpleExistNTimes = 1
Knowledge_Algorithm_Parameter_SimpleExistNOneByOne = 3


class MemoryToKnowledge(object):
    """
        样例数据
                    idInt	start	end
                    0	nvwa本我	接收
        第一条记录	1	0	3
                    2	牛字	有字
                    3	2	腿字
                    4	1	理解为
                    5	4	7
                    6	牛未知	有未知
                    7	6	腿未知

        第二条记录	8	0	10
                    9	牛字	有字
                    10	9	头字
                    11	8	理解为
                    12	11	14
                    13	牛未知	有未知
                    14	13	头未知
    """

    def __init__(self):
        """
        基础数据准备
        1、获取“女娲接收XXX”的全组信息
        2、获取“理解为”的信息
        :return:
        """

        # 获得“女娲”“接收”的数据Id（Knowledge），此是所有查询的开始源头
        self.NvwaReceiveMemory = None
        self.MemoryTModelListReadyForDistill = []
        # 根据“女娲”“接收”的start和end为条件，查询到女娲接收哪些数据，来自所有记忆信息。
        # 根据注释样例数据，返回结果应该为[1,8]，表示女娲接收到两条数据。
        # todo 未来要考虑不能全局搜索，要按时间或其它算法分批次选择待处理列表。
        # todo 目前简单处理，搜索全局记忆。

        """
        knowledge_list_from_nvwa_receive = memory_srv.base_select_start(self.NvwaReceiveKnowledge[0].Id)

        # 获取到 XXX理解为的内容
        # 查询条件为“女娲接收Id”开始，“理解为Id”结束。查询条件是多条list，需要组合为tuple。
        # 本例中查询条件为[(1,理解为id),(8,理解为id)]
        start_end_t = [(k.Id, self.UnderstandAsId) for k in knowledge_list_from_nvwa_receive]
        # 获取到 XXX理解内容的Id，是多个。本例中查询结果应为[4,11]
        understand_list_1 = memory_srv.base_select_start_end_s(start_end_t)

        # [5,12]
        ids = [k.Id for k in understand_list_1.values()]
        understand_list = memory_srv.base_select_start_s(ids)
        # [7,14]
        really_t_ids = [k.End for k in understand_list.values()]
        really_t_knowledge2_list = memory_srv.gets(really_t_ids)

        # [6,13]
        really_t_start_ids = [k.Start for k in really_t_knowledge2_list]
        really_t_knowledge1_list = memory_srv.gets(really_t_start_ids)

        self.MemoryTModelListReadyForDistill = []
        # 循环生成待处理list，结果为[TModel1,TModel2,TModel3]。
        # 本例中为[[牛未知，有未知，腿未知],[]]
        for index, k in enumerate(really_t_knowledge1_list):
            t_model = TModel(TStart=k.Start, TEnd=k.End, TEnd2=really_t_knowledge2_list[index].End)
            self.MemoryTModelListReadyForDistill.append(t_model)
       """
        self.KnowledgeResultList = []
        # 生成的新知识都在这里。
        self.fragment_new = []
        pass

    def get_memory_for_distill(self):
        if not self.NvwaReceiveMemory:
            self.NvwaReceiveMemory = memory_srv.base_select_start_end(original_srv.InnerSelf.obj().Id,
                                                                      original_srv.Receive.obj().Id)
        if self.NvwaReceiveMemory:
            _frag = fragment_srv.generate(self.NvwaReceiveMemory, memory_srv)
            self.MemoryTModelListReadyForDistill = fragment_srv.select_all_outer(_frag)
        kam = KnowledgeAlgorithmManage(KnowledgeAlgorithmSimpleExistNTimes(self.MemoryTModelListReadyForDistill,
                                                                           Knowledge_Algorithm_Parameter_SimpleExistNTimes),
                                       KnowledgeAlgorithmSimpleExistNOneByOne(self.MemoryTModelListReadyForDistill,
                                                                              Knowledge_Algorithm_Parameter_SimpleExistNOneByOne))
        self.KnowledgeResultList = kam.distill_or()

    def distill(self):
        """
        3、根据算法选择可提取为知识的信息
            暂定算法规则满足其一即可：（1）连续两次出现；（2）累计3次出现；
        4、生成理解后新含义的对象
        5、将这部分信息保存为知识。
        todo 考虑是否存在已有知识。
        :return:
        """
        # 根据算法选择可提取为知识的信息
        # 暂定算法规则满足其一即可：（1）连续两次出现；（2）累计3次出现；

        self.get_memory_for_distill()
        self.__gen_knowledge__()

        # for f in self.fragment_new:
        # print f.ref.Display
        pass

    def __gen_knowledge__(self):

        # 循环处理提取的知识
        # 生成新含义的对象，并挂到已有meta上。生成新含义Action。每次循环创建一条知识。
        # todo 暂不考虑与已有知识的重复或更新关系，或调整阈值置信度增强减弱，知识清理等。
        _dict = dict()
        _conflict_rep = fragment_srv.get_new_knowledge_for_fragment_service()
        for t in self.KnowledgeResultList:
            if fsc.memory.check(t, memory_srv):
                _memory_structure = fsc.memory.unassemble(t)

                if original_srv.Equal.check(_memory_structure[MemoryFragmentEnum.Mood].ref,
                                            original_srv.Question.obj()):
                    continue
                _frag_understand = _memory_structure[MemoryFragmentEnum.Understand]
                _new_knowledge_frag = _frag_understand
            if fragment_srv.get_same_from_target_service(_new_knowledge_frag, knowledge_srv):
                continue
            fragment_srv.save_to_target_service(_new_knowledge_frag, knowledge_srv)
            print(u'M2K :{0}'.format(_new_knowledge_frag.ref.Display))
        pass

    def __gen_new_object__(self, old_id):
        """
        如果对象时Unknown类型，则根据旧对象产生新对象，用于组成新知识理解。
        如果是Action，则生成新Action及相关数据
        :param old_id:
        :return:
        """
        # todo liuyl 2014-12-5 由于移除了未知对象,需要对处理逻辑进行修改.
        # 判断指定Id是否是RealObject。只处理Object
        old_object = real_object_srv.get(old_id)

        if old_object is not None:
            # 判断object类型，如果是unknown的则创建新对象，否则直接返回。
            if not original_srv.InheritFrom.NotUnderstood.check(old_object):
                return old_object
            else:
                # 获得meta idInt  #todo 暂时只取第一个id。
                meta_id = list(old_object.Metas)[0]
                meta = metadata_srv.get(meta_id)
                # 先找meta下的默认实意object,如没有则创建一个默认实意object  liuyl 2014.11.21
                _default_object_list = [_o for _o in [real_object_srv.get(_id) for _id in meta.RealObjectList] if
                                        original_srv.InheritFrom.DefaultMeaning.check(_o)]
                if len(_default_object_list):
                    new_object = _default_object_list[0]
                else:
                    new_object = real_object_srv.create(Metas=set([meta_id]), Display=meta.StringValue)
                    original_srv.InheritFrom.DefaultMeaning.set(new_object)
                    # 判断是否Action走不同的创建路径
                    # todo 暂不处理，原来是Action，变成Object，或者相反的变化。
                    if action_srv.is_action_by_real_object_id(old_id):
                        # 以下创建Action
                        _p1 = action_define_srv.create_placeholder(new_object, 1)
                        _p2 = action_define_srv.create_placeholder(new_object, 2)
                        _step = action_define_srv.create_t_structure(_p1, new_object, _p2)
                        # 修复bug,传入的StringValue有误 liuyl 2014.11.11
                        action_srv.create(meta.StringValue, RealObjectId=new_object.Id,
                                          Sequence=[[_step]],
                                          Steps=[[_step]])
                    else:
                        pass

                    # 挂到相应的meta上
                    metadata_srv.link_real_object_metadata(meta.StringValue, new_object)

                return new_object
        else:
            return None
        pass

    def __gen_new_knowledge_fragment(self):
        """
        生成新的知识，并存储。
        :return:
        """
        _rep_srv = fragment_srv.get_new_knowledge_for_fragment_service()

        def __judge_replace_by_new_object_or_keep_old__(old_object):
            """
            判断是否字典中已经生成了新对象。
            有则用新对象，没有则用就对象。
            :param old_object:
            :return:
            """
            if self.new_object_id_dict.has_key(old_object.Id):
                return self.new_object_id_dict[old_object.Id]
            else:
                return old_object
            pass

        def __inner_gen__(current_knowledge):
            """
            把T型结构最外层书籍递归处理产生所有的下层数据。
            其中新产生的对象要替换进来。
            :param current_knowledge:
            :return:
            """
            object_start = real_object_srv.get(current_knowledge.Start)
            object_end = real_object_srv.get(current_knowledge.End)
            if object_start:
                if object_end:
                    new_knowledge = _rep_srv.create_l_structure(
                        __judge_replace_by_new_object_or_keep_old__(object_start),
                        __judge_replace_by_new_object_or_keep_old__(object_end))
                else:
                    knowledge_end = memory_srv.get(current_knowledge.End)
                    new_knowledge = _rep_srv.create_l_structure(
                        __judge_replace_by_new_object_or_keep_old__(object_start), __inner_gen__(knowledge_end))
            else:
                if object_end:
                    knowledge_start = memory_srv.get(current_knowledge.Start)
                    new_knowledge = _rep_srv.create_l_structure(__inner_gen__(knowledge_start),
                                                                __judge_replace_by_new_object_or_keep_old__(
                                                                    object_end))
                else:
                    knowledge_start = memory_srv.get(current_knowledge.Start)
                    knowledge_end = memory_srv.get(current_knowledge.End)
                    new_knowledge = _rep_srv.create_l_structure(__inner_gen__(knowledge_start),
                                                                __inner_gen__(knowledge_end))
            return new_knowledge

        _ref = __inner_gen__(self.frag_understand.ref)

        # 赋值带回
        _frag = fragment_srv.generate(_ref, rep_srv=_rep_srv)
        _not_modifier_frag = fragment_srv.trans_to_not_be_modifier_for_rethink(_frag)
        fragment_srv.save_to_target_service(_not_modifier_frag, knowledge_srv)
        _new = fragment_srv.save_to_target_service(_not_modifier_frag, memory_srv)
        # memory_srv.replace_all_reference_id(self.frag_understand.ref.Id, _new.ref.Id)
        self.fragment_new.append(_frag)
