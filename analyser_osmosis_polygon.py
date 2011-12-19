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
    SELECT ways.id,
        st_difference(
          st_endpoint(
            st_union(
              st_exteriorring(linestring),
              st_endpoint(st_exteriorring(linestring))
            )
          ),
          st_endpoint(st_exteriorring(linestring))
        ) AS selfinter
      FROM ways
      WHERE is_polygon AND NOT st_isvalid(linestring)
) AS tmp
WHERE NOT st_isempty(selfinter)
"""

class Analyser_Osmosis_Polygon(Analyser_Osmosis):

    def __init__(self, father):
        Analyser_Osmosis.__init__(self, father)
        self.classs[1] = {"item":"1040", "desc":{"fr":"Polygone invalide", "en":"Invalid polygon"} }

    def analyser_osmosis(config, logger, giscurs):
        self.run(sql10, lambda res: {"class":1, "data":[self.way_full, self.positionAsText]} )
