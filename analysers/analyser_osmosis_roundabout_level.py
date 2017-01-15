#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2012-2015                                 ##
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
CREATE FUNCTION level(highway varchar) RETURNS int AS $$
DECLARE BEGIN
    RETURN CASE
        WHEN highway = 'motorway' THEN 7
        WHEN highway = 'motorway_link' THEN 7
        WHEN highway = 'trunk' THEN 7
        WHEN highway = 'trunk_link' THEN 7
        WHEN highway = 'primary' THEN 6
        WHEN highway = 'primary_link' THEN 6
        WHEN highway = 'secondary' THEN 5
        WHEN highway = 'secondary_link' THEN 5
        WHEN highway = 'tertiary' THEN 4
        WHEN highway = 'tertiary_link' THEN 4
        WHEN highway = 'unclassified' THEN 3
        WHEN highway = 'residential' THEN 3
        WHEN highway = 'service' THEN 2
        WHEN highway = 'road' THEN 1
        ELSE 0
    END;
END
$$ LANGUAGE plpgsql
   IMMUTABLE
   RETURNS NULL ON NULL INPUT
"""

sql11 = """
CREATE TEMP TABLE roundabout AS
SELECT
    id,
    level(tags->'highway') AS level,
    tags->'highway' AS highway,
    linestring,
    nodes
FROM
    ways
WHERE
    tags != ''::hstore AND
    tags?'junction' AND
    tags->'junction' = 'roundabout' AND
    tags?'highway' AND
    array_length(nodes, 1) > 3 AND
    nodes[1] = nodes[array_length(nodes,1)] AND
    level(tags->'highway') > 0
"""

sql12 = """
CREATE INDEX roundabout_id_idx ON roundabout(id)
"""

sql13 = """
CREATE INDEX roundabout_linestring_idx ON roundabout USING gist(linestring)
"""

sql14 = """
CREATE TEMP TABLE roundabout_ways AS
SELECT
    roundabout.id AS rid,
    roundabout.level AS rlevel,
    roundabout.highway AS rhighway,
    roundabout.linestring AS rlinestring,
    level(ways.tags->'highway') AS wlevel
FROM
    roundabout
    JOIN ways ON
        roundabout.linestring && ways.linestring AND
        roundabout.nodes && ways.nodes AND
        roundabout.id != ways.id AND
        ways.tags != ''::hstore AND
        ways.tags?'highway'
"""

sql15 = """
CREATE TEMP TABLE roundabout_ways_wlevel1 AS
SELECT
    rid,
    MAX(wlevel) AS wlevel1
FROM
    roundabout_ways
GROUP BY
    rid
HAVING
    MAX(wlevel) < 7 -- doesn't force motorway or trunk roundabout as local trafic may pass through
"""

sql15i = """
CREATE INDEX idx_roundabout_ways_wlevel1_rid ON roundabout_ways_wlevel1(rid)
"""

sql16 = """
CREATE TEMP TABLE roundabout_ways_wlevel2 AS
SELECT
    rid,
    MAX(wlevel) AS wlevel2
FROM
    (
    SELECT
        rid,
        wlevel
    FROM
        roundabout_ways
    GROUP BY
        rid,
        wlevel
    HAVING
        COUNT(*) >= 2
    ) AS t
GROUP BY
    rid
HAVING
    MAX(wlevel) < 7 -- doesn't force motorway or trunk roundabout as local trafic may pass through
"""

sql16i = """
CREATE INDEX idx_roundabout_ways_wlevel2_rid ON roundabout_ways_wlevel2(rid)
"""

sql17 = """
SELECT
    roundabout.id,
    ST_AsText(way_locate(roundabout.linestring)),
    roundabout.level
FROM
    roundabout
    LEFT JOIN roundabout_ways_wlevel1 ON
        roundabout.id = roundabout_ways_wlevel1.rid
    LEFT JOIN roundabout_ways_wlevel2 ON
        roundabout.id = roundabout_ways_wlevel2.rid
WHERE
    roundabout.level NOT IN (wlevel1, wlevel2)
"""

sql20 = """
DROP TABLE IF EXISTS roundabout_acces;
CREATE TEMP TABLE roundabout_acces AS
SELECT
    roundabout.id AS ra_id,
    ways.id AS a_id,
    CASE
        WHEN ways.nodes[1] = ANY (roundabout.nodes) THEN ARRAY[ways.nodes[2], ways.nodes[3], ways.nodes[4]]
        WHEN ways.nodes[array_length(ways.nodes,1)] = ANY (roundabout.nodes) THEN ARRAY[ways.nodes[array_length(ways.nodes,1)], ways.nodes[array_length(ways.nodes,1)-1], ways.nodes[array_length(ways.nodes,1)-2]]
    END AS n_ids,
    (ways.tags?'oneway' AND ways.tags->'oneway' IN ('yes', 'true', '-1', '1')) AS oneway
