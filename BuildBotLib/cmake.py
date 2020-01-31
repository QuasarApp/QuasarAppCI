# This Python file uses the following encoding: utf-8

from BuildBotLib.make import Make
from buildbot.plugins import secrets, util, steps
from pathlib import Path
import datetime
import os
import subprocess
from BuildBotLib.secretManager import *


class CMake(Make):

    def __init__(self, platform):
        Make.__init__(self, platform);

    def linuxXmakeCmd(self, props):
        secret = SecretManager(self.home + "/buildBotSecret/secret.json")

        QT_Dir = subprocess.getoutput(['qmake-android -query QT_HOST_PREFIX'])

        command = [
            'cmake', '-DCMAKE_PREFIX_PATH=' + QT_Dir,
            '-DSPEC_X=linux-g++',

            '-DSIGN_PATH="' + secret.getValue('SIGPATH') + '"',
            '-DSIGN_ALIES="quasarapp"',
            '-DSIGN_STORE_PASSWORD="' + secret.getValue('SIGPASS') + '"'

        ]

        return command

    def windowsXmakeCmd(self, props):
        secret = SecretManager(self.home + "/buildBotSecret/secret.json")

        QT_Dir = subprocess.getoutput(['qmake-android -query QT_HOST_PREFIX'])

        command = [
            'cmake', '-DCMAKE_PREFIX_PATH=' + QT_Dir,
            '-DSPEC_X=win64-g++',

            '-DSIGN_PATH="' + secret.getValue('SIGPATH') + '"',
            '-DSIGN_ALIES="quasarapp"',
            '-DSIGN_STORE_PASSWORD="' + secret.getValue('SIGPASS') + '"'

        ]

        return command

    def androidXmakeCmd(self, props):
        secret = SecretManager(self.home + "/buildBotSecret/secret.json")

        QT_Dir = subprocess.getoutput(['qmake-android -query QT_HOST_PREFIX'])

        command = [
            'cmake', '-DCMAKE_PREFIX_PATH=' + QT_Dir,
            '-DSPEC_X=android-clang',

            '-DSIGN_PATH="' + secret.getValue('SIGPATH') + '"',
            '-DSIGN_ALIES="quasarapp"',
            '-DSIGN_STORE_PASSWORD="' + secret.getValue('SIGPASS') + '"'

        ]

        return command
