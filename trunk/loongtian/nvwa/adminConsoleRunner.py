#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Leon"

"""
输入输出控制台（客户端）启动器
"""

from loongtian.nvwa.organs.console import Console
if __name__ == '__main__':
    from loongtian.nvwa.settings import auth
    console = Console(auth.adminUser.server_ip,auth.adminUser.server_port)
    console.run()
    pass