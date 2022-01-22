# This Python file uses the following encoding: utf-8

from BuildBotLib.cmake import CMake
from buildbot.plugins import util
from BuildBotLib.secretManager import SecretManager


class CMakeApple(CMake):

    def __init__(self, platform):
        CMake.__init__(self, platform)
#        self.buildSystems = self.B_CMake

    def makePrefix(self):
        return "XCode"

    def iosXmakeCmd(self, props):
        file = self.home + "/buildBotSecret/secret.json"
        secret = SecretManager(file, props)

        applePlatform = str(props.getProperty('ApplePlatform', ''))

        defines = self.getDefinesList(props)

        defines += secret.convertToCmakeDefines()

        defines += [
            '-DCMAKE_PREFIX_PATH=$QTDIR',
            '-DCMAKE_XCODE_ATTRIBUTE_DEVELOPMENT_TEAM=$XCODE_DEVELOPMENT_TEAM',
            '-DDEPLOYMENT_TARGET=$DEPLOYMENT_TARGET',
            '-DCMAKE_TOOLCHAIN_FILE=$CMAKE_TOOL_CHAIN_FILE',
            '-DPLATFORM=' + applePlatform,
            '-B cmake_build'
        ]

        options = [
            'cmake -G Xcode',
        ]
        options += defines

        return ' '.join(options)

    def getPropertyes(self):

        base = super().getPropertyes()

        return base + [
            util.StringParameter(
                name='ApplePlatform',
                label='Apple Platform (example OS64, SIMULATOR64)',
                default='OS64'
            ),
        ]
