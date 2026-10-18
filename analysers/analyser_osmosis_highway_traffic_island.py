#!/usr/bin/env python
###########################################################################
##                                                                       ##
## Copyright Osmose Contributors 2026                                    ##
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
SELECT DISTINCT ON (crossing.id)
    crossing.id,
    traffic_island.id,
    ST_AsText(way_locate(crossing.linestring))
FROM
    {0}highways AS crossing
    JOIN {1}highways AS traffic_island ON
        traffic_island.linestring && crossing.linestring AND
        traffic_island.id != crossing.id AND
        traffic_island.nodes && crossing.nodes AND
        traffic_island.tags != ''::hstore AND
        traffic_island.tags?'footway' AND
        traffic_island.tags->'footway' = 'traffic_island'
WHERE
    crossing.tags != ''::hstore AND
    crossing.tags?'crossing:island' AND
    crossing.tags->'crossing:island' = 'yes' AND
    crossing.tags?|ARRAY['footway', 'cycleway', 'path'] AND
    (
        crossing.tags->'footway' = 'crossing' OR
        crossing.tags->'cycleway' = 'crossing' OR
        crossing.tags->'path' = 'crossing'
    )
ORDER BY
    crossing.id,
    traffic_island.id
"""


class Analyser_Osmosis_Highway_Traffic_Island(Analyser_Osmosis):

    requires_tables_common = ['highways']
    requires_tables_diff = ['touched_highways', 'not_touched_highways']

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs_change[1] = self.def_class(item = 3040, level = 3, tags = ['tag', 'highway', 'footway', 'fix:survey'],
            title = T_('Crossing island tag on a split crossing'),
            detail = T_(
'''A crossing way is tagged with `crossing:island=yes` and connects to a
separately mapped `footway=traffic_island`.

When a traffic island is mapped as its own way, the crossing ways leading
to it usually should not also be tagged as having a crossing island.'''),
            fix = T_(
'''Check the highlighted crossing way. If it is a segment leading to
the separately mapped traffic island, remove `crossing:island=yes`. You may add
`crossing:island=no` for clarity.

If the crossing way continues all the way across the street and over the island
as one continuous crossing, keep `crossing:island=yes`.'''),
            trap = T_(
'''If you are not sure whether the crossing way ends at the island or continues
over it, do not change the tag.'''))

        self.callback10 = lambda res: {"class": 1, "data": [self.way_full, self.way_full, self.positionAsText]}

    def analyser_osmosis_full(self):
        self.run(sql10.format("", ""), self.callback10)

    def analyser_osmosis_diff(self):
        # Match issues when either the crossing way or the traffic island way is touched.
        # touched_highways and not_touched_highways views are created by requires_tables_build.
        self.run(sql10.format("touched_", ""), self.callback10)
        self.run(sql10.format("not_touched_", "touched_"), self.callback10)


###########################################################################

from .Analyser_Osmosis import TestAnalyserOsmosis


class Test(TestAnalyserOsmosis):
    @classmethod
    def setup_class(cls):
        from modules import config
        TestAnalyserOsmosis.setup_class()
        cls.analyser_conf = cls.load_osm("tests/osmosis_highway_traffic_island.osm",
                                         config.dir_tmp + "/tests/osmosis_highway_traffic_island.test.xml",
                                         {"proj": 2154})

    def test_classes(self):
        with Analyser_Osmosis_Highway_Traffic_Island(self.analyser_conf, self.logger) as a:
            a.analyser()

        self.root_err = self.load_errors()
        self.check_err(cl="1", elems=[("way", "100"), ("way", "200")])
        self.check_err(cl="1", elems=[("way", "110"), ("way", "210")])
        self.check_err(cl="1", elems=[("way", "120"), ("way", "220")])
        self.check_num_err(3)
