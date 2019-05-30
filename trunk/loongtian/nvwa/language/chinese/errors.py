#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'


class InstinctsErrors():
    """
    直觉对象处理中的错误。
    """
    Can_Not_Create_Instinct = "无法创建直觉对象，原因：%s"
    Load_Instincts_Failure = "加载所有直觉（包括\"属性\"、\"组件\"等顶级关系，\"意义为\"等分层“标签”）失败，原因："


class UserErrors():
    """
    作为用户的实际对象处理中的错误。
    """
    ObjType_Is_Not_USER = "查询到的实际对象类型非用户类型！"
    Multi_Results_And_ObjType_Is_Not_USER = "系统错误，用户查询不唯一，且对象类型非用户类型！"
    ObjType_Is_Not_ASSISTANT = "查询到的实际对象类型非个人助理类型！"
    Multi_Results_And_ObjType_Is_Not_ASSISTANT = "系统错误，个人助理查询不唯一，且对象类型非个人助理类型！"

    Can_Not_Create_User = "无法创建用户对象，应至少提供用户名、电话号码或Email其中的一个！"

class InnerOperationsErrors():
    """
    直觉对象处理中的错误。
    """
    Can_Not_Create_InnerOperation = "无法创建女娲系统操作对象，原因：%s"
    Load_InnerOperations_Failure = "加载所有女娲系统操作对象失败，原因："