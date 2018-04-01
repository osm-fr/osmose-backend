#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights                        ##
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
    ways3.id,
    ST_AsText(ST_Centroid(ways3.linestring))
FROM
    {0}buildings AS buildings
    JOIN {1}buildings AS ways3 ON
        ST_Intersects(buildings.polygon_proj, ways3.polygon_proj) AND
        ways3.id != buildings.id AND
        ways3.wall = buildings.wall
WHERE
    ways3.npoints = 3
GROUP BY
    ways3.id,
    ways3.linestring
"""


class Analyser_Osmosis_Building_3nodes(Analyser_Osmosis):

    requires_tables_full = ['buildings']
    requires_tables_diff = ['buildings', 'touched_buildings', 'not_touched_buildings']

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs_change[1] = {"item":"1", "level": 3, "tag": ["building", "fix:imagery"], "desc": T_(u"Merge building (triangle)") }
        self.callback70 = lambda res: {"class":1, "data":[self.way_full, self.positionAsText]}

    def analyser_osmosis_full(self):
        self.run(sql10.format("", ""), self.callback70)

    def analyser_osmosis_diff(self):
        self.run(sql10.format("touched_", ""), self.callback70)
        self.run(sql10.format("not_touched_", "touched_"), self.callback70)
