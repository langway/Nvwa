#!/usr/bin/env python
# coding: utf-8

__author__ = 'js'

import os
import imp
from loongtian.util.log.logger import logger



def readLines(filename):
    """
    读取文件的每一行并返回一个列表
    :rawParam filename:文件名
    :return:行列表
    """
    lines=[]
    filename = filename.decode('utf-8')
    fobj=None
    try:
        fobj = open(filename,  'r') #,encoding = "utf-8")
        for eachLine in fobj:
            if not eachLine:
                continue
            hasError=False
            try:
                eachLine=eachLine.decode("gbk")
            except UnicodeDecodeError as e:
                try:
                    eachLine=eachLine.decode("utf-8")
                except UnicodeDecodeError as e:
                    print(u"UnicodeDecodeError:" + e.message + u"  filename:" + filename +u"  eachLine:" )
                    print(eachLine)
                    hasError=True
                    # raise e
            if not hasError:
                lines.append(eachLine)
    except IOError as err:
        errorMsg='file open error: {0}'.format(err)
        logger.error(errorMsg)
        print(errorMsg)
    finally:
        if fobj:
            fobj.close()
    return lines



def writeLines(filename,lines,mode= 'w+'):
    """
    向文件写入（或追加写入行列表）
    :rawParam filename:文件名
    :rawParam lines:行列表
    :rawParam mode: 写入的状态：'w+'==覆盖，'a+'==追加
    :return:
    """

    try:
        fobj = open(filename, mode)
        # fobj.writelines(lines)
        for line in lines:
            if not line.endswith("\n"):
                line+="\n"
            fobj.write(line)
    except IOError as err:
        print('file open error: {0}'.format(err))
    finally:
        if fobj:
            fobj.close()


def writeLine(filename,line,mode= 'w+'):
    """
    向文件写入（或追加写入行列表）
    :rawParam filename:文件名
    :rawParam lines:行列表
    :rawParam mode: 写入的状态：'w+'==覆盖，'a+'==追加
    :return:
    """
    writeLines(filename,[line],mode)


def appendLines(filename,lines):
    """
    附加多行到文件。
    :rawParam filename:
    :rawParam lines:
    :return:
    """
    writeLines(filename,lines,"a+")


def appendLine(filename,line):
    """
    附加一行到文件。
    :rawParam filename:
    :rawParam lines:
    :return:
    """
    writeLines(filename,[line],"a+")


def overwriteLines(filename,lines):
    """
    重写多行到文件。
    :rawParam filename:
    :rawParam lines:
    :return:
    """
    writeLines(filename,lines,"w+")


def overwriteLine(filename,line):
    """
    重写多行到文件。
    :rawParam filename:
    :rawParam lines:
    :return:
    """
    writeLines(filename,[line],"w+")


def getFilesInPath(curPath,startswith=None,extension=None,endswith=None,contains=None):
    """
    获取当前目录下文件路径
    :rawParam curPath:当前目录
    :rawParam startswith: 文件名的开始字符串
    :rawParam extension: 文件名的后缀（可以不加.）
    :rawParam endswith: 文件名的结尾字符串
    :rawParam contains: 文件名包含的字符串
    :return:返回目录下文件路径及对应的模块的方法
    {'文件路径': 对应模块方法module}
    """
    files = []
    # 如果既不是目录也不是文件，直接返回，如果是文件，截取其路径
    if not os.path .isdir(curPath) :
        if not os.path .isfile(curPath) :
            return None

    #这里需要对文件名的后缀进行特殊处理（前面加.）
    if extension and not extension.startswith("."):
        extension="."+extension

    for item in os.listdir(curPath):
        curItem=os.path.join( curPath,item)
        #如果是文件，并且开头、结尾等都正确，添加到列表。

        istheFile=True
        if os.path.isfile(curItem):
            if  not startswith is None and not startswith=="" and not item.startswith(startswith):
                istheFile=False
            if  not contains is None and not contains=="" and not item.__contains__(contains) :
                istheFile=False
            filename=os.path.splitext(item)
            if  not extension is None and not extension=="" and not filename[1]==extension:
                istheFile=False
            if  not endswith is None and not endswith=="" and not filename[0]==endswith:
                istheFile=False

            if istheFile:
                files.append(curItem)
                continue

        if os.path.isdir(curItem) and not item[0] == '.':
            #检查下一个目录下的文件
            try:
                subFiles=getFilesInPath(curItem,startswith,extension,endswith,contains)
                files.extend(subFiles )
            except ImportError as e:
                print('error:'+e.message)


    return files



