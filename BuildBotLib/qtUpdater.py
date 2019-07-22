# This Python file uses the following encoding: utf-8

import BuildBotLib.basemodule as base
from buildbot.plugins import util, steps
from pathlib import Path
import subprocess
import hashlib
import os
import datetime


# Windows build command
#./configure -opensource -confirm-license -release -nomake examples -nomake tests -skip qtactiveqt -skip qtwebglplugin -skip qtlocation -skip qtvirtualkeyboard -skip qtwinextras -opengl desktop -prefix ~/Qt/5.12.3/win64 -xplatform win32-g++ -device-option CROSS_COMPILE=x86_64-w64-mingw32-

# Linux
# libclang-dev sudo apt install libclang-6.0-dev llvm-6.0 libxcomposite-dev и libwayland-dev
# '^libxcb.*-dev' libx11-xcb-dev libglu1-mesa-dev libxrender-dev libxi-dev gperf bison flex
# ./configure -skip qtpim -opensource -confirm-license -release -qt-doubleconversion -qt-pcre -qt-zlib -qt-freetype -qt-harfbuzz -qt-libpng -qt-libjpeg -qt-assimp -qt-tiff -qt-webp -qt-webengine-icu -qt-webengine-ffmpeg -qt-webengine-opus -qt-webengine-webp -nomake examples -nomake tests -prefix ~/Qt/5.14.3/win64


#android
# ./configure -opensource -confirm-license -release -xplatform android-clang --disable-rpath -nomake tests -nomake examples -android-ndk /home/andrei/Android/NDK/android-ndk-r19c -android-sdk /home/andrei/Android/SDK -skip qttranslations -skip qtserialport -no-warnings-are-errors -android-arch arm64-v8a -qt-doubleconversion -qt-pcre -qt-zlib -qt-freetype -qt-harfbuzz -qt-libpng -qt-libjpeg -qt-assimp -qt-tiff -qt-webp -qt-webengine-icu -qt-webengine-ffmpeg -qt-webengine-opus -qt-webengine-webp
# 10:47:23: The process "/home/andrei/Downloads/android-ndk-r19c-linux-x86_64/android-ndk-r19c/prebuilt/linux-x86_64/bin/make" exited normally.
# 10:47:23: Starting: "/media/D/Qt/5.12.4/android_arm64_v8a/bin/androiddeployqt" --input /media/D/own/build-SnakeMain-Android_for_arm64_v8a_Clang_Qt_5_12_4_for_Android_ARM64_v8a-Debug/Snake/android-libsnake.so-deployment-settings.json --output /media/D/own/build-SnakeMain-Android_for_arm64_v8a_Clang_Qt_5_12_4_for_Android_ARM64_v8a-Debug/android-build --android-platform android-29 --jdk /usr --gradle
# 15:41:18: The process "/home/andrei/Downloads/android-ndk-r19c-linux-x86_64/android-ndk-r19c/prebuilt/linux-x86_64/bin/make" exited normally.
# 15:41:18: Starting: "/media/D/Qt/5.12.4/android_arm64_v8a/bin/androiddeployqt"
# --input /media/D/own/build-SnakeMain-Android_for_arm64_v8a_Clang_Qt_5_12_4_for_Android_ARM64_v8a-Release/Snake/android-libsnake.so-deployment-settings.json
# --output /media/D/own/build-SnakeMain-Android_for_arm64_v8a_Clang_Qt_5_12_4_for_Android_ARM64_v8a-Release/android-build
# --android-platform android-29
# --jdk /usr
# --gradle
# --sign '******' --storepass '******' --keypass '******'

qtDefaultHelp = [[]]
LAST_TARGET_DIR = [""]

def isWin(step):
    return step.getProperty('Windows');

def isLinux(step):
    return step.getProperty('Linux');

def isAndroid(step):
    return step.getProperty('Android');


def getArrayQtParams(text):
    array = text.split('\n')
    res = []

    excludePlugins = ['freetype'];

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
def getHelp(props):

    result = "";
    dirpath = props.getProperty("builddir");
    stdout  = subprocess.getoutput([dirpath + '/build/configure -h'])
    result = "QT HELP: + \n" + stdout;

    qtDefaultHelp[0] = getArrayQtParams(stdout);

    if (len(qtDefaultHelp[0]) <= 0):
        result = "qt help is Empty. stdout= " + stdout;
    else:
        result += " ".join(qtDefaultHelp[0]);

    return ["echo", result];

@util.renderer
def lsLinux(props):
    return ["ln", "-sf", LAST_TARGET_DIR[0] + "/bin/qmake", "/home/andrei/.local/bin/qmake-linux"];

@util.renderer
def lsWindows(props):
    return ["ln", "-sf", LAST_TARGET_DIR[0] + "/bin/qmake", "/home/andrei/.local/bin/qmake-windows"];

