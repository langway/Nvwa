#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
基础层。
  数据库
  缓存
  用户
  文件
  安全
"""
__author__ = 'Leon'


import ctypes
import time
from functools import wraps

def disk_space(drive):
    freespace = ctypes.c_ulonglong()
    calcspace = ctypes.windll.kernel32.GetDiskFreeSpaceExA
    err = calcspace(drive,
                    ctypes.byref(freespace),
                    None,
                    None)
    assert err != 0, 'calcspace failed'
    disk_size = freespace.value
    return disk_size


def fn_timer(function):
    @wraps(function)
    def function_timer(*args, **kwargs):
        t0 = time.time()
        result = function(*args, **kwargs)
        t1 = time.time()
        print ("Total time running %s: %s seconds" %
                (function.func_name, str(t1-t0))
                )
        return result
    return function_timer



# _disk_size=disk_space("c:")
#
# print("c:",_disk_size)