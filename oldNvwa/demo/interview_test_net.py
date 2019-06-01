#!/usr/bin/env python
# coding: utf-8
"""
假设一个节点关系网模型, 这个模型用任意两个节点及两个节点之间的关系所构建的网络来表示某一个领域内事物间的关系,
那么模型的基本结构为 NodeA--Relation--NodeB.
我们预定义一个Node集合和一个Relation集合,并假定这个集合所组成的网络能够完整表示某个领域的某一个方面:
    {NodeA,NodeB,NodeC,NodeD,NodeE}
    {Relation1,Relation2,Relation3}
    
这个模型在构建时有一些规则限制:
1.Relation两端的Node不能相同, 以下的规则2,3,4都需要满足此规则. 不再赘述.
2.Relation1两端出现的Node没有限制
3.Relation2右端只能是NodeA或NodeB中的一个,
4.Relation3右端只能是NodeD , 左端无限制, 但有附加规则为, 假如有NodeN ,当生成了NodeN--Relation--NodeD 时,
  同时应自动生成NodeN--Relation1--NodeE.

现在要编写一套接口来构建和检验这些基本结构, 我们初步的设计了一个方案, 你可以通过这个方案了解到这个接口需要实现的功能,
同时, 我们对这个方案并不满意, 你可以试着改进这个方案或者将其抛弃并设计一个你自己的方案, 我们非常期待你的精妙结构.

下面是我们设计的初步方案的python实现
如果你对python比较陌生, 我们确信下面的代码中所体现的逻辑和技巧在大多数流行语言中都能够找到对应
你可以将其改写成任意你所熟悉的语言并进行你的设计
"""
net = list()


class BaseModel(object):
    def __init__(self, left_node, relation, right_node):
        self.left_node = left_node
        self.relation = relation
        self.right_node = right_node

    def __eq__(self, other):
        return other.left_node == self.left_node and self.relation == other.relation and self.right_node == other.right_node

    def __str__(self):
        return u'{0}--{1}--{2}'.format(self.left_node, self.relation, self.right_node)


def world_set(left_node, relation, right_node):
    _model = BaseModel(left_node, relation, right_node)
    net.append(_model)
    print(u'生成: {0}'.format(_model))


def world_check(left_node, relation, right_node):
    _temp_model = BaseModel(left_node, relation, right_node)
    for _model in net:
        if _model == _temp_model:
            print(u'检查: {0} 成功!'.format(_model))
            return True
    print(u'检查: {0} 失败!'.format(_temp_model))
    return False


class BaseOperator(object):
    def __init__(self, obj):
        self._obj = obj

    def get(self):
        return self._obj
    

class RelationOperator(BaseOperator):
    def __init__(self, relation):
        super(RelationOperator, self).__init__(relation)
        self._obj = relation

    def set(self, left_node, right_node):
        if left_node == right_node:
            raise Exception(u'违反规则1')
        world_set(left_node, self.get(), right_node)

    def check(self, left_node, right_node):
        return world_check(left_node, self.get(), right_node)


class RelationToNodeOperator(BaseOperator):
    def __init__(self, right_node, relation_op):
        super(RelationToNodeOperator, self).__init__(right_node)
        self.relation_op = relation_op

    def set(self, left_node):
        return self.relation_op.set(left_node, self.get())

    def check(self, left_node):
        return self.relation_op.check(left_node, self.get())


class Relation2Operator(RelationOperator):
    def __init__(self):
        super(Relation2Operator, self).__init__(u'Relation2')
        self.NodeA = RelationToNodeOperator(u'NodeA', self)
        self.NodeB = RelationToNodeOperator(u'NodeB', self)

    def set(self, left_node, right_node):
        if right_node == u'NodeA' or right_node == u'NodeB':
            super(Relation2Operator, self).set(left_node, right_node)
        else:
            raise Exception(u'违反规则3')


class Relation3ToNodeDOperator(RelationToNodeOperator):
    def __init__(self, relation_op):
        super(Relation3ToNodeDOperator, self).__init__(u'NodeD', relation_op)

    def set(self, left_node):
        super(Relation3ToNodeDOperator, self).set(left_node)
        # 满足规则4的附加规则
        world_set(left_node, u'Relation1', u'NodeE')


class Relation3Operator(RelationOperator):
    def __init__(self):
        super(Relation3Operator, self).__init__(u'Relation3')
        self.NodeD = Relation3ToNodeDOperator(self)

    def set(self, left_node, right_node):
        if right_node == u'NodeD':
            super(Relation3Operator, self).set(left_node, right_node)
        else:
            raise Exception(u'违反规则4')


class TestService(object):
    def __init__(self):
        self.Relation1 = RelationOperator(u'Relation1')
        self.Relation2 = Relation2Operator()
        self.Relation3 = Relation3Operator()


if __name__ == '__main__':
    _srv = TestService()
    _srv.Relation1.set(u'NodeA', u'NodeB')
    _srv.Relation2.NodeA.set(u'NodeC')
    try:
        _srv.Relation2.NodeB.set(u'NodeB')
    except Exception, e:
        print(e.message)
    try:
        _srv.Relation2.set(u'NodeC', u'NodeD')
    except Exception, e:
        print(e.message)
    _srv.Relation3.NodeD.set(u'NodeC')
    _srv.Relation1.check(u'NodeC', u'NodeE')

    """
    (输出)
    生成: NodeA--Relation1--NodeB
    生成: NodeC--Relation2--NodeA
    违反规则1
    违反规则3
    生成: NodeC--Relation3--NodeD
    生成: NodeC--Relation1--NodeE
    检查: NodeC--Relation1--NodeE 成功!
    """