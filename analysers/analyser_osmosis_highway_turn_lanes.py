#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2016                                      ##
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
CREATE TEMP TABLE turn_lanes_ends AS
SELECT
  DISTINCT ON (id)
  ends(nodes) AS id
FROM
  ways
WHERE
  tags != ''::hstore AND
  tags?'highway' AND
  (
    tags->'highway' = 'motorway' OR
    (tags->'highway' = 'trunk' AND tags->'oneway' = 'yes')
  ) AND
  tags?'turn:lanes'
"""

sql11 = """
CREATE INDEX idx_turn_lanes_ends_id ON turn_lanes_ends(id);
"""

sql12 = """
CREATE TEMP TABLE turn_lanes_steps AS
SELECT
  turn_lanes_ends.id AS nid,
  CASE ways.tags->'oneway'
    WHEN '-1' THEN turn_lanes_ends.id != ways.nodes[1]
    ELSE turn_lanes_ends.id = ways.nodes[1]
  END AS start_end,
  ways.id,
  ways.tags
FROM
  ways
  JOIN turn_lanes_ends ON
    turn_lanes_ends.id = ways.nodes[1] OR
    turn_lanes_ends.id = ways.nodes[array_length(ways.nodes, 1)]
WHERE
  ways.tags != ''::hstore AND
  ways.tags?'highway' AND
  (NOT ways.tags?'access' OR ways.tags->'access' != 'no')
"""

sql13 = """
CREATE TEMP TABLE sum_turn_lanes_steps AS
SELECT
  nid,
  start_end,
  SUM(CASE
    WHEN tags->'lanes' ~ E'^[0-9]+$' THEN (tags->'lanes')::integer
    WHEN tags?'turn:lanes' THEN array_length(string_to_array(tags->'turn:lanes', '|'), 1)
    WHEN tags->'highway' IN ('motorway', 'trunk') THEN 2
    ELSE 1
  END) AS lanes,
  SUM(array_length(string_to_array(tags->'turn:lanes', 'slight_'), 1) - 1) AS lanes_slight,
  SUM(array_length(string_to_array(tags->'turn:lanes', 'merge_to_'), 1) - 1) AS lanes_merge_to
FROM
  turn_lanes_steps
GROUP BY
  nid,
  start_end
HAVING
  BOOL_AND(tags->'highway' IN ('motorway', 'motorway_link') OR (tags->'highway' IN ('trunk', 'trunk_link') AND tags->'oneway' = 'yes'))
"""

sql14 = """
SELECT
  nid,
  ST_AsText(nodes.geom),
  lin_lanes,
  lin_lanes_merge_to,
  lin_lanes_slight,
  lout_lanes,
  lout_lanes_merge_to,
  lout_lanes_slight
FROM
  (
  SELECT
    lin.nid,
    lin.lanes AS lin_lanes,
    lin.lanes_merge_to AS lin_lanes_merge_to,
    lin.lanes_slight AS lin_lanes_slight,
    lout.lanes AS lout_lanes,
    lout.lanes_merge_to AS lout_lanes_merge_to,
    lout.lanes_slight AS lout_lanes_slight
  FROM
    sum_turn_lanes_steps AS lin
    JOIN sum_turn_lanes_steps AS lout ON
      lin.nid = lout.nid AND
      (
        (
          (lin.lanes_merge_to = 0 OR lin.lanes_merge_to IS NULL) AND
          lout.lanes < lin.lanes
        ) OR (
          lin.lanes_merge_to > 0 AND
          NOT (
            lout.lanes - lin.lanes_slight <= lin.lanes AND
            lout.lanes - lin.lanes_slight - lout.lanes_merge_to <= lin.lanes - lin.lanes_merge_to + lout.lanes_slight
          )
        )
      )
  WHERE
    NOT lin.start_end AND
    lout.start_end
  ORDER BY
    1 -- Just to force the query planner to does not merge sub and main request
  ) AS t
  JOIN nodes ON
    nodes.id = nid AND
    (NOT nodes.tags?'highway' OR nodes.tags->'highway' != 'traffic_signals')
"""

class Analyser_Osmosis_Highway_Turn_Lanes(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs[1] = {"item":"3160", "level": 2, "tag": ["highway", "fix:chair"], "desc": T_(u"Bad lanes number or lanes:turn before and after this node") }

    def analyser_osmosis(self):
        self.run(sql10)
        self.run(sql11)
        self.run(sql12)
        self.run(sql13)
        self.run(sql14, lambda res: {"class":1, "data":[self.node, self.positionAsText], "text": {"en": "lanes in %s(-%s+%s), lanes out %s(-%s+%s)" % (res[2], res[3] or 0, res[4] or 0, res[5], res[6] or 0, res[7] or 0) }})
