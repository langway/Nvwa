#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    printself 
Author:   fengyh 
DateTime: 2014/8/22 16:19 
UpdateLog:
1、fengyh 2014/8/22 Create this File.


"""

s1='s1=%s%s%s;s2=s1 %% (chr(39), s1, chr(39) );print s2';
s2=s1 % (chr(39), s1, chr(39) );print s2

_='_=%r;print _%%_';print _%_


a = ['print "a =", a', 'for s in a: print s']
print "a =", a
for s in a: print s

l='l=%s;print l%%`l`';print l%`l`

x='x=%s\012print x%%`x`'
print x%`x`


q='"'
q1="'"
n='\n'
s='\\'
r1="def f(a,s1,s2,s3,s4):"
r2=" print a+'1='+q+s1+q+n+a+'2='+q+s2+q"
r3=" print a+'3='+q+s3+q+n+a+'4='+q+s4+q"
r4=" print s1+n+s2+n+s3+n+s4"
def f(a,s1,s2,s3,s4):
 print a+'1='+q+s1+q+n+a+'2='+q+s2+q
 print a+'3='+q+s3+q+n+a+'4='+q+s4+q
 print s1+n+s2+n+s3+n+s4
p1="print 'q='+q1+q+q1+n+'q1='+q+q1+q"
p2="print 'n='+q1+s+'n'+q1+n+'s='+q1+s+s+q1"
p3="f('r',r1,r2,r3,r4)"
p4="f('p',p1,p2,p3,p4)"
print 'q='+q1+q+q1+n+'q1='+q+q1+q
print 'n='+q1+s+'n'+q1+n+'s='+q1+s+s+q1
f('r',r1,r2,r3,r4)
f('p',p1,p2,p3,p4)


import sys;f=sys.stdout;
x='import sys;f=sys.stdout;x=%s;f.write(x%%`x`)';f.write(x%`x`)

