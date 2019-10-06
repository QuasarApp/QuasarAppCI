# This Python file uses the following encoding: utf-8

import BuildBotLib.basemodule as BaseModule
from buildbot.plugins import util, steps
from pathlib import Path
import subprocess
import hashlib
import os
import datetime


class QtUpdater(BaseModule):

    def __init__(self):
        BaseModule.__init__(self);
        self.qtDefaultHelp = [];
        self.lastTargetDir = "";

    def isWin(self, step):
        return step.getProperty('Windows');

    def isLinux(self, step):
        return step.getProperty('Linux');

    def isAndroid(self, step):
        return step.getProperty('Android');

    def isConfigureonly(self, step):
        return step.getProperty('configureonly');

    def getArrayQtParams(self, text):
        array = text.split('\n')
        res = []

        excludePlugins = ['freetype', 'xcb', 'webengine'];

        for item in array:
            index = item.find('/qt')
            if index <= -1 :
                continue

            item = item.replace(" ", "")
            lenngth = item.find('.')

            if (lenngth <= -1):
                continue


            value = "-qt" + item[0: lenngth]

            toContinue = False;
            for plugin in excludePlugins :
                toContinue = toContinue or (value.find(plugin) >= 0);

            if toContinue :
                continue;

            res.append(value)


        return res


    @util.renderer
    def getHelp(self, props):

        result = "";
        dirpath = props.getProperty("builddir");
        stdout  = subprocess.getoutput([dirpath + '/build/configure -h'])
        result = "QT HELP: + \n" + stdout;

        self.qtDefaultHelp = getArrayQtParams(stdout);

        if (len(self.qtDefaultHelp) <= 0):
            result = "qt help is Empty. stdout= " + stdout;
        else:
            result += " ".join(self.qtDefaultHelp);

        return ["echo", result];

    @util.renderer
    def lsLinux(self, props):
        return ["ln", "-sf", self.lastTargetDir + "/bin/qmake", "/home/andrei/.local/bin/qmake-linux"];

    @util.renderer
    def lsWindows(self, props):
        return ["ln", "-sf", self.lastTargetDir + "/bin/qmake", "/home/andrei/.local/bin/qmake-windows"];

    @util.renderer
    def lsAndroid(self, props):
        return ["ln", "-sf", self.lastTargetDir + "/bin/qmake", "/home/andrei/.local/bin/qmake-android"];

    @util.renderer
    def cpGCCWindows(self, props):
        if not isWin(props) or isConfigureonly(props):
            return ['echo', " "]

        resFiles = base.copyRegExp("/usr/lib/gcc/x86_64-w64-mingw32/7.3-win32/*.dll", self.lastTargetDir + "/bin/")
        return ['echo', " ".join(resFiles)];

    @util.renderer
    def cpThreadWindows(self, props):
        if not isWin(props) or isConfigureonly(props):
            return ['echo', " "]

        resFiles = base.copyRegExp("/usr/x86_64-w64-mingw32/lib/*.dll", self.lastTargetDir + "/bin/")
        return ['echo', " ".join(resFiles)];

    @util.renderer
    def cpIcuLinux(self, props):
        if not isLinux(props) or isConfigureonly(props):
            return ['echo', " "]

        resFiles = base.copyRegExp("/usr/lib/x86_64-linux-gnu/libicu*", lastTargetDir[0] + "/lib/")
        return ['echo', " ".join(resFiles)];

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
        ];

        list += self.qtDefaultHelp;
        return list;

    def getTargetDir(self, configureOptions, branch, platform):

        if (not len(branch)) :
            branch = "Custom";

        if (not len(platform)) :
            branch = "Unknown";

        self.lastTargetDir = "/home/andrei/Qt/Qt-" + branch + "/" + platform;
        return ["-prefix", self.lastTargetDir];

    @util.renderer
    def getLinuxConfigOptions(self, props):
        list = ['-fontconfig', '-qt-xcb', '-dbus-linked' ];
        list += getGeneralConfigureOptions(props);
        list += getTargetDir(list, props.getProperty('branch'), "Linux");

        return ["./configure"] + list;


    @util.renderer
    def getWindowsConfigOptions(self, props):
        list = [
        "-skip", "qtactiveqt",
        "-skip", "qtwebglplugin",
        "-skip", "qtlocation",
        "-skip", "qtvirtualkeyboard",
        "-skip", "qtwinextras",
        "-skip", "qtactiveqt",
        "-opengl", "desktop",
        "-xplatform","win32-g++",
        "-device-option", "CROSS_COMPILE=x86_64-w64-mingw32-",
        "-no-pch"
        ];

        list += getGeneralConfigureOptions(props);
        list += getTargetDir(list, props.getProperty('branch'), "Windows");

        return ["./configure"] + list;

    @util.renderer
    def getAndroidConfigOptions(self, props):

        list = [
        "-xplatform", "android-clang",
        "--disable-rpath",
        "-android-ndk", "/home/andrei/Android/NDK/android-ndk-r19c",
        "-android-sdk", "/home/andrei/Android/SDK",
        "-skip", "qttranslations",
        "-skip", "qtserialport",
        "-no-warnings-are-errors",
        "-android-arch","arm64-v8a"
        ];

        list += getGeneralConfigureOptions(props);
        list += getTargetDir(list, props.getProperty('branch'), "Android");

        return ["./configure"] + list;


    def windowsSteps(self):

        list = [
            steps.ShellCommand(
                command = ['git', 'clean', '-xdf'],
                doStepIf = lambda step : isWin(step),

                name = 'clean for Windows',
                description = 'clean old build data',
            ),
            steps.ShellCommand(
                command = ['git', 'submodule', 'foreach', '--recursive', 'git', 'clean', '-xdf'],
                doStepIf = lambda step :isWin(step),

                name = 'clean submodule for Windows',
                description = 'clean submodule old build data',
            ),
            steps.ShellCommand(
                command = getWindowsConfigOptions,
                haltOnFailure = True,
                doStepIf = lambda step : isWin(step),

                name = 'configure Windows',
                description = 'create a make files for projects',
            ),
            steps.Compile(
                command = base.makeCommand,
                name = 'Build Qt for Windows',
                haltOnFailure = True,
                doStepIf = lambda step : isWin(step) and not isConfigureonly(step),

                description = 'run make for project',
            ),

            steps.Compile(
                command = ['make', 'install', '-j2'],
                name = 'Install Qt for Windows',
                haltOnFailure = True,
                timeout = 360000,
                doStepIf = lambda step : isWin(step) and not isConfigureonly(step),

                description = 'run make for project',
            ),

            steps.ShellCommand(
                command = cpGCCWindows,
                haltOnFailure = True,
                doStepIf = lambda step : isWin(step) and not isConfigureonly(step),
                name = 'Copy gcc libs for Windows',
                description = 'Copy extra libs',
            ),

            steps.ShellCommand(
                command = cpThreadWindows,
                haltOnFailure = True,
                doStepIf = lambda step : isWin(step) and not isConfigureonly(step),
                name = 'Copy thread libs for Windows',
                description = 'Copy extra libs',
            ),
            steps.ShellCommand(
                command = lsWindows,
                haltOnFailure = True,
                doStepIf = lambda step : isWin(step) and not isConfigureonly(step),
                name = 'Create ls links for Windows',
                description = 'deploy qt',
            ),

        ]

        return list;


    def linuxSteps(self):

        list = [
            steps.ShellCommand(
                command = ['git', 'clean', '-xdf'],
                doStepIf = lambda step : isLinux(step),
                name = 'clean for Linux',
                description = 'clean old build data',
            ),
            steps.ShellCommand(
                command = ['git', 'submodule', 'foreach', '--recursive', 'git', 'clean', '-xdf'],
                doStepIf = lambda step :isLinux(step),
                name = 'clean submodule for Linux',
                description = 'clean submodule old build data',
            ),
            steps.ShellCommand(
                command = getLinuxConfigOptions,
                haltOnFailure = True,
                doStepIf = lambda step : isLinux(step),
                name = 'configure Linux',
                description = 'create a make files for projects',
            ),
            steps.Compile(
                command = base.makeCommand,
                name = 'Build Qt for Linux',
                haltOnFailure = True,
                timeout = 360000,
                doStepIf = lambda step : isLinux(step) and not isConfigureonly(step),

                description = 'run make for project',
            ),

            steps.Compile(
                command = ['make', 'install', '-j2'],
                name = 'Install Qt for Linux',
                haltOnFailure = True,
                doStepIf = lambda step : isLinux(step) and not isConfigureonly(step),

                description = 'run make for project',
            ),

            steps.ShellCommand(
                command = cpIcuLinux,
                haltOnFailure = True,
                doStepIf = lambda step : isLinux(step) and not isConfigureonly(step),
                name = 'Copy ICU libs for Linux',
                description = 'Copy extra libs',
            ),

            steps.ShellCommand(
                command = lsLinux,
                haltOnFailure = True,
                doStepIf = lambda step : isLinux(step) and not isConfigureonly(step),
                name = 'Create ls links for Linux',
                description = 'deploy qt',
            ),

        ]

        return list;


    def androidSteps(self):

        list = [
            steps.ShellCommand(
                command = ['git', 'clean', '-xdf'],
                doStepIf = lambda step : isAndroid(step),
                name = 'clean for Android',
                description = 'clean old build data',
            ),
            steps.ShellCommand(
                command = ['git', 'submodule', 'foreach', '--recursive', 'git', 'clean', '-xdf'],
                doStepIf = lambda step :isAndroid(step),
                name = 'clean submodule for Android',
                description = 'clean submodule old build data',
            ),
            steps.ShellCommand(
                command = getAndroidConfigOptions,
                haltOnFailure = True,
                doStepIf = lambda step : isAndroid(step),
                name = 'configure Android',
                description = 'create a make files for projects',
            ),
            steps.Compile(
                command = base.makeCommand,
                name = 'Build Qt for Android',
                haltOnFailure = True,
                timeout = 360000,
                doStepIf = lambda step : isAndroid(step) and not isConfigureonly(step),

                description = 'run make for project',
            ),

            steps.Compile(
                command = ['make', 'install', '-j2'],
                name = 'Install Qt for Android',
                haltOnFailure = True,
                doStepIf = lambda step : isAndroid(step) and not isConfigureonly(step),

                description = 'run make for project',
            ),
            steps.ShellCommand(
                command = lsAndroid,
                haltOnFailure = True,
                doStepIf = lambda step : isAndroid(step) and not isConfigureonly(step),
                name = 'Create ls links for Android',
                description = 'deploy qt',
            ),

        ]

        return list;

    def getFactory(self):
        factory = base.getFactory();

        factory.addStep(
            steps.Git(
                repourl="https://github.com/qt/qt5.git",
                branch=util.Interpolate('%(prop:branch)s'),
                mode='full',
                method = 'fresh',
                submodules=True,
                name = 'git operations',
                description = 'operations of git like pull clone fetch',
            )
        );

        factory.addStep(
            steps.ShellCommand(
                command= getHelp,
                name = 'read help',
                haltOnFailure = True,
                description = 'read help for generate the configure command',
            )
        );

        factory.addSteps(linuxSteps());
        factory.addSteps(windowsSteps());
        factory.addSteps(androidSteps());

        return factory

    def getPropertyes(self):
        return [
            util.BooleanParameter(
                name = 'Windows',
                label = 'Windows version Qt',
                default = True
            ),

            util.BooleanParameter(
                name = 'Linux',
                label = 'Linux version Qt',
                default = True
            ),

            util.BooleanParameter(
                name = 'Android',
                label = 'Android version Qt',
                default = True
            ),

            util.BooleanParameter(
                name = 'configureonly',
                label = 'disable build and install qt (confugure only)',
                default = False
            )


        ]
