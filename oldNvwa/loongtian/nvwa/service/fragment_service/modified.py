#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    modified 
Author:   Liuyl 
DateTime: 2014/12/16 15:53 
UpdateLog:
1、Liuyl 2014/12/16 Create this File.

modified
>>> print("No Test")
No Test
"""
from loongtian.nvwa.service import original_srv, real_object_srv
from loongtian.nvwa.service.fragment_service.fragment import FragmentService, FragmentEnum
from loongtian.nvwa.service.fragment_service.fragment_definition.modified import ModifiedFragment

__author__ = 'Liuyl'


class ModifiedFragmentService(FragmentService):
    def __init__(self):
        super(ModifiedFragmentService, self).__init__()

    def generate(self, ref, rep_srv):
        if not ref:
            return None
        return ModifiedFragment(ref, rep_srv)

    def create_t_structure(self, left_frag, right_frag, bottom_frag, rep_srv):
        _frag = super(ModifiedFragmentService, self).create_t_structure(left_frag, right_frag, bottom_frag, rep_srv)
        _left_modified_frag = getattr(left_frag, 'modified_frag', left_frag)
        _right_modified_frag = getattr(right_frag, 'modified_frag', right_frag)
        _bottom_modified_frag = getattr(bottom_frag, 'modified_frag', bottom_frag)
        _frag.modified_frag = super(ModifiedFragmentService, self).create_t_structure(_left_modified_frag,
                                                                                      _right_modified_frag,
                                                                                      _bottom_modified_frag, rep_srv)
        return _frag

    def create_l_structure(self, left_frag, right_frag, rep_srv):
        _frag = super(ModifiedFragmentService, self).create_l_structure(left_frag, right_frag, rep_srv)
        _left_modified_frag = getattr(left_frag, 'modified_frag', left_frag)
        _right_modified_frag = getattr(right_frag, 'modified_frag', right_frag)
        _frag.modified_frag = super(ModifiedFragmentService, self).create_l_structure(_left_modified_frag,
                                                                                      _right_modified_frag, rep_srv)
        return _frag

    def save_to_target_service(self, fragment, target_srv):
        """
        将片段的完整信息保存到目标仓库服务中.
        :param fragment:需要保存的片段
        :param target_srv:目标仓库服务
        :return: 返回片段在目标仓库中的新实例
        """
        _frag = self.generate(fragment.save_to_target_rep_srv(target_srv), rep_srv=target_srv)
        _frag.modified_frag = getattr(fragment, 'modified_frag', fragment)
        return _frag

    @staticmethod
    def check(frag, rep_srv):
        if hasattr(frag.ref, "Start"):
            _s = rep_srv.get(frag.ref.Start)
            if hasattr(_s, "End"):
                if original_srv.Equal.check(original_srv.BeModified.obj(), real_object_srv.get(_s.End)):
                    return True
        return False

    def assemble(self, target_srv, *args, **kwargs):
        """
        组装
        :param target_srv:
        :param kwargs: deep_start,end
        :return:
        """
        deep_start = kwargs.get('deep_start', None)
        end = kwargs.get('end', None)
        _ref = original_srv.BeModified.set(deep_start, end, target_srv)
        return self.generate(_ref, rep_srv=target_srv)

    def unassemble(self, frag):
        _result = dict()
        _result[FragmentEnum.DeepStart] = self.get_deep_start(frag)
        _result[FragmentEnum.End] = self.get_end(frag)
        return _result


if __name__ == '__main__':
    import doctest

    doctest.testmod()