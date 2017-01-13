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
CREATE TEMP TABLE highway_level AS
SELECT
    id,
    nodes,
    ends(nodes) AS nid,
    tags?'junction' AS junction,
    CASE tags->'highway'
        WHEN 'motorway' THEN 1
        WHEN 'primary' THEN 1
        WHEN 'trunk' THEN 1
        WHEN 'motorway_link' THEN 2
        WHEN 'primary_link' THEN 2
        WHEN 'trunk_link' THEN 2
        WHEN 'secondary' THEN 2
        WHEN 'secondary_link' THEN 2
        WHEN 'tertiary' THEN 3
        WHEN 'tertiary_link' THEN 3
        WHEN 'unclassified' THEN 4
        WHEN 'unclassified_link' THEN 4
        WHEN 'residential' THEN 4
        WHEN 'residential_link' THEN 4
        ELSE 5
    END AS level
FROM
    ways
WHERE
    tags != ''::hstore AND
    tags?'highway'
"""

sql20 = """
CREATE INDEX idx_highway_level_id ON highway_level(id)
"""

sql40 = """
SELECT
    t.id,
    ST_AsText(nodes.geom),
    level
FROM
    (
    SELECT
        way_ends.id,
        way_ends.nid,
        way_ends.level
    FROM
        highway_level AS way_ends
        JOIN way_nodes ON
            way_ends.nid = way_nodes.node_id AND
            way_nodes.way_id != way_ends.id
        JOIN highway_level ON
            highway_level.id = way_nodes.way_id
    WHERE
        NOT way_ends.junction AND
        way_ends.level <= 3
    GROUP BY
        way_ends.id,
        way_ends.nid,
        way_ends.level
    HAVING
        BOOL_AND(way_ends.level + 1 < highway_level.level)
    ) AS t
    JOIN nodes ON
        nodes.id = nid
"""

class Analyser_Osmosis_Highway_CulDeSac_Level(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs[1] = {"item":"1090", "level": 1, "tag": ["highway", "fix:chair"], "desc": T_(u"Bad topology way level 1") }
        self.classs[2] = {"item":"1090", "level": 2, "tag": ["highway", "fix:chair"], "desc": T_(u"Bad topology way level 2") }
        self.classs[3] = {"item":"1090", "level": 2, "tag": ["highway", "fix:chair"], "desc": T_(u"Bad topology way level 3") }

    def analyser_osmosis(self):
        self.run(sql10)
        self.run(sql20)
        self.run(sql40, lambda res: {"class":res[2], "data":[self.way, self.positionAsText]} )
