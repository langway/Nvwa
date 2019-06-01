#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon（梁冰）'
"""
创建日期：2015-09-03
"""

import loongtian.nvwa.models.enum as Common
from loongtian.util.helper import stringHelper
#from loongtian.Tools.NvwaObjectsCodeConvertor import StringHelper

class TestA:

    def FuncA(self):
        pass
    pass

class TestB():

    def FuncB(self):
        pass

    pass

class TestC(object):

    def FuncC(self):
        pass


    pass


class gender(Common.Enum):

    def __int__(self):
        self._slots__=('Male','Female')

    Male=0
    Female=1

    pass

# g=gender()
#
# print g.Male

SimpleStrInstance=''


class Substances(object):
    """
    这里是原来的注释，在处理时，需要忽略掉
    <NvwaObject>
        <id></id>
        <ObjectType>RealObject</ObjectType>
        <Relation></Relation>
        <MetaData>物体;substances</MetaData>
    </NvwaObject>
    这里是原来的注释，在处理时，需要忽略掉
    """

    #region "变量及参数定义   "
    _X=0
    _Y=0
    _Z=0

    #end region


    def __init__(self):

        pass


    @property
    def X(self):
        """
        <NvwaObject>
            <id></id>
            <ObjectType>RealObject</ObjectType>
            <Relation>属性</Relation>
            <MetaData>X轴的值;X Position</MetaData>
        </NvwaObject>
        :return:
        """
        return self._X

    @X.setter
    def X(self,value):
        self._X=value

    @property
    def Y(self):
        """
        <NvwaObject>
            <id></id>
            <ObjectType>RealObject</ObjectType>
            <Relation>属性</Relation>
            <MetaData>Y轴的值;Y Position</MetaData>
        </NvwaObject>
        :return:
        """
        return self._Y

    @Y.setter
    def Y(self,value):
        self._Y=value

    @property
    def Z(self):
        """
        <NvwaObject>
            <id></id>
            <ObjectType>RealObject</ObjectType>
            <Relation>属性</Relation>
            <MetaData>Z轴的值;Z Position</MetaData>
        </NvwaObject>
        :return:
        """
        return self._Z

    @Z.setter
    def Z(self,value):
        self._Z=value

    pass #class Substances