@util.renderer
def lsAndroid(props):
    return ["ln", "-sf", LAST_TARGET_DIR[0] + "/bin/qmake", "/home/andrei/.local/bin/qmake-android"];

@util.renderer
def cpGCCWindows(props):
    if not isWin(props):
        return ['echo', " "]

    resFiles = base.copyRegExp("/usr/lib/gcc/x86_64-w64-mingw32/7.3-win32/*.dll", LAST_TARGET_DIR[0] + "/bin/")
    return ['echo', " ".join(resFiles)];

@util.renderer
def cpThreadWindows(props):
    if not isWin(props):
        return ['echo', " "]

    resFiles = base.copyRegExp("/usr/x86_64-w64-mingw32/lib/*.dll", LAST_TARGET_DIR[0] + "/bin/")
    return ['echo', " ".join(resFiles)];

@util.renderer
def cpIcuLinux(props):
    if not isLinux(props):
        return ['echo', " "]

    resFiles = base.copyRegExp("/usr/lib/x86_64-linux-gnu/libicu*", LAST_TARGET_DIR[0] + "/lib/")
    return ['echo', " ".join(resFiles)];

def getGeneralConfigureOptions(props):
    list = [
    "-opensource",
    "-confirm-license",
    "-release",
    "-nomake", "examples",
    "-nomake", "tests",
    "-skip", "qtdocgallery",
    "-skip", "qtpim",
    "-ccache"
    ];

    list += qtDefaultHelp[0];
    return list;

def getTargetDir(configureOptions, branch, platform):

    if (not len(branch)) :
        branch = "Custom";

    if (not len(platform)) :
        branch = "Unknown";

    LAST_TARGET_DIR[0] = "/home/andrei/Qt/Qt-" + branch + "/" + platform;
    return ["-prefix", LAST_TARGET_DIR[0]];

@util.renderer
def getLinuxConfigOptions(props):
    list = ['-fontconfig'];
    list += getGeneralConfigureOptions(props);
    list += getTargetDir(list, props.getProperty('branch'), "Linux");

    return ["./configure"] + list;


@util.renderer
def getWindowsConfigOptions(props):
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

    ];

    list += getGeneralConfigureOptions(props);
    list += getTargetDir(list, props.getProperty('branch'), "Windows");

    return ["./configure"] + list;

@util.renderer
def getAndroidConfigOptions(props):

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


def windowsSteps():

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
            doStepIf = lambda step : isWin(step),

            description = 'run make for project',
        ),

        steps.Compile(
            command = ['make', 'install', '-j2'],
            name = 'Install Qt for Windows',
            haltOnFailure = True,
            doStepIf = lambda step : isWin(step),

            description = 'run make for project',
        ),

        steps.ShellCommand(
            command = cpGCCWindows,
            haltOnFailure = True,
            doStepIf = lambda step : isWin(step),
            name = 'Copy gcc libs for Windows',
            description = 'Copy extra libs',
        ),

        steps.ShellCommand(
            command = cpThreadWindows,
            haltOnFailure = True,
            doStepIf = lambda step : isWin(step),
            name = 'Copy thread libs for Windows',
            description = 'Copy extra libs',
        ),
        steps.ShellCommand(
            command = lsWindows,
            haltOnFailure = True,
            doStepIf = lambda step : isWin(step),
            name = 'Create ls links for Windows',
            description = 'deploy qt',
        ),

    ]

    return list;


def linuxSteps():

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
            doStepIf = lambda step : isLinux(step),

            description = 'run make for project',
        ),

        steps.Compile(
            command = ['make', 'install', '-j2'],
            name = 'Install Qt for Linux',
            haltOnFailure = True,
            doStepIf = lambda step : isLinux(step),

            description = 'run make for project',
        ),

        steps.ShellCommand(
            command = cpIcuLinux,
            haltOnFailure = True,
            doStepIf = lambda step : isLinux(step),
            name = 'Copy ICU libs for Linux',
            description = 'Copy extra libs',
        ),

        steps.ShellCommand(
            command = lsLinux,
            haltOnFailure = True,
            doStepIf = lambda step : isLinux(step),
            name = 'Create ls links for Linux',
            description = 'deploy qt',
        ),

    ]

    return list;


def androidSteps():

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
            doStepIf = lambda step : isAndroid(step),

            description = 'run make for project',
        ),

        steps.Compile(
            command = ['make', 'install', '-j2'],
            name = 'Install Qt for Android',
            haltOnFailure = True,
            doStepIf = lambda step : isAndroid(step),

            description = 'run make for project',
        ),
        steps.ShellCommand(
            command = lsAndroid,
            haltOnFailure = True,
            doStepIf = lambda step : isAndroid(step),
            name = 'Create ls links for Android',
            description = 'deploy qt',
        ),

    ]

    return list;

def getFactory():
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

def getRepo():
    return "";

def getPropertyes():
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
        )
    ]