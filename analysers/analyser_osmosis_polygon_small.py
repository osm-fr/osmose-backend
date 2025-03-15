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
  'W' || id,
  ST_AsText(way_locate(linestring)),
  ST_Area(ST_MakePolygon(ST_Transform(linestring, {proj})))
FROM
  {touched}ways
WHERE
  is_polygon AND
  tags != ''::hstore AND
  tags?'{key}' AND
  tags->'{key}' = '{val}' AND
  ST_Area(ST_MakePolygon(ST_Transform(linestring, {proj}))) < {minarea}

UNION ALL

SELECT
  'R' || id,
  ST_AsText(polygon_locate(poly)),
  ST_Area(poly_proj)
FROM
  {touched}multipolygons
WHERE
  is_valid AND
  tags?'{key}' AND
  tags->'{key}' = '{val}' AND
  ST_Area(poly_proj) < {minarea}
"""


class Analyser_Osmosis_Polygon_Small(Analyser_Osmosis):

    requires_tables_full = ['multipolygons']
    requires_tables_diff = ['touched_multipolygons']

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        if "proj" in self.config.options:
            self.proj = self.config.options["proj"]
        else:
            return

        trapmsg = T_('''
Sometimes very small areas of this type may exist. In this case, please mark this issue as a false positive.''')

        self.classs_change[1] = self.def_class(item = 3100, level = 3, tags = ['natural', 'fix:chair'],
            title = T_('Natural area very small'),
            detail = T_(
'''A natural object of this type is typically larger than the current object.'''),
            example = T_(
'''A single tree should be tagged as `natural=tree` rather than `landuse=forest` or `natural=wood`.'''),
            trap = trapmsg)
        self.classs_change[2] = self.def_class(item = 3100, level = 3, tags = ['landuse', 'fix:chair'],
            title = T_('Landuse very small'),
            detail = T_(
'''Landuses of this type are typically larger than the current object.'''),
            example = T_(
'''A single tree should be tagged as `natural=tree` rather than `landuse=forest` or `natural=wood`.'''),
            trap = trapmsg)
        self.classs_change[3] = self.def_class(item = 3100, level = 3, tags = ['landuse', 'fix:chair'],
            title = T_('Small farm'),
            detail = T_(
'''Landuses of this type are typically larger than the current object.'''),
            example = T_(
'''Agricultural land that is used for barns, greenhouses, for cattle to graze, etcetera, should not be tagged as `landuse=farmland`.
The tag `landuse=farmland` is meant for land where i.e. crops are grown.
Other landuses could be tagged with:
- `{0}`
- etcetera.''', '`,\n- `'.join(('building=farm_auxiliary', 'building=farm', 'landuse=farmyard', 'landuse=allotments', 'building=barn', 'building=sty', 'building=cowshed', 'building=stable', 'building=greenhouse', 'landuse=greenhouse_horticulture', 'landuse=meadow'))),
            trap = trapmsg)
        self.classs_change[4] = self.def_class(item = 3100, level = 3, tags = ['landuse', 'fix:chair'],
            title = T_('Landuse very small'),
            detail = T_(
'''Landuses of this type are typically larger than the current object.'''),
            example = T_(
'''Small patches of maintained vegetation should be tagged as any of `{0}`, (etcetera) rather than `landuse=village_green`.''',
'`, `'.join(('natural=shrubbery', 'landuse=grass', 'natural=scrub', 'leisure=garden', 'landuse=flowerbed'))),
            trap = trapmsg)
        self.classs_change[5] = self.def_class(item = 3100, level = 3, tags = ['leisure', 'fix:chair'],
            title = T_('Leisure very small'),
            detail = T_(
'''Leisures of this type are typically larger than the current object.'''),
            example = T_(
'''Small individual patches of vegetation should be tagged as `{0}`, (etcetera) rather than `leisure=park`.
Usually a park contains grass, other vegetation, walking paths. A park often has a name.''',
'`, `'.join(('landuse=grass', 'natural=shrubbery', 'landuse=flowerbed'))),
            trap = trapmsg)

        self.checks = [
            # Objects to be checked. Requires: key, val(ue) of tag, min(imum)area (in m2) of the object, and class
            {'key': 'natural', 'val': 'wood', 'minarea': 20, 'class': 1}, # 20m2 is roughly 1 big tree of 5m diameter
            {'key': 'landuse', 'val': 'forest', 'minarea': 20, 'class': 2}, # 20m2 is roughly 1 big tree of 5m diameter
            {'key': 'landuse', 'val': 'farmland', 'minarea': 100, 'class': 3},
            {'key': 'landuse', 'val': 'village_green', 'minarea': 500, 'class': 4},
            {'key': 'leisure', 'val': 'park', 'minarea': 25, 'class': 5},
        ]

    def analyser_osmosis_full(self):
        for item in self.checks:
            self.run(sql10.format(key=item["key"], val=item["val"], minarea=item["minarea"], proj=self.proj, touched=""), lambda res: {
                "class": item["class"],
                "data": [self.any_full, self.positionAsText],
                "text": T_("{0} with an area of {1} m2", "`{0}={1}`".format(item["key"], item["val"]), round(res[2]))
            })

    def analyser_osmosis_diff(self):
        for item in self.checks:
            self.run(sql10.format(key=item["key"], val=item["val"], minarea=item["minarea"], proj=self.proj, touched='touched_'), lambda res: {
                "class": item["class"],
                "data": [self.any_full, self.positionAsText],
                "text": T_("{0} with an area of {1} m2", "`{0}={1}`".format(item["key"], item["val"]), round(res[2]))
            })

from .Analyser_Osmosis import TestAnalyserOsmosis

class Test(TestAnalyserOsmosis):
    @classmethod
    def setup_class(cls):
        from modules import config
        TestAnalyserOsmosis.setup_class()
        cls.analyser_conf = cls.load_osm("tests/osmosis_polygon_small.osm",
                                         config.dir_tmp + "/tests/osmosis_polygon_small.test.xml",
                                         {"proj": 23032})

    def test_classes(self):
        with Analyser_Osmosis_Polygon_Small(self.analyser_conf, self.logger) as a:
            a.analyser()

        self.root_err = self.load_errors()
        self.check_err(cl="1", elems=[("way", "100")])
        self.check_err(cl="3", elems=[("relation", "1000")])
        self.check_err(cl="3", elems=[("relation", "1001")])
        self.check_num_err(3)