FROM
    roundabout
    JOIN ways ON
        roundabout.linestring && ways.linestring AND
        (ways.nodes[1] = ANY (roundabout.nodes) OR ways.nodes[array_length(ways.nodes,1)] = ANY (roundabout.nodes)) AND
        roundabout.id != ways.id
WHERE
    ways.tags != ''::hstore AND
    ways.tags?'highway' AND
    ways.tags->'highway' IN ('primary', 'secondary', 'tertiary', 'unclassified', 'residential', 'road')
"""

sql21 = """
CREATE INDEX roundabout_acces_idx ON roundabout_acces(ra_id)
"""

sql22 = """
SELECT
    ra1.a_id,
    COALESCE(ra1.n_ids[2], ra1.n_ids[1])
FROM
    roundabout_acces AS ra1
    JOIN roundabout_acces AS ra2 ON
        ra1.ra_id = ra2.ra_id AND
        ra1.a_id != ra2.a_id
WHERE
    ra1.n_ids && ra2.n_ids AND
    NOT ra1.oneway
GROUP BY
    ra1.a_id,
    COALESCE(ra1.n_ids[2], ra1.n_ids[1])
"""

sql30 = """
CREATE TEMP TABLE access AS
SELECT
    roundabout.id AS rid,
    ways.id AS wid,
    (SELECT array_agg(e) FROM (SELECT unnest(roundabout.nodes) INTERSECT SELECT ends(ways.nodes)) AS dt(e)) AS nodes
FROM
    roundabout
    JOIN ways ON
      ways.tags != ''::hstore AND
      ways.tags?'highway' AND
      ways.tags->'highway' IN ('trunk', 'trunk_link', 'primary', 'primary_link', 'secondary', 'secondary_link', 'tertiary', 'tertiary_link', 'residential', 'unclassified', 'road') AND
      ways.linestring && roundabout.linestring AND
      ways.nodes && roundabout.nodes AND
      ways.id != roundabout.id
"""

sql31 = """
SELECT
    roundabout.id,
    ST_AsText(way_locate(roundabout.linestring))
FROM (
    SELECT
        rid AS id
    FROM
        access
    GROUP BY
        rid,
        nodes
    HAVING
        COUNT(*) > 1
) AS t
    NATURAL JOIN roundabout
"""

sql40 = """
SELECT
    roundabout.id,
    ways.id,
    ST_AsText(way_locate(ways.linestring))
FROM
    roundabout
    JOIN ways ON
        roundabout.id != ways.id AND
        roundabout.linestring && ways.linestring AND
        roundabout.nodes && ways.nodes[2:array_length(ways.nodes,1)-1]
WHERE
    ways.tags != ''::hstore AND
    ways.tags?'highway' AND
    ways.tags->'highway' NOT IN ('footway') AND
    ways.tags->'access' NOT IN ('no', 'psv', 'private') AND
    NOT ways.tags?'area'
"""

class Analyser_Osmosis_Roundabout_Level(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs[1] = {"item":"3010", "level": 2, "tag": ["highway", "roundabout", "fix:chair"], "desc": T_(u"Wrong highway on roundabout") }
        self.classs[2] = {"item":"2030", "level": 2, "tag": ["highway", "roundabout", "fix:chair"], "desc": T_(u"Missing oneway") }
        self.classs[3] = {"item":"3010", "level": 2, "tag": ["highway", "roundabout", "fix:imagery"], "desc": T_(u"Roundabout shortcut") }
        self.classs[4] = {"item":"3010", "level": 2, "tag": ["highway", "roundabout", "fix:chair"], "desc": T_(u"Roundabout crossing") }

    def analyser_osmosis_common(self):
        self.run(sql10)
        self.run(sql11)
        self.run(sql12)
        self.run(sql13)
        self.run(sql14)
        self.run(sql15)
        self.run(sql15i)
        self.run(sql16)
        self.run(sql16i)
        self.run(sql17, lambda res: {"class":1, "subclass":res[2], "data":[self.way_full, self.positionAsText]} )
        self.run(sql20)
        self.run(sql21)
        self.run(sql22, lambda res: {"class":2, "data":[self.way_full, self.node_position]} )
        self.run(sql30)
        self.run(sql31, lambda res: {"class":3, "data":[self.way_full, self.positionAsText]} )
        self.run(sql40, lambda res: {"class":4, "data":[self.way_full, self.way_full, self.positionAsText]} )
