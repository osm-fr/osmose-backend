#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Didier Marchand  <****@free.fr> 2013                       ##
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
from .Analyser_Osmosis import Analyser_Osmosis

sql10 = """
CREATE TEMP TABLE c1 AS
WITH
cvqnotag AS (
    SELECT
        ways.id,
        tags - ARRAY['source', 'created_by'] AS tags,
        CASE
            WHEN ST_X(ST_StartPoint(linestring)) = ST_X(ST_EndPoint(linestring)) THEN
                CASE
                    WHEN ST_Y(ST_StartPoint(linestring)) < ST_Y(ST_EndPoint(linestring)) THEN linestring
                    ELSE ST_Reverse(linestring)
                END
            WHEN ST_X(ST_StartPoint(linestring)) < ST_X(ST_EndPoint(linestring)) THEN linestring
            ELSE ST_Reverse(linestring)
        END as linestring,
        sha224(ST_AsBinary(
            CASE
                WHEN ST_X(ST_StartPoint(linestring)) = ST_X(ST_EndPoint(linestring)) THEN
                    CASE
                        WHEN ST_Y(ST_StartPoint(linestring)) < ST_Y(ST_EndPoint(linestring)) THEN linestring
                        ELSE ST_Reverse(linestring)
                    END
                WHEN ST_X(ST_StartPoint(linestring)) < ST_X(ST_EndPoint(linestring)) THEN linestring
                ELSE ST_Reverse(linestring)
            END
        )) as linestring_hash
    FROM
        ways
        LEFT JOIN relation_members ON
            relation_members.member_id = ways.id AND
            relation_members.member_type = 'W'
    WHERE
        relation_members.member_id IS NULL AND
        ways.tags = ''::hstore AND
        ST_NPoints(ways.linestring) > 1 AND
        ST_IsValid(linestring)
),
c AS (
    SELECT
        id,
        tags,
        linestring_hash,
        linestring,
        COUNT(*) OVER (PARTITION BY linestring_hash) as count
    FROM
        cvqnotag
)
SELECT
    *
FROM
    c
WHERE
    count >= 2
"""

sql11 = """
CREATE INDEX idx_c1_linestring_hash ON c1(linestring_hash)
"""

sql12 = """
SELECT
    b1.id AS id1,
    b2.id AS id2,
    ST_AsText(ST_Centroid(b1.linestring))
FROM
    c1 AS b1
    JOIN c1 AS b2 ON
        b1.id > b2.id AND
        b1.linestring_hash = b2.linestring_hash
WHERE
    ST_Equals(b1.linestring, b2.linestring)
"""

sql20 = """
CREATE TEMP TABLE c2 AS
WITH
cvqn AS (
    SELECT
        ways.id,
        tags - ARRAY['source', 'created_by'] AS tags,
        CASE
            WHEN ST_X(ST_StartPoint(linestring)) = ST_X(ST_EndPoint(linestring)) THEN
                CASE
                    WHEN ST_Y(ST_StartPoint(linestring)) < ST_Y(ST_EndPoint(linestring)) THEN linestring
                    ELSE ST_Reverse(linestring)
                END
            WHEN ST_X(ST_StartPoint(linestring)) < ST_X(ST_EndPoint(linestring)) THEN linestring
            ELSE ST_Reverse(linestring)
        END as linestring,
        sha224(ST_AsBinary(
            CASE
                WHEN ST_X(ST_StartPoint(linestring)) = ST_X(ST_EndPoint(linestring)) THEN
                    CASE
                        WHEN ST_Y(ST_StartPoint(linestring)) < ST_Y(ST_EndPoint(linestring)) THEN linestring
                        ELSE ST_Reverse(linestring)
                    END
                WHEN ST_X(ST_StartPoint(linestring)) < ST_X(ST_EndPoint(linestring)) THEN linestring
                ELSE ST_Reverse(linestring)
            END
        )) as linestring_hash
    FROM
        ways
        LEFT JOIN relation_members ON
            relation_members.member_id = ways.id AND
            relation_members.member_type = 'W'
    WHERE
        relation_members.member_id IS NULL AND
        ways.tags != ''::hstore AND
        tags ?| ARRAY['area', 'name', 'natural', 'landuse', 'waterway', 'amenity', 'highway', 'leisure', 'barrier', 'railway', 'addr:interpolation', 'man_made', 'power', 'aeroway'] AND
        ST_NPoints(ways.linestring) > 1 AND
        ST_IsValid(linestring)
),
c AS (
    SELECT
        id,
        tags,
        linestring_hash,
        linestring,
        COUNT(*) OVER (PARTITION BY linestring_hash) as count
    FROM
        cvqn
)
SELECT
    *
FROM
    c
WHERE
    count >= 2
"""

