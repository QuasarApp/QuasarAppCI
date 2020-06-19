# This Python file uses the following encoding: utf-8

from BuildBotLib.make import Make
from BuildBotLib.secretManager import SecretManager
import glob


class QMake(Make):

    def __init__(self, platform):
        Make.__init__(self, platform)

    def makePrefix(self):
        return "Q"

    def isSupport(self, step):
        return len(glob.glob1('.', '*.pro')) > 0

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
        secret = SecretManager(self.home + "/buildBotSecret/secret.json")

        command = [
            'qmake',
            '-spec', 'android-clang',
            "-r",
            "CONFIG+=qtquickcompiler",
            'SIGN_PATH="' + secret.getValue('SIGPATH') + '"',
            'SIGN_ALIES="quasarapp"',
            'SIGN_STORE_PASSWORD="' + secret.getValue('SIGPASS') + '"'

        ]

        return command
