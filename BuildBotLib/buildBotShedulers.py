# This Python file uses the following encoding: utf-8
from BuildBotLib.buildBotModule import BuildBotModule
from buildbot.plugins import schedulers


class BuildBotShedulers(BuildBotModule):
    codebases = {}
    shedulers = []

    def __init__(self, masterConf):
        BuildBotModule.__init__(self, masterConf)

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
                        'LinuxCMakeBuilder',
                        'AndroidCMakeBuilder',
                        'WindowsCMakeBuilder',
                        'Wasm32Builder',
                        ]

        buildersDeployCode = ['DocsGenerator']

        buildersRepo = ['RepoGen']
        self.masterConf['schedulers'] = self.shedulers

        self.masterConf['schedulers'] += [
            schedulers.AnyBranchScheduler(
                name='githubTest',
                builderNames=buildersCode,
                properties={
                    'clean': True,
                    'test': True,
                    'release': False,
                    'deploy': False
                },
                treeStableTimer=60
            ),

            schedulers.AnyBranchScheduler(
                name='githubDeploy',
                builderNames=buildersDeployCode,
                properties={
                    'clean': True,
                    'test': True,
                    'release': False,
                    'deploy': True
                },
                treeStableTimer=60
            ),

            schedulers.Triggerable(name="repogen",
                                   builderNames=buildersRepo)
        ]

        return self.getMasterConf()
