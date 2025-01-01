#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2017                                      ##
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

sql12 = """
CREATE TEMP TABLE way_ends AS
SELECT
  t.id,
  t.nid,
  t.nodes,
  geom AS ogeom,
  ST_Transform(nodes.geom, {0}) AS geom
FROM (
  SELECT
    t.id,
    t.nid,
    t.nodes
  FROM (
    SELECT
      id,
      linestring,
      ends(nodes) AS nid,
      nodes
    FROM
      highways
    WHERE
      highway NOT IN ('service', 'footway', 'path', 'platform', 'steps') AND
      NOT is_construction AND
      NOT is_polygon AND
      ST_Length(linestring_proj) > 10
    ) AS t
    LEFT JOIN highways ON
      highways.id != t.id AND
      highways.linestring && t.linestring AND
      t.nid = ANY(highways.nodes)
    WHERE
      highways.id IS NULL
  ) as t
  JOIN nodes ON
    nodes.id = t.nid AND
    NOT (
      nodes.tags?'noexit' OR
      (nodes.tags?'highway' AND nodes.tags->'highway' IN ('turning_circle', 'bus_stop')) OR
      (nodes.tags?'railway' AND nodes.tags->'railway' IN ('subway_entrance')) OR
      (nodes.tags?'public_transport' AND nodes.tags->'public_transport' IN ('platform')) OR
      nodes.tags?'amenity' OR
      nodes.tags?'barrier' OR
      array_length(array_positions(t.nodes, nodes.id), 1) != 1 -- exclude the self-intersecting node in P-shaped ways
    )
"""

sql13 = """
SELECT DISTINCT
  way_ends.id,
  way_ends.nid,
  ST_AsText(way_ends.ogeom)
FROM
  way_ends
  JOIN highways ON
    ST_DWithin(way_ends.geom, highways.linestring_proj, 10) AND
    highways.id != way_ends.id AND
    NOT way_ends.nodes && highways.nodes AND -- not connected, even in other place than nid
    NOT highways.tags ?| ARRAY ['tunnel', 'bridge']
  LEFT JOIN highways AS h2 ON
    h2.linestring && highways.linestring AND
    h2.nodes && highways.nodes AND
    h2.id != highways.id AND
    h2.id != way_ends.id AND
    way_ends.nodes && h2.nodes
WHERE
  h2.id IS NULL -- and there is not an intermediate way joining the two firsts
"""


class Analyser_Osmosis_Highway_Almost_Junction(Analyser_Osmosis):

    requires_tables_common = ['highways']

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs[1] = self.def_class(item = 1270, level = 1, tags = ['highway', 'fix:chair'],
            title = T_('Almost junction, join or use noexit tag'))

    def analyser_osmosis_common(self):
        self.run(sql12.format(self.config.options.get("proj")))
        self.run(sql13, lambda res: {"class":1, "data":[self.way_full, self.node, self.positionAsText]})


###########################################################################

from .Analyser_Osmosis import TestAnalyserOsmosis

class Test(TestAnalyserOsmosis):
    @classmethod
    def setup_class(cls):
        from modules import config
        TestAnalyserOsmosis.setup_class()
        cls.analyser_conf = cls.load_osm("tests/osmosis_highway_almost_junction.osm",
                                         config.dir_tmp + "/tests/osmosis_highway_almost_junction.test.xml",
                                         {"proj": 23032}) # Random proj to satisfy highway table generation

    def test_classes(self):
        with Analyser_Osmosis_Highway_Almost_Junction(self.analyser_conf, self.logger) as a:
            a.analyser()

        self.root_err = self.load_errors()
        self.check_err(cl="1", elems=[("node", "17"), ("way", "1008")])
        self.check_err(cl="1", elems=[("node", "18"), ("way", "1007")])
        self.check_err(cl="1", elems=[("node", "23"), ("way", "1010")])

        self.check_num_err(3)
