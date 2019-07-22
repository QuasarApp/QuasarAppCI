# This Python file uses the following encoding: utf-8
from BuildBotLib.buildBotModule import *
from buildbot.plugins import util
from buildbot.plugins import changes

class buildBotChangeSource(BuildBotModule):
    def __init__(self):
        BuildBotModule.__init__(self)

        self.masterConf['change_source'] = [
            changes.GitPoller(
                repourl = 'git@github.com:QuasarApp/Snake.git',
                project = 'Snake',
                branches = True, # получаем изменения со всех веток
                pollInterval = 60
            ),
            changes.GitPoller(
                repourl = 'git@github.com:QuasarApp/Console-QtDeployer.git',
                project = 'CQtDeployer',
                branches = True, # получаем изменения со всех веток
                pollInterval = 61
            ),
            changes.GitPoller(
                repourl = 'git@github.com:QuasarApp/Qt-Secret.git',
                project = 'Qt-Secret',
                branches = True, # получаем изменения со всех веток
                pollInterval = 62
            ),
            changes.GitPoller(
                repourl = 'git@github.com:QuasarApp/Hanoi-Towers.git',
                project = 'Hanoi-Towers',
                branches = True, # получаем изменения со всех веток
                pollInterval = 63
            ),
        ]

