#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Etienne Chové <chove@crans.org> 2009                       ##
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

from Analyser_Osmosis import Analyser_Osmosis

sql10 = """
SELECT
    id,
    ST_AsText(way_locate(linestring))
FROM
    {0}ways AS ways
WHERE
    tags ? 'junction' AND
    tags->'junction' = 'roundabout' AND
    is_polygon AND
    ST_IsSimple(linestring) AND
    {1} ST_OrderingEquals(ST_Makepolygon(linestring), st_forceRHR(ST_Makepolygon(linestring)))
;
"""

class Analyser_Osmosis_Roundabout_Reverse(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs_change[1] = {"item":"1050", "level": 1, "tag": ["highway", "roundabout", "fix:chair"], "desc": T_(u"Reverse roundabout") } # FIXME "menu":"rond-point à l'envers", "menu":"reverse roundabout"
        self.callback10 = lambda res: {"class":1, "data":[self.way_full, self.positionAsText]}
        if self.config.options.get("driving_side") == "left":
            self.driving_side = "NOT "
        else:
            self.driving_side = ""

    def analyser_osmosis_all(self):
        self.run(sql10.format("", self.driving_side), self.callback10)

    def analyser_osmosis_touched(self):
        self.run(sql10.format("touched_", self.driving_side), self.callback10)

###########################################################################

from Analyser_Osmosis import TestAnalyserOsmosis

class Test(TestAnalyserOsmosis):
    @classmethod
    def setup_class(cls):
        TestAnalyserOsmosis.setup_class()
        cls.analyser_conf = cls.load_osm("tests/osmosis_roundabout_reverse.test.osm",
                                         "tests/out/osmosis_roundabout_reverse.test.xml",
                                         {"driving_side": "left"})

    def test_left(self):
        self.analyser_conf.options["driving_side"] = "left"
        with Analyser_Osmosis_Roundabout_Reverse(self.analyser_conf, self.logger) as a:
            a.analyser()

        self.compare_results("tests/results/osmosis_roundabout_reverse.test.left.osm")

        self.root_err = self.load_errors()
        self.check_err(cl="1", lat="43.9535032231925", lon="6.36996821091771", elems=[("way", "2")])
        self.check_num_err(1)

    def test_right(self):
        self.analyser_conf.options["driving_side"] = "right"
        with Analyser_Osmosis_Roundabout_Reverse(self.analyser_conf, self.logger) as a:
            a.analyser()

        self.compare_results("tests/results/osmosis_roundabout_reverse.test.right.osm")

        self.root_err = self.load_errors()
        self.check_err(cl="1", lat="43.9533100018163", lon="6.36976238744323", elems=[("way", "1")])
        self.check_num_err(1)
