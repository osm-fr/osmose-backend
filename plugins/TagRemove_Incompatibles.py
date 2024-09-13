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

from modules.OsmoseTranslation import T_
from plugins.Plugin import Plugin

class TagRemove_Incompatibles(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[900] = self.def_class(item = 4030, level = 1, tags = ['tag', 'fix:chair'],
            title = T_('Tag conflict'),
            detail = T_(
'''This object has two tags that represent different features. According to the principle of
[one feature, one OSM element](https://wiki.openstreetmap.org/wiki/One_feature,_one_OSM_element),
these should be mapped as two separate objects.'''),
            trap = T_(
'''Sometimes the object needs both tags.'''))

        self.CONFLICT = {}
        self.CONFLICT[0] = set(['aerialway', 'aeroway', 'amenity', 'highway', 'railway', 'waterway', 'landuse'])
        self.CONFLICT[1] = set(['aerialway', 'aeroway', 'amenity', 'highway', 'leisure', 'railway', 'natural'])
        self.CONFLICT[2] = set(['aerialway', 'aeroway', 'amenity', 'highway', 'leisure', 'railway', 'waterway', 'place'])
        self.CONFLICT[3] = set(['building', 'place'])
        self.CONFLICT[4] = set(['information', 'place'])
        self.WHITE_LIST = {
            'landuse': [
                ['school', 'amenity', 'school'], # deprecated
                ['education', 'amenity', 'school'],
                ['education', 'amenity', 'university'],
                ['education', 'amenity', 'college'],
                ['education', 'amenity', 'kindergarten'],
                ['industrial', 'amenity', 'recycling'],
                ['retail', 'amenity', 'marketplace'],
                ['retail', 'amenity', 'fuel'],
                ['retail', 'shop', 'mall'],
                ['commercial', 'amenity', 'boat_storage'],
                ['commercial', 'amenity', 'food_court'],
                ['commercial', 'amenity', 'driving_school'],
                ['military', 'aeroway', 'aerodrome'],
                ['religious', 'amenity', 'monastery'],
                ['forest', 'leisure', 'playground'],
                ['farmyard', 'amenity', 'animal_breeding'],
            ],
            'water': [
                ['pond', 'leisure', 'fishing'],
            ],
            'place': [
                ['square', 'area', 'yes'],
                ['square', 'highway', 'pedestrian'],
            ],
            'highway': [
                ['elevator', 'railway', 'subway_entrance'],
                ['path', 'waterway', 'lock_gate'],
                ['footway', 'waterway', 'lock_gate'],
                ['footway', 'railway', 'disused'],
                ['path', 'railway', 'disused'],
                ['footway', 'leisure', 'barefoot'],
                ['path', 'leisure', 'barefoot'],
                ['service', 'amenity', 'weighbridge'],
                ['service', 'leisure', 'slipway'],
                ['corridor', 'aeroway', 'jet_bridge'],
                ['crossing', 'railway', 'tram_crossing'],
            ],
            'natural': [
                ['water', 'leisure', 'marina'],
                ['water', 'leisure', 'swimming_area'],
                ['water', 'leisure', 'swimming_pool'],
                ['water', 'leisure', 'fishing'],
                ['water', 'amenity', 'fountain'], # ?
                ['sand', 'leisure', 'playground'],
                ['birds_nest', 'highway', 'street_lamp'],
                ['wood', 'leisure', 'playground'],
            ],
            'amenity': [
                ['stables', 'leisure', 'horse_riding'],
                ['drinking_water', 'natural', 'spring'],
                ['drinking_water', 'man_made', 'water_tap'],
                ['shelter', 'highway', 'bus_stop'],
                ['event_venue', 'leisure', 'garden'],
                ['gambling', 'leisure', 'adult_gaming_centre'],
                ['restaurant', 'leisure', 'amusement_arcade'],
                ['sanitary_dump_station', 'waterway', 'sanitary_dump_station'],
            ],
        }.items()

    def node(self, data, tags):
        if tags.get('railway') in ('abandoned', 'tram', 'proposed', 'razed', 'dismantled', 'construction', 'platform'):
            del tags['railway']
        if tags.get('waterway') == 'dam':
            del tags['waterway']
        if tags.get('railway') == 'tram_stop' and tags.get('highway') == 'bus_stop':
            del tags['railway']
            del tags['highway']
        if tags.get('leisure') == 'nature_reserve' and 'natural' in tags:
            del tags['natural']
        stags = set(tags)
        for i in range(0, len(self.CONFLICT)):
            conflict = stags.intersection(self.CONFLICT[i])
            if len(conflict) > 1:
                for (k1, vs) in self.WHITE_LIST:
                    if k1 in conflict:
                        for (v1, k2, v2) in vs:
                            if tags[k1] == v1 and k2 in conflict and tags[k2] == v2:
                                if k1 in conflict:
                                    conflict.remove(k1)
                                conflict.remove(k2)
                if len(conflict) > 1:
                    return {"class": 900, "subclass": 1, "text": T_("Conflict between tags: {0}", (", ".join(sorted(conflict))))}

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
                  {"amenity": "fountain", "leisure": "swimming_pool", "natural": "water"},
                 ]:
            self.check_err(a.node(None, t), t)
            self.check_err(a.way(None, t, None), t)
            self.check_err(a.relation(None, t, None), t)

        for t in [{"aerialway": "yes"},
                  {"highway": "residential", "railway": "tram"},
                  {"highway": "bus_stop", "railway": "tram_stop"},
                  {"waterway": "dam", "highway": "road"},
                  {"landuse": "school", "amenity": "school"},
                  {"place": "square", "highway": "pedestrian"},
                  {"leisure": "nature_reserve", "natural": "scrub"}
                 ]:
            assert not a.node(None, t), t
