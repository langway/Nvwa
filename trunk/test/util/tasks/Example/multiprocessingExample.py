#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
多进程的例子。
"""
__author__ = 'Leon'

import os
import threading
import multiprocessing

# 简单的创建进程
def worker(num):
    """thread workmanager function"""
    print 'WorkManager:', num
    return

if __name__ == '__main__':
    jobs = []
    for i in range(5):
        p = multiprocessing.Process(target=worker, args=(i,))
        jobs.append(p)
        p.start()


#*****************************分割线**********************************
# import multiprocessing as mul
#
# def f(x):
#     return x**2
#
# pool = mul.Pool(5)
# rel  = pool.map(f,[1,2,3,4,5,6,7,8,9,10])
# print(rel)