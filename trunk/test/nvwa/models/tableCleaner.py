#!/usr/bin/env python
# -*- coding: utf-8 -*-


from loongtian.nvwa.tools.db import DbPools

DbPools["nvwa"].executeSQL([
            "delete from \"tbl_metaData\"",
            "delete from \"tbl_realObject\"",
            "delete from \"tbl_metaNet\"",
            "delete from \"tbl_knowledge\"",
            "delete from \"tbl_layer\"",
        ])