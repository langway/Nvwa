#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    speech 
Author:   fengyh 
DateTime: 2014/9/23 11:01 
UpdateLog:
1、fengyh 2014/9/23 Create this File.


"""

import speech
import time

response = speech.input("Say something, please.")
speech.say("You said " + response)

def callback(phrase, listener):
    if phrase == "goodbye":
        listener.stoplistening()
    speech.say(phrase)
    print phrase

listener = speech.listenforanything(callback)
while listener.islistening():
    time.sleep(.5)