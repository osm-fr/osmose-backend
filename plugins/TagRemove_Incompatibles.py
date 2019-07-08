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
        self.WHITE_LIST = {
            'landuse': [
                ['school', 'amenity', 'school'],
                ['industrial', 'amenity', 'recycling'],
                ['retail', 'amenity', 'marketplace'],
                ['water', 'amenity', 'fountain'], # ?
            ],
            'place': [
                ['square', 'area', 'yes'],
                ['square', 'highway', 'pedestrian'],
            ],
            'highway': [
                ['elevator', 'railway', 'subway_entrance'],
                ['path', 'waterway', 'lock_gate'],
                ['footway', 'waterway', 'lock_gate'],
            ],
            'natural': [
                ['water', 'leisure', 'marina'],
            ],
            'amenity': [
                ['stables', 'leisure', 'horse_riding'],
            ],
        }.items()

    def node(self, data, tags):
        if tags.get('railway') in ('abandoned', 'tram', 'proposed', 'razed', 'construction', 'platform'):
            del tags['railway']
        if tags.get('waterway') == 'dam':
            del tags['waterway']
        if tags.get('railway') == 'tram_stop' and tags.get('highway') == 'bus_stop':
            del tags['railway']
            del tags['highway']
        stags = set(tags)
        for i in range(0, len(self.CONFLICT)):
            conflict = stags.intersection(self.CONFLICT[i])
            if len(conflict) > 1:
                for (k1, vs) in self.WHITE_LIST:
                    if k1 in conflict:
                        for (v1, k2, v2) in vs:
                            if tags[k1] == v1 and k2 in conflict and tags[k2] == v2:
                                conflict.remove(k1)
                                conflict.remove(k2)
                if len(conflict) > 1:
                    return {"class": 900, "subclass": 1, "text": T_("Conflict between tags: %s", (", ".join(sorted(conflict))))}

        if tags.get('bridge') == 'yes' and tags.get('tunnel') == 'yes':
            return {"class": 900, "subclass": 2, "text": T_("Conflict between tags: 'bridge' and 'tunnel'")}

        if tags.get('highway') == 'crossing' and tags.get('crossing') == 'no':
            return {"class": 900, "subclass": 3, "text": T_("Conflict between tags: crossing=no must be used without a highway=crossing")}

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
                  {"crossing": "no", "highway": "crossing"},
                 ]:
            self.check_err(a.node(None, t), t)
            self.check_err(a.way(None, t, None), t)
            self.check_err(a.relation(None, t, None), t)

        for t in [{"aerialway": "yes"},
                  {"highway": "residential", "railway": "tram"},
                  {"highway": "bus_stop", "railway": "tram_stop"},
                  {"bridge": "yes", "tunnel": "no"},
                  {"waterway": "dam", "highway": "road"},
                  {"landuse": "school", "amenity": "school"},
                  {"place": "square", "highway": "pedestrian"},
                 ]:
            assert not a.node(None, t), t
