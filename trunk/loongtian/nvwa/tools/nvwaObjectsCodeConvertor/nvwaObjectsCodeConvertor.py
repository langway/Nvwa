#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import imp
import types
import re
import uuid
import xml.dom.minidom as minidom

from loongtian.util.helper import  stringHelper
from loongtian.util.common.enum import Enum
from loongtian.nvwa.tools.nvwaObjectsCodeConvertor import sourceCodeHelper
from loongtian.util.helper import jsonHelper

__author__ = 'Leon（梁冰）'

"""目前存在的问题：
   1、关键字对应：if xxx：yyy——>如果xxx，那么yyy
   2、外包（命名空间）、模块的引用
   3、未处理代码的抛出
   4、女娲系统的现有对象与代码生成的对象的关联
   5、Error处理
   6、变量或类型（函数、属性、类等）
      （1）当前module中的函数、属性、类
      （2）外包（命名空间）中的变量或类型
"""



class ObjectType(Enum):

    def __int__(self):
        self._slots__=('RealObject','Action','Modifier')

    @property
    def RealObject(self):
        return 0

    @property
    def Action(self):
        return 1

    @property
    def Modifier(self):
        return 2

    pass

a=ObjectType()
#a.Action=5
try:
    a.abc=23
except:
    print("You can not set the attribute to a Enum!")

try:
    print (a.abc)
except:
    print("'ObjectType' object has no attribute 'abc'")


class ReflectionType(Enum):
    """
    代码中反射的类型
    """
    ClassType=0
    FunctionType=1
    PropertyType=2
    InstanceType=3


    pass


class NvwaObjectDefinition():
    """
    Nvwa对象与代码的转换结构的定义。标准格式如下:
    # <NvwaObject>
    #         <id></id>
    #         <ObjectType>Action</ObjectType>
    #         <Relation>动作</Relation>
    #         <MetaData>说;speak</MetaData>
    #         <Position>1</Position>
    #         <Args>
    #             <NvwaObject>
    #                 <id></id>
    #                 <ObjectType>RealObject</ObjectType>
    #                 <Relation></Relation>
    #                 <Position>2</Position>
    #                 <MetaData>内容;content</MetaData>
    #             </NvwaObject>
    #         </Args>
    #         <Return></Return>
    #         <Remark>Position:用来存放与当前对象的位置关系，例如-1就是在当前对象前面(默认为1)</Remark>
    #     </NvwaObject>
    """


    def __init__(self):
        pass


    @property
    def ReflectedClass(self):
        """
        反射出来的Class
        :return:
        """
        return self._ReflectedClass

    @ReflectedClass.setter
    def ReflectedClass(self,value):
        if value is None:
            self._ReflectedClass=None

        if not type(value) is types.ClassType or not type(value) is type(object):
            raise TypeError(u'The type of id must be Reflected Class!')
        self._ReflectedClass=value

    @property
    def Xml(self):
        """
        从__doc__中取得的XmlDoc
        :return:
        """
        return self._Xml

    @Xml.setter
    def Xml(self,value):
        if value is None:
            self._Xml=None

        if not isinstance(value,minidom.Node) :
            raise TypeError(u'The type of Xml must be XmlNode!')
        self._Xml=value

    @property
    def ID(self):
        """

        :return:
        """
        return self._ID

    @ID.setter
    def ID(self,value):
        if value is None:
            self._ID=None

        if not isinstance(value,uuid) :
            raise TypeError(u'The type of id must be uuid!')
        self._ID=value


    @property
    def ObjectType(self):
        """

        :return:
        """
        return self._ObjectType

    @ObjectType.setter
    def ObjectType(self,value):
        # if value is None:
        #     self._ObjectType=None
        #
        # if not isinstance(value,int) :
        #     raise TypeError(u'The type of ObjectType must be integer!')
        self._ObjectType=value

    @property
    def Parent(self):
        """

        :return:
        """
        return self._Parent

    @Parent.setter
    def Parent(self,value):
        if value is None:
            self._Parent=None
        if not isinstance(value,NvwaObjectDefinition):
            return
        self._Parent=value

    @property
    def Relation(self):
        """

        :return:
        """
        return self._Relation

    @Relation.setter
    def Relation(self,value):
         self._Relation=value

    @property
    def MetaData(self):
        """

        :return:
        """
        return self._MetaData

    @MetaData.setter
    def MetaData(self,value):
         self._MetaData=value

    @property
    def Position(self):
        """

        :return:
        """
        return self._Position

    @Position.setter
    def Position(self,value):
        if value is None:
            self._Position=None

        if not isinstance(value,int) :
            raise TypeError(u'The type of Position must be integer!')
        self._Position=value

    @property
    def Args(self):
        """

        :return:
        """
        if self._Args is None:
            self._Args=Args()

        return self._Args

    @Args.setter
    def Args(self,value):
        if value is None:
            self._Args=None


        if not isinstance(value,Args):
            return
        self._Args=value

    @property
    def Return(self):
        """

        :return:
        """
        return self._Return

    @Return.setter
    def Return(self,value):
         self._Return=value


    @property
    def Remark(self):
        """

        :return:
        """
        return self._Remark

    @Remark.setter
    def Remark(self,value):
         self._Remark=value



    def __str__(self):
        # #s= "\"NvwaObject\":{\"ID\":\"{0}\"}"
        #    #,"ObjectType":"{1}","Relation":"{2}","MetaData":"{3}","Position":"{4}","Args":"{5}","Return":"{6}","Remark":"{7}",}'
        # s= '"NvwaObject":{"ID":"%(ID)s","ObjectType":"%(ObjectType)s","Parent":"%(Parent)s","Relation":"%(Relation)s","MetaData":"%(MetaData)s","Position":"%(Position)d","Args":"%(Args)s","Return":"%(Return)s","Remark":"%(Remark)s",}'
        # #s=s.format(self.ID)#,self.ObjectType,self.Relation,self.MetaData,self.Position,"Args",self.Return,self.Remark)
        # sArgs=''
        # i=0
        #
        # for arg in self.Args:
        #     if not isinstance(arg,NvwaObjectDefinition):
        #         continue
        #     if i==0:
        #         sArgs+='['
        #     sArgs+=arg.__str__()
        #     if i==self.Args.count()-1:
        #         sArgs+=']'
        #
        #
        # sParent=''
        # if not self.Parent is None:
        #     sParent+=self.Parent.ID+'/'
        # sParent+=self.MetaData
        #
        # s=s % {'ID':self.ID,'ObjectType':self.ObjectType,'Parent':sParent,'Relation':self.Relation,'MetaData':self.MetaData,'Position':self.Position,'Args':sArgs,'Return':self.Return,'Remark':self.Remark}
        # return s.encode('utf-8')

        return jsonHelper.obj2json(self,False )

        pass#def __str__(self):



    pass #class NvwaObjectDefinition()


