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
            u"Missing public_transport:version tag on a public_tranport route relation")}

    def _is_public_transport_route(self, type_tag, route_tag):
        public_transport_modes = ['bus', 'coach', 'tram', 'trolleybus', 'share_taxi',
                                  'train', 'light_rail', 'subway', 'school_bus', 'funicular', 'ferry']
        return type_tag == "route" and route_tag in public_transport_modes

    def relation(self, data, tags, members):
        err = []
        if "type" in tags and "route" in tags and self._is_public_transport_route(tags[u"type"], tags[u"route"]) and u"public_transport:version" not in tags:
            err.append({"class": 21401, "subclass": 0})
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
