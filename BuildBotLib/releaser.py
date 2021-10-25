# This Python file uses the following encoding: utf-8
from BuildBotLib.basemodule import BaseModule
from buildbot.plugins import util, steps


class Releaser(Make):
    def __init__(self):
        Make.__init__(self, BaseModule.P_Linux)


    def getFactory(self):
        factory = BaseModule.getFactory()

        @util.renderer
        def getProdName(props):
            return str(props.getProperty('prodName'))

        @util.renderer
        def getUrl(params):
            baseUrl = self.destDirUrl(params)
            prodName = str(props.getProperty('prodName'))
            return baseUrl + prodName

        factory.addStep(
            self.generateStep(["wget", getUrl],
                              self.platform,
                              'get last build ',
                              lambda step: True)
        )

        factory.addStep(
            self.generateStep(['dpkg', '-i', getProdName],
                              self.platform,
                              'Install new version of server',
                              lambda step: True)
        )

        factory.addStep(
            self.generateStep("rm * -rdf",
                              self.platform,
                              'Clean ',
                              lambda step: True)
        )


        return factory


    def getPropertyes(self):

        base = BaseModule().getPropertyes()

        return base + [
            util.BooleanParameter(
                name='prodName',
                label='Name of the production server file. (by default prod.deb)',
                default='prod.deb'
            ),
        ]