class Args(list):
    """
    函数使用的参数列表（NvwaObjectFefinition）
    """
    def __add__(self, other):
        if not isinstance(other,Args):
            raise TypeError(u'The type of item must be Args(NvwaObjectDefinition list)!')
        list.__add__(self,other)
        pass

    def append(self, p_object):
        if not isinstance(p_object,NvwaObjectDefinition):
            raise TypeError(u'The type of item must be NvwaObjectDefinition!')
        list.append(self,p_object)
        pass

    pass


# class NvwaObjectDefinitions(list):
#     """
#     已经取得的NvwaObjectFefinition列表。
#     """
#     def __add__(self, other):
#         if not isinstance(other,NvwaObjectDefinitions):
#             raise TypeError(u'The type of item must be Args(NvwaObjectDefinition list)!')
#         list.__add__(self,other)
#         pass
#
#     def append(self, p_object):
#         if not isinstance(p_object,NvwaObjectDefinition):
#             raise TypeError(u'The type of item must be NvwaObjectDefinition!')
#         list.append(self,p_object)
#         pass
#
#     pass

class SourceCode():
    """
    对象的源代码的包装类（包括文本及是否改变的标记）
    """


    def __init__(self):
        self._CodeType='py'
        self._Changed=False
        self._CodeBody=None
        self.__FunctionArgs=Args()
        pass


    @property
    def CodeType(self):
        """
        对象的源代码类型（包括python、c#、java等）
        """

        return self._CodeType

        pass

    @CodeType.setter
    def CodeType(self,value):

        self._CodeType=value

        pass

    @property
    def TypeType(self):
        """
        对象的源代码在程序集中的类型（包括module（c#、java中相当于包或命名空间）、class、property、function、method等）
        """

        return self._TypeType

        pass

    @TypeType.setter
    def TypeType(self,value):

        self._TypeType=value

        pass

    @property
    def TypeName(self):
        """
        对象的源代码在程序集中的名称
        """

        return self._TypeName

        pass

    @TypeName.setter
    def TypeName(self,value):

        self._TypeName=value

        pass

    @property
    def Decleration(self):
        """
        对象的源代码作为声明的那一行（多行）的字符串
        """

        return self._Decleration

        pass

    @Decleration.setter
    def Decleration(self,value):

        self._Decleration=value

        pass

    @property
    def Decorator(self):
        """
        对象声明的装饰器（上一行（多行）的字符串）
        """

        return self._Decorator

        pass

    @Decorator.setter
    def Decorator(self,value):

        self._Decorator=value

        pass

    @property
    def CodeBody(self):
        """
        对象除了声明之外的源代码体（文本、多行）
        """

        return self._CodeBody

        pass

    @CodeBody.setter
    def CodeBody(self,value):

        self._CodeBody=value

        pass


    @property
    def StartSpace(self):
        """
        对象的声明行所在字符前的空格（专为python准备）
        """

        return self._StartSpace

        pass

    @StartSpace.setter
    def StartSpace(self,value):

        self._StartSpace=value

        pass

    @property
    def StartLineNum(self):
        """
        对象的源代码声明行所在的位置
        """

        return self._StartLineNum

        pass

    @StartLineNum.setter
    def StartLineNum(self,value):

        self._StartLineNum=value

        pass



    @property
    def FunctionArgs(self):
        """
        对象的源代码类型的父对象
        """

        return self._FunctionArgs

        pass

    @FunctionArgs.setter
    def FunctionArgs(self,value):

        self._FunctionArgs=value

        pass

    @property
    def Changed(self):
        """
        对象的源代码是否有改变的标记
        """

        return self._Changed

        pass

    @Changed.setter
    def Changed(self,value):

        self._Changed=value

        pass
    pass#class SourceCode:

