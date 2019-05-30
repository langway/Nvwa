#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

import os
import sys
import pip
import subprocess
from subprocess import call
import io
import loongtian.util.pip.pip_settings as pip_settings
# from pywin import *

# 重载sys模块，设置默认字符串编码方式为utf8
reload(sys)
sys.setdefaultencoding('utf8')

# 是否使用douban等的国内镜像（默认为True）
useImageAddress=pip_settings.useImageAddress


# pipy国内镜像
imageHosts= pip_settings.imageHosts

imageAddress=""
if useImageAddress:
    # douban镜像
    imageAddress+=" -i " + imageHosts[0][1]#规定当前索引所在网址（如果不规定，使用默认）——
                                          # -i, --index-url <url>       Base URL of Python Package Index (default
                                          # https://pypi.python.org/simple).
    imageAddress+=" --trusted-host " + imageHosts[0][0] # 设置为可信任站点
    # for item in imageHosts  : #这里拼接find-links。注：不知为什么会重新转向到pypi主站点，弃用
    #     if item==None or item[0]==None or item[0]=="":
    #         continue
    #     imageAddress+=" --trusted-host " + item[0] + " --find-links=" +item[1]


#python版本号及文件路径
pyVersion=sys.version
if pyVersion >= '3':
    PY3 = True
else:
    PY3 = False

pyPath=sys.exec_prefix



currentPath=os.path.abspath('..\\..\\..')
supportPath= currentPath+"\\support\\" #为了防止Dos CMD命令行出现长文件名现象，在其两端加上引号。

def addQuoteMark(commandPath):
    """
    为了防止Dos CMD命令行出现长文件名现象，在其两端加上引号。
    :rawParam commandPath:
    :return:
    """
    if commandPath ==None and commandPath =="":
        return
    return "\"" + commandPath + "\""

if PY3:
    supportPath+="3.5\\"
else:
    supportPath+="2.7\\"

pipPath=pyPath +"\\Scripts\\pip.exe"#取得当前pip的完整路径（需判断python版本）

pipCommand=sys.executable + " " +pipPath #取得当前pip运行的命令行


def showEnviroment():
    """
    显示当前pip运行环境
    :return:
    """
    # 显示python版本号及文件路径
    print("Python Version: " + pyVersion)

    print("Python Path: " + pyPath)
    #显示当前pip版本号
    print("pip version: " +  pip.__version__ ) #+str(pip) )
    # call(pipCommand + " -V ", shell=True)



def displayAll():
    """
    显示全部已安装组件，并生成shell命令
    :return:
    """
    showEnviroment()

    installed=pip.get_installed_distributions()
    i=1
    for dist in installed:
        print("共计{0}个，当前第{1}--{2}".format(len(installed),i,dist.project_name))
        i+=1

    print("-----call pip install clause-------")
    for dist in installed:
        print("call(\"pip install --upgrade {0}\" + imageAddress, shell=True)".format(dist.project_name))

    print("-----call pipHelper install clause-------")
    for dist in installed:
        print("call(pipCommand + \" install --upgrade \" + {0} + imageAddress, shell=True)".format(dist.project_name))
        # pipCommand + " install --upgrade " + com + imageAddress

def installAllFromFile(filePath):
    """
    使用pip安装所有package
    :return:
    """
    showEnviroment()

    if filePath==None or filePath=="":
        print("你应该提供要转换的文件或路径！")
        return

    if not os.path.exists(filePath):
        print("提供的要转换的文件或路径错误！")
        return

    pipFile=io.open(filePath,encoding = 'utf-8')
    for line in pipFile.readlines():
        line=line.lstrip(' ').rstrip(' ')#去掉空格
        if line=='\n' or line=='':
            continue
        if line.startswith('#'):#过滤掉注释
            continue
        if line.__contains__('#'):
            line=line.split('#')[0]
        # line=addQuoteMark(line)
        call(line, shell=False)


def installAll(components):
    """
    安装所有components列表中定义的python组件。
    :rawParam components:组件名称的列表
    :return:
    """
    showEnviroment()

    # 取得已安装的组件列表
    installedlist, componentlist=getInstalledList()
    # 取得已安装、需更新的组件列表
    outdatelist, updatelist=getUpdateList()

    i=1
    succeed=0
    failureList=[]
    for component in components :

        if component==None or component=="":
            continue

        # 如果已安装，但不在需更新的组件列表中，说明不需要更新，继续下一个
        if componentlist.__contains__(component) and not updatelist.__contains__(component):
            print("——正在安装{0}，第{1}个，共{2}个。——".format(component, str(i), str(len(components))))

            print("——****  组件{0}已是最新，无需安装  ****————".format(component))
            succeed+=1
            i += 1
            continue

        print("——正在安装{0}，第{1}个，共{2}个。——".format(component,str(i),str(len(components) )) )
        i+=1
        result=install(component,False)
        if result:
            failureList.append(component)
            print("########  组件{0}安装未能完成。请检查输出，对可能的错误进行处理！  ########".format(component))
        else:
            succeed += 1
        pass #for com in components :

    output="\r\n——python组件已经安装完毕！共{0}个，成功{1}个。——" \
           "\r\n——安装未能完成的组件包括：" + str(failureList) + "，共{2}个——" \
           "\r\n——请检查输出，对可能的错误进行处理！——"
    output=output.format(str(len(components)),str(succeed),str(len(failureList)))
    print(output)

    pass # def installAll(components):

