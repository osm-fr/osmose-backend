#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2019                                      ##
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


sql01 = """
CREATE TEMP TABLE camp_sites AS
SELECT
    ST_MakePolygon(linestring) AS poly
FROM
    ways
WHERE
    tags != ''::hstore AND
    tags?'tourism' AND
    tags->'tourism' IN ('camp_site', 'caravan_site') AND
    is_polygon
UNION ALL
SELECT
    poly
FROM
    multipolygons
WHERE
    tags?'tourism' AND
    tags->'tourism' IN ('camp_site', 'caravan_site') AND
    is_valid
"""

sql02 = """
CREATE INDEX idx_camp_sites_poly ON camp_sites USING GIST(poly);
"""

sql10 = """
SELECT
  pitch.id,
  ST_AsText(way_locate(pitch.linestring))
FROM
  ways AS pitch
  LEFT JOIN camp_sites ON
    ST_Covers(camp_sites.poly, pitch.linestring)
WHERE
  pitch.tags != ''::hstore AND
  pitch.tags ?| ARRAY['tourism', 'camp_site'] AND
  (pitch.tags->'tourism' = 'camp_pitch' OR pitch.tags->'camp_site' IN ('camp_pitch', 'pitch')) AND
  camp_sites IS NULL
"""

sql11 = """
SELECT
  pitch.id,
  ST_AsText(pitch.geom)
FROM
  nodes AS pitch
  LEFT JOIN camp_sites ON
    ST_Covers(camp_sites.poly, pitch.geom)
WHERE
  pitch.tags != ''::hstore AND
  pitch.tags ?| ARRAY['tourism', 'camp_site'] AND
  (pitch.tags->'tourism' = 'camp_pitch' OR pitch.tags->'camp_site' IN ('camp_pitch', 'pitch')) AND
  camp_sites IS NULL
"""

class Analyser_Osmosis_Camp_Pitch_Out_Of_Camp_Site(Analyser_Osmosis):

    requires_tables_common = ['multipolygons']

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        if not "proj" in self.config.options:
            return
        self.classs[1] = self.def_class(item = 1290, level = 2, tags = ['geom', 'fix:chair'],
          title = T_('Camp pitches outside a camp site'))

    def analyser_osmosis_common(self):
        self.run(sql01)
        self.run(sql02)
        self.run(sql10, lambda res: {"class":1, "subclass":1, "data":[self.way_full, self.positionAsText]})
        self.run(sql11, lambda res: {"class":1, "subclass":2, "data":[self.node_full, self.positionAsText]})

from .Analyser_Osmosis import TestAnalyserOsmosis

class Test(TestAnalyserOsmosis):
    @classmethod
    def setup_class(cls):
        from modules import config
        TestAnalyserOsmosis.setup_class()
        cls.analyser_conf = cls.load_osm("tests/osmosis_camp_pitch_outside_site.osm",
                                         config.dir_tmp + "/tests/osmosis_camp_pitch_outside_site.test.xml",
                                         {"proj": 23032})

    def test(self):
        with Analyser_Osmosis_Camp_Pitch_Out_Of_Camp_Site(self.analyser_conf, self.logger) as a:
            a.analyser()

        self.root_err = self.load_errors()
        self.check_err(cl="1", elems=[("way", "105")])
        self.check_err(cl="1", elems=[("node", "8")])
        self.check_num_err(2)
