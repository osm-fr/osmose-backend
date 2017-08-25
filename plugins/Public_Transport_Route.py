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


class Public_Transport_Route(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[21401] = {"item": 2140, "level": 3, "tag": ["tag", "public_transport"], "desc": T_(
            u"Missing public_transport:version tag on a public_transport route relation")}
        self.errors[21402] = {"item": 2140, "level": 3, "tag": ["tag", "public_transport"], "desc": T_(
            u"Missing network tag on a public_transport relation")}
        self.errors[21403] = {"item": 2140, "level": 3, "tag": ["tag", "public_transport"], "desc": T_(
            u"Missing operator tag on a public_transport relation")}
        self.errors[21404] = {"item": 2140, "level": 3, "tag": ["tag", "public_transport"], "desc": T_(
            u"Missing ref tag on a public_transport relation")}
        self.errors[21405] = {"item": 2140, "level": 3, "tag": ["tag", "public_transport"], "desc": T_(
            u"Missing from/to tag on a public_transport route relation")}

    def _is_public_transport_mode(self, route_tag):
        public_transport_modes = ['bus', 'coach', 'tram', 'trolleybus', 'share_taxi', 'monorail', 'aerialway', 'share_taxi',
                                  'train', 'light_rail', 'subway', 'school_bus', 'funicular', 'ferry']
        return route_tag in public_transport_modes

    def relation(self, data, tags, members):
        err = []
        if "type" in tags and tags[u"type"] in ["route", "route_master"]:
            route_type = tags[u"type"]
            if route_type in tags and self._is_public_transport_mode(tags[route_type]) :
                if route_type == "route":
                    subclass = 0
                    if u"public_transport:version" not in tags:
                        err.append({"class": 21401, "subclass": subclass})
                    if u"from" not in tags or u"to" not in tags:
                        err.append({"class": 21405, "subclass": subclass})
                else:
                    subclass = 1
                if u"network" not in tags:
                    err.append({"class": 21402, "subclass": subclass})
                if u"operator" not in tags:
                    err.append({"class": 21403, "subclass": subclass})
                if u"ref" not in tags:
                    err.append({"class": 21404, "subclass": subclass})
        return err


###########################################################################
from plugins.Plugin import TestPluginCommon


class Test(TestPluginCommon):
    def test(self):
        a = Public_Transport_Route(None)
        a.init(None)

        rel_ = {"type": "route"}
        for t in [
            dict(rel_, **{"route": "bus"}),
            dict(rel_, **{"route": "funicular"}),
            dict(rel_, **{"route": "funicular",
                          "public_transport_version": "2"}),
            dict(rel_, **{"name": u"Bus 28", "route": "bus"}),
        ]:
            self.check_err(a.relation(None, t, None), t)

        for t in [{"highway": "primary"},
                  {"route_master": "bus", "type": "route_master"},
                  rel_,
                  dict(rel_, **{"route": "hiking"}),
                  dict(rel_, **{"route": "tram",
                                "public_transport:version": "1"}),
                  dict(rel_, **{"route": "tram",
                                "public_transport:version": "2"}),
                  dict(rel_, **{"route": "coach",
                                "public_transport:version": u"legacy"}),
                  ]:
            assert not a.relation(None, t, None), t
