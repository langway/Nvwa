#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    pyplot_test 
Author:   Liuyl 
DateTime: 2014/9/11 8:57 
UpdateLog:
1、Liuyl 2014/9/11 Create this File.

pyplot_test
>>> print("No Test")
No Test
"""
__author__ = 'Liuyl'
import networkx as nx
import matplotlib
matplotlib.use('Qt4Agg')
import matplotlib.pyplot as plt



def draw_knowledge(figure_id):
    print('before graph')
    plt.figure(figure_id)
    _g = nx.Graph()
    print('before plot')
    seed = figure_id * 3
    _g.add_nodes_from([seed + 1, seed + 2, seed + 3])
    _g.add_edge(seed + 1, seed + 2)
    pos = nx.random_layout(_g)
    print('before draw')
    nx.draw(_g, pos, with_labels=True, node_size=200)
    print('before show')
    plt.draw()

if __name__ == '__main__':
    for i in range(5):
        draw_knowledge(1)

    plt.show()