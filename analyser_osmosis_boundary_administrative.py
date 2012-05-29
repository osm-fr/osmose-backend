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
DROP TABLE commune CASCADE;
CREATE TABLE commune AS
SELECT
    relations.id AS id,
    relations.tags->'ref:INSEE' AS ref_insee,
    ST_Polygonize(ways.linestring) AS polygon
FROM
    relations
    JOIN relation_members ON
        relation_members.relation_id = relations.id AND
        relation_members.member_type = 'W'
    JOIN ways ON
        ways.id = relation_members.member_id AND
        ST_NPoints(ways.linestring) > 1
WHERE
    relations.tags?'type' AND
    relations.tags->'type' = 'boundary' AND
    relations.tags?'boundary' AND
    relations.tags->'boundary' = 'administrative' AND
    relations.tags?'admin_level' AND
    relations.tags->'admin_level' = '8'
GROUP BY
    relations.id,
    relations.tags->'ref:INSEE'
;
"""

sql11 = """
CREATE INDEX commune_polygon_idx ON commune USING gist(polygon);
CREATE INDEX commune_ref_insee_idx ON commune(ref_insee);
"""

sql12 = """
DROP VIEW commune_dump CASCADE;
CREATE VIEW commune_dump AS
SELECT
    id,
    ref_insee,
    (ST_Dump(polygon)).geom AS polygon
FROM
    commune
;
"""

sql20 = """
SELECT
    MIN(nodes.id) AS nid,
    commune.id AS rid,
    ST_AsText(nodes.geom)
FROM
    nodes
    JOIN commune_dump AS commune ON
        substring(nodes.tags->'ref', 1, 5) = commune.ref_insee
WHERE
    nodes.tags?'man_made' AND
    nodes.tags->'man_made' = 'survey_point' AND
    nodes.tags?'ref' AND
    length(nodes.tags->'ref') >= 5
GROUP BY
    commune.id,
    commune.polygon,
    nodes.geom
HAVING
    NOT ST_Within(nodes.geom, commune.polygon)
;
"""

sql30 = """
SELECT
    nodes.id AS nid,
    commune.id AS rid,
    ST_AsText(nodes.geom)
FROM
    nodes
    JOIN commune ON
        nodes.tags->'place' = commune.ref_insee AND
        ST_Within(nodes.geom, commune.polygon)
WHERE
    nodes.tags?'place' AND
    nodes.tags?'ref:INSEE'
;
"""

class Analyser_Osmosis_Boundary_Administrative(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs[100] = {"item":"6070", "desc":{"fr":"Repère géodésique hors de sa commune"} }
        self.classs[101] = {"item":"6070", "desc":{"fr":"Nœud place hors de sa commune"} }
        self.callback20 = lambda res: {"class":100, "data":[self.node_full, self.relation_full, self.positionAsText]}
        self.callback30 = lambda res: {"class":101, "data":[self.node_full, self.relation_full, self.positionAsText]}

    def analyser_osmosis_all(self):
        self.run(sql10)
        self.run(sql11)
        self.run(sql12)
        self.run(sql20, self.callback20)
        self.run(sql30, self.callback30)
