import threading
import Queue
import time
class Organ(object):
    pass


class Console(Organ):
    @staticmethod
    def output(t_struct):
        print('Console(Organ) output : ' + t_struct)

class Knowledge(Organ):
    @staticmethod
    def save(t_struct):
        print('Knowledge(Organ) save : ' + t_struct)


# command message [type,target,t_struct]
class Command_message(object):
    def __init__(self, type, target, t_struct):
        self.type = type
        self.target = target
        self.t_struct = t_struct


#command
class Command(object):
    def __init__(self, target):
        self.target = target

    def execute(self, t_struct):
        #print self
        if self.organs.has_key(self.target):
            self.organs[self.target](t_struct)


class SaveCommand(Command):
    def __init__(self, target):
        Command.__init__(self, target)
        self.organs = {'knowledge': Knowledge.save}
        pass

    def __str__(self):
        return 'save command:' + self.target


class OutputCommand(Command):
    def __init__(self, target):
        Command.__init__(self, target)
        self.organs = {'console': Console.output}

    def __str__(self):
        return 'output command:' + self.target


class CommandExec(threading.Thread):
    def __init__(self,queue):
        threading.Thread.__init__(self)
        self.commands = {'output': OutputCommand,
                         'save': SaveCommand}
        self.queue = queue

    def create_command(self, command_type, command_target):
        return self.commands.get(command_type)(command_target)

    def run(self):
        while True:
            command_message = self.queue.get()
            if isinstance(command_message, Command_message):
                command = self.create_command(command_message.type, command_message.target)
                command.execute(command_message.t_struct)
            self.queue.task_done()


if __name__ == '__main__':
    thread_number = 2
    q_command = Queue.Queue(maxsize=0)
    execs = [CommandExec(q_command) for x in range(thread_number)]
    for item in execs:
        item.setDaemon(True)
        item.start()
    q_command.join()

    while True:
        import random
        time.sleep(1)
        q_command.put(Command_message('save', 'knowledge', str(random.randint(10000,90000))))
        q_command.put(Command_message('output', 'console', str(random.randint(10000,90000))))