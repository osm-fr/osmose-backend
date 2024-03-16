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

sql10 = """
-- From https://wiki.postgresql.org/wiki/Array_reverse
-- Inverts the sequence of the elements in an array
CREATE OR REPLACE FUNCTION array_reverse(anyarray) RETURNS anyarray AS $$
SELECT ARRAY(
    SELECT $1[i]
    FROM generate_subscripts($1,1) AS s(i)
    ORDER BY i DESC
);
$$ LANGUAGE 'sql' STRICT IMMUTABLE;
"""

sql21 = """
CREATE TEMP TABLE bicycle_parking AS
SELECT
    linestring,
    nodes
FROM
    ways
WHERE
    tags != ''::hstore AND
    tags?'amenity' AND
    tags->'amenity' = 'bicycle_parking'
"""

sql22 = """
CREATE INDEX idx_bicycle_parking_linestring ON bicycle_parking USING GIST(linestring);
"""

sql23 = """
CREATE TEMP TABLE unconnected_highways AS
SELECT
    wid,
    nid,
    geom,
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
        (NOT nodes.tags?'amenity' OR nodes.tags->'amenity' NOT IN ('bicycle_parking', 'ferry_terminal')) AND
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
"""

sql24 = """
SELECT
    wid,
    nid,
    ST_AsText(geom)
FROM
    unconnected_highways
    LEFT JOIN bicycle_parking ON
        bicycle_parking.linestring && unconnected_highways.geom AND
        unconnected_highways.nid = ANY(bicycle_parking.nodes)
WHERE
    highway = 'cycleway' AND
    bicycle_parking IS NULL
"""

sql25 = """
SELECT
    wid,
    nid,
    ST_AsText(geom)
FROM
    unconnected_highways
WHERE
    highway != 'cycleway'
"""


sql30 = """
-- Collect all oneways
CREATE TEMP TABLE oneway_highway AS
SELECT
  id,
  CASE -- If oneway=-1, pretent the way is the other way around
    WHEN tags?'oneway' AND tags->'oneway' = '-1' THEN array_reverse(nodes)
    ELSE nodes
  END AS nodes,
  linestring,
  array_length(nodes, 1) AS length,
  generate_subscripts(nodes, 1) AS nid_index
FROM
  highways
WHERE
  (is_oneway OR is_roundabout) AND
  NOT is_area AND
  NOT is_construction
"""

sql31 = """
CREATE INDEX idx_oneway_highway_linestring ON oneway_highway USING GIST(linestring) WHERE nid_index=1;
"""

sql32 = """
-- Collect all nodes that could be possible (valid) end nodes
CREATE TEMP TABLE allowed_end_nodes AS
SELECT DISTINCT
  unnest(nodes) AS id
FROM
  ways
WHERE
  tags != ''::hstore AND
  (
    (tags?'amenity' AND tags->'amenity' = 'parking') OR
    (tags?'railway' AND tags->'railway' = 'platform') OR
    (tags?'aeroway' AND tags->'aeroway' = 'taxiway') OR
    (tags?'aerialway' AND tags->'aerialway' IN ('station', 'zip_line'))
  )
UNION ALL
SELECT
  id
FROM
  nodes
WHERE
  tags != ''::hstore AND
  (
    (tags?'amenity'  AND tags->'amenity' IN ('parking_entrance', 'parking', 'ferry_terminal')) OR
    (tags?'entrance' AND tags->'entrance' IN ('garage', 'emergency')) OR
    (tags?'aerialway' AND tags->'aerialway' = 'station')
  )
UNION ALL
SELECT DISTINCT
  unnest(nodes) AS id
FROM
  highways
WHERE
  -- Non-oneway highways are valid input nodes for oneways
  (NOT is_oneway AND NOT is_roundabout) OR
  -- Raceways are commonly isolated from the main network
  -- Escape (emergency stop) ways are supposed to be not used / dead-ended
  -- Footway can lead to anything (attraction entrances, ...) so exclude them even if oneway
  highway IN ('raceway', 'escape', 'footway') OR
  -- Construction roads are usually temporary, the connections are likely access=no or similar
  is_construction
UNION ALL
-- Include nodes of ways that cross the extract border. See #1949
-- Better would be to only include the nodes outside of the extract, but that's expensive
SELECT
  unnest(borderways.nodes)
FROM
  relation_members AS boundary_members
  JOIN ways AS boundary_ways ON
    boundary_members.member_id = boundary_ways.id
  JOIN highways AS borderways ON
    ST_Intersects(boundary_ways.linestring, borderways.linestring)
WHERE
  boundary_members.member_type = 'W' AND
  boundary_members.relation_id IN {boundary_ids}
"""

sql33 = """
CREATE INDEX idx_allowed_nodes_id ON allowed_end_nodes(id);
"""

