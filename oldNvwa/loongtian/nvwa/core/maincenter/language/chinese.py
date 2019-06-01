#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    chinese 
Created by zheng on 2014/10/16.
UpdateLog:

"""
from loongtian.nvwa.common.storage.db.entity_repository import metadata_rep, knowledge_rep
from loongtian.nvwa.service import *


def _get_stringval_by_wordobjectid(real_object):
    if 0 < len(real_object.Metas):
        meta = metadata_rep.get(list(real_object.Metas)[0])
        return meta.StringValue
    return real_object.Display


def trans_t_to_string(frag):
    _ret = ''
    # 数据流改变,改写翻译逻辑 liuyl 2014.11.14
    _r = real_object_srv.get(frag.ref.Id)
    if _r:
        return _get_stringval_by_wordobjectid(_r)
    if fragment_srv.is_be_modifier(frag):
        _new_frag = fragment_srv.remove_be_modifier(frag)
        return trans_t_to_string(_new_frag)
    elif fragment_srv.is_quantity_is(frag):
        return trans_t_to_string(fragment_srv.get_end(frag)) + trans_t_to_string(
            fragment_srv.get_deep_start(frag))
    else:
        return trans_t_to_string(fragment_srv.get_start(frag)) + trans_t_to_string(
            fragment_srv.get_end(frag))


if __name__ == '__main__':
    from loongtian.nvwa.entities.entity import *

    k1 = Knowledge(**{'Id': '4e37469f-37f8-11e4-b31b-00acf56dbacf'})
    k2 = Knowledge(**{'Id': '4dfb2801-37f8-11e4-911f-00acf56dbacf'})
    k3 = Knowledge(**{'Id': '4e2fa580-37f8-11e4-850b-00acf56dbacf'})
    k4 = Knowledge(**{'Id': '4e2fa580-37f8-11e4-850b-00acf56dbacf'})
    print 11
    print trans_t_to_string([k1, k4, [k2, k3, k1, k1]])