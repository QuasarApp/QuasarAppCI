# This Python file uses the following encoding: utf-8
from BuildBotLib.buildBotModule import *

class BuildBotDB(BuildBotModule):
    def __init__(self):
        BuildBotModule.__init__(self)

        ####### DB URL

        self.masterConf['db'] = {
            # This specifies what database buildbot uses to store its state.  You can leave
            # this at its default for all but the largest installations.
            'db_url' : "sqlite:///state.sqlite",
        }
