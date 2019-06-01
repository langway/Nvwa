#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    grouper 
Author:   fengyh 
DateTime: 2014/9/3 9:24 
UpdateLog:
1、fengyh 2014/9/3 Create this File.
                    创建分组器类及部分方法，目前在内存中运算，后续需要修改。
2、fengyh 2014/9/4 创建create_data_for_data_notfound方法。为新词创建对象。
3、fengyh 2014/9/9 将临时创建的对象都用真是数据库访问api实现为正式代码。
                    实现do_group方法，传入分词后词的序列，返回分组结果list
4、fengyh 2014/9/10 整理代码变量命名，完善注释等。
5、fengyh 2014/9/10 调整action_descartes方法，如‘腿’‘毛’连续出现无Action时，用虚无anything连接建立结构。
6、liuli 2014/10/31 分表后调整grouper的实现
grouper 
>>> print("No Test")
No Test

"""
import itertools
from loongtian.nvwa.entities import GrouperPriorityEnum
from loongtian.nvwa.service import *
from loongtian.nvwa.core.gdef import OID, GlobalDefine


class Grouper(object):
    def __init__(self):
        self.priority_dict = {}
        self._init_priority_dict_have_done = False

    def _init_priority_dict(self):
        """
        设置'有','的','是'的三个先天理解的特殊action的优先级
        用一个字典进行维护,避免分组时重复查找这些特殊action对象
        :return:
        """
        self.priority_dict[
            metadata_srv.get_default_action(metadata_srv.get_by_string_value(u'有'))[
                0].Id] = GrouperPriorityEnum.ActionLow0
        self.priority_dict[metadata_srv.get_default_action(
            metadata_srv.get_by_string_value(u'没有'))[0].Id] = GrouperPriorityEnum.ActionLow0
        self.priority_dict[metadata_srv.get_default_action(
            metadata_srv.get_by_string_value(u'是'))[0].Id] = GrouperPriorityEnum.ActionLow0
        self.priority_dict[metadata_srv.get_default_action(
            metadata_srv.get_by_string_value(u'不是'))[0].Id] = GrouperPriorityEnum.ActionLow0
        self.priority_dict[metadata_srv.get_default_action(
            metadata_srv.get_by_string_value(u'的'))[0].Id] = GrouperPriorityEnum.ActionLow2
        self._init_priority_dict_have_done = True

    def _get_priority(self, real_object):
        """
        为每一个real_object指定一个分组的优先级,级别高的将优先处于T结构的外层
        目前的优先级设定原则为,实意Action > '有'/'是'的Default型Action > '的'的Default型Action
                                    > 实意RealObject > Default RealObject > 词RealObject
        :param real_object:
        :return:
        """
        if not self._init_priority_dict_have_done:
            self._init_priority_dict()
        if real_object.Id in self.priority_dict:
            return self.priority_dict[real_object.Id]
        if original_srv.InheritFrom.DefaultAction.check(real_object):
            return GrouperPriorityEnum.Action
        return GrouperPriorityEnum.Class

    def _get_default_priority_list_for_metadata(self, meta):
        """
        传入metadata对象,获取其RealObjectList中关联的所有RealObject对象及对应的分组优先级所组成的二元组
        返回根据优先级对二元组进行降序排序后的列表
        :param meta: 传入一个Metadata对象
        :return:(RealObject对象,分组优先级)的排序后列表
        """
        _result = [[_obj, self._get_priority(_obj)] for _obj in metadata_srv.get_default(meta)]
        _result.sort(key=lambda _r: _r[1], reverse=True)
        return _result

    def execute(self, words, sentence):
        """
        执行分组
        :param words: 分词后的词语列表
        :param sentence: 传入句子对象的引用,将直接为该对象的unknown_model和sentence_model赋予默认分组结果
        :return:返回分组结果列表 列表元素为[出口Memory对象,[嵌套结构中的所有Memory对象]]
        """
        # 申请一个独立仓库,存储和传递一次分组执行的所有分组结果
        _rep_srv = fragment_srv.get_new_knowledge_for_fragment_service()

        def _forward_group(object_list):
            """
            按照排列次序进行分组,由于构造词对象表示的句子模型
            """
            if len(object_list) == 0:
                return None
            elif len(object_list) == 1:
                return [object_list[0][0], []]
            else:
                _out = object_list[0][0]
                for _o in object_list[1:]:
                    _k = _rep_srv.create_l_structure(_out, _o[0])
                    _out = _k
            return fragment_srv.generate(_out, _rep_srv)

        def _deep_group(object_list, one_time=False):
            """
            深度分组的递归函数
            :param object_list: 带有优先级的object列表
            :param one_time: 是否按照给定的优先级只得到一个结果,如为False,
                            将按优先级顺序以每个action级别的object为根都进行一次深度分组
            :return:分组结果的列表
            """

            def _generate_group_result(left, mid, right):
                """
                内部函数,深度递归时以action的left,right继续递归分组,内部递归返回的结果以list形式返回
                上层需要对left,right两个list进行笛卡尔积得到该层的分组结果列表
                """
                _result = []
                if len(left) == 0:
                    _result_cartesian = list(itertools.product(mid, right))
                elif len(right) == 0:
                    _result_cartesian = list(itertools.product(left, mid))
                else:
                    _result_cartesian = list(itertools.product(left, mid, right))
                for _r in _result_cartesian:
                    if len(_r) == 2:
                        _k = _rep_srv.create_l_structure(_r[0].ref, _r[1].ref)
                        _result.append(fragment_srv.generate(_k, rep_srv=_rep_srv))
                    else:
                        _k_1, _k_2 = _rep_srv.create_t_structure2(_r[0].ref, _r[1].ref, _r[2].ref)
                        _result.append(fragment_srv.generate(_k_2, rep_srv=_rep_srv))
                return _result

            # 深度分组执行
            _result = []
            if len(object_list) == 0:
                pass
            elif len(object_list) == 1:
                _result.append(fragment_srv.generate(object_list[0][0], rep_srv=_rep_srv))
            elif len(object_list) == 2:
                _k = _rep_srv.create_l_structure(object_list[0][0], object_list[1][0])
                _result.append(fragment_srv.generate(_k, rep_srv=_rep_srv))
            else:
                # 构造一个索引号和object的优先级所组成的二元组
                _order_list = [[_i, _obj[1]] for _i, _obj in enumerate(object_list)]
                # 先按索引号降序排序,保证两个相同优先级的对象相连时,优先处理后面的
                _order_list.sort(key=lambda _o: _o[0], reverse=True)
                # 排序是稳定的,再按优先级排序,保留了上一句的排序结果,优先级较高的将作为根优先执行分组,在结果中的位置将靠前
                _order_list.sort(key=lambda _o: _o[1], reverse=True)
                # 如果列表中存在优先级高于action优先级标志的,则列表中存在action,将只以action为根进行深度分组
                if _order_list[0][1] > GrouperPriorityEnum.ClassActionSplit:
                    for _order in _order_list:
                        if _order[1] > GrouperPriorityEnum.ClassActionSplit:
                            _left = _deep_group(object_list[:_order[0]], one_time=one_time)
                            _mid = [fragment_srv.generate(object_list[_order[0]][0],
                                                          rep_srv=_rep_srv)]
                            _right = _deep_group(object_list[_order[0] + 1:], one_time=one_time)
                            _result.extend(_generate_group_result(_left, _mid, _right))
                        if one_time:
                            break
                # 如果列表中不存在优先级高于action优先级标志的,则列表中不存在action,将以每个real_object为根都进行一次深度分组
                else:
                    # for _order in _order_list:
                    # _left = _deep_group(object_list[:_order[0]], one_time=one_time)
                    # _mid = [fragment_srv.generate(object_list[_order[0]][0], rep_srv=_rep_srv)]
                    #     _right = _deep_group(object_list[_order[0] + 1:], one_time=one_time)
                    #     _result.extend(_generate_group_result(_left, _mid, _right))
                    _index = range(len(object_list) - 1, 0, -1)
                    _right = object_list[_index[0]][0]
                    for _i in _index:
                        _left = object_list[_i - 1][0]
                        _right = _rep_srv.create_l_structure(_left, _right)
                    _result.append(fragment_srv.generate(_right, rep_srv=_rep_srv))
            # 不同递归路径有可能得到同样地分组结果,在这里进行过滤去除重复结果
            _result = fragment_srv.base_filter_repetition(_result)
            return _result

        # 分组执行逻辑
        all_words_metas = []
        # 获取所有词的对应meta
        for _w in words:
            _m = metadata_srv.get_by_string_value(_w)
            if not _m:
                _m = metadata_srv.create(_w)
            all_words_metas.append(_m)
        # all_action = [metadata_srv.get_default_action(_m) for _m in all_words_metas]
        # all_class = [metadata_srv.get_default_class(_m) for _m in all_words_metas]
        all_default = [self._get_default_priority_list_for_metadata(_m) for _m in all_words_metas]
        # 得到只有词类real_object的列表
        all_word = [[metadata_srv.get_word(_m), GrouperPriorityEnum.Word] for _m in all_words_metas]
        # 获得实意real_object列表的笛卡尔积
        all_default_cartesian = list(itertools.product(*all_default))
        # 对每一种组合进行深度分组
        _result_list = []
        for _ol in all_default_cartesian:
            _result_list.extend(_deep_group(_ol))
        # 将句子的文字模型放入句子对象中
        sentence.sentence_model = _forward_group(all_word)
        return _result_list


grouper_center = Grouper()

if __name__ == '__main__':
    # import doctest
    #
    # doctest.testmod()
    original_init_srv.init()
    from loongtian.nvwa.entities.sentence import Sentence

    g_word_list = [u'牛', u'有', u'黄色', u'的', u'腿']
    # g_word_list = [u'有', u'的', u'有']
    g_sentence = Sentence(g_word_list)
    g_result = grouper_center.execute(g_word_list, g_sentence)
    for _f in g_result:
        print(_f.__str__())
    g_start = fragment_srv.get_start(g_result[0])
    g_end = fragment_srv.get_end(g_result[0])
    print(g_start.__str__())
    print(g_end.__str__())