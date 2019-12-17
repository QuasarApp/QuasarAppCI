# This Python file uses the following encoding: utf-8

import BuildBotLib.basemodule as base
from buildbot.plugins import util, steps
import os
from pathlib import Path

LAST_FORMAT = [""]

AndroidBaseDir = str(Path.home()) + "/Android"


def isInit(step):
    return step.getProperty('module') == 'init'


@util.renderer
def RemoveOldData(props):

    res = ["mkdir", "-p", AndroidBaseDir]

    if os.path.exists(AndroidBaseDir):
        res = ["rm", "-rdf", AndroidBaseDir, ";",
               "mkdir", "-p", AndroidBaseDir]

    return res


@util.renderer
def NDKDownloadCMD(props):
    link = props.getProperty("link")

    res = []
    format = link[link.rfind('.'):].lower()
    LAST_FORMAT[0] = format

    res = ["curl", link, "--output", AndroidBaseDir + "/temp" + format]

    return res


@util.renderer
def ExtractCMD(props):

    format = LAST_FORMAT[0]

    res = ["echo", "format '" + format + "' not supported"]

    if format == ".zip":
        res = ["unzip", AndroidBaseDir "/temp" + format, "-d", AndroidBaseDir]

    return res


@util.renderer
def ConfigureCMD(props):

    module = props.getProperty("module")
    version = props.getProperty("version")

    res = ["sdkmanager"]

    unit_to_multiplier = {
        'SDK': ["platforms;android-"+version],
        'NDK': ["ndk-bundle"],
        'buildTools': ["platform-tools;tools;build-tools"+version]
    }

    return res + unit_to_multiplier[module]


@util.renderer
def InstallCMD(props):

    format = LAST_FORMAT[0]

    res = ["echo", "Configure failed"]

    if format == ".zip":

        all_subdirs = base.allSubdirsOf(AndroidBaseDir)
        latest_subdir = max(all_subdirs, key=os.path.getmtime)
        res = ["mv", latest_subdir, AndroidBaseDir + "/tools", ";",
               "ln", "-sf", AndroidBaseDir + "/tools/bin/sdkmanager",
               str(Path.home()) + "/.local/bin/sdkmanager"]

    return res


def getFactory():
    factory = base.getFactory()

    factory.addStep(
        steps.ShellCommand(
            command=RemoveOldData,
            name='rm old  item',
            doStepIf=isInit,
            description='rm old',
            haltOnFailure=True,
        )
    )

    factory.addStep(
        steps.ShellCommand(
            command=NDKDownloadCMD,
            name='download new item',
            doStepIf=isInit,
            description='download new item',
            haltOnFailure=True,
        )
    )

    factory.addStep(
        steps.ShellCommand(
            command=ExtractCMD,
            name='extract new item',
            doStepIf=isInit,
            description='extract new item',
            haltOnFailure=True,
        )
    )

    factory.addStep(
        steps.ShellCommand(
            command=ConfigureCMD,
            name='configure new item',
            doStepIf=isInit,
            description='configure new item',
            haltOnFailure=True,
        )
    )

    factory.addStep(
        steps.ShellCommand(
            command=InstallCMD,
            name='install module',
            doStepIf=lambda step: not isInit(step),
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
            choices=["init", "SDK", "NDK", "buildTools"],
            default="init"
        ),

        util.StringParameter(
            name='link',
            label="url to download item",
            default=""
        ),
        util.StringParameter(
            name='version',
            label="Version",
            default=""
        ),
    ]
