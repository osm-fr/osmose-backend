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
DROP VIEW IF EXISTS network CASCADE;
CREATE VIEW network AS
SELECT
    ways.id,
    ends(ways.nodes) AS nid,
    CASE tags->'highway'
        WHEN 'primary' THEN 1
        WHEN 'secondary' THEN 2
        WHEN 'tertiary' THEN 3
    END AS level
FROM
   ways
WHERE
   nodes[1] != nodes[array_length(nodes,1)] AND
   ways.tags?'highway' AND
   ways.tags->'highway' IN ('primary', 'secondary', 'tertiary')
;

CREATE OR REPLACE FUNCTION endin_level(highway varchar, level integer) RETURNS boolean AS $$
DECLARE BEGIN
    RETURN CASE level
        WHEN 1 THEN (highway IN ('motorway', 'motorway_link', 'trunk', 'trunk_link', 'primary', 'primary_link'))
        WHEN 2 THEN (highway IN ('motorway', 'motorway_link', 'trunk', 'trunk_link', 'primary', 'primary_link', 'secondary', 'secondary_link'))
        WHEN 3 THEN (highway IN ('motorway', 'motorway_link', 'trunk', 'trunk_link', 'primary', 'primary_link', 'secondary', 'secondary_link', 'tertiary', 'tertiary_link'))
    END;
END
$$ LANGUAGE plpgsql;

DROP VIEW IF EXISTS orphan_endin CASCADE;
CREATE VIEW orphan_endin AS
SELECT
    network.id,
    network.nid,
    network.level,
    endin_level(ways.tags->'highway', network.level) AS endin
FROM
    network
    JOIN way_nodes ON
        network.nid = way_nodes.node_id AND
        network.id != way_nodes.way_id
    JOIN ways ON
        way_nodes.way_id = ways.id AND
        ways.tags?'highway'
GROUP BY
    network.id,
    network.nid,
    network.level,
    endin_level(ways.tags->'highway', network.level)
;

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
;
"""

sql11 = """
CREATE TEMP TABLE orphan1 AS
SELECT
    orphan0.*,
    geom
FROM
    orphan0
    JOIN nodes ON
        orphan0.nid = nodes.id
;
"""

sql12 = """
CREATE INDEX orphan1_level_idx ON orphan1(level);
CREATE INDEX orphan1_geom_idx ON orphan1 USING gist(geom);
"""

sql13 = """
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
    ST_DWithin(o1.geom, o2.geom, 1e-2)
GROUP BY
    o1.id,
    o1.level,
    o1.geom
;
"""

class Analyser_Osmosis_Broken_Highway_Level_Continuity(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs[1] = {"item":"1120", "desc":{"fr":"Continuité rompue du niveau de voie", "en":"Broken highway level continuity"} }
        self.classs[2] = {"item":"1120", "desc":{"fr":"Continuité rompue du niveau de voie", "en":"Broken highway level continuity"} }
        self.classs[3] = {"item":"1120", "desc":{"fr":"Continuité rompue du niveau de voie", "en":"Broken highway level continuity"} }

    def analyser_osmosis(self):
        self.run(sql10)
        self.run(sql11)
        self.run(sql12)
        self.run(sql13, lambda res: {"class":res[2], "data":[self.way_full, self.positionAsText]} )
