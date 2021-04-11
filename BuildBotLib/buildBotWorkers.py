# This Python file uses the following encoding: utf-8

from BuildBotLib.buildBotModule import BuildBotModule
from buildbot.plugins import worker
from BuildBotLib.secretManager import SecretManager
from pathlib import Path


class BuildBotWorkers(BuildBotModule):
    def __init__(self, masterConf):
        BuildBotModule.__init__(self, masterConf)
        # WORKERS

        # The 'workers' list defines the set
        # of recognized workers. Each element is
        # a Worker object, specifying a unique worker
        # name and password.  The same
        # worker name and password must be configured on the worker.
        scr = SecretManager(str(Path.home()) + "/buildBotSecret/secret.json")

        password = scr.getValue('WorkerPass')

        self.masterConf['workers'] = [
            worker.Worker("LinuxBuilder", password),
            worker.Worker("WindowsBuilder", password),
            worker.Worker("AndroidBuilder_v7", password),
            worker.Worker("AndroidBuilder_v8", password),
            worker.Worker("LinuxCMakeBuilder", password),
            worker.Worker("WindowsCMakeBuilder", password),
            worker.Worker("RepoGen", password),
            worker.Worker("Wasm32Builder", password),
            worker.Worker("DocsGenerator", password),
            ]

        # 'protocols' contains information
        # about protocols which master will use for
        # communicating with workers.
        # You must define at least 'port' option that workers
        # could connect to your master with this protocol.
        # 'port' must match the value configured into the workers (with their
        # --master option)

        self.masterConf['protocols'] = {'pb': {'port': 9989}}
