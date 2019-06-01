#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
安装指定组件
"""
import loongtian.util.pip.pipHelper as pipHelper


if __name__ == '__main__':
    # 安装组件
    pipHelper.install("socketserver")
