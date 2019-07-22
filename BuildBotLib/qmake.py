# This Python file uses the following encoding: utf-8

import BuildBotLib.basemodule as base
from buildbot.plugins import util, steps
from pathlib import Path
import datetime
import os
import subprocess

def isClean(step):
    return step.getProperty('clean');

def isDeploy(step):
    return step.getProperty('deploy');


def isRelease(step):
    return step.getProperty('release');


def isTest(step):
    return step.getProperty('test');

def isWin(step):
    return step.getProperty('Windows');

def isLinux(step):
    return step.getProperty('Linux');

def isAndroid(step):
    return step.getProperty('Android');

@util.renderer
def destDir(props):
    home = str(Path.home())
    repo = str(props.getProperty('repository'));
    now = datetime.datetime.now().strftime("(%H %M) %m-%d-%Y")

    return home + '/shared/' + repo[repo.rfind('/'): len(repo) - 4] + "/" + now

@util.renderer
def permission(props):
    home = str(Path.home())
    return ["chmod", "-R", "775", home + '/shared']

def LinuxSteps() :

    list = [
        steps.ShellCommand(
            command = [
                'qmake-linux',
                "QMAKE_CXX='ccache g++'",
                "-r",
                "CONFIG+=qtquickcompiler",
                'ONLINE="~/repo"'
                ],
            haltOnFailure = True,
            doStepIf = lambda step : isLinux(step),

            name = 'QMake Linux',
            description = 'create a make files for projects',
        ),
        steps.ShellCommand(
            command = ['make', 'clean'],
            doStepIf = lambda step : isClean(step) and  isLinux(step),
            name = 'clean Linux',
            description = 'clean old build data',
        ),
        steps.Compile(
            command = base.makeCommand,
            name = 'Build Linux',
            doStepIf = lambda step : isLinux(step),

            haltOnFailure = True,
            description = 'run make for project',
        ),
        steps.ShellCommand(
            command= ['make', 'deploy'],
            doStepIf = lambda step : isDeploy(step) and  isLinux(step),
            name = 'deploy Linux',
            haltOnFailure = True,
            description = 'deploy project ',
        ),
        steps.Compile(
            command= ['make', 'test'],
            doStepIf = lambda step : isTest(step) and  isLinux(step),
            name = 'tests ',
            haltOnFailure = True,
            description = 'run autotests of project',
        ),
        steps.ShellCommand(
            command= ['make', 'release'],
            doStepIf = lambda step : isRelease(step) and  isLinux(step),
            name = 'release Linux',
            haltOnFailure = True,
            description = 'release project, like push to store or online repository',
        ),
        steps.ShellCommand(
            command = ['make', 'distclean'],
            doStepIf = lambda step : isLinux(step),
            name = 'clean Linux makefiles',
            description = 'clean old makefiles  ',
        ),


    ]

    return list;

def AndroidSteps() :

    list = [
        steps.ShellCommand(
            command = [
                'qmake-android',
                '-spec', 'android-clang',
                "-r",
                "CONFIG+=qtquickcompiler",
                'SIGN_PATH="' + util.Interpolate("%(secret:SIGPATH)s") + '"',
                'SIGN_ALIES="quasarapp"',
                'SIGN_STORE_PASSWORD="' + util.Interpolate("%(secret:SIGPASS)s") + '"',
            ],
            haltOnFailure = True,
            doStepIf = lambda step : isAndroid(step),

            name = 'QMake Android',
            description = 'create a make files for projects',
        ),
        steps.ShellCommand(
            command = ['make', 'clean'],
            doStepIf = lambda step : isClean(step) and  isAndroid(step),
            name = 'clean Android',
            description = 'clean old build data',
        ),
        steps.Compile(
            command = base.makeCommand,
            name = 'Build Android',
            doStepIf = lambda step : isAndroid(step),

            haltOnFailure = True,
            description = 'run make for project',
        ),
        steps.ShellCommand(
            command= ['make', 'deploy'],
            doStepIf = lambda step : isDeploy(step) and  isAndroid(step),
            name = 'deploy Android',
            haltOnFailure = True,
            description = 'deploy project ',
        ),
        steps.ShellCommand(
            command= ['make', 'release'],
            doStepIf = lambda step : isRelease(step) and  isAndroid(step),
            name = 'release Android',
            haltOnFailure = True,
            description = 'release project, like push to store or online repository',
        ),
        steps.ShellCommand(
            command = ['make', 'distclean'],
            doStepIf = lambda step : isAndroid(step),
            name = 'clean Android makefiles',
            description = 'clean old makefiles  ',
        ),


    ]

    return list;

def WinSteps() :
    list = [
        steps.ShellCommand(
            command = [
                'qmake-windows',
                '-spec', 'win32-g++',
                "QMAKE_CXX='ccache x86_64-w64-mingw32-g++'",
                "-r",
                "CONFIG+=qtquickcompiler",
                'ONLINE="~/repo"'
                ],
            name = 'QMake Windows',
            haltOnFailure = True,
            doStepIf = lambda step : isWin(step),
            description = 'create a make files for projects',
        ),
        steps.ShellCommand(
            command = ['make', 'clean'],
            doStepIf = lambda step : isClean(step) and  isWin(step),
            name = 'clean Windows',
            description = 'clean old build data',
        ),
        steps.Compile(
            command = base.makeCommand,
            name = 'Build Windows',
            haltOnFailure = True,
            doStepIf = lambda step : isWin(step),

            description = 'run make for project',
        ),
        steps.ShellCommand(
            command= ['make', 'deploy'],
            doStepIf = lambda step : isDeploy(step) and  isWin(step),
            name = 'deploy Windows',
            haltOnFailure = True,

            description = 'deploy project ',
        ),
        steps.ShellCommand(
            command= ['make', 'release'],
            doStepIf = lambda step : isRelease(step) and  isWin(step),
            name = 'release Windows',
            haltOnFailure = True,

            description = 'release project, like push to store or online repository',
        ),
        steps.ShellCommand(
            command = ['make', 'distclean'],
            doStepIf = lambda step : isWin(step),
            name = 'clean Windows makefiles',
            description = 'clean old makefiles  ',
        ),
    ]
    return list;


def getFactory():
    factory = base.getFactory();

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

    factory.addSteps(LinuxSteps());
    factory.addSteps(WinSteps());
    factory.addSteps(AndroidSteps());

    factory.addStep(
        steps.CopyDirectory(
            src = util.Interpolate('build/%(prop:copyFolder)s'),
            dest = destDir,
            doStepIf = lambda step : isDeploy(step),
            name = 'copy buildet files',
            description = 'copy buildet files to shared folder',
        )
    );

    factory.addStep(
        steps.ShellCommand(
            command= permission,
            name = 'set permission',
            haltOnFailure = True,

            description = 'set permission for shared folder',
        )
    );

    return factory

def getRepo():
    return "";

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