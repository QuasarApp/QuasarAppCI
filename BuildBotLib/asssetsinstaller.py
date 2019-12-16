# This Python file uses the following encoding: utf-8

import BuildBotLib.basemodule as base
from buildbot.plugins import util, steps
import os

LAST_FORMAT = [""]


@util.renderer
def RemoveOldData(props):
    module = props.getProperty("module")
    dirpath = props.getProperty("builddir") + "/build"

    res = ["echo",  dirpath + "/" + module + " not exits"]

    if os.path.exists(dirpath + "/" + module):
        res = ["rm", "-rdf", dirpath + "/" + module]

    return res


@util.renderer
def NDKDownloadCMD(props):
    link = props.getProperty("link")

    res = []
    format = link[link.rfind('.'):].lower()
    LAST_FORMAT[0] = format

    res = ["curl", link, "--output", "temp" + format]

    return res


@util.renderer
def ExtractCMD(props):

    format = LAST_FORMAT[0]
    module = props.getProperty("module")

    res = ["echo", "format '" + format + "' not supported"]

    if format == ".zip":
        res = ["unzip", "temp" + format, "-d", module]

    return res


@util.renderer
def ConfigureCMD(props):

    format = LAST_FORMAT[0]
    module = props.getProperty("module")

    res = ["echo", "Configure " + module + " failed"]

    if format == ".zip":
        dirpath = props.getProperty("builddir") + "/build/" + module

        all_subdirs = base.allSubdirsOf(dirpath)
        latest_subdir = max(all_subdirs, key=os.path.getmtime)
        res = ["mv", latest_subdir, dirpath + "/current"]

    return res


def getFactory():
    factory = base.getFactory()

    factory.addStep(
        steps.ShellCommand(
            command=RemoveOldData,
            name='rm old  item',
            description='rm old',
            haltOnFailure=True,
        )
    )

    factory.addStep(
        steps.ShellCommand(
            command=NDKDownloadCMD,
            name='download new item',
            description='download new item',
            haltOnFailure=True,
        )
    )

    factory.addStep(
        steps.ShellCommand(
            command=ExtractCMD,
            name='extract new item',
            description='extract new item',
            haltOnFailure=True,
        )
    )

    factory.addStep(
        steps.ShellCommand(
            command=ConfigureCMD,
            name='configure new item',
            description='configure new item',
            haltOnFailure=True,
        )
    )

    return factory


def getRepo():
    return ""


def getPropertyes():
    return [
        util.ChoiceStringParameter(
            name='module',
            choices=["AndroidNDK", "AndroidSDK"],
            default="AndroidNDK"
        ),

        util.StringParameter(
            name='link',
            label="url to download item",
            default=""
        ),
    ]
