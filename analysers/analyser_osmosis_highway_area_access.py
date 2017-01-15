#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo <@free.fr> 2016                           ##
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
SELECT
  nodes.id,
  ways.id,
  ST_AsText(nodes.geom),
  nodes.tags->'motor_vehicle' AS node_motor_vehicle,
  ways.tags->'motor_vehicle' AS way_motor_vehicle
FROM
  {0}nodes AS nodes
  JOIN way_nodes ON
    way_nodes.node_id = nodes.id
  JOIN {1}highways AS ways ON
    ways.id = way_nodes.way_id AND
    ways.highway = 'pedestrian' AND
    (NOT ways.tags?'area' OR ways.tags->'area'='no')
WHERE
  nodes.tags != ''::hstore AND
  nodes.tags?'barrier' AND
  nodes.tags->'barrier' = 'bollard' AND
  (NOT ways.tags?'motor_vehicle' OR ways.tags->'motor_vehicle' != 'no') AND
  (
    (ways.tags?'motor_vehicle' AND NOT nodes.tags?'motor_vehicle') OR
    (NOT ways.tags?'motor_vehicle' AND nodes.tags?'motor_vehicle') OR
    (ways.tags?'motor_vehicle' AND nodes.tags?'motor_vehicle' AND (ways.tags->'motor_vehicle') != (nodes.tags->'motor_vehicle'))
  )
"""


class Analyser_Osmosis_HighwayAreaAccess(Analyser_Osmosis):

    requires_tables_full = ['highways']
    requires_tables_diff = ['highways', 'touched_highways', 'not_touched_highways']

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs_change[1] = {"item":"2130", "level": 3, "tag": ["highway", "routing"], "desc": T_(u"Inconsistent Access") }
        self.callback10 = lambda res: {"class":1, "data":[self.node_full, self.way_full, self.positionAsText],
            "text": T_(u"Inconsistent motor_vehicle values ('%s'!='%s')", res[3] if res[3] else '', res[4] if res[4] else '') }

    def analyser_osmosis_full(self):
        self.run(sql10.format("", ""), self.callback10)

    def analyser_osmosis_diff(self):
        self.run(sql10.format("touched_", "not_touched_"), self.callback10)
        self.run(sql10.format("", "touched_"), self.callback10)
