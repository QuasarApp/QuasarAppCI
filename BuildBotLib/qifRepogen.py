# This Python file uses the following encoding: utf-8
from BuildBotLib.basemodule import BaseModule
from buildbot.plugins import util, steps


class QIFRepogen (BaseModule):
    def __init__(self):
        BaseModule.init(self, BaseModule.P_Linux)
        self.repogen = "repogen"

    def getFactory(self):
        factory = super().getFactory()

        def generateRepogenCmd(props):
            repoLocation = props.getProperty('repoLocation') + "/"
            repoLocation += props.getProperty('platform')
            tempPackage = props.getProperty('tempPackage')

            cmd = [self.repogen,
                   "--update-new-components",
                   "-p",
                   tempPackage,
                   repoLocation
                   ]

            return cmd

        factory.addStep(
            steps.ShellCommand(
                command=self.getWraper(generateRepogenCmd),
                haltOnFailure=True,
                name='Generate repository',
                description='Generate repository',
            )
        )

        def generateRemoveCmd(props):
            tempPackage = props.getProperty('tempPackage')

            cmd = ["rm",
                   "-rdf",
                   tempPackage
                   ]

            return cmd

        factory.addStep(
            steps.ShellCommand(
                command=self.getWraper(generateRemoveCmd),
                haltOnFailure=True,
                name='Remove old Data',
                description='Remove old Data',
            )
        )

        return factory

    def getPropertyes(self):
        return [
            util.StringParameter(
                name='tempPackage',
                label='Folder with temp value for packing',
                default=""
            ),

            util.StringParameter(
                name='platform',
                label='target platform (linux of windows)',
                default=BaseModule.P_Linux
            ),

            util.StringParameter(
                name='repoLocation',
                label='repository location',
                default=self.home + "/repo/"
            ),
        ]
