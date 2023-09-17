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

from modules.OsmoseTranslation import T_
from .Analyser_Osmosis import Analyser_Osmosis

sql00 = """
CREATE TEMP TABLE {0}highway AS
WITH railways_highways AS (
SELECT
    id,
    linestring,
    linestring_proj,
    tags,
    nodes
FROM
    {0}highways
WHERE
    NOT is_construction AND
    NOT is_area AND
    highway != 'elevator' AND
    NOT tags?'area:highway'
UNION ALL
SELECT
    id,
    linestring,
    ST_Transform(linestring, {1}) AS linestring_proj,
    tags,
    nodes
FROM
    {0}ways
WHERE
    tags != ''::hstore AND
    tags?'railway' AND
    tags->'railway' IN ('rail', 'tram') AND
    (NOT tags?'area' OR tags->'area' = 'no') AND
    ST_NPoints(linestring) > 1
),
ways AS ( -- WITH continuation
SELECT
    id,
    linestring,
    linestring_proj,
    ceil(ST_Length(ST_Transform(linestring, {1})) / 500)::integer AS split_n,
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
    railways_highways
)
SELECT
    id,
    linestring_part AS linestring,
    linestring_proj_part AS linestring_proj,
    nodes,
    highway,
    level,
    layer,
    onwater
FROM
    ways
    CROSS JOIN LATERAL (
        SELECT
            ST_LineSubstring(
                linestring,
                i::float / split_n,
                (i + 1)::float / split_n
            ) AS linestring_part,
            ST_LineSubstring(
                linestring_proj,
                i::float / split_n,
                (i + 1)::float / split_n
            ) AS linestring_proj_part
        FROM
            generate_series(0, split_n - 1) AS t(i)
    ) AS t
"""

sql01 = """
CREATE INDEX idx_{0}highway_linestring ON {0}highway USING gist(linestring);
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
    tags->'natural' = 'tree' AND
    (NOT tags?'level' OR tags->'level' = '0') AND
    (NOT tags?'layer' OR tags->'layer' = '0')
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

sql08 = """
CREATE TEMP TABLE commercial AS
SELECT
    id,
    geom,
    COALESCE(tags->'layer', '0') AS layer,
    ST_Buffer(geom::geography, 0.9)::geometry AS buffergeom
FROM
    nodes
WHERE
    tags != ''::hstore AND
    (
      (tags?'craft' AND tags->'craft'!='no') OR
      (tags?'shop' AND tags->'shop'!='no') OR
      (tags?'office' AND tags->'office'!='no')
    ) AND
    (NOT tags?'street_vendor' OR tags->'street_vendor' = 'no') AND
    (NOT tags?'drive_through' OR tags->'drive_through' = 'no') AND
    (NOT tags?'level' OR tags->'level' = '0')
"""

sql09 = """
CREATE INDEX idx_commercial_buffergeom ON commercial USING gist(buffergeom)
"""

sql10 = """
SELECT DISTINCT ON (highway.id, building.id)
    building.id,
    highway.id,
    ST_AsText(way_locate(building.linestring))
FROM
    {0}buildings AS building
    JOIN {1}highway AS highway ON
        highway.highway NOT IN ('footway', 'path', 'steps', 'corridor') AND
        highway.level = '0' AND
        highway.layer = '0' AND
        ST_Crosses(building.polygon_proj, highway.linestring_proj) AND
        ST_Dimension(ST_Intersection(building.polygon_proj, highway.linestring_proj)) >= 1 -- The cross is more than a point
WHERE
    building.wall AND
    NOT building.layer AND
    (NOT building.tags?'amenity' OR building.tags->'amenity'!='parking')
ORDER BY
    highway.id,
    building.id
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
SELECT DISTINCT ON (tree.id)
    tree.id,
    highway.id,
    ST_AsText(tree.geom)
FROM
    {0}tree AS tree
    JOIN {1}highway AS highway ON
        highway.level = '0' AND
        highway.layer = '0' AND
        highway.highway NOT IN ('footway', 'path', 'track') AND
        tree.geom && highway.linestring AND
        ST_Intersects(ST_Buffer(tree.geom::geography, 0.25)::geometry, highway.linestring)
ORDER BY
    tree.id
"""

sql31 = """
SELECT DISTINCT ON (power.id)
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
ORDER BY
    power.id
"""

sql32 = """
SELECT DISTINCT ON (commercial.id)
    commercial.id,
    highway.id,
    ST_AsText(commercial.geom)
FROM
    {0}commercial AS commercial
    JOIN {1}highway AS highway ON
        highway.level = '0' AND
        commercial.layer = highway.layer AND
        commercial.buffergeom && highway.linestring AND
        ST_Intersects(commercial.buffergeom, highway.linestring) AND
        (
            -- exclude shops nearly touching service roads (e.g. unmapped drivethroughs), pedestrian ways (e.g. shopping streets), ...
            highway.highway IS NULL OR -- railways are also in table highway
            highway.highway IN ('living_street', 'residential', 'unclassified', 'tertiary', 'tertiary_link',
                              'secondary', 'secondary_link', 'primary', 'primary_link', 'trunk', 'trunk_link',
                              'motorway', 'motorway_link', 'busway', 'bus_guideway')
        )
