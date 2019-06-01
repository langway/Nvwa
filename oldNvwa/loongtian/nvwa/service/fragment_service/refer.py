#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    refer 
Author:   Liuyl 
DateTime: 2015/6/15 16:03 
UpdateLog:
1、Liuyl 2015/6/15 Create this File.

refer
>>> print("No Test")
No Test
"""
from loongtian.nvwa.entities import enum
from loongtian.nvwa.service import original_srv
from loongtian.nvwa.service.fragment_service.fragment import FragmentService
from loongtian.nvwa.service.fragment_service.fragment_definition.refer import ReferFragment

__author__ = 'Liuyl'


class ReferFragmentEnum(object):
    def __init__(self):
        enum(ReferFragmentEnum,
             'PreRefer=0,PostRefer=1,Steps=2',
             sep=',')
        pass


ReferFragmentEnum()


class ReferFragmentService(FragmentService):
    def __init__(self):
        super(ReferFragmentService, self).__init__()

    def generate(self, ref, rep_srv):
        if not ref:
            return None
        return ReferFragment(ref, rep_srv)

    def assemble(self, target_srv, *args, **kwargs):
        """
        组装
        :param target_srv:
        :param kwargs: deep_start,deep_end,start,end
        :return:
        """
        refer_builder = kwargs.get('refer_builder', None)
        if refer_builder:
            _pre_refer_frag = self.save_to_target_service(refer_builder.move_result[refer_builder.pre_refer_string],
                                                          target_srv)
            _post_refer_frag = None
            for _step in refer_builder.step_string_list[::-1]:
                _step_frag = None
                for _item in _step[::-1]:
                    _item_frag = self.save_to_target_service(refer_builder.move_result[_item], target_srv)
                    if not _step_frag:
                        _step_frag = _item_frag
                    else:
                        _step_frag = self.generate(
                            original_srv.And.set(_item_frag.ref, _step_frag.ref, target_srv),
                            target_srv)
                if not _post_refer_frag:
                    _post_refer_frag = _step_frag
                else:
                    _post_refer_frag = self.generate(
                        original_srv.Next.set(_step_frag.ref, _post_refer_frag.ref, target_srv),
                        target_srv)
            _ref = original_srv.Refer.set(_pre_refer_frag.ref, _post_refer_frag.ref, target_srv)
            return self.generate(_ref, target_srv)
        else:
            return None

    def unassemble(self, frag):
        _result = dict()
        _result[ReferFragmentEnum.PreRefer] = self.get_deep_start(frag)
        _result[ReferFragmentEnum.PostRefer] = self.get_end(frag)

        _steps_frag = _result[ReferFragmentEnum.PostRefer]
        _steps = []

        def _get_items(items_frag):
            _items_frag = items_frag
            _items = []
            while _items_frag.deep_end and original_srv.Equal.check(_items_frag.deep_end, original_srv.And.obj()):
                _items.append(self.get_deep_start(_items_frag))
                _items_frag = self.get_end(_items_frag)
            _items.append(_items_frag)
            return _items

        while _steps_frag.deep_end and original_srv.Equal.check(_steps_frag.deep_end, original_srv.Next.obj()):
            _steps.append(_get_items(self.get_deep_start(_steps_frag)))
            _steps_frag = self.get_end(_steps_frag)
        _steps.append(_get_items(_steps_frag))
        _result[ReferFragmentEnum.Steps] = _steps
        return _result


if __name__ == '__main__':
    import doctest

    doctest.testmod()