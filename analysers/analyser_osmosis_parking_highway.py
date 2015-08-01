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

from Analyser_Osmosis import Analyser_Osmosis

sql10 = """
SELECT
  pr.id,
  ST_AsText(ST_Centroid(pr.linestring)),
  pr.tags->'park_ride' != 'no'
FROM
  ways AS pr
  LEFT JOIN ways as highway ON
    highway.tags?'highway' AND
    ST_NPoints(highway.linestring) >= 2 AND
    ST_Intersects(pr.linestring, highway.linestring)
WHERE
  ST_NPoints(pr.linestring) >= 2 AND
  pr.tags?'amenity' AND
  pr.tags->'amenity' = 'parking' AND
  highway.id IS NULL
"""

class Analyser_Osmosis_Parking_highway(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs[1] = {"item":"7180", "level": 1, "tag": ["highway", "fix:chair"], "desc": T_(u"Missing acces highway") }
        self.classs[2] = {"item":"7180", "level": 3, "tag": ["highway", "fix:chair"], "desc": T_(u"Missing acces highway") }

    def analyser_osmosis(self):
        self.run(sql10, lambda res: {
            "class": 1 if res[2] else 2,
            "data": [self.way_full, self.positionAsText]})
