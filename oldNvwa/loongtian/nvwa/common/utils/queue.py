#!/usr/bin/env python
# coding: utf-8
"""
女娲优先级队列模块

Project:  nvwa
Title:    queue.py 
Created by zheng on 2014/11/19.
UpdateLog:

"""
import Queue
# from Queue import PriorityQueue
import itertools

class PriorityQueue(Queue.PriorityQueue):
    '''
    为直观，相比PriorityQueue修改参数
    添加计数器，由于PriorityQueue为heapq实现，排序是不完全的，不能保证相同优先级的fifo。
    counter 计数器
    '''
    def __init__(self):
        Queue.PriorityQueue.__init__(self)

        self.counter = itertools.count()

    def put(self, item, priority=0, block=True, timeout=None):
        '''
        入队列，向队列中加入item，其加入位置由priority（优先级）指定。
        '''
        if not self._qsize():
            self.counter = itertools.count()

        Queue.PriorityQueue.put(self, (priority,self.counter.next(),item), block=True, timeout=None)
        
    def get(self, block=True, timeout=None):
        '''
        出队列
        '''
        return  Queue.PriorityQueue.get(self)[-1]

if __name__ == '__main__':
    import random
    bb=PriorityQueue()

    for i in reversed(range(100)):
        bb.put(int(i/2),random.randint(1,10))

    while not bb.empty():
        print(bb.get())