# This Python file uses the following encoding: utf-8
from BuildBotLib.buildBotModule import BuildBotModule
from buildbot.plugins import changes
import os
from BuildBotLib.secretManager import SecretManager


class BuildBotChangeSource(BuildBotModule):
    def __init__(self):
        BuildBotModule.__init__(self)

        secret = SecretManager("/home/andrei/buildBotSecret/secret.json")

        self.masterConf['www']['change_hook_dialects'] = [
            { 'github': {
                'secret': secret.getValue('WebHook'),
                'strict': True,
            },
            },
        ]
