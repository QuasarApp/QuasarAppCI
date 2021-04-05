# This Python file uses the following encoding: utf-8

from BuildBotLib.make import Make
from BuildBotLib.secretManager import SecretManager


class QMake(Make):

    def __init__(self, platform):
        Make.__init__(self, platform)
#        self.buildSystems = self.B_QMake

    def makePrefix(self):
        return "Q"

    def mainCmd(self):
        command = [
            'qmake',
            "-r",
            "CONFIG+=qtquickcompiler",
            "CONFIG+=ccache",
            'ONLINE="~/repo"'
        ]

        return command

    def linuxXmakeCmd(self, props):
        return self.mainCmd()

    def windowsXmakeCmd(self, props):
        return self.mainCmd()

    def androidXmakeCmd(self, props):
        file = self.home + "/buildBotSecret/secret.json"
        secret = SecretManager(file, props)

        command = [
            'qmake',
            '-spec', 'android-clang',
            "-r",
            "CONFIG+=qtquickcompiler",
            'SIGN_PATH="' + secret.getValue('SIGPATH') + '"',
            'SIGN_ALIES="quasarapp"',
            'SIGN_STORE_PASSWORD="' + secret.getValue('SIGPASS') + '"',
            'ANDROID_ABIS=arm64-v8a'

        ]

        return command
