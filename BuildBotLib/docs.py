# This Python file uses the following encoding: utf-8

from BuildBotLib.cmake import CMake
from buildbot.plugins import util


class Docs(CMake):

    def __init__(self, platform):
        CMake.__init__(self, platform)

    def generatePlatformSteps(self, platform):

        platformXcmd = {
            CMake.P_Linux: self.linuxXmakeCmd,
            CMake.P_Windows: self.windowsXmakeCmd,
            CMake.P_Android: self.androidXmakeCmd,
            CMake.P_Wasm: self.wasmXmakeCmd,
        }

        res = []

        res += [self.generateStep(platformXcmd[platform],
                                  platform,
                                  self.makePrefix() + 'Make',
                                  lambda step: True)]

        res += [self.generateStep(self.makeTarget('doc'),
                                  platform,
                                  'Generate docs for the project',
                                  self.isDeploy)]

        def move(props):
            return 'mv docs/* ' + str(props.getProperty('copyFolder'))

        res += [self.generateStep('mkdir -p Distro',
                          platform,
                          'make target dir',
                          self.isDeploy)]

        res += [self.generateStep(move,
                                  platform,
                                  'moveDocs',
                                  self.isDeploy)]

        return res

    def getPropertyes(self):

        return [
            util.BooleanParameter(
                name='deploy',
                label='deploy project',
                default=True
            ),
            util.StringParameter(
                name='copyFolder',
                label='Folder with buildet data',
                default="Distro"
            ),
        ]

    def destDirPrivate(self, props):
        repo = str(props.getProperty('repository'))
        branch = str(props.getProperty('branch'))

        name = branch
        if branch == "main" or branch == "master":
            name = "latest"

        return "docs/" + self.getNameProjectFromGitUrl(repo) + "/" + name
