#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
金字塔分润体系的分成比例计算
"""
__author__ = 'Leon'

import  loongtian .util .helper.stringHelper as stringHelper

def count(totalLevel):
    benifits=[]

    for i in range(totalLevel) :
        benifits.append(getCurrentBenifits(i,totalLevel))
        pass #

    total=0

    for item in benifits:
        total+=item

    for i in range(len(benifits )):
        benifits[i]=benifits[i]/total

    return benifits

    pass # def Count(totalLevel,currentLevel):


def getCurrentBenifits(currentLevel,totalLevel):

    benifit=1.0/(currentLevel+1)
    return benifit
    pass

print ("----开始计算----")

# raw_input("")
for i in range(2,6):
    benifits=count(i)
    temp=u"["
    for j in range(len(benifits ) ):
        temp+=u"第{0}级：{1}".format(str(j),str(benifits[j]))
    temp+=u"]"

    # print(stringHelper.ConverUnicodeToString("层级总数：{0}".format(str(i))) ,temp)
    print(benifits )


# print("----共计：{0}----".format(str(total)) )