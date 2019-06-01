# /usr/bin/python
# coding: utf-8
__author__ = 'Leon'

from loongtian.nvwa.models.enum import ObjType, DirectionType
from loongtian.nvwa.organs.character import Character

"""
[运行时对象]从数据库layer中取到的一个对象的关联对象（包括关联值，以便排序）
"""

# 弃用
# def comfun(x,y):
#     """
#     根据权重排序的计算函数
#     :param x:
#     :param y:
#     :return:
#     """
#     if hasattr(x,"weight") and hasattr(y,"weight"):
#         if x.weight>y.weight:
#             return True
#         else:
#             return False
#     else:
#         return False

class RelatedObjs(dict):
    """
    [运行时对象]与对象关联的其他对象、关联值weight[dict]，格式为：{obj.id : RelatedObj}
    """

    def __init__(self):
        """
        [运行时对象]与对象关联的其他对象、关联值weight[dict]，格式为：{obj.id : RelatedObj}
        """
        super(RelatedObjs, self).__init__()
        self.sorted_objs_by_weights = None
        self.cur_obj_index = 0  # 当前对象所处的位置

    def add(self, obj, weight=None,source=None):
        """
        添加相关对象
        :param obj:可能是RelatedObj，其他类型的对象，或是上述这样对象的列表
        :param weight:
        :return:
        """
        if obj is None:
            return False

        if isinstance(obj, list):
            for _obj in obj:
                self.add(_obj, weight,source)
        elif isinstance(obj, RelatedObj):
            if not obj.obj is None:
                self[obj.id] = obj
                if weight:
                    obj.weight = weight
                if source:
                    obj.source = source
        else:
            _obj = RelatedObj(obj, weight,source)
            self[obj.id] = _obj

        self.sort(forceToResort=True)  # 添加后强制重新排序

        return True

    def remove(self, relatedObj):
        """
        移除相关对象
        :param relatedObj:
        :return:
        """
        if relatedObj is None:
            return False

        if isinstance(relatedObj, RelatedObj):
            self.pop(relatedObj.id)
            return True
        elif isinstance(relatedObj, str):
            self.pop(relatedObj)
            return True

        return False

    def sort(self, reverse=True, forceToResort=False):
        """
        根据对象的关联值进行排序。
        :param reverse
        :return:
        """
        if self.sorted_objs_by_weights and not forceToResort:
            return self.sorted_objs_by_weights

        self.sorted_objs_by_weights = list(self.values())
        self.sorted_objs_by_weights.sort(key=lambda x: x.weight, reverse=reverse)

        return self.sorted_objs_by_weights

    def getCurObj(self,return_related_obj =False):
        """
        一个对象可能关联多个其他对象，所以可能要逐个处理。
        例如：苹果是个伟大的公司，根据weight，可能最先关联的是能够吃的“苹果”，发现不对后，再找到“苹果公司”
        :return:
        """

        sorted_objs_by_weights = self.sort()

        if self.cur_obj_index < len(sorted_objs_by_weights):
            cur_obj = sorted_objs_by_weights[self.cur_obj_index]
            self.cur_obj_index += 1
            if return_related_obj:
                return cur_obj
            else:
                return cur_obj.obj

        return None

    def getLinkWeight(self,obj):
        """
        取得相关对象的关联值
        :param obj:
        :return:
        """
        from loongtian.nvwa.models.baseEntity import BaseEntity
        if isinstance(obj,BaseEntity):
            relatedObj = self.get(obj.id)
            if relatedObj:
                return relatedObj.weight
        elif isinstance(obj,RelatedObj):
            return obj.weight

        return None

    def restoreCurObjIndex(self):
        """
        将当前对象所处的位置重置为0
        :return:
        """
        self.cur_obj_index = 0  # 当前对象所处的位置

    def merge(self, relatedObjs):
        """
        将relatedObjs与当前列表合并
        :param relatedObjs:
        :return:
        """
        for relatedObj in relatedObjs:
            self.add(relatedObj)

        # 重置index
        self.cur_obj_index = 0


class RelatedObj(object):
    """
    [运行时对象]与当前对象关联的其他对象、关联值。例如metaData关联的realObject，weight
    """

    def __init__(self, obj, weight=Character.Original_Link_Weight,source=None):
        """
        [运行时对象]与当前对象关联的其他对象、关联值。例如metaData关联的realObject，weight
        :param obj:
        :param weight:
        :param source:
        """
        self.obj = obj
        if weight is None:
            weight = Character.Original_Link_Weight
        self.weight = weight  # 与当前对象的关联值
        self.source = source

    @property
    def id(self):
        if self.obj:
            return self.obj.id
        return None

    def __repr__(self):
        return "{RelatedObj:{obj:%s,weight:%s}}" % (self.obj, self.weight)


