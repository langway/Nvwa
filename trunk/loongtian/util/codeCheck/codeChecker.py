# /usr/bin/python
# coding: utf-8
"""
检查指定文件夹下所有代码是否有错误（包括文件、子文件夹）
todo 当前不能处理程序自动抛出的错误，所以需要建立一个需要略过的文件列表Ignored_File_List
有可能在当前文件夹下生成各种文件，需定期检查并删除
"""
__author__ = 'Leon'

import os, subprocess, time
import loongtian.util.helper.stringHelper as stringHelper


def CheckSingleFile(path, timeout=500):
    """
    检查单个文件的代码是否正确
    :rawParam path:
    :return:
    """
    if path in Ignored_File_List:
        return

    command = "python \"" + path + "\""
    print("——正在检查文件：" + path)
    # if path.endswith("vtClient.py"):
    #     # print(path in Ignored_File_List)


    pro = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           shell=True)

    outdatelist = pro.stderr.readlines()

    if outdatelist:
        converted = ""
        for outdate in outdatelist:
            outdate = stringHelper.convert_hex_to_string(outdate)
            converted += outdate
        # print(converted.replace("\r\n", ""))
        print(converted)
    # out_temp = tempfile.SpooledTemporaryFile(bufsize=1000 * 1000)
    # fileno = out_temp.fileno()
    # p = subprocess.Popen(command, stdout=fileno, shell=True,
    #                      stderr=fileno)  # , close_fds=True)
    #
    # p.wait()
    #
    # out_temp.seek(0)
    # lines = out_temp.readlines()
    # print(lines)
    pass


def CheckAllPyFiles(path):
    """
    检查当前文件夹下所有代码是否有错误（包括文件、子文件夹）
    :rawParam path:
    :return:
    """
    errors = []
    try:

        for root, dirs, files in os.walk(path):
            # 检查当前目录下文件的代码量
            for fileItem in files:
                ext = os.path.splitext(fileItem)
                ext = ext[-1]  # get the postfix of the file
                if (ext in [".py"]):  # ["cpp", "c", "h", "java", "py", "xml", "properties", "php"]):

                    subpath = os.path.join(root, fileItem)

                    temp_errors = CheckSingleFile(subpath)
                    if temp_errors:
                        errors.append((subpath, temp_errors))

            # 检查下一个目录下文件的代码量
            for dir in dirs:
                print("正在检查目录：" + path)
                # print dir
                if dir != ".idea" and dir != ".svn":  # 略过svn文件夹

                    temp_errors = CheckAllPyFiles(os.path.join(path, dir))

                    errors.extend(temp_errors)
            return errors

    except BaseException as e:
        print('BaseException', e)

        pass


def CheckAllPythonFiles(path):
    """
    检查给定目录下的所有的python文件
    :param path:
    :return:
    """
    print("-" * 50)
    print("current path:" + path)
    print("---Code Check Stated---")
    errors = CheckAllPyFiles(path)
    if errors:
        print("---共有{0}个文件出现错误：---".format(len(errors)))
        for e in errors:
            print(e[0])
            print(e[1])

    print("---Code Check Ended---")


# 需要略过的文件列表
Ignored_File_List = [

    # autotrade部分
    "E:\\0-nvwa\\trunk\\loongtian\\autotrade\\trader\\archive\\vtClient.py",
    "E:\\0-nvwa\\trunk\\loongtian\\autotrade\\trader\\archive\\vtServer.py",

    # autotrade部分-api
    "E:\\0-nvwa\\trunk\\loongtian\\autotrade\\api\\cshshlp\\test\\cstest.py",
    "E:\\0-nvwa\\trunk\\loongtian\\autotrade\\api\\ctp\\vnctpmd\\test\\mdtest.py",
    "E:\\0-nvwa\\trunk\\loongtian\\autotrade\\api\\ctp\\vnctptd\\test\\tdtest.py",
    "E:\\0-nvwa\\trunk\\loongtian\\autotrade\\api\\femas\\vnfemasmd\\test\\mdtest.py",
    "E:\\0-nvwa\\trunk\\loongtian\\autotrade\\api\\femas\\vnfemastd\\test\\tdtest.py",
    "E:\\0-nvwa\\trunk\\loongtian\\autotrade\\api\\ib\\test\\test.py",
    "E:\\0-nvwa\\trunk\\loongtian\\autotrade\\api\\lhang\\test.py",
    "E:\\0-nvwa\\trunk\\loongtian\\autotrade\\api\\lts\\vnltsmd\\test\\mdtest.py",
    "E:\\0-nvwa\\trunk\\loongtian\\autotrade\\api\\lts\\vnltsqry\\test\\qrytest.py",
    "E:\\0-nvwa\\trunk\\loongtian\\autotrade\\api\\lts\\vnltstd\\test\\tdtest.py",
    "E:\\0-nvwa\\trunk\\loongtian\\autotrade\\api\\oanda\\test.py",
    "E:\\0-nvwa\\trunk\\loongtian\\autotrade\\api\\qdp\\vnqdpmd\\test\\mdtest.py",
    "E:\\0-nvwa\\trunk\\loongtian\\autotrade\\api\\qdp\\vnqdptd\\test\\tdtest.py",
    "E:\\0-nvwa\\trunk\\loongtian\\autotrade\\api\\shzd\\test\\test.py",
    "E:\\0-nvwa\\trunk\\loongtian\\autotrade\\api\\xspeed\\test\\xspeedmdtest.py",
    "E:\\0-nvwa\\trunk\\loongtian\\autotrade\\api\\xspeed\\test\\xspeedtdtest.py",

    # nvwa部分
    "E:\\0-nvwa\\trunk\\loongtian\\nvwa\\tools\\cidian\\BeautifulSoup.py",
    "E:\\0-nvwa\\trunk\\loongtian\\nvwa\\adminConsoleRunner.py",
    "E:\\0-nvwa\\trunk\\loongtian\\nvwa\\centralBrainRuner.py",

    # test部分
    "E:\\0-nvwa\\trunk\\test\\autotrade\\rpc\\testServer.py",
    "E:\\0-nvwa\\trunk\\test\\autotrade\\rpc\\testClient.py",
    "E:\\0-nvwa\\trunk\\test\\util\\tasks\\Example\\exceptRaisableThread.py",

    "E:\\0-nvwa\\trunk\\loongtian\\fuxi\\httpServerRunner.py",
    "E:\\0-nvwa\\trunk\\loongtian\\util\\codeCheck\\codeChecker.py",

]

# Ignored_File_List=[f.replace("\\","\\\\") for f in Ignored_File_List]
Ignored_File_List = [os.path.normpath(f) for f in Ignored_File_List]

# 是否检查输入的目录，如否，则检查Directories_to_check给定的目录
Check_from_input = True

# 需要自动化检查的目录列表
Directories_to_check = [
    # "E:\\0-nvwa\\trunk\\loongtian\\autotrade\\api",
    # "E:\\0-nvwa\\trunk\\loongtian\\autotrade\\data",
    # "E:\\0-nvwa\\trunk\\loongtian\\autotrade\\examples",
    "E:\\0-nvwa\\trunk\\loongtian\\nvwa",
    # "E:\\0-nvwa\\trunk\\loongtian\\autotrade\\trader",
]
# CheckSingleFile("E:\\0-nvwa\\trunk\\loongtian\\autotrade\\trader\\archive\\vtClient.py")


if Check_from_input:
    while True:
        path = input('请输入要检查代码的路径：')
        path = os.path.normpath(path)
        CheckAllPythonFiles(path)
else:
    for path in Directories_to_check:
        CheckAllPythonFiles(path)
