#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Noémie Lehuby 2017                                         ##
##                                                                       ##
## This program is free software: you can redistribute it and/or modify  ##
## it under the terms of the GNU General Public License as published by  ##
## the Free Software Foundation, either version 3 of the License, or     ##
## (at your option) any later version.                                   ##
##                                                                       ##
## This program is distributed in the hope that it will be useful,       ##
## but WITHOUT ANY WARRANTY; without even the implied warranty of        ##
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         ##
## GNU General Public License for more details.                          ##
##                                                                       ##
## You should have received a copy of the GNU General Public License     ##
## along with this program.  If not, see <http://www.gnu.org/licenses/>. ##
##                                                                       ##
###########################################################################

from plugins.Plugin import Plugin


class Public_Transport_Stop(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[21411] = {"item": 2140, "level": 3, "tag": ["tag", "public_transport", "fix:chair"], "desc": T_(
            u"Missing public_transport tag on a public transport stop")}
        self.errors[21412] = {"item": 2140, "level": 3, "tag": ["tag", "public_transport", "fix:chair"], "desc": T_(
            u"Missing legacy tag on a public transport stop")}

    def node(self, data, tags):
        err = []
        if u"public_transport" not in tags:
            if "highway" in tags and tags["highway"] == "bus_stop":
                err.append({"class": 21411, "subclass": 0,
                            "text": T_("Bus stop without public_transport tag"),
                            "fix": {"public_transport": "platform"}
                            })
            if "railway" in tags and tags["railway"] == "tram_stop":
                err.append({"class": 21411, "subclass": 1,
                            "text": T_("Tram stop without public_transport tag"),
                            "fix": {"public_transport": "stop_position"}
                            })

        else
            if tags["public_transport"] == "platform" and not ("highway" in tags and tags["highway"] == "bus_stop"):
                if tags["bus"]== "yes" or "shelter" in tags :
                    err.append({"class": 21412, "subclass": 0,
                            "text": T_("This seems to be a bus stop"),
                            "fix": {"highway": "bus_stop"}
                            })
        return err



###########################################################################
from plugins.Plugin import TestPluginCommon


class Test(TestPluginCommon):
    def test(self):
        a = Public_Transport_Stop(None)
        a.init(None)

        assert a.node(None, {"highway":"bus_stop"})
        assert not a.node(None, {"highway":"bus_stop", "public_transport":"platform"})
        assert not a.node(None, {"highway":"bus_stop", "public_transport":"stop_position"})
        assert a.node(None, {"railway":"tram_stop"})
        assert not a.node(None, {"railway":"tram_stop", "public_transport":"stop_position"})
        assert a.node(None, {"public_transport":"platform", "shelter":"yes"})
