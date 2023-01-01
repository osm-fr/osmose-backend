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
SELECT
  DISTINCT ON (ways.id)
  ways.id,
  buildings.id,
  -- Use the building location to point out the error, even though the landuse should be changed
  ST_AsText(way_locate(buildings.linestring)),
  buildings.tags->'building',
  ways.tags->'landuse'
FROM
  buildings
  JOIN ways ON
    ways.is_polygon AND
    ways.tags != ''::hstore AND
    ways.tags?'landuse' AND
    ways.tags->'landuse' IN ('farmland', 'vineyard', 'orchard') AND
    ways.linestring && buildings.linestring AND
    ST_Contains(ST_Transform(ST_MakePolygon(ways.linestring), {proj}), buildings.polygon_proj)
WHERE
  -- ignore e.g. small utility buildings that happen to be on the farmland or are fully surrounded by farmland
  buildings.area > 36 AND
  (NOT buildings.tags?'location' OR buildings.tags->'location' != 'underground')
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
'''Change or split the landuse way such that the farm buildings are on an area with `landuse=farmyard`
and the area where crops grow are within `landuse=farmland`.

For areas dedicated to greenhouse horticulture, use `landuse=greenhouse_horticulture`.'''))

    requires_tables_common = ['buildings']

    def analyser_osmosis_common(self):
        self.run(sql10.format(proj=self.config.options["proj"]), lambda res: {
            "class": 1,
            "data": [self.way_full, self.way, self.positionAsText],
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
        self.check_num_err(1)
