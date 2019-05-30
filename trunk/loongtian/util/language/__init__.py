# encoding: UTF-8

from loongtian.autotrade.trader.vtGlobal import get_setting

if get_setting('language')=="chinese":
    # 默认设置
    from chinese import text
elif get_setting('language')=="english":
    from english import text
