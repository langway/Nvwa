#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    msvcrt_test 
Author:   Liuyl 
DateTime: 2014/12/15 14:00 
UpdateLog:
1、Liuyl 2014/12/15 Create this File.

msvcrt_test
>>> print("No Test")
No Test
"""
import time
import sys

__author__ = 'Liuyl'
import msvcrt


def readInput(caption, default, timeout=5):
    start_time = time.time()
    sys.stdout.write('%s(%s):' % (caption, default))
    input = ''
    while True:
        if msvcrt.kbhit():
            chr = msvcrt.getche()
            if ord(chr) == 13:
                break
            elif ord(chr) >= 32:
                input += chr
        if len(input) == 0 and time.time() - start_time > timeout:
            break
    print ''
    if len(input) > 0:
        return input
    else:
        return default


if __name__ == '__main__':
    print('123')
    while True:
        _input = readInput('Please type a name', 'john')
        print('>{0}'.format(_input))