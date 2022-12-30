#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Osmose Project 2022                                        ##
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
  id,
  ST_AsText(way_locate(ways.linestring))
FROM
  {touched}ways AS ways
WHERE
  ways.is_polygon AND
  ways.tags != ''::hstore AND
  ways.tags?'{key}' AND
  ways.tags->'{key}' = '{val}' AND
  ST_Area(ST_MakePolygon(ST_Transform(ways.linestring, {proj}))) < {minarea}
"""


class Analyser_Osmosis_Geometry_Small(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        if "proj" in self.config.options:
            self.proj = self.config.options["proj"]
        else:
            return

        self.classs_change[1] = self.def_class(item = 1310, level = 3, tags = ['natural', 'fix:chair'],
            title = T_('Natural area too small'),
            detail = T_(
'''A natural object of this type is typically larger than the current object.'''),
            example = T_(
'''A single tree should be tagged as `natural=tree` rather than `natural=wood`.'''))
        self.classs_change[2] = self.def_class(item = 1310, level = 3, tags = ['landuse', 'fix:chair'],
            title = T_('Natural area too small'),
            detail = T_(
'''Landuses of this type are typically larger than the current object.'''),
            example = T_(
'''A single tree should be tagged as `natural=tree` rather than `landuse=forest`.'''))

        self.checks = [
            # Objects to be checked. Requires: key, val(ue) of tag, min(imum)area (in m2) of the object, and class nr
            {'key': 'natural', 'val': 'wood', 'minarea': 20, 'class': 1}, # 20m2 is roughly 1 big tree of 5m diameter
            {'key': 'landuse', 'val': 'forest', 'minarea': 20, 'class': 2}, # 20m2 is roughly 1 big tree of 5m diameter
        ]

    def analyser_osmosis_full(self):
        for item in self.checks:
            self.run(sql10.format(key=item["key"], val=item["val"], minarea=item["minarea"], proj=self.proj, touched=""), lambda res: {
                "class": item["class"],
                "data": [self.way_full, self.positionAsText]
            })

    def analyser_osmosis_diff(self):
        for item in self.checks:
            self.run(sql10.format(key=item["key"], val=item["val"], minarea=item["minarea"], proj=self.proj, touched='touched_'), lambda res: {
                "class": item["class"],
                "data": [self.way_full, self.positionAsText]
            })

from .Analyser_Osmosis import TestAnalyserOsmosis

class Test(TestAnalyserOsmosis):
    @classmethod
    def setup_class(cls):
        from modules import config
        TestAnalyserOsmosis.setup_class()
        cls.analyser_conf = cls.load_osm("tests/osmosis_geometry_small.osm",
                                         config.dir_tmp + "/tests/osmosis_geometry_small.test.xml",
                                         {"proj": 23032})

    def test_classes(self):
        with Analyser_Osmosis_Geometry_Small(self.analyser_conf, self.logger) as a:
            a.analyser()

        self.root_err = self.load_errors()
        self.check_err(cl="1", elems=[("way", "100")])
        self.check_num_err(1)
