# This Python file uses the following encoding: utf-8

from BuildBotLib.make import Make
from BuildBotLib.secretManager import SecretManager


class QMake(Make):

    def __init__(self):
        Make.__init__(self)

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
        return {'ANDROID_NDK_ROOT': self.home + 'andrei/Android/ndk-bundle',
                'JAVA_HOME': '/usr',
                'ANDROID_HOME': self.home + '/Android'}
