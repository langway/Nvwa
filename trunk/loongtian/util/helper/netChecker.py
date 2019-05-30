#!/usr/bin/python
# encoding=utf-8
# Filename: net_is_normal.py
import os
import socket
import subprocess

#判断网络是否正常
server='www.baidu.com'
#检测服务器是否能ping通，在程序运行时，会在标准输出中显示命令的运行信息
def pingServer(server):
    result=os.system('ping '+server+' -c 2')
    if result:
        print (u'服务器%s ping fail' % server)
    else:
        print (u'服务器%s ping ok' % server)
    print (result)
#把程序输出定位到/dev/null,否则会在程序运行时会在标准输出中显示命令的运行信息
def pingServerCall(server):
    fnull = open(os.devnull, 'w')
    result = subprocess.call('ping '+server+' -c 2', shell = True, stdout = fnull, stderr = fnull)
    if result:
        print (u'服务器%s ping fail' % server)
    else:
        print (u'服务器%s ping ok' % server)
    fnull.close()

def check_address_aliveness(address):

    if not type(address) is str:
        return False

    s=address.split(":")
    if len(s)==2:
        ip=s[0].lstrip("//")
        port=int(s[1])
        return check_host_aliveness(ip, port)
    elif len(s)==3:
        ip=s[1].lstrip("//")
        port=int(s[2])
        return check_host_aliveness(ip, port)
    else:
        print ("不是合法的网络地址，格式应该为：tcp://localhost:2014")
        return False


def check_host_aliveness(ip, port):
    """
    可用于检测程序是否正常，如检测redis是否正常，即检测redis的6379端口是否正常
    再如：检测ssh是否正常，即检测ssh的22端口是否正常
    :param ip:
    :param port:
    :return:
    """
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.settimeout(1)
    try:
        sk.connect((ip,port))
        print ('server %s:%d service is OK!' %(ip,port))
        return True
    except Exception as ex:
        print ('server %s:%d service is NOT OK!'  %(ip,port))
        return False
    finally:
        sk.close()
    return False

if __name__=='__main__':
    # pingServerCall(server)
    # pingServer(server)
    check_host_aliveness('192.168.230.128', 6379)