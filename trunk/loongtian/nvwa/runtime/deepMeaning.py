# /usr/bin/python
# coding: utf-8
__author__ = 'Leon'

from treelib import Tree
from loongtian.nvwa.models.baseEntity import BaseEntity
from loongtian.nvwa.runtime.relatedObjects import RelatedObj


class DeepMeaning(Tree):
    """
    深度语义网的包装类
    """
    #
    # def __init__(self):
    #     """
    #
    #     """

    def add_node(self,obj,parent=None):
        """
        添加根节点
        :param obj:
        :return:
        """
        if not isinstance(obj,BaseEntity) or not isinstance(obj,RelatedObj):
            raise Exception("深度语义网的根节点必须是BaseEntity/RelatedObjs及其子类！")
        if isinstance(parent,BaseEntity) or not isinstance(obj,RelatedObj):
            parent=parent.id



        return self.create_node(tag=obj.id,parent=parent,identifier=obj.id,data=obj)






