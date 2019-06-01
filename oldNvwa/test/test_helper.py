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
import matplotlib

#matplotlib.use('Qt4Agg')
import matplotlib.pyplot as plt


def draw_knowledge():
    _g = nx.Graph()
    seed = 1
    _g.add_nodes_from([seed + 1, seed + 2, seed + 3])
    _g.add_edge(seed + 1, seed + 2)
    pos = nx.spectral_layout(_g)
    nx.draw(_g, pos, with_labels=True, node_size=200)
    plt.show()


if __name__ == '__main__':
    draw_knowledge()