sql21 = """
CREATE INDEX idx_c2_linestring_hash ON c2(linestring_hash)
"""

sql22 = """
SELECT
    b1.id AS id1,
    b2.id AS id2,
    ST_AsText(ST_Centroid(b1.linestring)),
--    ((b1.tags @> b2.tags ) AND (b2.tags @> b1.tags ))
    b1.tags = b2.tags
FROM
    c2 AS b1
    JOIN c2 AS b2 ON
        b1.id > b2.id AND
        b1.linestring_hash = b2.linestring_hash
WHERE
    ST_Equals(b1.linestring, b2.linestring) AND
    (
        (b1.tags->'area' = b2.tags->'area') OR
        (b1.tags->'name' = b2.tags->'name') OR
        (b1.tags->'natural' = b2.tags->'natural') OR
        (b1.tags->'landuse' = b2.tags->'landuse') OR
        (b1.tags->'waterway' = b2.tags->'waterway') OR
        (b1.tags->'amenity' = b2.tags->'amenity') OR
        (b1.tags->'highway' = b2.tags->'highway') OR
        (b1.tags->'leisure' = b2.tags->'leisure') OR
        (b1.tags->'barrier' = b2.tags->'barrier') OR
        (b1.tags->'railway' = b2.tags->'railway') OR
        (b1.tags->'addr:interpolation' = b2.tags->'addr:interpolation') OR
        (b1.tags->'man_made' = b2.tags->'man_made') OR
        (b1.tags->'aeroway' = b2.tags->'aeroway') OR
        (b1.tags->'power' = b2.tags->'power')
    ) AND
    (NOT b1.tags?'layer' AND NOT b2.tags?'layer' OR b1.tags->'layer' = b2.tags->'layer') AND
    (NOT b1.tags?'level' AND NOT b2.tags?'level' OR b1.tags->'level' = b2.tags->'level') AND
    (NOT b1.tags?'addr:floor' AND NOT b2.tags?'addr:floor' OR b1.tags->'addr:floor' = b2.tags->'addr:floor') AND
    (NOT b1.tags?'min_height' AND NOT b2.tags?'min_height' OR b1.tags->'min_height' = b2.tags->'min_height') AND
    (NOT b1.tags?'ele' AND NOT b2.tags?'ele' OR b1.tags->'ele' = b2.tags->'ele')
"""

sql30 = """
CREATE TEMP TABLE c3 AS
WITH
onlynodesfull AS (
    SELECT
    id,
    tags - ARRAY['source', 'created_by', 'converted_by', 'attribution'] AS tags,
    geom,
    sha224(ST_AsBinary(geom)) AS geom_hash
FROM
    nodes
WHERE
    tags != ''::hstore AND
    tags - ARRAY['source', 'created_by', 'converted_by', 'attribution'] != ''::hstore
),
c AS (
    SELECT
        id,
        tags,
        geom_hash,
        geom,
        COUNT(*) OVER (PARTITION BY geom_hash) as count
    FROM
        onlynodesfull
)
SELECT
    *
FROM
    c
WHERE
    count >= 2
"""

