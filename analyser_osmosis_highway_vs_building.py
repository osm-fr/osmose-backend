#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Etienne Chové <chove@crans.org> 2010                       ##
##            Frédéric Rodrigo <****@free.fr> 2011                       ##
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
    buildings.id,
    highways.id,
    ST_AsText(ST_Centroid(buildings.linestring))
FROM
    {0}ways AS buildings,
    {1}ways AS highways
WHERE
    highways.tags?'highway' AND
    highways.tags->'highway' IN ('primary', 'secondary', 'tertiary') AND
    NOT highways.tags ? 'tunnel' AND
    NOT highways.tags ? 'bridge' AND
    buildings.tags?'building' = 'yes' AND
    NOT buildings.tags?'wall' AND
    ST_Intersects(buildings.linestring, highways.linestring)
;
"""

class Analyser_Osmosis_Highway_VS_Building(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs_change[1] = {"item":"1070", "desc":{"fr":"Intersection entre une voie et un bâtiment", "en":"Way intersecting building"} }
        self.callback10 = lambda res: {"class":1, "data":[self.way_full, self.way_full, self.positionAsText]}

    def analyser_osmosis_all(self):
        self.run(sql10.format("", ""), self.callback10)

    def analyser_osmosis_touched(self):
        dup = set()
        self.run(sql10.format("touched_", ""), lambda res: dup.add(res[0]) or self.callback10(res))
        self.run(sql10.format("", "touched_"), lambda res: res[0] in dup or dup.add(res[0]) or self.callback10(res))
