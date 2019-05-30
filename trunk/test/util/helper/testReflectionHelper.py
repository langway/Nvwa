#!/usr/bin/env python
# -*- coding: utf-8 -*-
from loongtian.util.helper import fileHelper
from unittest import TestCase
import loongtian.util.helper.reflectionHelper as ReflectionHelper
import os
import new


class ParameterObj(object):
    """
    测试用， 提供给测试参数
    """
    def parameterFun(self, arg):
        return []


class TestReflectionHelper(TestCase):

    def setUp(self):
        print("----setUp----")

    def test_get_module(self):
        print("----test_get_module----")
        moduleName = ReflectionHelper._get_module('fileHelper')
        print('fileHelper:', moduleName)
        moduleName = ReflectionHelper._get_module('jsonHelper')
        print('jsonHelper:', moduleName)
        moduleName = ReflectionHelper._get_module('notExist')
        print('notExist:', moduleName)


    def test_get_func(self):
        print("----test_get_func----")
        funName = ReflectionHelper._get_func('jsonHelper.obj2json')
        print('jsonHelper.obj2json', funName)
        funName = ReflectionHelper._get_func('reflectionHelper._get_module')
        print('reflectionHelper._get_module', funName)


    def test_get_Class(self):
        print("----test_get_Class----")
        className = ReflectionHelper._get_Class('fileHelper.FileHelper')
        print('FileHelper', className)

    def testApplyFuc(self):
        print("----testApplyFuc----")
        path = os.path.split(os.path.realpath(__file__))[0]
        applyFucName = ReflectionHelper.applyFuc(FileHelper(), 'getTree', (path,))
        print('getTree__applyFucName:', applyFucName)
        applyFucName = ReflectionHelper.applyFuc(FileHelper(), 'getTreePlane', (path,))
        print('getTreePlane__applyFucName:', applyFucName)

    def testGetObject(self):
        print("----testGetObject----")
        applyObjectName = ReflectionHelper.getObject('testReflectionHelper.TestGetObjectParameter')
        print('testGetObject:', applyObjectName)

    def testEnhance_method(self):
        print("----testEnhance_method----")
        Enhance_method_name = ReflectionHelper.enhance_method(FileHelper(), 'getTreePlane', 'getOtherTree')
        print('testEnhance_method:', Enhance_method_name)

    def testMethod_logger(self):
        print("----testMethod_logger----")
        path = os.path.split(os.path.realpath(__file__))[0]
        Method_logger_name = ReflectionHelper.method_logger(ParameterObj().parameterFun, self)
        print('testMethod_logger:', Method_logger_name)

    def testCreateInstance(self):
        print("----testCreateInstance----")
        createInstance_name = ReflectionHelper.createInstance('fileHelper.FileHelper')
        print('testCreateInstance:', createInstance_name)

    def testCreate_object_Dynamic(self):
        print("----testCreate_object_Dynamic----")
        create_object_Dynamic_name = ReflectionHelper.create_object_Dynamic('testReflectionHelper', 'TestCreateObj')
        print('testCreate_object_Dynamic:', create_object_Dynamic_name)

    def tearDown(self):
        print("----tearDown----")


class TestGetObjectParameter:
    """
    该类为测试testGetObject方法中new.instance需要参数
    new.instance 需要参数类型为classobj, 定义新式类的类型为type， 经典类类型为classobj
    """
    def __init__(self):
        pass
