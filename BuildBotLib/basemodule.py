import os
from buildbot.plugins import util
import multiprocessing
import glob
import shutil
from pathlib import Path


class BaseModule:

    def __init__(self):
        self.MULTIPLE_SH_COMMAND = ["/bin/bash", "-c"]
        self.home = str(Path.home())

    def isWin(self, step):
        return step.getProperty('Windows')

    def isLinux(self, step):
        return step.getProperty('Linux')

    def isAndroid(self, step):
        return step.getProperty('Android')

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
            util.BooleanParameter(
                name='Windows',
                label='Windows version project',
                default=True
            ),

            util.BooleanParameter(
                name='Linux',
                label='Linux version project',
                default=True
            ),

            util.BooleanParameter(
                name='Android',
                label='Android version project',
                default=True
            ),
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
