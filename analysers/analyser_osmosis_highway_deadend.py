#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2012                                      ##
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

sql20 = """
SELECT
    wid,
    nid,
    ST_AsText(geom),
    highway
FROM (
SELECT
    MIN(way_ends.id) AS wid,
    nodes.id AS nid,
    nodes.geom,
    MIN(way_ends.highway) AS highway
FROM
    {0}highway_ends AS way_ends
    JOIN highways ON
        highways.linestring && way_ends.linestring AND
        way_ends.nid = ANY(highways.nodes) AND
        NOT highways.is_construction
    JOIN nodes ON
        nodes.id = way_ends.nid AND
        (NOT nodes.tags?'amenity' OR nodes.tags->'amenity' != 'bicycle_parking') AND
        (NOT nodes.tags?'entrance' OR nodes.tags->'entrance' = 'no') AND
        (NOT nodes.tags?'noexit' OR nodes.tags->'noexit' = 'no')
WHERE
    way_ends.level < 3 OR way_ends.highway = 'cycleway'
GROUP BY
    nodes.id,
    nodes.geom
HAVING
    COUNT(*) = 1
) AS t
    LEFT JOIN ways AS ferry ON
        ferry.linestring && t.geom AND
        t.nid = ANY(ferry.nodes) AND
        ferry.tags != ''::hstore AND
        ferry.tags?'route' AND
        ferry.tags->'route' = 'ferry'
    LEFT JOIN ways AS bicycle_parking ON
        bicycle_parking.linestring && t.geom AND
        t.nid = ANY(bicycle_parking.nodes) AND
        bicycle_parking.tags != ''::hstore AND
        bicycle_parking.tags?'amenity' AND
        bicycle_parking.tags->'amenity' = 'bicycle_parking'
WHERE
    ferry.id IS NULL AND
    bicycle_parking.id IS NULL
"""

sql30 = """
CREATE TEMP TABLE oneway AS
SELECT
  id,
  t.nid,
  nid_index
FROM (
  SELECT
    id,
    CASE oneway_1
      WHEN false THEN nodes[nid_index]
      WHEN true THEN nodes[length - nid_index + 1]
    END AS nid,
    nid_index,
    length
  FROM (
    SELECT
      id,
      nodes,
      tags?'oneway' AND tags->'oneway' = '-1' AS oneway_1,
      generate_subscripts(nodes, 1) AS nid_index,
      array_length(nodes, 1) AS length
    FROM
      highways
    WHERE
      NOT highways.is_construction AND
      highway != 'motorway' AND -- Ignore motorway even with oneway tag
      highway != 'raceway' AND -- Usually not part of the regular road network
      (
        is_oneway OR
        is_roundabout
      )
  ) AS t
) AS t
  JOIN way_nodes ON
    way_nodes.node_id = t.nid
GROUP BY
  id,
  t.nid,
  nid_index,
  length
HAVING
  COUNT(*) > 1 OR
  nid_index IN (1, length)
"""

sql31 = """
CREATE INDEX idx_oneway_id ON oneway(id)
"""

sql32 = """
CREATE INDEX idx_oneway_nid ON oneway(nid)
"""

sql33 = """
CREATE TEMP TABLE input_nodes AS (
SELECT DISTINCT
  oneway.nid
FROM
  oneway
  JOIN way_nodes ON
    way_nodes.way_id != oneway.id AND
    way_nodes.node_id = oneway.nid
  JOIN ways ON
    ways.id = way_nodes.way_id
WHERE
  ways.tags != ''::hstore AND
  (
    ways.tags?'highway' AND
    (
        ways.tags->'highway' = 'motorway' OR -- Force motorway as input nodes
        ways.tags->'highway' = 'raceway' OR -- Commonly isolated chunks
        (
          (NOT ways.tags?'oneway' OR ways.tags->'oneway' NOT IN ('yes', 'true', '1', '-1')) AND
          (NOT ways.tags?'junction' OR ways.tags->'junction' != 'roundabout')
        )
    )
  ) OR (
    ways.tags?'amenity' AND ways.tags->'amenity' = 'parking'
  )
) UNION ALL (
SELECT
  oneway.nid
FROM
  oneway
  JOIN nodes ON
    nodes.id = oneway.nid
WHERE
  nodes.tags != ''::hstore AND
  (
    (
      nodes.tags?'amenity' AND
      nodes.tags->'amenity' = 'parking_entrance' -- entrance and/or exit
    ) OR
    (
      nodes.tags?'entrance' AND
      nodes.tags->'entrance' = 'garage'
    )
  )
)
"""

sql34 = """
CREATE TEMP TABLE r AS
WITH RECURSIVE t AS (
  SELECT nid FROM input_nodes
UNION
  SELECT
    oneway_next.nid AS nid
  FROM
    t
    JOIN oneway AS oneway_input ON
      oneway_input.nid = t.nid
    JOIN oneway AS oneway_next ON
      oneway_next.id = oneway_input.id AND
      oneway_next.nid_index > oneway_input.nid_index
)
SELECT
  *
FROM
  t
"""

sql35 = """
SELECT
  DISTINCT ON (oneway.id)
  oneway.id,
  oneway.nid,
  (SELECT ST_AsText(geom) FROM nodes WHERE id = oneway.nid)
FROM
  oneway
  LEFT JOIN r ON
    r.nid = oneway.nid
WHERE
  r.nid IS NULL
"""

