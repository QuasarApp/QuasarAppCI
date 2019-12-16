# This Python file uses the following encoding: utf-8

import BuildBotLib.basemodule as base
from buildbot.plugins import util, steps
import os
import subprocess

LAST_FORMAT = [""]


@util.renderer
def RemoveOldData(props):
    module = props.getProperty("module")
    dirpath = props.getProperty("builddir") + "/build"

    res = [dirpath + "/" + module + " not exits"]

    if os.path.exists(dirpath + "/" + module):
        res = ["rm", "-rdf", dirpath + "/" + module]

    return res


@util.renderer
def NDKDownloadCMD(props):
    link = props.getProperty("link")
    module = props.getProperty("module")

    res = []
    format = link[link.rfind('.'):].lower()
    LAST_FORMAT[0] = format

    if module == "AndroidNDK":
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
        dirpath = props.getProperty("builddir") + "/build"

        all_subdirs = base.allSubdirsOf(dirpath + "/" + module)
        latest_subdir = max(all_subdirs, key=os.path.getmtime)
        subprocess.getoutput(["ln -sf " + latest_subdir + " " +
                              dirpath + "/current"])

        res = ["echo", "Configure " + module]

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
