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

from Analyser_Osmosis import Analyser_Osmosis

sql20 = """
SELECT
    MIN(way_ends.id),
    ST_AsText(nodes.geom),
    MIN(way_ends.highway)
FROM
    {0}highway_ends AS way_ends
    JOIN nodes ON
        nodes.id = ANY (way_ends.nodes) AND
        (NOT nodes.tags?'highway' OR nodes.tags->'highway' != 'turning_circle')
WHERE
    way_ends.level < 3 OR way_ends.highway = 'cycleway'
GROUP BY
    nodes.id,
    nodes.geom
HAVING
    COUNT(*) = 1
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
    nodes[nid_index] AS nid,
    nid_index,
    length
  FROM (
    SELECT
      id,
      linestring,
      nodes,
      generate_subscripts(nodes, 1, tags?'oneway' AND tags->'oneway' = '-1') AS nid_index,
      array_length(nodes, 1) AS length
    FROM
      highways
    WHERE
      is_oneway OR
      is_roundabout
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
    way_nodes.node_id = oneway.nid
  JOIN ways ON
    ways.id = way_nodes.way_id
WHERE
  ways.tags != ''::hstore AND
  (
    ways.tags?'highway' AND
    (NOT ways.tags?'oneway' OR ways.tags->'oneway' IN ('no', 'false')) AND
    (NOT ways.tags?'junction' OR ways.tags->'junction' != 'roundabout')
  ) OR (
    ways.tags?'amenity' AND ways.tags->'amenity' = 'parking'
  )
) UNION (
SELECT
  oneway.nid
FROM
  oneway
  JOIN nodes ON
    nodes.id = oneway.nid
WHERE
  nodes.tags != ''::hstore AND
  nodes.tags?'amenity' AND
  nodes.tags->'amenity' = 'parking_entrance' -- entrance and/or exit
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

class Analyser_Osmosis_Highway_DeadEnd(Analyser_Osmosis):

    requires_tables_common = ['highways']
    requires_tables_full = ['highway_ends']
    requires_tables_diff = ['touched_highway_ends']

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs_change[1] = {"item":"1210", "level": 1, "tag": ["highway", "cycleway", "fix:chair"], "desc": T_(u"Unconnected cycleway") }
        self.classs_change[2] = {"item":"1210", "level": 1, "tag": ["highway", "fix:chair"], "desc": T_(u"Unconnected way") }
        self.classs[3] = {"item":"1210", "level": 1, "tag": ["highway", "fix:chair"], "desc": T_(u"One way inaccessible or missing parking or parking entrance") }
        self.callback20 = lambda res: {"class":1 if res[2]=='cycleway' else 2, "data":[self.way_full, self.positionAsText]}

    def analyser_osmosis_common(self):
        self.run(sql30)
        self.run(sql31)
        self.run(sql32)
        self.run(sql33)
        self.run(sql34)
        self.run(sql35, lambda res: {"class":3, "data":[self.way_full, self.node, self.positionAsText]})

    def analyser_osmosis_full(self):
        self.run(sql20.format(''), self.callback20)

    def analyser_osmosis_diff(self):
        self.run(sql20.format('touched_'), self.callback20)
