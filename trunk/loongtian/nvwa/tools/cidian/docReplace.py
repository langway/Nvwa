#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
文本处理的帮助类
"""
__author__ = 'Leon'

import sys
import os

path_r = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'newDict.xml')
file_r = open(path_r, 'r')
lines = file_r.readlines()
file_r.close()

finalLines=[]

replacedLines=[]
for line in lines:
    new_line=line.strip()
    if new_line.find("<F>")>=0 :#new_line.find("<X>")>=0 or new_line.find("<W>")>=0 or new_line.find("<S>")>=0:
        # if new_line.find("愚昧软弱")>=0:
        #     a=1
        replaced=False

        if new_line.find("：")>=0:
            new_line=new_line.replace("：", "<Example>")
            replaced=True
        if new_line.find(":")>=0:
            new_line=new_line.replace("：", "<Example>")
            replaced=True

        if new_line.find("<Example>")>=0:
            if new_line.find("。</X>")>=0:
                new_line=new_line.replace("。</X>", "。</Example></X>")
                replaced=True
            if  new_line.find("?</X>")>=0:
                new_line=new_line.replace("?</X>", "?</Example></X>")
                replaced=True
            if  new_line.find("？</X>")>=0:
                new_line=new_line.replace("？</X>", "?</Example></X>")
                replaced=True
            if new_line.find("！</X>")>=0:
                new_line=new_line.replace("！</X>", "！</Example></X>")
                replaced=True
            if new_line.find("!</X")>=0:
                new_line=new_line.replace("!</X", "！</Example></X>")
                replaced=True
            # 带空格
            if new_line.find("。 </X>")>=0:
                new_line=new_line.replace("。 </X>", "。</Example></X>")
                replaced=True
            if  new_line.find("? </X>")>=0:
                new_line=new_line.replace("? </X>", "?</Example></X>")
                replaced=True
            if  new_line.find("？ </X>")>=0:
                new_line=new_line.replace("？ </X>", "?</Example></X>")
                replaced=True
            if new_line.find("！ </X>")>=0:
                new_line=new_line.replace("！ </X>", "！</Example></X>")
                replaced=True
            if new_line.find("! </X")>=0:
                new_line=new_line.replace("! </X", "！</Example></X>")
                replaced=True

        if replaced:
            replacedLines.append(new_line)
            finalLines.append(new_line)
        else:
            finalLines.append(line)

    else:
        finalLines.append(line)

# print(replacedLines)

path_w = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'replacedDict.xml')
file_w = open(path_w, 'w')
lines = file_w.writelines(finalLines)
file_w.close()


