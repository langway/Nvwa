#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

from loongtian.nvwa import settings
from loongtian.util.db.postgres.dbPool import _DbPools

DbPools = None
# 设置数据库
if settings.db.db_type == "postgres":
    DbPools = _DbPools.getDbPools(settings.db.postgres,force_to_reload=True)
else:
    DbPools = None
