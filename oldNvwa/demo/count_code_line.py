#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    count_code_line 
Author:   fengyh 
DateTime: 2014/11/28 16:39 
UpdateLog:
1、fengyh 2014/11/28 Create this File.


"""

import sys,os
extens = [".py",".cpp",".hpp",".h"]
linesCount = 0
filesCount = 0
def funCount(dirName):
    global extens,linesCount,filesCount
    for root,dirs,fileNames in os.walk(dirName):
        for f in fileNames:
            fname = os.path.join(root,f)
            try :
                ext = f[f.rindex('.'):]
                if(extens.count(ext) > 0):
                    print 'support'
                    filesCount += 1
                    print fname
                    l_count = len(open(fname).readlines())
                    print fname," : ",l_count
                    linesCount += l_count
                else:
                    print ext," : not support"
            except:
                print "Error occur!"
                pass

if len(sys.argv) > 1 :
    #for m_dir in sys.argv[1:]:
    for m_dir in sys.argv[1:]:
        print m_dir
        funCount(m_dir)
else :
    funCount(".")

print "files count : ",filesCount
print "lines count : ",linesCount


# 参数 F:\dev\03DesignAndCode\nvwa\loongtian F:\dev\03DesignAndCode\nvwa\test