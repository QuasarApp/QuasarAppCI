# This Python file uses the following encoding: utf-8

from BuildBotLib.make import Make
from BuildBotLib.secretManager import SecretManager
from buildbot.plugins import util

import os


class CMake(Make):

    def __init__(self, platform):
        Make.__init__(self, platform)

    def makePrefix(self):
        return "C"

    @util.renderer
    def isSupport(self, step):
        return os.path.isfile('./CMakeLists.txt')

    def mainCmd(self):
        command = [
            'cmake',
            "."
        ]

        return command

    def linuxXmakeCmd(self, props):
        return self.mainCmd()

    def windowsXmakeCmd(self, props):
        return self.mainCmd()

    def androidXmakeCmd(self, props):
        secret = SecretManager(self.home + "/buildBotSecret/secret.json")

        command = [
            'cmake',
            '-DANDROID_ABI=arm64-v8a',
            '-DANDROID_BUILD_ABI_arm64-v8a=ON',
            '-DANDROID_BUILD_ABI_armeabi-v7a=ON',
            '-DSIGN_PATH="' + secret.getValue('SIGPATH') + '"',
            '-DSIGN_ALIES="quasarapp"',
            '-DSIGN_STORE_PASSWORD="' + secret.getValue('SIGPASS') + '"'

        ]

        return command
