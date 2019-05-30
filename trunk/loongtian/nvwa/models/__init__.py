#!/usr/bin/env python
# coding: utf-8
"""
模型层（含操作，eg：CRUD）。
    MetaData、MetaNet、RealObject、Knowledge、Layer
    CentreMessage(八大中枢消息封装类）
"""
# from loongtian.nvwa.models.enum import ObjType,DirectionType


# class Memory: 2019-03-02 弃用。现改由用户memoryCentral维护
#     """
#     记录当前对象的记忆区，便于直接从记忆区取对象而不用每次从数据库中取
#     """
#     memoryCentral=None

# ####################################
#      模型关系表
# ####################################

#                         MetaNet
#                        /n   |1
#                      /     |
#                    /      |
#                  /       |
#                /1       |1
#           MetaData    Knowledge
#              | n         /n
#             |          /
#            |         /
#           | n      /1
#           RealObject--------Pattern--------Meanings
#                     1     1        1     1

#  2018-12-06:再论RealObject与Knowledge关系：
# 有两种：1、由Knowledge的所有元素通过转换引擎生成的RealObject，知识链的所有元素之间是修限关系或是动作执行关系
#               例如：r:中国-r:人民-r:解放军——>r:中国人民解放军。r:小明-a:打-r:小丽——>r:小明-r:手疼，r:小丽-r:哭
#         2、从集合的角度考虑，由Knowledge的所有元素构成（组件关系）的RealObject。
#               例如：k:{r:中国-r:人民-r:解放军}——》r:x，r:x-r:父对象-r:集合,r:x-r:组件-r:中国......
#               其中：k的id 应与 r:x的id相同
