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

sql00 = """
CREATE TEMP TABLE {0}highway AS
SELECT
    id,
    linestring,
    highway.tags?'ford' OR highway.tags?'flood_prone' AS onwater
FROM
    {0}ways AS highway
WHERE
    ((
        highway.tags ? 'highway' AND
        highway.tags->'highway' IN (
            'motorway', 'motorway_link',
            'trunk', 'trunk_link',
            'primary', 'primary_link',
            'secondary', 'secondary_link',
            'tertiary', 'tertiary_link',
            'unclassified', 'residential', 'living_street')
    ) OR (
        highway.tags ? 'railway' AND
        highway.tags->'railway' IN ('rail', 'tram')
    )) AND
    NOT highway.tags?'tunnel' AND
    NOT highway.tags?'bridge' AND
    NOT highway.tags?'covered' AND
    NOT highway.tags?'area' AND
    NOT highway.tags?'layer' AND
    ST_NPoints(highway.linestring) > 1
"""

sql01 = """
CREATE INDEX idx_{0}highway_linestring ON {0}highway USING gist(linestring)
"""

sql02 = """
CREATE TEMP TABLE {0}building AS
SELECT
    id,
    linestring,
    relation_members.member_id IS NULL AS relation
FROM
    {0}ways AS building
    LEFT JOIN relation_members ON
        relation_members.member_type = 'W' AND
        relation_members.member_id = building.id
WHERE
    building.tags?'building' AND
    building.tags->'building' != 'no' AND
    NOT building.tags?'wall' AND
    building.is_polygon
"""

sql03 = """
CREATE INDEX idx_{0}building_linestring ON {0}building USING gist(linestring)
"""

sql04 = """
CREATE TEMP TABLE {0}tree AS
SELECT
    id,
    geom
FROM
    {0}nodes AS tree
WHERE
    tree.tags?'natural' AND
    tree.tags->'natural' = 'tree'
"""

sql05 = """
CREATE INDEX idx_{0}tree_linestring ON {0}tree USING gist(geom)
"""

sql10 = """
SELECT
    building.id,
    highway.id,
    ST_AsText(way_locate(building.linestring))
FROM
    {0}building
    JOIN {1}highway ON
        ST_Crosses(building.linestring, highway.linestring)
"""

sql20 = """
SELECT
    tree.id,
    building.id,
    ST_AsText(tree.geom)
FROM
    {0}tree
    JOIN {1}building ON
        NOT building.relation AND
        tree.geom && building.linestring AND
        ST_Intersects(tree.geom, ST_MakePolygon(building.linestring))
"""

sql30 = """
SELECT
    tree.id,
    highway.id,
    ST_AsText(tree.geom)
FROM
    {0}tree
    JOIN {1}highway ON
        tree.geom && highway.linestring AND
        ST_Intersects(ST_Buffer(tree.geom::geography, 0.25)::geometry, highway.linestring)
"""

sql40 = """
SELECT
    highway.id,
    water.id,
    ST_AsText(ST_Centroid(ST_Intersection(highway.linestring, water.linestring)))
FROM
    {0}highway
    JOIN {1}ways AS water ON
        highway.linestring && water.linestring AND
        ST_NPoints(water.linestring) > 1 AND
        ST_Crosses(highway.linestring, water.linestring)
    LEFT JOIN nodes ON
        nodes.geom && highway.linestring AND
        nodes.geom && water.linestring AND
        nodes.geom && ST_Centroid(ST_Intersection(highway.linestring, water.linestring))
WHERE
    NOT highway.onwater AND
    (nodes.id IS NULL OR NOT nodes.tags?'ford') AND
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
        self.classs_change[1] = {"item":"1070", "level": 2, "tag": ["highway", "building", "geom", "fix:imagery"], "desc": T_(u"Highway intersecting building") }
        self.classs_change[2] = {"item":"1070", "level": 2, "tag": ["tree", "building", "geom", "fix:imagery"], "desc": T_(u"Tree intersecting building") }
        self.classs_change[3] = {"item":"1070", "level": 2, "tag": ["highway", "tree", "geom", "fix:imagery"], "desc": T_(u"Tree and highway too close") }
        self.classs_change[4] = {"item":"1070", "level": 2, "tag": ["highway", "waterway", "geom", "fix:imagery"], "desc": T_(u"Highway intersecting water") }
        self.callback10 = lambda res: {"class":1, "data":[self.way_full, self.way_full, self.positionAsText]}
        self.callback20 = lambda res: {"class":2, "data":[self.node_full, self.way_full, self.positionAsText]}
        self.callback30 = lambda res: {"class":3, "data":[self.node_full, self.way_full, self.positionAsText]}
        self.callback40 = lambda res: {"class":4, "data":[self.way_full, self.way_full, self.positionAsText]}

    def analyser_osmosis_all(self):
        self.run(sql00.format(""))
        self.run(sql01.format(""))
        self.run(sql02.format(""))
        self.run(sql03.format(""))
        self.run(sql04.format(""))
        self.run(sql05.format(""))

        self.run(sql10.format("", ""), self.callback10)
        self.run(sql20.format("", ""), self.callback20)
        self.run(sql30.format("", ""), self.callback30)
        self.run(sql40.format("", ""), self.callback40)

    def analyser_osmosis_touched(self):
        self.run(sql00.format(""))
        self.run(sql01.format(""))
        self.run(sql02.format(""))
        self.run(sql03.format(""))
        self.run(sql04.format(""))
        self.run(sql05.format(""))
        self.run(sql00.format("touched_"))
        self.run(sql01.format("touched_"))
        self.run(sql02.format("touched_"))
        self.run(sql03.format("touched_"))
        self.run(sql04.format("touched_"))
        self.run(sql05.format("touched_"))

        self.run(sql10.format("touched_", ""), self.callback10)
        self.run(sql10.format("", "touched_"), self.callback10)
        self.run(sql20.format("touched_", ""), self.callback20)
        self.run(sql20.format("", "touched_"), self.callback20)
        self.run(sql30.format("touched_", ""), self.callback30)
        self.run(sql30.format("", "touched_"), self.callback30)
        self.run(sql40.format("touched_", ""), self.callback40)
        self.run(sql40.format("", "touched_"), self.callback40)
