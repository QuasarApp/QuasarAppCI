# This Python file uses the following encoding: utf-8
from BuildBotLib.buildBotModule import BuildBotModule
from BuildBotLib.secretManager import SecretManager
from pathlib import Path


class BuildBotChangeSource(BuildBotModule):
    def __init__(self, masterConf):
        BuildBotModule.__init__(self, masterConf)

        secret = SecretManager(str(Path.home()) + "/buildBotSecret/secret.json")

        self.masterConf['www']['change_hook_dialects'] = {
                'github':
                {
                    'secret': secret.getValue('WebHook'),
                },
            }