class Mouth(Substances):
    """
    <NvwaObject>
        <id></id>
        <ObjectType>RealObject</ObjectType>
        <Relation></Relation>
        <MetaData>嘴;mouth</MetaData>
    </NvwaObject>
    """
    #region "变量及参数定义   "
    _lowerLip=Substances()
    _upperLip=Substances()


    def __init__(self):
        pass


    @property
    def upperLip(self):
        """
        <NvwaObject>
            <id></id>
            <ObjectType>RealObject</ObjectType>
            <Relation>组件</Relation>
            <MetaData>上嘴唇;upperid lip</MetaData>
        </NvwaObject>
        :return:
        """
        if self._upperLip==None:
            self._upperLip=Substances()
            self._upperLip.Z=-400 #初始化为闭嘴状态
        if self._upperLip.Z<-400:
            self._upperLip.Z=-400#设置上嘴唇的最低状态
        if self._upperLip.Z>-300:
            self._upperLip.Z=-300#设置上嘴唇的最高状态

        return self._upperLip

    @upperLip.setter
    def upperLip(self,value):

        if value==None:
            value=Substances()
            value.Z=-400#初始化为闭嘴状态
        if value.Z<-400:
            value.Z=-400#设置上嘴唇的最低状态
        if value.Z>-300:
            value.Z=-300#设置上嘴唇的最高状态

        self._upperLip=value



    @property
    def lowerLip(self):
        """
        <NvwaObject>
            <id></id>
            <ObjectType>RealObject</ObjectType>
            <Relation>组件</Relation>
            <MetaData>下嘴唇;lowerid lip</MetaData>
        </NvwaObject>
        :return:
        """
        if self._lowerLip==None:
            self._lowerLip=Substances()
            self._lowerLip.Z=-400 #初始化为闭嘴状态
        if self._lowerLip.Z<-500:
            self._lowerLip.Z=-500#设置下嘴唇的最低状态
        if self._lowerLip.Z>-400:
            self._lowerLip.Z=-400#设置下嘴唇的最高状态

        return self._lowerLip

    @lowerLip.setter
    def lowerLip(self,value):

        if value==None:
            value=Substances()
            value.Z=-400#初始化为闭嘴状态
        if value.Z<-500:
            value.Z=-500#设置下嘴唇的最低状态
        if value.Z>-400:
            value.Z=-400#设置下嘴唇的最高状态

        self._lowerLip=value


    def Open(self):
        """
        <NvwaObject>
            <id></id>
            <ObjectType>Action</ObjectType>
            <Relation>能</Relation>
            <MetaData>张开;open</MetaData>
            <Position>-1</Position>
            <Remark>Position:用来存放与当前对象的位置关系，例如-1就是在当前对象前面(默认为1)</Remark>
        </NvwaObject>
        """

        if self.upperLip.Z<=-300 and self.upperLip.Z>=-400:
            self.upperLip.Z+=10
        else:
            raise TypeError(u'不能再张嘴了！')

        if self.lowerLip.Z<=-400 and self.lowerLip.Z>=-500:
            self.lowerLip.Z-=10
        else:
            raise TypeError(u'不能再张嘴了！')

    def Close(self):
        """
        <NvwaObject>
            <id></id>
            <ObjectType>Action</ObjectType>
            <Relation>能</Relation>
            <MetaData>闭上;close</MetaData>
            <Position>-1</Position>
            <Remark>Position:用来存放与当前对象的位置关系，例如-1就是在当前对象前面(默认为1)</Remark>
        </NvwaObject>
        """

        if self.upperLip.Z<=-300 and self.upperLip.Z>=-400:
            self.upperLip.Z-=10
        else:
            raise TypeError(u'不能再闭嘴了！')

        if self.lowerLip.Z<=-400 and self.lowerLip.Z>=-500:
            self.lowerLip.Z+=10
        else:
            raise TypeError(u'不能再闭嘴了！')



