#!/usr/bin/env python
# coding: utf-8
"""
原始知识初始化

Project:  nvwa
Title:    original 
Author:   Liuyl 
DateTime: 2014/10/28 13:55 
UpdateLog:
1、Liuyl 2014/10/28 Create this File.
2、Liuyl 2014/12/5 该文件不再负责初始化原始标签, 仅负责初始化用于测试的知识等
原始知识的初始化,维护及访问接口
>>> print("No Test")
No Test
"""
from loongtian.nvwa.core.engines.meantool.placeholder import PlaceHolder
from loongtian.nvwa.core.minds.action_functions_engine import function_dic

__author__ = 'Liuyl'

from loongtian.nvwa.core.gdef import GlobalDefine
from loongtian.nvwa.service import knowledge_srv, metadata_srv, real_object_srv, \
    original_srv, fsc
from loongtian.nvwa.core.gdef import OID
from loongtian.nvwa.core.minds.collection_mind import *

class OriginalInitService(object):
    def __init__(self):
        self.original_real_object_dict = GlobalDefine().original_real_object_dict
        self.inited = False

    def init(self, for_test=False):
        self.init_memory(for_test=for_test)

    def init_memory(self, is_to_db=False, for_test=False):
        """
        :return:
        """

        # 清空仓库
        knowledge_srv.clear()
        metadata_srv.clear()

        def init_real_object():
            pass

        def init_metadata():
            metadata_list = []
            metadata_list.extend([u'嗯哪', u'不知道', u'知道了', u'知道', u'但是', u'有',
                                  u'的', u'条', u'没有', u'不一定', u'不对',u'包含'])
            for _s in metadata_list:
                metadata_srv.create(_s)
            metadata_srv.create(u'是', is_create_first_class=False)
            metadata_srv.create(u'不是', is_create_first_class=False)

        def init_real_object_for_test():
            def generate_real_object_with_metadata(display, meta_string_value):
                _entity = real_object_srv.create(Display=display)
                metadata_srv.link_real_object_metadata(meta_string_value, _entity)
                return _entity

            def generate_number(num):
                metadata_srv.create(num)
                _object = generate_real_object_with_metadata(num, num)
                original_srv.InheritFrom.Number.set(_object)
                return _object

            for _n in range(10):
                generate_number(_n.__str__().decode("utf-8"))
            generate_number(u'几')
            generate_number(u'多少')
            # 条
            # _act_object = real_object_srv.create(Display=u'条')
            # metadata_srv.link_real_object_metadata(u'条', _act_object)
            # original_srv.InheritFrom.Quantifier.set(_act_object)
            # _p1 = action_define_srv.create_placeholder(_act_object, 1)
            # _p2 = action_define_srv.create_placeholder(_act_object, 2)
            # _p3 = action_define_srv.create_placeholder(_act_object, 3)
            # _s1 = original_srv.InheritFrom.Number.set(_p1, action_define_srv)
            # _restrict1 = original_srv.FRestrict.set(_p1, _s1, action_define_srv)
            # _seq = action_define_srv.create_t_structure(_p1, _act_object, _p2)
            # original_srv.InheritFrom.Collection.set(_p3, action_define_srv)
            # original_srv.ItemInf.set(_p3, _p2, action_define_srv)
            # original_srv.CountIs.set(_p3, _p1, action_define_srv)
            # original_srv.QuantifierIs.set(_p3, _act_object, action_define_srv)
            # _step = _p3
            # action_srv.create(u'条', RealObjectId=_act_object.Id,
            # Sequence=[[_seq.Id]],
            # Steps=[[_step.Id, _restrict1.Id]])

        def init_knowledge_for_test():
            def get_first_class(meta_string):
                _m = metadata_srv.get_by_string_value(meta_string)
                if not _m:
                    _m = metadata_srv.create(meta_string)
                _default_class = metadata_srv.get_default_class(_m)[0]
                _first_class = original_srv.relation_deep_find(original_srv.SymbolInherit, right=_default_class)[0]
                return _first_class

            # _cow = get_first_class(u"牛")
            # _horse = get_first_class(u"马")
            # _sheep = get_first_class(u"羊")
            # _leg = get_first_class(u"腿")
            # _animal = get_first_class(u"动物")
            # original_srv.Component.set(_sheep, _leg)
            # original_srv.CommonIs.set(_cow, _animal)
            # original_srv.CommonIs.set(_horse, _animal)
            # original_srv.CommonIs.set(_sheep, _animal)
            #
            # _yellow = get_first_class(u"黄色")
            # _green = get_first_class(u"绿色")
            # _white = get_first_class(u"白色")
            # _color = get_first_class(u"颜色")
            # # original_srv.Multi.set(_color, right=None)
            # original_srv.InheritFrom.set(_yellow, _color)
            # original_srv.InheritFrom.set(_white, _color)
            # original_srv.InheritFrom.set(_green, _color)
            # original_srv.Attribute.set(_leg, _yellow)
            # #original_srv.Attribute.set(_zhiti, _yellow)
            # _zhuzi = get_first_class(u'竹子')
            # original_srv.Attribute.set(_zhuzi, _green)

        def write_display():
            # 将描述名与知识的映射字典记录到文件中
            f = open('knowledge_display_dict.py', 'w')
            f.write('#!/usr/bin/env python\n')
            f.write('# -*- coding: utf-8 -*-\n')
            f.write('"""\n该文件为初始化知识库时自动创建,提供一个字典,可以通过描述名获取knowledge的id\n"""\n')
            f.write('display_dict={\n')
            for key in self.original_real_object_dict:
                f.write("    '%s':['%s','%s'],\n" % (
                    key, self.original_real_object_dict[key][0], self.original_real_object_dict[key][1]))
            f.write('}\n')
            f.close()

        def init_action():

            def create_common_action(action_object, relation_object):

                # 修改用通用占位符 fengyh 2015-7-1
                ph_list1 = PlaceHolder.get_n_placeholder(2)
                _p1 = ph_list1[0]
                _p2 = ph_list1[1]

                # _p1 = fsc.action.create_placeholder(action_object, 1)
                # _p2 = fsc.action.create_placeholder(action_object, 2)

                _step = knowledge_srv.create_t_structure(_p1, relation_object, _p2)
                _seq = knowledge_srv.create_t_structure(_p1, action_object, _p2)
                fsc.action.assemble(knowledge_srv,real_object=action_object,sequence=_seq,steps=[_step])

            for _a in GlobalDefine().action_list:
                _m = metadata_srv.create(_a)
                _c_object = metadata_srv.get_default_class(_m)[0]
                _object = original_srv.relation_deep_find(original_srv.SymbolInherit, right=_c_object)[0]
                _c_action_object = metadata_srv.create_default_action(_m)
                _action_object = real_object_srv.create(Display=_a)
                original_srv.SymbolInherit.set(_action_object, _c_action_object)
                create_common_action(_action_object, _object)

            # '有'的预定义继承树
            _have_meta = metadata_srv.get_by_string_value(u'有')
            _have_c_object = metadata_srv.get_default_class(_have_meta)[0]
            _have_common_object = original_srv.relation_deep_find(original_srv.SymbolInherit, right=_have_c_object)[0]
            _have_component_object = original_srv.Component.obj()
            _have_attribute_object = original_srv.Attribute.obj()
            original_srv.InheritFrom.set(_have_component_object, _have_common_object)
            original_srv.InheritFrom.set(_have_attribute_object, _have_common_object)

            _have_c_action_object = metadata_srv.create_default_action(_have_meta)
            _have_common_action_object = real_object_srv.create(Display=u'有[通用]')
            _have_component_action_object = real_object_srv.create(Display=u'有[组件]')
            _have_attribute_action_object = real_object_srv.create(Display=u'有[属性]')
            original_srv.SymbolInherit.set(_have_common_action_object, _have_c_action_object)
            original_srv.SymbolInherit.set(_have_component_action_object, _have_common_action_object)
            original_srv.SymbolInherit.set(_have_attribute_action_object, _have_common_action_object)

            create_common_action(_have_common_action_object, _have_common_object)
            create_common_action(_have_component_action_object, _have_component_object)
            create_common_action(_have_attribute_action_object, _have_attribute_object)

            # '没有'的预定义继承树
            _have_not_meta = metadata_srv.get_by_string_value(u'没有')
            _have_not_common_object = real_object_srv.create(Display=u'有[否定]')
            _have_not_component_object = real_object_srv.create(Display=u'组件[否定]')
            _have_not_attribute_object = real_object_srv.create(Display=u'属性[否定]')
            original_srv.Negate.set(_have_not_common_object, _have_common_object)
            original_srv.Negate.set(_have_not_component_object, _have_component_object)
            original_srv.Negate.set(_have_not_attribute_object, _have_attribute_object)
            original_srv.Negate.set(_have_common_object, _have_not_common_object)
            original_srv.Negate.set(_have_component_object, _have_not_component_object)
            original_srv.Negate.set(_have_attribute_object, _have_not_attribute_object)
            original_srv.InheritFrom.set(_have_not_component_object, _have_not_common_object)
            original_srv.InheritFrom.set(_have_not_attribute_object, _have_not_common_object)

            _have_not_c_action_object = metadata_srv.create_default_action(_have_not_meta)
            _have_not_common_action_object = real_object_srv.create(Display=u'没有[通用]')
            _have_not_component_action_object = real_object_srv.create(Display=u'没有[组件]')
            _have_not_attribute_action_object = real_object_srv.create(Display=u'没有[属性]')
            original_srv.SymbolInherit.set(_have_not_common_action_object, _have_not_c_action_object)
            original_srv.SymbolInherit.set(_have_not_component_action_object, _have_not_common_action_object)
            original_srv.SymbolInherit.set(_have_not_attribute_action_object, _have_not_common_action_object)

            create_common_action(_have_not_common_action_object, _have_not_common_object)
            create_common_action(_have_not_component_action_object, _have_not_component_object)
            create_common_action(_have_not_attribute_action_object, _have_not_attribute_object)

            # '是'的预定义继承树
            _is_meta = metadata_srv.get_by_string_value(u'是')
            _is_common_object = original_srv.CommonIs.obj()
            _is_self_object = original_srv.IsSelf.obj()
            _is_inherit_from_object = original_srv.InheritFrom.obj()
            original_srv.InheritFrom.set(_is_self_object, _is_common_object)
            original_srv.InheritFrom.set(_is_inherit_from_object, _is_common_object)

            _is_c_action_object = metadata_srv.create_default_action(_is_meta)
            _is_common_action_object = real_object_srv.create(Display=u'是[通用]')
            _is_self_action_object = real_object_srv.create(Display=u'是[自反]')
            _is_inherit_from_action_object = real_object_srv.create(Display=u'是[继承]')
            original_srv.SymbolInherit.set(_is_common_action_object, _is_c_action_object)
            original_srv.SymbolInherit.set(_is_self_action_object, _is_common_action_object)
            original_srv.SymbolInherit.set(_is_inherit_from_action_object, _is_common_action_object)

            create_common_action(_is_common_action_object, _is_common_object)
            create_common_action(_is_self_action_object, _is_self_object)
            create_common_action(_is_inherit_from_action_object, _is_inherit_from_object)

            # '不是'的预定义继承树
            _is_not_meta = metadata_srv.get_by_string_value(u'不是')
            _is_not_common_object = real_object_srv.create(Display=u'通用是[否定]')
            _is_not_self_object = real_object_srv.create(Display=u'自反是[否定]')
            _is_not_inherit_from_object = real_object_srv.create(Display=u'继承自[否定]')
            original_srv.Negate.set(_is_not_common_object, _is_common_object)
            original_srv.Negate.set(_is_not_self_object, _is_self_object)
            original_srv.Negate.set(_is_not_inherit_from_object, _is_inherit_from_object)
            original_srv.Negate.set(_is_common_object, _is_not_common_object)
            original_srv.Negate.set(_is_self_object, _is_not_self_object)
            original_srv.Negate.set(_is_inherit_from_object, _is_not_inherit_from_object)
            original_srv.InheritFrom.set(_is_not_self_object, _is_not_common_object)
            original_srv.InheritFrom.set(_is_not_inherit_from_object, _is_not_common_object)

            _is_not_c_action_object = metadata_srv.create_default_action(_is_not_meta)
            _is_not_common_action_object = real_object_srv.create(Display=u'不是[通用]')
            _is_not_self_action_object = real_object_srv.create(Display=u'不是[自反]')
            _is_not_inherit_from_action_object = real_object_srv.create(Display=u'不是[继承]')
            original_srv.SymbolInherit.set(_is_not_common_action_object, _is_not_c_action_object)
            original_srv.SymbolInherit.set(_is_not_self_action_object, _is_not_common_action_object)
            original_srv.SymbolInherit.set(_is_not_inherit_from_action_object, _is_not_common_action_object)

            create_common_action(_is_not_common_action_object, _is_not_common_object)
            create_common_action(_is_not_self_action_object, _is_not_self_object)
            create_common_action(_is_not_inherit_from_action_object, _is_not_inherit_from_object)

            # 的
            _de_meta = metadata_srv.get_by_string_value(u'的')
            _de_c_action_object = metadata_srv.create_default_action(_de_meta)
            _de_action_object = real_object_srv.create(Display=u'的')
            original_srv.SymbolInherit.set(_de_action_object, _de_c_action_object)

            # 修改用统一方法处理占位符 fengyh 2015-7-1
            create_common_action(_de_action_object, original_srv.BeModified.obj())

            # 包含
            _de_meta = metadata_srv.get_by_string_value(u'包含')
            _de_c_action_object = metadata_srv.create_default_action(_de_meta)
            _de_action_object = real_object_srv.create(Display=u'包含')
            original_srv.SymbolInherit.set(_de_action_object, _de_c_action_object)

            # 修改用统一方法处理占位符 fengyh 2015-7-1
            create_common_action(_de_action_object, original_srv.CollectionContainItem.obj())

            #
            # _de_p1 = fsc.action.create_placeholder(_de_action_object, 1)
            # _de_p2 = fsc.action.create_placeholder(_de_action_object, 2)
            # _de_step = knowledge_srv.create_t_structure(_de_p2, original_srv.BeModified.obj(), _de_p1)
            # _de_seq = knowledge_srv.create_t_structure(_de_p1, _de_action_object, _de_p2)
            # fsc.action.assemble(knowledge_srv,real_object=_de_action_object,sequence=_de_seq,steps=[_de_step])
            #
            # ph_list1 = PlaceHolder.get_n_placeholder(2)
            #     _p1 = ph_list1[0]
            #     _p2 = ph_list1[1]
            #
            #     # _p1 = fsc.action.create_placeholder(action_object, 1)
            #     # _p2 = fsc.action.create_placeholder(action_object, 2)
            #
            #     _step = knowledge_srv.create_t_structure(_p1, relation_object, _p2)
            #     _seq = knowledge_srv.create_t_structure(_p1, action_object, _p2)
            #     fsc.action.assemble(knowledge_srv,real_object=action_object,sequence=_seq,steps=[_step])

            # _default_de_class = metadata_srv.get_default_class(_m)[0]
            # # 是...的(属性)
            # _is_attribute_action = real_object_srv.create(Display=u'是...的')
            # original_srv.InheritFrom.set(_is_attribute_action, _is_action)
            # original_srv.SymbolInherit.set(_is_attribute_action, _is_action)
            # _p1 = action_define_srv.create_placeholder(_is_attribute_action, 1)
            # _p2 = action_define_srv.create_placeholder(_is_attribute_action, 2)
            # _step = action_define_srv.create_t_structure(_p1, original_srv.Attribute.obj(), _p2)
            # _l = action_define_srv.create_l_structure(_p2, _default_de_class)
            # _seq = action_define_srv.create_t_structure(_p1, _is_attribute_action, _l)
            # action_srv.create(Display=u'是...的', RealObjectId=_is_attribute_action.Id,
            # Sequence=[[_seq.Id]],
            # Steps=[[_step.Id]])

        # 以下添加函数初始化数据，创建函数初始元数据
        def init_function():
            for _a in function_dic.keys():
                _m = metadata_srv.create(_a)
                _c_object = metadata_srv.get_default_class(_m)[0]
                original_srv.InheritFrom.set(_c_object, real_object_srv.get(OID.FunctionBase))
                original_srv.FunctionName.set(_c_object,real_object_srv.create(Display=function_dic.__getitem__(_a)))
                _c_action_object = metadata_srv.create_default_action(_m)
                _action_object = real_object_srv.create(Display=_a)
                original_srv.SymbolInherit.set(_action_object, _c_action_object)
            pass

        # 建立系统中的基本RealObject
        init_real_object()
        # 建立一些预定义的object及其metadata
        init_metadata()
        # 建立用于测试的RealObject
        if for_test:
            init_real_object_for_test()
        # 建立一些预定义的action及其metadata
        init_action()
        # 初始化函数
        init_function()

        # 建立用于测试的知识
        if for_test:
            init_knowledge_for_test()


if __name__ == '__main__':
    # import doctest
    #
    # doctest.testmod()
    from loongtian.nvwa.service import original_init_srv

    original_init_srv.init()