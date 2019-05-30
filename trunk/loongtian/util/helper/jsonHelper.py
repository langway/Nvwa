#!/usr/bin/env python
# coding=utf-8

"""
JsonHelper.py Convent OBJECT to JSON
将对象结构转化成一个json字符串，使用递归思路，自定义dump解析器，项目地址；https://github.com/hustcc/object2json
python json库，对于对象嵌套的类型的数据转JSON无能为力

--
PS：实际上，采用lambda即可完成，我开眼了
json.dumps(obj, default = lambda o: o.__dict__)
--
（leon2015-10-15）PS:实际上，用lambda也完成不了，由于python天生缺少类型，
所以解析出的对象（除了基本数据类型，只能包括list和dict）无法按原类型进行还原

@author: hzwangzhiwei
@contact: http://50vip.com/

Edited on 2015年10月15日——10月27日
@editor:leon
@editor contact:langway@163.com
@editor remarks:based on hzwangzhiwei's work allmost rewrited.add json2obj function,rename it as JsonObjectHelpe
"""
import json
import types

from loongtian.util.helper import stringHelper
from loongtian.util.helper import fileHelper

simpleType = [types.StringType,
              types.BooleanType,
              types.IntType,
              types.LongType,
              types.FloatType,
              types.NoneType, ]

# complexType ={
#     1:types.
#
# }

notSupportTypes = [
    types.TypeType,
    types.StringTypes,
    types.ComplexType,
    types.BufferType,
    types.FunctionType,
    types.LambdaType,
    types.CodeType,
    types.GeneratorType,
    types.UnboundMethodType,
    types.MethodType,
    types.BuiltinFunctionType,
    types.BuiltinMethodType,
    types.FileType,
    types.XRangeType,
    types.TracebackType,
    types.FrameType,
    types.SliceType,
    types.EllipsisType,
    types.DictProxyType,
    types.NotImplementedType,
    types.GetSetDescriptorType,
    types.MemberDescriptorType,
]


def obj2json(obj, processSpecialType=True):
    """
    嵌套对象转json字符串
    :rawParam obj: python对象
    :rawParam usejsonpickle: 是否使用jsonpickle进行转换
    :rawParam processSpecialType: 是否在特殊类型（tuple、set、unicode）后面要带类型——这里定义为在value后面加#Type。例如"complexTuple#tuple": [1, "2\"", [3, 4], {"a": 1, "b": "2"}]
    :return:
    """
    # if usejsonpickle :
    #     return  pickler.encode(obj)

    s = __convertObj2Json(obj, processSpecialType)
    # 去掉多次dump产生的\\
    # while s.__contains__("\\\\\\\\\\\\"): #6个\
    #     s=s.replace("\\\\\\\\\\\\","\\")
    # while s.__contains__("\\\\\\\\\\"): #5个\
    #     s=s.replace("\\\\\\\\\\\\","\\")
    # while s.__contains__("\\\\\\\\"): #4个\
    #     s=s.replace("\\\\\\\\","\\\\")
    # while s.__contains__("\\\\\\"):#3个\
    #     s=s.replace("\\\\\\","\\")
    # while s.__contains__("\\\\"):#2个\
    #     s=s.replace("\\\\","\\")
    # s=s.replace("\\","")

    # if isinstance(s,str) or isinstance(s,unicode):
    #     splitByExecutable=s.split("\\")
    #     if splitByExecutable and len(splitByExecutable)>1:
    #         s=""
    #         for i in range(len(splitByExecutable)):
    #             split=splitByExecutable[i]
    #             if split=="" and s.endswith("\\"):
    #                 continue
    #             if i==len(splitByExecutable)-1: # 最后一个
    #                 s+=split
    #             else:
    #                 s+=split + "\\"
    #         # s=s[0:-2] # 去掉最后的"\\"

    return s


