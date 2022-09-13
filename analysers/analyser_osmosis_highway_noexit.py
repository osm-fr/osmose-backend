#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2014                                      ##
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
    nodes.id,
    ST_AsText(nodes.geom),
    COUNT(*) > 1
FROM
    {1}highways AS ways
    JOIN way_nodes ON
      way_nodes.way_id = ways.id
    JOIN {0}nodes AS nodes ON
      nodes.id = way_nodes.node_id AND
      nodes.tags != ''::hstore AND
      nodes.tags?'noexit' AND
      nodes.tags->'noexit' = 'yes'
WHERE
    NOT ways.is_construction AND
    NOT ways.is_area
GROUP BY
    nodes.id,
    nodes.geom
HAVING
    COUNT(*) > 1 OR
    nodes.id NOT IN (SELECT ends(MIN(ways.nodes)))
"""

sql20 = """
SELECT
    id,
    ST_AsText(way_locate(linestring))
FROM
    (
    SELECT
        w1.id,
        w1.linestring
    FROM
        highways AS w1
        JOIN highways AS w2 ON
            w2.id != w1.id AND
            w1.linestring && w2.linestring AND
            w1.nodes && w2.nodes
    WHERE
        w1.tags?'noexit' = 'yes' AND
        NOT w1.is_construction AND
        NOT w2.is_construction
    GROUP BY
        w1.id,
        w1.linestring,
        (SELECT MIN(nid) FROM (SELECT UNNEST(w1.nodes) INTERSECT SELECT UNNEST(w2.nodes)) AS t(nid))
    ) AS t
GROUP BY
    id,
    linestring
HAVING
    COUNT(*) > 1
"""

class Analyser_Osmosis_Highway_Noexit(Analyser_Osmosis):

    requires_tables_full = ['highways']
    requires_tables_diff = ['highways', 'touched_highways', 'not_touched_highways']

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        if not "proj" in self.config.options:
            return
        self.classs_change[1] = self.def_class(item = 3210, level = 2, tags = ['highway', 'tag', 'fix:chair'],
            title = T_('Noexit on node with exit'))
        self.classs[2] = self.def_class(item = 3210, level = 2, tags = ['highway', 'tag', 'fix:chair'],
            title = T_('Noexit on way with multiple exits'))
        self.callback10 = lambda res: {"class":1, "subclass":1 if res[2] else 2, "data":[self.node_full, self.positionAsText], "fix":{"-":["noexit"]}}
        self.callback20 = lambda res: {"class":2, "data":[self.way_full, self.positionAsText], "fix":{"-":["noexit"]} }

    def analyser_osmosis_common(self):
        self.run(sql20, self.callback20)

    def analyser_osmosis_full(self):
        self.run(sql10.format("", ""), self.callback10)

    def analyser_osmosis_diff(self):
        self.run(sql10.format("touched_", "not_touched_"), self.callback10)
        self.run(sql10.format("", "touched_"), self.callback10)

###########################################################################

from .Analyser_Osmosis import TestAnalyserOsmosis

class Test(TestAnalyserOsmosis):
    @classmethod
    def setup_class(cls):
        from modules import config
        TestAnalyserOsmosis.setup_class()
        cls.analyser_conf = cls.load_osm("tests/osmosis_noexit.test.osm",
                                         config.dir_tmp + "/tests/osmosis_noexit.test.xml",
                                         {"proj": 2969})

    def test(self):
        with Analyser_Osmosis_Highway_Noexit(self.analyser_conf, self.logger) as a:
            a.analyser()

        self.compare_results("tests/results/osmosis_noexit.test.xml")

        self.root_err = self.load_errors()
        self.check_err(cl="1", lat="43.5738441546", lon="7.1352332297", elems=[("node", "140")])
        self.check_err(cl="2", lat="43.58698923085", lon="7.13208912621", elems=[("way", "77")])
        self.check_err(cl="2", lat="43.56376388279", lon="7.05560008059", elems=[("way", "329")])
        self.check_num_err(3)
