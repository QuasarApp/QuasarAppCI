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

    def __init__(self, platform):
        self.MULTIPLE_SH_COMMAND = ["/bin/bash", "-c"]
        self.home = str(Path.home())
        self.platform = platform

    def isWin(self, step):
        return self.platform == BaseModule.P_Windows

    def isLinux(self, step):
        return self.platform == BaseModule.P_Linux

    def isAndroid(self, step):
        return self.platform == BaseModule.P_Android

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

    def makeCommand(self, props):
        command = ['make']
        cpus = multiprocessing.cpu_count()

        if cpus:
            command.extend(['-j', str(cpus)])
        else:
            command.extend(['-j', '1'])
        return command