def __convertObj2Json(obj, processSpecialType=True):
    """

    :param obj:
    :param processSpecialType:
    :return:
    """

    _t = type(obj)
    if _t in simpleType:  # 如果是简单类型，直接返回
        return obj
    if _t in notSupportTypes:
        raise Exception("不支持的对象类型：%s！" % _t)
    _isClass = False
    _isTuple = False
    _isSet = False
    _isInstance = False

    if _t is types.UnicodeType:  # unicode
        if processSpecialType:
            obj += __unicodeSuffix
        return obj

    elif _t is types.ListType:  # list
        _converted = [__convertObj2Json(itemChild, processSpecialType) for itemChild in obj]
    elif _t is types.TupleType:
        _converted = [__convertObj2Json(itemChild, processSpecialType) for itemChild in obj]
        _isTuple = True
    elif _t is types.DictionaryType:
        _converted = {}
        for childK, childV in obj.items():
            _tempK = __convertObj2Json(childK)
            _converted[_tempK] = __convertObj2Json(childV, processSpecialType)

    elif isinstance(obj, set):
        _converted = [__convertObj2Json(itemChild, processSpecialType) for itemChild in obj]
        _isSet = True
    elif _t is types.ClassType:
        _converted = obj
        _isClass = True
    elif _t is types.InstanceType:
        _converted = obj
        _isInstance = True
    else:
        if hasattr(obj, '__dict__'):
            # print 'not hasattr(obj,\'__dict__\'):',obj
            _converted = obj
            _isClass = True
        else:# 基本数据类型，直接返回
            return obj

    # 除了上面经过转换的list、Dict，其余的obj应该是一个类
    try:
        if processSpecialType:
            s = json.dumps(_converted, cls=ObjJsonEncoderWithType)  # ,encoding='utf-8')默认就是utf-8
        else:
            s = json.dumps(_converted, cls=ObjJsonEncoder)  # ,encoding='utf-8')
    except Exception as e:
        raise e

    if processSpecialType:
        if _isTuple:
            s += __tupleSuffix
        elif _isSet:
            s += __setSuffix
        elif _isClass:
            s += '#{'
            s += '"' + __typenameMark + '":"' + _t.__name__ + '"'
            # print '_t.__name__:',a

            import inspect
            a = inspect.getmodule(_t)
            # print a

            # a=sys.modules.get(_t.__module__)
            # print 'dir(a):',dir(a)
            if a:
                s += ',"' + __modulenameMark + '":"' + a.__name__ + '"'
                s += ',"' + __modulefileMark + '":"' + a.__file__ + '"'
                if a.__package__:
                    s += ',"' + __modulepackageMark + '":"' + a.__package__ + '"'

            s += '}#'

    return s


__tupleSuffix = '#type=tuple#'
__setSuffix = '#type=set#'
__unicodeSuffix = '#type=unicode#'

__typenameMark = 'typename'
__modulenameMark = 'modulename'
__modulefileMark = 'modulefile'
__modulepackageMark = 'modulepackage'


def object2dict(obj, processSpecialType=True):
    """
    递归 py对象转dict
    """
    # 基本数据类型，直接返回
    if not hasattr(obj, '__dict__'):
        # print '2 not hasattr(obj,\'__dict__\'):',obj
        return obj

    rst = {}
    for k, v in obj.__dict__.items():

        if k.startswith('-'):
            continue

        ele = __convertObj2Json(v, processSpecialType)

        # if ele is None:
        #     continue

        rst[k] = ele

    return rst

    pass  # def object2dict(obj,processSpecialType=True):


def __RecursiveObject2dictInListType(v, processSpecialType=True):
    ele = []
    for item in v:
        eleChild = __convertObj2Json(v, processSpecialType)
        ele.append(eleChild)

    return ele
    pass  # def __RecursiveObject2dictInListType(v,processSpecialType):


class ObjJsonEncoder(json.JSONEncoder):
    """
    重现实现自定义的json encoder
    """

    def default(self, obj):
        # for t in (list, dict, str, unicode, int, float, bool, type(None)):
        #     if isinstance(obj,t):
        #          return object2dict(obj)
        # return {'_python_object': pickle.dumps(obj)}
        return object2dict(obj, False)


class ObjJsonEncoderWithType(json.JSONEncoder):
    """
    重现实现自定义的json encoder
    """

    def default(self, obj):
        # if isinstance(obj, (list, dict, str, unicode, int, float, bool, type(None))):
        #     return object2dict(obj,True)
        # return {'_python_object': pickle.dumps(obj)}
        return object2dict(obj, True)

    pass  # class ObjJsonEncoderWithType(json.JSONEncoder):


