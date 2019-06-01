#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    adjust.py 
Created by zheng on 2014/11/17.
UpdateLog:
1、fengyh 201501014 增加阈值衰减方法
"""

import math
import datetime

# from loongtian.nvwa.entities.entity import RealObject, Knowledge
# from loongtian.nvwa.service import real_object_srv, knowledge_srv


def decrease(threshold, rate):
    '''
    阈值低，上升的快

    :param threshold:阈值
    :param rate:比例。
    :return:调整后的阈值
    '''
    if threshold == 100:
        return threshold
    a, b, c = 1, 100, 10
    _r = 1 - a * math.e ** (c / float(threshold - b))
    ret = threshold - a * rate * _r
    if ret < 0:
        return 0
    return ret

def testDecrease():
    for i in range(0, 10):
        print "%f ==> %s" % (i*0.1, decrease(i*0.1, 1))


def increase(threshold):
    '''
    遗忘，阈值很高或很低时，阈值下降的都很慢
    :param threshold:阈值
    :return:调整后的阈值
    '''
    a, b, c = 1, 50, 25
    rate = 0.1
    _r = a * math.e ** (-(threshold - b) ** 2 / c ** 2)
    _new = threshold + threshold * rate * _r
    if _new > 100:
        _new = 100
    return _new

def testIncrease():
    for i in range(0, 10):
        print "%f ==> %s" % (i*0.1, increase(i*0.1))


def draw_increase():
    import numpy as np
    import matplotlib.pyplot as plt

    x = np.linspace(0, 100, 1000)
    a, b, c = 1, 50, 25
    y = a * math.e ** (-(x - b) ** 2 / c ** 2)
    plt.figure(figsize=(8, 5))
    plt.plot(x, y, color="red", linewidth=2)
    plt.xlabel("threshold")
    plt.ylabel("Volt")
    plt.title("damping")
    plt.ylim(0, 1)
    plt.legend()
    plt.show()


def draw_decrease():
    import numpy as np
    import matplotlib.pyplot as plt

    x = np.linspace(0, 100, 100)
    a, b, c = 1, 100, 10
    y = 1 - a * math.e ** (c / (x - b))
    plt.figure(figsize=(8, 5))
    plt.plot(x, y, color="red", linewidth=2)
    plt.xlabel("threshold")
    plt.ylabel("Volt")
    plt.title("increase")
    plt.ylim(0, 1)
    plt.legend()
    plt.show()


if __name__ == '__main__':
    # print "decrease:"
    # testDecrease()
    # print "increase:"
    # testIncrease()
    # print "Me:"
    a = 0.125 #系数
    k = 100 # 放大倍数
    v = 0.568 # 系数
    for i in range(0, 100):
        x = i+1
        new = round(k*x**-a-(x-1)*v, 2)
        print "%d ==> %f" % (x, new)