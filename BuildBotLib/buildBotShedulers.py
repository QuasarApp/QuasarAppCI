# This Python file uses the following encoding: utf-8
from BuildBotLib.buildBotModule import BuildBotModule
from buildbot.plugins import schedulers
from buildbot.plugins import util


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
                        'AndroidBuilder_v7',
                        'AndroidBuilder_v8',
                        'AndroidBuilder_v8Qt6',
                        'WindowsBuilder',
                        'LinuxCMakeBuilder',
                        'LinuxCMakeBuilderQt6',
                        'WindowsCMakeBuilder',
                        'Wasm32Builder',
                        ]

        buildersDeployCode = ['DocsGenerator']
        buildersReleaseCode = ['prodDeployer']


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
                    'deploy': True,
                    'copyFolder': 'Distro'
                },
                treeStableTimer=60
            ),

            schedulers.SingleBranchScheduler(
                name='release',
                change_filter=util.ChangeFilter(branch="prod"),
                builderNames=buildersReleaseCode,
                properties={
                    'copyFolder': 'Distro',
                    'prodName': 'prod.deb'
                },
                treeStableTimer=1200
            ),

            schedulers.Triggerable(name="repogen",
                                   builderNames=buildersRepo)
        ]

        return self.getMasterConf()
