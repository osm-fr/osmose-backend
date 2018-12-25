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
CREATE TEMP TABLE {0}highway AS
SELECT
    id,
    linestring,
    nodes,
    tags->'highway' AS highway,
    coalesce(tags->'level', '0') AS level,
    CASE
        WHEN tags?'layer' THEN tags->'layer'
        WHEN tags->'tunnel' != 'no' THEN 'tunnel'
        WHEN tags->'bridge' != 'no' THEN 'bridge'
        ELSE '0'
    END AS layer,
    tags ?| ARRAY['ford', 'flood_prone'] AS onwater
FROM
    {0}ways AS ways
WHERE
    tags != ''::hstore AND
    ((
        tags?'highway' AND
        tags->'highway' NOT IN ('planned', 'proposed', 'construction', 'rest_area', 'razed', 'no')
    ) OR (
        tags?'railway' AND
        tags->'railway' IN ('rail', 'tram')
    )) AND
    (NOT tags?'area' OR tags->'area' = 'no') AND
    NOT tags?'area:highway' AND
    array_length(nodes, 1) <= 100 AND -- Large ways have too big bbox
    ST_NPoints(linestring) > 1
"""

sql01 = """
CREATE INDEX idx_{0}highway_linestring ON {0}highway USING gist(linestring)
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

sql06 = """
CREATE TEMP TABLE {0}water AS
SELECT
    id,
    tags->'waterway' AS waterway,
    nodes,
    CASE
        WHEN tags?'layer' THEN tags->'layer'
        WHEN tags->'tunnel' != 'no' THEN 'tunnel'
        WHEN tags->'bridge' != 'no' THEN 'bridge'
        ELSE '0'
    END AS layer,
    linestring AS linestring
FROM
    {0}ways AS ways
WHERE
    tags != ''::hstore AND
    (
        tags?'waterway' AND tags->'waterway' IN ('stream', 'ditch', 'river', 'drain', 'canal', 'riverbank') OR
        (
            tags?'natural' AND
            tags->'natural' = 'water'
        )
    ) AND
    ST_NPoints(linestring) > 1
"""

sql07 = """
CREATE INDEX idx_{0}water_linestring ON {0}water USING gist(linestring)
"""

sql10 = """
SELECT
    building.id,
    highway.id,
    ST_AsText(way_locate(building.linestring))
FROM
    {0}buildings AS building
    JOIN {1}highway AS highway ON
        highway.highway NOT IN ('footway', 'path', 'steps', 'elevator', 'corridor') AND
        highway.level = '0' AND
        highway.layer = '0' AND
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
        highway.level = '0' AND
        highway.layer = '0' AND
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
        highway.level = '0' AND
        highway.layer = '0' AND
        power.geom && highway.linestring AND
        ST_Intersects(ST_Buffer(power.geom::geography, 0.25)::geometry, highway.linestring)
"""

sql40 = """
SELECT
    highway.id,
    water.id,
    ST_AsText(ST_Centroid(ST_Intersection(highway.linestring, water.linestring))),
    CASE WHEN water.waterway IN ('river', 'canal') THEN 5 ELSE 4 END
FROM
    {0}highway AS highway
    JOIN {1}water AS water ON
        ST_Crosses(highway.linestring, water.linestring)
    LEFT JOIN nodes ON
        nodes.geom && highway.linestring AND
        nodes.geom && water.linestring AND
        ST_Intersects(nodes.geom, ST_Intersection(highway.linestring, water.linestring))
WHERE
    highway.level = '0' AND
    highway.layer = water.layer AND
    NOT highway.onwater AND
    (nodes.id IS NULL OR NOT nodes.tags?'ford')
"""

sql50 = """
CREATE TEMP TABLE {0}{1}inter AS
SELECT
  ih1.id AS id1,
  ih2.id AS id2,
  ih2.level = ih1.level AS level,
  ih2.layer = ih1.layer AS layer,
  ST_Dimension(ST_Intersection(ih2.linestring, ih1.linestring)) = 0 AS corsses,
  ST_Dimension(ST_Intersection(ih2.linestring, ih1.linestring)) = 1 AS overlaps_,
  ST_Intersection(ih2.linestring, ih1.linestring) AS intersection
FROM
  {0}highway AS ih1
  JOIN {1}highway AS ih2 ON
    ih1.highway IS NOT NULL AND
    ih2.highway IS NOT NULL AND
    ({2} OR ih2.id > ih1.id) AND
    (
      (
        NOT ih2.nodes && ih1.nodes AND
        ST_Crosses(ih2.linestring, ih1.linestring)
      ) OR
      ST_Overlaps(ih2.linestring, ih1.linestring)
    )
"""

sql51 = """
SELECT
  id1,
  id2,
  CASE ST_Dimension(geom)
    WHEN 0 THEN ST_AsText(geom)
    WHEN 1 THEN ST_ASText(way_locate(geom))
  END,
  CASE
    WHEN corsses THEN 8
    WHEN overlaps_ THEN 9
  END AS class
FROM (
  SELECT
    DISTINCT ON(id1, id2)
    id1,
    id2,
    (ST_DUMP(intersection)).geom AS geom,
    corsses,
    overlaps_
  FROM
    {0}{1}inter
  WHERE
    level AND
    layer
  ORDER BY
    id1,
    id2,
    ST_Dimension((ST_DUMP(intersection)).geom) DESC
  ) AS t
"""

