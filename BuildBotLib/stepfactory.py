# This Python file uses the following encoding: utf-8
from buildbot.plugins import util


class StepFactory:
    def __init__(self, pwd):
        self.factory = util.BuildFactory()
        self.factory.workdir = pwd
        self.pwd = pwd

    def addStep(self, step):
        step.workdir = self.pwd

        self.factory.addStep(step)

    def addSteps(self, steps):
        for step in steps:
            self.addStep(step)

    def source(self):
        return self.factory