sql34 = """
-- Make table as short as possible: keep only nodes that are actually nodes of oneways
CREATE TEMP TABLE allowed_oneway_end_nodes AS
SELECT DISTINCT
  allowed_end_nodes.id
FROM
  allowed_end_nodes
  JOIN oneway_highway ON
    -- Note that we cannot literally only get the first and last node, as i.e. in a looped oneway the 'oneway-entrance/exit node' might be in the middle
    allowed_end_nodes.id = ANY(oneway_highway.nodes) AND
    oneway_highway.nid_index = 1 -- no need to compare length(nodes) times
"""

sql35 = """
CREATE INDEX idx_allowed_oneway_nodes_id ON allowed_oneway_end_nodes(id);
DROP TABLE allowed_end_nodes;
"""

sql36 = """
-- All end nodes of oneway streets
CREATE TEMP TABLE oneway_terminal AS
SELECT
  t.*,
  geom
FROM (
  SELECT DISTINCT ON (nid)
    oneway.id AS wid,
    oneway.nodes[oneway.nid_index] AS nid,
    oneway.nid_index = oneway.length AS is_oneway_last_node
  FROM
    oneway_highway AS oneway
    LEFT JOIN allowed_oneway_end_nodes ON
      oneway.nodes[oneway.nid_index] = allowed_oneway_end_nodes.id
  WHERE
    oneway.nid_index IN (1, oneway.length) AND
    allowed_oneway_end_nodes IS NULL AND
    array_length(array_positions(oneway.nodes, oneway.nodes[oneway.nid_index]), 1) = 1 -- exclude end nodes folding back into the same way, e.g. in P or O-shaped ways
  ORDER BY
    nid,
    oneway.id
  ) AS t
  JOIN nodes ON
    id = nid
"""

sql37 = """
-- Find all end nodes that are not connected to a way that allows to enter/leave the oneway street
CREATE TEMP TABLE results_straightforward AS
SELECT
  wid,
  nid,
  geom
FROM
  oneway_terminal
  LEFT JOIN oneway_highway AS other_highway ON
    oneway_terminal.nid = ANY(other_highway.nodes) AND
    oneway_terminal.geom && other_highway.linestring AND -- much faster than comparison with nid
    other_highway.nid_index = 1 AND -- no need to compare length(nodes) times
    oneway_terminal.wid != other_highway.id AND
    (
      array_length(array_positions(other_highway.nodes, oneway_terminal.nid), 1) != 1 OR -- end node of loop/self-intersecting way that also occurs elsewhere
      (
        (oneway_terminal.is_oneway_last_node AND oneway_terminal.nid != other_highway.nodes[other_highway.length]) OR
        (NOT oneway_terminal.is_oneway_last_node AND oneway_terminal.nid != other_highway.nodes[1])
      )
    )
WHERE
  other_highway IS NULL
"""

sql38 = """
-- All nodes of oneways that have a connection (or are end nodes)
CREATE TEMP TABLE oneway_connection_nodes AS
SELECT
  wid,
  nid,
  nid_index
FROM (
  SELECT
    id AS wid,
    nid_index,
    length,
    nodes[nid_index] AS nid
  FROM
    oneway_highway
  ) AS t
  JOIN way_nodes ON
    way_nodes.node_id = t.nid
GROUP BY
  wid,
  nid,
  nid_index,
  length
HAVING
  COUNT(*) > 1 OR
  nid_index IN (1, length)
"""

sql39 = """
CREATE INDEX idx_oneway_connection_nodes_wid ON oneway_connection_nodes(wid);
CREATE INDEX idx_oneway_connection_nodes_nid ON oneway_connection_nodes(nid);
DROP TABLE oneway_terminal;
"""

sql40 = """
CREATE TEMP TABLE input_nodes AS
SELECT
  id
FROM
  allowed_oneway_end_nodes
UNION ALL
-- Avoid results via recursive checking that originate from a 'straightforward' deadend
SELECT
  nid AS id
FROM
  results_straightforward
"""

sql41 = """
CREATE TEMP TABLE r AS
WITH RECURSIVE t AS (
  SELECT id FROM input_nodes
UNION
  SELECT
    oneway_next.nid AS nid
  FROM
    t
    JOIN oneway_connection_nodes AS oneway_input ON
      oneway_input.nid = t.id
    JOIN oneway_connection_nodes AS oneway_next ON
      oneway_next.wid = oneway_input.wid AND
      oneway_next.nid_index > oneway_input.nid_index
)
SELECT
  *
FROM
  t
"""

sql42 = """
CREATE TEMP TABLE results_recursive AS
SELECT DISTINCT ON (oneway_connection_nodes.wid)
  oneway_connection_nodes.wid,
  oneway_connection_nodes.nid
FROM
  oneway_connection_nodes
  LEFT JOIN r ON
    r.id = oneway_connection_nodes.nid
WHERE
  r.id IS NULL
ORDER BY
  oneway_connection_nodes.wid
"""

