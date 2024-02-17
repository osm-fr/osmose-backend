#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Osmose Project 2023                                        ##
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
CREATE TEMP TABLE poly_landuse AS
SELECT
  type_id,
  poly_proj,
  tags->'landuse' AS landuse
FROM (
  SELECT
    'W' || id AS type_id,
    tags,
    ST_Transform(ST_MakePolygon(ways.linestring), {proj}) AS poly_proj
  FROM
    ways
  WHERE
    is_polygon AND
    tags != ''::hstore
  UNION ALL
  SELECT
    'R' || id AS type_id,
    tags,
    poly_proj
  FROM
    multipolygons
  WHERE
    is_valid
) AS t
WHERE
  tags?'landuse' AND
  tags->'landuse' IN ('farmland', 'vineyard', 'orchard', 'plant_nursery')
"""

sql11 = """
SELECT DISTINCT ON (poly_landuse.type_id)
  poly_landuse.type_id,
  buildings.id,
  -- Use the building location to point out the error, even though the landuse should be changed
  ST_AsText(way_locate(buildings.linestring)),
  buildings.tags->'building',
  poly_landuse.landuse
FROM
  buildings
  JOIN poly_landuse ON
    ST_Contains(poly_landuse.poly_proj, buildings.polygon_proj)
WHERE
  -- ignore e.g. small utility buildings that happen to be on the farmland or are fully surrounded by farmland
  buildings.area > 36 AND
  (NOT buildings.tags?'location' OR buildings.tags->'location' != 'underground')
ORDER BY
  poly_landuse.type_id,
  buildings.area DESC
"""


class Analyser_Osmosis_Building_In_Polygon(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        if not "proj" in self.config.options:
            return

        self.classs[1] = self.def_class(item = 1310, level = 3, tags = ['landuse', 'fix:chair'],
            title = T_('Building on agricultural land'),
            detail = T_(
'''Buildings of a farm (houses, sheds, stables, barns, ...) are usually located on the farmyard,
not on the farmland where the crops grow.'''),
            fix = T_(
'''Change or split the landuse such that the farm buildings are on an area with `landuse=farmyard`
and the area where crops grow are within `landuse=farmland` (or more dedicated types of farmland,
such as `landuse=vineyard` or `landuse=orchard`).

For areas dedicated to greenhouse horticulture, use `landuse=greenhouse_horticulture`.'''),
            resource = "https://wiki.openstreetmap.org/wiki/Tag:landuse%3Dfarmland")

    requires_tables_common = ['buildings', 'multipolygons']

    def analyser_osmosis_common(self):
        self.run(sql10.format(proj=self.config.options["proj"]))
        self.run(sql11, lambda res: {
            "class": 1,
            "data": [self.any_full, self.way, self.positionAsText],
            "text": T_("`{0}` inside `{1}`", "building=" + res[3], 'landuse=' + res[4])
        })

from .Analyser_Osmosis import TestAnalyserOsmosis

class Test(TestAnalyserOsmosis):
    @classmethod
    def setup_class(cls):
        from modules import config
        TestAnalyserOsmosis.setup_class()
        cls.analyser_conf = cls.load_osm("tests/osmosis_building_in_polygon.osm",
                                         config.dir_tmp + "/tests/osmosis_building_in_polygon.test.xml",
                                         {"proj": 23032})

    def test_classes(self):
        with Analyser_Osmosis_Building_In_Polygon(self.analyser_conf, self.logger) as a:
            a.analyser()

        self.root_err = self.load_errors()
        self.check_err(cl="1", elems=[("way", "100"), ("way", "101")])
        self.check_err(cl="1", elems=[("relation", "1000"), ("way", "107")])
        self.check_num_err(2)
