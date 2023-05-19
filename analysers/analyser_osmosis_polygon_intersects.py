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
-- Collect all major highways, railways and aeroways
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
-- Collect all landuse=* and natural=*, closed ways and multipolygons
CREATE TEMP TABLE landusage AS
SELECT
  'W' || id AS id,
  ST_Transform(linestring, {proj}) AS linestring_proj,
  ST_MakePolygon(linestring) AS poly,
  CASE
    WHEN tags?'landuse' THEN 'landuse'
    WHEN tags?'natural' THEN 'natural'
  END AS landusekey,
  CASE
    WHEN tags?'landuse' THEN tags->'landuse'
    WHEN tags?'natural' THEN tags->'natural'
  END AS landusevalue,
  tags
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
  'R' || mp.id AS id,
  ST_Transform(ST_LineMerge(ST_Collect(ways.linestring)), {proj}) AS linestring_proj, -- usually multilinestring
  mp.poly,
  CASE
    WHEN mp.tags?'landuse' THEN 'landuse'
    WHEN mp.tags?'natural' THEN 'natural'
  END AS landusekey,
  CASE
    WHEN mp.tags?'landuse' THEN mp.tags->'landuse'
    WHEN mp.tags?'natural' THEN mp.tags->'natural'
  END AS landusevalue,
  mp.tags
FROM
  multipolygons AS mp
  JOIN relation_members ON
    relation_id = mp.id
  JOIN ways ON
    member_role IN ('outer', 'inner') AND
    member_id = ways.id AND
    member_type = 'W'
WHERE
  mp.is_valid AND
  (mp.tags?'natural' OR mp.tags?'landuse')
GROUP BY
  mp.id,
  mp.poly,
  mp.tags
"""

sql12 = """
CREATE INDEX idx_mobilityway_linestring ON mobility_ways USING GIST(linestring);
CREATE INDEX idx_landusage_poly ON landusage USING GIST(poly);
"""

sql13 = """
-- Collect highway|railway|aeroways either entering or fully inside landuse/natural geometries
CREATE TEMP TABLE intersecting_geometries AS
SELECT
  mobility_way_id,
  mobility_way_linestring,
  mobility_way_type,
  landusage_id,
  landusage_poly,
  landusekey,
  landusevalue,
  tag_way,
  CONCAT(landusekey, '=', landusevalue) AS tag_polygon
FROM (
  SELECT
    mobility_ways.id AS mobility_way_id,
    mobility_ways.linestring AS mobility_way_linestring,
    mobility_ways.type AS mobility_way_type,
    landusage.id AS landusage_id,
    landusage.poly AS landusage_poly,
    landusage.linestring_proj AS landusage_linestring_proj,
    landusage.landusekey,
    landusage.landusevalue,
    CONCAT(mobility_ways.type, '=', mobility_ways.tags->mobility_ways.type) AS tag_way,
    (ST_Dump(ST_Transform(ST_Intersection(landusage.poly, mobility_ways.linestring), {proj}))).geom AS intersection_part_geom_proj
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
      landusage.poly && mobility_ways.linestring AND
      -- Only find ways where the highway/railway/aeroway actually enters the
      -- polygon. Exclude cases where the polygon is tied to the way without going inside.
      (
        ST_Crosses(landusage.poly, mobility_ways.linestring) OR
        ST_Contains(landusage.poly, mobility_ways.linestring)
      )
  ) AS t
WHERE
  -- Only include significant intersections
  ST_Length(intersection_part_geom_proj) > 2 AND
  (
    ST_Distance(ST_Centroid(intersection_part_geom_proj), ST_Transform(mobility_way_linestring, {proj})) > 1 OR
    ST_Distance(ST_Centroid(intersection_part_geom_proj), landusage_linestring_proj) > 1
  )
"""

sql14 = """
-- Intersections with railway, aeroway or highway
SELECT
  DISTINCT ON (mobility_way_id, landusage_id)
  mobility_way_id,
  landusage_id,
  ST_AsText(ST_PointOnSurface(ST_Intersection(landusage_poly, mobility_way_linestring))),
  mobility_way_type,
  tag_way,
  tag_polygon
FROM
  intersecting_geometries
WHERE
  (
    landusekey = 'landuse' AND
    landusevalue NOT IN ('civic_admin', 'commercial', 'construction', 'education', 'grass', 'harbour', 'industrial', 'military', 'port', 'proposed', 'quarry', 'railway', 'religious', 'residential', 'retail', 'winter_sports')
  ) OR (
    landusekey = 'natural' AND
    landusevalue IN ('bay', 'cliff', 'scrub', 'shrubbery', 'sinkhole', 'tree_group', 'wetland', 'wood') OR
    (
      -- Special case as highway=* vs. natural=water is already included in item 1070 class 4/5
      landusevalue = 'water' AND
      mobility_way_type != 'highway'
    )
  )
ORDER BY
  mobility_way_id,
  landusage_id,
  mobility_way_type,
  tag_way,
  tag_polygon
"""

class Analyser_Osmosis_Polygon_Intersects(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        if not "proj" in self.config.options:
            return

        self.classIndex = {'highway': 12, 'railway': 13, 'aeroway': 15}

        detailTxt = T_(
'''A way meant for transport (such as a highway or a railway) intersects with a
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
        self.classs[self.classIndex["aeroway"]] = self.def_class(
            item = 1070, level = 2, tags = ['landuse', 'fix:chair'],
            title = T_('Bad intersection with aeroway'),
            detail = detailTxt, example = exampleTxt, fix = fixTxt)

    requires_tables_common = ['highways', 'multipolygons']

    def analyser_osmosis_common(self):
        self.run(sql10)
        self.run(sql11.format(proj=self.config.options["proj"]))
        self.run(sql12)
        self.run(sql13.format(proj=self.config.options["proj"]))
        self.run(sql14, lambda res: {
            "class": self.classIndex[res[3]],
            "data": [self.way, self.any_id, self.positionAsText],
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
        self.check_err(cl=str(a.classIndex["railway"]), elems=[("way", "1025"), ("way", "1023")])
        self.check_err(cl=str(a.classIndex["aeroway"]), elems=[("way", "1026"), ("way", "1023")])
        self.check_err(cl=str(a.classIndex["aeroway"]), elems=[("way", "1058"), ("way", "1023")])
        self.check_err(cl=str(a.classIndex["highway"]), elems=[("way", "1027"), ("way", "1023")])
        self.check_err(cl=str(a.classIndex["highway"]), elems=[("way", "1036"), ("way", "1035")])
        self.check_err(cl=str(a.classIndex["highway"]), elems=[("way", "1049"), ("relation", "10002")])
        self.check_err(cl=str(a.classIndex["railway"]), elems=[("way", "1050"), ("relation", "10001")])
        self.check_err(cl=str(a.classIndex["railway"]), elems=[("way", "1063"), ("relation", "10001")])
        self.check_err(cl=str(a.classIndex["aeroway"]), elems=[("way", "1064"), ("relation", "10001")])
        self.check_err(cl=str(a.classIndex["railway"]), elems=[("way", "1055"), ("relation", "10003")])
        self.check_err(cl=str(a.classIndex["highway"]), elems=[("way", "1062"), ("way", "1059")])
        self.check_num_err(16)
