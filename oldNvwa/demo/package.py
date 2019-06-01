#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
新建python文件
>>> print("No Test")
No Test
"""
__author__ = 'Liuyl'
import __builtin__
import exceptions
import os
import os.path
import stat
import string
import re
import math
import cmath
import operator
import copy
import sys
import atexit
import time
import types
import gc

import fileinput

if __name__ == '__main__':
    # __biultin__
    print(all([0, 1, 1]))  # all
    print(any([0, 1, 1]))  # any

    def test_apply(*args, **kwds):
        print(args, kwds)

    apply(test_apply, (1, 2), {'s': 3, 'e': 4})  # apply
    print(bin(6))

    class TestCmp(object):
        static_data = 3

        def __init__(self, data):
            self.data = data

        def __cmp__(self, other):
            return -cmp(self.data, other.data)

    print(cmp(TestCmp(2), TestCmp(1)))  # cmp
    print(coerce(1.3, 13L))  # coerce
    exec_code = compile("print('test compile')\nprint('test compile2')", '', 'exec')
    exec exec_code  # compile exec
    eval_code = compile("2**8", '', 'eval')
    print(eval(eval_code))  # compile eval

    def test_dir(a, b=[1, 2], c=9):
        d = 0
        return b + [a + c + d]

    print(dir(test_dir))  # dir
    print(dir(TestCmp))
    print(dir(TestCmp(2)))

    print(divmod(5, 2))  # divmod

    print(format(75.6564, '.2f'))  # format  __format__()

    print(globals())

    hello = 0  # repr
    x = 'hello'
    y = 'world'
    z1 = repr(x)
    z2 = str(x)
    print(repr(x))
    print(eval(z1), eval(z1) == x)
    print(eval(z2), eval(z2) == x)
    print('The value of x is ' + repr(x) + ', and y is ' + repr(y) + '...')
    print('The value of x is ' + str(x) + ', and y is ' + str(y) + '...')

    ziped = zip((1, 2, 3), (4, 5, 6), (7, 8, 9))  # zip
    print(ziped)
    print(zip(*ziped))
    # object
    # http://blog.163.com/jackylau_v/blog/static/175754040201182113817834/
    # __call__  http://www.2cto.com/kf/201303/193851.html
    # http://www.ibm.com/developerworks/cn/opensource/os-cn-pythonwith/
    # contextlib 模块

    # stat
    fileStats = os.stat('GADemo.py')  # 获取文件/目录的状态
    fileInfo = {
        'Size': fileStats[stat.ST_SIZE],  # 获取文件大小
        'LastModified': time.ctime(fileStats[stat.ST_MTIME]),  # 获取文件最后修改时间
        'LastAccessed': time.ctime(fileStats[stat.ST_ATIME]),  # 获取文件最后访问时间
        'CreationTime': time.ctime(fileStats[stat.ST_CTIME]),  # 获取文件创建时间
        'Mode': fileStats[stat.ST_MODE]  # 获取文件的模式
    }
    for field in fileInfo:  # 显示对象内容
        print '%s:%s' % (field, fileInfo[field])

    # string
    s = 'abcdefg-1234567'
    table = string.maketrans('abc', 'ABC')
    print(s)
    print(s.translate(table, 'fg123'))

    # re
    m1 = re.search("[^abc]", "aebcdf")
    print(m1.group())
    m2 = re.match("[^abc]", "aebcdf")
    print(m2)
    m3 = re.findall("^a\w+", "abcdfa\na1b2c3", re.MULTILINE)
    print(m3)

    # copy
    a = [1, 2, 3, 4, ['a', 'b']]  # 原始对象
    b = a  # 赋值，传对象的引用
    c = copy.copy(a)  # 对象拷贝，浅拷贝
    d = copy.deepcopy(a)  # 对象拷贝，深拷贝
    a.append(5)  # 修改对象a
    a[4].append('c')  # 修改对象a中的['a', 'b']数组对象
    print 'a = ', a
    print 'b = ', b
    print 'c = ', c
    print 'd = ', d

    # sys
    print(sys.argv)
    print(sys.platform)
    print(sys.modules)

    # gc http://www.douban.com/note/311388840/

    # fileinput
    pattern = "\d{3}-\d{3}-\d{4}"
    filePath = "test.log"
    for eachline in fileinput.input(filePath):
        a = re.search(pattern, eachline)
        if a:
            print ('line:', fileinput.lineno(), 'filename:', fileinput.filename(), 'length:', len(eachline.strip('\n')),
                   eachline)
    fileinput.close()

    # shutil http://www.cnblogs.com/xiaowuyi/archive/2012/03/08/2385808.html
    # tempfile http://www.cnblogs.com/captain_jack/archive/2011/01/19/1939555.html
    # StringIO  cStringIO http://www.cnblogs.com/sislcb/archive/2008/11/27/1341996.html
    # mmap  http://blog.chinaunix.net/uid-20393955-idInt-1645587.html

    # import UserDict,UserList,UserString
    # traceback http://blog.csdn.net/sding/article/details/5316645
    # errno 定义错误代码
    # getopt http://blog.csdn.net/tianzhu123/article/details/7655499
    import glob

    print glob.glob(r"*.py")
    # fnmatch 使用模式来匹配文件名, glob 和 find 模块在内部使用 fnmatch 模块来实现
    # http://blog.sina.com.cn/s/blog_a04184c101010ksl.html
    # random  http://www.cnblogs.com/yd1227/archive/2011/03/18/1988015.html
    # md5, sha http://www.cnblogs.com/mingaixin/archive/2013/02/20/2919313.html
    # zlib http://blog.csdn.net/JGood/article/details/4608546
    # code 在程序中启动一个python解释器