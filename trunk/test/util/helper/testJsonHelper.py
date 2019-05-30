#!/usr/bin/env python
#coding=utf8
"""
an Simple example for lib https://github.com/hustcc/object2json

@author: hzwangzhiwei
@contact: http://50vip.com/
Created on 2014年11月12日
@modification： js   2015-11-27

今天写代码遇到一个问题，就是对象变成json，开始使用字符串模版变换对象中的各个属性，后来遇到一个问题：
就是在对象某一个字段中放另外一个对象（obj，字典，数组）的时候，会导致转成的JSON不是我想要的！找了各种办法，效果总是差一点点，蛋碎了，于是tm自己写了一个！
使用的递归算法！

另外，py代码写的不多，放到git上，希望大家不要喷~~~

代码见：https://github.com/hustcc/object2json
"""
import time
import json
from unittest import TestCase
import sys
import loongtian.util.helper.jsonHelper as JsonHelper
from loongtian.util.helper import stringHelper


class TestJsonHelper(TestCase):
    def setUp(self):
        print("----setUp----")


    def testOthers(self):
        print("----testOthers----")
        # import importlib,sys
        # importlib.reload(sys)
        # sys.setdefaultencoding('utf-8')
        ttt = 'asd中国是我家！'
        print('type(\'asd中国是我家！\'):',type(ttt))
        ttt=unicode(ttt)
        print('type(unicode(\'asd中国是我家！\'))',type(ttt))
        ttt=ttt.encode('utf-8')
        print('type(unicode(\'asd中国是我家！\').encode(\'utf-8\'))',type(ttt))
        print('\u6211\u662f\u4e2d\u56fd\u4eba decode raw_unicode_escape:',('\u6211\u662f\u4e2d\u56fd\u4eba').decode('raw_unicode_escape'))


    def testObj2json(self):
        print("----testObj2json----")
        l = 1.12
        j = JsonHelper .obj2json(l)
        print('float 1.12:',j)
        l = '1.12'
        j = JsonHelper .obj2json(l)
        print('string 1.12:',j)
        l='中文'
        j = JsonHelper .obj2json(l)
        print('string 中文:',j)
        l=u'中文unicode'
        j=JsonHelper .obj2json(l)
        print('unicode string 中文unicode:',j)
        l=['q', 'w', 'e']
        j=JsonHelper .obj2json(l)
        print('[\'q\',\'w\',\'e\']:',j)
        l=['q',1.12,u'abc',set([5,67])]
        j=JsonHelper .obj2json(l)
        print('[\'q\',1.12,u\'abc\',set([5,67])]:',j)
        j=str(l)
        print('[\'q\',1.12,u\'abc\',set([5,67])]:',j)
        l={'a':234,u'中文键值':('q','w','e'),u'中文键值2':'asd中国是我家！'}
        try:
            print('l[\'中文键值\']:',l[u'中文键值'])
        except  Exception as e:
            print('l[\'中文键值\'] Exception:',e)
        j=JsonHelper .obj2json(l)
        print('Dict l={\'a\':234,u\'中文键值\':(\'q\',\'w\',\'e\')}:',j)
        msg = Msg()
        print(type(msg.recordTime ))
        msg.ext2 = Msg() #object
        #print(json.dumps(msg)#这一句将执行不了：TypeError: <__main__.Msg object at 0x0000000002985EF0> is not JSON serializable
        print('——lambda——')
        try:
            print('json.dumps(msg, default=lambda o: o.__dict__):',json.dumps(msg, default=lambda o: o.__dict__))
        except AttributeError as e:
            print('AttributeError:',e)
        print('——end lambda——')
        j= JsonHelper.obj2json(None,True)
        print('JsonHelper.obj2json(None,True):',j)
        j= JsonHelper.obj2json(msg.extNone,True)
        print('JsonHelper.obj2json(msg.extNone,True):',j)
        print('dir(msg.extNone):',dir(msg.extNone))
        print('msg.extNone.__format__:',msg.extNone.__format__)
        j= JsonHelper.obj2json(msg,True)
        print(type(j))
        print('JsonHelper.obj2json(msg,True):',j)


    def testJson2obj(self):
        print("----testJson2obj----")
        l=1.12
        j=JsonHelper .obj2json(l)
        rebuiltedObj=JsonHelper .json2obj(j)
        print('rebuiltedObj float 1.12:', rebuiltedObj)
        print('rebuiltedObj type of float 1.12:', type(rebuiltedObj))
        #(已解决) 数字式字符串被转成了数字，这里怎么处理？！
        l = '1.12'
        j = JsonHelper .obj2json(l)
        rebuiltedObj = JsonHelper.json2obj(j)
        print('rebuiltedObj string 1.12:', rebuiltedObj)
        print('rebuiltedObj type of string 1.12:', type(rebuiltedObj))
        l = '中文'
        j = JsonHelper .obj2json(l)
        rebuiltedObj = JsonHelper .json2obj(j.decode('utf-8'))  # ???此处传人值编码为utf-8是，在方法内在进行encode（'utf-8')报错
        print('rebuiltedObj string 中文:', rebuiltedObj)
        print('rebuiltedObj type of string 中文:', type(rebuiltedObj))
        l=u'中文unicode'
        j=JsonHelper .obj2json(l)
        rebuiltedObj=JsonHelper .json2obj(j)
        print('rebuiltedObj unicode string 中文unicode:',rebuiltedObj)
        print('rebuiltedObj type of unicode string 中文unicode:',type(rebuiltedObj))
        l=['q', 'w', 'e']
        j=JsonHelper .obj2json(l)
        rebuiltedObj=JsonHelper .json2obj(j)
        print('rebuiltedObj [\'q\',\'w\',\'e\']:',rebuiltedObj)
        print('rebuiltedObj type of [\'q\',\'w\',\'e\']:',type(rebuiltedObj))
        l=['q',1.12,u'abc',set([5,67])]
        j=JsonHelper .obj2json(l)
        rebuiltedObj=JsonHelper .json2obj(j)
        print('rebuiltedObj [\'q\',1.12,u\'abc\',set([5,67])]:',rebuiltedObj)
        print('rebuiltedObj type of [\'q\',1.12,u\'abc\',set([5,67])]:',type(rebuiltedObj))
        l={'a':234,u'中文键值':('q','w','e'),u'中文键值2':'asd中国是我家！'}
        j=JsonHelper .obj2json(l)
        rebuiltedObj=JsonHelper .json2obj(j)
        print('rebuiltedObj Dict l={\'a\':234,u\'中文键值\':(\'q\',\'w\',\'e\')}::',rebuiltedObj)
        print('rebuiltedObj type of Dict l={\'a\':234,u\'中文键值\':(\'q\',\'w\',\'e\')}::',type(rebuiltedObj))
        msg = Msg()
        msg.ext2 = Msg() #object
        j= JsonHelper.obj2json(None,True)
        j= JsonHelper.obj2json(msg.extNone,True)
        rebuiltedObj=JsonHelper .json2obj(j)
        print('rebuiltedObj NoneType:',rebuiltedObj)
        print('rebuiltedObj type of NoneType:',type(rebuiltedObj))

        j= JsonHelper.obj2json(msg,True)
        print(type(j))
        print('JsonHelper.obj2json(msg,True):',j)
        j=j.replace(stringHelper.converStringToUnicode(u'我是中国人'), stringHelper.converStringToUnicode(u'日本人不是人！'))
        print('\u6211\u662f\u4e2d\u56fd\u4eba decode raw_unicode_escape:',('\u6211\u662f\u4e2d\u56fd\u4eba').decode('raw_unicode_escape'))
        print(j)
        rebuiltedObj=JsonHelper.json2obj(j)
        print(rebuiltedObj)
        print('rebuiltedObj.idInt:',rebuiltedObj.idInt)
        print('type(o.idInt):',type(rebuiltedObj.idInt))
        print('rebuiltedObj.numFloat:',rebuiltedObj.numFloat)
        print('type(o.numFloat):',type(rebuiltedObj.numFloat))
        print('rebuiltedObj.senderStr:',rebuiltedObj.senderStr)
        print('type(rebuiltedObj.senderStr):',type(rebuiltedObj.senderStr))
        print('rebuiltedObj.recipientUnicode:',rebuiltedObj.recipientUnicode)
        print('type(rebuiltedObj.recipientUnicode):',type(rebuiltedObj.recipientUnicode))
        print('rebuiltedObj.extNone:',rebuiltedObj.extNone)
        print('type(rebuiltedObj.extNone):',type(rebuiltedObj.extNone))
        print('rebuiltedObj.simpleList:',rebuiltedObj.simpleList)
        print('type(rebuiltedObj.simpleList):',type(rebuiltedObj.simpleList))
        print('rebuiltedObj.simpleTuple:',rebuiltedObj.simpleTuple)
        print('type(rebuiltedObj.simpleTuple):',type(rebuiltedObj.simpleTuple))
        print('rebuiltedObj.simpleSet:',rebuiltedObj.simpleSet)
        print('type(rebuiltedObj.simpleSet):',type(rebuiltedObj.simpleSet))
        import types
        for item in rebuiltedObj.simpleSet:
            if type(item ) is str :
                print('rebuiltedObj.simpleSet UnicodeType item:',item)
                print('rebuiltedObj.simpleSet UnicodeType item.encode(\'raw_unicode_escape\'):',item.encode('raw_unicode_escape'))
                try:
                    print('rebuiltedObj.simpleSet UnicodeType item.decode(\'raw_unicode_escape\'):',item.decode('raw_unicode_escape'))
                except Exception as e:
                    print('rebuiltedObj.simpleSet UnicodeType item.decode(\'raw_unicode_escape\')error:', e)
        print('rebuiltedObj.simpleDict:',rebuiltedObj.simpleDict)
        print('type(rebuiltedObj.simpleDict):',type(rebuiltedObj.simpleDict))
        print('rebuiltedObj.simpleDict[\'pos\']:',rebuiltedObj.simpleDict['pos'])
        print('type(rebuiltedObj.simpleDict[\'pos\']):',type(rebuiltedObj.simpleDict['pos']))
        print('rebuiltedObj.simpleDict[\'pos\'][\'x\']:',rebuiltedObj.simpleDict['pos']['x'])
        print('type(rebuiltedObj.simpleDict[\'pos\'][\'x\']):',type(rebuiltedObj.simpleDict['pos']['x']))
        print('rebuiltedObj.complexDict:',rebuiltedObj.complexDict)
        print('type(rebuiltedObj.complexDict):',type(rebuiltedObj.complexDict))
        print('rebuiltedObj.complexDict[\'pos\']:',rebuiltedObj.complexDict['pos'])
        print('type(rebuiltedObj.complexDict[\'pos\']):',type(rebuiltedObj.complexDict['pos']))
        print('rebuiltedObj.complexDict[\'pos\'][\'x\']:',rebuiltedObj.complexDict['pos']['x'])
        print('type(rebuiltedObj.complexDict[\'pos\'][\'x\']):',type(rebuiltedObj.complexDict['pos']['x']))
        print('rebuiltedObj.complexDict[\'pos\'][\'y\']:',rebuiltedObj.complexDict['pos']['y'])
        print('type(rebuiltedObj.complexDict[\'pos\'][\'y\']):',type(rebuiltedObj.complexDict['pos']['y']))
        for ie in rebuiltedObj.complexDict['pos']['y']:
            print('type of ie is :' ,type(ie))
            s=ie.encode('utf-8')
            print('type of s is :' ,type(s))
        print('rebuiltedObj.complexTuple:',rebuiltedObj.complexTuple)
        print('type(rebuiltedObj.complexTuple):',type(rebuiltedObj.complexTuple))
        print('rebuiltedObj.recordTime:',rebuiltedObj.recordTime)
        print('type(rebuiltedObj.recordTime):',type(rebuiltedObj.recordTime))
        print('rebuiltedObj.ext2:',rebuiltedObj.ext2)
        print('type(rebuiltedObj.ext2):',type(rebuiltedObj.ext2))
        print('JsonHelper .obj2json(rebuiltedObj,False) :',JsonHelper .obj2json(rebuiltedObj,False))
        print('--end--')



    def tearDown(self):
        print("----tearDown----")