def install(component,withOutput=True,specialComponents=None):
    """
    安装组件
    :rawParam component: 组件名称
    :rawParam withOutput: 是否输出有关信息
    :rawParam specialComponents:特殊处理pywin32，numpy，安装Numpy+MKL，scipy，Twisted，lxml等组件
    :return:
    """
    if withOutput:
        showEnviroment()

    if component==None or component=="":
        return 1

    if withOutput:
        print("——正在安装{0}——".format(component))
    result =0

    if not PY3:
        # 重载sys模块，设置默认字符串编码方式为utf8
        reload(sys)
        sys.setdefaultencoding('utf8')


    if component=="VCForPython27" :# 特殊处理VCForPython27
        return installfrominstallation("VCForPython27")
    elif component=="tesseract-ocr" :# 特殊处理tesseract-ocr
        return installfrominstallation("tesseract-ocr")


    from loongtian.util.helper import fileHelper
    # 特殊处理pywin32，numpy，安装Numpy+MKL，scipy，Twisted，lxml
    if specialComponents==None or len(specialComponents)<=0:

        specialComponents=pip_settings.SpecialComponents

    if specialComponents.__contains__(component):
        files=fileHelper.getFilesInPath(supportPath,component,"whl")
        if len(files)>0:
            filePath =files[0]
            filePath=addQuoteMark(filePath)#为了防止Dos CMD命令行出现长文件名现象，在其两端加上引号。
            result =call(pipCommand + " install --upgrade " + filePath, shell=True)

        else:
            print("未发现特殊处理的组件{0}所需要的文件".format(component))
            result=1
        return result

    if PY3:
        if component=="dbutils":
            dbutilsPath=supportPath + "DButils4Python3\\"+"setup.py"
            dbutilsCommand=sys.executable + " " + dbutilsPath + " install"
            dbutilsCommand=addQuoteMark(dbutilsCommand)#为了防止Dos CMD命令行出现长文件名现象，在其两端加上引号。
            print("dbutilsCommand: " +dbutilsCommand) #这里有可能出错，将该行输出拷贝到命令行执行！
            result=call(dbutilsCommand, shell=True)
            return result
        # elif component=="PySide":
        #     print("——目前{0}暂不支持Python3.5——".format(component))
        #     return
        else:
            result=call(pipCommand + " install --upgrade " + component + imageAddress, shell=True)

    else:
        result =call(pipCommand + " install --upgrade " + component + imageAddress, shell=True)

    if withOutput:
        print("\r\n——python组件:{0}已经安装完毕！请检查输出，对可能的错误进行处理！——".format(component))

    return result

def installfrominstallation(component):


    if component=="VCForPython27" :# 特殊处理VCForPython27
        if not PY3:
            VCForPython27Path=supportPath + "VCForPython27.msi"

            VCForPython27Path=addQuoteMark(VCForPython27Path)#为了防止Dos CMD命令行出现长文件名现象，在其两端加上引号。
            result=call(VCForPython27Path, shell=True)
            return (result)
    elif component == "tesseract-ocr":  # 特殊处理tesseract-ocr
        path=supportPath +  ""


def getInstalledList():
    # 取得已安装的组件列表
    command = "pip list"

    installedlist = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                     shell=True).stdout.readlines()

    componentlist = []
    for x in installedlist:
        result = str(x)
        if result.__contains__("("):
            result = result.split("(")[0]
        if result.__contains__("'"):
            result = result.split("'")[1]
        result = result.strip()
        componentlist.append(result)

    # 弃用：下面的方法弃用，因为使用pip.get_installed_distributions()会把非用户安装的组件（python自带）列出
    # import pip
    # installedlist =pip.get_installed_distributions()
    # installedlist.reverse()
    # componentlist=[x.key.strip() for x in installedlist]


    print("本机已安装的组件：" + str(installedlist) + "\r\n共计{0}个".format(str(len(installedlist))))

    return installedlist,componentlist

