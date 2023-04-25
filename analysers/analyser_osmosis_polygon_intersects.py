#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Osmose project 2023                                        ##
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

sql10 = """
-- Collect all major highways, waterways, railways and aeroways
CREATE TEMP TABLE mobility_ways AS
SELECT
  *
FROM (
  SELECT
    id,
    linestring,
    'highway' AS type,
    tags
  FROM
    highways
  WHERE
    level = 1 -- tertiary (0.8M issues) and secondary (0.4M issues) + _links excluded due to excessive reports
  UNION ALL
  SELECT
    id,
    linestring,
    CASE
      WHEN tags?'waterway' THEN 'waterway'
      WHEN tags?'railway' THEN 'railway'
      WHEN tags?'aeroway' THEN 'aeroway'
    END AS type,
    tags
  FROM
    ways
  WHERE
    tags != ''::hstore AND
    (
      (
        tags?'railway' AND
        tags->'railway' NOT IN ('abandoned', 'construction', 'disused', 'dismantled', 'miniature', 'proposed', 'razed', 'subway') AND
        NOT is_polygon
      ) OR (
        tags?'waterway' AND
        tags->'waterway' = 'canal' AND -- big waterways -- river excluded due to excessive reports
        (NOT tags?'seasonal' OR tags->'seasonal' = 'no') AND
        (NOT tags?'intermittent' OR tags->'intermittent' = 'no')
      ) OR (
        tags?'aeroway' AND
        tags->'aeroway' IN ('apron', 'helipad', 'runway', 'taxilane', 'taxiway') AND -- aircraft moving places
        (NOT tags?'surface' OR tags->'surface' IN ('asphalt', 'paved', 'concrete')) -- ignore almost invisible landing areas in i.e. meadows
      )
    )
  ) AS t
WHERE
  NOT tags?'abandoned' AND
  NOT tags?'disused' AND
  NOT tags?'razed' AND
  (NOT tags?'bridge' OR tags->'bridge' = 'no') AND
  (NOT tags?'tunnel' OR tags->'tunnel' = 'no')
"""

sql11 = """
-- Collect all landuse=* and natural=*, closed ways and outer ways of multipolygons
CREATE TEMP TABLE landusage AS
SELECT
  id,
  linestring,
  ST_MakePolygon(linestring) AS poly,
  CASE
    WHEN tags?'landuse' THEN 'landuse'
    WHEN tags?'natural' THEN 'natural'
  END AS landusekey,
  CASE
    WHEN tags?'landuse' THEN tags->'landuse'
    WHEN tags?'natural' THEN tags->'natural'
  END AS landusevalue,
  tags,
  FALSE AS is_multipolygon
FROM
  ways
WHERE
  is_polygon AND
  tags != ''::hstore AND
  (tags?'natural' OR tags?'landuse') AND
  -- Leave minipolygons for analyser osmosis_polygon_small
  ST_Area(ST_MakePolygon(ST_Transform(linestring, {proj}))) >= 20
UNION ALL
SELECT
  ways.id,
  ways.linestring,
  -- Better would be to parse inner and outer segments and create an SQL multipolygon
  -- For now, just use a very small buffer zone around the linestring
  ST_Buffer(ways.linestring, 0.0000000001, 'quad_segs=1 endcap=flat join=bevel') AS poly,
  CASE
    WHEN r.tags?'landuse' THEN 'landuse'
    WHEN r.tags?'natural' THEN 'natural'
  END AS landusekey,
  CASE
    WHEN r.tags?'landuse' THEN r.tags->'landuse'
    WHEN r.tags?'natural' THEN r.tags->'natural'
  END AS landusevalue,
  r.tags,
  TRUE AS is_multipolygon
FROM
  relation_members
  LEFT JOIN relations AS r ON
    relation_id = r.id
  JOIN ways ON
    member_role = 'outer' AND
    member_id = ways.id AND
    member_type = 'W'
WHERE
  r.tags->'type' = 'multipolygon' AND
  (r.tags?'natural' OR r.tags?'landuse')
"""

sql12 = """
CREATE INDEX idx_mobilityway_linestring ON mobility_ways USING GIST(linestring);
CREATE INDEX idx_landusage_linestring ON landusage USING GIST(linestring);
"""

