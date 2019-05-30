#/usr/bin/python
# coding: utf-8
import os

__author__ = 'Leon'



def CountSingleFileLine(path):
    """
    计算单个文件的行数（去掉空白行）
    :rawParam path:
    :return:
    """
    with open(path) as tempfile:
        total=0
        code = 0
        remarks=0
        space=0
        for line in tempfile:
            #总行数
            total+=1

            #空行数
            if line.isspace():
                space+=1
                continue

            if line.strip().startswith('#'):#这里还需记录一整行为注释的代码
                remarks+=1
                continue

            code += 1#这才是真正的代码
        print ("%s -total:%d code:%d remarks: %d space:%d" %(path,total ,code,remarks,space)) #output the file path and lines

        return total,code,remarks,space

    pass




def CountTotalLines(path,spaceHead):
    """
    计算当前文件夹下所有代码量（包括文件、子文件夹）
    :rawParam path:
    :return:
    """
    total = 0
    code = 0
    remarks=0
    space=0

    try:

        for root, dirs, files in os.walk(path):
            #检查当前目录下文件的代码量
            for fileItem in files:
                ext = os.path .splitext(fileItem)
                ext = ext[-1]  #get the postfix of the file
                if(ext in [u".py"]):  #["cpp", "c", "h", "java", "py", "xml", "properties", "php"]):
                    subpath = root + "/" + fileItem
                    curTotal,curCode,curRemarks,curSpace= CountSingleFileLine(subpath)
                    total +=curTotal
                    code+=curCode
                    remarks+=curRemarks
                    space+=curSpace

            #检查下一个目录下文件的代码量
            for dir in dirs:
                print (path)
                #print dir
                if dir !=u".idea" and dir!=u".svn": #略过svn文件夹

                    curTotal,curCode,curRemarks,curSpace=CountTotalLines(os.path.join( path,dir),spaceHead+spaceHead)
                    print (spaceHead+u'|---'+dir + u'--目录总实际行数：%d 代码量：%d 注释量：%d 空行量：%d' % (curTotal,curCode,curRemarks,curSpace))
                    total +=curTotal
                    code+=curCode
                    remarks+=curRemarks
                    space+=curSpace



            return total,code,remarks,space
    except BaseException as e:
        print ('BaseException',e)

        pass




print ("---Code Counter Stated---")

while True:
    path =raw_input('请输入要计算代码量的路径：').decode('utf-8')
    path=os.path .normpath(path)
    curTotal,curCode,curRemarks,curSpace= CountTotalLines(path,'    ')
    print(path + u'--目录总实际行数：%d 代码量：%d 注释量：%d 空行量：%d' % (curTotal,curCode,curRemarks,curSpace))

