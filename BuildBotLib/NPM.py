# This Python file uses the following encoding: utf-8

import BuildBotLib.basemodule as BaseModule
from buildbot.plugins import secrets, util, steps
from pathlib import Path
import datetime
import os
import subprocess
from BuildBotLib.secretManager import *


class NPM(BaseModule):

    def __init__(self):
        BaseModule.__init__(self);

    def isStopForce(self, step):
        return step.getProperty('stopForce');

    def isLog(self, step):
        return step.getProperty('showLog');

    def getFactory(self):
        factory = self.getFactory();

        factory.addStep(
            steps.Git(
                repourl=util.Interpolate('%(prop:repository)s'),
                branch=util.Interpolate('%(prop:branch)s'),
                mode='full',
                method = 'fresh',
                submodules=True,
                name = 'git operations',
                description = 'operations of git like pull clone fetch',
                doStepIf = lambda step : not self.isStopForce(step) and not self.isLog(step),

            )
        );

        factory.addStep(
            steps.ShellCommand(
                command = [
                    'npm',
                    "stop"
                    ],
                doStepIf = lambda step : (not self.isLog(step)) ,
                haltOnFailure = True,
                name = 'npm stop',
                description = 'stop old version',
            )
        );

        factory.addStep(
            steps.ShellCommand(
                command = [
                    'docker-compose',
                    "logs"
                    ],
                doStepIf = lambda step : (not self.isStopForce(step)) and self.isLog(step),
                haltOnFailure = True,
                name = 'docker logs',
                description = 'docker logs',
            )
        );

        factory.addStep(
            steps.ShellCommand(
                command = [
                    'npm',
                    "i"
                    ],
                doStepIf = lambda step : not self.isStopForce(step) and not self.isLog(step),
                haltOnFailure = True,
                name = 'npm install',
                description = 'install all dependecies',
            )
        );

        factory.addStep(
            steps.ShellCommand(
                command = [
                    'npm',
                    "run",
                    "start:detach"
                    ],
                doStepIf = lambda step : not self.isStopForce(step) and not self.isLog(step),
                haltOnFailure = True,
                name = 'npm start',
                description = 'install new versio to server',
            )
        );

        return factory

    def getPropertyes(self):
        return [
            util.BooleanParameter(
                name = 'stopForce',
                label = 'Stop Force',
                default = False
            ),
            util.BooleanParameter(
                name = 'showLog',
                label = 'show logs of the docker',
                default = False
            )
        ]