sql13 = """
-- Collect highway|rail|water|aeroways either entering or fully inside landuse/natural geometries
CREATE TEMP TABLE intersecting_geometries AS
SELECT
  mobility_ways.id AS mobility_way_id,
  mobility_ways.linestring AS mobility_way_linestring,
  mobility_ways.type AS mobility_way_type,
  landusage.id AS landusage_way_id,
  landusage.poly AS landusage_poly,
  landusage.landusekey,
  landusage.landusevalue,
  CONCAT(mobility_ways.type, '=', mobility_ways.tags->mobility_ways.type) AS tag_way,
  CONCAT(landusage.landusekey, '=', landusage.landusevalue) AS tag_polygon
FROM
  mobility_ways
  JOIN landusage ON
    (
      (
        NOT landusage.tags?'layer' AND NOT mobility_ways.tags?'layer'
      ) OR (
        landusage.tags?'layer' AND mobility_ways.tags?'layer' AND
        landusage.tags->'layer' = mobility_ways.tags->'layer'
      )
    ) AND
    landusage.linestring && mobility_ways.linestring AND
    -- Only find ways where the highway/railway/waterway/aeroway actually enters the
    -- polygon. Exclude cases where the polygon is tied to the way without going inside.
    (
      ST_Crosses(landusage.linestring, mobility_ways.linestring) OR
      (
        ST_Contains(landusage.poly, mobility_ways.linestring) AND
        NOT landusage.is_multipolygon -- due to ST_buffer approach for mp, instead of full parsing of inners/outers
      )
    )
"""

sql14 = """
-- Intersections with railway, aeroway or highway
SELECT
  mobility_way_id,
  landusage_way_id,
  ST_AsText(ST_PointOnSurface(ST_Intersection(landusage_poly, mobility_way_linestring))),
  mobility_way_type,
  tag_way,
  tag_polygon
FROM
  intersecting_geometries
WHERE
  mobility_way_type != 'waterway' AND
  (
    (
      landusekey = 'landuse' AND
      landusevalue NOT IN ('civic_admin', 'commercial', 'construction', 'education', 'grass', 'harbour', 'industrial', 'military', 'port', 'proposed', 'railway', 'religious', 'residential', 'retail', 'winter_sports')
    ) OR (
      landusekey = 'natural' AND
      landusevalue IN ('bay', 'cliff', 'scrub', 'shrubbery', 'sinkhole', 'tree_group', 'wetland', 'wood') OR
      (
        -- Special case as highway=* vs. natural=water is already included in item 1070 class 4/5
        landusevalue = 'water' AND
        mobility_way_type != 'highway'
      )
    )
  )
"""

sql15 = """
-- Intersections with waterway
SELECT
  mobility_way_id,
  landusage_way_id,
  ST_AsText(ST_PointOnSurface(ST_Intersection(landusage_poly, mobility_way_linestring))),
  mobility_way_type,
  tag_way,
  tag_polygon
FROM
  intersecting_geometries
WHERE
  mobility_way_type = 'waterway' AND
  (
    (
      landusekey = 'landuse' AND
      landusevalue NOT IN ('basin', 'civic_admin', 'commercial', 'construction', 'education', 'harbour', 'industrial', 'military', 'port', 'proposed', 'railway', 'recreation_ground', 'religious', 'reservoir', 'residential', 'retail', 'salt_pond', 'winter_sports')
    ) OR (
      landusekey = 'natural' AND
      landusevalue IN ('bare_rock', 'cliff', 'dune', 'grassland', 'rock', 'sand', 'scree', 'scrub', 'shrubbery', 'sinkhole', 'tree_group', 'wood')
    )
  )
"""

