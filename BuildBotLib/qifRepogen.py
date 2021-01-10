# This Python file uses the following encoding: utf-8
from BuildBotLib.basemodule import BaseModule
from buildbot.plugins import util, steps


class QIFRepogen (BaseModule):
    def __init__(self):
        BaseModule.__init__(self, BaseModule.P_Linux)
        self.repogen = "repogen"

    def getFactory(self):
        factory = super().getFactory()

        def getRepoLocation(props):
            repoLocation = str(props.getProperty('repoLocation')) + "/"
            projectName = str(props.getProperty('projectName'))

            if (len(projectName) <= 0):
                raise Exception('Project undefined')

            repoLocation += projectName + "/"
            return repoLocation + str(props.getProperty('platform'))

        def generateChmodCmd(props):
            tempPackage = str(props.getProperty('tempPackage'))

            cmd = ["chmod",
                   "775",
                   "-R",
                   tempPackage
                   ]

            return cmd

        factory.addStep(
            steps.ShellCommand(
                command=self.getWraper(generateChmodCmd),
                haltOnFailure=True,
                name='chmod files',
                description='set rights for files',
            )
        )

        def generateRepogenCmd(props):
            repoLocation = getRepoLocation(props)
            tempPackage = str(props.getProperty('tempPackage'))

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
                label='target platform (linux, windows)',
                default=BaseModule.P_Linux
            ),

            util.StringParameter(
                name='projectName',
                label='name of buildet project',
                default=''
            ),

            util.StringParameter(
                name='repoLocation',
                label='repository location',
                default=self.defaultLocationOfQIFRepository()
            ),
        ]
