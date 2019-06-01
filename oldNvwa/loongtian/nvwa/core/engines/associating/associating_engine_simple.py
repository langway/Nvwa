#!/usr/bin/env python
#coding: utf-8
"""
Project:  nvwa
Title:    ${NAME} 
Author:   fengyh 
DateTime: 2015/1/27 15:31 
UpdateLog:
1、fengyh 2015/1/27 Create this File.
2、                 将原来简单的类比功能分出来单独文件。

"""
from loongtian.nvwa.core.gdef import OID
from loongtian.nvwa.entities.const_values import ConstValues
from loongtian.nvwa.service import fsc, memory_srv, fragment_srv, real_object_srv, original_srv
from loongtian.nvwa.service.fragment_service.memory import MemoryFragmentEnum


class AssociatingEngineSimple(object):
    """
    问题定义：
    系统已知“牛组件腿”“桌子组件腿”，输入“羊有腿”时满足什么条件可以抽取为“羊组件腿”？

    规则：
    1、规则r1：系统已知“牛父对象动物”“羊父对象动物”“牛组件XXX”。类似“XXX父对象动物”且“XXX组件XXX”的出现次数k1。占权重w1。
    2、规则r2：系统已知“XXX组件腿”出现次数k2。占权重w2。
    3、类比值计算：V = k1*w1+k2*w2
    4、V大于类比门槛值T则为类比成功，符合条件。
    说明：
    1、w1和w2权重总和为1，可设置各规则占比，程序可设置。
    2、K1和k2是查询出来的数据。
    3、门槛值T可设置。
    """

    def __init__(self):
        self.analogy_rule_factor_k1 = 0
        self.analogy_rule_factor_k2 = 0
        self.fragment_pending_data = None
        pass

    def __init__(self, fragment_ready):
        """
        基础数据准备
        1、获取“女娲接收XXX”的全组信息
        2、获取“理解为”的信息
        :return:
        """

        self.analogy_rule_factor_k1 = 0
        self.analogy_rule_factor_k2 = 0
        self.fragment_pending_data = fsc.memory.unassemble(fragment_ready)
        self.fragment_pending_data_understand = self.fragment_pending_data[MemoryFragmentEnum.Understand]
        self.memory_frags = []

        # 女娲本我Id
        self.NvwaId = OID.InnerSelf
        # 女娲接收Idq
        self.ReceiveId = OID.Receive
        # 女娲理解为Id
        self.UnderstandAsId = OID.UnderstoodAs

        # 获得“女娲”“接收”的数据Id（Knowledge），此是所有查询的开始源头
        self.NvwaReceiveMemory = memory_srv.base_select_start_end(self.NvwaId, self.ReceiveId)

        # 根据“女娲”“接收”的start和end为条件，查询到女娲接收哪些数据，来自所有记忆信息。
        # 根据注释样例数据，返回结果应该为[1,8]，表示女娲接收到两条数据。
        # todo 未来要考虑不能全局搜索，要按时间或其它算法分批次选择待处理列表。
        # todo 目前简单处理，搜索全局记忆。
        if self.NvwaReceiveMemory:
            frag = fragment_srv.generate(self.NvwaReceiveMemory, memory_srv)
            self.memory_frags = fragment_srv.select_all_outer(frag)

        pass

    def run(self):
        # 查询规则1出现次数
        self.__query_rule1__()
        # 查询规则2出现次数
        self.__query_rule2__()
        # 如果符合算法，则把“牛有腿”生成为“牛组件腿”
        if self.__judge_success__():
            self.__gen_understand_data__()
        pass

    def __query_rule1__(self):
        # 找到左部分信息的Id
        _left_and_middle = fragment_srv.get_start(self.fragment_pending_data_understand)
        left_id = _left_and_middle.ref.Start
        middle_id = _left_and_middle.ref.End

        _left_and_middle_word = fragment_srv.get_start(self.fragment_pending_data[MemoryFragmentEnum.Receive])
        left_word_id = _left_and_middle_word.ref.Start
        middle_word_id = _left_and_middle_word.ref.End


        # 找到左侧信息的父对象
        _left_father_data = memory_srv.base_select_start_end(left_id, OID.InheritFrom)
        _left_father_data_frag = fragment_srv.generate(_left_father_data, memory_srv)
        _left_father_frags = fragment_srv.select_all_outer(_left_father_data_frag)
        # todo 暂时只考虑有一个父对象的情况
        _father_of_left_frag = _left_father_frags[0]
        _frag_include_father = fsc.memory.unassemble(_father_of_left_frag)

        # 父对象“动物”的Id
        left_father_id = _frag_include_father[MemoryFragmentEnum.Understand].ref.End
        # _frag_father_left = fragment_srv.get_start(_frag_include_father[MemoryFragmentEnum.Understand])
        # memory_srv.base_select_start(_frag_father_left.ref.Id)
        # _frag_father_left_data = fsc.memory.unassemble(_frag_father_left)
        # left_father_id = _frag_father_left.ref.End

        for f in self.memory_frags:
            _s = fsc.memory.unassemble(f)
            _left_and_middle_s = fragment_srv.get_start(_s[MemoryFragmentEnum.Understand])

            _left_and_middle_word_s = fragment_srv.get_start(_s[MemoryFragmentEnum.Receive])

            if _left_and_middle_s.ref.End == OID.InheritFrom:
                # 此分支跳过数据中是“继承自”的情况
                continue
            elif real_object_srv.get(middle_word_id).Metas.intersection(
                    real_object_srv.get(_left_and_middle_word_s.ref.End).Metas):
                find_father_r = memory_srv.base_select_start_end(_left_and_middle_s.ref.Start, OID.InheritFrom)
                if find_father_r is not None:
                    find_father_equal = memory_srv.base_select_start_end(find_father_r.Id, left_father_id)
                    if find_father_equal is not None:
                        self.analogy_rule_factor_k1 += 1
        pass

    def __query_rule2__(self):
        # 找到左部分信息的Id
        _left_and_middle = fragment_srv.get_start(self.fragment_pending_data_understand)
        left_id = _left_and_middle.ref.Start
        middle_id = _left_and_middle.ref.End
        right_id = self.fragment_pending_data_understand.ref.End

        _left_and_middle_word = fragment_srv.get_start(self.fragment_pending_data[MemoryFragmentEnum.Receive])
        left_word_id = _left_and_middle_word.ref.Start
        middle_word_id = _left_and_middle_word.ref.End

        for f in self.memory_frags:
            _s = fsc.memory.unassemble(f)
            _left_and_middle_s = fragment_srv.get_start(_s[MemoryFragmentEnum.Understand])
            _left_and_middle_word_s = fragment_srv.get_start(_s[MemoryFragmentEnum.Receive])

            if _left_and_middle_s.ref.End == OID.InheritFrom:
                # 此分支跳过数据中是“继承自”的情况
                continue
            elif real_object_srv.get(middle_word_id).Metas.intersection(
                    real_object_srv.get(_left_and_middle_word_s.ref.End).Metas):
                if OID.Component == _left_and_middle_s.ref.End:
                    find_middle_and_right = memory_srv.base_deduce_forward(_left_and_middle_s.ref.End, right_id)
                    if find_middle_and_right.__len__() > 0:
                        self.analogy_rule_factor_k2 += 1
        pass

    def __judge_success__(self):
        """
        类比规则草稿版，雏形占位。
        未来会随着女娲知识的丰富完善实现更智能的算法。
        :return:
        """
        result = self.analogy_rule_factor_k1 * ConstValues.analogy_rule_weight_w1 \
                 + self.analogy_rule_factor_k2 * ConstValues.analogy_rule_weight_w2
        if result >= ConstValues.analogy_rule_success_threshold:
            return True
        else:
            return False

    def __gen_understand_data__(self):
        """
        生成类比数据，将默认有替换为组件。
        :return:
        """
        # 处理
        a_have = memory_srv.get(self.fragment_pending_data_understand.ref.Start)
        have_to_component = original_srv.Component.set(memory_srv.get(a_have.Start),
                                                       memory_srv.get(self.fragment_pending_data_understand.ref.End),
                                                       memory_srv)
        print(have_to_component.Display)