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

from .Analyser_Osmosis import Analyser_Osmosis

sql10 = """
CREATE FUNCTION level(highway varchar) RETURNS int AS $$
DECLARE BEGIN
    RETURN CASE
        WHEN highway = 'motorway' THEN 1
        WHEN highway = 'motorway_link' THEN 1
        WHEN highway = 'trunk' THEN 1
        WHEN highway = 'trunk_link' THEN 1
        WHEN highway = 'primary' THEN 2
        WHEN highway = 'primary_link' THEN 2
        WHEN highway = 'secondary' THEN 3
        WHEN highway = 'secondary_link' THEN 3
        WHEN highway = 'tertiary' THEN 4
        WHEN highway = 'tertiary_link' THEN 4
        WHEN highway = 'unclassified' THEN 5
        WHEN highway = 'residential' THEN 5
        WHEN highway = 'service' THEN 6
        WHEN highway = 'road' THEN 7
        ELSE NULL
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
    level(highway) AS level,
    highway,
    linestring,
    nodes
FROM
    highways
WHERE
    is_roundabout AND
    NOT is_area AND
    NOT is_construction AND
    array_length(nodes, 1) > 3 AND
    nodes[1] = nodes[array_length(nodes,1)] AND
    level(highway) IS NOT NULL
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
    level(ways.highway) AS wlevel
FROM
    roundabout
    JOIN highways AS ways ON
        roundabout.linestring && ways.linestring AND
        roundabout.nodes && ways.nodes AND
        roundabout.id != ways.id AND
        NOT ways.is_construction
"""

sql15 = """
CREATE TEMP TABLE roundabout_ways_wlevel1 AS
SELECT
    rid,
    MIN(wlevel) AS wlevel1
FROM
    roundabout_ways
GROUP BY
    rid
HAVING
    MIN(wlevel) > 1 -- doesn't force motorway or trunk roundabout as local trafic may pass through
"""

sql15i = """
CREATE INDEX idx_roundabout_ways_wlevel1_rid ON roundabout_ways_wlevel1(rid)
"""

sql16 = """
CREATE TEMP TABLE roundabout_ways_wlevel2 AS
SELECT
    rid,
    MIN(wlevel) AS wlevel2
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
    MIN(wlevel) > 1 -- doesn't force motorway or trunk roundabout as local trafic may pass through
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
CREATE TEMP TABLE roundabout_access AS
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
    JOIN highways AS ways ON
        roundabout.linestring && ways.linestring AND
        (ways.nodes[1] = ANY (roundabout.nodes) OR ways.nodes[array_length(ways.nodes,1)] = ANY (roundabout.nodes)) AND
        roundabout.id != ways.id AND
        NOT ways.is_construction
WHERE
    ways.highway IN ('primary', 'secondary', 'tertiary', 'unclassified', 'residential', 'road')
"""

sql21 = """
CREATE INDEX roundabout_access_idx ON roundabout_access(ra_id)
"""

sql22 = """
SELECT
    ra1.a_id,
    COALESCE(ra1.n_ids[2], ra1.n_ids[1]),
    COALESCE(ra1.n_ids[2], ra1.n_ids[1])
FROM
    roundabout_access AS ra1
    JOIN roundabout_access AS ra2 ON
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
    JOIN highways AS ways ON
      ways.highway IN ('trunk', 'trunk_link', 'primary', 'primary_link', 'secondary', 'secondary_link', 'tertiary', 'tertiary_link', 'residential', 'unclassified', 'road') AND
      ways.linestring && roundabout.linestring AND
      ways.nodes && roundabout.nodes AND
      ways.id != roundabout.id AND
      NOT ways.is_construction
"""

sql31 = """
SELECT
    roundabout.id,
    ST_AsText(way_locate(roundabout.linestring))
FROM (
    SELECT DISTINCT ON (id)
        id
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
    JOIN highways AS ways ON
        roundabout.id != ways.id AND
        roundabout.linestring && ways.linestring AND
        roundabout.nodes && ways.nodes[2:array_length(ways.nodes,1)-1]
WHERE
    NOT ways.is_construction AND
    ways.highway NOT IN ('footway') AND
    ways.tags->'access' NOT IN ('no', 'psv', 'private') AND
    NOT is_area
"""

class Analyser_Osmosis_Roundabout_Level(Analyser_Osmosis):

    requires_tables_common = ['highways']

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs[1] = self.def_class(item = 3010, level = 2, tags = ['highway', 'roundabout', 'fix:chair'],
            title = T_('Wrong highway on roundabout'),
            detail = T_(
'''It must match the highest level of connected routes, except `motorway`
and `trunk`.'''),
            fix = T_(
'''Adjust the tag `highway=*` of the roundabout.'''),
            example = T_(
'''![](https://wiki.openstreetmap.org/w/images/3/3a/Osmose-eg-error-3010.png)

Highway level should be secondary.'''))
        self.classs[2] = self.def_class(item = 2030, level = 2, tags = ['highway', 'roundabout', 'fix:chair'],
            title = T_('Missing oneway'),
            detail = T_(
'''Short ways are connected to roundabout and join together. It is often
a sign of roundabout insertion way. These segments are often
one-way.'''),
            fix = T_(
'''After verifying that it is an access roads to the roundabout and they
were well oriented, set the tag `oneway=yes` on the two segments.'''),
            trap = T_(
'''* If a way is prolonged after joining the second segment, cut the way
before putting the tag oneway.
* Two roundabout close can be connected by a small lane in both
directions.'''))

        self.classs[3] = self.def_class(item = 3010, level = 2, tags = ['highway', 'roundabout', 'fix:imagery'],
            title = T_('Roundabout shortcut'),
            detail = T_(
'''Several roads connect to one node of the roundabout. In this case
input and output flow of vehicles bypassing the priority rules of
traffic.'''),
            fix = T_(
'''Separate the junction nodes into several separate ones .'''))
        self.classs[4] = self.def_class(item = 3010, level = 2, tags = ['highway', 'roundabout', 'fix:chair'],
            title = T_('Roundabout crossing'),
            detail = T_(
'''Way through the roundabout without stopping.'''),
            fix = T_(
'''Check if it is really a roundabout and cut the way.'''))

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
        self.run(sql22, lambda res: {"class":2, "data":[self.way_full, self.node, self.node_position]} )
        self.run(sql30)
        self.run(sql31, lambda res: {"class":3, "data":[self.way_full, self.positionAsText]} )
        self.run(sql40, lambda res: {"class":4, "data":[self.way_full, self.way_full, self.positionAsText]} )
