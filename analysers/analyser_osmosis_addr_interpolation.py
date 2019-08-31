#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2019                                      ##
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

sql00 = """
CREATE TEMP TABLE interpolations AS
SELECT
    *
FROM
    ways
WHERE
    tags != ''::hstore AND
    tags?'addr:interpolation'
"""

sql01 = """
CREATE INDEX idx_interpolations_geom ON interpolations USING gist(linestring)
"""

sql02 = """
CREATE TEMP TABLE interpolation_nodes AS
SELECT
    array_agg(interpolations.id) AS w_ids,
    nodes.id,
    nodes.tags,
    nodes.geom
FROM
    interpolations
    JOIN nodes ON
        nodes.geom && interpolations.linestring AND
        nodes.id = ANY (interpolations.nodes) AND
        nodes.tags != ''::hstore AND
        nodes.tags - ARRAY['source'] != ''::hstore
GROUP BY
    nodes.id,
    nodes.tags,
    nodes.geom
"""

sql03 = """
CREATE INDEX idx_interpolation_nodes_addr_housenumber ON interpolation_nodes((tags?'addr:housenumber')) WHERE tags?'addr:housenumber'
"""

sql04 = """
CREATE INDEX idx_interpolation_nodes_geom ON interpolation_nodes USING gist(geom)
"""

sql10 = """
SELECT
    id,
    St_AsText(geom)
FROM
    interpolation_nodes
WHERE
    NOT tags?'addr:housenumber'
"""

sql20 = """
SELECT
    id,
    St_AsText(geom)
FROM
    interpolation_nodes
WHERE
    tags?'addr:housenumber' AND
    array_length(w_ids, 1) > 1
"""

sql30 = """
SELECT
    w1.id,
    w2.id,
    ST_AsText(ST_Centroid(ST_Intersection(w1.linestring, w2.linestring)))
FROM
    interpolations AS w1
    JOIN interpolations AS w2 ON
        w1.id > w2.id AND
        ST_Crosses(w1.linestring, w2.linestring)
"""

sql40 = """
SELECT DISTINCT ON (ways.id)
    ways.id,
    St_AsText(coalesce(nodes.geom, way_locate(ways.linestring)))
FROM
    interpolations AS ways
    LEFT JOIN interpolation_nodes AS nodes ON
        ways.linestring && nodes.geom AND
        ways.id = ANY (nodes.w_ids) AND
        (
            nodes.id = ways.nodes[1] OR
            nodes.id = ways.nodes[array_length(nodes,1)]
        )
WHERE
    nodes.id IS NULL OR
    NOT nodes.tags?'addr:housenumber'
ORDER BY
    ways.id
"""

sql50 = """
SELECT
    ways.id,
    ST_AsText(nodes_s.geom)
FROM
    interpolations AS ways
    JOIN interpolation_nodes AS nodes_s ON
        ways.id = ANY (nodes_s.w_ids) AND
        nodes_s.id = ways.nodes[1] AND
        nodes_s.tags?'addr:housenumber'
    JOIN interpolation_nodes AS nodes_e ON
        ways.id = ANY (nodes_e.w_ids) AND
        nodes_e.id = ways.nodes[array_length(nodes,1)] AND
        nodes_e.tags?'addr:housenumber'
WHERE
    nodes_s.tags->'addr:housenumber' = nodes_e.tags->'addr:housenumber'
"""

sql60 = """
SELECT
    w_id,
    ST_AsText(min(geom)),
    string_agg(DISTINCT tags->'addr:street', ', ')
FROM
    (SELECT *, unnest(w_ids) AS w_id FROM interpolation_nodes) AS nodes
WHERE
    tags != ''::hstore AND
    tags?'addr:street'
GROUP BY
    w_id
HAVING
    COUNT(DISTINCT tags->'addr:street') != 1
"""

sql70 = """
SELECT
    nodes.id,
    ST_AsText(nodes.geom),
    string_agg(DISTINCT relations.tags->'name', ', ')
FROM
    interpolation_nodes AS nodes
    JOIN relation_members ON
        relation_members.member_type = 'N' AND
        relation_members.member_id = nodes.id
    JOIN relations ON
        relations.id = relation_members.relation_id AND
        relations.tags->'type' = 'associatedStreet'
GROUP BY
    nodes.id,
    nodes.geom
HAVING
    COUNT(DISTINCT relations.id) != 1
"""

class Analyser_Osmosis_Addr_Interpolation(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs[100] = {"item":"2060", "level": 3, "tag": ["addr", "fix:chair"], "desc": T_(u"Interpolation on nodes without tag \"addr:housenumber\"") }
        self.classs[101] = {"item":"2060", "level": 3, "tag": ["addr", "fix:chair"], "desc": T_(u"\"addr:housenumber\" in multiple interpolations") }
        self.classs[102] = {"item":"2060", "level": 2, "tag": ["addr", "fix:chair"], "desc": T_(u"Interpolation intersection") }
        self.classs[103] = {"item":"2060", "level": 3, "tag": ["addr", "fix:chair"], "desc": T_(u"Interpolation ends should have tag \"addr:housenumber\"") }
        self.classs[104] = {"item":"2060", "level": 3, "tag": ["addr", "fix:chair"], "desc": T_(u"Interpolation ends should have have different tag \"addr:housenumber\" values") }
        self.classs[16] = {"item":"2060", "level": 2, "tag": ["addr", "fix:chair"], "desc": T_(u"Interpolation on nodes of multiple street names") }
        self.classs[17] = {"item":"2060", "level": 2, "tag": ["addr", "fix:chair"], "desc": T_(u"Interpolation on nodes of multiple \"associatedStreet\" relations") }
        self.callback10 = lambda res: {"class":100, "subclass":0, "data":[self.node_full, self.positionAsText] }
        self.callback20 = lambda res: {"class":101, "subclass":0, "data":[self.node_full, self.positionAsText] }
        self.callback30 = lambda res: {"class":102, "subclass":0, "data":[self.way_full, self.way_full, self.positionAsText] }
        self.callback40 = lambda res: {"class":103, "subclass":0, "data":[self.way_full, self.positionAsText] }
        self.callback50 = lambda res: {"class":104, "subclass":0, "data":[self.way_full, self.positionAsText] }
        self.callback60 = lambda res: {"class":16, "subclass":1, "data":[self.way_full, self.positionAsText], "text": T_(u"Interpolation span on streets: %s", res[2]) }
        self.callback70 = lambda res: {"class":17, "subclass":1, "data":[self.node_full, self.positionAsText], "text": T_(u"Interpolation span on streets: %s", res[2]) }

    def analyser_osmosis_common(self):
        self.run(sql00)
        self.run(sql01)
        self.run(sql02)
        self.run(sql03)
        self.run(sql04)
        self.run(sql10, self.callback10)
        self.run(sql20, self.callback20)
        self.run(sql30, self.callback30)
        self.run(sql40, self.callback40)
        self.run(sql50, self.callback50)
        self.run(sql60, self.callback60)
        self.run(sql70, self.callback70)
