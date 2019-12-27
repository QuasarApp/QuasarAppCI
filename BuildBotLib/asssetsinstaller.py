# This Python file uses the following encoding: utf-8

from BuildBotLib.basemodule import BaseModule
from buildbot.plugins import util, steps
import os
from pathlib import Path


class AsssetsInstaller(BaseModule):
    def __init__(self):
        BaseModule.__init__(self)

    format = ""

    AndroidBaseDir = str(Path.home()) + "/Android"

    def isInit(self, step):
        return step.getProperty('module') == 'init'

    def RemoveOldData(self, props):

        cmd = "mkdir -p " + self.AndroidBaseDir

        if os.path.exists(self.AndroidBaseDir):
            cmd = "rm -rdf " + self.AndroidBaseDir + " ; " + cmd

        return self.generateCmd(cmd)

    def NDKDownloadCMD(self, props):
        link = props.getProperty("link")

        self.format = link[link.rfind('.'):].lower()

        return ["curl",
                link,
                "--output",
                self.AndroidBaseDir + "/temp" + self.format]

    def ExtractCMD(self, props):

        res = ["echo", "format '" + self.format + "' not supported"]

        if self.format == ".zip":
            res = ["unzip", self.AndroidBaseDir + "/temp" + self.format,
                   "-d", self.AndroidBaseDir]

        return res

    def InstallCMD(self, props):

        module = props.getProperty("module")
        version = props.getProperty("version")

        unit_to_multiplier = {
            'SDK': 'platform-tools;tools;platforms;android-'+version,
            'NDK': 'ndk-bundle'
        }

        return "sdkmanager " + unit_to_multiplier.get(module, "--list")

    def ConfigureCMD(self, props):

        res = ["echo", "Configure failed"]

        if self.format == ".zip":

            all_subdirs = self.allSubdirsOf(self.AndroidBaseDir)
            latest_subdir = max(all_subdirs, key=os.path.getmtime)
            res = "mv " + latest_subdir + " " + self.AndroidBaseDir + "/tools"
            res += " ; ln -sf "
            res += self.AndroidBaseDir + "/tools/bin/sdkmanager "
            res += self.home + "/.local/bin/sdkmanager"
            res += " ; yes | sdkmanager --licenses"

        return self.generateCmd(res)

    def getFactory(self):
        factory = super().getFactory()

        factory.addStep(
            steps.ShellCommand(
                command=self.getWraper(self.RemoveOldData),
                name='rm old  item',
                doStepIf=self.getWraper(self.isInit),
                description='rm old',
                haltOnFailure=True,
            )
        )

        factory.addStep(
            steps.ShellCommand(
                command=self.getWraper(self.NDKDownloadCMD),
                name='download new item',
                doStepIf=self.getWraper(self.isInit),
                description='download new item',
                haltOnFailure=True,
            )
        )

        factory.addStep(
            steps.ShellCommand(
                command=self.getWraper(self.ExtractCMD),
                name='extract new item',
                doStepIf=self.getWraper(self.isInit),
                description='extract new item',
                haltOnFailure=True,
            )
        )

        factory.addStep(
            steps.ShellCommand(
                command=self.getWraper(self.ConfigureCMD),
                name='configure new item',
                doStepIf=self.getWraper(self.isInit),
                description='configure new item',
                haltOnFailure=True,
            )
        )

        factory.addStep(
            steps.ShellCommand(
                command=self.getWraper(self.InstallCMD),
                name='install module',
                doStepIf=lambda step: not self.isInit(step),
                description='configure new item',
                haltOnFailure=True,
            )
        )

        return factory

    def getPropertyes(self):
        return [
            util.ChoiceStringParameter(
                name='module',
                choices=["init", "SDK", "NDK"],
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
