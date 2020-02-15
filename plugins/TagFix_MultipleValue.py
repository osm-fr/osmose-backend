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

# SQL code to generate the list of not-yet checked tags containing ";" in database
"""
DROP VIEW tags CASCADE;
CREATE TEMP VIEW tags AS
SELECT
    id,
    (each(tags)).key,
    (each(tags)).value
FROM
    nodes
;

SELECT
    DISTINCT(key, value)
FROM
    tags
WHERE
    NOT key LIKE '%source%' AND
    NOT key LIKE 'note%' AND
    NOT key LIKE '%ref%' AND
    NOT key LIKE '4C:%' AND
    NOT key LIKE 'CLC:%' AND
    NOT key LIKE 'seamark:%' AND
    key NOT IN (
    -- Accept multiple values
    'opening_hours', 'description', 'bus_routes', 'phone', 'created_by', 'comment', 'day_off', 'day_on', 'destination', 'fixme', 'FIXME', 'access', 'is_in', 'alt_name', 'boundary', 'fee', 'id', 'marked_trail', 'sport', 'shop', 'school:FR', 'hour_off', 'hour_on', 'old_name', 'operator', 'park_ride', 'antenna', 'brewery', 'collection_times', 'cuisine', 'exit_to', 'towards', 'traffic_sign', 'url', 'brand', 'service', 'material',
    -- No multiple value
    'cycleway', 'highway', 'foot', 'layer', 'landuse', 'foot', 'building', 'left:city', 'left:country', 'left:departement', 'left:village', 'right:city', 'right:country', 'right:departement', 'right:village', 'name','maxspeed', 'lanes', 'oneway', 'admin_level', 'natural', 'smoothness', 'surface', 'tracktype', 'type', 'voltage', 'waterway', 'width', 'wikipedia', 'wires', 'wood', 'trail_visibility', 'bicycle', 'est_width', 'motorcar' 'mtb:scale', 'ele', 'power', 'railway', 'addr:housenumber', 'addr:street', 'attraction', 'amenity', 'leisure' ) AND
    value LIKE '%;%'
;
"""

from plugins.Plugin import Plugin
from modules.Stablehash import stablehash64

class TagFix_MultipleValue(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[3070] = self.def_class(item = 3070, level = 2, tags = ['value', 'fix:chair'],
            title = T_('Multiple values'),
            detail = T_(
'''The tag contains multiple values.'''),
            fix = T_(
'''Check the accuracy of the values, if necessary, delete the obsolete
values.'''))

        self.SimpleValuedTag = set((
                    'addr:street', 'admin_level', 'amenity', 'attraction',
                    'bicycle', 'building',
                    'cycleway',
                    'ele', 'est_width',
                    'foot',
                    'highway',
                    'landuse', 'lanes', 'layer',
                    'left:city', 'left:country', 'left:departement', 'left:village',
                    'leisure',
                    'maxspeed', 'motorcar', 'mtb:scale',
                    'name', 'natural',
                    'oneway',
                    'power',
                    'railway',
                    'right:city', 'right:country', 'right:departement', 'right:village',
                    'smoothness', 'surface',
                    'tracktype', 'trail_visibility', 'type',
                    'waterway', 'width', 'wikipedia', 'wires', 'wood',
                   ))


    def node(self, data, tags):
        err = []
        keys = tags.keys()
        keys = set(keys) & self.SimpleValuedTag
        for k in keys:
            if ';' in tags[k]:
                err.append({"class": 3070, "subclass": stablehash64(k), "text": T_f("Concerns tag: `{0}`", '='.join([k, tags[k]])) })

        return err

    def way(self, data, tags, nds):
        return self.node(data, tags)

    def relation(self, data, tags, members):
        return self.node(data, tags)

###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = TagFix_MultipleValue(None)
        a.init(None)
        for t in [{"highway": "trunk;primary"},
                  {"oneway": "yes;yes"},
                  {"oneway": "yes;no"},
                 ]:
            self.check_err(a.node(None, t), t)
            self.check_err(a.way(None, t, None), t)
            self.check_err(a.relation(None, t, None), t)

        for t in [{"highway": "trunk"},
                  {"oneway": "yes"},
                  {"oneway": "yes"},
                  {"ueueau": "yes;no"},
                 ]:
            assert not a.node(None, t), t
