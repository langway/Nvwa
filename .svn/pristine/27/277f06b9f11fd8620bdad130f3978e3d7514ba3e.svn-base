#!/usr/bin/env python
# coding: utf-8
"""
项目入口
"""
from loongtian.nvwa.common.threadpool.runnable import run, Runnable
# from loongtian.nvwa.core.engines.rethinking.rethink_engine import RethinkEngine
# from loongtian.nvwa.core.minds.collection_mind import CollectionMind
# from loongtian.nvwa.core.minds.refer import Refer
# from loongtian.nvwa.core.minds.thinking import Thinking
# from loongtian.nvwa.service import original_init_srv
from loongtian.nvwa.core.gdef import GlobalDefine
# from loongtian.nvwa.core.minds.manage import Manage
from loongtian.nvwa.organs.extension.brain.tcp_console import ConsoleServerDeaMon
# from loongtian.nvwa.organs.extension.brain.tcp_manage import ManageServerDeaMon

__author__ = 'Liuyl'

class Brain(Runnable):
    ''' 
    大脑
    '''
    def __init__(self):
        super(Brain, self).__init__()
        self._name = "Brain"

    def _start_behavior(self):
        '''
        启动行为中枢
        '''
        thread_number = 1 # 可以同时打开的线程数
        q_command = GlobalDefine().command_msg
        from loongtian.nvwa.core.maincenter.behavior.behave import CommandExec

        execs = [CommandExec(q_command) for x in range(thread_number)]
        for item in execs:
            item.setDaemon(True) # 设置使用守护进程
            item.start()
        q_command.join() # 固定写法

    def _execute(self):
        '''
        重写父线程方法
        '''
        # # 判断数据库是否进行了初始化。
        # from loongtian.nvwa.common.storage.db.entity_repository import real_object_rep
        # if not real_object_rep.is_initiated():
        #     original_init_srv.init(for_test=True)
        #     real_object_rep.initial()
            
        # 初始化全局定义
        gd = GlobalDefine()
        # 启动任务调度（定时器） -- 遗忘
        # from loongtian.nvwa.core.sched import NvwaSched
        # NvwaSched(gd.console_output_queue).start()
        # TODO 都是同一个gd对象的，是否应该都移至到gd对象的init函数中去做？或者由一个方法初始化？
        gd.dispenser.register_queue(gd.manage_output_queue)
        gd.dispenser.register_queue(gd.console_output_queue)
        # 执行子线程
        self._sub_threads = [
            # CollectionMind(),
            # Thinking(),
            # Refer(),
            ConsoleServerDeaMon(),
            # Manage(),
            # ManageServerDeaMon(),
            gd.dispenser,
            # RethinkEngine(),
        ]
        map(lambda t: run(t), self._sub_threads) # 启动子线程，并put到线程池中。
        Runnable.pool.poll() # 通过线程池管理子线程，poll实现异步执行模式。

        # # 启动执行中枢
        # self._start_behavior()
        # 等待处理，如果state为False退出。
        while True:
            if not self.state():
                break

if __name__ == '__main__':
    brain = Brain()
    brain.run()