class Analyser_Osmosis_Polygon_Intersects(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        if not "proj" in self.config.options:
            return

        self.classIndex = {'highway': 12, 'railway': 13, 'waterway': 14, 'aeroway': 15}

        detailTxt = T_(
'''A way meant for transport (such as a highway or a waterway) intersects with a
land coverage that would pose an obstacle for this transportation mode.''')
        exampleTxt = T_(
'''A major highway usually does not have trees growing on it, so a crossing between
`landuse=forest` and `highway=trunk` is unlikely.
The same applies for a railway running through an area with `natural=water`,
without bridge or tunnel.''')
        fixTxt = T_(
'''If the way for transportation (such as a highway) has i.e. a forest growing on
either side of the way, cut out the shape of the highway from the forest polygon.
However, if the way for transportation is a tunnel or a bridge, add `tunnel=*` or
`bridge=*` where appropriate, together with `layer=*` if needed.''')

        self.classs[self.classIndex["highway"]] = self.def_class(
            item = 1070, level = 2, tags = ['landuse', 'fix:chair', 'highway'],
            title = T_('Bad intersection with major highway'),
            detail = detailTxt, example = exampleTxt, fix = fixTxt)
        self.classs[self.classIndex["railway"]] = self.def_class(
            item = 1070, level = 2, tags = ['landuse', 'fix:chair', 'railway'],
            title = T_('Bad intersection with railway'),
            detail = detailTxt, example = exampleTxt, fix = fixTxt)
        self.classs[self.classIndex["waterway"]] = self.def_class(
            item = 1070, level = 2, tags = ['landuse', 'fix:chair', 'waterway'],
            title = T_('Bad intersection with waterway'),
            detail = detailTxt, example = exampleTxt, fix = fixTxt)
        self.classs[self.classIndex["aeroway"]] = self.def_class(
            item = 1070, level = 2, tags = ['landuse', 'fix:chair'],
            title = T_('Bad intersection with aeroway'),
            detail = detailTxt, example = exampleTxt, fix = fixTxt)

    requires_tables_common = ['highways']

    def analyser_osmosis_common(self):
        self.run(sql10)
        self.run(sql11.format(proj=self.config.options["proj"]))
        self.run(sql12)
        self.run(sql13.format(proj=self.config.options["proj"]))
        self.run(sql14, lambda res: {
            "class": self.classIndex[res[3]],
            "data": [self.way, self.way, self.positionAsText],
            "text": T_("`{0}` intersects `{1}`", res[4], res[5])
        })
        self.run(sql15, lambda res: {
            "class": self.classIndex[res[3]],
            "data": [self.way, self.way, self.positionAsText],
            "text": T_("`{0}` intersects `{1}`", res[4], res[5])
        })


from .Analyser_Osmosis import TestAnalyserOsmosis

class Test(TestAnalyserOsmosis):
    @classmethod
    def setup_class(cls):
        from modules import config
        TestAnalyserOsmosis.setup_class()
        cls.analyser_conf = cls.load_osm("tests/osmosis_polygon_intersects.osm",
                                         config.dir_tmp + "/tests/osmosis_polygon_intersects.test.xml",
                                         {"proj": 23032})

    def test_classes(self):
        with Analyser_Osmosis_Polygon_Intersects(self.analyser_conf, self.logger) as a:
            a.analyser()

        self.root_err = self.load_errors()
        self.check_err(cl=str(a.classIndex["railway"]), elems=[("way", "1012"), ("way", "1011")])
        self.check_err(cl=str(a.classIndex["aeroway"]), elems=[("way", "1013"), ("way", "1011")])
        self.check_err(cl=str(a.classIndex["highway"]), elems=[("way", "1017"), ("way", "1016")])
        self.check_err(cl=str(a.classIndex["aeroway"]), elems=[("way", "1018"), ("way", "1016")])
        self.check_err(cl=str(a.classIndex["railway"]), elems=[("way", "1019"), ("way", "1016")])
        self.check_err(cl=str(a.classIndex["waterway"]), elems=[("way", "1020"), ("way", "1016")])
        self.check_err(cl=str(a.classIndex["waterway"]), elems=[("way", "1022"), ("way", "1021")])
        self.check_err(cl=str(a.classIndex["railway"]), elems=[("way", "1025"), ("way", "1023")])
        self.check_err(cl=str(a.classIndex["aeroway"]), elems=[("way", "1026"), ("way", "1023")])
        self.check_err(cl=str(a.classIndex["aeroway"]), elems=[("way", "1058"), ("way", "1023")])
        self.check_err(cl=str(a.classIndex["highway"]), elems=[("way", "1027"), ("way", "1023")])
        self.check_err(cl=str(a.classIndex["waterway"]), elems=[("way", "1028"), ("way", "1023")])
        self.check_err(cl=str(a.classIndex["highway"]), elems=[("way", "1036"), ("way", "1035")])
        self.check_err(cl=str(a.classIndex["highway"]), elems=[("way", "1049"), ("way", "1042")])
        self.check_err(cl=str(a.classIndex["highway"]), elems=[("way", "1049"), ("way", "1043")])
        self.check_err(cl=str(a.classIndex["railway"]), elems=[("way", "1050"), ("way", "1047")])
        self.check_err(cl=str(a.classIndex["waterway"]), elems=[("way", "1051"), ("way", "1048")])
        self.check_err(cl=str(a.classIndex["railway"]), elems=[("way", "1055"), ("way", "1052")])
        self.check_num_err(18)
