# This Python file uses the following encoding: utf-8

import BuildBotLib.basemodule as base
from buildbot.plugins import util, steps
import os
import shutil
import subprocess

LAST_FORMAT = [""]


@util.renderer
def NDKDownloadCMD(props):
    link = props.getProperty("link")
    module = props.getProperty("module")
    dirpath = props.getProperty("builddir")

    if os.path.exists(dirpath + "/" + module):
        shutil.rmtree(dirpath + "/" + module, ignore_errors=True)

    res = []
    format = link[link.rfind('.'):].lower()
    LAST_FORMAT[0] = format

    if module == "AndroidNDK":
        if os.path.exists(dirpath + "/temp" + format):
            os.remove(dirpath + "/temp" + format)
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
        dirpath = props.getProperty("builddir")

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
            command=NDKDownloadCMD,
            name='download new item',
            description='download new item',
        )
    )

    factory.addStep(
        steps.ShellCommand(
            command=ExtractCMD,
            name='extract new item',
            description='extract new item',
        )
    )

    factory.addStep(
        steps.ShellCommand(
            command=ConfigureCMD,
            name='configure new item',
            description='configure new item',
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
