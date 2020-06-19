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

    def __init__(self):
        self.masterConf = {}
        self.masterConf['builders'] = []
        self.masterConf['schedulers'] = []
        self.masterConf['change_source'] = []

        # WORKERS
        self.workers = BuildBotWorkers(self.masterConf)
        self.masterConf.update(self.workers.getMasterConf())

        # BUILDBOT SERVICES
        self.services = BuildBotServices(self.masterConf)
        self.masterConf.update(self.services.getMasterConf())

        # PROJECT IDENTITY
        self.identity = BuildBotIdentity(self.masterConf)
        self.masterConf.update(self.identity.getMasterConf())

        # DB URL
        self.db = BuildBotDB(self.masterConf)
        self.masterConf.update(self.db.getMasterConf())

        # change_source
        self.sources = BuildBotChangeSource(self.masterConf)
        self.masterConf.update(self.sources.getMasterConf())

        # Shedulers
        self.shedulers = BuildBotShedulers(self.masterConf)

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

    def addService(self, service):
        logging.error("addService not support!")

    def getMaster(self):
        self.masterConf.update(self.shedulers.initScheduler())
        return self.masterConf
