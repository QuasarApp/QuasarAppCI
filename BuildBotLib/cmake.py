# This Python file uses the following encoding: utf-8

import BuildBotLib.make as Make
from buildbot.plugins import secrets, util, steps
from pathlib import Path
import datetime
import os
import subprocess
from BuildBotLib.secretManager import *


class QMake(Make):

    def __init__(self):
        Make.__init__(self);

        @util.renderer
        def linuxXmakeCmd(self, props):
            secret = SecretManager("/home/andrei/buildBotSecret/secret.json")

            QT_Dir = subprocess.getoutput(['qmake-android -query QT_HOST_PREFIX'])

            command = [
                'cmake', '-DCMAKE_PREFIX_PATH=' + QT_Dir,
                '-DSPEC_X=linux-g++',

                '-DSIGN_PATH="' + secret.getValue('SIGPATH') + '"',
                '-DSIGN_ALIES="quasarapp"',
                '-DSIGN_STORE_PASSWORD="' + secret.getValue('SIGPASS') + '"'

            ]

            return command

        @util.renderer
        def windowsXmakeCmd(self, props):
            secret = SecretManager("/home/andrei/buildBotSecret/secret.json")

            QT_Dir = subprocess.getoutput(['qmake-android -query QT_HOST_PREFIX'])

            command = [
                'cmake', '-DCMAKE_PREFIX_PATH=' + QT_Dir,
                '-DSPEC_X=win64-g++',

                '-DSIGN_PATH="' + secret.getValue('SIGPATH') + '"',
                '-DSIGN_ALIES="quasarapp"',
                '-DSIGN_STORE_PASSWORD="' + secret.getValue('SIGPASS') + '"'

            ]

            return command

        @util.renderer
        def androidXmakeCmd(self, props):
            secret = SecretManager("/home/andrei/buildBotSecret/secret.json")

            QT_Dir = subprocess.getoutput(['qmake-android -query QT_HOST_PREFIX'])

            command = [
                'cmake', '-DCMAKE_PREFIX_PATH=' + QT_Dir,
                '-DSPEC_X=android-clang',

                '-DSIGN_PATH="' + secret.getValue('SIGPATH') + '"',
                '-DSIGN_ALIES="quasarapp"',
                '-DSIGN_STORE_PASSWORD="' + secret.getValue('SIGPASS') + '"'

            ]

            return command
