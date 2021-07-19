# This Python file uses the following encoding: utf-8
from buildbot.plugins import util


class StepFactory:
    def __init__(self, pwd):
        self.pwd = pwd
        self.array = []

    def insertToBegin(self, step):
        step.workdir = self.pwd
        self.array = [step] + self.array

    def addStep(self, step):
        step.workdir = self.pwd

        self.array += [step]

    def addSteps(self, steps):
        for step in steps:
            self.addStep(step)

    def source(self):
        factory = util.BuildFactory()
        for step in array:
            factory.addStep(step)

        factory.workdir = self.pwd

        return factory
