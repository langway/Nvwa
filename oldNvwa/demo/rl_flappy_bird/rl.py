#!/usr/bin/env python
# coding: utf-8
"""
Project:  FlappyBirdClone-master
Title:    rl 
Author:   Liuyl 
DateTime: 2015/2/26 10:43 
UpdateLog:
1、Liuyl 2015/2/26 Create this File.

rl
>>> print("No Test")
No Test
"""
from pybrain.rl.environments import Task, Environment
from pybrain.rl.learners.valuebased import ActionValueTable
from pybrain.rl.agents import LearningAgent
from pybrain.rl.learners import Q
from pybrain.rl.experiments import Experiment
from pybrain.utilities import Named
from runnable import Runnable
from Queue import Queue
from scipy import array

__author__ = 'Liuyl'


class Sky(Environment, Named):
    width = 0
    height = 0
    # current state
    perseus = None
    S = False
    J = True
    allActions = [S, J]

    def __init__(self, height, width, **args):
        self.setArgs(**args)
        self.width = width
        self.height = height
        self.out_of_sky = False
        self.reset()

    def reset(self):
        """ return to initial position (stochastically): """
        self.out_of_sky = False
        self.perseus = (0, 0)

    def performAction(self, action):
        rl.put_command(self.allActions[action])


class MDPSkyTask(Task):
    """ This is a MDP task for the MazeEnvironment. The state is fully observable,
        giving the agent the current position of perseus. Reward is given on reaching
        the goal, otherwise no reward. """

    def getReward(self):
        """ compute and return the current reward (i.e. corresponding to the last action performed) """
        state = rl.get_state()
        print(state)
        self.env.perseus = (state[0]/4 + 64, state[1]/4)
        if not state[2]:

            self.env.reset()
            reward = -1000.
            rl.put_command(True)
            rl.put_command(True)
        else:
            reward = 1.

        print(self.env.perseus)
        return reward

    def performAction(self, action):
        """ The action vector is stripped and the only element is cast to integer and given
            to the super class.
        """
        Task.performAction(self, int(action[0]))

    def getObservation(self):
        """ The agent receives its position in the maze, to make this a fully observable
            MDP problem.
        """
        obs = array([self.env.perseus[0] * self.env.width + self.env.perseus[1]])
        return obs


class RL(Runnable):
    def __init__(self):
        super(RL, self).__init__()
        self.state_queue = Queue()
        self.command_queue = Queue()
        self.environment = Sky(128, 60)
        self.controller = ActionValueTable(128 * 60, 2)
        self.controller.initialize(0.)
        self.learner = Q(0.7,1)
        self.learner.explorer.epsilon=0
        self.agent = LearningAgent(self.controller, self.learner)
        self.task = MDPSkyTask(self.environment)
        self.experiment = Experiment(self.task, self.agent)

    def put_state(self, pos, alive):
        self.state_queue.put((pos[0], pos[1], alive))

    def get_state(self):
        return self.state_queue.get()

    def put_command(self, jump):
        self.command_queue.put(jump)

    def get_command(self):
        return self.command_queue.get()

    def _execute(self):
        rl.put_command(True)
        while True:
            self.experiment.doInteractions(1000)
            self.agent.learn()
            self.agent.reset()


rl = RL()
if __name__ == '__main__':
    import doctest

    doctest.testmod()