def json2obj(jsonString, targetType=None, processSpecialType=True, usejsonpickle=False):
    """
    将json字符串按后面的对象定义
    :rawParam jsonString:json字符串（有可能包含特殊类型（tuple、set、unicode）的定义：为在value后面加#Type）
    :rawParam targetType:指定要将json字符串转化成的对象的类型
    :rawParam usejsonpickle: 是否使用jsonpickle进行转换
    :rawParam processSpecialType: 是否在特殊类型（tuple、set、unicode）后面要带类型——这里定义为在value后面加#Type。例如"complexTuple#tuple": [1, "2\"", [3, 4], {"a": 1, "b": "2"}]
    :return:
    """

    # getDefinedType=False
    # if targetType is None:#如果没有给定要转换的类型，需要从json字符串中读取字符串所代表的类型
    #    getDefinedType =True

    return __processValueToObject(jsonString, targetType)

    pass  # def json2obj(jsonString,targetType=None,processSpecialType=True,usejsonpickle=False):


def __processValueToObject(value, targetType):
    # 这里只处理str及unicode、list、dict（在其中循环）
    vType = type(value)
    # print 'vType:',vType
    # print 'vType is unicode:',vType is unicode
    # print 'vType is dict:',type(v) is types.DictionaryType
    # if vType is types .IntType or vType is types.FloatType or vType is types.LongType or vType is types.BooleanType:

    if vType is types.StringType or vType is types.UnicodeType:

        return __processSpecialDefinedStrToObj(value, targetType)

        # if not type(s) is types .StringType and not type(s) is types.UnicodeType :
        #     return s
        #
        # if targetType is None:
        #     targetType=t
        #
        # return (s,targetType)1

    else:
        if vType is types.ListType:
            _atrrib = []
            for item in value:
                _atrrib.append(__processValueToObject(item, None))

        elif vType is types.DictionaryType:
            _atrrib = {}
            for itemK, itemV in value.items():
                itemK = __processValueToObject(itemK, None)

                _atrrib[itemK] = __processValueToObject(itemV, None)
        else:
            return value

    return _atrrib

    pass  # def __processValueToObject(value,targetType):


def __processSpecialDefinedStrToObj(value, targetType):
    """
    将带有特殊处理标记的字符串转换为
    :rawParam value:
    :rawParam getDefinedType:
    :return:
    """
    # _type =None

    if value is None:
        return None

    if not isinstance(value, str) and not type(value) is types.UnicodeType:
        return value

    if value == '':
        return value

    if value.endswith('#'):  # 如果后缀有#，说明是一个特殊类型定义的对象，进行特殊处理

        if value.endswith(unicode(__unicodeSuffix)):
            _stripped = value[:-len(__unicodeSuffix)]
            return unicode(_stripped)

        elif value.endswith(unicode(__tupleSuffix)):
            _stripped = value[:-len(__tupleSuffix)]
            # _converted=__loadListFromStr(_stripped,__tupleSuffix)
            _converted = __fillTargetTypeWithJson(_stripped, tuple)

            if _converted:  # 已经分别处理子元素，直接转换成元组
                return tuple(_converted)

        elif value.endswith(unicode(__setSuffix)):
            _stripped = value[:-len(__setSuffix)]
            # _converted=__loadListFromStr(_stripped,__setSuffix)
            _converted = __fillTargetTypeWithJson(_stripped, None)

            if _converted:  # 已经分别处理子元素，直接转换成set
                return set(_converted)

        else:
            import re
            patternStr = '#{"typename":".*","modulename":".*","modulefile":".*"}#'
            pattern = re.compile(patternStr, re.S)
            # 使用Pattern匹配文本，获得匹配结果，无法匹配时将返回None
            matched = pattern.findall(value)

            if matched:
                _typeStr = matched[-1]

                value = value.replace(_typeStr, '')
                # #这里有可能是经过特殊类型处理（后面是#）之后产生的list、dict等的字符串，所以要对对象进行内部转换
                # value=__fillTargetTypeWithJson(value,_type)
                if targetType is None:
                    targetType = __loadTypeFromTypeStr(_typeStr)

                return __fillTargetTypeWithJson(value, targetType)

                pass  # if matched:

            # return __fillTargetTypeWithJson(value,targetType)
            raise ValueError('Illegal string with # suffix!')

        return _converted

    else:

        # 这里需将unicode字符串转换成utf-8格式（字符串）。否则，输出的所有字符串都将变成unicode类型
        return __fillTargetTypeWithJson(value, targetType)

    pass  # def __processSpecialDefinedStrToObj(value):


