#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
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

from Analyser_Osmosis import Analyser_Osmosis

sql10 = """
SELECT
    nodes.id,
    ST_AsText(nodes.geom)
FROM
    nodes
    LEFT JOIN way_nodes ON
        nodes.id = way_nodes.node_id
    LEFT JOIN ways ON
        way_nodes.way_id = ways.id AND
        ways.tags?'power' AND
        ways.tags->'power' IN ('line', 'minor_line', 'cable')
WHERE
    nodes.tags?'power' AND
    (nodes.tags->'power' = 'pole' OR nodes.tags->'power' = 'tower') AND
    ways.id IS NULL
;
"""

sql20 = """
DROP VIEW IF EXISTS line_ends CASCADE;
CREATE VIEW line_ends AS
SELECT
    ends(ways.nodes) AS id
FROM
    ways
WHERE
    ways.tags?'power' AND
    ways.tags->'power' IN ('line', 'minor_line', 'cable')
;

DROP VIEW IF EXISTS line_ends1 CASCADE;
CREATE VIEW line_ends1 AS
SELECT
    line_ends.id
FROM
    line_ends
    JOIN way_nodes ON
        way_nodes.node_id = line_ends.id
    JOIN ways ON
        way_nodes.way_id = ways.id AND
        ways.tags?'power' AND
        ways.tags->'power' IN ('line', 'minor_line', 'cable')
GROUP BY
    line_ends.id
HAVING
    COUNT(*) = 1
;

DROP VIEW IF EXISTS line_terminators CASCADE;
CREATE VIEW line_terminators AS
(
SELECT
    'N' as type,
    id,
    geom
FROM
    nodes
WHERE
    tags?'power' AND
    tags->'power' NOT IN ('pole', 'tower')
)
UNION
(
SELECT
    'W' as type,
    id,
    way_locate(linestring) AS geom
FROM
    ways
WHERE
    tags?'power' AND
    tags->'power' NOT IN ('line', 'minor_line', 'cable')
)
;

SELECT
    nodes.id,
    ST_AsText(nodes.geom)
FROM
    line_ends1
    JOIN nodes ON
        line_ends1.id = nodes.id AND
        NOT tags?'riser'
    LEFT JOIN line_terminators ON
        ST_Distance_Sphere(nodes.geom, line_terminators.geom) < 100
WHERE
    line_terminators.id IS NULL
;
"""

sql30 = """
CREATE TEMP TABLE power_line AS
SELECT
    id,
    ends(nodes) AS nid,
    voltage
FROM
(
SELECT
    id,
    nodes,
    regexp_split_to_table(tags->'voltage','; *') AS voltage
FROM
    ways
WHERE
    tags?'power' AND
    (tags->'power' = 'line' OR tags->'power' = 'minor_line') AND
    tags?'voltage'
) AS d
;

CREATE VIEW power_line_junction AS
SELECT
    nid
FROM
    (SELECT nid FROM power_line GROUP BY id, nid) AS p
GROUP BY
    nid
HAVING
    COUNT(*) > 1
;

SELECT
    DISTINCT(nid),
    ST_AsText(geom)
FROM
    power_line_junction
    NATURAL JOIN power_line
    JOIN nodes ON
        power_line.nid = nodes.id
GROUP BY
    nid,
    voltage,
    geom
HAVING
    COUNT(*) = 1
;
"""

sql40 = """
SELECT
    nodes.id,
    ST_AsText(nodes.geom)
FROM
    {0}ways AS ways
    JOIN way_nodes ON
        ways.id = way_nodes.way_id
    JOIN nodes ON
        way_nodes.node_id = nodes.id
WHERE
    nodes.id != ways.nodes[1] AND
    nodes.id != ways.nodes[array_length(nodes,1)] AND
    ways.tags?'power' AND
    ways.tags->'power' IN ('line', 'minor_line') AND
    (NOT ways.tags?'tunnel' OR NOT ways.tags->'tunnel' IN ('yes', 'true')) AND
    (NOT ways.tags?'submarine' OR NOT ways.tags->'submarine' IN ('yes', 'true')) AND
    not nodes.tags?'power'
;
"""

