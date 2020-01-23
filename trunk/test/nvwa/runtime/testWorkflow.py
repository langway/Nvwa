#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Leon'


from unittest import TestCase
from loongtian.nvwa.runtime.workflow import Workflow,Step,Status

class TestWorkflow(TestCase):
    def setUp(self):
        print("----setUp----")

    def testCreateByCode(self):
        print("----testCreateByCode----")
        workflow = Workflow()
        step1 = Step()
        status1 =Status([1,2,3])
        step1.addStatus(status1)
        workflow.addStep(step1)

        print (workflow.toObjChain(forceToNvwaObject=False))

        status2 = Status(["a","b","c"])
        step1.addStatus(status2)
        print (workflow.toObjChain(forceToNvwaObject=False))

        step2 = Step()
        status3 = Status(["B", "C"])
        step2.addStatus(status3)
        workflow.addStep(step2)
        print (workflow.toObjChain(forceToNvwaObject=False))

    def testCreateByObjChain(self):

        workflow =Workflow.createByStepsObjChain([[[1, 2, 3], ['a', 'b', 'c']], [[u'A', u'B', u'C']]])
        print (workflow.toObjChain(forceToNvwaObject=False))

    def testCreateKnowledgeByObjChain(self):

        workflow =Workflow.createByStepsObjChain([[[1, 2, 3], ['a', 'b', 'c']], [[u'A', u'B', u'C']]])
        print (workflow.toObjChain())
        klg = workflow.createKnowledge(recordInDB=False,memory=workflow.Memory)
        print (klg.getSequenceComponents())