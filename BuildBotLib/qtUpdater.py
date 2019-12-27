# This Python file uses the following encoding: utf-8

from BuildBotLib.make import Make
from BuildBotLib.basemodule import BaseModule

from buildbot.plugins import util, steps

import subprocess


class QtUpdater(Make):

    def __init__(self):
        Make.__init__(self)
        self.qtDefaultHelp = []
        self.lastTargetDir = ""

    def linuxXmakeCmd(self, props):
        command = [
            'aqt',
            "install",
            "--outputdir", self.home + "/Qt",
            'linux', 'desktop'
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

        command = [
            'aqt',
            "install",
            "--outputdir", self.home + "/Qt",
            'linux', 'android'
        ]

        return command

    def isConfigureonly(self, step):
        return step.getProperty('configureonly')

    def getArrayQtParams(self, text):
        array = text.split('\n')
        res = []

        excludePlugins = ['freetype', 'xcb', 'webengine']

        for item in array:
            index = item.find('/qt')
            if index <= -1:
                continue

            item = item.replace(" ", "")
            lenngth = item.find('.')

            if (lenngth <= -1):
                continue

            value = "-qt" + item[0: lenngth]

            toContinue = False
            for plugin in excludePlugins:
                toContinue = toContinue or (value.find(plugin) >= 0)

            if toContinue:
                continue

            res.append(value)

        return res

    def getHelp(self, props):

        result = ""
        dirpath = props.getProperty("builddir")
        stdout = subprocess.getoutput([dirpath + '/build/configure -h'])
        result = "QT HELP: + \n" + stdout

        self.qtDefaultHelp = self.getArrayQtParams(stdout)

        if (len(self.qtDefaultHelp) <= 0):
            result = "qt help is Empty. stdout= " + stdout
        else:
            result += " ".join(self.qtDefaultHelp)

        return ["echo", result]

    def lsLinux(self):
        res = "ln -sf " + self.lastTargetDir + "/bin/qmake "
        res += self.home + "/.local/bin/qmake-linux"
        return res

    def lsWindows(self):

        res = "ln -sf " + self.lastTargetDir + "/bin/qmake "
        res += self.home + "/.local/bin/qmake-windows"
        return res

    def lsAndroid(self):

        res = "ln -sf " + self.lastTargetDir + "/bin/qmake "
        res += self.home + "/.local/bin/qmake-android"
        return res

    def cpExtraWindows(self):

        cmd = ""
        path = "/usr/lib/gcc/x86_64-w64-mingw32/7.3-win32/*.dll"
        path2 = "/usr/x86_64-w64-mingw32/lib/*.dll"

        cmd += "cp " + path + " " + self.lastTargetDir + "/bin/"
        cmd += "; cp " + path2 + " " + self.lastTargetDir + "/bin/"

        return cmd

    def getGeneralConfigureOptions(self, props):
        list = [
            "-opensource",
            "-confirm-license",
            "-release",
            "-nomake", "examples",
            "-nomake", "tests",
            "-skip", "qtdocgallery",
            "-skip", "qtpim",
            "-skip", "qtwebengine",
            "-ccache"
        ]

        list += self.qtDefaultHelp
        return list

    def getTargetDir(self, configureOptions, branch, platform):

        if (not len(branch)):
            branch = "Custom"

        if (not len(platform)):
            branch = "Unknown"

        self.lastTargetDir = self.home + "/Qt/" + branch + "/" + platform
        return ["-prefix", self.lastTargetDir]

    def getWindowsConfigOptions(self, props):
        list = [
            "-skip", "qtactiveqt",
            "-skip", "qtwebglplugin",
            "-skip", "qtlocation",
            "-skip", "qtvirtualkeyboard",
            "-skip", "qtwinextras",
            "-skip", "qtactiveqt",
            "-opengl", "desktop",
            "-xplatform", "win32-g++",
            "-device-option", "CROSS_COMPILE=x86_64-w64-mingw32-",
            "-no-pch"
        ]

        list += self.getGeneralConfigureOptions(props)
        list += self.getTargetDir(list, props.getProperty('branch'), "Windows")

        return ["./configure"] + list

    def installStep(self, platform):

        platformLsCmd = {
            'linux': self.lsLinux(),
            'windows': self.lsWindows(),
            'android': self.lsAndroid(),
        }

        cpCmd = {
            'windows': self.cpExtraWindows(),
        }

        stringCmd = platformLsCmd[platform] + "; " + cpCmd.get(platform, "")

        return self.generateCmd(stringCmd)

    def generateInstallStep(self, platform):

        def dustepIf(step):
            return not self.isConfigureonly(step)

        res = [self.generateStep(self.installStep(platform),
                                 platform,
                                 "install qt into worker",
                                 dustepIf)]

        res += [self.generateStep(['git', 'clean', '-xdf'],
                                  platform,
                                  "clean old build data",
                                  lambda step: True)]

        return res

    def getFactory(self):
        factory = util.BuildFactory()

        factory.addStep(
            steps.Git(
                repourl="https://github.com/qt/qt5.git",
                branch=util.Interpolate('%(prop:branch)s'),
                mode='full',
                method='fresh',
                submodules=True,
                name='git operations',
                description='operations of git like pull clone fetch',
            )
        )

        factory.addStep(
            steps.ShellCommand(
                command=self.getHelp,
                name='read help',
                haltOnFailure=True,
                description='read help for generate the configure command',
            )
        )

        factory.addSteps(self.generatePlatformSteps('linux'))
        factory.addSteps(self.generateInstallStep('linux'))

        factory.addSteps(self.generatePlatformSteps('windows'))
        factory.addSteps(self.generateInstallStep('windows'))

        factory.addSteps(self.generatePlatformSteps('android'))
        factory.addSteps(self.generateInstallStep('android'))

        return factory

    def getPropertyes(self):

        base = BaseModule.getPropertyes(self)

        return base + [
            util.BooleanParameter(
                name='configureonly',
                label='disable build and install qt (confugure only)',
                default=False
            )
        ]
