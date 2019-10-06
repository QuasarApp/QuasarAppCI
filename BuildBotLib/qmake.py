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
            command = [
                'qmake-linux',
                "-r",
                "CONFIG+=qtquickcompiler",
                'ONLINE="~/repo"'
            ];

            return command;

        @util.renderer
        def windowsXmakeCmd(self, props):
            command = [
                'qmake-windows',
                '-spec', 'win32-g++',
                "-r",
                "CONFIG+=qtquickcompiler",
                'ONLINE="~/repo"'
            ];

            return command;

        @util.renderer
        def androidXmakeCmd(self, props):
            secret = SecretManager("/home/andrei/buildBotSecret/secret.json")

            command = [
                'qmake-android',
                '-spec', 'android-clang',
                "-r",
                "CONFIG+=qtquickcompiler",
                'SIGN_PATH="' + secret.getValue('SIGPATH') + '"',
                'SIGN_ALIES="quasarapp"',
                'SIGN_STORE_PASSWORD="' + secret.getValue('SIGPASS') + '"'

            ];

            return command;