sql31 = """
CREATE INDEX idx_c3_geom_hash ON c3(geom_hash)
"""

sql32 = """
SELECT
    b1.id AS id1,
    b2.id AS id2,
    ST_AsText(b1.geom),
    b1.tags = b2.tags
FROM
    c3 AS b1
    JOIN c3 AS b2 ON
        b1.id > b2.id AND
        b1.geom_hash = b2.geom_hash
WHERE
    ST_Equals(b1.geom, b2.geom) AND
    -- fix false positive in denmark
    NOT (b1.tags?'osak:identifier' AND b2.tags?'osak:identifier' AND b1.tags->'osak:identifier' != (b2.tags->'osak:identifier')) AND
    (b1.tags @> b2.tags OR b2.tags @> b1.tags) AND
    (NOT b1.tags?'layer' AND NOT b2.tags?'layer' OR b1.tags->'layer' = b2.tags->'layer') AND
    (NOT b1.tags?'level' AND NOT b2.tags?'level' OR b1.tags->'level' = b2.tags->'level') AND
    (NOT b1.tags?'addr:floor' AND NOT b2.tags?'addr:floor' OR b1.tags->'addr:floor' = b2.tags->'addr:floor') AND
    (NOT b1.tags?'min_height' AND NOT b2.tags?'min_height' OR b1.tags->'min_height' = b2.tags->'min_height') AND
    (NOT b1.tags?'ele' AND NOT b2.tags?'ele' OR b1.tags->'ele' = b2.tags->'ele')
"""

sql40 = """
WITH
c AS (
    SELECT
        id,
        COUNT(*) OVER (PARTITION BY sha224(ST_AsBinary(geom))) as count,
        geom,
        sha224(ST_AsBinary(geom)) AS geom_hash
    FROM
        nodes
    WHERE
        tags - ARRAY['source', 'created_by', 'converted_by', 'attribution'] = ''::hstore
)
SELECT
    array_agg('N' || id::text) AS ids,
    ST_AsText(min(geom))
FROM
    c
WHERE
    count >= 2
GROUP BY
    geom_hash
"""

class Analyser_Osmosis_Duplicated_Geotag(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs[1] = self.def_class(item = 1230, level = 1, tags = ['geom', 'fix:chair'],
            title = T_('Duplicated way geometry and tags'),
            fix = T_(
'''Delete one of the two objects.'''))
        self.classs[2] = self.def_class(item = 1230, level = 2, tags = ['geom', 'fix:chair'],
            title = T_('Duplicated way geometry but different tags'),
            fix = T_(
'''Compare tags and delete object or merge them.'''))
        self.classs[3] = self.def_class(item = 1230, level = 1, tags = ['geom', 'fix:chair'],
            title = T_('Duplicated node geometry and tags'))
        self.classs[4] = self.def_class(item = 1230, level = 2, tags = ['geom', 'fix:chair'],
            title = T_('Duplicated node geometry but different tags'))
        self.classs[5] = self.def_class(item = 1230, level = 3, tags = ['geom', 'fix:chair'],
            title = T_('Duplicated node without tag'))

        self.callback10 = lambda res: {"class":1, "data":[self.way, self.way, self.positionAsText]}
        self.callback20 = lambda res: {"class":1 if res[3] else 2, "data":[self.way_full, self.way_full, self.positionAsText]}
        self.callback30 = lambda res: {"class":3 if res[3] else 4, "data":[self.node_full, self.node_full, self.positionAsText]}

    def analyser_osmosis_common(self):
        self.run(sql10)
        self.run(sql11)
        self.run(sql12, self.callback10)

        self.run(sql20)
        self.run(sql21)
        self.run(sql22, self.callback20)

        self.run(sql30)
        self.run(sql31)
        self.run(sql32, self.callback30)

        self.run(sql40, lambda res: {"class":5, "data":[self.array_full, self.positionAsText]})
