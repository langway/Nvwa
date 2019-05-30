#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 作者：余博伦
# 链接：https://zhuanlan.zhihu.com/p/25034403
# 来源：知乎
# 著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

import itchat, time, requests, random
from itchat.content import *

replied = []

@itchat.msg_register([TEXT])
def text_reply(msg):
    if '年' in msg['Text'] and msg['FromUserName'] not in replied:
      sendGreeting(msg)

@itchat.msg_register([PICTURE, RECORDING, VIDEO, SHARING])
def other_reply(msg):
  if msg['FromUserName'] not in replied:
    sendGreeting(msg)

def sendGreeting(msg):
  global replied
  friend = itchat.search_friends(userName=msg['FromUserName'])
  itchat.send((friend['RemarkName']+'，'+getRandomGreeting()), msg['FromUserName'])
  replied.append(msg['FromUserName'])

def getRandomGreeting():
  response = requests.get("http://www.xjihe.com/api/life/greetings?festival=新年&page=10", headers = {'apiKey':'sQS2ylErlfm9Ao2oNPqw6TqMYbJjbs4g'})
  results = response.json()['result']
  greeting = results[random.randrange(len(results))]['words']
  return greeting

itchat.auto_login(enableCmdQR=False,hotReload=True)
itchat.run()