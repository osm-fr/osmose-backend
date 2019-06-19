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

from .Analyser_Osmosis import Analyser_Osmosis

sql10 = """
SELECT
  highways.id,
  ST_AsText(nodes.geom)
FROM
  {0}highways AS motorways
  JOIN {1}highways AS highways ON
    highways.linestring && motorways.linestring AND
    highways.nodes && motorways.nodes AND
    highways.highway NOT IN ('motorway', 'motorway_link', 'trunk', 'trunk_link', 'primary', 'primary_link', 'escape') AND
    NOT(highways.tags?'access' AND highways.tags->'access' IN ('no', 'private', 'emergency')) AND
    NOT(highways.highway = 'service' AND highways.tags->'service' = 'emergency_access') AND
    NOT highways.is_construction
  JOIN nodes ON
    nodes.id = (SELECT * FROM (SELECT unnest(highways.nodes) INTERSECT SELECT unnest(motorways.nodes)) AS t LIMIT 1)
WHERE
  motorways.highway = 'motorway'
"""

class Analyser_Osmosis_Highway_Motorway(Analyser_Osmosis):

    requires_tables_full = ['highways']
    requires_tables_diff = ['highways', 'touched_highways', 'not_touched_highways']

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs_change[1] = {"item": 3220, "level": 1, "tag": ["tag", "highway", "fix:chair"], "desc": T_(u"Direct or too permissive access to motorway") }
        self.callback10 = lambda res: {"class":1, "data":[self.way_full, self.positionAsText]}

    def analyser_osmosis_full(self):
        self.run(sql10.format("", ""), self.callback10)

    def analyser_osmosis_diff(self):
        self.run(sql10.format("touched_", "not_touched_"), self.callback10)
        self.run(sql10.format("", "touched_"), self.callback10)