class ReflectedInfo(object):
    """
    反射对象的基本信息。
    """

    #_SourceCode=SourceCode()
    def __init__(self):
        super(ReflectedInfo,self).__init__()
        self._SourceCode=SourceCode()
        self._ProceedCodeList=[]
        self._NvwaObjectDefinition=NvwaObjectDefinition()
        pass



    @property
    def SourceCode(self):
        """
        反射对象的源代码
        """
        # if self._SourceCode is None:#not "_SourceCode" in vars():
        #     self._SourceCode=SourceCode()
        return self._SourceCode

        pass

    # @SourceCode.setter
    # def SourceCode(self,value):
    #
    #     self._SourceCode=value
    #
    #     pass

    @property
    def ProceedCodeList(self):
        """
        反射后经处理的对象列表（包括：空白行、注释、Doc、类、函数等）
        """
        # if self._SourceCode is None:#not "_SourceCode" in vars():
        #     self._SourceCode=SourceCode()
        return self._ProceedCodeList

        pass

    # @ProceedCodeList.setter
    # def ProceedCodeList(self,value):
    #
    #     self._ProceedCodeList=value
    #
    #     pass

    @property
    def ReflectedType(self):
        """
        反射对象的类型定义
        """
        return self._ReflectedType

        pass

    @ReflectedType.setter
    def ReflectedType(self,value):

        self._ReflectedType=value

        pass

    @property
    def ParentInfo(self):
        """
        反射对象的父对象的信息定义
        """
        return self._ParentInfo

        pass

    @ParentInfo.setter
    def ParentInfo(self,value):

        self._ParentInfo=value

        pass
    @property
    def NvwaObjectDefinition(self):
        """
        反射对象包含的Nvwa对象的定义（在__doc__中以Xml形式存在）
        """

        if self._NvwaObjectDefinition is None:
            self._NvwaObjectDefinition=NvwaObjectDefinition()
        return self._NvwaObjectDefinition

        pass

    @NvwaObjectDefinition.setter
    def NvwaObjectDefinition(self,value):

        self._NvwaObjectDefinition=value

        pass

    @property
    def FileInfo(self):
        """
        当前module所在的文件信息
        """
        return self._FileInfo

    @FileInfo.setter
    def FileInfo(self,value):
        self._FileInfo=value


    @property
    def Docs(self):
        """
        当前反射类型的注释信息
        """
        return self._Docs

    @Docs.setter
    def Docs(self,value):
        self._Docs=value




    pass#class ReflectedInfo:

class ContainerInfo(ReflectedInfo):
    """
    具有子类、函数、实例化对象
    """

    def __init__(self):
        super(ContainerInfo,self).__init__()
        self._ImportedModules=ImportedModules()
        self._ChildClasses=ClassInfos()
        self._Functions=Functions()
        self._Instances=Instances()



        pass


    @property
    def ImportedModules(self):
        """
        反射出来的子Class列表
        :return:
        """
        if self._ImportedModules==None:
            self._ImportedModules=ImportedModules()
        return self._ImportedModules

    @ImportedModules.setter
    def ImportedModules(self,value):
        if value is None:
            self._ImportedModules=None
            return

        if not type(value) is type(ImportedModules):
            raise TypeError(u'The type of Imported Modules must be ImportedModules!')
        self._ImportedModules=value


    @property
    def ChildClasses(self):
        """
        反射出来的子Class列表
        :return:
        """
        if self._ChildClasses==None:
            self._ChildClasses=ClassInfos()
        return self._ChildClasses

    @ChildClasses.setter
    def ChildClasses(self,value):
        if value is None:
            self._ChildClasses=None
            return

        if not type(value) is type(ClassInfos):
            raise TypeError(u'The type of ChildClasses must be ClassInfos!')
        self._ChildClasses=value

    @property
    def Functions(self):
        """
        反射出来的Function列表
        :return:
        """
        if self._Functions==None:
            self._Functions=Functions()
        return self._Functions

    @Functions.setter
    def Functions(self,value):
        if value is None:
            self._Functions=None
            return

        if not type(value) is type(Functions):
            raise TypeError(u'The type of Functions must be Functions!')
        self._Functions=value


    @property
    def Instances(self):
        """
        反射出来的Instance列表
        :return:
        """
        if self._Instances==None:
            self._Instances=Instances()
        return self._Instances

    @Instances.setter
    def Instances(self,value):
        if value is None:
            self._Instances=None
            return

        if not type(value) is type(Instances):
            raise TypeError(u'The type of Instances must be Instances!')
        self._Instances=value




    pass#class ContainerInfo(ReflectedInfo):

class ModuleInfo(ContainerInfo):
    """
    模块对象的转换结构定义。
    """

    pass#class ModuleInfo()

class ClassInfo(ContainerInfo):
    """
    反射出的类（包括NvwaObjectFefinition）
    """

    def __init__(self):
        super(ClassInfo,self).__init__()
        self._Propertites=Propertites()

        pass


    @property
    def Propertites(self):
        """
        反射出来的属性列表
        :return:
        """
        if self._Propertites==None:
            self._Propertites=Propertites()
        return self._Propertites

    @Propertites.setter
    def Propertites(self,value):
        if value is None:
            self._Propertites=None
            return

        if not type(value) is type(Propertites):
            raise TypeError(u'The type of Propertites must be PropertyInfo list!')
        self._Propertites=value

    pass#class ClassInfo(ReflectedInfo):

class ImportedModules(list):
    """
    当前模块或类、属性、函数中引用的module
    """
    def __add__(self, other):
        if not isinstance(other,ImportedModules):
            raise TypeError(u'The type of item must be Imported Module list!')
        list.__add__(self,other)
        pass

    def append(self, p_object):
        if not type(p_object) is types.ModuleType:
            raise TypeError(u'The type of item must be ModuleType!')
        list.append(self,p_object)
        pass

    pass#class ImportedModules(list):

