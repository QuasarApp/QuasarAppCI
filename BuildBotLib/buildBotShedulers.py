# This Python file uses the following encoding: utf-8
from BuildBotLib.buildBotModule import *
from buildbot.schedulers import *
from buildbot.plugins import schedulers

class buildBotShedulers(BuildBotModule):
    codebases = {}
    shedulers = []
    def __init__(self):
        BuildBotModule.__init__(self)


    def addScheduler(self , prop, worker):
        shedulerName = 'force-' + worker;

        self.shedulers.append(
           schedulers.ForceScheduler(
                name = shedulerName,
                properties = prop,
                builderNames = [worker]
            )
        )


    def getShedulers(self, builders, prop):

        self.masterConf['schedulers'] = self.shedulers + [
            schedulers.AnyBranchScheduler(
                name='Tester',
                builderNames=builders,
                properties=prop,
                treeStableTimer = None
            )
        ]

        return self.getMasterConf();

