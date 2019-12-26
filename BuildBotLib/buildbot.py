from buildbot.plugins import util
import logging
import sys
import os

from BuildBotLib.buildBotIdentity import BuildBotIdentity
from BuildBotLib.buildBotServices import BuildBotServices
from BuildBotLib.buildBotWorkers import BuildBotWorkers
from BuildBotLib.buildBotDB import BuildBotDB
from BuildBotLib.buildBotShedulers import BuildBotShedulers
from BuildBotLib.buildBotChangeSource import BuildBotChangeSource

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)


class BuildBot:
    masterConf = {}
    workers = BuildBotWorkers()
    services = BuildBotServices()
    identity = BuildBotIdentity()
    db = BuildBotDB()
    shedulers = BuildBotShedulers()
    sources = BuildBotChangeSource()
    builders = []

#    def importWithReload(self, name):
#        module = importlib.import_module(name);
#        return module;
    def __init__(self):
        self.masterConf = {}
        self.masterConf['builders'] = []
        self.masterConf['schedulers'] = []
        self.masterConf['change_source'] = []

        # WORKERS
        self.masterConf.update(self.workers.getMasterConf())

        # BUILDBOT SERVICES
        self.masterConf.update(self.services.getMasterConf())

        # PROJECT IDENTITY
        self.masterConf.update(self.identity.getMasterConf())

        # DB URL
        self.masterConf.update(self.db.getMasterConf())

        # change_source
        self.masterConf.update(self.sources.getMasterConf())

    def addBuilder(self, worker, factory):
        self.masterConf['builders'].append(
            util.BuilderConfig(
                name=worker,
                workernames=[worker],
                factory=factory.getFactory()
            )
        )
        self.shedulers.addScheduler(factory.getPropertyes(),
                                    worker)
        self.builders.append(worker)

    def addService(self, service):
        logging.error("addService not support!")

    def getMaster(self):
        self.masterConf.update(self.shedulers.initScheduler())
        return self.masterConf
