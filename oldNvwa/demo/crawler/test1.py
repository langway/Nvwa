#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    test1 
Author:   fengyh 
DateTime: 2015/1/28 9:37 
UpdateLog:
1、fengyh 2015/1/28 Create this File.


"""

from selenium import webdriver
from bs4 import BeautifulSoup
import MySQLdb
import sys
from selenium.webdriver import DesiredCapabilities


def mydebug():
    driver.quit()
    exit(0)

def catchDate(s):
    """页面数据提取"""
    soup = BeautifulSoup(s)
    z,z2 = [],[]
    global nowtimes

    m = soup.findAll("div",class_="date-buy")
    for obj in m:
        try:
            tmp = obj.find('br').contents
        except Exception, e:
            continue
        if(tmp != ""):
            z.append(tmp)
            nowtimes += 1
    m2 = soup.findAll("div",class_="comment-content")
    for obj in m2:
        try:
            tmp = obj.text.lstrip('\n\t\t\t').rstrip('\n\t\t\t').strip()
        except Exception, e:
            continue
        if(tmp != ""):
            z2.append(tmp)
            nowtimes += 1
    return z,z2

def getTimes(n,t):
    """获取当前进度"""
    return "当前进度为：" + str(int(100*n/t)) + "%"


#———————————————————————————————————| 程序开始 |—————————————————————————————————
#确定图书大类
cate = {"3273":"历史","3279":"心理学","3276":"政治军事","3275":"国学古籍","3274":"哲学宗教","3277":"法律","3280":"文化","3281":"社会科学"}

#断点续抓
num1 = input("bookid:")
num2 = input("pagenumber:")

#生成图书大类链接，共需17355*20 = 347100次
totaltimes = 347100.0
nowtimes = 0

#开启webdirver的PhantomJS对象
#driver = webdriver.PhantomJS()
driver = webdriver.Ie('C:\Program Files\Internet Explorer\IEDriverServer')
#driver = webdriver.Chrome('C:\Python27\Scripts\chromedriver')

#读出Mysql中的评论页面，进行抓取
# 连接数据库　
try:
    conn = MySQLdb.connect(host='localhost',user='root',passwd='',db='crawler')
    conn.set_character_set('utf8')
except Exception, e:
    print e
    sys.exit()

# 获取cursor对象
cursor = conn.cursor()
cursor.execute('SET character_set_connection=utf8;')
sql = "SELECT * FROM booknew ORDER BY pagenumber DESC"
cursor.execute(sql)
alldata = cursor.fetchall()

flag = 1
flag2 = 0

# 如果有数据返回就循环输出,http://club.jd.com/review/10178500-1-154.html
if alldata:
    for rec in alldata:
        #rec[0]--bookid,rec[1]--cateid,rec[2]--pagenumber
        if(rec[0] != str(num1) and flag == 0):
            continue
        else:
            flag = 1
        for p in range(num2,rec[2]):
            if(flag2 == 0):
                num2 = 0
                flag2 = 1
            p += 1
            #link = "http://club.jd.com/review/" + rec[0] + "-1-" + str(p) + ".html"
            link = "http://item.jd.com/11615131.html"
            link = "http://club.jd.com/review/10178500-1-154.html"
            #抓网页
            driver.get(link)
            html = driver.page_source
            #抓评论
            buydate,content = catchDate(html)
            #写入数据库
            for z in content:
                sql = "INSERT INTO ljj ( cateid, bookid, content) VALUES ( "+str(rec[0]) +",'" + rec[1] + "','" + z + "');"
                try:
                    cursor.execute(sql)
                except Exception, e:
                    print e
            conn.commit()
        print getTimes(nowtimes,totaltimes)

driver.quit()
cursor.close()
conn.close()

