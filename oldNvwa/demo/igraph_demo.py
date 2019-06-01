#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    igraph 
Author:   fengyh 
DateTime: 2014/8/22 11:04 
UpdateLog:
1、fengyh 2014/8/22 Create this File.


"""

import igraph

g = igraph.Graph(1)
print g
g.add_vertices(3)
g.add_edges([(0, 1), (1, 2)])
g.add_edges([(2, 0)])
g.add_vertices(3)
g.add_edges([(2, 3), (3, 4), (4, 5), (5, 3)])
print g
print g.get_eid(2, 3)

print igraph.summary(g)

print "test nvwa "
g = igraph.Graph()
g.add_vertex("牛")
g.add_vertex("有")
g.add_edge("牛", "有", name="牛有")
g.add_vertex("腿",fromid=[0])
g.add_vertex("角",fromid=[0])

g.add_vertex("马")
g.add_edge("马", "有", name="马有")

v1 = g.vs.find("腿")
v1_fromid = v1.attributes().get('fromid')
v1_fromid.append(1)

print v1_fromid

v1 = g.vs.find("腿")
v1_name = v1.attributes().get('name')
v1_fromid = v1.attributes().get('fromid')
print v1_fromid

for id in v1_fromid:
    e1 = g.es.find(id)
    e1_name = e1.attributes().get('name')
    print e1_name+v1_name

print g.vs.find(fromid=[0,1])