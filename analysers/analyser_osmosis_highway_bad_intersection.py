#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2015                                      ##
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

from .Analyser_Osmosis import Analyser_Osmosis

sql10 = """
SELECT
  w1_id,
  w2_id,
  ST_AsText(geom)
FROM
  (
  SELECT
    w1.id AS w1_id,
    w2.id AS w2_id,
    (SELECT * FROM (SELECT unnest(w1.nodes) INTERSECT SELECT unnest(w2.nodes)) AS t LIMIT 1) AS n_id
  FROM
    {0}highways AS w1
    JOIN {1}ways AS w2 ON
      w2.linestring && w1.linestring AND
      w2.nodes && w1.nodes AND
      w2.id != w1.id AND
      w2.tags != ''::hstore AND
      w2.tags?'power' AND
      w2.tags->'power' IN ('line', 'minor_line', 'cable')
  GROUP BY
    1, 2, 3
  ) AS t
  JOIN nodes ON
    nodes.id = n_id
"""

sql20 = """
SELECT
  w1_id,
  w2_id,
  ST_AsText(geom)
FROM
  (
  SELECT
    w1.id AS w1_id,
    w2.id AS w2_id,
    (SELECT * FROM (SELECT unnest(w1.nodes) INTERSECT SELECT unnest(w2.nodes)) AS t LIMIT 1) AS n_id
  FROM
    {0}highways AS w1
    JOIN {1}ways AS w2 ON
      w2.linestring && w1.linestring AND
      w2.nodes && w1.nodes AND
      w2.id != w1.id AND
      w2.tags != ''::hstore AND
      w2.tags?'waterway' AND
      w2.tags->'waterway' IN ('river', 'stream', 'canal', 'drain')
  WHERE
    NOT w1.tags?'ford' OR w1.tags->'ford' != 'yes'
  GROUP BY
    1, 2, 3
  ) AS t
  JOIN nodes ON
    nodes.id = n_id
WHERE
  (NOT tags?'highway' OR tags->'highway' != 'ford') AND
  (NOT tags?'ford' OR tags->'ford' = 'no')
"""

class Analyser_Osmosis_Highway_Bad_Intersection(Analyser_Osmosis):

    requires_tables_full = ['highways']
    requires_tables_diff = ['highways', 'touched_highways']

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs_change[1] = {"item":"1250", "level": 3, "tag": ["highway", "power", "fix:chair"], "desc": T_(u"Intersection of unrelated highway and power objects") }
        self.classs_change[2] = {"item":"1250", "level": 3, "tag": ["highway", "waterway", "fix:chair"], "desc": T_(u"Intersection of unrelated highway and waterway objects") }

    def analyser_osmosis_full(self):
        self.run(sql10.format("", ""), lambda res: {"class": 1, "data": [self.way, self.way, self.positionAsText] })
        self.run(sql20.format("", ""), lambda res: {"class": 2, "data": [self.way, self.way, self.positionAsText] })

    def analyser_osmosis_diff(self):
        self.run(sql10.format("touched_", "not_touched_"), lambda res: {"class": 1, "data": [self.way, self.way, self.positionAsText] })
        self.run(sql10.format("", "touched_"), lambda res: {"class": 1, "data": [self.way, self.way, self.positionAsText] })
        self.run(sql20.format("touched_", "not_touched_"), lambda res: {"class": 2, "data": [self.way, self.way, self.positionAsText] })
        self.run(sql20.format("", "touched_"), lambda res: {"class": 2, "data": [self.way, self.way, self.positionAsText] })
