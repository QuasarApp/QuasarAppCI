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

        buildersCode = ['AndroidBuilder_v8Qt6',
                        'LinuxCMakeBuilderQt6',
                        'WindowsCMakeBuilder',
                        'Wasm32Builder',
                        'IOSCMakeBuilder',
                        ]

        prodBuilders = ['AndroidBuilder_v8Qt6',
                        'LinuxCMakeBuilderQt6',
                        'WindowsCMakeBuilder',
                        'IOSCMakeBuilder'
                        ]

        webBuilders = ['LinuxCMakeBuilderQt6']

        buildersDeployCode = ['DocsGenerator']
        buildersReleaseCode = ['prodDeployer']
        buildersReleaseWebCode = ['webDeployer']

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
                    'repogen': False,
                    'prodDeploer': False,
                    'deploy': False,
                    'stopOnErrors': True
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
                    'repogen': False,
                    'prodDeploer': False,
                    'deploy': True,
                    'copyFolder': 'Distro',
                    'stopOnErrors': True

                },
                treeStableTimer=60
            ),

            schedulers.SingleBranchScheduler(
                name='production',
                change_filter=util.ChangeFilter(branch="prod"),
                builderNames=prodBuilders,
                properties={
                    'clean': True,
                    'test': True,
                    'release': False,
                    'repogen': False,
                    'prodDeploer': True,
                    'deploy': True,
                    'copyFolder': 'Distro',
                    'stopOnErrors': True

                },
                treeStableTimer=70
            ),

            schedulers.SingleBranchScheduler(
                name='productionWeb',
                change_filter=util.ChangeFilter(repository_re=".*quasarappsite.*", branch="prod"),
                builderNames=webBuilders,
                properties={
                    'clean': True,
                    'test': True,
                    'release': False,
                    'repogen': False,
                    'webDeploer': True,
                    'deploy': True,
                    'copyFolder': 'Distro',
                    'stopOnErrors': True

                },
                treeStableTimer=70
            ),


            schedulers.Triggerable(name="repogen",
                                   builderNames=buildersRepo),

            schedulers.Triggerable(name="releaser",
                                   builderNames=buildersReleaseCode)

            schedulers.Triggerable(name="releaserweb",
                                  builderNames=buildersReleaseWebCode)

        ]

        return self.getMasterConf()
