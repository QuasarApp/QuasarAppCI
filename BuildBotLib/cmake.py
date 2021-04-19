# This Python file uses the following encoding: utf-8

from BuildBotLib.make import Make
from BuildBotLib.secretManager import SecretManager
import multiprocessing


class CMake(Make):

    def __init__(self, platform):
        Make.__init__(self, platform)
#        self.buildSystems = self.B_CMake

    def makePrefix(self):
        return "C"

    def mainCmd(self):
        options = [
            'cmake',
            "-B cmake_build"
        ]

        return ' '.join(options)

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
        return self.mainCmd()

    def windowsXmakeCmd(self, props):

        options = [
            'cmake -DCMAKE_PREFIX_PATH=%QTDIR%',
            '-DBUILD_SHARED_LIBS=1',
            '-DCMAKE_CXX_COMPILER=g++ -DCMAKE_C_COMPILER=gcc',
            '-DQT_QMAKE_EXECUTABLE=%QTDIR%/bin/qmake.exe',
            '"-GCodeBlocks - MinGW Makefiles"',
            '-B cmake_build'
        ]

        return ' '.join(options)

    def androidXmakeMultiAbiCmd(self, props):
        file = self.home + "/buildBotSecret/secret.json"
        secret = SecretManager(file, props)
        toochainFile = 'build/cmake/android.toolchain.cmake'

        options = [
            'cmake -GNinja',
            '-DCMAKE_PREFIX_PATH=$QTDIR',
            '-DQT_QMAKE_EXECUTABLE=$QTDIR/bin/qmake',
            '-DANDROID_ABI=arm64-v8a',
            '-DANDROID_BUILD_ABI_arm64-v8a=ON',
            '-DANDROID_BUILD_ABI_armeabi-v7a=ON',
            '-DCMAKE_FIND_ROOT_PATH=$QTDIR',
            '-DCMAKE_TOOLCHAIN_FILE=$ANDROID_NDK_ROOT/' + toochainFile,
            '-DANDROID_NDK=$ANDROID_NDK_ROOT/',
            '-DANDROID_SDK=$ANDROID_SDK_ROOT/',
            '-DSIGN_PATH="' + secret.getValue('SIGPATH') + '"',
            '-DSIGN_ALIES="quasarapp"',
            '-DSIGN_STORE_PASSWORD="' + secret.getValue('SIGPASS') + '"',
            '-B cmake_build'
        ]

        return ' '.join(options)

    def androidXmakeSinglAbiCmd(self, props):
        file = self.home + "/buildBotSecret/secret.json"
        secret = SecretManager(file, props)
        toochainFile = 'build/cmake/android.toolchain.cmake'

        options = [
            'cmake -GNinja',
            '-DCMAKE_PREFIX_PATH=$QTDIR',
            '-DQT_QMAKE_EXECUTABLE=$QTDIR/bin/qmake',
            '-DANDROID_ABI=$ANDROID_ABI',
            '-DCMAKE_FIND_ROOT_PATH=$QTDIR',
            '-DCMAKE_TOOLCHAIN_FILE=$ANDROID_NDK_ROOT/' + toochainFile,
            '-DANDROID_NDK=$ANDROID_NDK_ROOT/',
            '-DANDROID_SDK=$ANDROID_SDK_ROOT/',
            '-DSIGN_PATH="' + secret.getValue('SIGPATH') + '"',
            '-DSIGN_ALIES="quasarapp"',
            '-DSIGN_STORE_PASSWORD="' + secret.getValue('SIGPASS') + '"',
            '-B cmake_build'
        ]

        return ' '.join(options)

    def androidXmakeCmd(self, props):
        return self.androidXmakeSinglAbiCmd(props)

    def wasmXmakeCmd(self, props):
        options = [
            'cmake -DCMAKE_PREFIX_PATH=$QTDIR',
            '-DTARGET_PLATFORM_TOOLCHAIN=wasm32',
            '-B cmake_build'
        ]

        return ' '.join(options)