sql43 = """
SELECT DISTINCT ON(nid)
  wid,
  nid,
  ST_AsText(geom)
FROM (
  SELECT
    wid,
    nid,
    geom
  FROM
    results_straightforward
  UNION ALL
  SELECT
    wid,
    nid,
    geom
  FROM
    results_recursive
    JOIN nodes ON
      nodes.id = results_recursive.nid
) AS t
ORDER BY
  nid,
  wid
"""

sql50 = """
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
  drivethroughs.nodes[1] != drivethroughs.nodes[array_length(drivethroughs.nodes,1)] AND
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

        self.callback21 = lambda res: {"class": 1, "data": [self.way_full, self.node_full, self.positionAsText]}
        self.callback22 = lambda res: {"class": 2, "data": [self.way_full, self.node_full, self.positionAsText]}

    def analyser_osmosis_common(self):
        boundary_relation = self.config.polygon_id # Either a number, None or (number, number, ...)
        if isinstance(boundary_relation, int):
          boundary_relation = "({0})".format(boundary_relation)
        elif not boundary_relation:
          boundary_relation = "(0)"

        self.run(sql10)
        self.run(sql30)
        self.run(sql31)
        self.run(sql32.format(boundary_ids=boundary_relation))
        self.run(sql33)
        self.run(sql34)
        self.run(sql35)
        self.run(sql36)
        self.run(sql37)
        self.run(sql38)
        self.run(sql39)
        self.run(sql40)
        self.run(sql41)
        self.run(sql42)
        self.run(sql43, lambda res: {"class":3, "data":[self.way_full, self.node_full, self.positionAsText]})
        self.run(sql50, lambda res: {"class":5, "data":[self.way_full, self.node, self.positionAsText]})

    def analyser_osmosis_full(self):
        self.run(sql21)
        self.run(sql22)
        self.run(sql23.format(''))
        self.run(sql24, self.callback21)
        self.run(sql25, self.callback22)

    def analyser_osmosis_diff(self):
        self.run(sql21)
        self.run(sql22)
        self.run(sql23.format('touched_'))
        self.run(sql24, self.callback21)
        self.run(sql25, self.callback22)


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
        self.check_err(cl="1", elems=[("node", "161"), ("way", "1087")])
        self.check_err(cl="2", elems=[("node", "59"), ("way", "1026")])
        self.check_err(cl="2", elems=[("node", "55"), ("way", "1024")])

        # Detection of straightforward oneway deadends
        self.check_err(cl="3", elems=[("node", "1"), ("way", "1000")])
        self.check_err(cl="3", elems=[("node", "2"), ("way", "1000")])
        self.check_err(cl="3", elems=[("node", "9"), ("way", "1003")])
        self.check_err(cl="3", elems=[("node", "14"), ("way", "1005")])
        self.check_err(cl="3", elems=[("node", "15"), ("way", "1006")]) # way 1006 or 1007 are both fine
        self.check_err(cl="3", elems=[("node", "55"), ("way", "1024")])
        self.check_err(cl="3", elems=[("node", "65"), ("way", "1028")])
        self.check_err(cl="3", elems=[("node", "82"), ("way", "1036")]) # way 1036 or 1037 are both fine
        self.check_err(cl="3", elems=[("node", "84"), ("way", "1038")]) # way 1038 or 1040 are both fine
        self.check_err(cl="3", elems=[("node", "90"), ("way", "1043")])
        self.check_err(cl="3", elems=[("node", "92"), ("way", "1045")])
        self.check_err(cl="3", elems=[("node", "97"), ("way", "1049")])
        self.check_err(cl="3", elems=[("node", "98"), ("way", "1048")])
        self.check_err(cl="3", elems=[("node", "101"), ("way", "1051")])
        self.check_err(cl="3", elems=[("node", "102"), ("way", "1052")])
        # Detections of deadend circular oneway highways. Note that some test cases have multiple valid 'solutions'
        # for dead-end oneway islands upon traversing, so results may change upon code update and still be valid
        self.check_err(cl="3", elems=[("node", "4"), ("way", "1001")]) # way 1001 or 1002 are both fine
        self.check_err(cl="3", elems=[("node", "21"), ("way", "1009")]) # way 1009 or 1034 are both fine
        self.check_err(cl="3", elems=[("node", "108"), ("way", "1058")]) # way 1058 or 1059 are both fine
        self.check_err(cl="3", elems=[("node", "109"), ("way", "1060")]) # way 1058 or 1060 are both fine

        self.check_err(cl="5", elems=[("node", "73"), ("way", "1031")])

        self.check_num_err(23)
