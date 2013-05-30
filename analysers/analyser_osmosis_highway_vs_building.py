#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Etienne Chové <chove@crans.org> 2010                       ##
##            Frédéric Rodrigo <****@free.fr> 2011                       ##
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
    buildings.id,
    highways.id,
    ST_AsText(way_locate(buildings.linestring))
FROM
    {0}ways AS buildings,
    {1}ways AS highways
WHERE
    ((
        highways.tags ? 'highway' AND
        highways.tags->'highway' IN ('motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'residential', 'unclassified')
    ) OR (
        highways.tags ? 'railway' AND
        highways.tags->'railway' IN ('rail', 'tram')
    )) AND
    NOT highways.tags ? 'tunnel' AND
    NOT highways.tags ? 'bridge' AND
    NOT highways.tags ? 'covered' AND
    NOT highways.tags ? 'area' AND
    buildings.tags->'building' = 'yes' AND
    NOT buildings.tags ? 'wall' AND
    ST_NPoints(buildings.linestring) > 1 AND
    ST_NPoints(highways.linestring) > 1 AND
    ST_Crosses(buildings.linestring, highways.linestring)
"""

sql20 = """
SELECT
    tree.id,
    building.id,
    ST_AsText(tree.geom)
FROM
    nodes AS tree
    JOIN ways AS building ON
        tree.geom && building.linestring AND
        ST_NPoints(building.linestring) > 2 AND
        ST_Intersects(tree.geom, ST_MakePolygon(building.linestring))
    LEFT JOIN relation_members ON
        relation_members.member_type = 'W' AND
        relation_members.member_id = building.id
WHERE
    relation_members.member_id IS NULL AND
    tree.tags?'natural' AND
    tree.tags->'natural' = 'tree' AND
    building.tags?'building' AND
    building.tags->'building' != 'no' AND
    NOT building.tags ? 'wall' AND
    building.is_polygon
"""

sql30 = """
SELECT
    tree.id,
    highway.id,
    ST_AsText(tree.geom)
FROM
    nodes AS tree
    JOIN ways AS highway ON
        tree.geom && highway.linestring AND
        ST_NPoints(highway.linestring) > 1 AND
        ST_Intersects(ST_Buffer(tree.geom::geography, 0.25)::geometry, highway.linestring)
WHERE
    tree.tags?'natural' AND
    tree.tags->'natural' = 'tree' AND
    highway.tags?'highway' AND
    highway.tags->'highway' IN (
        'motorway', 'motorway_link',
        'trunk', 'trunk_link',
        'primary', 'primary_link',
        'secondary', 'secondary_link',
        'tertiary', 'tertiary_link',
        'unclassified', 'residential', 'living_street') AND
    NOT highway.tags?'layer'
"""

sql40 = """
SELECT
    highways.id,
    water.id,
    ST_AsText(ST_Centroid(ST_Intersection(highways.linestring, water.linestring)))
FROM
    ways AS highways
    JOIN ways AS water ON
        highways.linestring && water.linestring AND
        ST_NPoints(highways.linestring) > 1 AND
        ST_NPoints(water.linestring) > 1 AND
        ST_Crosses(highways.linestring, water.linestring)
WHERE
    (highways.tags?'highway' OR highways.tags?'railway') AND
    NOT highways.tags?'tunnel' AND
    NOT highways.tags?'bridge' AND
    (
        (
            water.tags?'waterway' AND
            NOT water.tags?'tunnel' AND
            NOT water.tags?'bridge'
        ) OR (
            water.tags?'natural' AND
            water.tags->'natural' = 'water'
        )
    )
"""

class Analyser_Osmosis_Highway_VS_Building(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs_change[1] = {"item":"1070", "level": 2, "tag": ["highway", "building", "geom"], "desc":{"fr": u"Intersection entre une voie et un bâtiment", "en": u"Highway intersecting building"} }
        self.classs_change[2] = {"item":"1070", "level": 2, "tag": ["tree", "building", "geom"], "desc":{"fr": u"Intersection entre un arbre et un bâtiment", "en": u"Tree intersecting building"} }
        self.classs_change[3] = {"item":"1070", "level": 2, "tag": ["highway", "tree", "geom"], "desc":{"fr": u"Arbre très proche d'une voie", "en": u"Tree and highway too close"} }
        self.classs_change[4] = {"item":"1070", "level": 2, "tag": ["highway", "waterway", "geom"], "desc":{"fr": u"Intersection entre une voie et de l'eau", "en": u"Highway intersecting water"} }
        self.callback10 = lambda res: {"class":1, "data":[self.way_full, self.way_full, self.positionAsText]}
        self.callback20 = lambda res: {"class":2, "data":[self.node_full, self.way_full, self.positionAsText]}
        self.callback30 = lambda res: {"class":3, "data":[self.node_full, self.way_full, self.positionAsText]}
        self.callback40 = lambda res: {"class":4, "data":[self.way_full, self.way_full, self.positionAsText]}

    def analyser_osmosis_all(self):
        self.run(sql10.format("", ""), self.callback10)
        self.run(sql20.format("", ""), self.callback20)
        self.run(sql30.format("", ""), self.callback30)
        self.run(sql40.format("", ""), self.callback40)

    def analyser_osmosis_touched(self):
        self.run(sql10.format("touched_", ""), self.callback10)
        self.run(sql10.format("", "touched_"), self.callback10)
        self.run(sql20.format("touched_", ""), self.callback20)
        self.run(sql20.format("", "touched_"), self.callback20)
        self.run(sql30.format("touched_", ""), self.callback30)
        self.run(sql30.format("", "touched_"), self.callback30)
        self.run(sql40.format("touched_", ""), self.callback40)
        self.run(sql40.format("", "touched_"), self.callback40)
