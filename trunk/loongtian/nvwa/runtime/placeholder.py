# /usr/bin/python
# coding: utf-8
__author__ = 'Leon'

"""
[运行时对象]占位符操作的封装类（不在数据库中存储）
"""
from loongtian.nvwa.models.enum import ObjType
from loongtian.nvwa.models.realObject import RealObject
from loongtian.nvwa.models.knowledge import Knowledge
from loongtian.nvwa.runtime.instinct import Instincts

class Placeholder(object):
    """
    [运行时对象]占位符操作的封装类（不在数据库中存储）
    """

    @staticmethod
    def get_placeholder_dict(inputs, objs_with_placeholders):
        """
        取得占位符对应的输入实际对象的词典，例如：牛-有-尾巴，？1-有-？2，？1就对应牛，？2就对应尾巴
        :param inputs:
        :param objs_with_placeholders:
        :return:
        """
        if not len(inputs) == len(objs_with_placeholders):  # 如果两者长度不相等，说明模式不匹配
            return None
        placeholder_obj_dict = {}
        obj_placeholder_dict = {}
        for i in range(len(objs_with_placeholders)):
            obj_with_placeholder = objs_with_placeholders[i]
            # 这里要取出对应的输入
            try:
                cur_input = inputs[i]
            except:  # 如果取不出来，说明两者不相匹配
                return None

            if isinstance(obj_with_placeholder, RealObject) and obj_with_placeholder.isPlaceHolder():
                if not isinstance(cur_input, RealObject):  # 如果两者不相匹配，说明模式不匹配
                    return None
                placeholder_obj_dict[obj_with_placeholder] = cur_input
                obj_placeholder_dict[cur_input] = obj_with_placeholder
            elif isinstance(obj_with_placeholder, list):
                if not isinstance(cur_input, list):  # 如果两者不相匹配，说明模式不匹配
                    return None
                child_placeholder_obj_dict, child_obj_placeholder_dict = Placeholder.get_placeholder_dict(cur_input,
                                                                                                               obj_with_placeholder)
                if child_placeholder_obj_dict:
                    placeholder_obj_dict.update(child_placeholder_obj_dict)
                    obj_placeholder_dict.update(child_obj_placeholder_dict)

        return placeholder_obj_dict, obj_placeholder_dict

    @staticmethod
    def replaceWithPlaceholderDict(objs, placeholder_dict):
        """
        使用占位符词典，对现有对象序列进行替换。例如：将牛 组件 腿，使用"占位符牛 有 占位符腿"，替换为"占位符牛 组件 占位符腿"
        :param objs:
        :param placeholder_dict:
        :return:
        """
        if not isinstance(objs, list):
            return None
        replaced_objs = []
        for obj in objs:
            if isinstance(obj, list):
                child_replaced_objs = Placeholder.replaceWithPlaceholderDict(obj, placeholder_dict)
                replaced_objs.append(child_replaced_objs)
            else:
                replaced_obj = placeholder_dict.get(obj)
                if replaced_obj:
                    replaced_objs.append(replaced_obj)
                else:
                    replaced_objs.append(obj)

        return replaced_objs

    @staticmethod
    def _createPlaceHolders(objs,
                            executable=None,
                            checkExist=False,
                            recordInDB=False,
                            memory=None,
                            addParent=False,
                            other_executables=None):
        """
        根据对象链创建pattern
        :param objs:
        :param executable:可执行性的实际对象（包括Instinct\Action\Modifier\Knowledge[因为...所以...]\List）
        :param checkExist:
        :param recordInDB:
        :param memory:
        :param addParent: 是否将模式的父对象添加到占位符的父对象（默认False），例如根据“牛有腿”生成“有”，牛是动物，是否将动物添加到左占位符
        :return:
        """
        pattern_objs = []
        pattern_dict = {}
        splits = []
        cur_split = []
        if other_executables:
            other_executables.append(executable)
            executable = other_executables
        for i in range(len(objs)):
            obj = objs[i]
            if isinstance(obj, list):
                child_pattern_objs, child_pattern_dict, child_splits = \
                    Placeholder._createPlaceHolders(obj, executable,
                                                    recordInDB=recordInDB,
                                                    memory=memory)
                pattern_objs.append(child_pattern_objs)
                pattern_dict.update(child_pattern_dict)
                splits.append(tuple(child_splits))
                continue

            if executable:  # 把executable及other_executables剔除，并把前面的链打包，例如：
                if isinstance(executable, list):
                    objExecutable = False
                    for exe in executable:
                        if obj.id == exe.id:  # 一个对象不能解释自身
                            pattern_objs.append(obj)
                            objExecutable = True
                            break
                    if objExecutable:
                        if len(cur_split) > 0:
                            splits.append(tuple(cur_split))
                            splits.append(executable)
                            cur_split = []
                        else:
                            splits.append(executable)
                        continue
                elif isinstance(executable, RealObject):
                    if obj.id == executable.id:  # 一个对象不能解释自身
                        pattern_objs.append(obj)
                        if len(cur_split) > 0:
                            splits.append(tuple(cur_split))
                            splits.append(executable)
                            cur_split = []
                        else:
                            splits.append(executable)
                        continue

            _remark = "placeholder-%s"
            if isinstance(obj, RealObject):  # 略去所有的可执行性对象
                if obj.isExecutable():
                    pattern_objs.append(obj)
                    if len(cur_split) > 0:
                        splits.append(tuple(cur_split))
                        splits.append(obj)
                        cur_split = []
                    else:
                        splits.append(obj)
                    continue
                _remark = _remark % obj.remark
            elif isinstance(obj, Knowledge):
                obj.getChainItems()
                _remark = _remark % obj._t_chain_words

            # 剩下的应该是不可执行的RealObject、knowledge，创建占位符
            placeholder = RealObject(remark=_remark,
                                     type=ObjType.PLACEHOLDER,
                                     memory=memory).create(checkExist=checkExist,
                                                           recordInDB=recordInDB)
            pattern_objs.append(placeholder)
            pattern_dict[obj] = placeholder
            cur_split.append(placeholder)

            # 对占位符的父对象进行限定，例如：牛-有-腿，马-有-腿，生成的第一个占位符应该是牛和马的共同父对象
            if isinstance(obj, Knowledge):
                placeholder.Constitutions.addParent(Instincts.instinct_original_knowledge,recordInDB=recordInDB)

            elif isinstance(obj, RealObject) and addParent:
                # 首先取得obj的父对象
                parents, parents_ks = obj.Constitutions.getSelfParentObjects()
                if parents:
                    # 逐个添加父对象
                    for parent in parents:
                        placeholder.Constitutions.addParent(parent,recordInDB=recordInDB)

            if i == len(objs) - 1:  # 如果是最后一个，直接添加到splits
                splits.append(tuple(cur_split))

        return pattern_objs, pattern_dict, splits



