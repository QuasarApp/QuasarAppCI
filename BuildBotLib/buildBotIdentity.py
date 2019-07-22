# This Python file uses the following encoding: utf-8
from buildbot.www import authz, auth
from buildbot.plugins import *
from BuildBotLib.buildBotModule import *

####### PROJECT IDENTITY

# the 'title' string will appear at the top of this buildbot installation's
# home pages (linked to the 'titleURL').

class buildBotIdentity(BuildBotModule):
    def __init__(self):
        self.masterConf['title'] = "QuasarApp CI"
        self.masterConf['titleURL'] = "https://github.com/QuasarApp/Console-QtDeployer"

        # the 'buildbotURL' string should point to the location where the buildbot's
        # internal web server is visible. This typically uses the port number set in
        # the 'www' entry below, but with an externally-visible host name which the
        # buildbot cannot figure out without some help.

        self.masterConf['buildbotURL'] = "http://quasarapp.ddns.net:8010/"
        #c['buildbotURL'] = "http://192.168.100.2:8010/"


        # minimalistic config to activate new web UI
        self.masterConf['www'] = dict(port=8010,
                        plugins=dict(waterfall_view={}, console_view={}, grid_view={}))

        self.masterConf['www']['authz'] = util.Authz(
                allowRules = [
                    util.AnyEndpointMatcher(role="admins")
                ],
                roleMatchers = [
                    util.RolesFromUsername(roles=['admins'], usernames=['EndrII']),
                    util.RolesFromUsername(roles=['admins'], usernames=['ZIG'])
                ]
        )

        self.masterConf['www']['auth'] = util.UserPasswordAuth([
            ('EndrII', util.Interpolate('%(secret:ENDRII)s')),
            ('ZIG', util.Interpolate('%(secret:ZIG)s'))
            ])

