#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    sort 
Author:   Liuyl 
DateTime: 2015/1/5 9:28 
UpdateLog:
1、Liuyl 2015/1/5 Create this File.

sort
>>> print("No Test")
No Test
"""
__author__ = 'Liuyl'
threshold_wight = 1
distance_wight = 10
threshold_distance_function = lambda threshold, distance: threshold * threshold_wight + distance * distance_wight


def threshold_sort(x, y):
    return cmp(x.Threshold, y.Threshold)


def threshold_distance_sort(x, y):
    return cmp(threshold_distance_function(x[0].Threshold, x[1]), threshold_distance_function(y[0].Threshold, y[1]))


if __name__ == '__main__':
    import doctest

    doctest.testmod()