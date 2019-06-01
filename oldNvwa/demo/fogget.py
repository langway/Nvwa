#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    fogget 
Author:   fengyh 
DateTime: 2014-10-15 9:22 
UpdateLog:
1、fengyh 2014-10-15 Create this File.


"""

"""
赫尔曼·艾宾浩斯（Hermann Ebbinghaus 1850.1.24～1909.2.26）德国心理学 家。
1、复习的原则
　　时间间隔：20分钟 1小时 8小时 1天 2天 6天 31天 　　
重学节省诵读时间百分数：58.2 44.2 35.8 33.7 27.8 25.4 21.1 　　
2、复习点的确定 　　
    人的记忆周期分为短期记忆和长期记忆 两种。 　　
        第一个记忆周期是 5分钟 　　
        第二个记忆周期是30分钟 　　
        第三个记忆周期是12小时
    这三个记忆周期属于短期记忆的范畴。 　　
    下面是几个比较重要的周期。 　　
        第四个记忆周期是 1天 　　
        第五个记忆周期是 2天 　　
        第六个记忆周期是 4天 　　
        第七个记忆周期是 7天 　　
        第八个记忆周期是15天 　　
    以上的8个周期应用于背词法，作为一个大的背词的循环的8个复习点，可以最大程度的提高背单词的效率
3. 我自己的时间点
    我选取了比较有规律的时间点作为自己的记忆点：
        5分钟   30分钟   12小时    1天    2天   4天   8天    16天
    其中5分钟和30分钟在一次记忆中实现，记忆一个单词单元要30分钟以上。
    其中16天时复习效率会比较高，可以灵活处理，因此不再强制记忆计划中。
    因此，最终的记忆点为：
        now    0.5天    1天    2天   4天   8天 （共记忆复习6次 即可完成该单元的记忆）
4. python 实现
    用到 time模块，list 结构, dict 结构，以及for , while , if 等逻辑分支结构。
"""

import time
listnum = 20    # 单元总数
wordlist = [ [] for i in range( listnum + 1 )]
# 第1单元 到 第4单元
for j in range(1,5) :
    # start at recordTime : "10 Aug 26 21" : 2010-8-26 21:00
    t = time.mktime( time.strptime( "10 Aug 26 21", "%y %b %d %H" ) )
    # print '=== WordList', j, '==='
    t += 60*60*12*(j-1)
    for i in [ 0, 0.5, 1, 2, 4, 8 ] :
        t += 60*60*24*i
        c = time.ctime(t)
        p = time.strptime(c)
        s = time.strftime( "%Y-%b-%d %H", p )
        wordlist[j].append(s)
        # print s
# 第5单元 到 第8单元
for j in range( 5, 9 ) :
    # start at recordTime : "10 Aug 30 21" : 2010-8-30 21:00
    t = time.mktime( time.strptime( "10 Aug 30 21", "%y %b %d %H" ) )
    # print '=== WordList', j, '==='
    t += 60*60*12*(j-5)
    for i in [ 0, 0.5, 1, 2, 4, 8 ] :
        t += 60*60*24*i
        c = time.ctime(t)
        p = time.strptime(c)
        s = time.strftime( "%Y-%b-%d %H", p )
        wordlist[j].append(s)
        # print s
# 第9单元 到 第20单元
for j in range( 9, listnum + 1 ) :
    # start at recordTime : "10 Sep 01 21" : 2010-9-01 21:00
    t = time.mktime( time.strptime( "10 Aug 30 21", "%y %b %d %H" ) )
    # print '=== WordList', j, '==='
    t += 60*60*12*(j-5)
    for i in [ 0, 0.5, 1, 2, 4, 8 ] :
        t += 60*60*24*i
        c = time.ctime(t)
        p = time.strptime(c)
        s = time.strftime( "%Y-%b-%d %H", p )
        wordlist[j].append(s)
        # print s
# 时间点作为key建立字典存储结构
j = 1
timedict = {}
while j <= listnum :
    for listtime in wordlist[j] :
        if listtime not in timedict :
            timedict[ listtime ] = [j]
        else :
            timedict[ listtime ].append(j)
    j += 1
# print '=== timedict ==='
# print timedict
# 按照时间先后顺序存储“艾宾浩斯”时间表
timelist = []
for i in timedict.keys() :
    t = time.mktime( time.strptime( i, "%Y-%b-%d %H" ) )
    timelist.append( t )
timelist.sort()
for i in range( len( timelist ) ) :
    c = time.ctime( timelist[i] )
    p = time.strptime(c)
    s = time.strftime( "%Y-%b-%d %H", p )
    timelist[i] = s
# print '=== timelist ==='
# print timelist
# 按照时间先后顺序打印“艾宾浩斯”记忆计划表
for j in timelist :
    print '=== ', j, ' ==='
    temp = timedict[j]
    for i in temp :
        print 'WordList ', i
