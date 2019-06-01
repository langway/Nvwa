#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    complex_network_du 
Author:   fengyh 
DateTime: 2014/8/22 10:06 
UpdateLog:
1、fengyh 2014/8/22 Create this File.


"""


"""
一、度、度分布

NetworkX可以用来统计图中每个节点的度，并生成度分布序列。
度分布是图论和网络理论中的概念。一个图（或网络）由一些顶点（节点）和连接它们的边（连结）构成。
每个顶点（节点）连出的所有边（连结）的数量就是这个顶点（节点）的度。
度分布是对一个图（网络）中顶点（节点）度数的总体描述。对于随机图，度分布指的是图中顶点度数的概率分布。
"""

import networkx as nx
G = nx.random_graphs.barabasi_albert_graph(10,3)   #生成一个n=1000，m=3的BA无标度网络
print G.degree(0)                                   #返回某个节点的度
print G.degree()                                     #返回所有节点的度
print nx.degree_histogram(G)    #返回图中所有节点的度分布序列（从1至最大度的出现频次） 索引是度，值是频次。

"""
对上述结果稍作处理，可以用matplotlib直接作图，输入：
"""
import matplotlib.pyplot as plt                 #导入科学绘图的matplotlib包
degree = nx.degree_histogram(G)          #返回图中所有节点的度分布序列
x = range(len(degree))                             #生成x轴序列，从1到最大度
y = [z / float(sum(degree)) for z in degree]
#将频次转换为频率，这用到Python的一个小技巧：列表内涵，Python的确很方便：）
plt.loglog(x,y,color="blue",linewidth=2)           #在双对数坐标轴上绘制度分布曲线
plt.show()                                       #显示图表                                                       #显示图表

"""
二、群聚系数

这个在NetworkX里实现起来很简单，只需要调用方法nx.average_clustering(G) 就可以完成平均群聚系数的计算，而调用nx.clustering(G) 则可以计算各个节点的群聚系数。

三、直径和平均距离

nx.diameter(G)返回图G的直径（最长最短路径的长度），而nx.average_shortest_path_length(G)则返回图G所有节点间平均最短路径长度。

四、匹配性

这个也比较简单，调用 nx.degree_assortativity(G) 方法可以计算一个图的度匹配性。

五、中心性

这个我大部分不知道怎么翻译，直接上NX的帮助文档吧，需要计算哪方面的centrality自己从里边找：）

Degree centrality measures.（点度中心性？）
degree_centrality(G)     Compute the degree centrality for nodes.
in_degree_centrality(G)     Compute the in-degree centrality for nodes.
out_degree_centrality(G)     Compute the out-degree centrality for nodes.

Closeness centrality measures.（紧密中心性？）
closeness_centrality(G[, v, weighted_edges])     Compute closeness centrality for nodes.

Betweenness centrality measures.（介数中心性？）
betweenness_centrality(G[, normalized, ...])     Compute betweenness centrality for nodes.
edge_betweenness_centrality(G[, normalized, ...])     Compute betweenness centrality for edges.

Current-flow closeness centrality measures.（流紧密中心性？）
current_flow_closeness_centrality(G[, ...])     Compute current-flow closeness centrality for nodes.
Current-Flow Betweenness

Current-flow betweenness centrality measures.（流介数中心性？）
current_flow_betweenness_centrality(G[, ...])     Compute current-flow betweenness centrality for nodes.
edge_current_flow_betweenness_centrality(G)     Compute current-flow betweenness centrality for edges.

Eigenvector centrality.（特征向量中心性？）
eigenvector_centrality(G[, max_iter, tol, ...])     Compute the eigenvector centrality for the graph G.
eigenvector_centrality_numpy(G)     Compute the eigenvector centrality for the graph G.

Load centrality.（彻底晕菜~~~）
load_centrality(G[, v, cutoff, normalized, ...])     Compute load centrality for nodes.
edge_load(G[, nodes, cutoff])     Compute edge load.
"""

"""
复杂网络分析库NetworkX学习笔记（3）：网络演化模型

一、规则图

规则图差不多是最没有复杂性的一类图了，在NetworkX中，用random_graphs.random_regular_graph(d, n)方法可以生成一个含有n个节点，
每个节点有d个邻居节点的规则图。下面是一段示例代码，生成了包含20个节点、每个节点有3个邻居的规则图：
"""
import networkx as nx
import matplotlib.pyplot as plt
RG = nx.random_graphs.random_regular_graph(3,20)  #生成包含20个节点、每个节点有3个邻居的规则图RG
pos = nx.spectral_layout(RG)          #定义一个布局，此处采用了spectral布局方式，后变还会介绍其它布局方式，注意图形上的区别
nx.draw(RG,pos,with_labels=False,node_size = 30)  #绘制规则图的图形，with_labels决定节点是非带标签（编号），node_size是节点的直径
plt.show()  #显示图形

"""
二、ER随机图

ER随机图是早期研究得比较多的一类“复杂”网络，这个模型的基本思想是以概率p连接N个节点中的每一对节点。
在NetworkX中，可以用random_graphs.erdos_renyi_graph(n,p)方法生成一个含有n个节点、以概率p连接的ER随机图：
"""
import networkx as nx
import matplotlib.pyplot as plt
ER = nx.random_graphs.erdos_renyi_graph(20,0.2)  #生成包含20个节点、以概率0.2连接的随机图
pos = nx.shell_layout(ER)          #定义一个布局，此处采用了shell布局方式
nx.draw(ER,pos,with_labels=False,node_size = 30)
plt.show()

"""
三、WS小世界网络

在NetworkX中，可以用random_graphs.watts_strogatz_graph(n, k, p)方法生成一个含有n个节点、每个节点有k个邻居、以概率p随机化重连边的WS小世界网络，下面是一个例子：
"""

import networkx as nx
import matplotlib.pyplot as plt
WS = nx.random_graphs.watts_strogatz_graph(20,4,0.3)  #生成包含20个节点、每个节点4个近邻、随机化重连概率为0.3的小世界网络
pos = nx.circular_layout(WS)          #定义一个布局，此处采用了circular布局方式
nx.draw(WS,pos,with_labels=False,node_size = 30)  #绘制图形
plt.show()

"""
四、BA无标度网络

在NetworkX中，可以用random_graphs.barabasi_albert_graph(n, m)方法生成一个含有n个节点、每次加入m条边的BA无标度网络，下面是一个例子：
"""
import networkx as nx
import matplotlib.pyplot as plt
BA= nx.random_graphs.barabasi_albert_graph(20,1)  #生成n=20、m=1的BA无标度网络
pos = nx.spring_layout(BA)          #定义一个布局，此处采用了spring布局方式
nx.draw(BA,pos,with_labels=False,node_size = 30)  #绘制图形
plt.show()