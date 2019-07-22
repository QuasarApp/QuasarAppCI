# This Python file uses the following encoding: utf-8

import BuildBotLib.basemodule as base
from buildbot.plugins import util, steps

def getFactory():
    factory = base.getFactory();

    factory.addStep(steps.Git(repourl='git://github.com/buildbot/hello-world.git', mode='incremental'));
    factory.addStep(steps.ShellCommand(command=["trial", "hello"],
                                       env={"PYTHONPATH": "."}));
    return factory

def getRepo():
    return "git://github.com/buildbot/hello-world.git";

def getPropertyes():
    return []
