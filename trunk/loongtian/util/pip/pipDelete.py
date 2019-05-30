#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
删除制定组件
"""
import loongtian.util.pip.pipHelper as pipHelper



if __name__ == '__main__':
    # 删除已安装组件(尽量不要使用)
    pipHelper.delete("pip")
