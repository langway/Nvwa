#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

class InstinctsText():
    """
    直觉对象处理中的文本。
    """
    ######################################
    #    元数据对象（系统内置）
    ######################################

    # 元对象（基础对象）
    none = "无"
    original_object = "元对象"
    original_knowledge = "元知识链"

    original_anything = "什么"

    # 集合
    original_collection = "元集合"
    original_next = "下一个"
    # 集合中的省略元素
    original_ellipsis = "…"
    # 内部集合标记（k1     k0     List，将k0包裹在集合中）=""
    original_list = "#List#"

    # 元占位符,2018-09-02 取消，否则无法计算有多少个占位符，直接用realobject的type表示
    # original_placeholder="元占位符"

    # 构成
    ingredient = "成分"
    attribute = "属性"
    component = "组件"
    parent = "父对象"
    # contrary="相反"
    # equivalent="相同"
    belongs = "所属物"
    relevancy = "相关物"
    action = "动作"
    # 模式创建使用，2018-07-04 不再使用意思、指、指的是等含义太多的对象
    meaning1 = "意义为"
    meaning2 = "意义"
    meaning3 = "意义是"
    meaning4 = "指的是"
    meaning5 = "理解为"
    meaning6 = " meaning as "

    # 观察者
    observer = "观察者"
    # 女娲本身
    nvwa_ai = "女娲AI"
    # self ="我"

    # 代码，关联女娲世界与代码世界
    original_code = "代码"
    original_code_language = "代码语言"

    inner_operation = "#inner_operation#"
    inner_operation_createExcutionInfo = "#createExcutionInfo#"

# from loongtian.nvwa.models.model import Model
# class UserModel(Model):
#
#     def __init__(self):
#         super(UserModel, self).__init__()
    

class UserTags():
    """
    作为用户的实际对象中的文本。
    """
    username = "用户名"
    realname ="真实姓名"
    nickname = "昵称"
    email = "用户邮箱"
    phone = "手机"
    password = "密码"
    gender = "性别"
    manager = "是否管理员"  # 0-会员;1-管理员
    photo = "用户头像"  # 存储原图路径，不同尺寸头像单独方法处理
    location = "地区代码"  # 记录地区唯一编码，单独方法处理
    oauth = "是否第三方授权登录"  # 0为非授权， 1为授权
    adder = "添加人"
    adderip = "添加人IP"
    addtime = "添加时间"
    status = "状态"  # 0-不可用(逻辑删除);200-正常

    facility = "当前登录设备"
    ip = "当前登录设备的ip地址"
    port = "当前登录设备的ip地址的port"

    assistant = "个人助理"
