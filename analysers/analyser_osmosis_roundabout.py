#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Etienne Chové <chove@crans.org> 2010                       ##
##            Frédéric Rodrigo 2010-2015                                 ##
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

sql10 = u"""
SELECT
    ways.id,
    ST_AsText(way_locate(ways.linestring)) AS geom
FROM
    {1}highways AS ways
    JOIN {2}highways AS conns ON
        conns.linestring && ways.linestring AND
        conns.nodes && ways.nodes AND
        conns.id != ways.id AND
        conns.level < 5 AND -- it's a car road
        NOT conns.is_area AND
        NOT conns.is_construction
WHERE
    -- tags
    ways.level < 5 AND -- it's a car road
    NOT ways.is_roundabout AND
    NOT ways.is_area AND
    NOT ways.is_construction AND
    (NOT ways.tags?'name' OR ways.tags->'name' LIKE 'Rond%' OR ways.tags->'name' LIKE 'Giratoire%') AND -- no name or start with 'Rond' or 'Giratoire' (French)
    ways.is_oneway AND
    NOT ways.tags?'junction' AND
    -- geometry
    ways.is_polygon AND -- It's a polygon
    ST_NPoints(ways.linestring) < 24 AND
    ST_MaxDistance(ST_Transform(ways.linestring,{0}),ST_Transform(ways.linestring,{0})) < 70 AND -- The way diameter is less than 70m
    ST_Area(ST_MakePolygon(ST_Transform(ways.linestring,{0})))/ST_Area(ST_MinimumBoundingCircle(ST_Transform(ways.linestring,{0}))) > 0.6 -- 90% of roundabout covert more than 60% bounding circle
GROUP BY
    ways.id,
    geom
HAVING
    COUNT(*) >= 2 -- select roundabout at least connected with two other ways
"""


sql20 = """
SELECT
  roundabouts.id,
  nodes.id,
  ST_AsText(nodes.geom)
FROM
  highways AS roundabouts
  JOIN nodes ON
    roundabouts.linestring && nodes.geom AND
    nodes.id = ANY(roundabouts.nodes) AND
    nodes.tags != ''::hstore AND
    nodes.tags?'highway' AND nodes.tags->'highway' IN ('traffic_signals', 'give_way', 'stop') AND -- "yield-nodes"
    (-- tolerate rarely-red traffic_signals such as emergency, blink_mode, continuous_green, ...
      NOT nodes.tags?'traffic_signals' OR
      nodes.tags->'traffic_signals' IN ('signal', 'traffic_lights', 'stop', 'pedestrian_crossing', 'cyclist_crossing')
    )
WHERE
  roundabouts.is_roundabout
"""

class Analyser_Osmosis_Roundabout(Analyser_Osmosis):

    requires_tables_full = ['highways']
    requires_tables_diff = ['highways', 'touched_highways', 'not_touched_highways']

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        if not "proj" in self.config.options:
            return
        self.classs_change[1] = self.def_class(item = 2010, level = 1, tags = ['highway', 'roundabout', 'fix:imagery'],
            title = T_('Missing `junction=roundabout`'),
            detail = T_(
'''This looks like a roundabout, but the tag `junction=roundabout` is not
present. See [Roundabout](https://wiki.openstreetmap.org/wiki/Roundabout)
for more info.'''),
            fix = T_(
'''If it is really a roundabout, add the tag `junction=roundabout`,
verify that the way direction is counter-clockwise when the driving side is
on the right, and remove the tag `oneway=yes` if present.'''),
            trap = T_(
'''Ensure that it is a roundabout, using satellite imagery or a local
survey.
Ensure the traffic on the roundabout has right of way. If not, use `junction=circular` instead.'''))
        self.classs[2] = self.def_class(item = 2010, level = 2, tags = ['highway', 'roundabout', 'fix:imagery'],
            title = T_('Roundabout without right of way'),
            detail = T_(
'''A highway with `junction=roundabout` must by definition have the right of way.
Circular highways without right of way should be tagged as `junction=circular`.'''),
            fix = T_(
'''Replace `junction=roundabout` on the entire circular road with `junction=circular`.
If the node with `highway=traffic_signals`, `give_way` or `stop` is actually for the road entering the roundabout, tag it on that way only.'''),
            trap = T_(
'''Make sure to tag `oneway=*` when using `junction=circular`. Unlike `junction=roundabout`, `junction=circular` does not imply `oneway=yes`.'''),
            resource = "https://wiki.openstreetmap.org/wiki/Tag:junction%3Dcircular")

        self.callback10 = lambda res: {"class":1, "data":[self.way_full, self.positionAsText], "fix":{"+":{"junction":"roundabout"}} }

    def analyser_osmosis_full(self):
        self.run(sql10.format(self.config.options.get("proj"), "", ""), self.callback10)

    def analyser_osmosis_diff(self):
        self.run(sql10.format(self.config.options.get("proj"), "touched_", ""), self.callback10)
        self.run(sql10.format(self.config.options.get("proj"), "not_touched_", "touched_"), self.callback10)

    def analyser_osmosis_common(self):
        self.run(sql20, lambda res: {"class":2, "data":[self.way_full, self.node_full, self.positionAsText]})



###########################################################################

from .Analyser_Osmosis import TestAnalyserOsmosis

class Test(TestAnalyserOsmosis):
    @classmethod
    def setup_class(cls):
        from modules import config
        TestAnalyserOsmosis.setup_class()
        cls.analyser_conf = cls.load_osm("tests/osmosis_roundabout.test.osm",
                                         config.dir_tmp + "/tests/osmosis_roundabout.test.xml",
                                         {"proj": 2154}) # Random proj to satisfy highway table generation

    def test_class1(self):
        with Analyser_Osmosis_Roundabout(self.analyser_conf, self.logger) as a:
            a.analyser()

        self.root_err = self.load_errors()
        self.check_err(cl="1", elems=[("way", "119")])
        self.check_num_err(1)
