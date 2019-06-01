#!/usr/bin/env python
# coding: utf-8
""" m2k
记忆到知识
"""
from loongtian.nvwa.core.engines.conflicting.conflict import deep_check, remove_conflict
from loongtian.nvwa.core.gdef import GlobalDefine
from loongtian.nvwa.entities import ConflictTypeEnum
from loongtian.nvwa.service import knowledge_srv, fragment_srv

__author__ = 'Liuyl'


def memory2knowledge(frag):
    _check_result_list = deep_check(frag, knowledge_srv)
    if len(_check_result_list) == 0:
        generate_new_knowledge(frag)
    elif _check_result_list[0].state == ConflictTypeEnum.Finded:
        if len(_check_result_list) > 1:
            handle_conflict(frag, _check_result_list[1:])
    else:
        handle_conflict(frag, _check_result_list)


def generate_new_knowledge(frag):
    fragment_srv.save_to_target_service(frag, knowledge_srv)
    print(u'm2k: generate {}'.format(frag))
    GlobalDefine().rethink_queue.put(frag)


def handle_conflict(frag, conflict_result_list):
    _frag_count = len(fragment_srv.select_all_outer(fragment_srv.get_same_from_target_service(frag, memory_srv)))
    _conflict_sum = 0
    for _c in conflict_result_list:
        _conflict_sum += len(
            fragment_srv.select_all_outer(fragment_srv.get_same_from_target_service(_c.conflict_frag, memory_srv)))
    if _frag_count > _conflict_sum:
        for _c in conflict_result_list:
            remove_conflict(frag, _c.conflict_frag)
            print(u'm2k: remove {}'.format(_c.conflict_frag))
        generate_new_knowledge(frag)


if __name__ == '__main__':
    import doctest

    doctest.testmod()