#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

from loongtian.util.common.enum import Enum

class OriginalType(Enum):
    """
    集合的原始类型。realobject或knowledge
    """
    UNKNOWN = 0
    REALOBJECT = 1
    KNOWLEDGE = 2


"""
传统上，在不同场合，同一语词可以表达集合概念，也可以不表达集合概念。
如：“人”，在“人包括男人、女人”这一判断中，“人”是集合概念，因为这里指的是所有的人，不是具体到每一个人都具有由猿转化的性质； 
在“张三是人”以及“人是由猿转化而来的”两个判断中，“人”是非集合概念，表示人这一类动物或其中一分子，是虚对象。
区别某个语词是否表达集合概念，须结合语言环境而定，
即需要把某一领域的每一个对象与概念反映的性质联系起来考察。
准确区分集合概念与非集合概念，有助于避免犯混淆概念的逻辑错误。
实际上，集合概念与非集合概念，是一体两面的东西，只要一个对象在四维空间中出现组件这一构成，它既具有两面性

我的衣服是我的
我的衣服，构成了一个集合（所有衣服）
我的东西，构成了一个集合（所有物品）
前者属于后者，是后者的一个子集
"""


# todo 目前未考虑嵌套集合
class Collection():
    """
    [运行时对象]所有集合操作的封装类（不在数据库中存储）。
    """
    """
    在nvwa系统中，集合并不是真实存在的。
    集合只是realobject的组件的列表（自然无序，除非有‘下一步’关联），
    或是knowledge的所有构成元素（有顺序）
    例如：我的衣服是我的
        我的衣服，构成了一个集合（所有衣服）
        我的，构成了一个集合（所有构成）
        前者属于后者，是后者的一个子集
    """

    def __init__(self, entity):
        """
        [运行时对象]所有集合操作的封装类。
        :param entity:realobject或knowledge
        """
        self.entity = entity
        self.type = OriginalType.UNKNOWN

        # 以下为运行时数据
        self.total_num = None  # 元素总数

    def getOriginalType(self):
        """
        取得集合的原始类型。realobject或knowledge
        :return:
        """
        if self.entity is None:
            return OriginalType.UNKNOWN
        if not self.type == OriginalType.UNKNOWN:
            return self.type

        from loongtian.nvwa.models.realObject import RealObject
        if isinstance(self.entity, RealObject):
            self.type = OriginalType.REALOBJECT
            return self.type

        from loongtian.nvwa.models.knowledge import Knowledge
        if isinstance(self.entity, Knowledge):
            self.type = OriginalType.KNOWLEDGE
            return self.type

        raise Exception("集合的原始类型既不是realobject，也不是knowledge，数据类型错误！")

    @staticmethod
    def checkOriginalType(target_type, obj):
        """
        判断集合的原始类型是否正确。realobject或knowledge
        :return:
        """
        if target_type == OriginalType.REALOBJECT:
            from loongtian.nvwa.models.realObject import RealObject
            if obj is None or not isinstance(obj, RealObject):
                raise Exception("参数错误，当前参数应为实际对象！")
        elif target_type == OriginalType.KNOWLEDGE:
            from loongtian.nvwa.models.knowledge import Knowledge
            if obj is None or not isinstance(obj, Knowledge):
                raise Exception("参数错误，当前参数应为知识链！")
        else:
            raise Exception("参数错误，当前参数应为实际对象或知识链！")

    def isDefinedAsCollection(self):
        """
        当前集合的原始类型是否明确定义为集合。
        :return:
        """
        if self.getOriginalType == OriginalType.UNKNOWN:
            return False
        elif self.getOriginalType == OriginalType.REALOBJECT:
            return Collection.isRealObjectDefinedAsCollection(self.entity)
        elif self.getOriginalType == OriginalType.KNOWLEDGE:
            return Collection.isKnowledgeDefinedAsCollection(self.entity)

    @staticmethod
    def isRealObjectDefinedAsCollection(real):
        """
        判断一个实际对象是否明确定义为集合（如果没有元素，也可以当成一个空集合）。
        :return: 是否集合,集合元素（可能一个或多个）。实际上，任何实际对象都快可以看成是一个集合
        """
        Collection.checkOriginalType(OriginalType.REALOBJECT, real)
        from loongtian.nvwa.runtime.instinct import Instincts
        if real.isChild(Instincts.instinct_original_collection):
            return True
        return False

    @staticmethod
    def isKnowledgeDefinedAsCollection(know):
        """
        判断知识链是否明确定义为集合（首先是realobject，然后real的父对象包括集合）。
        :param know: 知识链
        :return:
        """
        Collection.checkOriginalType(OriginalType.KNOWLEDGE, know)
        isReal, realObj = know.isSelfRealObject()
        if isReal:
            if Collection.isRealObjectDefinedAsCollection(realObj):
                return True

        return False

    def defineAsCollection(self):
        """
        将当前集合的原始类型明确定义为集合。
        :return:
        """
        if self.getOriginalType == OriginalType.UNKNOWN:
            return False
        elif self.getOriginalType == OriginalType.REALOBJECT:
            return Collection.defineRealObjectAsCollection(self.entity)
        elif self.getOriginalType == OriginalType.KNOWLEDGE:
            return Collection.defineKnowledgeAsCollection(self.entity)

    @staticmethod
    def defineRealObjectAsCollection(real):
        """
        将实际对象明确定义为集合。
        :param real: 实际对象
        :return:
        """
        Collection.checkOriginalType(OriginalType.REALOBJECT, real)
        if Collection.isRealObjectDefinedAsCollection(real):
            return True
        from loongtian.nvwa.runtime.instinct import Instincts
        return real.Constitutions.addParent(Instincts.instinct_original_collection)

    @staticmethod
    def defineKnowledgeAsCollection(know):
        """
        将知识链明确定义为集合。
        :param know: 知识链
        :return:
        """
        Collection.checkOriginalType(OriginalType.KNOWLEDGE, know)
        # 查找已有关联的实际对象
        isReal, realObj = know.isSelfRealObject()
        if not isReal:  # 如果没有关联，创建之
            realObj = know.toCollectionRealObject()
        if not realObj:
            raise Exception("知识链没有已关联的实际对象！系统错误！")

        return Collection.defineRealObjectAsCollection(realObj)

    @staticmethod
    def createRealObjectAsCollection(components,memory=None):
        """
        根据元素列表，创建collection（实际对象）
        :param components:
        :return:
        """
        from loongtian.nvwa.models.knowledge import Knowledge
        klg = Knowledge.getKnowledgeByObjectChain(components,memory=memory)
        if not klg:
            klg = Knowledge.createKnowledgeByObjChain(components,memory=memory)
        return klg.toCollectionRealObject()

    @staticmethod
    def createKnowledgeAsCollection(components,recordInDB=False,memory=None):
        """
        根据元素列表，创建collection（实际对象）
        :param components:
        :return:
        """
        from loongtian.nvwa.models.knowledge import Knowledge
        klg = Knowledge.getKnowledgeByObjectChain(components,memory=memory)
        if not klg:
            klg = Knowledge.createKnowledgeByObjChain(components,recordInDB=recordInDB,memory=memory)

        klg.toCollectionRealObject(recordInDB=recordInDB)
        return klg


    def isOrdered(self):
        """
        是否是有序集合。
        :return:
        """
        if self.getOriginalType == OriginalType.UNKNOWN:
            return False
        elif self.getOriginalType == OriginalType.REALOBJECT:
            return Collection.isRealObjectAllComponentsOrdered(self.entity)
        elif self.getOriginalType == OriginalType.KNOWLEDGE:  # 知识链天生就是有序集合
            return True

    @staticmethod
    def isRealObjectAllComponentsOrdered(real):
        """
        判断实际对象的所有组件是否是有序。
        :param real:
        :return:
        """
        Collection.checkOriginalType(OriginalType.REALOBJECT, real)
        sequence_components = real.Constitutions.getSequenceComponents()
        return not sequence_components is None

    def isEnumerated(self):
        """
        是否已经枚举出全部（有限个数，不包含省略元素…）
        :return:
        """
        elements, ks = self.getAllComponents()
        from loongtian.nvwa.runtime.instinct import Instincts
        for element in elements:
            if element.obj.id == Instincts.instinct_original_ellipsis:
                return False

        return True

    def isFinite(self):
        """
        是否是有限集合（查看最后一个组件是否是省略号）。
        :return:
        """
        elements, ks = self.getAllComponents()
        from loongtian.nvwa.runtime.instinct import Instincts
        if elements[-1].obj.id == Instincts.instinct_original_ellipsis:
            return False

        return True

    def isEmpty(self):
        """
        判断一个对象是否是空集合
        :return:
        """
        num = self.count()
        if num is None or num == 0:
            return True
        return False

    def getAllComponents(self):
        """
        取得集合的所有元素。
        :return: elements（元素列表，realobject或knowledge）, ks(关联的知识链列表)
        """
        if self.getOriginalType == OriginalType.UNKNOWN:
            return None, None
        elif self.getOriginalType == OriginalType.REALOBJECT:
            return Collection.getRealObjectAllComponents(self.entity)
        elif self.getOriginalType == OriginalType.KNOWLEDGE:
            return Collection.defineKnowledgeAsCollection(self.entity)

    @staticmethod
    def getRealObjectAllComponents(real):
        """
        取得实际对象（作为集合）的所有元素（组件）。
        :param real: 实际对象（作为集合）
        :return: elements, ks(关联的知识链列表)
        """
        Collection.checkOriginalType(OriginalType.REALOBJECT, real)
        elements, ks = real.getSelfComponentObjects()
        if elements is None or len(elements) < 1:
            return None, None
        return elements, ks

    @staticmethod
    def getKnowledgeAllComponents(know):
        """
        取得知识链（作为集合）的所有元素（组件）。
        :param know: 知识链（作为集合）
        :return: elements, ks(关联的知识链列表)
        """
        Collection.checkOriginalType(OriginalType.KNOWLEDGE, know)
        return know.getSequenceComponents(keepEndKnowledge=True), know

    def getAllComponentsFuzzySet(self):
        """
        取得集合的所有元素、关联值(模糊集合)。
        :return:[(元素、关联值)]（realobject或knowledge）
        """
        elements, ks = self.getAllComponents()
        if elements is None:
            return None
        fuzzy_set = []
        i = 0
        for element in elements:
            fuzzy_set.append((element, ks[i].weight))
            i += 1

        return fuzzy_set

    def count(self):
        """
        计数。（如果无限集合，返回无限符号∞）
        :return:
        """
        if not self.total_num is None:  # 如果已经数过了，直接返回结果
            return self.total_num

        elements, ks = self.getAllComponents()
        if elements is None:
            return 0

        self.total_num = 0
        for element in elements:
            # 过滤掉None
            if element.obj.isNone():
                continue
            self.total_num += 1
        return self.total_num

    def getByPosition(self, pos):
        """
        根据位置取得对应的元素（有序集合）
        :param pos:
        :return:
        """
        elements, ks = self.getAllComponents()
        if elements is None:
            return None
        if pos >= 0 and pos < len(elements):
            return elements[pos]
        return None

    def getPosition(self, element):
        """
        取得元素的位置（第一个，有序集合）
        :param element:realobject或knowledge
        :return:int
        """
        elements, ks = self.getAllComponents()
        if elements is None:
            return -1

        i = 0
        for t_element in elements:
            if t_element.obj.id == element.id:
                return i
            i += 1
        return -1

    def getAllPositions(self, element):
        """
        取得元素的所有位置（有序集合）
        :param element:realobject或knowledge
        :return:[int]
        """
        elements, ks = self.getAllComponents()
        if elements is None:
            return -1
        poss = []
        i = 0
        for t_element in elements:
            if t_element.obj.id == element.id:
                poss.append(i)
            i += 1
        return poss

    def getNext(self, element):
        """
        取得当前元素的下一个元素（有序集合）
        :param element: realobject或knowledge
        :return:
        """
        elements, ks = self.getAllComponents()
        if elements is None:
            return None
        i = 0
        elements = []
        for t_element in elements:
            if t_element.obj.id == element.id:
                try:
                    return elements[i + 1]
                except:
                    return None
            i += 1
        return None

    def getBefore(self, element):
        """
        取得当前元素的上一个元素（有序集合）
        :param element: realobject或knowledge
        :return:
        """
        elements, ks = self.getAllComponents()
        if elements is None:
            return None
        i = 0
        for t_element in elements:
            if t_element.obj.id == element.id:
                if i == 0:
                    return None
                try:
                    return elements[i - 1]
                except:
                    return None
            i += 1
        return None

    def insert(self, element, pos, insert_self_entity=True):
        """
        根据位置添加对应的元素（有序集合）
        :param element:
        :param pos:
        :param insert_self_entity:是否添加到自身的相关实体（实际对象添加到自身知识链，知识链添加到自身实际对象）
        :return:
        """
        if self.getOriginalType == OriginalType.UNKNOWN:
            return False, None
        elif self.getOriginalType == OriginalType.REALOBJECT:
            if insert_self_entity:
                # 将元素添加实际对象的对应知识链末尾（如果有的话）
                _is_self_know, self_know = self.entity.isSelfKnowledge()
                if _is_self_know:
                    self_know.Collection.insert(element, pos, insert_self_entity=False)

            return Collection.insertRealObjectComponent(self.entity, element, pos)

        elif self.getOriginalType == OriginalType.KNOWLEDGE:
            if insert_self_entity:
                # 将元素添加知识链的对应实际对象组件末尾（如果有的话）
                _is_self_real, self_real = self.entity.isSelfRealObject()
                if _is_self_real:
                    self_real.Collection.insert(element, pos, insert_self_entity=False)
            return Collection.insertKnowledgeComponent(self.entity, element, pos)

    @staticmethod
    def insertRealObjectComponent(real, element, pos):
        """
        根据位置添加对应的元素到实际对象的组件列表（有序集合）
        :param real:
        :param element:
        :param pos:
        :return:
        """

    @staticmethod
    def insertKnowledgeComponent(know, element, pos):
        """
        根据位置添加对应的元素到实际对象的组件列表（有序集合）
        :param know:知识链
        :param element:要插入的元素
        :param pos:指定位置
        :return:
        """
        # [a,b,c]:
        # k0    a     b
        # k1    k0    c
        # 先在某个位置插入d，形成
        # 1、位置0 [d,a,b,c]：
        # k0    k2     b
        # k1    k0    c
        # k2    d    a
        # 2、位置1 [a,d,b,c]：
        # k0    k2     b
        # k1    k0    c
        # k2    a    d
        # 3、位置2 [a,b,d,c]：
        # k0     a    b
        # k1    k2    c
        # k2    k0    d
        # 4、位置2 [a,b,c,d]：
        # k0     a    b
        # k1    k0    c
        # k2    k1    d
        if not isinstance(pos,int) or pos<0:
            raise Exception("指定的插入位置必须是整数，并且大于等于0！")
        from loongtian.nvwa.models.realObject import RealObject
        from loongtian.nvwa.models.knowledge import Knowledge
        if element is None or not isinstance(element,RealObject) or not isinstance(element,Knowledge):
            raise Exception("要插入元素必须是实际对象或知识链！")
        if pos == 0:
            pass


    def append(self, element, insert_self_entity=True):
        """
        将元素添加到集合的末尾（有序集合）
        :param element:
        :param insert_self_entity:是否添加到自身的相关实体（实际对象添加到自身知识链，知识链添加到自身实际对象）
        :return:
        """
        if not element:
            return False, None, None  # 未添加组件元素，当然没有顺序组件集合
        if self.getOriginalType == OriginalType.UNKNOWN:
            return False, None
        elif self.getOriginalType == OriginalType.REALOBJECT:
            if insert_self_entity:
                # 将元素添加实际对象的对应知识链末尾（如果有的话）
                _is_self_know, self_know = self.entity.isSelfKnowledge()
                if _is_self_know:
                    self_know.Collection.append(element,insert_self_entity = False)

            return Collection.appendRealObjectComponent(self.entity, element)

        elif self.getOriginalType == OriginalType.KNOWLEDGE:
            if insert_self_entity:
                # 将元素添加知识链的对应实际对象组件末尾（如果有的话）
                _is_self_real, self_real = self.entity.isSelfRealObject()
                if _is_self_real:
                    self_real.Collection.append(element,insert_self_entity = False)
            return Collection.appendKnowledgeComponent(self.entity, element)

    @staticmethod
    def appendRealObjectComponent(real, obj):
        """
        将对象添加到实际对象组件及其组件知识链列表的末尾（有序集合）
        :param real:
        :param obj:
        :return:是否成功,组件对象知识链,组件对象知识链顺序知识链
        """
        if not obj:
            return False, None, None  # 未添加组件元素，当然没有顺序组件集合
        Collection.checkOriginalType(OriginalType.REALOBJECT, real)

        sequence_components = real.Constitutions.getSequenceComponents()
        sequence_klg = None
        if sequence_components:  # 如果已经有了一个顺序组件集合，特殊处理
            component_klg = real.Constitutions.addComponent(obj)
            sequence_klg = real._sequence_components_sequence_klg
            if sequence_klg:
                sequence_klg.Collection.append(component_klg)
            else:
                raise Exception("实际对象的顺序组件集合错误！有sequence_components但无sequence_components_sequence_klg！")
        else:  # 没有顺序组件集合，直接添加
            component_klg = real.Constitutions.addComponent(obj)

        if sequence_klg:
            return True, component_klg, sequence_klg  # 添加了组件元素，并形成顺序组件集合（有顺序）
        else:
            return True, component_klg, None  # 虽然添加了组件元素，但没有形成顺序组件集合（没有顺序）

    @staticmethod
    def appendKnowledgeComponent(know, obj):
        """
        将对象添加到知识链的末尾
        :param know:
        :param obj:
        :return:
        """
        if not obj:
            return False, None, None  # 未添加组件元素，当然没有顺序组件集合
        Collection.checkOriginalType(OriginalType.KNOWLEDGE, know)

        from loongtian.nvwa.models.knowledge import Knowledge
        new_klg = Knowledge.createKnowledgeByStartEnd(know, obj,memory=know.Memory)
        return not new_klg is None, new_klg

    def extend(self, *elements):
        """
        将列表元素逐一添加到集合（默认添加顺序）。
        :param ordered: 是否添加顺序
        :param elements: 集合元素列表（实际对象）或eid（rid）列表
        :return:
        """
        if not elements:
            return False

        for e in elements:
            self.append(e)

        return True

    def replace(self, element, pos):
        """
        根据位置替换对应的元素（有序集合）
        :param pos:
        :return:
        """

    def delete(self, pos):
        """
        根据位置删除对应的元素（有序集合）
        :param pos:
        :return:
        """

    def remove(self):
        """
        将集合的末尾元素删除（有序集合）
        :return:
        """

    def cut(self, pos):
        """
        根据位置将集合一分为二（有序集合）
        :param pos:
        :return:
        """

    def slice(self, start, end):
        """
        根据开始、结束位置取得集合的切片（有序集合）。
        :param start:
        :param end:
        :return:
        """

    def slices(self, *positions):
        """
        根据位置列表取得多重切片（有序集合）。
        :param positions:
        :return:
        """

    def differed_with(self,obj):
        """
        取当前对象与另一个实际对象/知识链的差集
        :param obj:
        :return:
        """
        return Collection.difference(self.entity,obj)

    def intersected_with(self,obj):
        """
        取当前对象与另一个实际对象/知识链的交集
        :param obj:
        :return:
        """
        return Collection.intersection(self.entity, obj)

    def unioned_with(self,obj):
        """
        取当前对象与另一个实际对象/知识链的并集
        :param obj:
        :return:
        """
        return Collection.union(self.entity, obj)

    @staticmethod
    def changeListComponentToKnowledge(components):
        """
        将组件中的list转化成Knowledge
        :param components:
        :return:
        """
        result = []
        for component in components:
            if isinstance(component, list):
                from loongtian.nvwa.models.knowledge import Knowledge
                component = Knowledge.createKnowledgeByObjChain(component)
            result.append(component)
        return result

    @staticmethod
    def isPlainRealChain(reals):
        """
        判断输入是否是单纯由实际对象组成的列表
        :param reals:
        :return:
        """
        if not isinstance(reals, list) and not isinstance(reals, tuple):
            return False
        for real in reals:
            if isinstance(real, list) or isinstance(real, tuple):
                return False
        return True

    @staticmethod
    def difference(obj1, obj2):
        """
        求两个实际对象/知识链的差集
        :param obj1:
        :param obj2:
        :return:
        """
        from loongtian.nvwa.models.realObject import RealObject
        from loongtian.nvwa.models.knowledge import Knowledge

        if obj1 is None:
            if obj2 is None:
                return []
            elif isinstance(obj2, RealObject) or isinstance(obj2, Knowledge):
                return obj2.getSequenceComponents()
            elif isinstance(obj2,list):
                return obj2
            else:
                raise Exception("obj2必须为实际对象或知识链或list！")
        elif not isinstance(obj1, RealObject) and not isinstance(obj1, Knowledge) and not isinstance(obj1, list):
            raise Exception("obj1必须为实际对象或知识链或list！")
        else:
            if obj2 is None:
                if isinstance(obj1, RealObject) or isinstance(obj1, Knowledge):
                    return obj1.getSequenceComponents()
                else: # 肯定是list
                    return obj1

        if not isinstance(obj2, RealObject) and not isinstance(obj2, Knowledge) and not isinstance(obj2, list):
            raise Exception("obj2必须为实际对象或知识链或list！")

        try:
            if isinstance(obj1, RealObject) or isinstance(obj1, Knowledge):
                obj1_components = obj1.getSequenceComponents()
            else:
                obj1_components = obj1
            if isinstance(obj2, RealObject) or isinstance(obj2, Knowledge):
                obj2_components = obj2.getSequenceComponents()
            else:
                obj2_components = obj2

            obj1_components=Collection.changeListComponentToKnowledge(obj1_components)
            obj2_components = Collection.changeListComponentToKnowledge(obj2_components)

            set1 = set(obj1_components)
            set2 = set(obj2_components)
            return set1 - set2
        except Exception as ex:
            raise Exception("求两个实际对象/知识链的差集错误！%s" % ex)

    @staticmethod
    def intersection(obj1, obj2):
        """
        求两个实际对象/知识链的交集
        :param obj1:
        :param obj2:
        :return:
        """
        # todo 参照difference
        if obj1 is None or obj2 is None:
            return []
        from loongtian.nvwa.models.realObject import RealObject
        from loongtian.nvwa.models.knowledge import Knowledge
        if not isinstance(obj1,RealObject) or not isinstance(obj1,Knowledge):
            raise Exception("obj1必须为实际对象或知识链！")
        if not isinstance(obj2,RealObject) or not isinstance(obj2,Knowledge):
            raise Exception("obj2必须为实际对象或知识链！")

        try:
            obj1_components=obj1.getSequenceComponents()
            obj2_components = obj2.getSequenceComponents()

            set1 = set(obj1_components)
            set2 = set(obj2_components)
            return set1 & set2
        except Exception as ex:
            raise ex

    @staticmethod
    def union(obj1, obj2):
        """
        求两个实际对象/知识链的并集
        :param obj1:
        :param obj2:
        :return:
        """
        # todo 参照difference
        from loongtian.nvwa.models.realObject import RealObject
        from loongtian.nvwa.models.knowledge import Knowledge

        if obj1 is None:
            if obj2 is None:
                return []
            elif isinstance(obj2, RealObject) or isinstance(obj2, Knowledge):
                return obj2.getSequenceComponents()
            else:
                raise Exception("obj2必须为实际对象或知识链！")
        elif not isinstance(obj1, RealObject) and not isinstance(obj1, Knowledge):
            raise Exception("obj1必须为实际对象或知识链！")
        else:
            if obj2 is None:
                return obj1.getSequenceComponents()


        if not isinstance(obj2, RealObject) and not isinstance(obj2, Knowledge):
            raise Exception("obj2必须为实际对象或知识链！")

        try:
            obj1_components = obj1.getSequenceComponents()
            obj2_components = obj2.getSequenceComponents()

            set1 = set(obj1_components)
            set2 = set(obj2_components)
            return set1 | set2
        except Exception as ex:
            raise ex


