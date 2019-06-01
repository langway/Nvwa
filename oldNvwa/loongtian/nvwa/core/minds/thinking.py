#!/usr/bin/env python
# coding: utf-8
# encoding=utf-8
"""
女娲思维模块，这是核心模块。

Project:  nvwa
Title:    thinking 
Author:   fengyh 
DateTime: 2014/8/20 11:22 
UpdateLog:
1、fengyh 2014/8/20 Create this File.
"""
import datetime
import new
import jieba

from loongtian.nvwa.common.threadpool.runnable import Runnable
from loongtian.nvwa.core.gdef import GlobalDefine, OID
from loongtian.nvwa.core.maincenter.evaluator.evaluator import EvaluateResult, State
from loongtian.nvwa.core.maincenter.planner.plan import planer_center
from loongtian.nvwa.core.maincenter import *
from loongtian.nvwa.core.minds.action_functions_engine import FunctionActionSplit
from loongtian.nvwa.entities import CommandJobTypeEnum
from loongtian.nvwa.entities.sentence import Sentence
from loongtian.nvwa.service import knowledge_srv, real_object_srv, metadata_srv, fsc, fragment_srv

class Thinking(Runnable):
    ''' 思维
    :attributes
        inputMsg 命令行输入字符串，Queue类型。
        outMsg 命令行输出字符串，Queue类型。
    '''
    def __init__(self):
        super(Thinking, self).__init__()
        self._name = "Thinking"
        self.inputMsg = GlobalDefine().console_input_queue
        self.outMsg = GlobalDefine().console_output_queue
        pass

    def _call_from_string_to_plan(self, str_param):
        """
        提取出来给定字符串走个中枢的方法。
        依次会经过分词，分组，迁移，评估，计划等操作。
        fengyh 2015-10-15
        :param str_param:待处理字符串
        :return:（1）计划中枢执行结果；（2）迁移结果（备用）
        """
        _word_list = [word for word in list(jieba.cut(str_param)) if word.strip() != '']
        _sentence = Sentence(_word_list)
        # 分组
        _group_results = grouper_center.execute(_word_list, _sentence)
        # 迁移
        _moved_results = mover_center.execute(_group_results, _sentence)
        # 评估
        _evaluated_result = evaluator_center.execute(_moved_results, _sentence)
        _time3 = datetime.datetime.now()
        # 计划
        _planed_results = planer_center.execute(_evaluated_result, _sentence)
        return _planed_results,_moved_results[0]

    def _execute(self):
        ''' 
        提取系统中所有走函数的action及其函数名。
        此列表的存在意味着要有限处理。todo 未来扩展为各种类型的优先列表
        '''
        function_list = knowledge_srv.base_select_end(OID.FunctionBase)
        function_dic = {}
        for f in function_list:
            f_object = knowledge_srv.base_select_start_end(knowledge_srv.get(f.Start).Start,OID.FunctionName)
            f_name = knowledge_srv.base_select_start(f_object.Id)
            m = metadata_srv.get_by_default_meaning_object(real_object_srv.get(f_object.Start))
            function_dic[m.StringValue] = knowledge_srv.get(f_name[0].End).Display

        def get_function_object_by_function_name(function_name):
            ''' 
            闭包函数_execute，反射获取函数对象。
            :param function_name 函数对象名称
            :return 函数对象。
            '''
            function_class_name = "ActionFunctions"
            _packet_name = 'loongtian.nvwa.core.minds.action_functions_engine'
            _module_home = __import__(_packet_name,globals(),locals(),[function_class_name])
            #class_type = getattr(_module_home,'ActionFunctions')
            #function_object = new.instancemethod(class_type,function_name)
            function_object = getattr(_module_home,function_name)
            return function_object

        _rep_srv = fragment_srv.get_new_knowledge_for_fragment_service()
        while True:
            if not self.inputMsg.empty():
                # 分词
                # _input = unicode(self.inputMsg.get(), "utf-8")
                _input, _client_address = self.inputMsg.get()

                _rb = FunctionActionSplit(_input,function_dic)
                _rb.input_split()

                _planed_results = []
                if function_dic.items().__len__()>0  and _rb.current_operator is not None:
                # 以下插入函数处理
                    f_object = get_function_object_by_function_name(function_dic.get(_rb.current_operator))

                    # 以下增加分支处理逗号特殊情况.逗号分割的两个短句建立关联。  fengyh 2015-10-14
                    if _rb.current_operator== u',' or _rb.current_operator == u'，':
                        result1,t_struct1 = self._call_from_string_to_plan(_rb.first_param)
                        _planed_results.extend(result1)
                        result2,t_struct2 = self._call_from_string_to_plan(_rb.second_param)
                        _planed_results.extend(result2)

                        _rb.first_param = result1
                        _rb.second_param = result2

                        _rf = fragment_srv.create_l_structure(t_struct1[0],t_struct2[0],_rep_srv)
                        _s = Sentence(['非常好'])
                        # _es = evaluator_center.execute([[_rf]*2], _s)
                        _es = EvaluateResult(State.NotExist, 0, left_frag=_rf, right_frag=_rf, frag=_rf)
                        result3 = planer_center.execute(_es, _s)
                        _planed_results.extend(result3)
                    else:
                        # apply(f_object,[_rb.first_param,_rb.second_param])  本句效果同下一句
                        rt_str = f_object(_rb.first_param,_rb.second_param)
                        rt_frag = real_object_srv.create(Display = rt_str)

                        _rf = fsc.fragment.generate(rt_frag,_rep_srv)

                        _s = Sentence(['非常好','!'])
                        # _es = evaluator_center.execute([[_rf]*2], _s)
                        _es = EvaluateResult(State.NotExist, 0, left_frag=_rf, right_frag=_rf, frag=_rf)
                        _planed_results = planer_center.execute(_es, _s)
                else:
                    _cut_word_list = [word for word in list(jieba.cut(_input, False)) if word.strip() != '']
                    _word_list = []
                    # 由于采用了完全分词,这里对 孙悟空-->孙悟空,悟空 和 人民银行-->人民,人民银行,银行 这样的分组结果进行筛选
                    if len(_cut_word_list) > 0:
                        _pre = _cut_word_list[0]
                        _word_list.append(_pre)
                        for _w in _cut_word_list[1:]:
                            if _w.find(_pre) == -1 and _pre.find(_w) == -1:
                                _word_list.append(_w)
                                _pre = _w
                    else:
                        _word_list = _cut_word_list
                    # 问句时分词结果中没有问号,在这里把问号加到结果结尾,并在Sentence对象中对句子的类型进行标注
                    if _input[-1] == u'?' or _input[-1] == u'？' :
                        if _word_list[-1] != u'?' and _word_list[-1] != u'？':
                            _word_list.append(u'?')
                    _sentence = Sentence(_word_list)
                    _time0 = datetime.datetime.now()
                    # 分组
                    _group_results = grouper_center.execute(_word_list, _sentence)
                    _time1 = datetime.datetime.now()
                    # 迁移
                    _moved_results = mover_center.execute(_group_results, _sentence)
                    _time2 = datetime.datetime.now()
                    # 评估
                    _evaluated_result = evaluator_center.execute(_moved_results, _sentence)
                    _time3 = datetime.datetime.now()
                    # 计划
                    _planed_results = planer_center.execute(_evaluated_result, _sentence)
                    _time4 = datetime.datetime.now()
                    _time5 = datetime.datetime.now()
                    # 输出调试辅助信息
                    for _moved in _moved_results:
                        print(u'迁移 M:{}  T:{}  '.format(_moved[0], _moved[1]))
                    _left = _evaluated_result.left_frag
                    _right = u'没有评估成功的分组'
                    if _evaluated_result.right_frag:
                        _right = _evaluated_result.right_frag
                    print(u'评估 LM:{} LT:{}  R:{}'.format(getattr(_left, 'modified_frag', _left), _left, _right))
                    _time6 = datetime.datetime.now()
                    # print(u'group:{0}.{1}s'.format((_time1 - _time0).seconds, (_time1 - _time0).microseconds / 1000))
                    # print(u'move:{0}.{1}s'.format((_time2 - _time1).seconds, (_time2 - _time1).microseconds / 1000))
                    # print(u'evaluate:{0}.{1}s'.format((_time3 - _time2).seconds, (_time3 - _time2).microseconds / 1000))
                    # print(u'plan:{0}.{1}s'.format((_time4 - _time3).seconds, (_time4 - _time3).microseconds / 1000))
                    # print(u'behavior:{0}.{1}s'.format((_time5 - _time4).seconds, (_time5 - _time4).microseconds / 1000))
                    # print(u'output:{0}.{1}s'.format((_time6 - _time5).seconds, (_time6 - _time5).microseconds / 1000))
                    # print(u'all:{0}.{1}s'.format((_time6 - _time0).seconds, (_time6 - _time0).microseconds / 1000))

                # 执行
                for item in _planed_results:
                    if item.type == CommandJobTypeEnum.Output:
                        item.t_struct = (item.t_struct, _client_address)
                    GlobalDefine().command_msg.put(item)

            if not self.state():
                break