sql60 = """
CREATE TEMP TABLE {0}{1}winter AS
SELECT
  ih1.id AS id1,
  ih2.id AS id2,
  ih2.layer = ih1.layer AS layer,
  ST_Dimension(ST_Intersection(ih2.linestring, ih1.linestring)) = 0 AS corsses,
  ST_Dimension(ST_Intersection(ih2.linestring, ih1.linestring)) = 1 AS overlaps_,
  ST_Intersection(ih2.linestring, ih1.linestring) AS intersection
FROM
  {0}water AS ih1
  JOIN {1}water AS ih2 ON
    ih1.waterway IN ('stream', 'ditch', 'river', 'drain', 'canal') AND
    ih2.waterway IN ('stream', 'ditch', 'river', 'drain', 'canal') AND
    ({2} OR ih2.id > ih1.id) AND
    (
      (
        NOT ih2.nodes && ih1.nodes AND
        ST_Crosses(ih2.linestring, ih1.linestring)
      ) OR
      ST_Overlaps(ih2.linestring, ih1.linestring)
    )
"""

sql61 = """
SELECT
  id1,
  id2,
  CASE ST_Dimension(geom)
    WHEN 0 THEN ST_AsText(geom)
    WHEN 1 THEN ST_ASText(way_locate(geom))
  END,
  CASE
    WHEN corsses THEN 10
    WHEN overlaps_ THEN 11
  END AS class
FROM (
  SELECT
    DISTINCT ON(id1, id2)
    id1,
    id2,
    (ST_DUMP(intersection)).geom AS geom,
    corsses,
    overlaps_
  FROM
    {0}{1}winter
  WHERE
    layer
  ORDER BY
    id1,
    id2,
    ST_Dimension((ST_DUMP(intersection)).geom) DESC
  ) AS t
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
        self.classs_change[8] = {"item":"1070", "level": 2, "tag": ["highway", "geom", "fix:imagery"], "desc": T_(u"Highway intersecting highway without junction") }
        self.classs_change[9] = {"item":"1070", "level": 2, "tag": ["highway", "geom", "fix:imagery"], "desc": T_(u"Highway overlaps") }
        self.classs_change[10] = {"item":"1070", "level": 3, "tag": ["waterway", "geom", "fix:imagery"], "desc": T_(u"Waterway intersecting waterway without junction") }
        self.classs_change[11] = {"item":"1070", "level": 3, "tag": ["waterway", "geom", "fix:imagery"], "desc": T_(u"Waterway overlaps") }
        self.callback10 = lambda res: {"class":1, "data":[self.way_full, self.way_full, self.positionAsText]}
        self.callback20 = lambda res: {"class":2, "data":[self.node_full, self.way_full, self.positionAsText]}
        self.callback21 = lambda res: {"class":6, "data":[self.node_full, self.way_full, self.positionAsText]}
        self.callback30 = lambda res: {"class":3, "data":[self.node_full, self.way_full, self.positionAsText]}
        self.callback31 = lambda res: {"class":7, "data":[self.node_full, self.way_full, self.positionAsText]}
        self.callback40 = lambda res: {"class":res[3], "data":[self.way_full, self.way_full, self.positionAsText]}
        self.callback50 = lambda res: {"class":res[3], "data":[self.way_full, self.way_full, self.positionAsText] }
        self.callback60 = lambda res: {"class":res[3], "data":[self.way_full, self.way_full, self.positionAsText] }

    def analyser_osmosis_full(self):
        self.run(sql00.format(""))
        self.run(sql01.format(""))
        self.run(sql02)
        self.run(sql03)
        self.run(sql04)
        self.run(sql05)
        self.run(sql06.format(""))
        self.run(sql07.format(""))

        self.run(sql10.format("", ""), self.callback10)
        self.run(sql20.format("", ""), self.callback20)
        self.run(sql21.format("", ""), self.callback21)
        self.run(sql30.format("", ""), self.callback30)
        self.run(sql31.format("", ""), self.callback31)
        self.run(sql40.format("", ""), self.callback40)
        self.run(sql50.format("", "", "false"))
        self.run(sql51.format("", ""), self.callback50)
        self.run(sql60.format("", "", "false"))
        self.run(sql61.format("", ""), self.callback60)

    def analyser_osmosis_diff(self):
        self.run(sql00.format(""))
        self.run(sql01.format(""))
        self.run(sql02)
        self.run(sql03)
        self.run(sql04)
        self.run(sql05)
        self.run(sql06.format(""))
        self.run(sql07.format(""))
        self.create_view_touched("highway", "W")
        self.create_view_touched("tree", "N")
        self.create_view_touched("power", "N")
        self.create_view_touched("water", "N")
        self.create_view_not_touched("highway", "W")
        self.create_view_not_touched("tree", "N")
        self.create_view_not_touched("power", "N")
        self.create_view_not_touched("water", "W")

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
        self.run(sql50.format("not_touched_", "touched_", "true"))
        self.run(sql51.format("not_touched_", "touched_"), self.callback50)
        self.run(sql50.format("touched_", "not_touched_", "true"))
        self.run(sql51.format("touched_", "not_touched_"), self.callback50)
        self.run(sql50.format("touched_", "touched_", "false"))
        self.run(sql51.format("touched_", "touched_"), self.callback50)
        self.run(sql60.format("not_touched_", "touched_", "true"))
        self.run(sql61.format("not_touched_", "touched_"), self.callback60)
        self.run(sql60.format("touched_", "not_touched_", "true"))
        self.run(sql61.format("touched_", "not_touched_"), self.callback60)
        self.run(sql60.format("touched_", "touched_", "false"))
        self.run(sql61.format("touched_", "touched_"), self.callback60)
