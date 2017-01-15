#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2012                                      ##
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
    ST_AsText(way_locate(linestring))
FROM
    {1}ways AS ways
WHERE
    is_polygon AND
    tags?'landuse' AND
    tags->'landuse' IN ('farm', 'farmland') AND
    ST_Area(ST_Transform(ST_MakePolygon(linestring), {0})) < 5000
"""

class Analyser_Osmosis_Mini_Farm(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        if "proj" in self.config.options:
            self.classs_change[1] = {"item":"3100", "level": 2, "tag": ["tag", "landuse", "fix:imagery"], "desc": T_(u"Small farm : consider farmyard or building instead") }
            self.callback10 = lambda res: {"class":1, "data":[self.way_full, self.positionAsText], "fix":[
                {"-":["landuse"], "+":{"building":"yes"}},
                {"-":["landuse"], "+":{"building":"farm_auxiliary"}},
                {"-":["landuse"], "+":{"building":"farm"}},
                {"-":["landuse"], "+":{"building":"farmhouse"}},
                {"landuse":"farmyard"},
                {"landuse":"farmland"},
                {"landuse":"allotments"},
                ]}

    def analyser_osmosis_full(self):
        if "proj" in self.config.options:
            self.run(sql10.format(self.config.options.get("proj"), ""), self.callback10)

    def analyser_osmosis_diff(self):
        if "proj" in self.config.options:
            self.run(sql10.format(self.config.options.get("proj"), "touched_"), self.callback10)
