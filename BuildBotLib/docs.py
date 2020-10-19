# This Python file uses the following encoding: utf-8

from BuildBotLib.cmake import CMake
from buildbot.plugins import util, steps


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

        def mkDirProp(props):
            return str(props.getProperty('copyFolder'))

        res += [self.generateStep(mkDirProp,
                                  platform,
                                  'create dir ',
                                  self.isDeploy)]

        res += [steps.CopyDirectory(
                    src="docs/html",
                    dest=util.Interpolate('%(prop:copyFolder)s'))]

        return res

    def getPropertyes(self):

        base = super().getPropertyes()

        return base + [
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
