# This Python file uses the following encoding: utf-8

from BuildBotLib.buildBotModule import BuildBotModule
from buildbot.plugins import worker


class BuildBotWorkers(BuildBotModule):
    def __init__(self):
        BuildBotModule.__init__(self)
        # WORKERS

        # The 'workers' list defines the set
        # of recognized workers. Each element is
        # a Worker object, specifying a unique worker
        # name and password.  The same
        # worker name and password must be configured on the worker.
        self.masterConf['workers'] = [
            worker.Worker("github-worker", "pass"),
            worker.Worker("Tester", "pass"),
            worker.Worker("qtBuilder", "pass"),
            worker.Worker("NPM", "pass"),
            worker.Worker("assets-builder", "pass")

            ]

        # 'protocols' contains information
        # about protocols which master will use for
        # communicating with workers.
        # You must define at least 'port' option that workers
        # could connect to your master with this protocol.
        # 'port' must match the value configured into the workers (with their
        # --master option)

        self.masterConf['protocols'] = {'pb': {'port': 9989}}