class Person(Substances):
    """
    <NvwaObject>
        <id></id>
        <ObjectType>RealObject</ObjectType>
        <Relation></Relation>
        <MetaData>人;person</MetaData>
    </NvwaObject>
    """
    #region "变量及参数定义   "
    _name=''
    _gender=None
    _age=0

    _knowledges=None
    _Mouth=Mouth()

    def __init__(self):
        __slots__=('name','gender','age')
        pass

    #这里用来测试类是否能够拥有子类
    class classChildClass:
        pass

    @property
    def name(self):
        """
        <NvwaObject>
            <id></id>
            <ObjectType>RealObject</ObjectType>
            <Relation>属性</Relation>
            <MetaData>姓名;name</MetaData>
        </NvwaObject>
        :return:
        """

        return self._name

    @name.setter
    def name(self,value):
        if not isinstance(value,str):
            raise TypeError(u'string type value is needed!')
        else:
            self._name=value

    @property
    def gender(self):
        """
        <NvwaObject>
            <id></id>
            <ObjectType>RealObject</ObjectType>
            <Relation>属性</Relation>
            <MetaData>性别;gender</MetaData>
        </NvwaObject>
        :return:
        """
        #这里用来测试属性是否能够拥有子类
        class genderChildClass:
            pass

        return self._gender

    @gender.setter
    def gender(self,value):
        if not isinstance(value,gender) :
            raise TypeError(u'The type of scores must be gender!')
        self._gender=value


    @property
    def age(self):
        """
        <NvwaObject>
            <id></id>
            <ObjectType>RealObject</ObjectType>
            <Relation>属性</Relation>
            <MetaData>年龄;age</MetaData>
        </NvwaObject>
        :return:
        """
        return self._age

    @age.setter
    def age(self,value):
        if not isinstance(value,int) :
            raise TypeError(u'The type of age must be integer!')
        self._age=value

    @property
    def knowledges(self):
        """
        <NvwaObject>
            <id></id>
            <ObjectType>RealObject</ObjectType>
            <Relation></Relation>
            <MetaData>知识;knowledges</MetaData>
        </NvwaObject>
        :return:
        """
        if self._knowledges==None:
            self._knowledges=[]

        return self._knowledges

    @knowledges.setter
    def knowledges(self,value):
        if self.value==None:
            self.value=[]

        self._knowledges=value



    @property
    def Mouth(self):
        """
        <NvwaObject>
            <id></id>
            <ObjectType>RealObject</ObjectType>
            <Relation>组件</Relation>
            <MetaData>嘴;mouth</MetaData>
        </NvwaObject>
        :return:
        """
        if self._Mouth is None:
            self._Mouth=Mouth()

        return self._Mouth

    @Mouth.setter
    def Mouth(self,value):
        if not isinstance(value,Mouth) :
            raise TypeError(u'The type of age must be integer!')
        self._Mouth=value

    def Speak(self,content):
        """
        <NvwaObject>
            <id></id>
            <ObjectType>Action</ObjectType>
            <Relation>动作</Relation>
            <MetaData>说;speak</MetaData>
            <Position>1</Position>
            <Args>
                <NvwaObject>
                    <id></id>
                    <ObjectType>RealObject</ObjectType>
                    <Relation></Relation>
                    <Position>2</Position>
                    <MetaData>内容;content</MetaData>
                </NvwaObject>
            </Args>
            <Return></Return>
            <Remark>Position:用来存放与当前对象的位置关系，例如-1就是在当前对象前面(默认为1)</Remark>
        </NvwaObject>
        """
        # if not isinstance(content,str) :
        #     raise TypeError(u'The type of content must be string!')

        #初始化为闭嘴
        self.Mouth.lowerLip.Z=-400
        self.Mouth.upperLip.Z=-400

        i=11

        #这里用来测试函数是否能够拥有子类
        class speakChildClass:
            pass

        #张嘴闭嘴10次
        while i>0:
            i-=1
            self.Mouth.Open()
            self.Mouth.Close()

        print (self.name+'说：'+content.encode('utf-8'))

    def Walk(self,distance):
        """
        <NvwaObject>
            <id></id>
            <ObjectType>Action</ObjectType>
            <Relation>动作</Relation>
            <MetaData>走;walk</MetaData>
            <Position>1</Position>
            <Args>
                <NvwaObject>
                    <id></id>
                    <ObjectType>RealObject</ObjectType>
                    <Relation></Relation>
                    <Position>2</Position>
                    <MetaData>距离;distance</MetaData>
                    <Todo>目前还是个数值（int）类型</Todo>
                </NvwaObject>
            </Args>
            <Remark>Position:用来存放与当前对象的位置关系，例如-1就是在当前对象前面(默认为1)
                    Arg:应该天然继承里面创建的RealObject对象及Anything
            </Remark>
        </NvwaObject>
        """
        self.Y+=distance

    def Jump(self,distance):
        """
        <NvwaObject>
            <id></id>
            <ObjectType>Action</ObjectType>
            <Relation>动作</Relation>
            <MetaData>跳;jump</MetaData>
            <Position>1</Position>
            <Args>
                <NvwaObject>
                    <id></id>
                    <ObjectType>RealObject</ObjectType>
                    <Relation></Relation>
                    <Position>2</Position>
                    <MetaData>距离;distance</MetaData>
                    <Todo>目前还是个数值（int）类型</Todo>
                </NvwaObject>
            </Args>
            <Remark>Position:用来存放与当前对象的位置关系，例如-1就是在当前对象前面(默认为1)
                    Arg:应该天然继承里面创建的RealObject对象及Anything
            </Remark>
        </NvwaObject>
        """
        self.Z+=distance

    def Sway(self,distance):
        """
        <NvwaObject>
            <id></id>
            <ObjectType>Action</ObjectType>
            <Relation>动作</Relation>
            <MetaData>横挪;sway</MetaData>
            <Position>1</Position>
            <Args>
                <NvwaObject>
                    <id></id>
                    <ObjectType>RealObject</ObjectType>
                    <Relation></Relation>
                    <Position>2</Position>
                    <MetaData>距离;distance</MetaData>
                    <Todo>目前还是个数值（int）类型</Todo>
                </NvwaObject>
            </Args>
            <Remark>Position:用来存放与当前对象的位置关系，例如-1就是在当前对象前面(默认为1)
                    Arg:应该天然继承里面创建的RealObject对象及Anything
            </Remark>
        </NvwaObject>
        """
        self.X+=distance



    pass  #class Person