def loadPythonModules(files):

    modules={}
    if not files :
        return None
    for curfile in files :
        # if os.path.splitext(curfile)[1]
        try:
            loadedMod=imp.load_source(curfile,curfile)
            if not loadedMod is None:
                modules[curfile]=loadedMod
        except ImportError as e:
            loadedMod = None
            print('error:'+e.message)

    return modules


def getPathList(curPath,startswith,extension,endswith,contains):
    """
    获取当前目录下文件路径
    :rawParam curPath:
    :return:返回目录下文件路径及对应的模块的方法
    [{'path': '文件路径', 'mod': 对应模块方法module}]
    """
    path_list = []  # 返回数据列表

    # 循环迭代目录及文件
    for item in os.listdir(curPath):
        curItem=os.path.join(curPath, item)
        # 判断是否是文件，进行处理
        if os.path.isfile(curItem) and item.endswith('.py'):
            filenameToModuleName = os.path.splitext(item)[0]
            loadedMod=imp.load_source(filenameToModuleName, curItem)
            path_list.append({'path': curItem, 'mod': loadedMod})
        # 判断是否是目录，进行处理
        if os.path.isdir(curItem) and not item[0] == '.':
            #检查下一个目录下的测试文件
            try:
                subModules=getFilesInPath(curItem,startswith,extension,endswith,contains)
            except ImportError as e:
                subModules = None
                print('error:'+e.message)
            if subModules:
                path_list.append({'path': curItem, 'mod': subModules})

    return path_list



def getTree(path_f):
    """
    获取当前目录下文件路径
    :rawParam path_f:
    :return:返回路径下目录及文件路径
    type: dire 目录 , file 文件
    [{'path': '路径', 'type': 'dire/file', 'child': [树形子项]}]
    """
    dataList = []  # 返回数据列表
    fileList = os.listdir(path_f)
    # 循环迭代路径下目录及文件
    for f in fileList:
        # 拼接路径
        pathFull = os.path.normpath(os.path.join(path_f, '%s') % f)
        # 判断是否是目录
        if os.path.isdir(pathFull):
            if not f[0] == '.':
                direDict = {'path': pathFull, 'type': 'dire', 'child': []}
                dataList.append(direDict)
                # 查询目录下子目录和文件进行处理
                childList = getTree(pathFull)
                if childList:
                    direDict['child'] = childList
        # 判断是否是文件
        if os.path.isfile(pathFull) and f.endswith('.py'):
            dataList.append({'path': pathFull, 'type': 'file'})

    return dataList


def getTreePlane(path_f, level=1):
    """
    获取当前目录下文件路径
    :rawParam path_f:
    :rawParam level:
    :return:以平面形式返回路径下目录及文件路径
    [{'path': '路径', 'type': 'dire/file', 'depth': '层级，起始1'}，
    {'path': '路径', 'type': 'dire/file', 'depth': '子层级，父层级加1'}]
    """
    dataList = []  # 返回数据列表
    fileList = os.listdir(path_f)
    # 循环迭代路径下目录及文件
    for f in fileList:
        # 拼接路径
        pathFull = os.path.normpath(os.path.join(path_f, '%s') % f)
        direDict = {'path': pathFull, 'type': 'dire', 'depth': level}
        # 判断是否是文件
        if os.path.isfile(pathFull) and f.endswith('.py'):
            direDict['type'] = 'file'
            dataList.append(direDict)
        # 判断是否是目录
        if os.path.isdir(pathFull):
            if not f[0] == '.':
                direDict['type'] = 'dire'
                dataList.append(direDict)
                # 查询目录下子目录和文件进行处理
                childList = getTreePlane(pathFull, level+1)
                # 处理后子目录及文件以列表形式返回， 为显示为平面形式树而循环子项插入到父项同列表
                for cl in childList:
                    dataList.append(cl)

    return dataList


def getRealPath(_file_):
    """
    取得当前运行文件的实际路径（弃用，应在自己的文件中使用）
    :return:
    """
    return os.path.split(os.path.realpath(_file_))[0]