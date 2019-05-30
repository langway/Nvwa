#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

import scipy as sp

data=sp.genfromtxt("web_traffic_data.tsv",delimiter="\t")# 第一个是数据路径名。第二个参数是分隔符，由于原文件中使用的制表符隔开数据的，所以这里是\t

print(data[:10])
print(data.shape)

x=data[:,0]# 取全部第一列数据
y=data[:,1]# 取全部第二列数据

# print(x)
# print(y)

nanY=sp.sum(sp.isnan(y))# 查询无效数据

print(nanY )

x=x[~sp.isnan(y)]# 去掉无效数据
y=y[~sp.isnan(y)]

print(x[:10])
print(y[:10])

import matplotlib.pyplot as plt

plt.scatter(x,y)

plt.title("Web traffic over last month")

plt.xlabel("Time")

plt.ylabel("Hints/hour")

plt.xticks([w*7*24 for w in range(10)],['week %i'%w for w in range(10)])

plt.autoscale(tight=True)

plt.grid()

fp1,residuals,rank,sv,rcond=sp.polyfit(x,y,1,full=True,)

f1=sp.poly1d(fp1)

fx=sp.linspace(0,x[-1],1000)

plt.plot(fx,f1(fx),linewidth=4)

plt.legend(["d=%i" %f1.order],loc="upper left")# 图例

plt.show()

input()