sql50 = """
CREATE TEMP TABLE power_segement AS
SELECT
    id,
    ST_MakeLine(p1, p2) AS seg,
    ST_Length(ST_MakeLine(p1, p2)::geography) AS l
FROM
    (
    SELECT
        ways.id,
        generate_series(1,ST_NPoints(linestring)-1) AS n,
        ST_PointN(linestring, generate_series(1,ST_NPoints(linestring)-1)) AS p1,
        ST_PointN(linestring, generate_series(2,ST_NPoints(linestring))) AS p2
    FROM
        {0}ways AS ways
    WHERE
        ways.tags?'power' AND
        ways.tags->'power' = 'line' AND
        (NOT ways.tags?'tunnel' OR NOT ways.tags->'tunnel' IN ('yes', 'true')) AND
        (NOT ways.tags?'submarine' OR NOT ways.tags->'submarine' IN ('yes', 'true')) AND
        array_length(nodes, 1) >= 30
    ) AS d
"""

sql51 = """
CREATE TEMP TABLE power_segement_stddev AS
SELECT
    id,
    stddev(l) AS ll,
    avg(l) AS a
FROM
    power_segement
WHERE
    l > 50 AND l < 800
GROUP BY
    id
HAVING
    stddev(l)/avg(l) < 0.25 AND
    COUNT(*) > 20
"""

sql52 = """
SELECT
    power_segement.id,
    ST_AsText(ST_Line_Interpolate_Point(
        power_segement.seg,
        generate_series(1, (power_segement.l / power_segement_stddev.a)::int-1)
            /round(power_segement.l / power_segement_stddev.a)
    ))
FROM
    power_segement
    JOIN power_segement_stddev ON
        power_segement.id = power_segement_stddev.id AND
        power_segement.l / power_segement_stddev.a > 1.8
WHERE
    power_segement.l / power_segement_stddev.a < 8
ORDER BY
    power_segement.id,
    power_segement.l / power_segement_stddev.a
"""

class Analyser_Osmosis_Powerline(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs[1] = {"item":"7040", "level": 3, "tag": ["power", "fix:imagery"], "desc":{"fr": u"Pylône ou poteau électrique isolé", "en": u"Power tower or pole alone", "es":u"Torre eléctrica o poste de energía aislada"} }
        self.classs[2] = {"item":"7040", "level": 2, "tag": ["power", "fix:imagery"], "desc":{"fr": u"Ligne électrique non terminée", "en": u"Power line non terminated", "es": u"Línea eléctrica no terminada"} }
        self.classs[3] = {"item":"7040", "level": 3, "tag": ["power", "fix:chair"], "desc":{"fr": u"Connexion entre différents voltages", "en": u"Connection between different voltages", "es": u"Conexión entre voltajes diferentes"} }
        self.classs_change[4] = {"item":"7040", "level": 3, "tag": ["power", "fix:imagery"], "desc":{"en": u"Non power node on power way", "es": u"Nodo no eléctrico en un camino eléctrico"} }
        self.classs_change[5] = {"item":"7040", "level": 3, "tag": ["power", "fix:imagery"], "desc":{"fr": u"Pylône ou poteau électrique manquant", "en": u"Missing power tower or pole", "es": u"Poste o torre eléctrico ausente"} }
        self.callback20 = lambda res: {"class":2, "data":[self.node_full, self.positionAsText]}
        self.callback40 = lambda res: {"class":4, "data":[self.node_full, self.positionAsText]}
        self.callback50 = lambda res: {"class":5, "data":[self.way_full, self.positionAsText]}

    def analyser_osmosis(self):
        self.run(sql10, lambda res: {"class":1, "data":[self.node_full, self.positionAsText]} )
        self.run(sql20, lambda res: {"class":2, "data":[self.node_full, self.positionAsText]} )
        self.run(sql30, lambda res: {"class":3, "data":[self.node_full, self.positionAsText], "fix":[{"+": {"power": "tower"}}, {"+": {"power": "pole"}}] } )

    def analyser_osmosis_all(self):
        self.run(sql40.format(""), self.callback40)
        self.run(sql50.format(""))
        self.run(sql51)
        self.run(sql52, self.callback50)

    def analyser_osmosis_touched(self):
        self.run(sql40.format("touched_"), self.callback40)
        self.run(sql50.format("touched_"))
        self.run(sql51)
        self.run(sql52, self.callback50)
