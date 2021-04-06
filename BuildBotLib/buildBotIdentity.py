# This Python file uses the following encoding: utf-8
from BuildBotLib.buildBotModule import BuildBotModule
from BuildBotLib.secretManager import SecretManager
from buildbot.plugins import util
from pathlib import Path


# PROJECT IDENTITY

# the 'title' string will appear at the top of this buildbot installation's
# home pages (linked to the 'titleURL').

class BuildBotIdentity(BuildBotModule):
    def __init__(self, masterConf):
        BuildBotModule.__init__(self, masterConf)

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

        self.masterConf['buildbotURL'] = "https://quasarapp.ddns.net:8043/"

        # minimalistic config to activate new web UI
        self.masterConf['www'] = dict(port=8010,
                                      plugins=dict(
                                        waterfall_view={},
                                        console_view={},
                                        grid_view={}))

        scr = SecretManager(str(Path.home()) + "/buildBotSecret/secret.json")

        self.masterConf['www']['auth'] = util.GitHubAuth(
            scr.getValue("QuasarAppCIID"),
            scr.getValue("QuasarAppCIToken"),
            apiVersion=4, getTeamsMembership=True)

        self.masterConf['www']['authz'] = util.Authz(
                allowRules=[
#                    util.StopBuildEndpointMatcher(role="owner"),

                    util.StopBuildEndpointMatcher(role="QuasarApp"),
                    util.ForceBuildEndpointMatcher(role="QuasarApp"),
                    util.RebuildBuildEndpointMatcher(role="QuasarApp"),
                    util.AnyEndpointMatcher(role="admins"),

#                    util.AnyEndpointMatcher(role="QuasarApp"),

                ],
                roleMatchers=[
                  util.RolesFromGroups(groupPrefix=''),
                  util.RolesFromUsername(roles=[
                                                    "admins",
                                               ],
                                         usernames=[
                                                    "EndrII"
                                                   ]),

                  util.RolesFromOwner(role="owner")

                ]
        )
