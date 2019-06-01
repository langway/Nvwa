#!/usr/bin/env python
# coding: utf-8
"""
片段（数据集）模块

Project:  nvwa
Title:    fragment 
Author:   Liuyl 
DateTime: 2014/12/17 16:40 
UpdateLog:
1、Liuyl 2014/12/17 Create this File.

fragment
>>> print("No Test")
No Test
"""
__author__ = 'Liuyl'
import functools

from loongtian.nvwa.common.storage.db.repository import Repository
from loongtian.nvwa.entities.entity import Entity
from loongtian.nvwa.service.repository_service.base_knowledge_service import BaseKnowledgeService
from loongtian.nvwa.service import real_object_srv, original_srv
from loongtian.nvwa.common.utils.display import DisplayHelper


class KnowledgeForFragment(Entity):
    """
    片段的数据对象
    
    Id 唯一标识，要考虑上亿级数据的不重复。
    Start 丁字形结构的开始节点，记录的是Id。
    End 丁字形结构的右上角节点，记录的是Id。
    _display 调试时显示的内容
    """
    __slots__ = ('Id', 'Start', 'End', '_display')

    def __init__(self, **kwargs):
        super(KnowledgeForFragment, self).__init__()
        self.Id = str(kwargs.get('Id', None))
        self.Start = kwargs.get('Start', '')
        self.End = kwargs.get('End', '')
        self._display = kwargs.get('Display', '')

    def __eq__(self, other):
        """
        判断两个KnowledgeForFragment结构是否相同
        :param other:
        :return:
        """
        if self.Id == other.Id and self.Start == other.Start and self.End == other.End:
            return True
        else:
            return False

    def __hash__(self):
        ids = self.Id + self.Start + self.End
        return ids.__hash__()

    @property
    def Display(self):
        return self._display


class KnowledgeForFragmentRepository(Repository):
    """
    独立片段的数据仓库,不可手动调用，由KnowledgeForFragment的多个实例组成。
    """
    def __init__(self):
        super(KnowledgeForFragmentRepository, self).__init__('Fragment', KnowledgeForFragment)
        self.index2i_dict['start_bin'] = 'Start'
        self.index2i_dict['end_bin'] = 'End'
        self.get_by_start = functools.partial(self.get_by_index2i, idx='start_bin')
        self.gets_by_start = functools.partial(self.gets_by_index2i, idx='start_bin')
        self.get_key_by_start = functools.partial(self.get_key_by_index2i, idx='start_bin')
        self.gets_key_by_start = functools.partial(self.gets_key_by_index2i, idx='start_bin')
        self.get_by_end = functools.partial(self.get_by_index2i, idx='end_bin')
        self.gets_by_end = functools.partial(self.gets_by_index2i, idx='end_bin')
        self.get_key_by_end = functools.partial(self.get_key_by_index2i, idx='end_bin')
        self.gets_key_by_end = functools.partial(self.gets_key_by_index2i, idx='end_bin')


class KnowledgeForFragmentService(BaseKnowledgeService):
    """
    独立片段的数据仓库服务
    如需创建一个公用片段数据仓库,可调用fragment_srv.get_new_knowledge_for_fragment_service()
    """
    def __init__(self, rep):
        super(KnowledgeForFragmentService, self).__init__(rep)

class Fragment(object):
    """
    片段
    """
    def __init__(self, ref, rep_srv):
        """
        不可手动创建Fragment对象,须通过FragmentService的generate相关函数创建
        :param rep_srv: 如指定,则片段使用传入的rep_srv作为读写rep,否则片段将拥有自己的独立rep
        :return:
        """
        self._rep_srv = rep_srv
        self._ref = self.rep_srv.get(ref.Id)
        if not self._ref:
            raise Exception('指定ref不存在于rep中')
        self._extra_ref = []

    def save_to_target_rep_srv(self, target_rep_srv):
        """
        不可手动调用,只可在创建新片段且片段拥有独立rep时由FragmentService的generate相关函数调用
        直接在rep中生成了新的数据,所有的非引用id都应存在对应的RealObject
        :param ref: 对象必须存在与data参数中
        :param dataDict: 拥有id,start,end结构的entity列表
        :return:
        """

        def deep_save(cur_id):
            if real_object_srv.get(cur_id):
                return cur_id
            _cur = self.rep_srv.get(cur_id)
            if _cur:
                _new_start_id = deep_save(_cur.Start)
                _new_end_id = deep_save(_cur.End)
                _next_cur = target_rep_srv.create(Start=_new_start_id, End=_new_end_id, Display=_cur.Display)
                return _next_cur.Id
            else:
                raise Exception('片段内数据不完整,无法保存')

        _new_id = deep_save(self.ref.Id)
        for _extra in self._extra_ref:
            deep_save(_extra)
        return target_rep_srv.get(_new_id)

    def __str__(self):
        return DisplayHelper.get(self.ref, self.rep_srv)

    @property
    def rep_srv(self):
        return self._rep_srv

    @property
    def ref(self):
        return self._ref

    @property
    def deep_start(self):
        _entity = self.start
        if _entity and hasattr(_entity, 'Start'):
            _r = self.rep_srv.get(_entity.Start)
            if not _r:
                raise Exception('片段内数据不完整,无法得到deep_start')
            return _r
        return None

    @property
    def deep_end(self):
        _entity = self.start
        if _entity and hasattr(_entity, 'End'):
            _r = self.rep_srv.get(_entity.End)
            if not _r:
                raise Exception('片段内数据不完整,无法得到deep_end')
            return _r
        return None

    @property
    def start(self):
        if not hasattr(self.ref, 'Start'):
            return None
        _entity = self.rep_srv.get(self.ref.Start)
        if not _entity:
            raise Exception('片段内数据不完整,无法得到start')
        return _entity

    @property
    def end(self):
        if not hasattr(self.ref, 'End'):
            return None
        _entity = self.rep_srv.get(self.ref.End)
        if not _entity:
            raise Exception('片段内数据不完整,无法得到end')
        return _entity

    @property
    def data(self):
        """
        返回片段的data列表,即能够表示该片段信息的所有Knowledge(或其他)的对象集合
        :return:
        """
        _result = []

        def get_deep_inner(cur):
            if hasattr(cur, 'Start'):
                _next = self.rep_srv.get(cur.Start)
                if _next:
                    _result.append(_next)
                    get_deep_inner(_next)
            if hasattr(cur, 'End'):
                _next = self.rep_srv.get(cur.End)
                if _next:
                    _result.append(_next)
                    get_deep_inner(_next)

        if self.rep_srv.get(self.ref.Id):
            _result.append(self.ref)
        get_deep_inner(self.ref)
        for _extra in self._extra_ref:
            get_deep_inner(_extra)
        return _result

    def __eq__(self, other):
        """
        判断两个Fragment结构是否相同.
        仅比较ref是否为相同对象
        :param other:
        :return:
        """
        return original_srv.Equal.check(self.ref, other.ref)

    def __hash__(self):
        return self.ref.Id.__hash__()


if __name__ == '__main__':
    import doctest

    doctest.testmod()