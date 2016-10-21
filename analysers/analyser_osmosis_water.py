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

sql00 = """
CREATE TEMP TABLE water AS
(
SELECT
  id,
  linestring
FROM
  ways
WHERE
  (
    ways.tags?'waterway' AND
    ways.tags->'waterway' IN ('river', 'riverbank', 'canal', 'dock')
  ) OR (
    ways.tags?'water' AND
    ways.tags->'water' IN ('lake', 'reservoir', 'river', 'canal', 'lagoon')
  ) OR (
    ways.tags?'natural' AND
    ways.tags->'natural' = 'water' AND
    (
      NOT ways.tags?'water' OR
      ways.tags->'water' IN ('lake', 'reservoir', 'river', 'canal', 'lagoon')
    )
  ) OR (
    ways.tags?'natural' AND
    ways.tags->'natural' IN ('coastline', 'beach', 'wetland')
  ) OR (
    ways.tags?'landuse' AND
    ways.tags->'landuse' IN ('basin', 'reservoir')
  ) OR (
    tags?'man_made' AND
    tags->'man_made' IN ('quay', 'pier')
  )
) UNION
(
SELECT
  ways.id,
  ways.linestring
FROM
  relations
  JOIN relation_members ON
    relation_members.relation_id = relations.id AND
    relation_members.member_type= 'W' AND
    relation_members.member_role IN ('inner', 'outer')
  JOIN ways ON
    ways.id = relation_members.member_id
WHERE
  (
    relations.tags?'waterway' AND
    relations.tags->'waterway' IN ('river', 'riverbank', 'canal', 'dock')
  ) OR (
    relations.tags?'water' AND
    relations.tags->'water' IN ('lake', 'reservoir', 'river', 'canal', 'lagoon')
  ) OR (
    relations.tags?'natural' AND
    relations.tags->'natural' = 'water' AND
    (
      NOT relations.tags?'water' OR
      relations.tags->'water' IN ('lake', 'reservoir', 'river', 'canal', 'lagoon')
    )
  ) OR (
    relations.tags?'natural' AND
    relations.tags->'natural' IN ('beach', 'wetland')
  ) OR (
    relations.tags?'landuse' AND
    relations.tags->'landuse' IN ('basin', 'reservoir')
  )
)
"""

sql01 = """
CREATE INDEX idx_water_linestring ON water USING GIST(linestring);
"""

sql10 = """
CREATE TEMP TABLE {0}objects AS
(
SELECT
  'W'::CHAR(1) AS type,
  id AS id,
  linestring AS geom,
  ST_Transform(ST_Expand(ST_Transform(linestring, {1}), 20), 4326) AS bbox
FROM
  {0}ways AS ways
WHERE
  (
    tags?'leisure' AND
    tags->'leisure' = 'slipway'
  ) OR (
    tags?'man_made' AND
    tags->'man_made' IN ('quay', 'pier')
  )
)
UNION
(
SELECT
  'N'::CHAR(1) AS type,
  id,
  geom,
  ST_Transform(ST_Expand(ST_Transform(geom, {1}), 20), 4326) AS bbox
FROM
  {0}nodes AS nodes
WHERE
  tags?'leisure' AND
  tags->'leisure' = 'slipway'
)
"""

sql11= """
SELECT
  objects.type || objects.id,
  ST_AsText(any_locate(objects.type, objects.id))
FROM
  {0}objects AS objects
  LEFT JOIN water ON
    (objects.type != 'W' OR water.id != objects.id) AND
    objects.bbox && water.linestring AND
    ST_DistanceSphere(objects.geom, water.linestring) < 20
WHERE
  water IS NULL
"""

class Analyser_Osmosis_Water(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs_change[1] = {"item":"1221", "level": 2, "tag": ["water", "fix:imagery"], "desc": T_(u"Object must be close to coast or water") }
        self.callback10 = lambda res: {"class":1, "data":[self.any_full, self.positionAsText]}

    def analyser_osmosis_all(self):
        self.run(sql00)
        self.run(sql01)
        self.run(sql10.format("", self.config.options.get("proj")))
        self.run(sql11.format(""), self.callback10)

    def analyser_osmosis_touched(self):
        self.run(sql00)
        self.run(sql01)
        self.run(sql10.format("touched_", self.config.options.get("proj")))
        self.run(sql11.format("touched_"), self.callback10)
