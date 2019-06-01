#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    graph 
Author:   Liuyl 
DateTime: 2014/9/10 9:53 
UpdateLog:
1、Liuyl 2014/9/10 Create this File.

graph
>>> print("No Test")
No Test
"""
__author__ = 'Liuyl'
import networkx as nx
# import matplotlib

# matplotlib.use('Qt4Agg')
import matplotlib.pyplot as plt
from loongtian.nvwa.common.storage.db.entity_repository import knowledge_rep
from loongtian.nvwa.core.gdef import OID


def draw_knowledge():
    class Nodes(object):
        def __init__(self):
            self.nodes = set()
            self.split_nodes = {}
            self.label = {}

        def add(self, node, split=False):
            _label = OID.get_name_by_id(node)
            if _label == '':
                _label = node
            if split:
                if node in self.split_nodes:
                    self.split_nodes[node] += 1
                else:
                    self.split_nodes[node] = 1
                _index = self.split_nodes[node]
                node = '{}-{}'.format(node, _index)
                self.label[node] = _label + str(_index)
            else:
                self.nodes.add(node)
                self.label[node] = _label  # + '\n' + node
            return node

        def get_list(self):
            _list = list(self.nodes)
            _list.extend(
                ['{}-{}'.format(_node[0], _i) for _node in self.split_nodes.items() for _i in range(1, _node[1] + 1)])
            return _list

    _object_keys = knowledge_rep.get_key_by_end('')
    _keys = knowledge_rep.get_keys()
    _nodes = Nodes()
    _edges = set()
    for _key in _keys:
        if _key not in _object_keys:
            _k = knowledge_rep.get(_key)
            if _k.Start in _object_keys and _k.End in _object_keys:
                _nodes.add(_k.Start)

                _next_list = knowledge_rep.get_by_start(_k.Id)
                _next_start = _nodes.add(_k.End, len(_next_list) != 0)
                _edges.add((_k.Start, _next_start))
                while len(_next_list) > 0:
                    _next_k = _next_list[0]
                    _next_list = knowledge_rep.get_by_start(_next_k.Id)
                    _end = _nodes.add(_next_k.End, len(_next_list) != 0)
                    _edges.add((_next_start, _end))
                    _next_start = _end
    _g = nx.DiGraph()
    _g.add_nodes_from(_nodes.get_list())
    _g.add_edges_from(_edges)
    _pos = nx.spring_layout(_g)
    nx.draw(_g, _pos, with_labels=False, node_size=200)
    nx.draw_networkx_labels(_g, _pos, _nodes.label, font_size=16)
    plt.show()

    def mark_node(nodes):
        pass


def init_to_memory():
    pass


if __name__ == '__main__':
    draw_knowledge()