# This Python file uses the following encoding: utf-8
from BuildBotLib.buildBotModule import *
from buildbot.schedulers import *
from buildbot.plugins import schedulers, util

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


    def initScheduler(self):

        self.masterConf['schedulers'] = self.shedulers + [
            schedulers.AnyBranchScheduler(
                name='Tester',
                builderNames=['Tester'],
                properties= {
                    'clean': True,
                    'test': True,
                    'release': False,
                    'deploy': False,
                    'Linux': True,
                    'Windows': True,
                    'Android': True

                },
                change_filter=util.ChangeFilter(project_re='*-qmake'),
                treeStableTimer = None
            ),
            schedulers.SingleBranchScheduler(
                name='NPM Deployer',
                change_filter=util.ChangeFilter(branch='master', project='Chat-npm'),
                builderNames=['NPM'],
                properties = {},
                treeStableTimer = None
            )

        ]

        return self.getMasterConf();


