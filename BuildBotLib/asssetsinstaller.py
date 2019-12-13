# This Python file uses the following encoding: utf-8

import BuildBotLib.basemodule as base
from buildbot.plugins import util, steps
import os
import shutil


@util.renderer
def NDKDownloadCMD(props):
    link = props.getProperty("revision")
    module = props.getProperty("module")

    if os.path.isfile(module):
        shutil.rmtree(module)

    res = []
    format = link[link.rfind('.'):]

    if module == "AndroidNDK":
        os.remove("temp" + format)
        res = ["curl", link, "--output", "temp" + format]

    return res


@util.renderer
def ExtractCMD(props):

    arr = os.listdir()
    format = ""
    module = props.getProperty("module")

    for file in arr:
        ix = file.find("temp.")
        if ix == 0:
            format = file[file.rfind('.'):]

    res = ["echo", "format '" + format + "' not supported"]

    if format == "zip":
        res = ["unsip", "-d", module]

    return res


def getFactory():
    factory = base.getFactory();

    factory.addStep(
            steps.ShellCommand(
            command = NDKDownloadCMD,
            name = 'download new item',
            description = 'download new item',
        )
    );

    factory.addStep(
            steps.ShellCommand(
            command = ExtractCMD,
            name = 'extract new item',
            description = 'extract new item',
        )
    );

    return factory


def getRepo():
    return "";


def getPropertyes():
    return [
        util.ChoiceStringParameter(
            name = 'module',
            choices=["AndroidNDK", "AndroidSDK"],
            default = "AndroidNDK"
        ),
    ]
