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
CREATE OR REPLACE FUNCTION level(highway varchar) RETURNS int AS $$
DECLARE BEGIN
    RETURN CASE
        WHEN highway = 'motorway' THEN 7
        WHEN highway = 'trunk' THEN 7
        WHEN highway = 'primary' THEN 6
        WHEN highway = 'secondary' THEN 5
        WHEN highway = 'tertiary' THEN 4
        WHEN highway = 'unclassified' THEN 3
        WHEN highway = 'residential' THEN 3
        WHEN highway = 'service' THEN 2
        WHEN highway = 'road' THEN 1
        ELSE 0
    END;
END
$$ LANGUAGE plpgsql;

DROP TABLE IF EXISTS roundabout CASCADE;
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
    tags?'junction' AND
    tags->'junction' = 'roundabout' AND
    tags?'highway' AND
    nodes[1] = nodes[array_length(nodes,1)] AND
    level(tags->'highway') > 0
;

CREATE INDEX roundabout_id_idx ON roundabout(id);
CREATE INDEX roundabout_linestring_idx ON roundabout USING gist(linestring);
"""

sql11 = """
SELECT
    roundabout.id,
    ST_AsText(way_locate(roundabout.linestring)),
    roundabout.level
FROM
    roundabout
    JOIN ways ON
        roundabout.id != ways.id
WHERE
    roundabout.linestring && ways.linestring AND
    roundabout.nodes && ways.nodes AND
    ways.tags?'highway'
GROUP BY
    roundabout.id,
    roundabout.level,
    roundabout.highway,
    roundabout.linestring
HAVING
    MAX(level(tags->'highway')) < 7 AND -- doesn't force motorway or trunk roundabout as local trafic may pass through
    MAX(level(tags->'highway')) != roundabout.level
;
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
    ways.tags?'highway' AND
    ways.tags->'highway' IN ('primary', 'secondary', 'tertiary', 'unclassified', 'residential', 'road')
;

CREATE INDEX roundabout_acces_idx ON roundabout_acces(ra_id);
"""

sql21 = """
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
;
"""

sql30 = """
SELECT
    junction.id AS junction_id,
    ST_AsText(way_locate(junction.linestring))
FROM
    ways AS junction
    JOIN ways AS w1 ON
        junction.linestring && w1.linestring AND
        w1.tags?'highway' AND
        w1.tags->'highway' IN ('trunk', 'trunk_link', 'primary', 'primary_link', 'secondary', 'secondary_link', 'tertiary', 'tertiary_link', 'residential', 'unclassified', 'road') AND
        w1.id != junction.id
    JOIN ways AS w2 ON
        junction.linestring && w2.linestring AND
        w2.tags?'highway' AND
        w2.tags->'highway' IN ('trunk', 'trunk_link', 'primary', 'primary_link', 'secondary', 'secondary_link', 'tertiary', 'tertiary_link', 'residential', 'unclassified', 'road') AND
        w2.id != junction.id
WHERE
    junction.tags->'highway' IN ('trunk', 'trunk_link', 'primary', 'primary_link', 'secondary', 'secondary_link', 'tertiary', 'tertiary_link', 'residential', 'unclassified', 'road') AND
    array_length(junction.nodes, 1) > 3 AND
    junction.nodes[1] = junction.nodes[array_length(junction.nodes, 1)] AND
    w1.id != w2.id AND
    junction.tags?'junction' AND
    junction.tags->'junction' = 'roundabout' AND
    w1.linestring && w2.linestring AND
    (select array_agg(e) from (SELECT unnest(junction.nodes) INTERSECT SELECT ends(w1.nodes)) AS dt(e)) =
    (select array_agg(e) from (SELECT unnest(junction.nodes) INTERSECT SELECT ends(w2.nodes)) AS dt(e))
;
"""


class Analyser_Osmosis_Roundabout_Level(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs[1] = {"item":"3010", "level": 2, "tag": ["highway", "roundabout"], "desc":{"fr": u"Mauvais highway sur roundabout", "en": u"Wrong highway on roundabout"} }
        self.classs[2] = {"item":"2030", "level": 2, "tag": ["highway", "roundabout"], "desc":{"fr": u"oneway manquant sur insertion rond-point", "en": u"Missing oneway"} }
        self.classs[3] = {"item":"3010", "level": 2, "tag": ["highway", "roundabout"], "desc":{"fr": u"Raccourci sur rond-point", "en": u"Roundabout shortcut"} }

    def analyser_osmosis(self):
        self.run(sql10)
        self.run(sql11, lambda res: {"class":1, "subclass":res[2], "data":[self.way_full, self.positionAsText]} )
        self.run(sql20)
        self.run(sql21, lambda res: {"class":2, "data":[self.way_full, self.node_position]} )
        self.run(sql30, lambda res: {"class":3, "data":[self.way_full, self.positionAsText]} )
