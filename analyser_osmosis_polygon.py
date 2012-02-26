#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2011                                      ##
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
    id,
    ST_AsText(selfinter)
FROM
(
    SELECT
        id,
        ST_Difference(
          ST_Endpoint(
            ST_Union(
              ST_Exteriorring(polygon),
              ST_Endpoint(st_exteriorring(polygon))
            )
          ),
          ST_Endpoint(ST_Exteriorring(polygon))
        ) AS selfinter
      FROM
        (
            SELECT
                id,
                ST_MakePolygon(linestring) AS polygon
            FROM
                {0}ways AS ways
            WHERE
                is_polygon
        ) AS p
    WHERE
        NOT ST_IsValid(polygon)
) AS tmp
WHERE NOT ST_IsEmpty(selfinter)
"""

class Analyser_Osmosis_Polygon(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs_change[1] = {"item":"1040", "desc":{"fr":"Polygone invalide", "en":"Invalid polygon"} }
        self.callback10 = lambda res: {"class":1, "data":[self.way_full, self.positionAsText]}

    def analyser_osmosis_all(self):
        self.run(sql10.format(""), self.callback10)

    def analyser_osmosis_touched(self):
        self.run(sql10.format("touched_"), self.callback10)
