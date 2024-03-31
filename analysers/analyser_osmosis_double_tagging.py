#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2011                                      ##
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
CREATE TEMP TABLE relations_alb AS
SELECT
    id,
    geom,
    tags,
    tags->'name' AS name
FROM (
    SELECT
        id,
        ST_Buffer(relation_shape(id), 0.0000001) AS geom, -- Force convertion of Collection to Multipolygon
        tags
    FROM
        relations
    WHERE
        tags?'type' AND
        tags->'type' != 'multipolygon'
    UNION ALL
    -- Treat type=multipolygon relations separate as inners aren't excluded by relation_shape
    SELECT
        id,
        poly AS geom,
        tags
    FROM
        multipolygons
    WHERE
        is_valid
) AS t
WHERE
    tags ?| ARRAY['amenity', 'leisure', 'building'] AND
    (NOT tags?'building' OR tags?'name')
"""

sql11 = """
CREATE TEMP TABLE nodes_alb AS
SELECT
  id,
  geom,
  tags,
  tags->'name' AS name
FROM
  nodes
WHERE
  tags ?| ARRAY['amenity', 'leisure', 'building'] AND
  (NOT tags?'building' OR tags?'name')
"""

sql12 = """
CREATE INDEX idx_nodes_alb_geom ON nodes_alb USING gist(geom)
"""

sql13 = """
CREATE TEMP TABLE ways_alb AS
SELECT
  id,
  linestring AS geom,
  tags,
  tags->'name' AS name
FROM
  ways
WHERE
  tags ?| ARRAY['amenity', 'leisure', 'building'] AND
  (NOT tags?'building' OR tags?'name')
"""

sql14 = """
CREATE INDEX idx_ways_alb_geom ON ways_alb USING gist(geom)
"""

sql20 = """
SELECT
    {2}.id,
    {3}.id,
    ST_AsText(ST_Centroid({3}.geom))
FROM
    {0}{2} AS {2}
    JOIN {1}{3} AS {3} ON
        ST_Covers({2}.geom, {3}.geom) AND
        (
            ({2}.name IS NULL AND {3}.name IS NULL) OR
            {2}.name = {3}.name
        ) AND
        (
            {2}.tags->'amenity' = {3}.tags->'amenity' OR
            {2}.tags->'leisure' = {3}.tags->'leisure' OR
            {2}.tags->'building' = {3}.tags->'building'
        )
"""

class Analyser_Osmosis_Double_Tagging(Analyser_Osmosis):

    requires_tables_full = ['multipolygons']
    requires_tables_diff = ['multipolygons']

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        doc = dict(
            fix = T_(
'''An entity must be present only once, remove one and eventually merge
the tags.'''),
            example = T_(
'''![](https://wiki.openstreetmap.org/w/images/0/08/Osmose-eg-error-4080.png)'''))
        self.classs_change[1] = self.def_class(item = 4080, level = 1, tags = ['tag', 'fix:chair'],
            title = T_('Object tagged twice as node and way'),
            **doc)
        self.classs_change[2] = self.def_class(item = 4080, level = 1, tags = ['tag', 'fix:chair'],
            title = T_('Object tagged twice as way and relation'),
            **doc)
        self.classs_change[3] = self.def_class(item = 4080, level = 1, tags = ['tag', 'fix:chair'],
            title = T_('Object tagged twice as node and relation'),
            **doc)

    def analyser_osmosis_full(self):
        self.run(sql10)
        self.run(sql11)
        self.run(sql12)
        self.run(sql13)
        self.run(sql14)
        def f(o1, o2, ret1, ret2, class_):
            self.run(sql20.format("", "", o1, o2), lambda res: {"class":class_, "data":[ret1, ret2, self.positionAsText]})
        self.apply(f)

    def analyser_osmosis_diff(self):
        self.run(sql10)
        self.run(sql11)
        self.run(sql12)
        self.run(sql13)
        self.run(sql14)
        self.create_view_touched("relations_alb", "R")
        self.create_view_not_touched("relations_alb", "R")
        self.create_view_touched("nodes_alb", "N")
        self.create_view_not_touched("nodes_alb", "N")
        self.create_view_touched("ways_alb", "W")
        self.create_view_not_touched("ways_alb", "W")
        def f(o1, o2, ret1, ret2, class_):
            self.run(sql20.format("touched_", "", o1, o2), lambda res: {"class":class_, "data":[ret1, ret2, self.positionAsText]})
            self.run(sql20.format("not_touched_", "touched_", o1, o2), lambda res: {"class":class_, "data":[ret1, ret2, self.positionAsText]})
        self.apply(f)

    def apply(self, callback):
        ret = {"nodes_alb": self.node_full, "ways_alb": self.way_full, "relations_alb": self.relation_full}
        for c in [["ways_alb", "nodes_alb", 1], ["relations_alb", "ways_alb", 2], ["relations_alb", "nodes_alb", 3]]:
            callback(c[0], c[1], ret[c[0]], ret[c[1]], c[2])


from .Analyser_Osmosis import TestAnalyserOsmosis

class Test(TestAnalyserOsmosis):
    @classmethod
    def setup_class(cls):
        from modules import config
        TestAnalyserOsmosis.setup_class()
        cls.analyser_conf = cls.load_osm("tests/osmosis_double_tagging.osm",
                                         config.dir_tmp + "/tests/osmosis_double_tagging.test.xml",
                                         {"proj": 23032})

    def test_classes(self):
        with Analyser_Osmosis_Double_Tagging(self.analyser_conf, self.logger) as a:
            a.analyser()

        self.root_err = self.load_errors()
        self.check_err(cl="1", elems=[("way", "1000"), ("node", "3")])
        self.check_err(cl="2", elems=[("relation", "10000"), ("way", "1001")])
        self.check_err(cl="2", elems=[("relation", "10001"), ("way", "1006")])
        self.check_err(cl="2", elems=[("relation", "10001"), ("way", "1007")])
        self.check_err(cl="3", elems=[("relation", "10000"), ("node", "17")])
        self.check_err(cl="3", elems=[("relation", "10001"), ("node", "13")])
        self.check_num_err(6)
