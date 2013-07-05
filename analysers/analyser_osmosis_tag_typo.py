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

from Analyser_Osmosis import Analyser_Osmosis

sql10 = """
DROP TABLE IF EXISTS rtag;
CREATE TEMP TABLE rtag AS
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
            %s
        GROUP BY
            key
        ) AS keys
    WHERE
        length(key) > 3 AND
        key NOT IN (
            'tower', 'power',
            'food', 'foot',
            'line', 'lines',
            'level', 'levels',
            'color', 'colour',
            'maxweight', 'maxheight',
            'stop', 'shop',
            'stars', 'start',
            'services', 'service')
    ) AS keys
GROUP BY
    key
;
"""

sql20 = """
DROP TABLE IF EXISTS fix CASCADE;
CREATE TEMP TABLE fix AS
SELECT
    t1.key as low_key,
    t2.key as hight_key
FROM
    rtag AS t1,
    rtag AS t2
WHERE
    t1.count < t2.count / 20 AND
    abs(length(t1.key) - length(t1.key)) <= 1 AND
    levenshtein(t1.key, t2.key) <= 1
;
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
    fix
WHERE
    keys.key = fix.low_key OR
    (POSITION(':' IN keys.key) > 0 AND SUBSTRING(keys.key FROM 1 FOR LENGTH(fix.low_key)+1) = fix.low_key || ':')
;
"""

class Analyser_Osmosis_Tag_Typo(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs[1] = {"item":"3150", "level": 1, "tag": ["tag", "fix:chair"], "desc": T_(u"Typo in tag") }

    def analyser_osmosis(self):
        self.run(sql10 % "nodes")
        self.run(sql20)
        self.run(sql30 % {"as_text": "geom", "table": "nodes", "geo": "geom"}, lambda res: {
            "class":1,
            "data":[self.node_full, None, None, None, None, self.positionAsText],
            "fix":{"-": [res[1]], "+": {res[1].replace(res[3], res[4], 1): res[2] }} })

        self.run(sql10 % "ways")
        self.run(sql20)
        self.run(sql30 % {"as_text": "way_locate(linestring)", "table": "ways", "geo": "linestring"}, lambda res: {
            "class":1,
            "data":[self.way_full, None, None, None, None, self.positionAsText],
            "fix":{"-": [res[1]], "+": {res[1].replace(res[3], res[4], 1): res[2] }} })

        # TODO relations
