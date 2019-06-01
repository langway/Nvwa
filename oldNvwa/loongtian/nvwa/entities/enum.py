#!/usr/bin/env python
# coding: utf-8
"""
枚举模块

Project:  nvwa
Title:    enum 
Author:   fengyh 
DateTime: 2014/9/3 9:45 
UpdateLog:
1、fengyh 2014/9/3 Create this File.
2、fengyh 2014/9/3 创建生成enum的方法enum。
3、fengyh 2014/9/3 创建EndTypeEnum类。
4、fengyh 2014/9/16 创建SentenceTypeEnum类，MatchDegreeTypeEnum类，CommandJobTypeEnum，DataSourceTypeEnum。
"""
def enum(module, str_enum, sep=None):
    """
    把用特定分隔符隔开的 str_enum 字符串实现为 module 的枚举值.
    @param module 宿主对象, 可以是 module, class, ...
    @param str_enum 输入的需要枚举的字符串
    @param sep 分割符，默认为空格。
    eg1: enum(test, "A B C") => test.A,test.B,test.C == 0,1,2
    eg2: enum(CTest, 'one=1,two,three,ten=0x0A,eleven', sep=',') => CTest.one,CTest.two,CTest.ten, CTest.eleven == 1,2,10,11
    """
    idx = 0
    for name in str_enum.split(sep):
        if '=' in name:
            name, val = name.rsplit('=', 1)
            if val.isalnum():
                idx = eval(val)
        setattr(module, name.strip(), idx)
        idx += 1


class GrouperPriorityEnum(object):
    """
    Metadata优先级分组枚举
    Grouper中对Metadata的关联RealObject和Action的排序优先级。
    NoPriority=-1,RealObjectLow1=0,RealObject=1,ActionLow2=2,ActionLow1=3,Action=4
    fengyh 2014-9-3
    """
    def __init__(self):
        enum(GrouperPriorityEnum,
             'NoPriority,'
             'Word,'
             'Class,'
             'ClassActionSplit,'
             'ActionLow2,'
             'ActionLow1,'
             'ActionLow0,'
             'Action',
             sep=',')
        pass

class EndTypeEnum(object): # TODO 目前未使用
    """
    Knowledge中EndType的枚举值。
    UnKnown=0,RealObject=1,Relation=2,Action=3,Modifier=4,Anything=5,Empty=6
    fengyh 2014-9-3
    """
    def __init__(self):
        enum(EndTypeEnum, 'UnKnown=0,RealObject=1,Relation=2,Action=3,Modifier=4,Anything=5,Empty=6', sep=',')
        pass

class CommandJobTypeEnum(object):
    """
    行为中枢任务类型。
    输出响应文字0，保存数据1，阈值增加2，阈值减少3，记忆To知识4
    fengyh 2014-10-16
    """
    def __init__(self):
        enum(CommandJobTypeEnum, 'Output=0,Save=1,Increase=2,Decrease=3,M2K=4', sep=',')
        pass

class SentenceTypeEnum(object):
    """
    句子的类型。
    非疑问句0，问句1是否问句，问句2指代问句，问句3选择问句，问句4叠加问句,命令句子5
    fengyh 2014-10-16
    增加指代问句类型，what，where，who，when,how many
    """
    def __init__(self): # TODO 未来进行替换
        enum(SentenceTypeEnum,
             'NotAsk=0,'
             'AskSplit=1,'
             'AskYesNo=11,'
             'AskNeedReplaceWhat=21,AskNeedReplaceWhere=22,AskNeedReplaceWho=23,'
             'AskNeedReplaceWhen=24,AskNeedReplaceHowMany=25,'
             'AskSelection=3,'
             'AskComposition=4,'
             'Command=5',
             sep=',')
        pass

class MatchDegreeTypeEnum(object):
    """
    评估结果匹配程度类型。
    完全匹配0，部分匹配1，无匹配2，完全或部分匹配3
    fengyh 2014-10-16
    """
    def __init__(self):
        enum(MatchDegreeTypeEnum, 'Full=0,Partial=1,No=2,FullAndPartial=3', sep=',')
        pass

class DataSourceTypeEnum(object):
    """
    数据来源类型。
    来自知识库用0表示，控制台2，RealObject3
    fengyh 2014-10-16
    """
    def __init__(self):
        enum(DataSourceTypeEnum, 'Knowledge=0,Console=2,RealObject=3', sep=',')
        pass

class ConflictTypeEnum(object):
    """
    冲突返回值 
    未发现0，冲突1，发现并匹配（无冲突）2，发现冲突3。 # TODO 1和3有冲突。
    """
    def __init__(self):
        enum(ConflictTypeEnum, 'NotFinded=0,Conflict=1,Finded=2,FindedAndConflict=3', sep=',')
        pass

class ThresholdDecreaseRateTypeEnum(object):
    """
    阈值衰减率枚举
    0.01, 0.1, 0.4, 0.8
    """
    def __init__(self):
        enum(ThresholdDecreaseRateTypeEnum,'Rate01_001=0.01,Rate02_01=0.1,Rate03_04=0.4,Rate04_0.8=0.8')
        pass