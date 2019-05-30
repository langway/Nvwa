#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon（梁冰）'
"""
创建日期：2015-10-12
"""
import types

from loongtian.util.helper import stringHelper


def ResolvePyTypeDecleration(codeLine,type=types.ClassType ):
    """
    处理一行中的类型（类、函数、属性等）的声明
    :rawParam codeLine:声明所在的代码行
    :return:
    """
    if stringHelper.IsStringNullOrEmpty(codeLine):
        return

    if type is None:
        type=types.ClassType

    _defName,_space,_inheritedFrom,_args=None,'',None,None


    if codeLine[0]==' ':#取得开始的空格

        for s in codeLine:
            if s==' ':#如果一直是空格，一直加下去
                _space+=' '
            else:#如果不是空格，跳出循环
                break
            pass#for s in codeLine:

        pass#for s in codeLine:

    codeLine=codeLine.strip().lstrip().rstrip(':')
    if codeLine.startswith(type+' '):
        codeLine=codeLine.replace(type+' ','')

    codeLine=codeLine.strip()


    c=codeLine.split('(')

    if c:
        _defName=c[0]
        if len(c)>1:
            if type==types.ClassType: #需要取得类的父类
                _inheritedFrom=c[1].rstrip(')')
            elif type==types.FunctionType : #需要取得函数的参数
                _args=c[1].split(',')#todo 这里需要处理默认参数、可变参数、self等。

    return _defName,_space,_inheritedFrom,_args

    pass#def ResolvePyTypeDecleration(codeLine):

def GetPyTypeBody(start,ParentCodeBody,parentSpace,bodyMark=' ',bodyEndMark=None):
    """
    根据缩进取得子代码体。
    :rawParam start:子代码体的开始位置
    :rawParam ParentCodeBody:父代码体
    :rawParam parentSpace:父代码体的缩进
    :rawParam bodyMark :每一行子代码体的开始标记
    :rawParam bodyEndMark:子代码体的结束标记（一般为None）
    :return:
    """
    if not ParentCodeBody or not isinstance(ParentCodeBody,list):
        raise ValueError('ParentCodeBody must be a list!')

    length=len(ParentCodeBody)
    if length<=0:
        return

    _typeBody=[]
    while start<=length:

        _line=ParentCodeBody[start]

        #如果已经到了结尾（根据结尾标识符），那么结束循环，返回结果
        if _line .startswith(bodyEndMark):
            _typeBody .append(_line )
            break

        if stringHelper.isStringNullOrEmpty(_line) or _line=='\n':#如果该行是空白或是换行，仍然添加#_line.isspace():
            _typeBody.append(_line)
            start+=1#增加行数计数器
            continue

        _ltrimedLine=_line
        if stringHelper.isStringNullOrEmpty(parentSpace) and _ltrimedLine.startswith(parentSpace):
            #这里需要把前面的空格截取下去（不能使用replace！）
            _ltrimedLine=_ltrimedLine[len(parentSpace)]

        if _ltrimedLine.startswith(bodyMark):#如果这行代码前面仍有空格，说明是这一类型的代码体，否则，将进入下一类型
            _typeBody.append(_line)
            start+=1#增加行数计数器
        else:
            break

    return _typeBody

    pass#def GetPyTypeBody(i,ParentCodeBody,parentSpace):



