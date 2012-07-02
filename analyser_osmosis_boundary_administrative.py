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
DROP TABLE IF EXISTS commune CASCADE;
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
DROP TABLE IF EXISTS commune_dump CASCADE;
CREATE TABLE commune_dump AS
SELECT
    id,
    ref_insee,
    (ST_Dump(polygon)).geom AS polygon
FROM
    commune
;
"""

sql12 = """
CREATE INDEX commune_dump_polygon_idx ON commune_dump USING gist(polygon);
CREATE INDEX commune_dump_ref_insee_idx ON commune_dump(ref_insee);
"""

sql20 = """
DROP TABLE IF EXISTS geodesic_hull CASCADE;
CREATE TABLE geodesic_hull AS
SELECT
    relations.id,
    ST_ConvexHull(ST_Collect(nodes.geom)) AS hull,
    substring(relations.tags->'ref', 1, 5) AS ref_insee
FROM
    relations
    JOIN relation_members ON
        relation_members.relation_id = relations.id AND
        relation_members.member_type = 'N'
    JOIN nodes ON
        nodes.id = relation_members.member_id
WHERE
    relations.tags?'type' AND
    relations.tags->'type' = 'site' AND
    relations.tags?'site' AND
    relations.tags->'site' = 'geodesic' AND
    relations.tags?'ref' AND
    length(relations.tags->'ref') >= 5
GROUP BY
    relations.id,
    substring(relations.tags->'ref', 1, 5)
;
"""

sql21 = """
CREATE INDEX geodesic_hull_ref_insee ON geodesic_hull(ref_insee);
"""

sql22 = """
SELECT
    geodesic_hull.id,
    commune.id,
    ST_AsText(ST_Centroid(geodesic_hull.hull))
FROM
    geodesic_hull
    JOIN commune_dump AS commune ON
        geodesic_hull.ref_insee = commune.ref_insee
GROUP BY
    commune.id,
    geodesic_hull.hull,
    geodesic_hull.id
HAVING
    NOT BOOL_OR(ST_Intersects(geodesic_hull.hull, commune.polygon))
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

sql40 = """
SELECT
    c1.id,
    c2.id,
    ST_AsText(ST_Centroid(ST_Intersection(c1.polygon, c2.polygon)))
FROM
    commune_dump AS c1
    JOIN commune_dump AS c2 ON
        c1.polygon && c2.polygon AND
        ST_Overlaps(c1.polygon, c2.polygon)
;
"""

class Analyser_Osmosis_Boundary_Administrative(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs[100] = {"item":"6070", "level": 2, "tag": ["boundary", "geom"], "desc":{"fr":"Repère géodésique hors de sa commune"} }
        self.classs[101] = {"item":"6070", "level": 1, "tag": ["boundary", "place"], "desc":{"fr":"Nœud place hors de sa commune"} }
        self.classs[2] = {"item":"6060", "level": 1, "tag": ["boundary", "geom"], "desc":{"fr":"Intersection entre commune"} }
        self.callback20 = lambda res: {"class":100, "data":[self.relation_full, self.relation_full, self.positionAsText]}
        self.callback30 = lambda res: {"class":101, "data":[self.node_full, self.relation_full, self.positionAsText]}
        self.callback40 = lambda res: {"class":2, "data":[self.relation_full, self.relation_full, self.positionAsText]}

    def analyser_osmosis_all(self):
        self.run(sql10)
        self.run(sql11)
        self.run(sql12)
        self.run(sql20)
        self.run(sql21)
        self.run(sql22, self.callback20)
        self.run(sql30, self.callback30)
        self.run(sql40, self.callback40)