class ClassInfos(list):
    """
    反射出的类的列表（包括NvwaObjectFefinition）
    """
    def __add__(self, other):
        if not isinstance(other,ClassInfos):
            raise TypeError(u'The type of item must be ClassInfo list!')
        list.__add__(self,other)
        pass

    def append(self, p_object):
        if not isinstance(p_object,ClassInfo):
            raise TypeError(u'The type of item must be ClassInfo!')
        list.append(self,p_object)
        pass

    pass#class ClassInfos(list):

class PropertyInfo(ReflectedInfo):
    """
    属性的反射信息。
    """

    def __init__(self):
        self._ImportedModules=ImportedModules()
        pass


    @property
    def ImportedModules(self):
        """
        反射出来的子Class列表
        :return:
        """
        if self._ImportedModules==None:
            self._ImportedModules=ImportedModules()
        return self._ImportedModules

    @ImportedModules.setter
    def ImportedModules(self,value):
        if value is None:
            self._ImportedModules=None
            return

        if not isinstance(value,ImportedModules):
            raise TypeError(u'The type of Imported Modules must be ImportedModules!')
        self._ImportedModules=value


    pass#class PropertyInfo(ReflectedInfo):

class Propertites(list):
    """
    反射出的类的列表（包括NvwaObjectFefinition）
    """
    def __add__(self, other):
        if not isinstance(other,Propertites):
            raise TypeError(u'The type of item must be PropertyInfo list!')
        list.__add__(self,other)
        pass

    def append(self, p_object):
        if not isinstance(p_object,PropertyInfo):
            raise TypeError(u'The type of item must be PropertyInfo!')
        list.append(self,p_object)
        pass

    pass#class Propertites(list):

class FunctionInfo(ReflectedInfo):
    """
    函数的反射信息。
    """
    def __init__(self):
        self._ImportedModules=ImportedModules()
        pass


    @property
    def ImportedModules(self):
        """
        反射出来的子Class列表
        :return:
        """
        if self._ImportedModules==None:
            self._ImportedModules=ImportedModules()
        return self._ImportedModules

    @ImportedModules.setter
    def ImportedModules(self,value):
        if value is None:
            self._ImportedModules=None
            return

        if not isinstance(value,ImportedModules):
            raise TypeError(u'The type of Imported Modules must be ImportedModules!')
        self._ImportedModules=value


    pass#class FunctionInfo(ReflectedInfo):

class Functions(list):
    """
    反射出的函数的列表（包括NvwaObjectFefinition）
    """
    def __add__(self, other):
        if not isinstance(other,Functions):
            raise TypeError(u'The type of item must be FunctionInfo list!')
        list.__add__(self,other)
        pass

    def append(self, p_object):
        if not isinstance(p_object,FunctionInfo):
            raise TypeError(u'The type of item must be FunctionInfo!')
        list.append(self,p_object)
        pass

    pass#class Functions(list):

class InstanceInfo(ReflectedInfo):
    """
    实例的反射信息。
    """
    pass#class InstanceInfo(ReflectedInfo):

class Instances(list):
    """
    反射出的实例的列表（包括NvwaObjectFefinition）
    """
    def __add__(self, other):
        if not isinstance(other,Instances):
            raise TypeError(u'The type of item must be InstanceInfo list!')
        list.__add__(self,other)
        pass

    def append(self, p_object):
        if not isinstance(p_object,InstanceInfo):
            raise TypeError(u'The type of item must be InstanceInfo!')
        list.append(self,p_object)
        pass

    pass#class Instances(list):

class FileInfo:
    """
    文件的相关信息
    """

    #文件的绝对路径
    FilePath=''

    # #文件中的字符串
    # Text=''

    #文件的各行的字符串
    Mutilines=None

    # #编译完成的程序集（Python为Module，Java为jar？）
    # Assembly=None


    pass#class FileInfo:

class DocInfo(ReflectedInfo):
    """
    注释部分的代码信息
    """
    pass#class DocInfo(ReflectedInfo):


