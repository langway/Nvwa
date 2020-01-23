#/usr/bin/python
# coding: utf-8
__author__ = 'Leon'



import os

def FillXmlDocOfNvwaObjects(path):

    for root, dirs, files in os.walk(path):
        # #
        # for fileItem in files:
        #     ext = os.path .splitext(fileItem)
        #     ext = ext[-1]  #get the postfix of the file
        #     if(ext in [".py"]):  #["cpp", "c", "h", "java", "py", "xml", "properties", "php"]):
        #         subpath = root + "/" + fileItem
        #         total += CountSingleFileLine(subpath)
        # #检查下一个目录下文件的代码量
        # for dir in dirs:
        #     print path
        #     #print dir
        #     if dir<>".idea" and dir<>".svn": #略过svn文件夹
        #
        #         curTotal=CountTotalLines(os.path.join( path,dir))
        #         print dir + u'代码量：' + curTotal.__str__()
        #         total +=curTotal
        #
        # return total
        pass#for root, dirs, files in os.walk(path):


    pass

