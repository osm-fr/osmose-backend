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
CREATE OR REPLACE FUNCTION ends(nodes bigint[]) RETURNS SETOF bigint AS $$
DECLARE BEGIN
    RETURN NEXT nodes[1];
    RETURN NEXT nodes[array_length(nodes,1)];
    RETURN;
END
$$ LANGUAGE plpgsql;

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
    endin_level(w1.tags->'highway', network.level) AS endin
FROM
    network
    JOIN way_nodes AS wn1 ON
        network.nid = wn1.node_id AND
        network.id != wn1.way_id
    JOIN ways AS w1 ON
        wn1.way_id = w1.id AND
        w1.tags?'highway'
GROUP BY
    network.id,
    network.nid,
    network.level,
    endin_level(w1.tags->'highway', network.level)
;

CREATE TEMP TABLE orphan AS
SELECT
    oai1.*
FROM
    orphan_endin AS oai1
    LEFT JOIN orphan_endin AS oai2 ON
        oai1.id = oai2.id AND
        oai1.nid = oai2.nid AND
        oai1.level = oai2.level AND
        oai2.endin = true
WHERE
    oai1.endin = false AND
    oai2.id IS NULL
;

CREATE INDEX orphan_level_idx ON orphan(level);

"""

sql11 = """
SELECT
    o1.id,
    ST_AsText(n1.geom),
    o1.level
FROM
    orphan AS o1
    JOIN nodes AS n1 ON
        o1.nid = n1.id,
    orphan AS o2
    JOIN nodes AS n2 ON
        o2.nid = n2.id
WHERE
    o1.nid != o2.nid AND
    o1.level = o2.level AND
    ST_DWithin(n1.geom, n2.geom, 1e-2)
GROUP BY
    o1.id,
    o1.level,
    n1.geom
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
        self.run(sql11, lambda res: {"class":res[2], "data":[self.way_full, self.positionAsText]} )
