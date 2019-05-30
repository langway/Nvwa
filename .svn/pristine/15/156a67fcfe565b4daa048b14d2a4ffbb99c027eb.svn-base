#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" service
service服务包
"""
__author__ = 'Liuyl'

# knowledge（知识库）服务, 不依赖其他服务
from loongtian.nvwa.service.repository_service.knowledge import KnowledgeService
knowledge_srv = KnowledgeService()

# real_object（实际对象）服务,依赖knowledge服务
from loongtian.nvwa.service.repository_service.real_object import RealObjectService
real_object_srv = RealObjectService()

# original（原始知识）服务, 依赖服务: real_object, knowledge
from original import OriginalService
original_srv = OriginalService()

# metadata（元数据）服务, 依赖服务: real_object, knowledge, original
from loongtian.nvwa.service.repository_service.metadata import MetadataService
metadata_srv = MetadataService()

# fragment（片段--数据集）服务集, 依赖服务: real_object, knowledge, original
from loongtian.nvwa.service.fragment_service_container import FragmentServiceContainer
fsc = FragmentServiceContainer() # 片段服务容器
fragment_srv = fsc.fragment

# original_init（原始知识初始化）服务, 依赖服务: real_object, knowledge, metadata, action, action_define
from original_init import OriginalInitService
original_init_srv = OriginalInitService()

# command（命令）服务, 依赖服务: original_init
from command import CommandService
command_srv = CommandService()

__all__ = [
    "original_init_srv",
    "real_object_srv",
    "knowledge_srv",
    "metadata_srv",
    "original_srv",
    "fragment_srv",
    "fsc",
    "command_srv"]