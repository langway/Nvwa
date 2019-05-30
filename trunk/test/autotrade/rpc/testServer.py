# encoding: UTF-8

from time import sleep, time

from loongtian.util.rpc.vnrpc import RpcServer


########################################################################
class TestServer(RpcServer):
    """测试服务器"""

    #----------------------------------------------------------------------
    def __init__(self, repAddress, pubAddress):
        """Constructor"""
        super(TestServer, self).__init__(repAddress, pubAddress)

        self.register(self.add)

    #----------------------------------------------------------------------
    def add(self, a, b):
        """测试函数"""
        print ('receiving: %s, %s' % (a,b))
        return a + b

class testData():
    def __init__(self):
        self.content1=None
        self.content2 = None

    def __str__(self):
        return "testData:content1={0};content1={1}".format(str(self.content1),str(self.content2))

if __name__ == '__main__':
    repAddress = 'tcp://127.0.0.1:2014'
    pubAddress = 'tcp://127.0.0.1:0602'
    
    ts = TestServer(repAddress, pubAddress)
    ts.start()

    num=0
    while 1:
        data=testData()
        data.content1 = 'server time is %s' % time()
        data.content2=num
        print (data)
        ts.publish('test', data)
        num+=1
        sleep(2)

    ts.stop()