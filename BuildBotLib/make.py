# This Python file uses the following encoding: utf-8

from BuildBotLib.basemodule import BaseModule

from buildbot.plugins import util, steps
import datetime
from BuildBotLib.secretManager import SecretManager


class Make(BaseModule):
    def __init__(self):
        BaseModule.__init__(self)

    def isClean(self, step):
        return step.getProperty('clean')

    def isDeploy(self, step):
        return step.getProperty('deploy')

    def isRelease(self, step):
        return step.getProperty('release')

    def isTest(self, step):
        return step.getProperty('test')

    def destDirPrivate(self, props):
        repo = str(props.getProperty('repository'))
        now = datetime.datetime.now().strftime("(%H_%M)_%m-%d-%Y")

        return repo[repo.rfind('/'): len(repo) - 4] + "/" + now

    def destDir(self, props):

        return self.home + '/shared/' + self.destDirPrivate(props)

    def destDirUrl(self, props):
        return "http://quasarapp.ddns.net:3031" + self.destDirPrivate(props)

    def permission(self):
        return ["chmod", "-R", "775", self.home + '/shared']

    def linuxXmakeCmd(self, props):
        command = [
            'qmake-linux',
            "-r",
            "CONFIG+=qtquickcompiler",
            'ONLINE="~/repo"'
        ]

        return command

    def windowsXmakeCmd(self, props):
        command = [
            'qmake-windows',
            '-spec', 'win32-g++',
            "-r",
            "CONFIG+=qtquickcompiler",
            'ONLINE="~/repo"'
        ]

        return command

    def androidXmakeCmd(self, props):
        secret = SecretManager(self.home + "/buildBotSecret/secret.json")

        command = [
            'qmake-android',
            '-spec', 'android-clang',
            "-r",
            "CONFIG+=qtquickcompiler",
            'SIGN_PATH="' + secret.getValue('SIGPATH') + '"',
            'SIGN_ALIES="quasarapp"',
            'SIGN_STORE_PASSWORD="' + secret.getValue('SIGPASS') + '"'

        ]

        return command

    def androidXmakeEnv(self, props):
        return {}

    def windowsXmakeEnv(self, props):
        return {}

    def linuxXmakeEnv(self, props):
        return {}

    def makePrefix(self):
        return "X"

    def generateStep(self, cmd, platform, desc, checkFunc):

        platformCgek = {
            'linux': self.isLinux,
            'windows': self.isWin,
            'android': self.isAndroid,
        }

        @util.renderer
        def envWraper(step):

            platformEnv = {
                'linux': self.linuxXmakeEnv,
                'windows': self.windowsXmakeEnv,
                'android': self.androidXmakeEnv,
            }

            return platformEnv[platform](step)

        def dustepIf(step):
            return checkFunc(step) and platformCgek[platform](step)

        @util.renderer
        def cmdWraper(step):
            if not callable(cmd):
                return cmd

            return cmd(step)

        res = steps.ShellCommand(
            command=cmdWraper,
            haltOnFailure=True,
            doStepIf=lambda step: dustepIf(step),
            hideStepIf=lambda results, step: not dustepIf(step),
            name=desc + ' ' + platform,
            env=envWraper,
            description=desc,
        )

        return res

    def generatePlatformSteps(self, platform):

        platformXcmd = {
            'linux': self.linuxXmakeCmd,
            'windows': self.windowsXmakeCmd,
            'android': self.androidXmakeCmd,
        }

        res = []

        res += [self.generateStep(platformXcmd[platform],
                                  platform,
                                  self.makePrefix() + 'Make',
                                  lambda step: True)]

        res += [self.generateStep('make clean',
                                  platform,
                                  'clean old data',
                                  self.isClean)]

        res += [self.generateStep(self.makeCommand,
                                  platform,
                                  'Make',
                                  lambda step: True)]

        res += [self.generateStep('make deploy',
                                  platform,
                                  'deploy project',
                                  self.isDeploy)]

        res += [self.generateStep('make test',
                                  platform,
                                  'test project',
                                  self.isTest)]

        res += [self.generateStep('make release',
                                  platform,
                                  'release project',
                                  self.isRelease)]

        res += [self.generateStep('make distclean',
                                  platform,
                                  'clear all data',
                                  lambda step: True)]

        return res

    def getFactory(self):
        factory = super().getFactory()

        factory.addStep(
            steps.Git(
                repourl=util.Interpolate('%(prop:repository)s'),
                branch=util.Interpolate('%(prop:branch)s'),
                mode='full',
                method='fresh',
                submodules=True,
                name='git operations',
                description='operations of git like pull clone fetch',
            )
        )

        factory.addSteps(self.generatePlatformSteps('linux'))
        factory.addSteps(self.generatePlatformSteps('windows'))
        factory.addSteps(self.generatePlatformSteps('android'))

        factory.addStep(
            steps.DirectoryUpload(
                workersrc=util.Interpolate('%(prop:copyFolder)s'),
                masterdest=self.getRendererWraper(self.destDir),
                url=self.getRendererWraper(self.destDirUrl),
                doStepIf=self.getRendererWraper(self.isDeploy),
                name='copy buildet files',
                description='copy buildet files to shared folder',
            )
        )

        factory.addStep(
            steps.ShellCommand(
                command=self.permission(),
                name='set permission',
                haltOnFailure=True,

                description='set permission for shared folder',
            )
        )

        return factory

    def getPropertyes(self):

        base = super().getPropertyes()

        return base + [
            util.BooleanParameter(
                name='clean',
                label='clean old build ',
                default=True
            ),
            util.BooleanParameter(
                name='deploy',
                label='deploy project',
                default=True
            ),
            util.BooleanParameter(
                name='test',
                label='test project ',
                default=True
            ),
            util.BooleanParameter(
                name='release',
                label='release project',
                default=False
            ),
            util.StringParameter(
                name='copyFolder',
                label='Folder with buildet data',
                default="Distro"
            ),

        ]
