#!/usr/bin/env python
# coding: utf-8
"""
电子邮件帮助类。
"""

from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

class EmailHelper:
    # 构造函数：初始化基本信息
    def __init__(self, host, user, passwd):
        lInfo = user.split("@")
        self._user = user
        self._account = lInfo[0]
        self._me = self._account + "<" + self._user + ">"

        server = smtplib.SMTP()
        server.connect(host)
        server.login(self._account, passwd)
        self._server = server

    # 发送文件或html邮件
    def sendTxtMail(self, to_list, sub, content, subtype='html'):
        # 如果发送的是文本邮件，则_subtype设置为plain
        # 如果发送的是html邮件，则_subtype设置为html
        msg = MIMEText(content, _subtype=subtype, _charset='utf-8')
        msg['Subject'] = sub
        msg['From'] = self._me
        msg['To'] = ";".join(to_list)
        try:
            self._server.sendmail(self._me, to_list, msg.as_string())
            return True
        except Exception as e:
            print(str(e))
            return False

    # 发送带附件的文件或html邮件
    def sendAttachMail(self, to_list, sub, content, subtype='html'):
        # 创建一个带附件的实例
        msg = MIMEMultipart()
        # 增加附件1
        att1 = MIMEText(open(r'D:\javawork\PyTest\src\main.py','rb').read(), 'base64', 'utf-8')
        att1["Content-Type"] = 'application/octet-stream'
        # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
        att1["Content-Disposition"] = 'attachment; filename="main.py"'
        msg.attach(att1)

        # 增加附件2
        att2 = MIMEText(open(r'D:\javawork\PyTest\src\main.py','rb').read(), 'base64', 'utf-8')
        att2["Content-Type"] = 'application/octet-stream'
        att2["Content-Disposition"] = 'attachment; filename="main.txt"'
        msg.attach(att2)

        # 增加邮件内容
        msg.attach(MIMEText(content, _subtype=subtype, _charset='utf-8'))

        msg['Subject'] = sub
        msg['From'] = self._me
        msg['To'] = ";".join(to_list)

        try:
            self._server.sendmail(self._me, to_list, msg.as_string())
            return True
        except Exception as e:
            print(str(e))
            return False
     # 发送带附件的文件或html邮件
    def sendImageMail(self, to_list, sub, content, subtype='html'):
        # 创建一个带附件的实例
        msg = MIMEMultipart()

        # 增加邮件内容
        msg.attach(MIMEText(content, _subtype=subtype, _charset='utf-8'))

        # 增加图片附件
        image = MIMEImage(open(r'D:\javawork\PyTest\src\test.jpg','rb').read())
        #附件列表中显示的文件名
        image.add_header('Content-Disposition', 'attachment;filename=p.jpg')
        msg.attach(image)

        msg['Subject'] = sub
        msg['From'] = self._me
        msg['To'] = ";".join(to_list)

        try:
            self._server.sendmail(self._me, to_list, msg.as_string())
            return True
        except Exception as e:
            print(str(e))
            return False

    # 析构函数：释放资源
    def __del__(self):
        self._server.quit()
        self._server.close()

mailto_list = ['xxx@163.com']
mail = EmailHelper('smtp.163.com', 'xxx@163.com', 'xxxxxx')
if mail.sendTxtMail(mailto_list, "测试邮件", "hello world！<br><br><h1>你好，发送文本文件测试<h1>"):
    print("发送成功")
else:
    print("发送失败")
if mail.sendAttachMail(mailto_list, "测试邮件-带两个附件", "hello world！<br><br><h1>你好，发送文本文件测试<h1>"):
    print("发送成功")
else:
    print("发送失败")

if mail.sendImageMail(mailto_list, "测试邮件-带一个图片的附件", "hello world！<br><br><h1>你好，发送文本文件测试<h1>"):
    print("发送成功")
else:
    print("发送失败")