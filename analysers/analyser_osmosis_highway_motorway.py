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
SELECT
  service.id,
  ST_AsText(way_locate(service.linestring))
FROM
  (
  SELECT * FROM {0}ways AS motorway WHERE
  motorway.tags != ''::hstore AND
  motorway.tags?'highway' AND
  motorway.tags->'highway' = 'motorway'
  ) AS motorway
  JOIN {1}ways AS service ON
    motorway.linestring && service.linestring AND
    motorway.nodes && service.nodes
WHERE
  service.tags != ''::hstore AND
  service.tags?'highway' AND
  service.tags->'highway' NOT IN ('motorway', 'motorway_link', 'trunk', 'trunk_link', 'primary', 'primary_link', 'secondary', 'secondary_link', 'tertiary', 'tertiary_link', 'escape', 'proposed', 'construction', 'disused', 'rest_area', 'services') AND
  service.tags->'access' NOT IN ('no', 'emergency') AND
  NOT (
    service.tags->'highway' = 'service' AND
    service.tags->'service' = 'emergency_access'
  )
"""

class Analyser_Osmosis_Highway_Motorway(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs_change[1] = {"item": 3220, "level": 1, "tag": ["tag", "highway", "fix:chair"], "desc": T_(u"Too permissive access to motorway") }
        self.callback10 = lambda res: {"class":1, "data":[self.way_full, self.positionAsText]}

    def analyser_osmosis_all(self):
        self.run(sql10.format("", ""), self.callback10)

    def analyser_osmosis_touched(self):
        self.run(sql10.format("touched_", ""), self.callback10)
        self.run(sql10.format("", "touched_"), self.callback10)
        self.run(sql10.format("touched_", "touched_"), self.callback10)
