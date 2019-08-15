# This Python file uses the following encoding: utf-8
from BuildBotLib.buildBotModule import *
from buildbot.plugins import util
from buildbot.plugins import changes
import os

class buildBotChangeSource(BuildBotModule):
    def __init__(self):
        BuildBotModule.__init__(self)

        self.masterConf['change_source'] = [
            changes.GitPoller(
                repourl = 'git@github.com:QuasarApp/Snake.git',
                project = 'qmake-Snake',
                gitbin = os.path.dirname(os.path.realpath(__file__)) + "/git/gitBin.sh",
                branches = True, # получаем изменения со всех веток
                pollInterval = 60
            ),
            changes.GitPoller(
                repourl = 'git@github.com:QuasarApp/Console-QtDeployer.git',
                project = 'qmake-CQtDeployer',
                gitbin = os.path.dirname(os.path.realpath(__file__)) + "/git/gitBin.sh",
                branches = True, # получаем изменения со всех веток
                pollInterval = 61
            ),
            changes.GitPoller(
                repourl = 'git@github.com:QuasarApp/Qt-Secret.git',
                project = 'qmake-Qt-Secret',
                gitbin = os.path.dirname(os.path.realpath(__file__)) + "/git/gitBin.sh",
                branches = True, # получаем изменения со всех веток
                pollInterval = 62
            ),
            changes.GitPoller(
                repourl = 'git@github.com:QuasarApp/Hanoi-Towers.git',
                project = 'qmake-Hanoi-Towers',
                gitbin = os.path.dirname(os.path.realpath(__file__)) + "/git/gitBin.sh",
                branches = True, # получаем изменения со всех веток
                pollInterval = 63
            ),
            changes.GitPoller(
                repourl = 'https://github.com/usermeme/chat-vironit.git',
                project = 'npm-Chat',
                gitbin = os.path.dirname(os.path.realpath(__file__)) + "/git/gitBin.sh",
                branch = 'master',
                pollInterval = 64
            )
        ]

