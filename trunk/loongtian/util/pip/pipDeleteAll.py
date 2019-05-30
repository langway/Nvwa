#!/usr/bin/env python
# -*- coding: utf-8 -*-
import loongtian.util.pip.pipHelper as pipHelper
import loongtian.util .pip.pipInstallAll as pipInstallAll


if __name__ == '__main__':
    # 删除全部已安装组件(尽量不要使用)
    pipHelper.deleteAll(pipInstallAll.COMPONENTS)