ORDER BY
    commercial.id,
    highway.id
"""

sql40 = """
SELECT DISTINCT ON (highway.id, water.id)
    highway.id,
    water.id,
    ST_AsText(ST_Centroid(ST_Intersection(highway.linestring, water.linestring))),
    CASE WHEN water.waterway IN ('river', 'canal') THEN 5 ELSE 4 END
FROM
    {0}highway AS highway
    JOIN {1}water AS water ON
        ST_Crosses(highway.linestring, water.linestring)
    LEFT JOIN nodes ON
        ST_Intersects(nodes.geom, ST_Intersection(highway.linestring, water.linestring))
WHERE
    highway.level = '0' AND
    highway.layer = water.layer AND
    NOT highway.onwater AND
    (nodes.id IS NULL OR NOT nodes.tags?'ford')
    {2} -- used to exclude specific types for specific countries
ORDER BY
    highway.id,
    water.id
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

    requires_tables_full = ['buildings', 'highways']
    requires_tables_diff = ['buildings', 'touched_buildings', 'highways']

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        doc = dict(
            detail = T_(
'''Two features overlap with no shared node to indicate a physical connection or tagging to indicate a vertical separation.'''),
            fix = T_(
'''Move a feature if it's in the wrong place. Connect the features if appropriate or update the tags if not.'''),
            trap = T_(
'''A feature may be missing a tag, such as `tunnel=*`, `bridge=*`, `covered=*` or `ford=*`.
If a road or railway intersects a building, consider adding the `layer=*` tag to it.
Warning: information sources can be contradictory in time or with spatial offset.'''),
            example = T_(
'''![](https://wiki.openstreetmap.org/w/images/d/dc/Osmose-eg-error-1070.png)

Intersection lane / building.'''))
        self.classs_change[1] = self.def_class(item = 1070, level = 2, tags = ['highway', 'building', 'geom', 'fix:imagery'], title = T_(u'Highway intersecting building'), **doc)
        self.classs_change[2] = self.def_class(item = 1070, level = 2, tags = ['tree', 'building', 'geom', 'fix:imagery'], title = T_(u'Tree intersecting building'), **doc)
        self.classs_change[3] = self.def_class(item = 1070, level = 2, tags = ['highway', 'tree', 'geom', 'fix:imagery'], title = T_(u'Tree and highway too close'), **doc)
        self.classs_change[4] = self.def_class(item = 1070, level = 3, tags = ['highway', 'waterway', 'geom', 'fix:imagery'], title = T_(u'Highway intersecting small water piece'), **doc)
        self.classs_change[5] = self.def_class(item = 1070, level = 2, tags = ['highway', 'waterway', 'geom', 'fix:imagery'], title = T_(u'Highway intersecting large water piece'), **doc)
        self.classs_change[6] = self.def_class(item = 1070, level = 2, tags = ['power', 'building', 'geom', 'fix:imagery'], title = T_(u'Power object intersecting building'), **doc)
        self.classs_change[7] = self.def_class(item = 1070, level = 2, tags = ['highway', 'power', 'geom', 'fix:imagery'], title = T_(u'Power object and highway too close'), **doc)
        self.classs_change[8] = self.def_class(item = 1070, level = 2, tags = ['highway', 'geom', 'fix:imagery'], title = T_(u'Highway intersecting highway'), **doc)
        self.classs_change[9] = self.def_class(item = 1070, level = 2, tags = ['highway', 'geom', 'fix:imagery'], title = T_(u'Highway overlaps'), **doc)
        self.classs_change[10] = self.def_class(item = 1070, level = 3, tags = ['waterway', 'geom', 'fix:imagery'], title = T_(u'Waterway intersecting waterway'), **doc)
        self.classs_change[11] = self.def_class(item = 1070, level = 3, tags = ['waterway', 'geom', 'fix:imagery'], title = T_(u'Waterway overlaps'), **doc)
        self.classs_change[16] = self.def_class(item = 1070, level = 2, tags = ['highway', 'shop', 'geom'], title = T_(u'Commercial object or office and highway too close'), **doc)
        self.callback10 = lambda res: {"class":1, "data":[self.way_full, self.way_full, self.positionAsText]}
        self.callback20 = lambda res: {"class":2, "data":[self.node_full, self.way_full, self.positionAsText]}
        self.callback21 = lambda res: {"class":6, "data":[self.node_full, self.way_full, self.positionAsText]}
        self.callback30 = lambda res: {"class":3, "data":[self.node_full, self.way_full, self.positionAsText]}
        self.callback31 = lambda res: {"class":7, "data":[self.node_full, self.way_full, self.positionAsText]}
        self.callback32 = lambda res: {"class":16, "data":[self.node_full, self.way_full, self.positionAsText]}
        self.callback40 = lambda res: {"class":res[3], "data":[self.way_full, self.way_full, self.positionAsText]}
        self.callback50 = lambda res: {"class":res[3], "data":[self.way_full, self.way_full, self.positionAsText] }
        self.callback60 = lambda res: {"class":res[3], "data":[self.way_full, self.way_full, self.positionAsText] }

        self.country = self.config.options.get("country")

    def analyser_osmosis_full(self):
        self.run(sql00.format("", self.config.options.get("proj")))
        self.run(sql01.format(""))
        self.run(sql02)
        self.run(sql03)
        self.run(sql04)
        self.run(sql05)
        self.run(sql08)
        self.run(sql09)
        self.run(sql06.format(""))
        self.run(sql07.format(""))

        self.run(sql10.format("", ""), self.callback10)
        self.run(sql20.format("", ""), self.callback20)
        self.run(sql21.format("", ""), self.callback21)
        self.run(sql30.format("", ""), self.callback30)
        self.run(sql31.format("", ""), self.callback31)
        self.run(sql32.format("", ""), self.callback32)
        if self.country and self.country.startswith("CA-BC"): # Too many results
            self.run(sql40.format("", "", "AND water.waterway != 'stream'"), self.callback40)
        else:
            self.run(sql40.format("", "", ""), self.callback40)
        self.run(sql50.format("", "", "false"))
        self.run(sql51.format("", ""), self.callback50)
        self.run(sql60.format("", "", "false"))
        self.run(sql61.format("", ""), self.callback60)

    def analyser_osmosis_diff(self):
        self.run(sql00.format("", self.config.options.get("proj")))
        self.run(sql01.format(""))
        self.run(sql02)
        self.run(sql03)
        self.run(sql04)
        self.run(sql05)
        self.run(sql06.format(""))
        self.run(sql07.format(""))
        self.run(sql08)
        self.run(sql09)
        self.create_view_touched("highway", "W")
        self.create_view_touched("tree", "N")
        self.create_view_touched("power", "N")
        self.create_view_touched("water", "N")
        self.create_view_touched("commercial", "N")
        self.create_view_not_touched("highway", "W")
        self.create_view_not_touched("tree", "N")
        self.create_view_not_touched("power", "N")
        self.create_view_not_touched("water", "W")
        self.create_view_not_touched("commercial", "N")

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
        self.run(sql32.format("touched_", ""), self.callback31)
        self.run(sql32.format("not_touched_", "touched_"), self.callback31)
        if self.country and self.country.startswith("CA-BC"): # Too many results
            self.run(sql40.format("touched_", "not_touched_", "AND water.waterway != 'stream'"), self.callback40)
            self.run(sql40.format("", "touched_", "AND water.waterway != 'stream'"), self.callback40)
        else:
            self.run(sql40.format("touched_", "not_touched_", ""), self.callback40)
            self.run(sql40.format("", "touched_", ""), self.callback40)
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


