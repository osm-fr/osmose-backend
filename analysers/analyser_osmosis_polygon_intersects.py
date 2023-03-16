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
    level <= 3
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
        tags->'waterway' IN ('river', 'canal') AND -- big waterways
        (NOT tags?'seasonal' OR tags->'seasonal' = 'no') AND
        (NOT tags?'intermittent' OR tags->'intermittent' = 'no')
      ) OR (
        tags?'aeroway' AND
        tags->'aeroway' IN ('apron', 'helipad', 'runway', 'taxilane', 'taxiway') -- aircraft moving places
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
SELECT
  mobility_ways.id,
  ways.id,
  ST_AsText(ST_Centroid(ST_Intersection(ST_MakePolygon(ways.linestring), mobility_ways.linestring))),
  mobility_ways.type,
  CONCAT(mobility_ways.type, '=', mobility_ways.tags->mobility_ways.type),
  CASE
    WHEN ways.tags?'landuse' THEN CONCAT('landuse=', ways.tags->'landuse')
    WHEN ways.tags?'natural' THEN CONCAT('natural=', ways.tags->'natural')
  END
FROM
  mobility_ways
  JOIN ways ON
    ways.is_polygon AND
    ways.tags != ''::hstore AND
    (
      (
        --ways.tags?'landuse' (...) sometimes causes bad route
        (
          ways.tags?'landuse' AND
          ways.tags->'landuse' NOT IN ('basin', 'civic_admin', 'commercial', 'construction', 'education', 'grass', 'harbour', 'industrial', 'military', 'port', 'proposed', 'railway', 'recreation_ground', 'religious', 'reservoir', 'residential', 'retail', 'salt_pond', 'winter_sports')
        ) OR (
          ways.tags->'landuse' = 'grass' AND
          mobility_ways.type = 'waterway'
        ) OR (
          ways.tags->'landuse' IN ('basin', 'reservoir', 'recreation_ground', 'salt_pond') AND
          mobility_ways.type != 'waterway'
        )
      ) OR (
        --ways.tags?'natural' (...) sometimes causes bad route
        ways.tags->'natural' IN ('cliff', 'scrub', 'shrubbery', 'sinkhole', 'tree_group', 'wood') OR
        (
          ways.tags->'natural' IN ('bay', 'water', 'wetland') AND
          mobility_ways.type != 'waterway' AND
          mobility_ways.type != 'highway' --Caught by item 1070 class 4/5
        )
      )
    ) AND
    (
      NOT ways.tags?'layer' AND NOT mobility_ways.tags?'layer' OR
      (
        ways.tags?'layer' AND mobility_ways.tags?'layer' AND
        ways.tags->'layer' = mobility_ways.tags->'layer'
      )
    ) AND
    ways.linestring && mobility_ways.linestring AND
    -- Only find ways where the highway/railway/waterway/aeroway actually enters the
    -- polygon. Exclude cases where the polygon is tied to the way without going inside.
    ST_Intersects(ST_MakePolygon(ways.linestring), mobility_ways.linestring) AND
    NOT ST_Touches(ST_MakePolygon(ways.linestring), mobility_ways.linestring) AND
    (
      -- Ignore very minor overlaps. The distance between the center of the overlap and one of the ways must be at least 1m
      ST_Distance(ST_Centroid(ST_Transform(ST_Intersection(ST_MakePolygon(ways.linestring), mobility_ways.linestring), {proj})), ST_Transform(mobility_ways.linestring, {proj})) > 1 OR
      ST_Distance(ST_Centroid(ST_Transform(ST_Intersection(ST_MakePolygon(ways.linestring), mobility_ways.linestring), {proj})), ST_Transform(ways.linestring, {proj})) > 1
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
        self.run(sql11.format(proj=self.config.options["proj"]), lambda res: {
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
        self.check_err(cl=str(a.classIndex["highway"]), elems=[("way", "1027"), ("way", "1023")])
        self.check_err(cl=str(a.classIndex["waterway"]), elems=[("way", "1028"), ("way", "1023")])
        self.check_err(cl=str(a.classIndex["highway"]), elems=[("way", "1036"), ("way", "1035")])
        self.check_num_err(12)
