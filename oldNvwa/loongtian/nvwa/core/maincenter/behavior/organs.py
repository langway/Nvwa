#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    organs.py 
Created by zheng on 2014/10/16.
UpdateLog:

"""
from loongtian.nvwa.core.engines import m2k
from loongtian.nvwa.core.gdef import GlobalDefine
from loongtian.nvwa.core.maincenter.language import chinese
from loongtian.nvwa.service import fragment_srv, real_object_srv, knowledge_srv, fsc, original_srv
from loongtian.nvwa.service.fragment_service.memory import MemoryFragmentEnum
from loongtian.nvwa.service.repository_service import knowledge
import util


class Organ(object):
    pass


class Console(Organ):
    @staticmethod
    def output(t_struct):
        _out_msg = chinese.trans_t_to_string(t_struct[0])
        # 输出内容送入控制台输出队列
        _m = GlobalDefine()
        _m.console_output_queue.put((_out_msg, t_struct[1]))
        # print('NvWa say:[ Console(Organ) output : ' + _out_msg + ' ]')


'''
def save_t_struct(t_struct):
    _k = list()
    for item in t_struct:
        if(isinstance(item,list)):
            _k.append(save_t_struct(item))
        else:
            knowledge_rep.save(item)
            _k.append(item.Id)

        if(len(_k) == 2):
            start,end = _k[0]._k[1]
            from loongtian.nvwa.service import knowledge
            _list = knowledge.base_select_start_end(start,end)
            if(len(_list)==0):
                _id = knowledge.generate(0,None,start,end).Id
            else:
                _id = _list[0].Id

            del _k[:]
            _k.append(_id)
    if(len(_k)==0):
        return ''
    return _k[0]
'''


def save_t_struct(t_struct):
    '''
    存储T字型结构 必须三叉
    '''
    _k = []
    for item in t_struct:
        if (isinstance(item, list)):
            _k.append(save_t_struct(item))
        else:
            # knowledge_rep.save(item)
            _k.append(item)

        if (len(_k) == 3):
            start, end, bottom = _k[0], _k[1], _k[2]

            return knowledge.generate_t_structure(start, end, bottom)
    return None


class Knowledge(Organ):
    @staticmethod
    def save(t_struct):
        fragment_srv.save_to_target_service(t_struct, knowledge_srv)

    @staticmethod
    def decrease(t_struct):
        util.do_decrease(t_struct, knowledge_srv)

    @staticmethod
    def increase(t_struct):
        util.do_increase(t_struct, knowledge_srv)


class RealObject(Organ):
    @staticmethod
    def decrease(t_struct):
        util.do_decrease(t_struct, real_object_srv)

    @staticmethod
    def increase(t_struct):
        util.do_increase(t_struct, real_object_srv)


if __name__ == '__main__':
    Knowledge.save('')