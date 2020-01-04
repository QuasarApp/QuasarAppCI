# This Python file uses the following encoding: utf-8
from BuildBotLib.buildBotModule import BuildBotModule
from BuildBotLib.secretManager import SecretManager
from buildbot.plugins import util


# PROJECT IDENTITY

# the 'title' string will appear at the top of this buildbot installation's
# home pages (linked to the 'titleURL').

class BuildBotIdentity(BuildBotModule):
    def __init__(self):
        self.masterConf['title'] = "QuasarApp CI"
        cqtdeployer_path = 'https://github.com/QuasarApp/CQtDeployer'
        self.masterConf['titleURL'] = cqtdeployer_path

        # the 'buildbotURL' string should point to the
        # location where the buildbot's
        # internal web server is visible.
        # This typically uses the port number set in
        # the 'www' entry below,
        # but with an externally-visible host name which the
        # buildbot cannot figure out without some help.

        self.masterConf['buildbotURL'] = "http://quasarapp.ddns.net:8010/"

        # minimalistic config to activate new web UI
        self.masterConf['www'] = dict(port=8010,
                                      plugins=dict(
                                        waterfall_view={},
                                        console_view={},
                                        grid_view={}))

        self.masterConf['www']['authz'] = util.Authz(
                allowRules=[
                    util.AnyEndpointMatcher(role="admins"),
                    util.StopBuildEndpointMatcher(builder="*", role="owner"),
                    util.ForceBuildEndpointMatcher(builder="github",
                                                   role="quasarcore"),
                    util.RebuildBuildEndpointMatcher(builder="github",
                                                     role="quasarcore")
                ],
                roleMatchers=[
                  util.RolesFromGroups(groupPrefix='QuasarApp/'),
                  #util.RolesFromEmails(admins=["EndrIIMail@gmail.com"]),
                  util.RolesFromOwner(role="owner")

                ]
        )

        secret = SecretManager("/home/andrei/buildBotSecret/secret.json")

        self.masterConf['www']['auth'] = util.GitHubAuth(
            secret.getValue("QuasarAppCIID"),
            secret.getValue("QuasarAppCIToken"),
            apiVersion=4, getTeamsMembership=True)
