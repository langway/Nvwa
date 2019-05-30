# encoding: UTF-8

from time import sleep

from loongtian.util.rpc.vnrpc import RpcClient


########################################################################
class TestClient(RpcClient):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, reqAddress, subAddress):
        """Constructor"""
        super(TestClient, self).__init__(reqAddress, subAddress)
        
    #----------------------------------------------------------------------
    def callback(self, topic, data):
        """回调函数实现"""
        print ('client received topic:', topic, ', data:', str(data))
    
class testData():
    def __init__(self):
        self.content1=None
        self.content2 = None

    def __str__(self):
        return "testData:content1={0};content1={1}".format(str(self.content1),str(self.content2))

if __name__ == '__main__':
    reqAddress = 'tcp://localhost:2014'
    subAddress = 'tcp://localhost:0602'
    
    tc = TestClient(reqAddress, subAddress)
    tc.subscribeTopic('')
    if tc.start():

        while 1:
            print (tc.add(1, 3))
            sleep(2)