# #导入json模块，你也可以用simplejson，一个第三模块，比较好用
#
# #定义一个dict对象，并有些value还是以json的形式出现，形式如下
# adict={"xiaoqiangk":"xiaoqiangv","xiaofeik":"xiaofeiv","xiaofeis":{"xiaofeifk":"xiaofeifv","xiaofeimk":{"xiaoqik":"xiaoqiv","xiaogou":{"xiaolei":"xiaolei"}}},"xiaoer":{"xiaoyuk":"xiaoyuv"}}
# #定义一个函数，用来处理json，传入json1对象，层深初始为0，对其进行遍历
#
# def hJson(json1,i=0):
#
#     #判断传入的是否是json对象，不是json对象就返回异常
#
#     if(isinstance(json1,dict)):
#
#         #遍历json1对象里边的每个元素
#         for item in json1:
#
#             #如果item对应的value还是json对象，就调用这个函数进行递归，并且层深i加1，如果不是，直接z在else处进行打印
#             if (isinstance(json1[item],dict)):
#
#                 #打印item和其对应的value
#                 print("****"*i+"%s : %s"%(item,json1[item]))
#
#                 #调用函数进行递归，i加1
#                 hJson(json1[item],i=i+1)
#             else:
#
#                 #打印
#                 print("****"*i+"%s : %s"%(item,json1[item]))
#     #程序入口，对adict进行处理，第二个参数可以不传
#     else:
#         print("json1  is not josn object!")
#
#
# hJson(adict,0)

class Msg(object):
    #idInt = 0 #id生成必须全局唯一
    """
    resq:请求消息
    resp:返回消息
    """
    # type = 'resq'
    # complexTuple = ''
    # simpleDict = ''
    # senderStr = ''
    # recipientUnicode = ''
    # simpleList = 0
    # extNone = ''
    # ext2 = ''
    #默认构造方法，构造一个空的消息
    def __init__(self):
        self.idInt = 5201314 #int
        self.numFloat = 124.0 #float
        self.senderStr = '50vip' #string
        self.recipientUnicode = u'我是中国人' #unicode
        self.extNone = None #null
        self.simpleList = ['a', 1, 1.0]
        self.simpleTuple=('A',255,8032445.657,1232132131231232132132131213432434342)
        self.simpleSet=set([4, 5, 6,u"女娲智能"])
        self.simpleDict = {'pos':{'x': 100, 'y':50}} #dict
        self.complexDict = {'pos':{'x': u"这3", 'y':['a',u'b']},u'中文键值':u'pinyin'} #dict
        self.recordTime=time.time()
        self.complexTuple = (1, "2\"", [3,4], {'a':1, 'b':'2'},u"这",set([1, 2, 3])) #tuple, list, dict,set