from .Analyser_Osmosis import TestAnalyserOsmosis

class Test(TestAnalyserOsmosis):
    @classmethod
    def setup_class(cls):
        from modules import config
        TestAnalyserOsmosis.setup_class()
        cls.analyser_conf = cls.load_osm("tests/osmosis_highway_vs_building.osm",
                                         config.dir_tmp + "/tests/osmosis_highway_vs_building.test.xml",
                                         {"proj": 23032})

    def test_classes(self):
        with Analyser_Osmosis_Highway_VS_Building(self.analyser_conf, self.logger) as a:
            a.analyser()

        self.root_err = self.load_errors()
        self.check_err(cl="1", elems=[("way", "106047"), ("way", "105973")])
        self.check_err(cl="1", elems=[("way", "106100"), ("way", "105973")])
        self.check_err(cl="1", elems=[("way", "106047"), ("way", "106077")])
        self.check_err(cl="1", elems=[("way", "116804"), ("way", "116609")])
        self.check_err(cl="1", elems=[("way", "116666"), ("way", "116609")])
        self.check_err(cl="1", elems=[("way", "116638"), ("way", "116609")])
        self.check_err(cl="2", elems=[("way", "106047"), ("node", "139726")])
        self.check_err(cl="3", elems=[("way", "105973"), ("node", "139808")])
        self.check_err(cl="3", elems=[("way", "105973"), ("node", "139838")])
        self.check_err(cl="4", elems=[("way", "105973"), ("way", "106401")])
        self.check_err(cl="4", elems=[("way", "105973"), ("way", "106260")])
        self.check_err(cl="5", elems=[("way", "105973"), ("way", "106234")])
        self.check_err(cl="6", elems=[("way", "106047"), ("node", "139728")])
        self.check_err(cl="7", elems=[("way", "105973"), ("node", "139807")])
        self.check_err(cl="8", elems=[("way", "105973"), ("way", "106603")])
        self.check_err(cl="8", elems=[("way", "105973"), ("way", "106285")])
        self.check_err(cl="9", elems=[("way", "105973"), ("way", "106427")])
        self.check_err(cl="10", elems=[("way", "106234"), ("way", "106526")])
        self.check_err(cl="11", elems=[("way", "106234"), ("way", "106555")])
        self.check_err(cl="16", elems=[("way", "105973"), ("node", "139809")])
        self.check_num_err(20)
