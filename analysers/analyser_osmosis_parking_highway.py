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
CREATE TEMP TABLE park_highway AS
SELECT
  id,
  linestring
FROM
  highways
WHERE
  highway NOT IN ('footway', 'cycleway', 'steps', 'platform')
"""

sql11= """
CREATE INDEX park_highway_linestring_idx ON park_highway USING gist(linestring)
"""

sql12 = """
SELECT
  pr.id,
  ST_AsText(ST_Centroid(pr.linestring)),
  pr.tags->'park_ride' != 'no'
FROM
  ways AS pr
  LEFT JOIN park_highway as highway ON
    ST_Intersects(pr.linestring, highway.linestring)
WHERE
  ST_NPoints(pr.linestring) >= 2 AND
  pr.tags != ''::hstore AND
  pr.tags?'amenity' AND
  pr.tags->'amenity' = 'parking' AND
  highway.id IS NULL
"""

class Analyser_Osmosis_Parking_highway(Analyser_Osmosis):

    requires_tables_common = ['highways']

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs[1] = {"item":"3161", "level": 1, "tag": ["highway", "fix:chair"], "desc": T_(u"Missing access to parking") }
        self.classs[2] = {"item":"3161", "level": 3, "tag": ["highway", "fix:chair"], "desc": T_(u"Missing access to parking") }

    def analyser_osmosis_common(self):
        self.run(sql10.format(""))
        self.run(sql11.format(""))
        self.run(sql12, lambda res: {
            "class": 1 if res[2] else 2,
            "data": [self.way_full, self.positionAsText]})