def __fillTargetTypeWithJson(s, targetType):
    # 这里应该判断是否是json字符串
    if not s.startswith('{') and not s.endswith('}') and not s.startswith('[') and not s.endswith(']'):
        return s.encode('utf-8')

    _loaded = False
    # 试着加载json字符串
    try:
        _loaded = json.loads(s)  # ,'utf-8')
    except Exception, e:
        # done （已解决）这里为什么出现类似于['q', 'w', 'e']不能被正确加载的情况？
        if s.startswith('[') and s.endswith(']'):
            _loaded = __loadListFromStr(s)
        if not _loaded:
            return str(s)  # 这里由于各种原因不能加载，直接返回s
        # raise ValueError ('you must provide a legally json string to load!'+ e.message)

    # 如果这里的对象是一个数字、布尔值等简单类型，说明是一个单独进入的字符串，这里要将其重新转换成字符串，以避免数字式、布尔值字符串被转换
    _t = type(_loaded)
    if _t is types.IntType or _t is types.FloatType or _t is types.LongType or _t is types.BooleanType:
        return str(_loaded)

    if targetType is None:
        return __processValueToObject(_loaded, targetType)

    # 试着创建对象
    _o = None
    try:
        _o = targetType()
    except Exception, e:
        print '_o=targetType() Error:', e
        try:
            import new
            _o = new.instance(targetType)
        except Exception, e:
            print '_o=new.instance(targetType) Error:', e

    if _o is None or type(_o) is types.NoneType:
        raise ValueError('you must provide a legally targetType to load json attributes!')

    # 这里要过滤掉本身就是dict、list、unicode、str、int等基本类型的情况
    # 基本数据类型，对其进行进一步处理，然后返回
    if not hasattr(_o, '__dict__'):
        return __processValueToObject(_loaded, None)

    # 将json字符串加载的字典装填进对象，这里要注意对特殊类型（tuple、set、unicode）的定义：为在value后面加#Type）
    try:
        __fillDict2Obj(_loaded, _o)
    except Exception, e:
        print '__fillDict2Obj(_loaded,_o) Exception:', e

    return _o

    pass  # def __fillTargetTypeWithJson(s,targetType):


def __fillDict2Obj(dict, o):
    """
    将json字符串加载的字典装填进对象，这里要注意对特殊类型（tuple、set、unicode）的定义：为在value后面加#Type）
    :rawParam dict:
    :rawParam o:
    :return:
    """
    for k, v in dict.items():

        _atrrib = __processValueToObject(v, None)
        _key = __processValueToObject(k, None)
        # _atrrib=getattr(o,k)
        # if _atrrib is None :
        #     continue
        if _atrrib:
            setattr(o, _key, _atrrib)

    pass  # def __fillDict2Obj(dict,o):


def __loadListFromStr(s):
    # _list=list(s)
    # s=''
    # s=s.encode('utf-8')
    s = s.strip()
    if s == '':
        return

    s = s.lstrip('[').rstrip(']')  # StripChar(s,'[',']')

    _list = s.split(',')
    _list = [__processValueToObject(x.strip().lstrip('\'').rstrip('\''), None) for x in
             _list]  # [StripChar(x.strip(),'\'','\'') for x in _list]

    # if listtype== __tupleSuffix:
    #     _o=tuple(_list)
    # elif listtype== __setSuffix:
    #     _o=set(_list)

    return _list
    pass  # def __loadListFromStr(s):


