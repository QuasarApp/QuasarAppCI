# This Python file uses the following encoding: utf-8

import BuildBotLib.basemodule as base
from buildbot.plugins import util, steps


def getFactory():
    factory = base.getFactory();

    list = [
        steps.Git(
            repourl='https://github.com/QuasarApp/quasarAppCoin.git',
            branch=util.Interpolate('%(prop:Branch)s'),
            mode='incremental',
            submodules=True
        ),
        steps.ShellCommand(
            command= ['qmake'],
        ),
        steps.ShellCommand(
            command= ['make', 'deploy'],
        ),
        steps.CopyDirectory(
            src="build/Distro",
            dest="~/shared/quasarAppCoin/"
        )

    ]

    factory.addSteps(list);

    return factory

def getRepo():
    return "https://github.com/QuasarApp/quasarAppCoin.git";

def getPropertyes():
    return [
        util.StringParameter(
            name = 'Branch',
            label = 'Branch of project',
            default = 'master',
        )
    ]
