# This Python file uses the following encoding: utf-8

import BuildBotLib.basemodule as BaseModule

from buildbot.plugins import secrets, util, steps
from pathlib import Path
import datetime
import os
import subprocess
from BuildBotLib.secretManager import *


class Make(BaseModule):
    def __init__(self):
        BaseModule.__init__(self);


    def isClean(self, step):
        return step.getProperty('clean');

    def isDeploy(self, step):
        return step.getProperty('deploy');

    def isRelease(self, step):
        return step.getProperty('release');

    def isTest(self, step):
        return step.getProperty('test');

    def isWin(self, step):
        return step.getProperty('Windows');

    def isLinux(self, step):
        return step.getProperty('Linux');

    def isAndroid(self, step):
        return step.getProperty('Android');

    def destDirPrivate(self, props):
        repo = str(props.getProperty('repository'));
        now = datetime.datetime.now().strftime("(%H_%M)_%m-%d-%Y")

        return repo[repo.rfind('/'): len(repo) - 4] + "/" + now;

    @util.renderer
    def destDir(self, props):
        home = str(Path.home())

        return home + '/shared/' + destDirPrivate(props);

    @util.renderer
    def destDirUrl(self, props):
        path = destDirPrivate(props);
        return "http://quasarapp.ddns.net:3031" + path;

    @util.renderer
    def permission(self, props):
        home = str(Path.home())
        return ["chmod", "-R", "775", home + '/shared']

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

    def LinuxSteps(self) :
        list = [
            steps.ShellCommand(
                command = self.linuxXmakeCmd ,
                haltOnFailure = True,
                doStepIf = lambda step : isLinux(step),
                name = 'QMake Linux',
                description = 'create a make files for projects',
            ),
            steps.ShellCommand(
                command = ['make', 'clean'],
                doStepIf = lambda step : self.isClean(step) and self.isLinux(step),
                name = 'clean Linux',
                description = 'clean old build data',
            ),
            steps.Compile(
                command = self.makeCommand,
                name = 'Build Linux',
                doStepIf = lambda step : self.isLinux(step),

                haltOnFailure = True,
                description = 'run make for project',
            ),
            steps.ShellCommand(
                command= ['make', 'deploy'],
                doStepIf = lambda step : self.isDeploy(step) and  self.isLinux(step),
                name = 'deploy Linux',
                haltOnFailure = True,
                description = 'deploy project ',
            ),
            steps.Compile(
                command= ['make', 'test'],
                doStepIf = lambda step : self.isTest(step) and  self.isLinux(step),
                name = 'tests ',
                haltOnFailure = True,
                description = 'run autotests of project',
            ),
            steps.ShellCommand(
                command= ['make', 'release'],
                doStepIf = lambda step : self.isRelease(step) and  self.isLinux(step),
                name = 'release Linux',
                haltOnFailure = True,
                description = 'release project, like push to store or online repository',
            ),
            steps.ShellCommand(
                command = ['make', 'distclean'],
                doStepIf = lambda step : self.isLinux(step),
                name = 'clean Linux makefiles',
                description = 'clean old makefiles  ',
            ),


        ]

        return list;

    def AndroidSteps(self) :
        list = [
            steps.ShellCommand(
                command = androidQmake,
                haltOnFailure = True,
                doStepIf = lambda step : self.isAndroid(step),

                name = 'QMake Android',
                description = 'create a make files for projects',
            ),
            steps.ShellCommand(
                command = ['make', 'clean'],
                doStepIf = lambda step : self.isClean(step) and  self.isAndroid(step),
                name = 'clean Android',
                description = 'clean old build data',
            ),
            steps.Compile(
                command = self.makeCommand,
                name = 'Build Android',
                doStepIf = lambda step : self.isAndroid(step),

                haltOnFailure = True,
                description = 'run make for project',
            ),
            steps.ShellCommand(
                command= ['make', 'deploy'],
                doStepIf = lambda step : self.isDeploy(step) and  self.isAndroid(step),
                name = 'deploy Android',
                haltOnFailure = True,
                description = 'deploy project ',
            ),
            steps.ShellCommand(
                command= ['make', 'release'],
                doStepIf = lambda step : self.isRelease(step) and  self.isAndroid(step),
                name = 'release Android',
                haltOnFailure = True,
                description = 'release project, like push to store or online repository',
            ),
            steps.ShellCommand(
                command = ['make', 'distclean'],
                doStepIf = lambda step : self.isAndroid(step),
                name = 'clean Android makefiles',
                description = 'clean old makefiles  ',
            ),


        ]

        return list;

    def WinSteps(self) :
        list = [
            steps.ShellCommand(
                command = self.windowsXmakeCmd,
                name = 'QMake Windows',
                haltOnFailure = True,
                doStepIf = lambda step : isWin(step),
                description = 'create a make files for projects',
            ),
            steps.ShellCommand(
                command = ['make', 'clean'],
                doStepIf = lambda step : self.isClean(step) and  self.isWin(step),
                name = 'clean Windows',
                description = 'clean old build data',
            ),
            steps.Compile(
                command = self.makeCommand,
                name = 'Build Windows',
                haltOnFailure = True,
                doStepIf = lambda step : self.isWin(step),

                description = 'run make for project',
            ),
            steps.ShellCommand(
                command= ['make', 'deploy'],
                doStepIf = lambda step : self.isDeploy(step) and  self.isWin(step),
                name = 'deploy Windows',
                haltOnFailure = True,

                description = 'deploy project ',
            ),
            steps.ShellCommand(
                command= ['make', 'release'],
                doStepIf = lambda step : self.isRelease(step) and  self.isWin(step),
                name = 'release Windows',
                haltOnFailure = True,

                description = 'release project, like push to store or online repository',
            ),
            steps.ShellCommand(
                command = ['make', 'distclean'],
                doStepIf = lambda step : self.isWin(step),
                name = 'clean Windows makefiles',
                description = 'clean old makefiles  ',
            ),
        ]
        return list;


    def getFactory(self):
        factory = self.getFactory();

        factory.addStep(
            steps.Git(
                repourl=util.Interpolate('%(prop:repository)s'),
                branch=util.Interpolate('%(prop:branch)s'),
                mode='full',
                method = 'fresh',
                submodules=True,
                name = 'git operations',
                description = 'operations of git like pull clone fetch',
            )
        );

        factory.addSteps(self.LinuxSteps());
        factory.addSteps(self.WinSteps());
        factory.addSteps(self.AndroidSteps());

        factory.addStep(
            steps.DirectoryUpload(
                workersrc = util.Interpolate('%(prop:copyFolder)s'),
                masterdest = destDir,
                url = destDirUrl,
                doStepIf = lambda step : self.isDeploy(step),
                name = 'copy buildet files',
                description = 'copy buildet files to shared folder',
            )
        );

        factory.addStep(
            steps.ShellCommand(
                command= self.permission,
                name = 'set permission',
                haltOnFailure = True,

                description = 'set permission for shared folder',
            )
        );

        return factory


    def getPropertyes():
        return [
            util.BooleanParameter(
                name = 'Windows',
                label = 'Windows version project',
                default = True
            ),

            util.BooleanParameter(
                name = 'Linux',
                label = 'Linux version project',
                default = True
            ),

            util.BooleanParameter(
                name = 'Android',
                label = 'Android version project',
                default = True
            ),

            util.BooleanParameter(
                name = 'clean',
                label = 'clean old build ',
                default = True
            ),
            util.BooleanParameter(
                name = 'deploy',
                label = 'deploy project',
                default = True
            ),
            util.BooleanParameter(
                name = 'test',
                label = 'test project ',
                default = True
            ),
            util.BooleanParameter(
                name = 'release',
                label = 'release project',
                default = False
            ),
            util.StringParameter(
                name = 'copyFolder',
                label = 'Folder with buildet data',
                default = "Distro"
            ),

        ]
