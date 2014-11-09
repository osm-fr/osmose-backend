#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Etienne Chové <chove@crans.org> 2009                       ##
## Copyrights Frédéric Rodrigo 2011                                      ##
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

class TagRemove_Incompatibles(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[900] = { "item": 4030, "level": 1, "tag": ["tag", "fix:chair"], "desc": T_(u"Tag conflict") }
        self.CONFLICT = {}
        self.CONFLICT[0] = set(['aerialway', 'aeroway', 'amenity', 'highway', 'railway', 'waterway', 'landuse'])
        self.CONFLICT[1] = set(['aerialway', 'aeroway', 'amenity', 'highway', 'leisure', 'railway', 'natural'])
        self.CONFLICT[2] = set(['aerialway', 'aeroway', 'amenity', 'highway', 'leisure', 'railway', 'waterway', 'place'])
        self.CONFLICT[3] = set(['building', 'place'])
        self.CONFLICT[4] = set(['information', 'place'])

    def node(self, data, tags):
        if 'railway' in tags and tags['railway'] in ('abandoned', 'tram'):
            del tags['railway']
        if ('railway' in tags and tags['railway'] == 'tram_stop' and
            'highway' in tags and tags['highway'] == 'bus_stop'):
            del tags['railway']
            del tags['highway']
        for i in range(0, len(self.CONFLICT)):
            conflict = set(tags).intersection(self.CONFLICT[i])
            if len(conflict) > 1:
                return [(900, 1, T_("Conflict between tags: %s", (", ".join(conflict))))]

        if 'bridge' in tags and 'tunnel' in tags and tags['bridge'] == 'yes' and tags['tunnel'] == 'yes':
            return [(900, 2, T_("Conflict between tags: 'bridge' and 'tunnel'"))]

    def way(self, data, tags, nds):
        return self.node(data, tags)

    def relation(self, data, tags, members):
        return self.node(data, tags)

###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = TagRemove_Incompatibles(None)
        a.init(None)
        for t in [{"aerialway": "yes", "aeroway": "yes"},
                  {"highway": "trunk", "railway": "rail"},
                  {"bridge": "yes", "tunnel": "yes"},
                 ]:
            self.check_err(a.node(None, t), t)
            self.check_err(a.way(None, t, None), t)
            self.check_err(a.relation(None, t, None), t)

        for t in [{"aerialway": "yes"},
                  {"highway": "residential", "railway": "tram"},
                  {"highway": "bus_stop", "railway": "tram_stop"},
                  {"bridge": "yes", "tunnel": "no"},
                 ]:
            assert not a.node(None, t), t
