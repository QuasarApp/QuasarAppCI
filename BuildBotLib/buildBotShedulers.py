# This Python file uses the following encoding: utf-8
from BuildBotLib.buildBotModule import BuildBotModule
from buildbot.plugins import schedulers, util


class BuildBotShedulers(BuildBotModule):
    codebases = {}
    shedulers = []

    def __init__(self):
        BuildBotModule.__init__(self)

    def addScheduler(self, prop, worker):

        shedulerName = 'force-' + worker

        self.shedulers.append(
           schedulers.ForceScheduler(
                name=shedulerName,
                properties=prop,
                builderNames=[worker]
            )
        )

    def initScheduler(self):

        self.masterConf['schedulers'] = self.shedulers + [
            schedulers.AnyBranchScheduler(
                name='github',
                change_filter=util.ChangeFilter(project_re="qmake-*"),
                builderNames=['LinuxBuilder',
                              'AndroidBuilder',
                              'WindowsBuilder',
                              ],
                properties={
                    'clean': True,
                    'test': True,
                    'release': False,
                    'deploy': False,
                    'Linux': True,
                    'Windows': True,
                    'Android': True

                },
                treeStableTimer=None
            ),

        ]

        return self.getMasterConf()
