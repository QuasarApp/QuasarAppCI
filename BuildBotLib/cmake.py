# This Python file uses the following encoding: utf-8

from BuildBotLib.make import Make
from BuildBotLib.secretManager import SecretManager
import multiprocessing
import os

class CMake(Make):

    def __init__(self, platform):
        Make.__init__(self, platform)
#        self.buildSystems = self.B_CMake

    def makePrefix(self):
        return "C"

    def make(self):
        return 'cmake --build cmake_build --target all'

    def makeTarget(self, target):
        return 'cmake --build cmake_build --target ' + target

    def makeCommand(self, props):
        command = self.make()

        cpus = multiprocessing.cpu_count()

        if cpus:
            command += ' --parallel ' + str(cpus)

        return command

    def linuxXmakeCmd(self, props):
        defines = self.getDefinesList(props)

        defines += [
            '-DCMAKE_PREFIX_PATH=$QTDIR',
            '-B cmake_build'
        ]

        options = [
            'cmake',
        ]
        options += defines

        return ' '.join(options)

    def windowsXmakeCmd(self, props):
        defines = self.getDefinesList(props)

        defines += [
            '-DCMAKE_PREFIX_PATH=%QTDIR%',
            '-DBUILD_SHARED_LIBS=1',
            '-DCMAKE_CXX_COMPILER=g++ -DCMAKE_C_COMPILER=gcc',
            '-DQT_QMAKE_EXECUTABLE=%QTDIR%/bin/qmake.exe',
            '"-GCodeBlocks - MinGW Makefiles"',
            '-B cmake_build'
        ]

        options = [
            'cmake',
        ]
        options += defines

        return ' '.join(options)

    def androidXmakeMultiAbiCmd(self, props):
        file = self.home + "/buildBotSecret/secret.json"
        secret = SecretManager(file, props)
        toochainFile = 'build/cmake/android.toolchain.cmake'

        defines = self.getDefinesList(props)

        defines += secret.convertToCmakeDefines()

        defines += [
            '-DCMAKE_PREFIX_PATH=$QTDIR',
            '-DQT_QMAKE_EXECUTABLE=$QTDIR/bin/qmake',
            '-DANDROID_ABI=arm64-v8a',
            '-DANDROID_BUILD_ABI_arm64-v8a=ON',
            '-DANDROID_BUILD_ABI_armeabi-v7a=ON',
            '-DCMAKE_FIND_ROOT_PATH=$QTDIR',
            '-DANDROID_NDK=$ANDROID_NDK_ROOT/',
            '-DANDROID_SDK=$ANDROID_SDK_ROOT/',
            '-DSIGN_ALIES="quasarapp"',
            '-DANDROID_NATIVE_API_LEVEL=$ANDROID_API_VERSION',
            '-DCMAKE_TOOLCHAIN_FILE=$ANDROID_NDK_ROOT/' + toochainFile,
            '-B cmake_build'
        ]

        options = [
            'cmake -GNinja',
        ]
        options += defines

        return ' '.join(options)

    def getQtMajorVersion(self):
        qtDir = os.getenv('QTDIR', "")
        if "5." in qtDir :
            return "5"
        elif "6." in qtDir:
            return "6"

        return "5"

    def androidXmakeSinglAbiCmd(self, props):
        file = self.home + "/buildBotSecret/secret.json"
        secret = SecretManager(file, props)
        toochainFile = 'build/cmake/android.toolchain.cmake'

        defines = self.getDefinesList(props)

        defines += secret.convertToCmakeDefines()

        qtDir = "$QTDIR/lib/cmake/Qt" + self.getQtMajorVersion()

        defines += [
            '-DQT_DIR=' + qtDir,
            '-DCMAKE_PREFIX_PATH=$QTDIR',
            '-DQT_QMAKE_EXECUTABLE=$QTDIR/bin/qmake',
            '-DANDROID_ABI=$ANDROID_ABI',
            '-DCMAKE_FIND_ROOT_PATH=$QTDIR',
            '-DANDROID_NDK=$ANDROID_NDK_ROOT/',
            '-DANDROID_SDK=$ANDROID_SDK_ROOT/',
            '-DSIGN_ALIES="quasarapp"',
            '-DANDROID_NATIVE_API_LEVEL=$ANDROID_API_VERSION',
            '-DCMAKE_TOOLCHAIN_FILE=$ANDROID_NDK_ROOT/' + toochainFile,
            '-B cmake_build'
        ]

        options = [
            'cmake -GNinja',
        ]
        options += defines

        return ' '.join(options)

    def androidXmakeCmd(self, props):
        return self.androidXmakeSinglAbiCmd(props)

    def wasmXmakeCmd(self, props):

        defines = self.getDefinesList(props)

        defines += [
            '-DCMAKE_PREFIX_PATH=$QTDIR',
            '-DTARGET_PLATFORM_TOOLCHAIN=wasm32',
            '-B cmake_build'
        ]

        options = [
            'cmake',
        ]

        options += defines

        return ' '.join(options)
