#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""

from __future__ import nested_scopes
import sys, types



__author__ = 'Administrator'

def _get_module(moduleName):

    aMod=None
    try:
        aMod = sys.modules[moduleName]
        if not isinstance(aMod, types.ModuleType):
            raise KeyError
    except KeyError:
        # The last [''] is very important!
        try:
            aMod = __import__(moduleName, globals(), locals(), [''])
            sys.modules[moduleName] = aMod
        # except ImportError:
        #     print(ImportError)#"ImportError:" + ImportError.message.__str__()  )
        finally:
            pass
    finally:
        return aMod

def _get_func(fullFuncName):
    """Retrieve a function object from a full dotted-package name."""

    # Parse out the path, module, and function
    lastDot = fullFuncName.rfind(u".")
    funcName = fullFuncName[lastDot + 1:]
    modPath = fullFuncName[:lastDot]

    aMod = _get_module(modPath)
    aFunc = getattr(aMod, funcName)

    # Assert that the function is a *callable* attribute.
    assert callable(aFunc), u"%s is not callable." % fullFuncName

    # Return a reference to the function itself,
    # not the results of the function.
    return aFunc

def _get_Class(fullClassName, parentClass=None):
    """Load a module and retrieve a class (NOT an instance).

    If the parentClass is supplied, className must be of parentClass
    or a subclass of parentClass (or None is returned).
    """
    aClass = _get_func(fullClassName)

    # Assert that the class is a subclass of parentClass.
    if parentClass is not None:
        if not issubclass(aClass, parentClass):
            raise TypeError(u"%s is not a subclass of %s" %
                            (fullClassName, parentClass))

    # Return a reference to the class itself, not an instantiated object.
    return aClass

def applyFuc(obj,strFunc,arrArgs):
    objFunc = getattr(obj, strFunc)
    return apply(objFunc,arrArgs)

def getObject(fullClassName):
    clazz = _get_Class(fullClassName)
    return new.instance(clazz)


def enhance_method(klass, method_name, replacement):
    '替代已有的方法'
    method = getattr(klass, method_name)
    setattr(klass, method_name, new.instancemethod(
        lambda *args, **kwds: replacement(method, *args, **kwds), None, klass))

def method_logger(old_method, self, *args, **kwds):
    '给方法添加调用执行日志'
    print ('*** calling: %s%s, kwds=%s' % (old_method.__name__, args, kwds))
    return_value = old_method(self, *args, **kwds) # call the original method
    print ('*** %s returns: %s' % (old_method.__name__, `return_value`))
    return return_value

# def demo():
#     class Deli:
#         def order_cheese(self, cheese_type):
#             print 'Sorry, we are completely out of %s' % cheese_type
#
#     d = Deli()
#     d.order_cheese('Gouda')
#
#     enhance_method(Deli, 'order_cheese', method_logger)
#     d.order_cheese('Cheddar')


"""本类用来动态创建类的实例"""
def createInstance(class_name, *args, **kwargs):
    """动态创建类的实例。
    [Parameter]
    class_name - 类的全名（包括模块名）
    *args - 类构造器所需要的参数(list)
    *kwargs - 类构造器所需要的参数(dict)
    [Return]
    动态创建的类的实例
    [Example]
    class_name = 'knightmade.logging.Logger'
    logger = Activator.createInstance(class_name, 'logname')
    """
    (module_name, class_name) = class_name.rsplit('.', 1)
    module_meta = __import__(module_name, globals(), locals(), [class_name])
    class_meta = getattr(module_meta, class_name)
    object = class_meta(*args, **kwargs)
    return object


    #author: D.Lucifer
def create_object_Dynamic(module_name, class_name,**object_attribute):
    """
    动态创建类
    :rawParam object_attribute:
    :return:
    """
    class o: pass

    if '#class' in object_attribute.keys():
        (module_name, class_name) = object_attribute['#class'].rsplit('.', 1)
        module_meta = __import__(module_name)
        class_meta = getattr(module_meta, class_name)
        o = class_meta()
    for k in object_attribute.keys():
        if str(type(object_attribute[k])) == '<class \'dict\'>':
            setattr(o, k, create_object_Dynamic(object_attribute[k]))
        else:
            setattr(o, k, object_attribute[k])
    return o


