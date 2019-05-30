#!/usr/bin/env python
# -*- coding: utf-8 -*-

from loongtian.nvwa import settings

from chinese import text, constant
from chinese.text import *
from chinese.constant import *
from chinese.errors import *

# 默认设置
cur_language = settings.language
if cur_language =="chinese":
    pass # 已经作为默认选项加载过了（见上面）

elif cur_language=="english":
    from english import text,constant
    from english.text import *
    from english.constant import *
    from english.errors import *
