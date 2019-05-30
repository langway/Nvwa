#!/usr/bin/env python
#coding=utf-8

"""
联想引擎。
"""
__author__ = 'Leon'

from loongtian.util.log.logger import  *
from loongtian.nvwa.engines.engineBase import EngineBase
from loongtian.nvwa.models.realObject import RealObject
from loongtian.nvwa.models.knowledge import Knowledge
from loongtian.nvwa.organs.character import Character

class AssociationEngine(EngineBase):
    """
    联想引擎。
    """

    def __init__(self,memory):
        """
        联想引擎。
        :param memory: 用来存放当前对象的内存空间（避免每次都从数据库中调用）
                       当前AssociationEngine的memory是MemoryCentral
        """
        super(AssociationEngine, self).__init__(memory)

    def associate(self,obj):
        """
        对一个实际对象（或实际对象列表，或知识链）进行联想
        :param obj:
        :return:
        """
        if not obj:
            return None
        associated_objs = []
        if isinstance(obj,list):
            for _obj in obj:
                child_associated_objs = self.associate(_obj)
                if child_associated_objs:
                    associated_objs.extend(child_associated_objs)
        elif isinstance(obj,RealObject):
            self._associateRealObject(obj,associated_objs)
        elif isinstance(obj,Knowledge):
            self._associateKnowledge(obj,associated_objs)
        else:
            raise Exception("无法进行联想的数据类型，必须是：实际对象（或实际对象列表，或知识链）")

        return associated_objs

    def _associateRealObject(self,real,associated_objs):
        """
        对一个实际对象进行联想
        :param real:
        :return:
        :remarks: 实际对象1-构成1-实际对象2-构成3...，联想深度取决于Character.Association.Depth
        """
        cur_depth = 0
        while cur_depth <= Character.Association.Real_Constituent_Depth:

            # todo 实际对象的联想
            cur_depth+=1

    def _associateKnowledge(self, know, associated_objs):
        """
        对一个知识链进行联想
        :param know:
        :return:
        """

        cur_depth = 0
        while cur_depth <= Character.Association.Knowledge_Search_Depth:

            # todo 知识链的联想

            cur_depth += 1

        # 继续对知识链中的每一个实际对象进行联想？(todo 需要进一步考量)
        components = know.getSequenceComponents()
        components_associated_objs =self.associate(components)
        associated_objs.extend(components_associated_objs)

