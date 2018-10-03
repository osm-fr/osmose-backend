#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2018                                      ##
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
CREATE TEMP TABLE starts AS
SELECT
  id
FROM
  ways
WHERE
  tags != ''::hstore AND
  (
    (tags?'route' AND tags->'route' = 'ferry') OR
    (tags?'man_made' AND tags->'man_made' = 'pier') OR
    (tags?'aeroway' AND tags->'aeroway' IN ('taxiway', 'runway', 'apron')) OR
    (tags?'railway' AND tags->'railway' = 'platform') OR
    (tags?'public_transport' AND tags->'public_transport' = 'platform') OR
    (tags?'highway' AND tags->'highway' IN ('motorway', 'motorway_link', 'trunk', 'trunk_link', 'primary', 'primary_link'))
  )
"""

sql11 = """
CREATE TEMP TABLE islands AS
WITH RECURSIVE t AS (
  SELECT
    id
  FROM
    starts
UNION
  SELECT
    highways.id
  FROM
    t
    JOIN ways AS t_ways ON
      t_ways.id = t.id
    JOIN highways ON
      highways.id != t.id AND
      highways.linestring && t_ways.linestring AND
      highways.nodes && t_ways.nodes
)
SELECT
  *
FROM
  t
"""

sql12 = """
SELECT
  highways.id,
  ST_AsText(way_locate(highways.linestring))
FROM
  highways
  LEFT JOIN islands ON
    islands.id = highways.id
WHERE
  highways.level IS NOT NULL AND
  islands.id IS NULL
"""

class Analyser_Osmosis_Highway_Floating_Islands(Analyser_Osmosis):

    requires_tables_common = ['highways']

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs[4] = {"item":"1210", "level": 1, "tag": ["highway"], "desc": T_(u"Small highway group apart from the main network or with insufficient access upstream") }
        self.callback10 = lambda res: {"class":4, "subclass":1, "data":[self.way_full, self.positionAsText]}

    def analyser_osmosis_common(self):
        self.run(sql10)
        self.run(sql11)
        self.run(sql12, self.callback10)
