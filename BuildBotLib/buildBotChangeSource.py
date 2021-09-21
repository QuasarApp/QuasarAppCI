# This Python file uses the following encoding: utf-8
from BuildBotLib.buildBotModule import BuildBotModule
from BuildBotLib.secretManager import SecretManager
from pathlib import Path
from BuildBotLib.customgithubhandler import CustomGitHubHandler
from BuildBotLib.customgiteahandler import CustomGiteaHandler


class BuildBotChangeSource(BuildBotModule):
    def __init__(self, masterConf):
        BuildBotModule.__init__(self, masterConf)
        secretpath = str(Path.home()) + "/buildBotSecret/secret.json"
        secret = SecretManager(secretpath)

        self.masterConf['www']['change_hook_dialects'] = {
                'github':
                {
                    'secret': secret.getValue('WebHook'),
                    'class': CustomGitHubHandler
                },
                'gitea': {
                    'secret': secret.getValue('WebHookGitiea'),
                    'onlyIncludePushCommit': True,
                    'class': CustomGiteaHandler
                }
            }
