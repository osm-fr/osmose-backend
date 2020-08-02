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

from modules.Stablehash import stablehash64
from .Analyser_Osmosis import Analyser_Osmosis

sql10 = """
CREATE TEMP TABLE rtag_{0} AS
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
            {0}
        WHERE
            tags != ''::hstore
        GROUP BY
            key
        ) AS keys
    WHERE
        length(key) > 3 AND
        key NOT IN (
            'tower', 'power',
            'food', 'foot',
            'diet', 'dist',
            'line', 'lines',
            'level', 'levels',
            'color', 'colour',
            'maxweight', 'maxheight',
            'stop', 'shop',
            'stars', 'start',
            'right', 'light',
            'truck',
            'size', 'site',
            'weight', 'height',
            'lawyer',
            'hall', 'well',
            'clock',
            'plane',
            'services', 'service',
            'room', 'rooms',
            'house', 'horse',
            'addr2', 'addr3',
            'kerb', 'kern',
            'lock_name', 'loc_name',
            'camp_type', 'lamp_type',
            'static_caravans', 'static_caravan',
            'loc_ref', 'lock_ref',
            'charge', 'change',
            'mail', 'email',
            'lock', 'rock',
            'reg_name', 'ref_name',
            'massage', 'message',
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
CREATE TEMP TABLE fix_{0} AS
SELECT DISTINCT ON (t1.key)
    t1.key as low_key,
    t2.key as hight_key
FROM
    rtag_{0} AS t1,
    rtag_{0} AS t2
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
    ST_AsText(%(as_text)s)
FROM
    (
    SELECT
        id,
        (each(tags)).key AS key,
        (each(tags)).value AS value,
        %(geo)s
    FROM
        %(table)s
    GROUP BY
        id,
        key,
        value,
        %(geo)s
    ) AS keys,
    fix_{0} As fix
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
        self.run(sql10.format("nodes"))
        self.run(sql20.format("nodes"))
        self.run(sql30.format("nodes") % {"as_text": "geom", "table": "nodes", "geo": "geom"}, lambda res: {
            "class":1,
            "subclass": stablehash64(res[1]),
            "data":[self.node_full, None, None, None, None, self.positionAsText],
            "text": {"en": "{0} -> {1}".format(res[1], res[1].replace(res[3], res[4], 1))},
            "fix":{"-": [res[1]], "+": {res[1].replace(res[3], res[4], 1): res[2] }} })

        self.run(sql10.format("ways"))
        self.run(sql20.format("ways"))
        self.run(sql30.format("ways") % {"as_text": "way_locate(linestring)", "table": "ways", "geo": "linestring"}, lambda res: {
            "class":1,
            "subclass": stablehash64(res[1]),
            "data":[self.way_full, None, None, None, None, self.positionAsText],
            "text": {"en": "{0} -> {1}".format(res[1], res[1].replace(res[3], res[4], 1))},
            "fix":{"-": [res[1]], "+": {res[1].replace(res[3], res[4], 1): res[2] }} })

        self.run(sql10.format("relations"))
        self.run(sql20.format("relations"))
        self.run(sql30.format("relations") % {"as_text": "relation_locate(id)", "table": "relations", "geo": "user"}, lambda res: {
            "class":1,
            "subclass": stablehash64(res[1]),
            "data":[self.relation_full, None, None, None, None, self.positionAsText],
            "text": {"en": "{0} -> {1}".format(res[1], res[1].replace(res[3], res[4], 1))},
            "fix":{"-": [res[1]], "+": {res[1].replace(res[3], res[4], 1): res[2] }} })
