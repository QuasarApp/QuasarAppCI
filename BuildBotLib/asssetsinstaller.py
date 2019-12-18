# This Python file uses the following encoding: utf-8

import BuildBotLib.basemodule as base
from buildbot.plugins import util, steps
import os
from pathlib import Path

LAST_FORMAT = [""]

AndroidBaseDir = str(Path.home()) + "/Android"
MULTIPLE_SH_COMMAND = ["/bin/bash", "-c"]


def isInit(step):
    return step.getProperty('module') == 'init'


@util.renderer
def RemoveOldData(props):

    cmd = "mkdir -p " + AndroidBaseDir

    if os.path.exists(AndroidBaseDir):
        cmd = "rm -rdf " + AndroidBaseDir + " ; " + cmd

    return MULTIPLE_SH_COMMAND + [cmd]


@util.renderer
def NDKDownloadCMD(props):
    link = props.getProperty("link")

    format = link[link.rfind('.'):].lower()
    LAST_FORMAT[0] = format

    return ["curl", link, "--output", AndroidBaseDir + "/temp" + format]


@util.renderer
def ExtractCMD(props):

    format = LAST_FORMAT[0]

    res = ["echo", "format '" + format + "' not supported"]

    if format == ".zip":
        res = ["unzip", AndroidBaseDir + "/temp" + format,
               "-d", AndroidBaseDir]

    return res


@util.renderer
def InstallCMD(props):

    module = props.getProperty("module")
    version = props.getProperty("version")

    unit_to_multiplier = {
        'SDK': '"platforms;android-'+version+'"',
        'NDK': '"ndk-bundle"',
        'buildTools': '"platform-tools;tools;build-tools'+version+'"'
    }

    return ["sdkmanager", unit_to_multiplier.get(module, "--list")]


@util.renderer
def ConfigureCMD(props):

    format = LAST_FORMAT[0]

    res = ["echo", "Configure failed"]

    if format == ".zip":

        all_subdirs = base.allSubdirsOf(AndroidBaseDir)
        latest_subdir = max(all_subdirs, key=os.path.getmtime)
        res = "mv " + latest_subdir + " " + AndroidBaseDir + "/tools"
        res += " ; ln -sf " + AndroidBaseDir + "/tools/bin/sdkmanager "
        res += str(Path.home()) + "/.local/bin/sdkmanager"

    return MULTIPLE_SH_COMMAND + [res]


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
