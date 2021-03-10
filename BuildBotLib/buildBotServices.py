# This Python file uses the following encoding: utf-8
from BuildBotLib.buildBotModule import BuildBotModule
from buildbot.plugins import reporters, util
from BuildBotLib.secretManager import SecretManager
from pathlib import Path
from buildbot.reporters.generators.build import BuildStartEndStatusGenerator


class BuildBotServices(BuildBotModule):
    def __init__(self, masterConf):
        BuildBotModule.__init__(self, masterConf)

        # BUILDBOT SERVICES

        # 'services' is a list of BuildbotService
        # items like reporter targets. The
        # status of each build will be pushed to these targets.
        # buildbot/reporters/*.py
        # has a variety to choose from, like IRC bots.

        self.masterConf['services'] = []
        secretPath = str(Path.home()) + "/buildBotSecret/secret.json"
        secret = SecretManager(secretPath)

        status_generator = BuildStartEndStatusGenerator(
            start_formatter=reporters.MessageFormatterRenderable('Build started.'),
            end_formatter=reporters.MessageFormatterRenderable('Build finished.'),
        )

        contextVal = util.Interpolate("buildbot/%(prop:buildername)s")
        gc = reporters.GitHubStatusPush(
                                        token=secret.getValue('gitHub'),
                                        context=contextVal,
                                        verbose=True,
                                        generators=[status_generator]
                                        )

        self.masterConf['services'].append(gc)
