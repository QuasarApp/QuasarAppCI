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

        buildersCode = ['LinuxBuilder',
                        'AndroidBuilder',
                        'WindowsBuilder',
                        ]

        buildersCode = ['LinuxCMakeBuilder',
                        'AndroidCMakeBuilder',
                        'WindowsCMakeBuilder',
                        ]

        buildersRepo = ['RepoGen']
        self.masterConf['schedulers'] = self.shedulers

        self.masterConf['schedulers'] += [
            schedulers.AnyBranchScheduler(
                name='githubQmake',
                change_filter=util.ChangeFilter(project_re="qmake-*"),
                builderNames=buildersCode,
                properties={
                    'clean': True,
                    'test': True,
                    'release': False,
                    'deploy': False
                },
                treeStableTimer=None
            ),

            schedulers.AnyBranchScheduler(
                name='githubCmake',
                change_filter=util.ChangeFilter(project_re="cmake-*"),
                builderNames=buildersCode,
                properties={
                    'clean': True,
                    'test': True,
                    'release': False,
                    'deploy': False
                },
                treeStableTimer=None
            ),

            schedulers.Triggerable(name="repogen",
                                   builderNames=buildersRepo)
        ]

        return self.getMasterConf()
