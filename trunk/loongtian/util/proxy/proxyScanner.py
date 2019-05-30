# -*- coding:utf-8 -*-
"""
	@name	Base Functions
	@modify	2014/11/27
	@author	Holger
	@github	https://github.com/h01/ProxyScanner
	@myblog	http://ursb.org
"""
import Queue
import socket
import threading

from ipsGenerator import ipsGenerator
from loongtian.util.helper.outputer import *
import loongtian.util.helper.threadHelper as threadHelper
import loongtian.util.proxy.proxyChecker as proxyChecker

ipgen = ipsGenerator()
cor = ColorSetter()

testAddress=[
    "http://club.china.com/favicon.ico", # 中华网 大小：1406b
    "http://www.weather.com.cn/favicon.ico", # 天气预报 大小：894b
]

class ProxyScanner:
    """
    代理扫描器。
    """

    def __init__(self):
        self._port = 8080 # 端口
        self._threadNum = 10 # 线程数
        self._ips = [] # 要扫描的网段
        self._openIps = [] # 检查到的开放ip
        self._checkedProxies = [] # 已经过验证的代理列表
        self._fileNameToSave = '' # 要将结果保存到的文件名

    def run(self, opts):
        """
        供命令行调用的启动扫描程序的入口
        :rawParam opts: 命令行参数
        :return:
        """
        for k, v in opts:
            if k in ['-v', '--version']:
                self.version()
            elif k in ['-p', '--port']:
                self._port = int(v)
            elif k in ['-i', '--ips']:
                _temp = v.split('-')
                self._ips = ipgen.gen(_temp[0], _temp[1])
            elif k in ['-t', '--thread']:
                self._threadNum = int(v)
            elif k in ['-s', '--save']:
                self._fileNameToSave = v
            else:
                self.usage()
        if (65535 >= self._port > 0) and (100 >= self._threadNum > 0) and (len(self._ips) > 0):
            self.start()
        else:
            self.usage()

    def runScanner(self,ips,port,threadNum,fileName=None):
        """
        供程序调用的启动扫描程序的入口
        :rawParam ips: 要扫描的网段 eg:1.1.1.1-1.1.2.255
        :rawParam port: 端口
        :rawParam threadNum: 线程数
        :rawParam fileName: 要将结果保存到的文件名
        :return:
        """

        self._port = port # 端口
        self._threadNum = threadNum # 线程数
        _temp = ips.split('-')
        self._ips = ipgen.gen(_temp[0], _temp[1])# 生成ip列表

        self._openIps = [] # 检查到的开放ip
        self._checkedProxies = [] # 已经过验证的代理列表
        self._fileNameToSave = fileName # 要将结果保存到的文件名
        if (65535 >= self._port > 0) and (100 >= self._threadNum > 0) and (len(self._ips) > 0):
            self.start()

    def start(self):
        Outputer.w('Proxy Scanner started')
        Outputer.i('Nums: %s' % len(self._ips))
        Outputer.i('Port: %s' % self._port)
        Outputer.i('Thread: %s' % self._threadNum)


        self.scanports()
        proxyChecker.checkProxy(self._openIps,self._threadNum,self._checkedProxies)
        self.result()

    def scanports(self):
        Outputer.w('Start scanning the open port\'s IP..')

        def run(q):
            while not q.empty():
                _ip = q.get()
                if self.checkPort(_ip, self._port):
                    Outputer.s('Open: %s' % _ip)

                    self._openIps.append("%s:%s" % (_ip, self._port))
                else:
                    Outputer.e('Close: %s' % _ip)


        threadHelper.startThread(self._ips, run,self._threadNum)





    def checkPort(self, host, port):
        try:
            _s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            _s.settimeout(3)
            _s.connect((host, int(port)))
            _s.close()
            return True
        except:
            return False


    def result(self):
        if len(self._checkedProxies) > 0:
            Outputer.i('Scan result:')

            for _r in self._checkedProxies:
                print ("\t%s:%s" % (_r, self._port))
            if self._fileNameToSave != '':
                _f = open(self._fileNameToSave, 'a')
                for _r in self._checkedProxies:
                    _f.write('%s:%s\n' % (_r, self._port))
                _f.close()
                Outputer.s('Save as (%s)' % self._fileNameToSave)

        else:
            Outputer.i('Not result!')

        if not __debug__:
            exit(0)

    def banner(self):
        return """\
	______                    _____                                 
	| ___ \                  /  ___|                                
	| |_/ / __ _____  ___   _\ `--.  ___ __ _ _ __  _ __   ___ _ __ 
	|  __/ '__/ _ \ \/ / | | |`--. \/ __/ _` | '_ \| '_ \ / _ \ '__|
	| |  | | | (_) >  <| |_| /\__/ / (_| (_| | | | | | | |  __/ |   
	\_|  |_|  \___/_/\_\\\\__, \____/ \___\__,_|_| |_|_| |_|\___|_|   
	                     __/ |                                      
	                    |___/                                       """

    def usage(self):
        cor.p(self.banner(), cor.RED)
        cor.p('PS 1.0 (Proxy Scanner)', cor.GREEN)
        cor.p('\tAuthor: Holger', cor.YELLOW)
        cor.p('\tModify: 2014/11/27', cor.YELLOW)
        cor.p('\tGitHub: https://github.com/h01/ProxyScanner', cor.YELLOW)
        cor.p('\tMyBlog: http://ursb.org', cor.YELLOW)
        cor.p('\tVersion: 1.0', cor.RED)
        cor.p('Usage: ./ps [args] [value]', cor.GREEN)
        cor.p('Args: ', cor.PURPLE)
        cor.p('\t-v --version\t\tPS version')
        cor.p('\t-h --help\t\tHelp menu')
        cor.p('\t-i --ips\t\tIPS: 192.168.1.1-192.168.1.100')
        cor.p('\t-p --port\t\tProxy port (default:8080)')
        cor.p('\t-t --thread\t\tScan thread (default:10)')
        cor.p('\t-s --save\t\tSave scan result')
        if not __debug__:
            exit(0)

    def version(self):
        Outputer.i('ProxyScanner version 1.0')

        if not __debug__:
            exit(0)
