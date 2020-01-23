#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" 

"""
__author__ = 'Leon'


# s = 'q|w;e|r;r|t;t|y;y|u;u|i;i|o;'
#
#
# # s = 待分割字符串
# # ds = 分割符字符串
# def mySplit(s, ds):
#     res = [s]
#     # 循环所有的分割符
#     for d in ds:
#         print(d)
#         t = []
#         # 一定要list 一下才能正确使用
#         res2 = list(map(lambda x: t.extend(x.split(d)), res))
#         # print(res2)
#         res = t
#     # 过滤掉空字串
#     return [x for x in res if x]
#
#
# r = mySplit(s, ';|')
# print('r', r)
#
# import re
#
# s = 'q|w;e|r;r|t;t|y;y|u;u|i;i|o;\r\n'
#
# r = re.split(r'[,;\t|]+', s)
# print(r)
#
#
#

# import re
#
#
# def my_split(str,sep="要求\d+|岗位\S+"):  # 分隔符可为多样的正则表达式
#     wlist = re.split(sep,str)
#     sepword = re.findall(sep,str)
#     sepword.insert(0," ") # 开头（或末尾）插入一个空字符串，以保持长度和切割成分相同
#     wlist = [ y+x for x,y in zip(wlist,sepword) ] # 顺序可根据需求调换
#     return wlist


#
# if __name__ == "__main__":
#     inputstr = "岗位：学生： \n要求1.必须好好学习。\n要求2.必须踏实努力。\n要求3.必须求实上进。"
#     res = my_split(inputstr)
#     print ('\n'.join(res))
