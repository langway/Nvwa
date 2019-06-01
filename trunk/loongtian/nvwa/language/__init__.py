#!/usr/bin/env python
# -*- coding: utf-8 -*-

from loongtian.nvwa import settings

from loongtian.nvwa.language.chinese import text, constant
from loongtian.nvwa.language.chinese.text import *
from loongtian.nvwa.language.chinese.constant import *
from loongtian.nvwa.language.chinese.errors import *

# 默认设置
cur_language = settings.language
if cur_language =="chinese":
    pass # 已经作为默认选项加载过了（见上面）

elif cur_language=="english":
    from loongtian.nvwa.language.english import text,constant
    from loongtian.nvwa.language.english.text import *
    from loongtian.nvwa.language.english.constant import *
    from loongtian.nvwa.language.english.errors import *
