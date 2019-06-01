#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
配置参数读写单例类
>>> conf=Config()
>>> conf.add_section("ConfigTest")
>>> conf.set("ConfigTest","ConfigTestKey","ConfigTestValue")
>>> print(conf.get("ConfigTest","ConfigTestKey"))
ConfigTestValue
>>> conf.remove_section("ConfigTest")
"""
__author__ = 'Liuyl'
import ConfigParser
import singleton
import os


@singleton.singleton
class Config:
    def __init__(self):
        path = os.path.normpath(os.path.join('conf', 'app.conf'))
        root = os.path.normpath(os.path.dirname(os.path.dirname(__file__)))
        self.__path = os.path.join(root, path)
        self.cf = ConfigParser.ConfigParser()
        self.cf.read(self.__path)
        if not self.cf.has_section('app'):
            self.add_section('app')
        self.set('app', 'root', root)

    def get(self, section, option):
        return self.cf.get(section=section, option=option)

    def set(self, section, option, value):
        self.cf.set(section=section, option=option, value=value)

    def save(self):
        self.cf.write(open(self.__path, "w"))

    def add_section(self, section):
        self.cf.add_section(section)

    def remove_section(self, section):
        self.cf.remove_section(section)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