sql40 = """
SELECT
  drivethroughs.id,
  nid,
  ST_AsText(nodes.geom)
FROM
  highways AS drivethroughs
  JOIN highway_ends ON
    drivethroughs.linestring && highway_ends.geom AND
    highway_ends.nid = ANY(drivethroughs.nodes)
  LEFT JOIN highways AS other_highways ON
    other_highways.linestring && highway_ends.geom AND
    highway_ends.nid = ANY(other_highways.nodes) AND
    other_highways.id != drivethroughs.id
  JOIN nodes ON
    nodes.id = highway_ends.nid AND
    (NOT nodes.tags?'highway' OR (
      nodes.tags->'highway' != 'turning_circle' AND
      nodes.tags->'highway' != 'turning_loop' AND
      nodes.tags->'highway' != 'mini_roundabout'
    )) AND
    (NOT nodes.tags?'entrance' OR nodes.tags->'entrance' = 'no') -- i.e. indoor part not drawn
WHERE
  drivethroughs.highway = 'service' AND
  drivethroughs.tags?'service' AND
  drivethroughs.tags->'service' = 'drive-through' AND
  NOT drivethroughs.is_oneway AND
  other_highways.id IS NULL
"""

class Analyser_Osmosis_Highway_DeadEnd(Analyser_Osmosis):

    requires_tables_common = ['highways', 'highway_ends']
    requires_tables_full = ['highway_ends']
    requires_tables_diff = ['touched_highway_ends']

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        if not "proj" in self.config.options:
            return
        detail = T_(
'''The end of the way is not connected to another way.''')
        self.classs_change[1] = self.def_class(item = 1210, level = 1, tags = ['highway', 'cycleway', 'fix:chair'],
            title = T_('Unconnected cycleway'),
            detail = self.merge_doc(detail, T_(
'''The end of a `highway=cycleway` must be connected to the rest of the
road network to ensure continuity, especially for routes planner.''')),
            fix = T_(
'''Connect the `cycleway` to the road, even with a little virtual
path.'''))
        self.classs_change[2] = self.def_class(item = 1210, level = 1, tags = ['highway', 'fix:chair'],
            title = T_('Unconnected highway'),
            detail = self.merge_doc(detail, T_(
'''Highway from `motorway` to `tertiary` are important ways. They should
lead to somewhere and in particular to a network of minor roads.''')),
            fix = T_(
'''Review the classification of road or draw the local road network.'''))
        self.classs[3] = self.def_class(item = 1210, level = 1, tags = ["highway", "fix:chair"],
            title = T_('One way inaccessible or missing parking or parking entrance'))
        self.classs[5] = self.def_class(item = 1210, level = 2, tags = ['highway', 'fix:chair'],
            title = T_('Unconnected drive-through'),
            detail = self.merge_doc(detail, T_(
'''Drive-throughs are usually not dead-ended. Make sure the full drive-through path was drawn, including i.e. turning circles and covered areas.
Ensure that `service=drive-through` is the correct tag.''')),
            fix = T_(
'''Review the type of the service road or draw the local road network.'''),
            resource = 'https://wiki.openstreetmap.org/wiki/Tag:service%3Ddrive-through')

        self.callback20 = lambda res: {"class":1 if res[3] == 'cycleway' else 2, "data":[self.way_full, self.node_full, self.positionAsText]}

    def analyser_osmosis_common(self):
        self.run(sql30)
        self.run(sql31)
        self.run(sql32)
        self.run(sql33)
        self.run(sql34)
        self.run(sql35, lambda res: {"class":3, "data":[self.way_full, self.node, self.positionAsText]})
        self.run(sql40, lambda res: {"class":5, "data":[self.way_full, self.node, self.positionAsText]})

    def analyser_osmosis_full(self):
        self.run(sql20.format(''), self.callback20)

    def analyser_osmosis_diff(self):
        self.run(sql20.format('touched_'), self.callback20)


###########################################################################

from .Analyser_Osmosis import TestAnalyserOsmosis

class Test(TestAnalyserOsmosis):
    @classmethod
    def setup_class(cls):
        from modules import config
        TestAnalyserOsmosis.setup_class()
        cls.analyser_conf = cls.load_osm("tests/osmosis_highway_deadend.osm",
                                         config.dir_tmp + "/tests/osmosis_highway_deadend.test.xml",
                                         {"proj": 2154}) # Random proj to satisfy highway table generation

    def test_classes(self):
        with Analyser_Osmosis_Highway_DeadEnd(self.analyser_conf, self.logger) as a:
            a.analyser()

        self.root_err = self.load_errors()
        self.check_err(cl="2", elems=[("node", "59"), ("way", "1026")])
        self.check_err(cl="2", elems=[("node", "55"), ("way", "1024")])

        self.check_err(cl="3", elems=[("node", "2"), ("way", "1000")]) # May become node = 1
        self.check_err(cl="3", elems=[("node", "5"), ("way", "1001")]) # May become node = 3
        self.check_err(cl="3", elems=[("node", "3"), ("way", "1002")]) # May become node = 4
        self.check_err(cl="3", elems=[("node", "9"), ("way", "1003")])
        self.check_err(cl="3", elems=[("node", "14"), ("way", "1005")])
        self.check_err(cl="3", elems=[("node", "65"), ("way", "1028")])
        self.check_err(cl="3", elems=[("node", "15"), ("way", "1006")])
        self.check_err(cl="3", elems=[("node", "15"), ("way", "1007")])
        self.check_err(cl="3", elems=[("node", "21"), ("way", "1009")]) # May become node = 23
        self.check_err(cl="3", elems=[("node", "23"), ("way", "1034")]) # May become node = 21

        self.check_err(cl="5", elems=[("node", "73"), ("way", "1031")])

        self.check_num_err(13)
