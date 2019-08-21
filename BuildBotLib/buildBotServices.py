# This Python file uses the following encoding: utf-8
from BuildBotLib.buildBotModule import *
from buildbot.plugins import reporters, util
from BuildBotLib.secretManager import *

class buildBotServices(BuildBotModule):
    def __init__(self):
        BuildBotModule.__init__(self)

        ####### BUILDBOT SERVICES

        # 'services' is a list of BuildbotService items like reporter targets. The
        # status of each build will be pushed to these targets. buildbot/reporters/*.py
        # has a variety to choose from, like IRC bots.

        self.masterConf['services'] = []
        secret = SecretManager("/home/andrei/buildBotSecret/secret.json")

        contextVal = util.Interpolate("buildbot/%(prop:buildername)s")
        gc = reporters.GitHubStatusPush(token=secret.getValue('gitHub'),
                                            context = contextVal,
                                            verbose = True,
                                            startDescription='Build started.',
                                            endDescription='Build done.')

        self.masterConf['services'].append(gc)