class _RelatedObjsWithDirection(RelatedObjs):
    """
    [运行时对象]当前对象的上一层对象
    """
    # 在与其他对象的分层中，包含的方向，
    # 例如，MetaNet只能有下层对象MetaData，Knowledge，
    # # MetaData 的上层对象为MetaNet，下层对象为RealObject
    Direction = DirectionType.UNKNOWN

    def __init__(self):
        """
        [运行时对象]当前对象的上一层对象
        """
        super(_RelatedObjsWithDirection, self).__init__()
        self.typed_objects = {}  # IdTypeEnum作为key，其他对象的id为子key，格式为：{ObjType:{id:RelatedObj}}
        self.sorted_typed_objects = {}  # 经过weight排序的对象列表。格式为：{ObjType:[RelatedObj]}
        self.cur_typed_obj_index = {}

    def add(self, relatedObj, weight=None,source=None):
        """
        添加相关对象
        :param relatedObj:
        :param weight:
        :return:
        """
        if relatedObj is None:
            return False

        if not weight:
            if hasattr(relatedObj,"weight"):
                weight=getattr(relatedObj,"weight")
            else:
                weight =Character.Original_Link_Weight

        self._add_to_typed_objects(relatedObj, weight,source)

        self.sort(forceToResort=True)  # 添加后强制重新排序

        return super(_RelatedObjsWithDirection, self).add(relatedObj, weight,source)

    def _add_to_typed_objects(self, relatedObj, weight=Character.Original_Link_Weight,source=None):

        if isinstance(relatedObj, list):
            for obj in relatedObj:
                self._add_to_typed_objects(obj,weight,source)
        else:
            if isinstance(relatedObj, RelatedObj):
                _type = relatedObj.obj.getType()
            else:
                from loongtian.nvwa.models.baseEntity import BaseEntity
                if isinstance(relatedObj, BaseEntity):
                    _type = relatedObj.getType()
                    relatedObj = RelatedObj(relatedObj, weight,source)
                else:
                    raise Exception("不支持的对象类型%s，无法添加到RelatedObjsWithDirection中！" % type(relatedObj))

            if not _type in self.typed_objects:
                self.typed_objects[_type] = {}
            if not _type in self.cur_typed_obj_index:
                self.cur_typed_obj_index[_type] = 0

            self.typed_objects[_type][relatedObj.id] = relatedObj



    def merge(self, relatedObjs):
        """
        将relatedObjs与当前列表合并
        :param relatedObjs:
        :return:
        """
        if isinstance(relatedObjs,list):
            for relatedObj in relatedObjs:
                self.add(relatedObj)
        elif isinstance(relatedObjs,dict):
            for id,relatedObj in relatedObjs.items():
                self.add(relatedObj)
        else:
            raise Exception("无法将relatedObjs与当前列表合并，错误的类型：%s！" % type(relatedObjs))

        # 重置index
        self.cur_obj_index = 0

    def remove(self, relatedObj):
        """
        移除相关对象
        :param relatedObj:
        :return:
        """
        if isinstance(relatedObj, list):
            for obj in relatedObj:
                self.remove(obj)
        elif isinstance(relatedObj, RelatedObj):
            relatedObj = relatedObj.obj
        from loongtian.nvwa.models.baseEntity import BaseEntity
        if isinstance(relatedObj, BaseEntity):
            _type = relatedObj.getType()
            if _type in self.typed_objects:
                self.typed_objects[_type].pop(relatedObj.id)

        super(_RelatedObjsWithDirection, self).remove(relatedObj)

    def getObjsByType(self, type=ObjType.UNKNOWN):
        """
        取得所有指定类型的对象，例如：realobject类型，还会取得实对象、虚对象、动作等
        :param direction:
        :param type:Nvwa对象类型的枚举类型
        :return:{id:RelatedObj}
        """
        if type == ObjType.UNKNOWN:
            return None
        # 取得子类型，例如：要取得realobject类型，还会取得实对象、虚对象、动作等
        sub_types = ObjType.getSubTypes(type)
        if sub_types:
            sub_types.append(type)
            objs = {}
            for sub_type in sub_types:
                sub_objs = self.typed_objects.get(sub_type)
                if sub_objs:
                    objs.update(sub_objs)
            return objs

        else:
            return self.typed_objects.get(type)

    def getSortedObjsByType(self, type=ObjType.UNKNOWN):
        """
        取得所有指定类型的对象，例如：取得MetaNet下一层关联的所有MetaData
        :param direction:
        :param type:Nvwa对象类型的枚举类型
        :return:{id:RelatedObj}
        """
        if type == ObjType.UNKNOWN:
            return None
        self.sort()
        # 取得子类型，例如：要取得realobject类型，还会取得实对象、虚对象、动作等
        sub_types = ObjType.getSubTypes(type)
        if sub_types:
            sub_types.append(type)
            objs = []
            for sub_type in sub_types:
                sub_objs = self.sorted_typed_objects.get(sub_type)
                if sub_objs:
                    objs.extend(sub_objs)
            return objs

        else:
            return self.sorted_typed_objects.get(type)

    def sort(self, reverse=True, forceToResort=False):
        """
        [重载函数]对所有相关对象按weight进行排序
        :param reverse:
        :param forceToResort:
        :return:
        """

        for _type, relatedObjs in self.typed_objects.items():
            self.sortTypedObjs(_type, reverse, forceToResort)

        return super(_RelatedObjsWithDirection, self).sort(reverse, forceToResort)

    def sortTypedObjs(self, type=ObjType.UNKNOWN, reverse=True, forceToResort=False):
        """
        对所有指定类型的相关对象按weight进行排序
        :param type:
        :param reverse:默认由大到小
        :param forceToResort:
        :return:
        """
        if not forceToResort and type in self.sorted_typed_objects:
            return self.sorted_typed_objects[type]

        objs = self.getObjsByType(type)  # {id:RelatedObj}
        if not objs:
            return None
        objs = list(objs.values())

        # objs.sort(cmp=comfun, reverse=reverse)
        objs.sort(key=lambda x: x.weight, reverse=reverse)
        self.sorted_typed_objects[type] = objs
        return objs

    def hasCurTypedObj(self, type=ObjType.UNKNOWN):
        """
        当前游标下的对象是否存在
        :param type:
        :return:
        """
        self.sort()
        cur_typed_index = self.cur_typed_obj_index.get(type)
        if not cur_typed_index:
            return False

        if cur_typed_index < len(self.sorted_typed_objects[type]):
            return True
        return False

    def hasLastTypedObj(self, type=ObjType.UNKNOWN):
        """
        当前游标下的对象是否存在
        :param type:
        :return:
        """
        self.sort()
        cur_typed_index = self.cur_typed_obj_index.get(type)
        if not cur_typed_index:
            return False

        if cur_typed_index >= 0 and cur_typed_index < len(self.sorted_typed_objects[type]):
            return True
        return False

    def getCurTypedObj(self, type=ObjType.UNKNOWN):
        """
        取得当前游标下的对象。一个对象可能关联多个其他对象，所以可能要逐个处理。
        例如：苹果是个伟大的公司，根据weight，可能最先关联的是能够吃的“苹果”，发现不对后，再找到“苹果公司”
        :return:
        """
        self.sort()
        cur_typed_index = self.cur_typed_obj_index.get(type)
        if not cur_typed_index:
            return None

        if cur_typed_index < len(self.sorted_typed_objects[type]):
            self.cur_typed_obj_index[type] += 1
            return self.sorted_typed_objects[type][cur_typed_index]
        return None

    def getLastTypedObj(self, type=ObjType.UNKNOWN):
        """
        一个对象可能关联多个其他对象，所以可能要逐个处理。
        例如：苹果是个伟大的公司，根据weight，可能最先关联的是能够吃的“苹果”，发现不对后，再找到“苹果公司”
        :return:
        """
        self.sort()
        cur_typed_index = self.cur_typed_obj_index.get(type)
        if not cur_typed_index:
            return None
        cur_typed_index -= 1
        if cur_typed_index >= 0 and cur_typed_index < len(self.sorted_typed_objects[type]):
            return self.sorted_typed_objects[type][cur_typed_index]
        return None

    pass


class UpperObjs(_RelatedObjsWithDirection):
    """
    [运行时对象]当前对象的上一层对象
    """
    # 在与其他对象的分层中，包含的方向，
    # 例如，MetaNet只能有下层对象MetaData，Knowledge，
    # # MetaData 的上层对象为MetaNet，下层对象为RealObject
    Direction = DirectionType.UPPER


class LowerObjs(_RelatedObjsWithDirection):
    """
    [运行时对象]当前对象的下一层对象
    """
    # 在与其他对象的分层中，包含的方向，
    # 例如，MetaNet只能有下层对象MetaData，Knowledge，
    # # MetaData 的上层对象为MetaNet，下层对象为RealObject
    Direction = DirectionType.LOWER
    pass

