#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon（梁冰）'

#import loongtian.Tools.NvwaObjectsCodeConvertor.NvwaObjectsCodeConvertor as converter
import imp,new,os,types

#fragement=converter.NvwaObjectsCodeConvertor.convertPyFileToNvwaObjects('C:\Users\Administrator\PycharmProjects\NvwaObjectsCodeConvertor\Test\nvwaObjectsCodeConvertorSingleClass.py')

path=os.getcwd()+'\NvwaObjectsCodeConvertorSingleClass.py'
aMod = imp.load_source('NvwaObjectsCodeConvertorSingleClass',path)
aModFile=open(path)

aModText=aModFile.read().decode('utf-8')

#print aModText


print 'aMod的类型：',type(aMod) is types.ModuleType

print 'aMod的子项：',dir(aMod)

for name in dir(aMod):
    aAttrib= getattr(aMod, name)
    print 'aMod中'+name+'的类型：',type(aAttrib)

    print type(aAttrib) is property


aClass= getattr(aMod, 'Student')

print 'aClass的类型：',type(aClass)

print 'aClass的属性：',dir(aClass)#这里还要查看class中的子类classChildClass是否创建

print 'aClass的注释：',aClass.__doc__

for name in dir(aClass):
    aAttrib= getattr(aClass, name)
    print 'aClass中'+name+'的类型：',type(aAttrib)

    print type(aAttrib) is property

#查看gender属性中的子类是否创建
genderAttrib=getattr(aClass,'gender')

print genderAttrib
print 'Student.gender属性的属性列表：',dir(genderAttrib)

print 'genderAttrib.__subclasshook__:',dir(genderAttrib.__subclasshook__)

#查看Speak函数中的子类是否创建
speakFunction=getattr(aClass,'Speak')

print speakFunction
print 'Student.Speak函数的属性列表：',dir(speakFunction)

print 'Student.Speak.__subclasshook__:',dir(speakFunction.__subclasshook__)

oldText=aClass.__doc__.decode('utf-8')
newText=u'New Docs这是新文档注释'

try:
    aClass.__doc__=newText
except Exception,e:
    print e

print 'aClass的新注释：',aClass.__doc__

aModText=aModText.replace(oldText,newText)


#print aModText


# print aClass.__source__



# genderClass=getattr(aMod,'gender')
#
# print type(genderClass)
#
# print genderClass.__doc__#.decode('utf-8')
#
# print dir(genderClass)



#s=aClass()#new.instance(aClass)

try:
    s=new.instance(aClass)
except Exception,e:

    print e
    s=aClass()



print s.__class__

print s.__doc__#.decode('utf-8')

s.__doc__=u'New Docs这是第二次更改的新文档注释'

print s.__doc__




genderAttrib=getattr(aClass,'gender')

print type(genderAttrib)

print genderAttrib.__doc__.decode('utf-8')


aClass=getattr(aMod,'TestA')
print 'TestA:',aClass
print 'TestA type:',type(aClass)
print 'TestA is class type:',type(aClass) is types.ClassType
print 'TestA is class:',aClass is types.ClassType

aClass=getattr(aMod,'TestB')
print 'TestB:',aClass
print 'TestB type:',type(aClass)
print 'TestB is class type:',type(aClass) is types.ClassType
print 'TestB is class:',aClass is types.ClassType

aAttrib=getattr(aClass,'FuncB')
print 'FuncB:',aAttrib
print 'FuncB type:',type(aAttrib)
print 'FuncB is method type:',type(aAttrib) is types.MethodType
print 'FuncB is method:',aAttrib is types.MethodType
print 'FuncB is function type:',type(aAttrib) is types.FunctionType
print 'FuncB is function:',aAttrib is types.FunctionType

print 'FuncB is type:',type(aAttrib) is types.TypeType

aClass=getattr(aMod,'TestC')
print 'TestC:',aClass
print 'TestC type:',type(aClass)

print dir(aClass)
print 'TestC is class type:',type(aClass) is types.ClassType
print 'TestC is type:',type(aClass) is types.TypeType
print 'TestC name:',aClass.__name__
print 'TestC str:',aClass.__str__
print 'TestC class:',aClass.__class__
print 'TestC class string is <class \'NvwaObjectsCodeConvertorSingleClass.TestC\'>:',str(aClass)=='<class \'NvwaObjectsCodeConvertorSingleClass.TestC\'>'
print 'TestC type str:',type(aClass).__str__


aAttrib=getattr(aClass,'FuncC')
print 'FuncC:',aAttrib
print 'FuncC type:',type(aAttrib)
print 'FuncC is method type:',type(aAttrib) is types.MethodType
print 'FuncC is method:',aAttrib is types.MethodType
print 'FuncC is function type:',type(aAttrib) is types.FunctionType
print 'FuncC is function:',aAttrib is types.FunctionType
print 'FuncC is type:',type(aAttrib) is types.TypeType