def getUpdateList():
    # 取得已安装、需更新的组件列表
    command = "pip list --outdated"

    print("正在查询本机需要更新的组件，这可能需要一定时间，根据您的网速及已安装组件的数量，可能会有所不同......")

    # outdatelist = subprocess.check_output(command)
    outdatelist = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   shell=True).stdout.readlines()

    updatelist = []

    for x in outdatelist:
        result = str(x)
        if result.__contains__("("):
            result = result.split("(")[0]
        if result.__contains__("'"):
            result = result.split("'")[1]
        result = result.strip()
        updatelist.append(result)

    print("本机需要更新的组件：" + str(updatelist))

    if updatelist.__contains__("numpy") or updatelist.__contains__("scipy"):
        print ("numpy or scipy 出现重大更新，请至:\r\n"
               "http://www.lfd.uci.edu/~gohlke/pythonlibs/ \r\n"
               "下载对应的numpy或scipy版本，以免其他组件安装中出现问题！")

    return outdatelist,updatelist

def updateAll():
    """
    使用pip升级更新全部已安装组件（package）
    :return:
    """
    showEnviroment()

    # 取得已安装的组件列表
    installedlist, componentlist=getInstalledList()
    # 取得已安装、需更新的组件列表
    outdatelist, updatelist=getUpdateList()


    i=1
    for dist in updatelist:
        print("共计{0}个，当前第{1}个--{2}".format(len(installedlist),i,dist))
        install(dist,False)
        # call("pip install --upgrade " + dist.project_name, shell=True)

        i+=1

    print("\r\n——python组件已经更新完毕！请检查输出，对可能的错误进行处理！——")

def delete(component):
    """
    删除全部已安装组件(尽量不要使用)
    :return:
    """
    showEnviroment()
    if component==None or component=="":
        return

    if component=="pip":#不删除pip
        return

    print("——正在删除{0}——".format(component))

    call("pip uninstall " + component, shell=True)



def deleteAll():
    """
    删除全部已安装组件(尽量不要使用)
    :return:
    """
    showEnviroment()

    installed=pip.get_installed_distributions()
    i=1
    for dist in installed:
        if dist.project_name=="pip":#不删除pip
            continue
        print("共计{0}个，正在删除第{1}个--{2}".format(len(installed),i,dist.project_name))
        call("pip uninstall " + dist.project_name, shell=True)
        i+=1

def deleteAll(components):
    """
    删除全部已安装组件(尽量不要使用)
    :return:
    """
    showEnviroment()

    i=1
    for com in components :

        if com==None or com=="":
            continue

        if com=="pip":#不删除pip
            continue

        print("——正在删除{0}，第{1}个，共{2}个。——".format(com,str(i),str(len(components) )) )

        print("共计{0}个，当前第{1}个--{2}".format(len(components),i,com))
        call("pip uninstall " + com, shell=True)
        i+=1

# ----------------------------------说明-------------------------------------------------------
# python27、python35配置：
# 1、环境变量Path:C:\Python\Python35\Scripts\;C:\Python\Python35\;C:\Python27\Scripts\;C:\Python27\;
# 2、以某一版本为默认值，修改另一版本的python.exe为python[版本号].exe，例如：python2.exe

# 如果安装时报错，error: Microsoft Visual C++ 9.0 is required (Unable to find vcvarsall.bat)，下载地址：
# http://aka.ms/vcpython27
# 实际下载地址：
# http://www.microsoft.com/en-us/download/details.aspx?id=44266

# ---------------postgre安装错误或运行时报错的处理办法---------------------------
# 一、psycopg2 ImportError: DLL load failed
# from psycopg2._psycopg import BINARY, NUMBER, STRING, DATETIME
# ImportError: DLL load failed
# 这个错误
# 1. 使用了mingw32作为编译器
# 2. 然后这个_psycopg.pyd 老是加载不成功.
# 3. 有资料说是libpg.dll的版本和本机的postgresql不匹配, 或者说libpg.dll 不在windows的Path路径里
# 反正没解决, 最后在stackoverflow上找到答案, 安装一个别人编译好的windows版本, 地址在: http://www.stickpeople.com/projects/python/win-psycopg/
# 选择自己的python和postgresql对应的版本即可。

# ---------------scipy安装错误或运行时报错的处理办法---------------------------
# 到网站Python Extension Packages for Windows - Christoph Gohlke
# http://www.lfd.uci.edu/~gohlke/pythonlibs/ 下载对应的scipy版本（根据python版本及win版本），使用pip install [下载目录]即可安装。
# 注意：下载目录不能有空格!
#        http://www.lfd.uci.edu/~gohlke/pythonlibs/ 这个地址非常重要！有大多数组件的下载！
# 如果pip下载不了，请登陆上面网址，手动下载！！！


