#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    mean2action 
Author:   fengyh 
DateTime: 2015/6/15 16:10 
UpdateLog:
1、fengyh 2015/6/15 Create this File.


"""
from loongtian.nvwa.core.engines.meantool.placeholder import PlaceHolder
from loongtian.nvwa.core.gdef import OID
from loongtian.nvwa.entities.entity import RealObject, Knowledge
from loongtian.nvwa.service import original_srv, real_object_srv, knowledge_srv, fsc, metadata_srv
from loongtian.nvwa.service.fragment_service.fragment_definition.fragment import KnowledgeForFragment


class Mean2Action(object):
    def __init__(self, refer_frag):
        self.u_frag = fsc.refer.unassemble(refer_frag)

        self.action_semantic = real_object_srv.get(OID.ActionSemantic)
        self.action_semantic_frag = fsc.fragment.generate(self.action_semantic,knowledge_srv)
        self.action_base_object = real_object_srv.get(OID.Action)
        self.action_structure = real_object_srv.get(OID.ActionStructure)
        self.action_structure_frag = fsc.fragment.generate(self.action_structure,knowledge_srv)

        # 执行find action后会赋值
        self.action_object = None
        self.action_object_frag = None

        # 用变量占位符替换对象的字典
        self.replace_dic = {}

        self.structure_content = None
        self.semantic_content = None

    def do(self):
        self.__find_action__()
        self.structure_content = self.__replace_placeholder__(self.u_frag[0])
        # self.structure_content = fsc.refer.replace_real_object_and_create_new_frag(self.u_frag[0],self.replace_dic)
        self.semantic_content = self.__replace_placeholder__(self.u_frag[1])

        self.save()
        #fsc.refer.save_to_target_service(self.structure_content, knowledge_srv)
        #fsc.refer.save_to_target_service(self.semantic_content, knowledge_srv)
        pass

    def __find_action__(self):
        """
        找到待处理的action，规则是“指的是”前面有后面没有。
        :return:
        """
        a_list = [d for d in self.u_frag[0].data if isinstance(d, RealObject)]
        b_list = [d for d in self.u_frag[1].data if isinstance(d, RealObject)]
        action_list = list(set(a_list).difference(set(b_list)))
        if action_list is not None and action_list.__len__() > 0:
            # todo fengyh 2015-6-16 暂时只考虑action是一个词的情况。为了可能要考虑多个词。
            self.action_object = action_list[0]
            self.action_object_frag = fsc.fragment.generate(self.action_object,knowledge_srv)

        # # 不是action的用变量替换

        #去掉action对象
        if a_list.__contains__(self.action_object):
            a_list.remove(self.action_object)
            self.replace_dic[self.action_object] = self.action_object

        # 生成或获取指定个数占位符
        ph_list = PlaceHolder.get_n_placeholder(a_list.__len__())
        for index, a in enumerate(a_list):
            if a != self.action_object:
                self.replace_dic[a] = ph_list[index]
        b_object_list = list(set(b_list).difference(set(a_list)))
        for b in b_object_list:
            self.replace_dic[b] = b
        pass

    def __replace_placeholder__(self, frag):
        _rep_srv = fsc.fragment.get_new_knowledge_for_fragment_service()
        # 过滤出来frag data中的所有knowledge片段
        _knowledge_frag_data_list = filter((lambda f: isinstance(f, KnowledgeForFragment)), frag.data)

        def __find_frag_in_frag_data__(frag_id):
            """
            查找指定id在frag片段data数据中的对应数据
            :param frag_id:
            :return:
            """
            find_frag = filter((lambda k: k.Id == frag_id), _knowledge_frag_data_list)
            if find_frag is not None and find_frag.__len__() > 0:
                return find_frag[0]
            else:
                return None

        def __inner_fragment_deal__(current_ref):
            """
            内部递归方法，遍历整个fragment并对其中的对象替换为占位符变量。
            """
            object_start = real_object_srv.get(current_ref.Start)
            object_end = real_object_srv.get(current_ref.End)
            if object_start:
                if object_end:
                    new_knowledge = _rep_srv.create_l_structure(
                        self.replace_dic[object_start],
                        self.replace_dic[object_end])
                else:
                    knowledge_end = __find_frag_in_frag_data__(current_ref.End)
                    if knowledge_end is None:
                        return None

                    new_knowledge = _rep_srv.create_l_structure(
                        self.replace_dic[object_start], __inner_fragment_deal__(knowledge_end))
            else:
                if object_end:
                    knowledge_start = __find_frag_in_frag_data__(current_ref.Start)
                    if knowledge_start is None:
                        return None
                    new_knowledge = _rep_srv.create_l_structure(__inner_fragment_deal__(knowledge_start),
                                                                self.replace_dic[object_end])
                else:
                    knowledge_start = __find_frag_in_frag_data__(current_ref.Start)
                    knowledge_end = __find_frag_in_frag_data__(current_ref.End)
                    if knowledge_start is None or knowledge_end is None:
                        return None
                    new_knowledge = _rep_srv.create_l_structure(__inner_fragment_deal__(knowledge_start),
                                                                __inner_fragment_deal__(knowledge_end)
                    )
            return new_knowledge

        _ref = __inner_fragment_deal__(frag.ref)
        if _ref:
            _frag = fsc.fragment.generate(_ref, rep_srv=_rep_srv)
            # knowledge_frag = fsc.fragment.get_same_from_target_service(_frag, knowledge_srv)
            return _frag
        else:
            return _ref
        pass

    def save(self):


        # _de_c_action_object = metadata_srv.create_default_action(_de_meta)
        # _de_action_object = real_object_srv.create(Display=u'的')
        # original_srv.SymbolInherit.set(_de_action_object, _de_c_action_object)

        meta = metadata_srv.get_by_default_meaning_object(self.action_object)
        _action_object = metadata_srv.create_default_action(meta)
        original_srv.SymbolInherit.set(self.action_object, _action_object,knowledge_srv)

        fsc.fragment.create_t_structure(self.action_object_frag, self.action_semantic_frag, self.semantic_content,knowledge_srv)
        fsc.fragment.create_t_structure(self.action_object_frag, self.action_structure_frag, self.structure_content,knowledge_srv)

        fsc.fragment.create_t_structure(self.action_object_frag,fsc.fragment.generate(real_object_srv.get(OID.SequenceIs),knowledge_srv),self.structure_content,knowledge_srv)
        fsc.fragment.create_t_structure(self.action_object_frag,fsc.fragment.generate(real_object_srv.get(OID.StepIs),knowledge_srv),self.semantic_content,knowledge_srv)


        pass



