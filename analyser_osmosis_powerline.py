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
        ST_DWithin(nodes.geom, line_terminators.geom, 5e-3)
WHERE
    line_terminators.id IS NULL
;
"""

sql30 = """
DROP VIEW IF EXISTS power_line CASCADE;
CREATE VIEW power_line AS
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
;

DROP VIEW IF EXISTS power_line_junction CASCADE;
CREATE VIEW power_line_junction AS
SELECT
    nodes.id,
    nodes.geom
FROM
    (SELECT voltage, ends(nodes) AS id FROM power_line) AS v
    JOIN nodes ON
        v.id = nodes.id
GROUP BY
    nodes.id,
    nodes.geom
HAVING
    COUNT(*) > 1
;

SELECT
    DISTINCT(id),
    ST_AsText(geom)
FROM
    power_line_junction
    NATURAL JOIN (SELECT voltage, ends(nodes) AS id FROM power_line) AS v
GROUP BY
    id,
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
    not nodes.tags?'power'
;
"""

class Analyser_Osmosis_Powerline(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs[1] = {"item":"7040", "level": 3, "tag": ["power"], "desc":{"fr":"Pylône ou poteau électrique isolé", "en":"Power tower or pole alone"} }
        self.classs[2] = {"item":"7040", "level": 2, "tag": ["power"], "desc":{"fr":"Ligne électrique non terminée", "en":"Power line non terminated"} }
        self.classs[3] = {"item":"7040", "level": 3, "tag": ["power"], "desc":{"fr":"Connexion entre différents voltages", "en":"Connection between different voltages"} }
        self.classs_change[4] = {"item":"7040", "level": 3, "tag": ["power"], "desc":{"en":"Non power node on power way"} }
        self.callback40 = lambda res: {"class":4, "data":[self.node_full, self.positionAsText]}

    def analyser_osmosis(self):
        self.run(sql10, lambda res: {"class":1, "data":[self.node_full, self.positionAsText]} )
        self.run(sql20, lambda res: {"class":2, "data":[self.node_full, self.positionAsText]} )
        self.run(sql30, lambda res: {"class":3, "data":[self.node_full, self.positionAsText], "fix":[{"+": {"power": "tower"}}, {"+": {"power": "pole"}}] } )

    def analyser_osmosis_all(self):
        self.run(sql40.format(""), self.callback40)

    def analyser_osmosis_touched(self):
        self.run(sql40.format("touched_"), self.callback40)