class NvwaObjectsCodeConvertor(object):
    """
    代码(包括python，c#，vb，java等)与Nvwa对象的转换器。
    """

    NvwaObjectTagPattern='<NvwaObject>.*</NvwaObject>'
    IDTagPattern='<id>.*</id>'
    ObjectTypeTagPattern='<ObjectType>.*</ObjectType>'
    RelationTagPattern='<Relation>.*</Relation>'
    MetaDataTagPattern='<MetaData>.*</MetaData>'

    importAsPattern='import .* as *.'
    fromImportPattern='from .* import *.'
    classPattern='class .*:'
    functionPattern='def .*:'
    propertyGetterPattern='@property .*'
    propertySetterPattern='@.*\.setter .*'

    @staticmethod
    def convertFileToNvwaObjects(filePath, codeType='py', shouldCover=True):
        """
        将文件中的代码转换成Nvwa对象。
        :rawParam filePath: 文件的地址
        :rawParam codeType: 代码类型（包括python，c#，vb，java等）
        :rawParam shouldCover: 是否覆盖以前的（默认为是）
        :return:返回转换后的代码
        """
        _fileInfo=FileInfo()


        if stringHelper.isStringNullOrEmpty(filePath):  # 判断文件路径（字符串）是否为空
            return
        with open(filePath, 'r') as f:  # 打开文件
            _fileInfo.Mutilines=f.readlines()# 读取代码（多行字符串）
            print (_fileInfo.Mutilines)
            # _fileInfo.Text = _fileInfo.Mutilines.decode('utf-8')
            # print '_fileInfo.Text:',_fileInfo.Text
            if not _fileInfo.Mutilines or len(_fileInfo.Mutilines)==0:
                return None

            _fileInfo.FilePath=filePath


            pass#with open(filePath, 'r') as f:  # 打开文件

            return NvwaObjectsCodeConvertor.convertCodeToNvwaObjects(_fileInfo, codeType, shouldCover)
        pass#def convertFileToNvwaObjects(filePath, codeType='py', shouldCover=True):

    @staticmethod
    def convertCodeToNvwaObjects(fileInfo, codeType='py', shouldCover=True):
        """
        将代码转换成Nvwa对象。
        :rawParam fileInfo: 代码文件的全部信息.
        :rawParam codeType: 代码类型（包括python，c#，vb，java等）
        :rawParam shouldCover: 是否覆盖以前的（默认为是）
        :return:返回转换后的代码
        """
        codeType=codeType.lower()

        if codeType == 'py' or codeType == 'python':
            return NvwaObjectsCodeConvertor.convertPyFileToNvwaObjects(fileInfo, shouldCover)
        elif codeType == 'c#' or codeType == 'csharp'or codeType == 'c#.net':
            pass
        elif codeType == 'vb' or codeType == 'vbnet' or codeType == 'vb.net':
            pass
        elif codeType == 'java':
            pass

        elif codeType == 'js':
            pass
        else:
            raise TypeError('unexpected fileInfo type!you can only convert python，c#，vb，java fileInfo to Nvwa Object(s)!')
            pass

        pass #def convertCodeToNvwaObjects(fileInfo, codeType='py', shouldCover=True):


    @staticmethod
    def IsFileInfoEffective(fileInfo):
        """
        判断一个fileInfo是否含有有效信息。
        :rawParam fileInfo:
        :return:
        """
        if fileInfo is None:
            return False

        if not isinstance(fileInfo,FileInfo):
            return False

        if stringHelper.isStringNullOrEmpty(fileInfo.FilePath):  # 判断代码（字符串）是否为空
            return False

        if not fileInfo.Mutilines or len(fileInfo.Mutilines)==0:  # 判断代码（字符串）是否为空
            return False

        return True

        pass#def IsFileInfoEffective(fileInfo):



    @staticmethod
    def convertPyFileToNvwaObjects(fileInfo, shouldCover=True):
        """
        将python文件中的代码转换成Nvwa对象。
        :rawParam fileInfo: python代码所在的文件的相关信息.
        :rawParam shouldCover: 是否覆盖以前的（默认为是）
        :return:返回转换后的代码
        """
        if not NvwaObjectsCodeConvertor.IsFileInfoEffective(fileInfo):  # 判断代码（字符串）是否为空
             return None

        # if not os.path.isfile(fileInfo) :
        #     a=os.path.abspath(fileInfo)#.decode('utf-8')
        #     t=os.path.isfile(a)
        #     if not os.path.isfile(a) :
        #         return

        fileName=os.path.basename(fileInfo.FilePath)
        #取得从代码加载的Module
        aMod= imp.load_source(fileName,fileInfo.FilePath)

        #这里验证是否是合法的
        if aMod is None:
            return None
        print(aMod)

        aModuleInfo=ModuleInfo()
        #aModuleInfo.__init__()
        aModuleInfo.ParentInfo=None
        aModuleInfo.FileInfo=fileInfo
        aModuleInfo.ReflectedType=aMod

        #取得文件中的代码中的相关信息
        aModuleInfo.SourceCode.CodeType='py'
        aModuleInfo.SourceCode.TypeType=types.ModuleType
        aModuleInfo.SourceCode.TypeName=fileName
        aModuleInfo.SourceCode.Decleration=None
        aModuleInfo.SourceCode.CodeBody=fileInfo.Mutilines
        aModuleInfo.SourceCode.StartSpace=''

        NvwaObjectsCodeConvertor.FillDefinitionWithPySourceCode(aModuleInfo)

        pass #def convertPyFileToNvwaObjects(fileInfo, shouldCover=True):

    @staticmethod
    def FillDefinitionWithPyReflection(reflectedType,reflectedInfo):
        """
        根据反射信息（优先根据其XmlDoc定义）来填充（创建）女娲对象的结构定义
        :rawParam reflectedType: 当前反射的类型（优先根据其XmlDoc定义）
        :rawParam reflectedInfo: 当前对象的结构信息
        :return:
        """

        print 'reflectedType:',reflectedType#.__class__
        #print type(reflectedType) is types.ModuleType
        #
        # if (not isinstance(reflectedType,type)) and (not type(reflectedType) is types.ModuleType):
        #     #print 'TypeError reflectedType:',reflectedType.__name__
        #     raise TypeError(u'reflectedType must be a type!')

        if not isinstance(reflectedInfo,ReflectedInfo):
            raise TypeError(u'Argument reflectedInfo must be a reflectedInfo!')


        #取得模块中定义的类
        for tempName in dir(reflectedType):

            aType= getattr(reflectedType, tempName)
            # print "aType name is:",tempName
            # print "aType is:",aType
            # print 'type(aType):',type(aType)
            # print 'type(aType) is object:',type(aType) is type(object)
            # print 'type(aType) is ClassType:',type(aType) is types.ClassType

            #下面分别处理：Class、Property、Function、实例等类型
            if type(aType) is types.ClassType or str(aType).startswith('<class'):#type(aType) is types.TypeType:#处理Class类型

                # if not str(aType).startswith('<class'):
                #     print aType,u' is not a class!'
                #     continue

                _classInfo=ClassInfo()
                _classInfo.ParentInfo=reflectedInfo
                #根据Type中的__doc__取得NvwaObject
                aNvwaObject=NvwaObjectsCodeConvertor.GetNvwaObjectByXmlDocInType(aType)

                _classInfo.NvwaObjectDefinition=aNvwaObject#这里可能没取到（没有__doc__或__doc__中没有NvwaObject定义）

                #递归处理子Class、Property、Function、实例等类型
                NvwaObjectsCodeConvertor.FillDefinitionWithPyReflection(aType,_classInfo)

                reflectedInfo.ChildClasses.append(_classInfo)

                pass
            elif type(aType) is property:#处理Property类型

                _propertyInfo=PropertyInfo()
                _propertyInfo.ParentInfo=reflectedInfo
                _propertyInfo.ReflectedType=aType
                _propertyInfo.SourceCode=NvwaObjectsCodeConvertor.GetSourceCode(reflectedInfo.SourceCode,tempName,'property')
                #根据Type中的__doc__取得NvwaObject
                aNvwaObject=NvwaObjectsCodeConvertor.GetNvwaObjectByXmlDocInType(aType)

                _propertyInfo.NvwaObjectDefinition=aNvwaObject#这里可能没取到（没有__doc__或__doc__中没有NvwaObject定义）


                #递归处理子Class、Property、Function、实例等类型
                NvwaObjectsCodeConvertor.FillDefinitionWithPyReflection(aType,_propertyInfo)

                reflectedInfo.Propertites.append(_propertyInfo)


                pass

            elif type(aType) is types.FunctionType or type(aType) is types.MethodType:#处理：Class、Property、Function、实例等类型

                _functionInfo=FunctionInfo()
                _functionInfo.ParentInfo=reflectedInfo
                #根据Type中的__doc__取得NvwaObject
                aNvwaObject=NvwaObjectsCodeConvertor.GetNvwaObjectByXmlDocInType(aType)
                code=aType.__code__
                print (str(code))
                print (dir(code))
                print (code.co_code.encode('utf-8'))
                print (code.co_lnotab.encode('utf-8'))

                _functionInfo.NvwaObjectDefinition=aNvwaObject#这里可能没取到（没有__doc__或__doc__中没有NvwaObject定义）

                #递归处理子Class、Function、Function、实例等类型
                NvwaObjectsCodeConvertor.FillDefinitionWithPyReflection(aType,_functionInfo)

                reflectedInfo.Functions.append(_functionInfo)

                pass

            elif type(aType) is types.InstanceType:#处理：Class、Property、Function、实例等类型

                _instanceInfo=InstanceInfo()
                _instanceInfo.ParentInfo=reflectedInfo
                #根据Type中的__doc__取得NvwaObject
                aNvwaObject=NvwaObjectsCodeConvertor.GetNvwaObjectByXmlDocInType(aType)

                _instanceInfo.NvwaObjectDefinition=aNvwaObject#这里可能没取到（没有__doc__或__doc__中没有NvwaObject定义）

                # #递归处理子Class、Instance、Instance、实例等类型
                # NvwaObjectsCodeConvertor.FillDefinitionWithPyReflection(aType,_instanceInfo)

                reflectedInfo.Instances.append(_instanceInfo)

                pass
            elif type(aType) is types.ModuleType:#处理：Class、Property、Function、实例等类型
                pass

            else:
                print (u'未处理的类型名称为：%s'% tempName)
                print (u'未处理的类型：%s' % type(aType))





        for item in reflectedInfo.ChildClasses:
            print (item.NvwaObjectDefinitions)
                        #print aType,NvwaObjectTagMatch#[1]
                        #取得ID



        pass #def FillDefinitionWithPyReflection(reflectedType,Definition):


    @staticmethod
    def FillDefinitionWithPySourceCode(reflectedInfo, shouldCover=True):
        """
        将python文件中的代码转换成代码信息定义。
        :rawParam filePath: python代码所在的文件.
        :rawParam shouldCover: 是否覆盖以前的（默认为是）
        :return:返回转换后的代码信息定义
        """

        #i：行的计数器
        i=0
        _codeBody=reflectedInfo.SourceCode.CodeBody
        if not _codeBody:
            return

        while i < len(_codeBody):

            codeLine=_codeBody[i]
            #codeLine=''
            decoratorLine=None
            if i>0:
                decoratorLine=_codeBody[i-1]
            #这里需要将当前代码段的空格截取下去（不能使用replace！）
            _stripped=codeLine[len(reflectedInfo.SourceCode.StartSpace):]

            #1、处理空行（空白）
            if stringHelper.isStringNullOrEmpty(_stripped) or _stripped =='\n':#_stripped .isspace:
                #添加到总的经处理的代码流中（反射后经处理的对象列表（包括：空白行、注释、Doc、类、函数等））
                reflectedInfo.ProceedCodeList.append(codeLine)
                i+=1#增加行计数器，继续下一行代码
                continue

            #2、处理单行注释
            #todo 这里不仅应处理单行注释，而且应把注释作为下一句代码的说明
            if _stripped .startswith('#'):
                #添加到总的经处理的代码流中（反射后经处理的对象列表（包括：空白行、注释、Doc、类、函数等））
                reflectedInfo.ProceedCodeList.append(codeLine)
                i+=1#增加行计数器，继续下一行代码
                continue

            #3、处理多行注释（代码文档级）
            if _stripped .startswith('\'\'\'') :
                #往下查找
                _docBody= sourceCodeHelper.GetPyTypeBody(i+1,_codeBody,reflectedInfo.SourceCode.StartSpace,'','\'\'\'')
                if _docBody :
                    _docBody.insert(0,codeLine)
                    _docInfo=DocInfo()
                    _docInfo.SourceCode.CodeBody=_docBody
                    reflectedInfo.ProceedCodeList.append(_docInfo)
                    i+=_docBody.count() #增加行计数器，继续下一行代码
                continue


            #4、处理引入的模块
            if _stripped .startswith('import ') or _stripped .startswith ('from '):
                i,proceed=NvwaObjectsCodeConvertor.ProcessCodeDefinition(i,codeLine,reflectedInfo,decoratorLine,types.ModuleType)
                if proceed:
                    i+=1#增加行计数器，继续下一行代码
                    continue

                continue



            #5、处理类的定义
            if _stripped .startswith('class ') :
                i,proceed=NvwaObjectsCodeConvertor.ProcessCodeDefinition(i,codeLine,reflectedInfo,decoratorLine)
                if proceed:
                    i+=1#增加行计数器，继续下一行代码
                    continue

            # 6、处理函数（包括属性）的定义
            if _stripped .startswith('def ') :
                i,proceed=NvwaObjectsCodeConvertor.ProcessCodeDefinition(i,codeLine,reflectedInfo,decoratorLine,ReflectionType.FunctionType)
                if proceed:
                    i+=1#增加行计数器，继续下一行代码
                    continue

            # 7、处理实例（对象）的定义
            # NvwaObjectsCodeConvertor.ProcessClass(line)

            # 8、处理pass
            if _stripped .startswith('pass'):
                #添加到总的经处理的代码流中（反射后经处理的对象列表（包括：空白行、注释、Doc、类、函数等））
                reflectedInfo.ProceedCodeList.append(codeLine)
                i+=1#增加行计数器，继续下一行代码
                continue

            # 9、没有进行任何处理，应该为代码的逻辑部分（真实的代码/可执行的代码）。
            # _realCodeInfo=RealCodeInfo()
            # _realCodeInfo.
            #reflectedInfo.ProceedCodeList.append(_realCodeInfo )

            # 继续下一行代码
            i+=1

            pass#while i < len(_codeBody):



        pass#def FiPyllDefinitionWithSourceCode(filePath, shouldCover=True):

    @staticmethod
    def ProcessCodeDefinition(lineNum,declerationLine,parentReflectedInfo,decoratorLine,definitionType=ReflectionType.ClassType):

        # 将正则表达式编译成Pattern对象
        patternStr=None

        if definitionType==ReflectionType.ClassType:
            patternStr=NvwaObjectsCodeConvertor.classPattern
        elif definitionType==ReflectionType.FunctionType:
            patternStr=NvwaObjectsCodeConvertor.functionPattern

        pattern = re.compile(patternStr, re.S)
        # 使用Pattern匹配文本，获得匹配结果，无法匹配时将返回None
        matched = pattern.findall(declerationLine)
        #是否已经处理的标记
        proceed=False

        if matched:

            #处理代码层面的相关信息
            _typeName,_space,_inheritedFrom,_args= sourceCodeHelper.ResolvePyTypeDecleration(declerationLine)

            aType= getattr(parentReflectedInfo.ReflectedType, _typeName)
            if aType is None:
                s=u'无法在代码中取得对应的类型！代码为：%(code)s \n 类型为：%(type)s \n 请检查源代码！'
                s=s % {'code':parentReflectedInfo.SourceCode.CodeBody,'type':_typeName}
                raise ValueError(s)
                pass#if aType is None:

            #根据缩进取得代码体
            _codeBody= sourceCodeHelper.GetPyTypeBody(lineNum+1,parentReflectedInfo.SourceCode.CodeBody,_space)

            _typeInfo=ClassInfo()

            if definitionType==ReflectionType.FunctionType:
                _typeInfo=FunctionInfo()
            elif definitionType ==ReflectionType.PropertyType:
                _typeInfo=PropertyInfo()


            _typeInfo.SourceCode.CodeType='py'
            _typeInfo.SourceCode.TypeType=types.ClassType
            _typeInfo.SourceCode.TypeName=_typeName
            _typeInfo.SourceCode.Decleration=declerationLine
            _typeInfo.SourceCode.Decorator=decoratorLine
            _typeInfo.SourceCode.CodeBody=_codeBody
            _typeInfo.SourceCode.StartSpace=_space
            _typeInfo.SourceCode.StartLineNum=lineNum
            _nextLineNum=lineNum
            _nextLineNum +=len(_codeBody)#这里直接将行数调整到下一个声明

            if definitionType==ReflectionType.ClassType:
                _typeInfo.SourceCode.TypeInheritedFrom=_inheritedFrom
            elif definitionType==ReflectionType.FunctionType:
                _typeInfo.SourceCode.FunctionArgs=_args

            _typeInfo.ReflectedType=aType
            _typeInfo.ParentInfo=parentReflectedInfo

            # #处理反射层面的相关信息
            #
            # #根据Type中的__doc__取得NvwaObject
            # aNvwaObject,xmlStr=NvwaObjectsCodeConvertor.GetNvwaObjectByXmlDocInType(aType)
            #
            # #如果在Type中的__doc__未能取得NvwaObject，说明没有定义，或定义格式不对，这里分别处理
            # if aNvwaObject is None:
            #
            #     if StringHelper.IsStringNullOrEmpty(xmlStr):
            #         aNvwaObject=NvwaObjectsCodeConvertor.GetNvwaObjectByCodeDefinition
            #         pass
            #     else:
            #
            #         pass
            #
            #
            #     pass#if aNvwaObject is None:
            #
            # _typeInfo.NvwaObjectDefinition=aNvwaObject#这里可能没取到（没有__doc__或__doc__中没有NvwaObject定义）

            if definitionType==ReflectionType.ClassType:
                parentReflectedInfo.ChildClasses.append(_typeInfo)
            elif definitionType==ReflectionType.FunctionType:
                parentReflectedInfo.Functions.append(_typeInfo)
            elif definitionType==ReflectionType.PropertyType:
                parentReflectedInfo.Properties.append(_typeInfo)

            #继续处理_codeBody
            if _codeBody :
                NvwaObjectsCodeConvertor .FillDefinitionWithPySourceCode(_typeInfo)

            #添加到总的经处理的代码流中（反射后经处理的对象列表（包括：空白行、注释、Doc、类、函数等））
            parentReflectedInfo.ProceedCodeList.append(_typeInfo)

            #已经找到了类型，所以继续下一个代码段
            proceed=True
            return _nextLineNum,proceed

            pass #if matched:

        #未找到类型，所以只能返回当前循环
        return lineNum,proceed

        pass#def ProcessCodeDefinition(lineNum,declerationLine,parentReflectedInfo,decoratorLine,definitionType=types.ClassType):

    @staticmethod
    def GetNvwaObjectByCodeDefinition():
        pass#def GetNvwaObjectByCodeDefinition():


    @staticmethod
    def GetNvwaObjectByXmlDocInType(aType):
        """
        根据Type中的__doc__取得NvwaObject
        :rawParam aType:
        :return:
        """
        #取得注释
        _Doc=aType.__doc__

        aNvwaObject=NvwaObjectsCodeConvertor.GetNvwaObjectByXmlDoc(_Doc)
        aNvwaObject.ReflectedClass=aType

        return aNvwaObject

        pass#def GetNvwaObjectByXmlDocInType(aType):

    @staticmethod
    def GetNvwaObjectByXmlDoc(Doc):
        """
        根据注释取得NvwaObject
        :rawParam Doc:注释（字符串）
        :return:
        """

        aNvwaObject=None
        xmlStr=None

        #下面根据注释创建NvwaObjectDefinition，或是直接根据反射对象创建
        if not stringHelper.isStringNullOrEmpty(Doc):
            # 将正则表达式编译成Pattern对象
            pattern = re.compile(NvwaObjectsCodeConvertor.NvwaObjectTagPattern, re.S)
            # 使用Pattern匹配文本，获得匹配结果，无法匹配时将返回None
            NvwaObjectTagMatch = pattern.findall(Doc)
            if NvwaObjectTagMatch:
                xmlStr=NvwaObjectTagMatch[0]
                xmlDoc=minidom.parseString(xmlStr)#.decode('utf-8'))
                if xmlDoc:
                    docElement=xmlDoc.documentElement
                    if docElement:
                        aNvwaObject=NvwaObjectsCodeConvertor.convertXmlNodeToNvwaObject(docElement)

            pass#if NvwaObjectTagMatch:

        return aNvwaObject,xmlStr

        pass#def GetNvwaObjectByTypeDefinition(aType):

    @staticmethod
    def convertXmlNodeToNvwaObject(xmlNode):

        if xmlNode is None or not isinstance(xmlNode,minidom.Element):
            return None

        if xmlNode.localName!='NvwaObject':
            return None

        _NvwaObject=NvwaObjectDefinition()

        #print '_NvwaObject:',_NvwaObject


        for node in xmlNode.childNodes:

            nodeName=node.localName
            if nodeName==None or node.nodeType==3 or node.nodeValue==u'\n':#过滤掉空文本节点
                continue

            #取得标签之间的文本
            nodeText=None
            #print 'node.firstCMutiLineshild is minidom.Text:',isinstance(node.firsMutiLinestChild, minidom.Text)
            if isinstance(node.firstChild, minidom.Text):
                nodeText=node.firstChild.data
            if stringHelper.isStringNullOrEmpty(nodeText):
                continue


            if nodeName=='ID':
                _NvwaObject.ID=nodeText
            elif nodeName=='ObjectType':
                _NvwaObject.ObjectType=nodeText
            elif nodeName=='Relation':
                _NvwaObject.Relation=nodeText
            elif nodeName=='MetaData':
                _NvwaObject.MetaData=nodeText
            elif nodeName=='Position':
                _NvwaObject.Position=int(nodeText)
            elif nodeName=='Args':
                for childNode in node.childNodes:
                    childObj=NvwaObjectsCodeConvertor.convertXmlNodeToNvwaObject(childNode)
                    if childObj:
                        _NvwaObject.Args.__add__(childObj)

            elif nodeName=='Return':
                _NvwaObject.Return=nodeText
            elif nodeName=='Remark':
                _NvwaObject.Remark=nodeText
            else:
                raise ValueError(u'NvwaObject定义不支持的数据类型！')


        pass #for node in xmlNode.childNodes:

        return _NvwaObject


        pass #def convertXmlNodeToNvwaObject(self,xmlNode):

    pass #class NvwaObjectsCodeConvertor(object):

path='.\Test\SimpleClass.py'
#path='.\Test\nvwaObjectsCodeConvertorSingleClass.py'

NvwaObjectsCodeConvertor.convertFileToNvwaObjects(path)


