import sys
from buildbot.plugins import util
import multiprocessing
import glob
import shutil

def getFactory():
    return util.BuildFactory()

def getRepo():
    return "";

def getPropertyes():
    return []

@util.renderer
def makeCommand(props):
    command = ['make']
    cpus = multiprocessing.cpu_count()

    if cpus:
        command.extend(['-j', str(cpus)])
    else:
        command.extend(['-j', '1'])
    return command

def copyRegExp(source, dist):

    res = []

    for file in glob.glob(source):
        res.append(file)
        shutil.copy(file, dist)

    return res;
