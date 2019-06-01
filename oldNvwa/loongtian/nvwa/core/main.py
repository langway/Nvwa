#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    main 
Author:   fengyh 
DateTime: 2014/8/20 11:07 
UpdateLog:
1、fengyh 2014/8/20 Create this File.


"""

from loongtian.nvwa.common.threadpool.runnable import run, Runnable
from loongtian.nvwa.service import original_init_srv
from loongtian.nvwa.core.gdef import GlobalDefine


class MainThread(Runnable):
    def __init__(self):
        super(MainThread, self).__init__()
        self._name = "MainThread"

    def _start_behavior(self):
        thread_number = 2
        q_command = GlobalDefine().command_msg
        from loongtian.nvwa.core.maincenter.behavior.behave import CommandExec

        execs = [CommandExec(q_command) for x in range(thread_number)]
        for item in execs:
            item.setDaemon(True)
            item.start()
        q_command.join()

    def _execute(self):
        original_init_srv.init()
        gd = GlobalDefine()
        input_msg = gd.console_input_queue
        output_msg = gd.console_output_queue
        main_msg = gd.manage_input_queue

        # 启动任务调度
        from loongtian.nvwa.core.sched import NvwaSched

        NvwaSched(output_msg).start()
        from loongtian.nvwa.input.consoleInput import ConsoleInput
        from loongtian.nvwa.output.consoleOutput import ConsoleOutput
        from loongtian.nvwa.core.minds.thinking import Thinking

        self._sub_threads = [ConsoleOutput(output_msg),
                             Thinking(input_msg, output_msg),
                             ConsoleInput(input_msg, main_msg), ]
        # RethinkEngine()]
        map(lambda t: run(t), self._sub_threads)
        Runnable.pool.poll()

        # 启动执行中枢
        self._start_behavior()

        from loongtian.nvwa.service import command_srv

        while True:
            if not main_msg.empty():
                command_srv.execute_command(main_msg.get(), self)
            if not self.state():
                break


if __name__ == '__main__':
    main_thread = MainThread()
    main_thread.run()
