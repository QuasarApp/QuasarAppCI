# This Python file uses the following encoding: utf-8

from BuildBotLib.basemodule import BaseModule

from buildbot.plugins import util, steps
from BuildBotLib.secretManager import SecretManager
import hashlib


class Make(BaseModule):
    def __init__(self, platform):
        BaseModule.__init__(self,
                            platform,
                            self.getProject())
        self.tempRepoDir = ""

    def getProject(self):

        @util.renderer
        def cmdWraper(step):
            repository = step.getProperty('repository')
            project = self.getNameProjectFromGitUrl(repository)
            if not len(project):
                return "build"

            return project

        return cmdWraper

    def isSupport(self, step):
        return True

    def isDeploy(self, step):
        return step.getProperty('deploy')

    def isRelease(self, step):
        return step.getProperty('release')

    def isTest(self, step):
        return step.getProperty('test')

    def getNameProjectFromGitUrl(self, repository):
        if not len(repository):
            return ""

        repository = repository.replace('.git', '')
        begin = repository.rfind('/')
        begin = max(repository.rfind('/', 0, begin),
                    repository.rfind(':', 0, begin))

        if begin < 0:
            return ""

        project = repository[begin + 1:len(repository)]
        return project

    def getLastRepoName(self, url):
        fullName = self.getNameProjectFromGitUrl(url)
        array = fullName.split('/')
        if len(array) <= 0:
            return ""

        return array[-1]

    def destDirPrivate(self, props):
        repo = str(props.getProperty('repository'))
        got_revision = str(props.getProperty('got_revision'))

        name = got_revision

        return self.getNameProjectFromGitUrl(repo) + "/" + name

    def tempDirPrivate(self, props):
        repo = str(props.getProperty('repository'))
        got_revision = str(props.getProperty('got_revision'))

        name = got_revision

        m = hashlib.md5()
        repoPath = self.getLastRepoName(repo) + "/" + name

        m.update(repoPath.encode('utf-8'))

        return m.hexdigest()

    def destDir(self, props):
        return '/var/www/builds/' + self.destDirPrivate(props)

    def tempDir(self, props):
        self.tempRepoDir = self.home + '/rTemp/' + self.tempDirPrivate(props)
        return self.tempRepoDir

    def destDirUrl(self, props):
        return "https://quasarapp.ddns.net:3031/" + self.destDirPrivate(props)

    def permission(self):
        return ["chmod", "-R", "775", '/var/www/builds/']

    def linuxXmakeCmd(self, props):
        command = [
            'qmake-linux',
            "-r",
            "CONFIG+=qtquickcompiler",
            'ONLINE="~/repo"'
        ]

        return command

    def wasmXmakeCmd(self, props):
        return []

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
        file = self.home + "/buildBotSecret/secret.json"
        secret = SecretManager(file, props)

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

    def wasmXmakeEnv(self, props):
        return {}

    def windowsXmakeEnv(self, props):
        return {}

    def linuxXmakeEnv(self, props):
        return {}

    def makePrefix(self):
        return "X"

    def generateStep(self, cmd, platform, desc, checkFunc, log=False):

        @util.renderer
        def envWraper(step):

            platformEnv = {
                BaseModule.P_Linux: self.linuxXmakeEnv,
                BaseModule.P_Windows: self.windowsXmakeEnv,
                BaseModule.P_Android: self.androidXmakeEnv,
                BaseModule.P_Wasm: self.wasmXmakeEnv,

            }

            return platformEnv[platform](step)

        def dustepIf(step):
            return checkFunc(step) and self.isSupport(step)

        res = steps.Compile(
            command=self.getWraper(cmd),
            haltOnFailure=True,
            doStepIf=lambda step: dustepIf(step),
            hideStepIf=lambda results, step: not dustepIf(step),
            name=desc + ' ' + platform,
            env=envWraper,
            want_stdout=True,
            want_stderr=True,
            warningPattern=".*[Ww]arning[: ].*",
            description=desc,
        )

        if log:
            res = steps.Compile(
                command=self.getWraper(cmd),
                haltOnFailure=True,
                doStepIf=lambda step: dustepIf(step),
                hideStepIf=lambda results, step: not dustepIf(step),
                name=desc + ' ' + platform,
                env=envWraper,
                want_stdout=True,
                want_stderr=True,
                logfiles={"LogFile": "buildLog.log"},
                warningPattern=".*[Ww]arning[: ].*",
                description=desc,
            )

        return res

    def generatePlatformSteps(self, platform):

        platformXcmd = {
            BaseModule.P_Linux: self.linuxXmakeCmd,
            BaseModule.P_Windows: self.windowsXmakeCmd,
            BaseModule.P_Android: self.androidXmakeCmd,
            BaseModule.P_Wasm: self.wasmXmakeCmd,

        }

        res = []

        res += [self.generateStep(platformXcmd[platform],
                                  platform,
                                  self.makePrefix() + 'Make',
                                  lambda step: True)]

        res += [self.generateStep(self.makeCommand,
                                  platform,
                                  'Make',
                                  lambda step: True)]

        res += [self.generateStep(self.makeTarget('deploy'),
                                  platform,
                                  'deploy project',
                                  self.isDeploy)]

        res += [self.generateStep(self.makeTarget('test'),
                                  platform,
                                  'test project',
                                  self.isTest,
                                  True)]

        res += [self.generateStep(self.makeTarget('release'),
                                  platform,
                                  'release project',
                                  self.isRelease)]

        if platform != BaseModule.P_Android:

            res += [steps.DirectoryUpload(
                workersrc=util.Interpolate('%(prop:repoFolder)s'),
                masterdest=self.getWraper(self.tempDir),
                doStepIf=self.getWraper(self.isRelease),
                name='copy repository files',
                description='copy repository files to temp folder',
            )]

            @util.renderer
            def tempDirProp(props):
                return self.tempRepoDir

            @util.renderer
            def projectName(props):
                repo = str(props.getProperty('repository'))
                return self.getLastRepoName(repo)

            @util.renderer
            def repoLocation(props):
                return self.defaultLocationOfQIFRepository()

            res += [steps.Trigger(schedulerNames=['repogen'],
                                  doStepIf=lambda step:
                                      self.isRelease(step) and
                                      self.isSupport(step),
                                  set_properties={"tempPackage": tempDirProp,
                                                  "platform": platform,
                                                  "projectName": projectName,
                                                  "repoLocation": repoLocation}
                                  )]

            res += [steps.Trigger(schedulerNames=['releaser'],
                                doStepIf=lambda step:
                                    self.isRelease(step) and
                                    self.isSupport(step),
                                )]

        return res

    def getFactory(self):
        factory = super().getFactory()

        factory.addStep(
            steps.Git(
                repourl=util.Interpolate('%(prop:repository)s'),
                branch=util.Interpolate('%(prop:branch)s'),
                mode='full',
                method='fresh',
                clobberOnFailure=True,
                submodules=True,
                retryFetch=True,
                name='git operations',
                description='operations of git like pull clone fetch',
            )
        )

#        factory.addStep(self.checkSupportedBuildSystems())
        factory.addSteps(self.generatePlatformSteps(self.platform))

        factory.addStep(
            steps.DirectoryUpload(
                workersrc=util.Interpolate('%(prop:copyFolder)s'),
                masterdest=self.getWraper(self.destDir),
                url=self.getWraper(self.destDirUrl),
                doStepIf=self.getWraper(self.isDeploy),
                name='copy buildet files',
                description='copy buildet files to shared folder',
            )
        )

        factory.addStep(
            self.generateStep("git clean -xdf",
                              self.platform,
                              'Clean',
                              lambda step: True)
        )

        factory.addStep(
            self.generateStep("git submodule foreach --recursive git clean -xdf",
                              self.platform,
                              'Clean submodules',
                              lambda step: True)
        )

        return factory

    def getDefinesList(self, props):
        return str(props.getProperty('defines', '')).split(' ')

    def getPropertyes(self):

        base = super().getPropertyes()

        return base + [
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
            util.StringParameter(
                name='repoFolder',
                label='Folder with repository data',
                default="Repo"
            ),
            util.StringParameter(
                name='defines',
                label='Custom Defines list: Example: -DHANOI_ADMOD=1',
                default=""
            ),
        ]