class Student(Person):
    """
    <NvwaObject>
        <id>ce7d89da-a696-413e-85bf-bc4955ad5383</id>
        <ObjectType>RealObject</ObjectType><Relation></Relation>
        <MetaData>学生;student</MetaData>
    </NvwaObject>
    """

    #region "变量及参数定义   "
    _id=None
    _class=None
    _scores={}
    #end region


    def __init__(self):

        __slots__=('idInt','class','scores')
        # self._gender=gender().Female
        # self._gender.

    @property
    def id(self):
        """
        <NvwaObject>
            <id></id>
            <ObjectType>RealObject</ObjectType><Relation></Relation>
            <MetaData>学号;student idInt</MetaData>
        </NvwaObject>
        :return:
        """
        return self._id

    @id.setter
    def id(self,value):
        self._id=value



    @property
    def Class(self):
        """
        <NvwaObject>
            <id></id>
            <ObjectType>RealObject</ObjectType><Relation></Relation>
            <MetaData>班级;class</MetaData>
        </NvwaObject>
        :return:
        """
        return self._class

    @Class.setter
    def Class(self,value):
        self._class=value



    @property
    def scores(self):
        """
        <NvwaObject>
            <id></id>
            <ObjectType>RealObject</ObjectType><Relation></Relation>
            <MetaData>成绩;scores</MetaData>
        </NvwaObject>
        :return:
        """
        if self._scores==None:
            self._scores={}

        return self._scores

    @scores.setter
    def scores(self, value):
        if value==None:
            value={}

        if not isinstance(value, dict):
            raise ValueError('The type of scores must be dictionary!')
        self._scores = value


    @property
    def TotalScore(self):
        """
        <NvwaObject>
            <id></id>
            <ObjectType>RealObject</ObjectType><Relation></Relation>
            <MetaData>总成绩;Total Score</MetaData>
        </NvwaObject>
        :return:
        """
        total=0
        for k,v in self.scores:
            total+=v
        return total

        pass

    def Learn(self,content):
        """
        <NvwaObject>
            <id></id>
            <ObjectType>Action</ObjectType>
            <Relation>动作</Relation>
            <MetaData>学习;learn</MetaData>
            <Position>1</Position>
            <Args>
                <NvwaObject>
                    <id></id>
                    <ObjectType>RealObject</ObjectType>
                    <Relation></Relation>
                    <Position>2</Position>
                    <MetaData>内容;content</MetaData>
                </NvwaObject>
            </Args>
            <Return></Return>
            <Remark>Position:用来存放与当前对象的位置关系，例如-1就是在当前对象前面(默认为1)</Remark>
        </NvwaObject>
        """

        if stringHelper.isStringNullOrEmpty(content):
            raise ValueError(u'你总得告诉我点什么吧！')

        self.knowledges.append(content)

        return u'我知道'+content +u'了！'




    pass



Smile=Student()

Smile.name='笑笑'

Smile.Speak(u'爸爸，你好！')

def TestFunc():
    pass


# class Student2(object):
#
#     #_birth=2000
#
#     @property
#     def birth(self):
#         if self._birth==None:
#             self._birth=2000
#         return self._birth
#
#     @birth.setter
#     def birth(self, value):
#         self._birth = value
#
#     @property
#     def age(self):
#         return 2014 - self._birth
#
#
# s=Student2()
#
# print s.birth
#
# print s.age
# s.birth=2220
#
# print s.age
