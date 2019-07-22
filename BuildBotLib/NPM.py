# This Python file uses the following encoding: utf-8

import BuildBotLib.basemodule as base
from buildbot.plugins import secrets, util, steps
from pathlib import Path
import datetime
import os
import subprocess
from BuildBotLib.secretManager import *

def getFactory():
    factory = base.getFactory();

    factory.addStep(
        steps.Git(
            repourl=util.Interpolate('%(prop:repository)s'),
            branch=util.Interpolate('%(prop:branch)s'),
            mode='full',
            method = 'fresh',
            submodules=True,
            name = 'git operations',
            description = 'operations of git like pull clone fetch',
        )
    );

    factory.addStep(
        steps.ShellCommand(
            command = [
                'npm',
                "stop"
                ],
            haltOnFailure = True,
            name = 'npm stop',
            description = 'stop old version',
        )
    );

    factory.addStep(
        steps.ShellCommand(
            command = [
                'npm',
                "i"
                ],
            haltOnFailure = True,
            name = 'npm install',
            description = 'install all dependecies',
        )
    );

    factory.addStep(
        steps.ShellCommand(
            command = [
                'npm',
                "start"
                ],
            haltOnFailure = True,
            name = 'npm start',
            description = 'install new versio to server',
        )
    );

    return factory

def getRepo():
    return "";

def getPropertyes():
    return [
    ]
