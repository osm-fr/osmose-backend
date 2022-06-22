#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2012                                      ##
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
from modules.Stablehash import stablehash64
from .Analyser_Osmosis import Analyser_Osmosis

sql10 = """
CREATE TEMP TABLE rtag_{type} AS
SELECT
    key,
    SUM(count) AS count
FROM
    (
    SELECT
        key,
        count
    FROM
        (
        SELECT
            split_part((each(tags)).key, ':', 1) AS key,
            COUNT(*) AS count
        FROM
            {type}
        WHERE
            tags != ''::hstore
        GROUP BY
            key
        ) AS keys
    WHERE
        length(key) > 3 AND
        key NOT IN (
            'tower', -- vs power
            'food', -- vs foot, ford
            'fdot', -- vs foot (Florida)
            'diet', -- vs dirt, dist
            'dist', -- vs dirt, list, diet
            'lines', -- vs line, lanes
            'linz', -- vs line (New Zealand)
            'wine', -- vs line
            'levels', -- vs level
            'maxweight', -- vs maxheight
            'stop', -- vs shop
            'ship', -- vs shop
            'stars', -- vs start, stairs
            'right', -- vs light
            'truck',
            'tracks', -- vs traces
            'size', -- vs site, side
            'weight', -- vs height
            'lawyer', -- vs layer
            'hall', -- vs wall
            'well', -- vs wall
            'clock', -- vs lock
            'plane', -- vs place, plant, lane
            'services', -- vs service
            'room', -- vs roof, rooms
            'house', -- vs horse
            'addr2', 'addr3', 'addr4', 'addr5',
            'kern', -- vs kerb
            'lock_name', -- vs loc_name
            'camp_type', -- vs lamp_type
            'lock_ref', -- vs loc_ref
            'change', -- vs charge
            'mail', -- vs email
            'lock', -- vs rock, dock
            'rock', -- vs lock, dock, rack
            'reg_name', -- vs ref_name
            'massage', -- vs message
            'bath', -- vs path
            'port', -- vs sport, post
            'cave', -- vs cafe
            'produce', -- vs product
            'side', -- vs site, sides, hide
            'draft', -- vs craft
            'fridge', -- vs bridge
            'moved', -- vs moped
            'name_1', 'name_2', 'name_3', 'name_4', 'name_5', 'name_6', 'name_7', 'name_8', 'name_9', -- Tiger mess

            -- Regional hiking/cycling/etc. routes. Lesser used ones like 'rhn' for horse riding trigger false positives:
            'rcn', 'rhn', 'rin', 'rmn', 'rpn', 'rwn',
            'rcn:name', 'rhn:name', 'rin:name', 'rmn:name', 'rpn:name', 'rwn:name',
            'operator:rcn', 'operator:rhn', 'operator:rin', 'operator:rmn', 'operator:rpn', 'operator:rwn',
            'rcn_ref', 'rhn_ref', 'rin_ref', 'rmn_ref', 'rpn_ref', 'rwn_ref',
            'expected_rcn_route_relations', 'expected_rhn_route_relations', 'expected_rin_route_relations',
            'expected_rmn_route_relations', 'expected_rpn_route_relations', 'expected_rwn_route_relations'
        ) AND
        NOT key LIKE 'AND_%'
    ) AS keys
GROUP BY
    key
"""

sql20 = """
CREATE TEMP TABLE fix_{type} AS
SELECT DISTINCT ON (t1.key)
    t1.key as low_key,
    t2.key as hight_key
FROM
    rtag_{type} AS t1,
    rtag_{type} AS t2
WHERE
    t1.count < t2.count / 20 AND
    abs(length(t1.key) - length(t2.key)) <= 1 AND
    levenshtein(t1.key, t2.key) <= 1
ORDER BY
    t1.key,
    t2.count DESC
"""

sql30 = """
SELECT
    id,
    key,
    value,
    low_key,
    hight_key,
    ST_AsText({as_text})
FROM
    (
    SELECT
        id,
        (each(tags)).key AS key,
        (each(tags)).value AS value,
        {geo}
    FROM
        {table}
    GROUP BY
        id,
        key,
        value,
        {geo}
    ) AS keys,
    fix_{type} As fix
WHERE
    keys.key = fix.low_key OR
    (POSITION(':' IN keys.key) > 0 AND SUBSTRING(keys.key FROM 1 FOR LENGTH(fix.low_key)+1) = fix.low_key || ':')
"""

class Analyser_Osmosis_Tag_Typo(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs[1] = self.def_class(item = 3150, level = 1, tags = ['tag', 'fix:chair'],
            title = T_('Typo in tag'),
            detail = T_(
'''The tag is misspelled. Detection is based on statistics.'''),
            trap = T_(
'''Check that the correction does not change the intent of the tag.'''))

    def analyser_osmosis_common(self):
        self.run(sql10.format(type="nodes"))
        self.run(sql20.format(type="nodes"))
        self.run(sql30.format(type="nodes", as_text="geom", table="nodes", geo="geom"), lambda res: {
            "class":1,
            "subclass": stablehash64(res[1]),
            "data":[self.node_full, None, None, None, None, self.positionAsText],
            "text": {"en": "{0} -> {1}".format(res[1], res[1].replace(res[3], res[4], 1))},
            "fix":{"-": [res[1]], "+": {res[1].replace(res[3], res[4], 1): res[2] }} })

        self.run(sql10.format(type="ways"))
        self.run(sql20.format(type="ways"))
        self.run(sql30.format(type="ways", as_text="way_locate(linestring)", table="ways", geo="linestring"), lambda res: {
            "class":1,
            "subclass": stablehash64(res[1]),
            "data":[self.way_full, None, None, None, None, self.positionAsText],
            "text": {"en": "{0} -> {1}".format(res[1], res[1].replace(res[3], res[4], 1))},
            "fix":{"-": [res[1]], "+": {res[1].replace(res[3], res[4], 1): res[2] }} })

        self.run(sql10.format(type="relations"))
        self.run(sql20.format(type="relations"))
        self.run(sql30.format(type="relations", as_text="relation_locate(id)", table="relations", geo="user"), lambda res: {
            "class":1,
            "subclass": stablehash64(res[1]),
            "data":[self.relation_full, None, None, None, None, self.positionAsText],
            "text": {"en": "{0} -> {1}".format(res[1], res[1].replace(res[3], res[4], 1))},
            "fix":{"-": [res[1]], "+": {res[1].replace(res[3], res[4], 1): res[2] }} })
