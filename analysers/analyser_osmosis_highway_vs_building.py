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

from .Analyser_Osmosis import Analyser_Osmosis

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

sql03 = """
CREATE INDEX idx_tree_geom ON tree USING gist(geom)
"""

sql04 = """
CREATE TEMP TABLE power AS
SELECT
    id,
    geom
FROM
    nodes
WHERE
    tags != ''::hstore AND
    tags?'power' AND
    tags->'power' IN ('tower', 'pole', 'portal')
"""

sql05 = """
CREATE INDEX idx_power_geom ON power USING gist(geom)
"""

sql10 = """
SELECT
    building.id,
    highway.id,
    ST_AsText(way_locate(building.linestring))
FROM
    {0}buildings AS building
    JOIN {1}highway AS highway ON
        ST_Crosses(building.linestring, highway.linestring)
WHERE
    building.wall AND
    NOT building.layer
"""

sql20 = """
SELECT
    tree.id,
    building.id,
    ST_AsText(tree.geom)
FROM
    {0}tree AS tree
    JOIN {1}buildings AS building ON
        tree.geom && building.linestring AND
        ST_Intersects(tree.geom, ST_MakePolygon(building.linestring)) AND
        NOT building.relation AND
        building.wall AND
        NOT building.layer
"""

sql21 = """
SELECT
    power.id,
    building.id,
    ST_AsText(power.geom)
FROM
    {0}power AS power
    JOIN {1}buildings AS building ON
        power.geom && building.linestring AND
        ST_Intersects(power.geom, ST_MakePolygon(building.linestring)) AND
        NOT building.relation AND
        building.wall AND
        NOT building.layer
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

sql31 = """
SELECT
    power.id,
    highway.id,
    ST_AsText(power.geom)
FROM
    {0}power AS power
    JOIN {1}highway AS highway ON
        power.geom && highway.linestring AND
        ST_Intersects(ST_Buffer(power.geom::geography, 0.25)::geometry, highway.linestring)
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

    requires_tables_full = ['buildings']
    requires_tables_diff = ['buildings', 'touched_buildings']

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs_change[1] = {"item":"1070", "level": 2, "tag": ["highway", "building", "geom", "fix:imagery"], "desc": T_(u"Highway intersecting building") }
        self.classs_change[2] = {"item":"1070", "level": 2, "tag": ["tree", "building", "geom", "fix:imagery"], "desc": T_(u"Tree intersecting building") }
        self.classs_change[3] = {"item":"1070", "level": 2, "tag": ["highway", "tree", "geom", "fix:imagery"], "desc": T_(u"Tree and highway too close") }
        self.classs_change[4] = {"item":"1070", "level": 3, "tag": ["highway", "waterway", "geom", "fix:imagery"], "desc": T_(u"Highway intersecting small water piece") }
        self.classs_change[5] = {"item":"1070", "level": 2, "tag": ["highway", "waterway", "geom", "fix:imagery"], "desc": T_(u"Highway intersecting large water piece") }
        self.classs_change[6] = {"item":"1070", "level": 2, "tag": ["power", "building", "geom", "fix:imagery"], "desc": T_(u"Power object intersecting building") }
        self.classs_change[7] = {"item":"1070", "level": 2, "tag": ["highway", "power", "geom", "fix:imagery"], "desc": T_(u"Power object and highway too close") }
        self.callback10 = lambda res: {"class":1, "data":[self.way_full, self.way_full, self.positionAsText]}
        self.callback20 = lambda res: {"class":2, "data":[self.node_full, self.way_full, self.positionAsText]}
        self.callback21 = lambda res: {"class":6, "data":[self.node_full, self.way_full, self.positionAsText]}
        self.callback30 = lambda res: {"class":3, "data":[self.node_full, self.way_full, self.positionAsText]}
        self.callback31 = lambda res: {"class":7, "data":[self.node_full, self.way_full, self.positionAsText]}
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
        self.run(sql21.format("", ""), self.callback21)
        self.run(sql30.format("", ""), self.callback30)
        self.run(sql31.format("", ""), self.callback31)
        self.run(sql40.format("", ""), self.callback40)

    def analyser_osmosis_diff(self):
        self.run(sql00)
        self.run(sql01)
        self.run(sql02)
        self.run(sql03)
        self.run(sql04)
        self.run(sql05)
        self.create_view_touched("highway", "W")
        self.create_view_touched("tree", "N")
        self.create_view_touched("power", "N")
        self.create_view_not_touched("highway", "W")
        self.create_view_not_touched("tree", "N")
        self.create_view_not_touched("power", "N")

        self.run(sql10.format("touched_", "not_touched_"), self.callback10)
        self.run(sql10.format("", "touched_"), self.callback10)
        self.run(sql20.format("touched_", ""), self.callback20)
        self.run(sql20.format("not_touched_", "touched_"), self.callback20)
        self.run(sql21.format("touched_", ""), self.callback21)
        self.run(sql21.format("not_touched_", "touched_"), self.callback21)
        self.run(sql30.format("touched_", ""), self.callback30)
        self.run(sql30.format("not_touched_", "touched_"), self.callback30)
        self.run(sql31.format("touched_", ""), self.callback31)
        self.run(sql31.format("not_touched_", "touched_"), self.callback31)
        self.run(sql40.format("touched_", "not_touched_"), self.callback40)
        self.run(sql40.format("", "touched_"), self.callback40)
