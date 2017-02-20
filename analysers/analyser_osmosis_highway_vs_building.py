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
CREATE TEMP TABLE highway AS
SELECT
    id,
    linestring,
    tags ?| ARRAY['ford', 'flood_prone'] AS onwater
FROM
    ways
WHERE
    tags != ''::hstore AND
    ((
        tags?'highway' AND
        tags->'highway' IN (
            'motorway', 'motorway_link',
            'trunk', 'trunk_link',
            'primary', 'primary_link',
            'secondary', 'secondary_link',
            'tertiary', 'tertiary_link',
            'unclassified', 'residential', 'living_street')
    ) OR (
        tags?'railway' AND
        tags->'railway' IN ('rail', 'tram')
    )) AND
    NOT tags ?| ARRAY['tunnel', 'bridge', 'covered', 'area', 'layer'] AND
    ST_NPoints(linestring) > 1
"""

sql01 = """
CREATE INDEX idx_highway_linestring ON highway USING gist(linestring)
"""

sql02 = """
CREATE TEMP TABLE building AS
SELECT
    id,
    linestring,
    (relation_members.member_id IS NOT NULL) AS in_relation
FROM
    ways AS building
    LEFT JOIN relation_members ON
        relation_members.member_type = 'W' AND
        relation_members.member_id = building.id
WHERE
    building.tags != ''::hstore AND
    building.tags?'building' AND
    NOT building.tags->'building' IN ('no', 'roof') AND
    NOT building.tags?'wall' AND
    NOT building.tags?'layer' AND
    building.is_polygon
"""

sql03 = """
CREATE INDEX idx_building_linestring ON building USING gist(linestring)
"""

sql04 = """
CREATE TEMP TABLE tree AS
SELECT
    id,
    geom
FROM
    nodes
WHERE
    tags != ''::hstore AND
    tags?'natural' AND
    tags->'natural' = 'tree'
"""

sql05 = """
CREATE INDEX idx_tree_linestring ON tree USING gist(geom)
"""

sql10 = """
SELECT
    building.id,
    highway.id,
    ST_AsText(way_locate(building.linestring))
FROM
    {0}building AS building
    JOIN {1}highway AS highway ON
        ST_Crosses(building.linestring, highway.linestring)
"""

sql20 = """
SELECT
    tree.id,
    building.id,
    ST_AsText(tree.geom)
FROM
    {0}tree AS tree
    JOIN {1}building AS building ON
        NOT building.in_relation AND
        tree.geom && building.linestring AND
        ST_Intersects(tree.geom, ST_MakePolygon(building.linestring))
"""

sql30 = """
SELECT
    tree.id,
    highway.id,
    ST_AsText(tree.geom)
FROM
    {0}tree AS tree
    JOIN {1}highway AS highway ON
        tree.geom && highway.linestring AND
        ST_Intersects(ST_Buffer(tree.geom::geography, 0.25)::geometry, highway.linestring)
"""

sql40 = """
SELECT
    highway.id,
    water.id,
    ST_AsText(ST_Centroid(ST_Intersection(highway.linestring, water.linestring))),
    CASE WHEN water.tags->'waterway' IN ('river', 'canal') THEN 5 ELSE 4 END
FROM
    {0}highway AS highway
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
        water.tags != ''::hstore AND
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
        self.classs_change[4] = {"item":"1070", "level": 3, "tag": ["highway", "waterway", "geom", "fix:imagery"], "desc": T_(u"Highway intersecting small water piece") }
        self.classs_change[5] = {"item":"1070", "level": 2, "tag": ["highway", "waterway", "geom", "fix:imagery"], "desc": T_(u"Highway intersecting large water piece") }
        self.callback10 = lambda res: {"class":1, "data":[self.way_full, self.way_full, self.positionAsText]}
        self.callback20 = lambda res: {"class":2, "data":[self.node_full, self.way_full, self.positionAsText]}
        self.callback30 = lambda res: {"class":3, "data":[self.node_full, self.way_full, self.positionAsText]}
        self.callback40 = lambda res: {"class":res[3], "data":[self.way_full, self.way_full, self.positionAsText]}

    def analyser_osmosis_full(self):
        self.run(sql00)
        self.run(sql01)
        self.run(sql02)
        self.run(sql03)
        self.run(sql04)
        self.run(sql05)

        self.run(sql10.format("", ""), self.callback10)
        self.run(sql20.format("", ""), self.callback20)
        self.run(sql30.format("", ""), self.callback30)
        self.run(sql40.format("", ""), self.callback40)

    def analyser_osmosis_diff(self):
        self.run(sql00)
        self.run(sql01)
        self.run(sql02)
        self.run(sql03)
        self.run(sql04)
        self.run(sql05)
        self.create_view_touched("highway", "W")
        self.create_view_touched("building", "W")
        self.create_view_touched("tree", "N")
        self.create_view_not_touched("highway", "W")
        self.create_view_not_touched("tree", "N")

        self.run(sql10.format("touched_", "not_touched_"), self.callback10)
        self.run(sql10.format("", "touched_"), self.callback10)
        self.run(sql20.format("touched_", ""), self.callback20)
        self.run(sql20.format("not_touched_", "touched_"), self.callback20)
        self.run(sql30.format("touched_", ""), self.callback30)
        self.run(sql30.format("not_touched_", "touched_"), self.callback30)
        self.run(sql40.format("touched_", "not_touched_"), self.callback40)
        self.run(sql40.format("", "touched_"), self.callback40)
