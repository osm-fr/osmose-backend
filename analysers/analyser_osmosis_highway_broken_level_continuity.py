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

sql13 = """
CREATE TEMP VIEW orphan_endin AS
SELECT
    network.id,
    network.nid,
    network.level,
    CASE network.level
        WHEN 1 THEN (ways.highway IN ('construction', 'motorway', 'motorway_link', 'trunk', 'trunk_link', 'primary', 'primary_link'))
        WHEN 2 THEN (ways.highway IN ('construction', 'motorway', 'motorway_link', 'trunk', 'trunk_link', 'primary', 'primary_link', 'secondary', 'secondary_link'))
        WHEN 3 THEN (ways.highway IN ('construction', 'motorway', 'motorway_link', 'trunk', 'trunk_link', 'primary', 'primary_link', 'secondary', 'secondary_link', 'tertiary', 'tertiary_link'))
    END AS endin
FROM
    highway_ends AS network
    JOIN way_nodes ON
        way_nodes.node_id = network.nid AND
        way_nodes.way_id != network.id
    JOIN highways AS ways ON
        ways.id = way_nodes.way_id
WHERE
    network.nodes[1] != network.nodes[array_length(network.nodes,1)] AND
    network.highway IN ('primary', 'secondary', 'tertiary')
GROUP BY
    1,
    2,
    3,
    4
"""

sql14 = """
CREATE TEMP VIEW orphan0 AS
SELECT
    id,
    nid,
    level
FROM
    orphan_endin
GROUP BY
    id,
    nid,
    level
HAVING
    NOT BOOL_OR(orphan_endin.endin)
"""

sql15 = """
CREATE TEMP TABLE orphan1 AS
SELECT
    orphan0.*,
    geom
FROM
    orphan0
    JOIN nodes ON
        orphan0.nid = nodes.id
"""

sql16 = """
CREATE INDEX orphan1_level_idx ON orphan1(level)
"""

sql17 = """
CREATE INDEX orphan1_geom_idx ON orphan1 USING gist(geom)
"""

sql18 = """
SELECT
    o1.id,
    ST_AsText(o1.geom),
    o1.level
FROM
    orphan1 AS o1,
    orphan1 AS o2
WHERE
    o1.nid != o2.nid AND
    o1.level = o2.level AND
    ST_Distance_Sphere(o1.geom, o2.geom) < 1000
GROUP BY
    o1.id,
    o1.level,
    o1.geom
"""

class Analyser_Osmosis_Highway_Broken_Level_Continuity(Analyser_Osmosis):

    requires_tables_common = ['highways', 'highway_ends']

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs[1] = {"item":"1120", "level": 1, "tag": ["highway", "fix:chair"], "desc": T_(u"Broken highway level continuity") }
        self.classs[2] = {"item":"1120", "level": 2, "tag": ["highway", "fix:chair"], "desc": T_(u"Broken highway level continuity") }
        self.classs[3] = {"item":"1120", "level": 2, "tag": ["highway", "fix:chair"], "desc": T_(u"Broken highway level continuity") }

    def analyser_osmosis_common(self):
        self.run(sql13)
        self.run(sql14)
        self.run(sql15)
        self.run(sql16)
        self.run(sql17)
        self.run(sql18, lambda res: {"class":res[2], "data":[self.way_full, self.positionAsText]} )
