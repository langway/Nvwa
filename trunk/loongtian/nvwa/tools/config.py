# encoding: UTF-8

"""
通过VT_setting.json加载全局配置
"""

import os
import traceback
import json

"""
2019-01-21 目前弃用，直接在setting.py中设置，原因：json不能传入类型
"""
globalSetting = {}  # 全局配置字典

__settingFileName = "settings.json"


try:
    currentFolder = os.path.split(os.path.realpath(__file__))[0]
    currentJsonPath = os.path.join(currentFolder, __settingFileName)
    if os.path.isfile(currentJsonPath):
        f = file(currentJsonPath)
        globalSetting = json.load(f)
except:
    print (u'加载全局配置字典错误！')
    traceback.print_exc()


def get_setting(key):
    """
    从全局配置字典取得对应的配置
    :param key:
    :return:
    """
    if key is None or not type(key) is str:
        return
    return globalSetting.get(key, None)




