import os
from buildbot.plugins import util
import multiprocessing
import glob
import shutil
from pathlib import Path


class BaseModule:

    P_Windows = 'Windows'
    P_Linux = 'Linux'
    P_Android = 'Android'
    P_Wasm = 'Wasm'

    def __init__(self, platform):
        self.MULTIPLE_SH_COMMAND = ["/bin/bash", "-c"]
        self.home = str(Path.home())
        self.platform = platform
#        self.detectedBuildSystems = 0
#        self.buildSystems = 0
#        self.B_CMake = 1
#        self.B_QMake = 2

    def isWin(self, step):
        return self.platform == BaseModule.P_Windows

    def isLinux(self, step):
        return self.platform == BaseModule.P_Linux

    def isAndroid(self, step):
        return self.platform == BaseModule.P_Android

    def isWasm(self, step):
        return self.platform == BaseModule.P_Wasm

    def generateCmd(self, bashString):

        if isinstance(bashString, list):
            return bashString

        return self.MULTIPLE_SH_COMMAND + [bashString]

    def getFactory(self):
        return util.BuildFactory()

    def getRepo(self):
        return ""

    def getWraper(self, object):

        @util.renderer
        def cmdWraper(step):
            if not callable(object):
                return self.generateCmd(object)

            return object(step)

        return cmdWraper

    def getPropertyes(self):
        return [
        ]

    def copyRegExp(self, source, dist):

        res = []

        for file in glob.glob(source):
            res.append(file)
            shutil.copy(file, dist)

        return res

    def allSubdirsOf(self, b='.'):
        result = []
        for d in os.listdir(b):
            bd = os.path.join(b, d)
            if os.path.isdir(bd):
                result.append(bd)

        return result

    def make(self):
        if self.platform == BaseModule.P_Windows:
            return 'mingw32-make'

        return 'make'

    def makeTarget(self, target):
        command = [self.make()]
        return command + [target]

    def makeCommand(self, props):
        command = [self.make()]

        cpus = multiprocessing.cpu_count()

        if cpus:
            command.extend(['-j', str(cpus)])
        else:
            command.extend(['-j', '1'])
        return command

    def defaultLocationOfQIFRepository(self):
        return "/var/www/repo/"
