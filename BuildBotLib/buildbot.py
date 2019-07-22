from buildbot.plugins import util
import logging
import importlib
import sys
from BuildBotLib.testmodule import *
import os
from buildbot.changes.gitpoller import GitPoller

from BuildBotLib.buildBotIdentity import *
from BuildBotLib.buildBotServices import *
from BuildBotLib.buildBotWorkers import *
from BuildBotLib.buildBotDB import *
from BuildBotLib.buildBotShedulers import *
from BuildBotLib.buildBotChangeSource import *

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)

class BuildBot:
    masterConf = {}
    workers = buildBotWorkers()
    services = buildBotServices()
    identity = buildBotIdentity()
    db = BuildBotDB()
    shedulers = buildBotShedulers()
    sources = buildBotChangeSource()
    builders = []


    def importWithReload(self, name):
        module = importlib.import_module(name);
        return module;

    def __init__(self):
        self.masterConf = BuildmasterConfig = {}
        self.masterConf['builders'] = []
        self.masterConf['schedulers'] = []
        self.masterConf['change_source'] = []

        ####### WORKERS
        self.masterConf.update(self.workers.getMasterConf());

        ####### BUILDBOT SERVICES
        self.masterConf.update(self.services.getMasterConf());

        ####### PROJECT IDENTITY
        self.masterConf.update(self.identity.getMasterConf());

        ####### DB URL
        self.masterConf.update(self.db.getMasterConf());

        ####### change_source
        self.masterConf.update(self.sources.getMasterConf());


    def addBuilder(self, worker, factory):
        module = self.importWithReload(factory);
        self.masterConf['builders'].append(
            util.BuilderConfig(
                name = worker,
                workernames = [worker],
                factory = module.getFactory()
            )
        )
        self.shedulers.addScheduler(module.getPropertyes(), worker)
        self.builders.append(worker);


    def addService(self, service):
        logging.error("addService not support!")

    def getMaster(self):

        self.masterConf.update(self.shedulers.initScheduler());
        return self.masterConf
