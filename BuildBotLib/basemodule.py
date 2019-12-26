from buildbot.plugins import util
import multiprocessing
import glob
import shutil


class BaseModule:

    MULTIPLE_SH_COMMAND = ["/bin/bash", "-c"]

    def __init__(self):
        self

    def generateCmd(self, bashString):
        return self.MULTIPLE_SH_COMMAND + [bashString]

    def getFactory(self):
        return util.BuildFactory()

    def getRepo(self):
        return ""

    def getPropertyes(self):
        return []

    def copyRegExp(self, source, dist):

        res = []

        for file in glob.glob(source):
            res.append(file)
            shutil.copy(file, dist)

        return res

    @util.renderer
    def makeCommand(self, props):
        command = ['make']
        cpus = multiprocessing.cpu_count()

        if cpus:
            command.extend(['-j', str(cpus)])
        else:
            command.extend(['-j', '1'])
        return command