def __loadTypeFromTypeStr(typeStr):
    """
    根据Type的定义（字符串）取得type
    :rawParam typeStr:
    :return:
    """

    if typeStr is None or typeStr == '':
        return

    typeStr = typeStr.lstrip('#').rstrip('#').strip()
    # 试着加载json字符串
    try:
        try:
            _dict = json.loads(typeStr)  # ,'utf-8')
        except:
            # 此处转换normpath， join 生成标准格式依然报错，此处暂用替换， linux系统不会生成'\\',此处不执行
            # js 2015-11-30
            moduleFileIndex = typeStr.find('modulefile')
            if moduleFileIndex > 0:
                typeStrMouleFile = typeStr[moduleFileIndex:]
                typeStrMouleFile = typeStrMouleFile.replace('\\', '/')
                typeStr = typeStr[0:moduleFileIndex] + typeStrMouleFile
            _dict = json.loads(typeStr)
    except:
        raise ValueError('you must provide a legally json string to load!')

    if _dict:
        _package = _dict.get(__modulepackageMark)
        _modulename = _dict.get(__modulenameMark)
        _typename = _dict.get(__typenameMark)
        _modulefile = _dict.get(__modulefileMark)

        if _modulename is None or _modulename == '':
            raise ValueError('you must provide a module name to get the module!')

        if _typename is None or _typename == '':
            raise ValueError('you must provide a type name to get the type!')

        # todo:这样处理package是否正确？
        if _package:
            _modulename = _package + '.' + _modulename
        import sys
        aMod = sys.modules.get(_modulename)
        if not aMod:  # 如果未找到module，试着从文件中加载
            import imp
            aMod = imp.load_source(_modulename, _modulefile)
        if not aMod:  # 如果仍未找到module，直接返回
            return

        return getattr(aMod, _typename)

    pass  # def __loadTypeFromTypeStr(typeStr):


def loadObjectsFromJsonFile(fileName):
    """
    从文件中读取每一行，然后加载为对象
    :rawParam fileName:
    :return:
    """
    lines = fileHelper.readLines(fileName)
    objs = []
    for eachLine in lines:
        line = eachLine.strip().decode('utf-8')  # 去除每行首位可能的空格，并且转为Unicode进行处理
        line = line.strip(',')  # 去除Json文件每行大括号后的逗号
        js = None
        try:
            js = json2obj(line)  # 加载Json文件
            objs.append(js)
        except Exception, e:
            print 'bad line'
            continue
    return objs

    pass  # def loadObjectsFromJsonFile(fileName):


def saveObjectToFile(objs, fileName):
    """
    以json格式将多个对象保存到文件。
    :rawParam objs: 多个对象的列表
    :rawParam fileName: 文件名
    :return:
    """

    jsons = []
    if type(objs) is types.ListType:
        for obj in objs:
            line = obj2json(obj)
            jsons.append(line)
    elif type(objs) is types.DictionaryType:
        line = obj2json(objs)
        jsons.append(line)
    else:
        line = obj2json(objs)
        jsons.append(line)

    fileHelper.writeLines(fileName, jsons)

    pass  # def saveObjectToFile(objs,fileName):


def get_dict_value(date, keys, default=None):
    # default=None，在key值不存在的情况下，返回None
    # 以“.”为间隔，将字符串分裂为多个字符串，其实字符串为字典的键，保存在列表keys_list里
    keys_list = keys.split('.')
    # 如果传入的数据为字典
    if isinstance(date, dict):
        # 初始化字典
        dictionary = dict(date)
        # 按照keys_list顺序循环键值
        for i in keys_list:
            try:
                if dictionary.get(i) != None:  # 如果键对应的值不为空，返回对应的值
                    dict_values = dictionary.get(i)

                elif dictionary.get(i) == None:  # 如果键对应的值为空，将字符串型的键转换为整数型，返回对应的值
                    dict_values = dictionary.get(int(i))

            except:
                return default  # 如果字符串型的键转换整数型错误，返回None

            dictionary = dict_values

        return dictionary
    else:
        # 如果传入的数据为非字典
        try:
            # 如果传入的字符串数据格式为字典格式，转字典类型，不然返回None
            dictionary = dict(eval(date))
            if isinstance(dictionary, dict):
                # 按照keys_list顺序循环键值
                for i in keys_list:
                    try:
                        if dictionary.get(i) != None:  # 如果键对应的值不为空，返回对应的值
                            dict_values = dictionary.get(i)

                        elif dictionary.get(i) == None:  # 如果键对应的值为空，将字符串型的键转换为整数型，返回对应的值
                            dict_values = dictionary.get(int(i))

                    except:
                        return default  # 如果字符串型的键转换整数型错误，返回None

                    dictionary = dict_values
                return dictionary
        except:
            return default


if __name__ == '__main__':
    data_a = {2: {"b": {"c": "嗨，你好！"}}}
    print(get_dict_value(data_a, "2.b.c"))
    data_a = '{2:{"b":{"c":"嗨，你好！"}}}'
    print(get_dict_value(data_a, "2.b.c"))

# def as_python_object(dct):
#     if '_python_object' in dct:
#         return pickle.loads(str(dct['_python_object']))
#     return dct
